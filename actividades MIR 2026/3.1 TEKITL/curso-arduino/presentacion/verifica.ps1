# Comprueba la presentación con PowerPoint (hace falta tenerlo instalado): marca el texto que se sale de su cuadro y las tablas que bajan demasiado.
# Uso:   .\verifica.ps1                       (revisa Curso-Arduino-presentacion.pptx)
#        .\verifica.ps1 -Imagenes .\imagenes  (además exporta cada lámina a PNG para mirarlas)
param([string]$Pptx = (Join-Path $PSScriptRoot "Curso-Arduino-presentacion.pptx"), [string]$Imagenes = "")
$ErrorActionPreference = "Stop"
$Pptx = (Resolve-Path $Pptx).Path
$salida = Join-Path $env:TEMP "medidas-presentacion.tsv"
$app = New-Object -ComObject PowerPoint.Application
try {
    $pres = $app.Presentations.Open($Pptx, $true, $false, $false)      # solo lectura, sin ventana
    $lineas = New-Object System.Collections.Generic.List[string]
    $i = 0
    foreach ($sl in $pres.Slides) {
        $i++
        foreach ($sh in $sl.Shapes) {
            if ($sh.HasTable) {
                $lineas.Add("TAB`t$i`t$($sh.Name)`t$([math]::Round($sh.Top,1))`t$([math]::Round($sh.Height,1))`t0`t0`t0")
            } elseif ($sh.HasTextFrame -and $sh.TextFrame.HasText) {
                $tr = $sh.TextFrame.TextRange
                $lineas.Add("TXT`t$i`t$($sh.Name)`t$([math]::Round($sh.Top,1))`t$([math]::Round($sh.Height,1))`t$([math]::Round($tr.BoundHeight,1))`t$($tr.Lines().Count)`t$($sh.Rotation)")
            }
        }
    }
    $lineas | Out-File -Encoding utf8 $salida
    if ($Imagenes) {
        New-Item -ItemType Directory -Force $Imagenes | Out-Null
        $dir = (Resolve-Path $Imagenes).Path
        $alto = [int](1280 * $pres.PageSetup.SlideHeight / $pres.PageSetup.SlideWidth)
        for ($k = 1; $k -le $pres.Slides.Count; $k++) { $pres.Slides.Item($k).Export((Join-Path $dir ("lamina-{0:D3}.png" -f $k)), "PNG", 1280, $alto) }
        "Láminas exportadas a $dir"
    }
    $pres.Close()
} finally {
    try { $app.Quit() } catch {}
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($app) | Out-Null
}
$env:PYTHONIOENCODING = "utf-8"
python (Join-Path $PSScriptRoot "qa_texto.py") $salida
