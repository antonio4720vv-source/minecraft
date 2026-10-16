# =====================================================================
#  Servidor de Minecraft casero (Java + Bedrock) - script de arranque
#  Paper + Geyser + Floodgate + ViaVersion + ViaBackwards + datapack de granjas
#  Se ejecuta con INICIAR_SERVIDOR.bat (no hace falta abrirlo a mano).
# =====================================================================

# ------------------------- CONFIGURACION -----------------------------
$RAM     = "4G"     # memoria maxima del servidor (ej. "3G", "6G")
$RAM_MIN = "2G"     # memoria inicial
$VERSION = "26.2"   # version de Paper/Minecraft. NO subir a 26.3: Geyser falla ("asBukkitCopy")
$JAVA_VERSION = 25  # Minecraft 26.x pide Java 25
# ---------------------------------------------------------------------

$ErrorActionPreference = "Stop"
$ProgressPreference    = "SilentlyContinue"   # descargas mucho mas rapidas en PowerShell 5
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$UA = "ServidorMinecraftCasero/1.0 (iniciar.ps1)"   # la API de Paper (Fill) exige User-Agent

$DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $DIR
$Host.UI.RawUI.WindowTitle = "Servidor Minecraft - Java y Bedrock ($VERSION)"

function Info($t) { Write-Host "[*] $t" -ForegroundColor Cyan }
function Ok($t)   { Write-Host "[OK] $t" -ForegroundColor Green }
function Warn($t) { Write-Host "[!] $t" -ForegroundColor Yellow }

function Descargar($url, $destino) {
    $tmp = "$destino.descargando"
    if (Test-Path $tmp) { Remove-Item $tmp -Force }
    Invoke-WebRequest -Uri $url -OutFile $tmp -UserAgent $UA -UseBasicParsing
    Move-Item $tmp $destino -Force
}

# Compara versiones tipo "26.2", "26.3", "1.21.11". Devuelve -1, 0 o 1.
function CompararVersion($a, $b) {
    $pa = ($a -split '[^0-9]+') | Where-Object { $_ -ne "" } | ForEach-Object { [int]$_ }
    $pb = ($b -split '[^0-9]+') | Where-Object { $_ -ne "" } | ForEach-Object { [int]$_ }
    for ($i = 0; $i -lt [Math]::Max($pa.Count, $pb.Count); $i++) {
        $x = if ($i -lt $pa.Count) { $pa[$i] } else { 0 }
        $y = if ($i -lt $pb.Count) { $pb[$i] } else { 0 }
        if ($x -lt $y) { return -1 }
        if ($x -gt $y) { return 1 }
    }
    return 0
}

Write-Host ""
Write-Host "  ==============================================" -ForegroundColor Magenta
Write-Host "    SERVIDOR DE MINECRAFT  (Java + Bedrock)  $VERSION" -ForegroundColor Magenta
Write-Host "  ==============================================" -ForegroundColor Magenta
Write-Host ""

# ----------------------------- JAVA ----------------------------------
$JAVA = Join-Path $DIR "java\bin\java.exe"
if (-not (Test-Path $JAVA)) {
    Info "No encuentro Java $JAVA_VERSION portable. Descargando Temurin JDK $JAVA_VERSION (unos 200 MB)..."
    $zip = Join-Path $DIR "java_descarga.zip"
    $url = "https://api.adoptium.net/v3/binary/latest/$JAVA_VERSION/ga/windows/x64/jdk/hotspot/normal/eclipse"
    Descargar $url $zip
    $tmpDir = Join-Path $DIR "java_tmp"
    if (Test-Path $tmpDir) { Remove-Item $tmpDir -Recurse -Force }
    Expand-Archive -Path $zip -DestinationPath $tmpDir -Force
    $interior = Get-ChildItem $tmpDir -Directory | Select-Object -First 1
    if (Test-Path (Join-Path $DIR "java")) { Remove-Item (Join-Path $DIR "java") -Recurse -Force }
    Move-Item $interior.FullName (Join-Path $DIR "java")
    Remove-Item $tmpDir -Recurse -Force
    Remove-Item $zip -Force
    Ok "Java instalado en la carpeta java\"
}

