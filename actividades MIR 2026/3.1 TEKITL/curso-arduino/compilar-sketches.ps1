# Compila los sketches de curso-arduino\sketches para Arduino UNO.
# Usa el arduino-cli que ya viene dentro de Arduino IDE 2.x. No instala nada ni modifica tu carpeta de Arduino.
#
# Uso (desde PowerShell, en esta carpeta):
#   .\compilar-sketches.ps1                     compila todos los sketches
#   .\compilar-sketches.ps1 -Filtro "P1*"       compila solo los que empiezan con P1 (admite comodines * y ?)
#   .\compilar-sketches.ps1 -Filtro "P23_vent*" compila uno solo (util para probar un cambio rapido)
#
# Compilar solo verifica que el codigo es valido; no sustituye la prueba con la placa y el circuito.
# Este archivo es solo ASCII (sin acentos) a proposito: Windows PowerShell 5.1 lee mal los acentos de un archivo sin BOM.

param([string]$Filtro = "*")

$ErrorActionPreference = "Stop"

# Busca arduino-cli: instalacion "solo para mi" (la normal) o "para todos los usuarios".
$rutaRelativa = "Arduino IDE\resources\app\lib\backend\resources\arduino-cli.exe"
$cli = $null
foreach ($base in @((Join-Path $env:LOCALAPPDATA "Programs"), $env:ProgramFiles)) {
    $candidato = Join-Path $base $rutaRelativa
    if (Test-Path $candidato) { $cli = $candidato; break }
}
if (-not $cli) { throw "No encuentro arduino-cli.exe (esta instalado Arduino IDE 2.x? Se busco en %LOCALAPPDATA%\Programs y en Program Files)." }

# Librerias que vienen con el IDE (Servo, LiquidCrystal...)
$libs = Join-Path $env:LOCALAPPDATA "Arduino15\libraries"
$libArgs = @()
if (Test-Path $libs) { $libArgs = @("--libraries", $libs) }

$carpeta = Join-Path $PSScriptRoot "sketches"
if (-not (Test-Path $carpeta)) { throw "No encuentro la carpeta de sketches: $carpeta" }
$sketches = @(Get-ChildItem -Path $carpeta -Directory | Where-Object { $_.Name -like $Filtro } | Sort-Object Name)
if ($sketches.Count -eq 0) { throw "Ningun sketch coincide con el filtro '$Filtro'." }

$fallos = 0
$avisos = 0

foreach ($s in $sketches) {
    # arduino-cli escribe por stderr los avisos del NUCLEO de Arduino (por ejemplo, de new.cpp) cuando tiene que
    # recompilar el nucleo, o sea cuando su cache esta vacio. En Windows PowerShell 5.1, con
    # $ErrorActionPreference = "Stop", la primera linea de stderr se convierte en una excepcion (NativeCommandError)
    # y el script se detiene sin compilar nada. Por eso, solo durante esta llamada, se usa "Continue", y cada linea se
    # pasa a texto con "$_" para conservarla entera (sin el formato de error de PowerShell, que parte las lineas largas).
    $ErrorActionPreference = "Continue"
    $lineas = & $cli compile --fqbn arduino:avr:uno --warnings all @libArgs $s.FullName 2>&1 | ForEach-Object { "$_" }
    $codigo = $LASTEXITCODE
    $ErrorActionPreference = "Stop"

    $salida = $lineas -join "`n"
    $lineasAviso = @($lineas | Where-Object { $_ -match "warning:" -and $_ -like "*$($s.Name)*" })
    $avisos += $lineasAviso.Count
    if ($codigo -eq 0) {
        $flash = ""
        if ($salida -match "\((\d+)%\)") { $flash = $Matches[1] + "% flash" }
        "{0,-28} OK     {1}" -f $s.Name, $flash
    } else {
        $fallos++
        "{0,-28} FALLA" -f $s.Name
        ($lineas | Where-Object { $_ -match "error" } | Select-Object -First 5) | ForEach-Object { "    $_" }
    }
    $lineasAviso | ForEach-Object { "    AVISO: $_" }
}

""
"Total: $($sketches.Count)  |  Con error: $fallos  |  Avisos en codigo propio: $avisos"
if ($fallos -gt 0) { exit 1 }
