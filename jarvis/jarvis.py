"""JARVIS: asistente por voz o texto con Gemini (gratis) que también prende y apaga luces.

Uso:
    python jarvis.py          -> ventana con el círculo animado + voz (decí "Jarvis, ...")
    python jarvis.py --texto  -> modo texto (escribís en la consola)
"""
import datetime
import math
import os
import queue
import subprocess
import sys
import threading
import urllib.parse
import webbrowser

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODELO = os.getenv("GEMINI_MODELO", "gemini-2.5-flash")
LUZ_TIPO = os.getenv("LUZ_TIPO", "simulado").lower()  # simulado | tuya | homeassistant
PALABRA_CLAVE = os.getenv("PALABRA_CLAVE", "jarvis").lower()


# ---------------------------------------------------------------- luces

def _luz_tuya(encender: bool) -> str:
    import tinytuya

    disp = tinytuya.OutletDevice(
        os.getenv("TUYA_ID"), os.getenv("TUYA_IP"), os.getenv("TUYA_LOCAL_KEY")
    )
    disp.set_version(float(os.getenv("TUYA_VERSION", "3.3")))
    resp = disp.set_status(encender, switch=int(os.getenv("TUYA_DPS", "1")))
    if isinstance(resp, dict) and "Error" in resp:
        raise RuntimeError(resp["Error"])
    return "ok"


def _luz_homeassistant(encender: bool) -> str:
    import requests

    servicio = "turn_on" if encender else "turn_off"
    r = requests.post(
        f"{os.getenv('HA_URL', '').rstrip('/')}/api/services/homeassistant/{servicio}",
        headers={"Authorization": f"Bearer {os.getenv('HA_TOKEN')}"},
        json={"entity_id": os.getenv("HA_ENTIDAD")},
        timeout=10,
    )
    r.raise_for_status()
    return "ok"


def controlar_luz(encender: bool) -> str:
    """Prende o apaga la luz de la habitación del usuario.

    Args:
        encender: True para prender la luz, False para apagarla.
    """
    estado = "prendida" if encender else "apagada"
    try:
        if LUZ_TIPO == "tuya":
            _luz_tuya(encender)
        elif LUZ_TIPO == "homeassistant":
            _luz_homeassistant(encender)
        else:
            print(f"   [simulado] la luz quedaría {estado}")
        return f"Luz {estado}."
    except Exception as e:  # el modelo le explica el error al usuario
        return f"No pude controlar la luz: {e}"


# ---------------------------------------------------------------- otras herramientas

def fecha_y_hora() -> str:
    """Devuelve la fecha y la hora actuales de la computadora."""
    return datetime.datetime.now().strftime("%A %d/%m/%Y, %H:%M")


def abrir_pagina(url: str) -> str:
    """Abre una página web en el navegador.

    Args:
        url: dirección completa, por ejemplo https://www.youtube.com
    """
    webbrowser.open(url)
    return f"Abrí {url}"


def buscar_en_youtube(busqueda: str) -> str:
    """Busca un video o canción en YouTube y abre los resultados.

    Args:
        busqueda: lo que hay que buscar.
    """
    webbrowser.open("https://www.youtube.com/results?search_query=" + busqueda.replace(" ", "+"))
    return f"Busqué {busqueda} en YouTube"


PROGRAMAS = {
    "bloc de notas": "notepad",
    "calculadora": "calc",
    "explorador": "explorer",
    "paint": "mspaint",
    "minecraft server": os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "ServidorMinecraft", "INICIAR_SERVIDOR.bat"
    ),
}


def abrir_programa(nombre: str) -> str:
    """Abre un programa de la computadora (Windows).

    Args:
        nombre: uno de: bloc de notas, calculadora, explorador, paint, minecraft server.
            También puede ser el nombre de un ejecutable, por ejemplo "chrome".
    """
    comando = PROGRAMAS.get(nombre.lower().strip(), nombre)
    try:
        if sys.platform == "win32":
            os.startfile(comando) if os.path.exists(comando) else subprocess.Popen(f'start "" {comando}', shell=True)
        else:
            subprocess.Popen([comando])
        return f"Abrí {nombre}"
    except Exception as e:
        return f"No pude abrir {nombre}: {e}"


CARPETA_IMAGENES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "imagenes")
eventos = queue.Queue()  # mensajes del hilo de JARVIS hacia la ventana