# ------------------- CAMBIO DE VERSION / RESPALDO ---------------------
$verFile = Join-Path $DIR "version.txt"
$verAnterior = if (Test-Path $verFile) { (Get-Content $verFile -Raw).Trim() } else { "" }
if ($verAnterior -ne "" -and $verAnterior -ne $VERSION) {
    Warn "La version cambio: $verAnterior -> $VERSION. Se descargara Paper $VERSION de nuevo."
    if (Test-Path "paper.jar") { Remove-Item "paper.jar" -Force }
    if ((CompararVersion $VERSION $verAnterior) -lt 0) {
        # Bajar de version: un mundo abierto en una version mas nueva NO abre en una mas vieja.
        $respaldo = Join-Path $DIR "mundo_respaldo_$verAnterior"
        Warn "Estas BAJANDO de version. Muevo el mundo a $respaldo (no se borra nada)."
        New-Item -ItemType Directory -Force -Path $respaldo | Out-Null
        Get-ChildItem $DIR -Directory -Filter "world*" | ForEach-Object { Move-Item $_.FullName (Join-Path $respaldo $_.Name) -Force }
    }
}

# ----------------------------- PAPER ---------------------------------
if (-not (Test-Path "paper.jar")) {
    Info "Descargando Paper $VERSION (ultima build ESTABLE)..."
    $builds = Invoke-RestMethod -Uri "https://fill.papermc.io/v3/projects/paper/versions/$VERSION/builds" -UserAgent $UA
    $build = $builds | Where-Object { $_.channel -eq "STABLE" } | Select-Object -First 1
    if (-not $build) { $build = $builds | Select-Object -First 1; Warn "No hay build ESTABLE de $VERSION, uso la ultima disponible." }
    $url = $build.downloads."server:default".url
    Descargar $url (Join-Path $DIR "paper.jar")
    Ok "Paper $VERSION build $($build.id) descargado."
}
Set-Content -Path $verFile -Value $VERSION -Encoding ASCII

# ----------------------------- EULA ----------------------------------
if (-not (Test-Path "eula.txt") -or -not (Select-String -Path "eula.txt" -Pattern "eula=true" -Quiet)) {
    Set-Content -Path "eula.txt" -Value "eula=true" -Encoding ASCII
}

# ---------------------------- PLUGINS --------------------------------
New-Item -ItemType Directory -Force -Path "plugins" | Out-Null

# Si ya hay un .jar del plugin (con cualquier nombre), no se vuelve a bajar.
# Para ACTUALIZAR un plugin: borra su .jar de la carpeta plugins y reinicia.
function YaEsta($patron) { return [bool](Get-ChildItem (Join-Path $DIR "plugins") -Filter $patron -File -ErrorAction SilentlyContinue) }

function PluginGeyser($proyecto, $archivo, $patron) {
    $dest = Join-Path $DIR "plugins\$archivo"
    if (YaEsta $patron) { return }
    try {
        Info "Descargando $archivo..."
        Descargar "https://download.geysermc.org/v2/projects/$proyecto/versions/latest/builds/latest/downloads/spigot" $dest
        Ok "$archivo listo."
    } catch { Warn "No se pudo descargar $archivo ($($_.Exception.Message)). El servidor arranca igual." }
}

