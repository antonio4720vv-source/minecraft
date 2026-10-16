# Servidor de Minecraft casero (Java + Bedrock) — contexto para Claude Code

## Qué es
Servidor de Minecraft para jugar con amigos, en mi PC con Windows. Se juega desde PC (Java) y desde celular (Bedrock).
- Carpeta: `C:\Users\User\Downloads\ServidorMinecraft_Java_Bedrock\ServidorMinecraft`
- **Paper 26.2** (fijado a propósito: en 26.3 el plugin Geyser fallaba con `Couldn't find asBukkitCopy`).
- Java portable **Temurin JDK 25** dentro de la carpeta `java\`, porque Minecraft 26.x pide Java 25.
- Se juega por internet con **playit.gg** (túnel). Mi red tuvo problemas de DNS y los cambié a 8.8.8.8 / 1.1.1.1.

## Arranque
- `INICIAR_SERVIDOR.bat` → ejecuta `iniciar.ps1` (PowerShell con `-ExecutionPolicy Bypass`).
- `iniciar.ps1`:
  - Configuración: `$RAM="4G"`, `$VERSION="26.2"`.
  - Si falta Java, lo descarga de api.adoptium.net. Si falta paper.jar, lo descarga de Fill v3 (`https://fill.papermc.io/v3/projects/paper/versions/{v}/builds`, canal STABLE, `downloads."server:default".url`).
  - Descarga los plugins de download.geysermc.org y de la API de Modrinth. Si una descarga falla, no detiene el arranque.
  - Si `version.txt` no coincide con la versión, borra paper.jar. Si se baja de versión, mueve `world*` a `mundo_respaldo_<ver>`. Hay una copia vieja así: `mundo_respaldo_26.3`, que no se puede abrir en 26.2.
  - Inicia con `-Xms2G -Xmx$RAM -XX:+UseG1GC ... -jar paper.jar --nogui`.
- Plugins: **Geyser-Spigot** (Bedrock, UDP 19132), **Floodgate**, **ViaVersion** y **ViaBackwards** (permiten clientes más viejos; yo juego en 1.21.11).
- `server.properties`:
  - `online-mode=false` y `enforce-secure-profile=false` (no premium)
  - `difficulty=hard`, `gamemode=survival`, `max-players=10`, `spawn-protection=0`, `allow-flight=true`
  - Quizá bajé `view-distance` a 6 y `simulation-distance` a 5 por lag del celular.
- Los jugadores de Bedrock aparecen con un **punto adelante** en el nombre (ej. `.Juan123`).
- Para dar op: escribir `op Nombre` en la consola.

## Datapack de granjas (lo principal)
- Archivo: `world\datapacks\granjas_datapack.zip`. Namespace `granjas`. Funciones en `data/granjas/function/*.mcfunction`.
- `pack.mcmeta`: `min_format 88`, `max_format 999`. Se recarga escribiendo `reload` en la consola.
- Lo genera un script en Python (ver más abajo). Ojo: un solo error de sintaxis en una función hace que Minecraft la rechace entera y salga "función desconocida". Ya pasó por un salto de línea mal escapado dentro de un texto.

### Convenciones internas
- Cada estructura es una función interna `_nombre` que construye relativa a `~ ~ ~`. La versión pública `nombre` hace `execute align xyz positioned ~0.5 ~ ~0.5 run function granjas:_nombre`.
- Coordenadas locales (x, y, z): **y=0 es el bloque del suelo** (en el archivo queda como `~-1`). El jugador está parado en y=1. Las estructuras crecen hacia **+x (este) y +z (sur)**.
- Límite de `fill`: 32 768 bloques por comando. Los rellenos grandes van partidos en pedazos.
- Formato de 1.21.5+:
  - Textos en SNBT: `text:{text:"..."}`.
  - Ítems con `{id:"minecraft:x",count:N}`.
  - Equipo con `equipment:{head:...}` y `drop_chances`. Silla de caballo en `equipment:{saddle:...}`.
- Todos los contenedores de salida son **barriles**, no cofres: un cofre no se abre si tiene un bloque encima.
- Etiquetas flotantes: `text_display` con `billboard:"center"`.

### Megabase v7 (la que está en uso)
- `/function granjas:megabase`: crea una megabase nueva en la posición del jugador.
- `/function granjas:rehacer_megabase`: borra y reconstruye en el mismo lugar, usando un marker `tag=granjas_mega`.
- Cómo se construye:
  - Zona de x −115..115, z −150..115 (relativa al marker). Se forzó la carga con 2 comandos `forceload`.
  - Va por etapas con `schedule` (`_mega1` … `_mega11`). Cada etapa hace `execute at <marker>`.
