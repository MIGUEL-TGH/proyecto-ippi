# Compila todos los sketches de curso-arduino\sketches para Arduino UNO.
# Usa el arduino-cli que ya viene dentro de Arduino IDE 2.x. No instala nada ni modifica tu carpeta de Arduino.
# Uso (desde PowerShell, en esta carpeta):   .\compilar-sketches.ps1
# Compilar solo verifica que el codigo es valido; no sustituye la prueba con la placa y el circuito.

$ErrorActionPreference = "Stop"

$cli = Join-Path $env:LOCALAPPDATA "Programs\Arduino IDE\resources\app\lib\backend\resources\arduino-cli.exe"
if (-not (Test-Path $cli)) { throw "No encuentro arduino-cli en: $cli (esta instalado Arduino IDE 2.x?)" }

# Librerias que vienen con el IDE (Servo, LiquidCrystal...)
$libs = Join-Path $env:LOCALAPPDATA "Arduino15\libraries"
$libArgs = @()
if (Test-Path $libs) { $libArgs = @("--libraries", $libs) }

$sketches = Get-ChildItem -Path (Join-Path $PSScriptRoot "sketches") -Directory | Sort-Object Name
$fallos = 0
$avisos = 0

foreach ($s in $sketches) {
    $salida = & $cli compile --fqbn arduino:avr:uno --warnings all @libArgs $s.FullName 2>&1 | Out-String
    $lineasAviso = $salida -split "`r?`n" | Where-Object { $_ -match "warning:" -and $_ -like "*$($s.Name)*" }
    $avisos += @($lineasAviso).Count
    if ($LASTEXITCODE -eq 0) {
        $flash = ""
        if ($salida -match "(\d+)%") { $flash = $Matches[1] + "% flash" }
        "{0,-28} OK     {1}" -f $s.Name, $flash
    } else {
        $fallos++
        "{0,-28} FALLA" -f $s.Name
        ($salida -split "`r?`n" | Where-Object { $_ -match "error" } | Select-Object -First 5) | ForEach-Object { "    $_" }
    }
    $lineasAviso | ForEach-Object { "    AVISO: $_" }
}

""
"Total: $($sketches.Count)  |  Con error: $fallos  |  Avisos en codigo propio: $avisos"
if ($fallos -gt 0) { exit 1 }