function PluginModrinth($proyecto, $archivo, $patron) {
    $dest = Join-Path $DIR "plugins\$archivo"
    if (YaEsta $patron) { return }
    try {
        Info "Descargando $archivo (Modrinth)..."
        $q = "loaders=" + [uri]::EscapeDataString('["paper"]') + "&game_versions=" + [uri]::EscapeDataString("[`"$VERSION`"]")
        $versiones = Invoke-RestMethod -Uri "https://api.modrinth.com/v2/project/$proyecto/version?$q" -UserAgent $UA
        if (-not $versiones) { throw "no hay version para $VERSION" }
        $v = $versiones | Where-Object { $_.version_type -eq "release" } | Select-Object -First 1
        if (-not $v) { $v = $versiones | Select-Object -First 1 }
        $f = $v.files | Where-Object { $_.primary } | Select-Object -First 1
        if (-not $f) { $f = $v.files | Select-Object -First 1 }
        Descargar $f.url $dest
        Ok "$archivo $($v.version_number) listo."
    } catch { Warn "No se pudo descargar $archivo ($($_.Exception.Message)). El servidor arranca igual." }
}

PluginGeyser   "geyser"       "Geyser-Spigot.jar"    "Geyser*.jar"
PluginGeyser   "floodgate"    "floodgate-spigot.jar" "floodgate*.jar"
PluginModrinth "viaversion"   "ViaVersion.jar"       "ViaVersion*.jar"
PluginModrinth "viabackwards" "ViaBackwards.jar"     "ViaBackwards*.jar"

# ------------------------ DATAPACK DE GRANJAS ------------------------
# La copia "maestra" esta en datapacks\. Se copia al mundo si falta o si la maestra es mas nueva.
$dpOrigen = Join-Path $DIR "datapacks\granjas_datapack.zip"
if (Test-Path $dpOrigen) {
    $dpDir = Join-Path $DIR "world\datapacks"
    New-Item -ItemType Directory -Force -Path $dpDir | Out-Null
    $dpDestino = Join-Path $dpDir "granjas_datapack.zip"
    if (-not (Test-Path $dpDestino) -or ((Get-Item $dpOrigen).LastWriteTime -gt (Get-Item $dpDestino).LastWriteTime)) {
        Copy-Item $dpOrigen $dpDestino -Force
        Ok "Datapack de granjas copiado a world\datapacks\"
    }
}

# ----------------------------- ARRANQUE ------------------------------
Write-Host ""
Ok "Todo listo. Iniciando el servidor con $RAM de RAM..."
Write-Host "    Java:    puerto 25565 (TCP)" -ForegroundColor Gray
Write-Host "    Bedrock: puerto 19132 (UDP)" -ForegroundColor Gray
Write-Host "    Para dar op:     op Nombre    (los de Bedrock llevan punto: op .Nombre)" -ForegroundColor Gray
Write-Host "    Para apagar:     stop" -ForegroundColor Gray
Write-Host ""

$flags = @(
    "-Xms$RAM_MIN", "-Xmx$RAM",
    "-XX:+UseG1GC", "-XX:+ParallelRefProcEnabled", "-XX:MaxGCPauseMillis=200",
    "-XX:+UnlockExperimentalVMOptions", "-XX:+DisableExplicitGC", "-XX:+AlwaysPreTouch",
    "-XX:G1NewSizePercent=30", "-XX:G1MaxNewSizePercent=40", "-XX:G1HeapRegionSize=8M",
    "-XX:G1ReservePercent=20", "-XX:G1HeapWastePercent=5", "-XX:G1MixedGCCountTarget=4",
    "-XX:InitiatingHeapOccupancyPercent=15", "-XX:G1MixedGCLiveThresholdPercent=90",
    "-XX:G1RSetUpdatingPauseTimePercent=5", "-XX:SurvivorRatio=32", "-XX:+PerfDisableSharedMem",
    "-XX:MaxTenuringThreshold=1", "-Dusing.aikars.flags=https://mcflags.emc.gs", "-Daikars.new.flags=true",
    "-jar", "paper.jar", "--nogui"
)
$ErrorActionPreference = "Continue"
& $JAVA @flags

Write-Host ""
Warn "El servidor se apago."