def generar_imagen(descripcion: str) -> str:
    """Dibuja una imagen nueva a partir de una descripción y la muestra en pantalla.

    Args:
        descripcion: qué tiene que verse en la imagen, detallado y escrito en inglés.
    """
    import requests

    try:
        url = "https://image.pollinations.ai/prompt/" + urllib.parse.quote(descripcion)
        r = requests.get(url, params={"width": 768, "height": 768, "nologo": "true"}, timeout=120)
        r.raise_for_status()
        os.makedirs(CARPETA_IMAGENES, exist_ok=True)
        ruta = os.path.join(CARPETA_IMAGENES, datetime.datetime.now().strftime("img_%Y%m%d_%H%M%S.jpg"))
        with open(ruta, "wb") as f:
            f.write(r.content)
        eventos.put(("imagen", ruta))
        if "--texto" in sys.argv:
            os.startfile(ruta) if sys.platform == "win32" else webbrowser.open(ruta)
        return f"Imagen lista y mostrada en pantalla (guardada en {ruta})."
    except Exception as e:
        return f"No pude generar la imagen: {e}"


HERRAMIENTAS = [controlar_luz, fecha_y_hora, abrir_pagina, buscar_en_youtube, abrir_programa, generar_imagen]

INSTRUCCIONES = (
    "Sos JARVIS, el asistente personal del usuario, al estilo del de Iron Man: "
    "inteligente, amable y con un toque de humor. Hablás en español. "
    "Respondé cualquier pregunta lo mejor que puedas. Tus respuestas se leen en voz alta, "
    "así que sé breve (1 a 3 oraciones) salvo que te pidan detalle, y no uses markdown, "
    "asteriscos ni listas. Cuando el usuario pida prender o apagar la luz, abrir algo o "
    "saber la hora, usá las herramientas que tenés. Si te piden un dibujo, foto o imagen, "
    "usá generar_imagen y después decí en una oración qué dibujaste."
)


# ---------------------------------------------------------------- voz

class Voz:
    def __init__(self):
        import pyttsx3
        import speech_recognition as sr

        self.sr = sr
        self.rec = sr.Recognizer()
        self.mic = sr.Microphone()
        self.tts = pyttsx3.init()
        for v in self.tts.getProperty("voices"):
            if "spanish" in v.name.lower() or "es" in str(v.languages).lower() or "es-" in v.id.lower():
                self.tts.setProperty("voice", v.id)
                break
        self.tts.setProperty("rate", 180)
        with self.mic as fuente:
            print("Calibrando el micrófono, silencio un segundo...")
            self.rec.adjust_for_ambient_noise(fuente, duration=1)

    def decir(self, texto: str):
        print(f"JARVIS: {texto}")
        eventos.put(("jarvis", texto))
        eventos.put(("estado", "hablando"))
        self.tts.say(texto)
        self.tts.runAndWait()
        eventos.put(("estado", "esperando"))

    def escuchar(self) -> str:
        eventos.put(("estado", "esperando"))
        with self.mic as fuente:
            try:
                audio = self.rec.listen(fuente, timeout=None, phrase_time_limit=10)
            except self.sr.WaitTimeoutError:
                return ""
        try:
            return self.rec.recognize_google(audio, language="es-AR")
        except (self.sr.UnknownValueError, self.sr.RequestError):
            return ""


# ---------------------------------------------------------------- ventana

COLORES = {"esperando": "#00b4ff", "escuchando": "#00ffd0", "pensando": "#ffb000", "hablando": "#00e5ff"}