- Qué hay (coordenadas relativas al marker):
  - **Centro:** fuente con beacon (`_fuente`), con la plaza pavimentada en r=14.
  - **(28,−25):** portal del End decorado (`_portal_end`), con portal activo.
  - **Edificio de granjas** (`_edif_a` y `_edif_b`), origen (−26,−70). Mide 52×28 y tiene 6 pisos con base en y = 0 / 8 / 18 / 25 / 33 / 51 y techo en 73:
    - Piso 0: 3 hornos.
    - Piso 1: 3 de caña, 2 de sandía y 1 de comida.
    - Piso 2: 2 criaderos de aldeanos.
    - Piso 3: 1 sala de comercio.
    - Piso 4: 2 granjas de hierro (piso de vidrio para que los gólems no aparezcan afuera).
    - Piso 5: 1 granja de experiencia (spawner de zombis).
    - Escaleras en zigzag por el lado oeste, en 2 carriles. Entrada principal al sur.
  - **(−78,−55):** granja de mobs (torre de 28 de alto, caída de 24).
  - **(−72,−12):** caballeriza.
  - **(−60,70):** montaña (`_montana`) con la casa grande arriba (`_casa_grande`, para 2 personas).
  - **(−18,45):** animales.
  - **(10,45):** cuarto de cofres (12 categorías con marcos de ítem).
  - **(52,48):** torre de élitros (60 bloques, ascensor de burbujas con arena de almas).
  - **(65,0):** casa en el árbol (ascensor de burbujas y escalera de mano).
  - **Tren** (`_tren`): circuito rectangular x ±45, z ±40.
    - Riel propulsor encendido cada 8 bloques, sobre bloque de redstone.
    - 10 estaciones: 2 rieles propulsores apagados (frenan); un botón encima de un bloque al lado los enciende; un barril con vagonetas.
  - Además:
    - `_paisaje`: 10 colinas alrededor.
    - `_arboles`: árboles y flores con `place feature`.
    - 12 gólems de hierro `PlayerCreated`.
    - Bloques `light` invisibles cada 8 bloques en y=1 (para que no aparezcan monstruos).

### Producción asegurada ("respaldo")
- Cada granja crea un `marker` con un tag `go_*` en su barril de salida (`go_hierro`, `go_cana`, `go_comida`, `go_sandia`, `go_mobs`, `go_xp`, `go_xpbarril`, `go_bebes`).
- `granjas:producir` se repite cada 30 s con `schedule`. Si `#on granjas` vale 1, mete botín con `loot insert` en esos barriles, da XP a quien esté cerca de `go_xp` y genera aldeanos bebé en `go_bebes`.
- Se activa con `granjas:respaldo_on` y se apaga con `granjas:respaldo_off`.
- **Motivo:** nunca pude probar las granjas en un servidor real, así que la mecánica normal (redstone, gólems, etc.) puede fallar; el respaldo garantiza que produzcan.

### Otros comandos
- `granjas:lista` muestra todos los comandos en el chat.
- Estructuras sueltas, que se construyen donde está el jugador: `hierro`, `experiencia`, `aldeanos`, `comercio`, `cana`, `comida`, `sandia`, `hornos`, `mobs`, `animales`, `casa`, `casa_grande`, `montana`, `portal_end`, `cofres`, `torre_elitros`, `caballeriza`, `arbol`, `fuente`, `edificio_granjas`.
- `quitar_carga` hace `forceload remove all`.
- Versiones viejas que siguen en el datapack: plaza (`aplanar`, `construir`, `reconstruir`, `arreglar`, `hierro_arreglar`).

## Generador (carpeta `generador/`)
- Scripts en Python que escriben todas las funciones y el zip. Se encadenan así: `gen6.py` ejecuta `gen5` (hasta la parte de MEGABASE), `gen5` ejecuta `gen4`, y así hacia atrás.
- Las rutas están fijas en `/tmp/claude-0/dp/...`. Hay que **cambiarlas** antes de usarlos en Windows.
- `validar.py` revisa nombres de bloques, propiedades, ítems y entidades contra un `data.json` sacado del paquete npm `minecraft-data` (versión 26.1):
  ```
  npm install minecraft-data
  ```
  Para generar ese archivo, exportar `blocksArray` / `itemsArray` / `entitiesArray`.
- Alternativa: editar directamente los `.mcfunction` dentro del zip.

## Pendientes / cosas a tener en cuenta
- Nada de la mecánica real de las granjas está probada en el juego. Lo más arriesgado: los pistones y observadores de caña/sandía, los vagones tolva bajo la tierra, y si los gólems caen al foso de fogatas.
- Con muchos aldeanos y vagones tolva puede haber lag.
- No hay copia de seguridad reciente del mundo. **Antes de cambios grandes: `stop` y copiar la carpeta `world`.**
- Revertir terreno aplanado: borrar esos chunks con MCA Selector para que se generen de nuevo.
