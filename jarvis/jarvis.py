"""JARVIS: asistente por voz o texto con Gemini (gratis) que también prende y apaga luces.

Uso:
    python jarvis.py          -> modo voz (decí "Jarvis, ..." )
    python jarvis.py --texto  -> modo texto (escribís en la consola)
"""
import datetime
import os
import subprocess
import sys
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


HERRAMIENTAS = [controlar_luz, fecha_y_hora, abrir_pagina, buscar_en_youtube, abrir_programa]

INSTRUCCIONES = (
    "Sos JARVIS, el asistente personal del usuario, al estilo del de Iron Man: "
    "inteligente, amable y con un toque de humor. Hablás en español. "
    "Respondé cualquier pregunta lo mejor que puedas. Tus respuestas se leen en voz alta, "
    "así que sé breve (1 a 3 oraciones) salvo que te pidan detalle, y no uses markdown, "
    "asteriscos ni listas. Cuando el usuario pida prender o apagar la luz, abrir algo o "
    "saber la hora, usá las herramientas que tenés."
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
        self.tts.say(texto)
        self.tts.runAndWait()

    def escuchar(self) -> str:
        with self.mic as fuente:
            try:
                audio = self.rec.listen(fuente, timeout=None, phrase_time_limit=10)
            except self.sr.WaitTimeoutError:
                return ""
        try:
            return self.rec.recognize_google(audio, language="es-AR")
        except (self.sr.UnknownValueError, self.sr.RequestError):
            return ""


# ---------------------------------------------------------------- principal

def main():
    if not GEMINI_API_KEY:
        sys.exit("Falta GEMINI_API_KEY en el archivo .env (sacala gratis en https://aistudio.google.com/apikey)")

    cliente = genai.Client(api_key=GEMINI_API_KEY)
    chat = cliente.chats.create(
        model=MODELO,
        config=types.GenerateContentConfig(system_instruction=INSTRUCCIONES, tools=HERRAMIENTAS),
    )

    def preguntar(texto: str) -> str:
        try:
            return (chat.send_message(texto).text or "Listo.").replace("*", "")
        except Exception as e:
            return f"Tuve un problema hablando con Gemini: {e}"

    if "--texto" in sys.argv:
        print("JARVIS en modo texto. Escribí 'salir' para terminar.")
        while True:
            texto = input("Vos: ").strip()
            if texto.lower() in ("salir", "chau", "exit"):
                break
            if texto:
                print("JARVIS:", preguntar(texto))
        return

    voz = Voz()
    voz.decir(f"Sistemas en línea. Decí {PALABRA_CLAVE} y lo que necesites.")
    while True:
        oido = voz.escuchar()
        if not oido:
            continue
        print(f"Vos: {oido}")
        minus = oido.lower()
        if PALABRA_CLAVE not in minus:
            continue
        pedido = minus.split(PALABRA_CLAVE, 1)[1].strip(" ,.")
        if pedido in ("apagate", "apágate", "desconectate", "salir"):
            voz.decir("Hasta luego.")
            break
        if not pedido:
            voz.decir("¿Sí?")
            pedido = voz.escuchar()
            if not pedido:
                continue
            print(f"Vos: {pedido}")
        voz.decir(preguntar(pedido))


if __name__ == "__main__":
    main()