class Ventana:
    def __init__(self):
        import tkinter as tk

        self.tk = tk
        self.raiz = tk.Tk()
        self.raiz.title("J.A.R.V.I.S.")
        self.raiz.configure(bg="#05080f")
        self.raiz.geometry("900x620")
        self.estado = "esperando"
        self.paso = 0
        self.foto = None

        izq = tk.Frame(self.raiz, bg="#05080f")
        izq.pack(side="left", fill="both", expand=True)
        self.lienzo = tk.Canvas(izq, width=380, height=380, bg="#05080f", highlightthickness=0)
        self.lienzo.pack(pady=(20, 0))
        self.lbl_estado = tk.Label(izq, text="", fg="#00b4ff", bg="#05080f", font=("Consolas", 14, "bold"))
        self.lbl_estado.pack()
        self.lbl_vos = tk.Label(izq, text="", fg="#7f8fa6", bg="#05080f", font=("Segoe UI", 11),
                                wraplength=400, justify="center")
        self.lbl_vos.pack(pady=(14, 4))
        self.lbl_jarvis = tk.Label(izq, text="", fg="#e8f6ff", bg="#05080f", font=("Segoe UI", 13),
                                   wraplength=400, justify="center")
        self.lbl_jarvis.pack(padx=10)

        self.lbl_imagen = tk.Label(self.raiz, bg="#05080f", fg="#33455c", font=("Segoe UI", 11),
                                   text="Pedime una imagen:\n\"Jarvis, dibujá un dragón en la luna\"")
        self.lbl_imagen.pack(side="right", padx=20, pady=20)

        self.animar()
        self.revisar_eventos()

    def animar(self):
        c, color = self.lienzo, COLORES.get(self.estado, "#00b4ff")
        c.delete("all")
        cx = cy = 190
        self.paso += 1
        rapidez = {"hablando": 0.35, "pensando": 0.25, "escuchando": 0.18}.get(self.estado, 0.07)
        pulso = math.sin(self.paso * rapidez) * (14 if self.estado == "hablando" else 5)
        for i, r in enumerate((150, 125, 100)):
            inicio = (self.paso * (3 + i * 2) * (-1 if i % 2 else 1)) % 360
            for k in range(3):
                c.create_arc(cx - r, cy - r, cx + r, cy + r, start=inicio + k * 120, extent=80,
                             style="arc", outline=color, width=3 - i * 0.5)
        r = 60 + pulso
        c.create_oval(cx - r, cy - r, cx + r, cy + r, outline=color, width=2)
        c.create_oval(cx - 40, cy - 40, cx + 40, cy + 40, fill="#0a1a2a", outline=color, width=4)
        c.create_text(cx, cy, text="J.A.R.V.I.S.", fill=color, font=("Consolas", 11, "bold"))
        self.raiz.after(33, self.animar)

    def revisar_eventos(self):
        try:
            while True:
                tipo, dato = eventos.get_nowait()
                if tipo == "estado":
                    self.estado = dato
                    self.lbl_estado.config(text=dato.upper(), fg=COLORES.get(dato, "#00b4ff"))
                elif tipo == "vos":
                    self.lbl_vos.config(text=f"Vos: {dato}")
                elif tipo == "jarvis":
                    self.lbl_jarvis.config(text=dato)
                elif tipo == "imagen":
                    self.mostrar_imagen(dato)
                elif tipo == "salir":
                    self.raiz.destroy()
                    return
        except queue.Empty:
            pass
        self.raiz.after(100, self.revisar_eventos)

    def mostrar_imagen(self, ruta):
        from PIL import Image, ImageTk

        img = Image.open(ruta)
        img.thumbnail((440, 440))
        self.foto = ImageTk.PhotoImage(img)
        self.lbl_imagen.config(image=self.foto, text="")


# ---------------------------------------------------------------- principal

def crear_chat():
    cliente = genai.Client(api_key=GEMINI_API_KEY)
    chat = cliente.chats.create(
        model=MODELO,
        config=types.GenerateContentConfig(system_instruction=INSTRUCCIONES, tools=HERRAMIENTAS),
    )

    def preguntar(texto: str) -> str:
        eventos.put(("estado", "pensando"))
        try:
            return (chat.send_message(texto).text or "Listo.").replace("*", "")
        except Exception as e:
            return f"Tuve un problema hablando con Gemini: {e}"

    return preguntar


def bucle_voz(preguntar):
    try:
        voz = Voz()
    except Exception as e:
        eventos.put(("jarvis", f"No encontré el micrófono: {e}. Abrí JARVIS con --texto."))
        return
    voz.decir(f"Sistemas en línea. Decí {PALABRA_CLAVE} y lo que necesites.")
    while True:
        oido = voz.escuchar()
        if not oido:
            continue
        print(f"Vos: {oido}")
        minus = oido.lower()
        if PALABRA_CLAVE not in minus:
            continue
        eventos.put(("vos", oido))
        pedido = minus.split(PALABRA_CLAVE, 1)[1].strip(" ,.")
        if pedido in ("apagate", "apágate", "desconectate", "salir"):
            voz.decir("Hasta luego.")
            eventos.put(("salir", None))
            break
        if not pedido:
            voz.decir("¿Sí?")
            pedido = voz.escuchar()
            if not pedido:
                continue
            print(f"Vos: {pedido}")
            eventos.put(("vos", pedido))
        voz.decir(preguntar(pedido))


def main():
    if not GEMINI_API_KEY:
        sys.exit("Falta GEMINI_API_KEY en el archivo .env (sacala gratis en https://aistudio.google.com/apikey)")

    preguntar = crear_chat()

    if "--texto" in sys.argv:
        print("JARVIS en modo texto. Escribí 'salir' para terminar.")
        while True:
            texto = input("Vos: ").strip()
            if texto.lower() in ("salir", "chau", "exit"):
                break
            if texto:
                print("JARVIS:", preguntar(texto))
        return

    ventana = Ventana()
    threading.Thread(target=bucle_voz, args=(preguntar,), daemon=True).start()
    ventana.raiz.mainloop()


if __name__ == "__main__":
    main()
