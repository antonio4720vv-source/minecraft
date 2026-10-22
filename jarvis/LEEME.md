# JARVIS con Gemini (gratis)

Asistente por voz: le hablás ("Jarvis, ¿cuánto mide la Luna?", "Jarvis, prendé la luz") y te contesta en voz alta.
Usa **Gemini** (plan gratuito de Google AI Studio) para responder de todo y herramientas propias para:
prender/apagar la luz, decir la hora, abrir páginas, buscar en YouTube y abrir programas (incluido el servidor de Minecraft).

## Instalación (Windows)
1. Instalá **Python 3.11 o más nuevo** desde python.org (tildá "Add Python to PATH").
2. Sacá tu clave gratis en https://aistudio.google.com/apikey.
3. Doble clic en `INICIAR_JARVIS.bat`. La primera vez instala todo y abre el `.env`: pegá la clave en `GEMINI_API_KEY`, guardá y volvé a abrir el `.bat`.
4. Decí **"Jarvis"** + lo que quieras. "Jarvis apagate" lo cierra.

Sin micrófono: `INICIAR_JARVIS.bat --texto` para escribirle.

Si la voz sale en inglés: Configuración de Windows → Hora e idioma → Voz → agregar una voz en español.

## La luz
Por defecto está en `LUZ_TIPO=simulado` (solo muestra el mensaje). Para una luz real necesitás algo inteligente:

### Opción A: foco o enchufe Wi-Fi Tuya / Smart Life (los más baratos)
1. Configuralo en la app **Smart Life** o **Tuya**.
2. Para sacar `TUYA_ID`, `TUYA_IP` y `TUYA_LOCAL_KEY` ejecutá `.venv\Scripts\python -m tinytuya wizard` y seguí los pasos (pide crear una cuenta gratis en iot.tuya.com y vincular la app). Guía: https://github.com/jasonacox/tinytuya#setup-wizard---getting-local-keys
3. En el `.env`: `LUZ_TIPO=tuya`. Si es un foco y no responde, probá `TUYA_DPS=20` y `TUYA_VERSION=3.4` o `3.5`.

### Opción B: Home Assistant
`LUZ_TIPO=homeassistant`, la URL, un token de larga duración (Perfil → Seguridad) y la entidad (ej. `light.habitacion` o `switch.lampara`).

## Límites
- El plan gratis de Gemini tiene un tope de pedidos por minuto y por día; para uso personal sobra.
- El reconocimiento de voz usa el servicio gratis de Google: necesita internet.
- Para agregar otra habilidad: escribí una función con docstring en `jarvis.py` y sumala a `HERRAMIENTAS`.
