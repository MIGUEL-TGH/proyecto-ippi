"""Base técnica para armar la presentación del curso sobre la plantilla institucional (cursos-arduino.pptx).

Qué resuelve:
  - medir texto con las fuentes reales (Gilroy, Montserrat, Consolas) para repartir bien cada lámina antes de dibujarla;
  - formato en línea (**negritas**, *cursivas*, `código`) a partir del Markdown de las guías;
  - cuadros de texto, tarjetas, tablas, imágenes y paneles de código con el estilo de la plantilla;
  - «marcos»: copias de las láminas modelo de la plantilla (fondo, logotipos, barra lateral) sobre las que se pone el contenido;
  - notas del orador, secciones de PowerPoint y limpieza de las láminas originales de la plantilla.
Unidades: pulgadas (la plantilla mide 20 x 11.25 pulgadas).
"""
import copy
import os
import re
import uuid
from dataclasses import dataclass

from lxml import etree
from PIL import Image, ImageFont
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

# ---------------------------------------------------------------- paleta de la plantilla
VINO = "731440"
VINO_OSC = "4A0E28"
DORADO = "BF9F63"
TEXTO = "3A3A3A"
CLARO = "F2F2F2"
CLARO_SUAVE = "E6D9DF"
ROSA = "F7EEF1"
VERDE = "25625A"
GRIS = "8C8C8C"
BLANCO = "FFFFFF"
CODIGO_FONDO = "1F0A14"

F_CUERPO = "Gilroy"
F_TITULO = "Montserrat ExtraBold"
F_CODIGO = "Consolas"

ANCHO_PAG, ALTO_PAG = 20.0, 11.25

# ---------------------------------------------------------------- medición de texto con las fuentes reales
_DIR_FUENTES = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "Windows", "Fonts")
_ARCHIVOS = {
    ("Gilroy", False, False): "Gilroy-Regular.otf",
    ("Gilroy", True, False): "Gilroy-Bold.otf",
    ("Gilroy", False, True): "Gilroy-RegularItalic.otf",
    ("Gilroy", True, True): "Gilroy-BoldItalic.otf",
    ("Montserrat ExtraBold", False, False): "Montserrat-ExtraBold.otf",
    ("Montserrat ExtraBold", True, False): "Montserrat-ExtraBold.otf",
    ("Consolas", False, False): r"C:\Windows\Fonts\consola.ttf",
    ("Consolas", True, False): r"C:\Windows\Fonts\consolab.ttf",
}
_cache_fuentes = {}


def _fuente(nombre, bold=False, italic=False):
    clave = (nombre, bool(bold), bool(italic))
    if clave not in _cache_fuentes:
        arch = _ARCHIVOS.get(clave) or _ARCHIVOS.get((nombre, bool(bold), False)) or _ARCHIVOS[(nombre, False, False)]
        ruta = arch if os.path.isabs(arch) else os.path.join(_DIR_FUENTES, arch)
        _cache_fuentes[clave] = ImageFont.truetype(ruta, 1000)
    return _cache_fuentes[clave]


def ancho_in(texto, nombre, pt, bold=False, italic=False):
    return _fuente(nombre, bold, italic).getlength(texto) / 1000.0 * pt / 72.0


# Factores calibrados contra PowerPoint (ver calibra.py): alto de línea = FACTOR_LINEA * pt
FACTOR_LINEA = {"Gilroy": 1.21, "Montserrat ExtraBold": 1.22, "Consolas": 1.17}
HOLGURA_ANCHO = 0.95          # se usa el 97 % del ancho para decidir los saltos de línea (margen de seguridad)


def alto_linea_in(nombre, pt, interlin=1.0):
    return FACTOR_LINEA.get(nombre, 1.22) * pt * interlin / 72.0


# ---------------------------------------------------------------- formato en línea del Markdown
_PAT = re.compile(r"\*\*(.+?)\*\*|`([^`]+)`|(?<![\*\w])\*([^*\n]+?)\*(?!\*)")


def runs_md(texto, base=None):
    """[(texto, {"b": bool, "i": bool, "c": bool})] a partir de **negritas**, *cursivas* y `código`."""
    base = base or {"b": False, "i": False, "c": False}
    salida, pos = [], 0
    for m in _PAT.finditer(texto):
        if m.start() > pos:
            salida.append((texto[pos:m.start()], dict(base)))
        if m.group(1) is not None:
            salida.extend(runs_md(m.group(1), {**base, "b": True}))
        elif m.group(2) is not None:
            salida.append((m.group(2), {**base, "c": True}))
        else:
            salida.append((m.group(3), {**base, "i": True}))
        pos = m.end()
    if pos < len(texto):
        salida.append((texto[pos:], dict(base)))
    return [(t, e) for t, e in salida if t != ""]


def plano(texto):
    return "".join(t for t, _ in runs_md(texto))


_ORACIONES = re.compile(r"(?<=[.!?…])\s+(?=[A-ZÁÉÍÓÚÑ¿¡«“\"*`(0-9])")


def oraciones(texto):
    return [s for s in _ORACIONES.split(texto.strip()) if s]


# lo que es solo para quien imparte: no se muestra en la lámina, va a las notas del orador
_INTERNO = re.compile(r"\bV(?:[1-9]|1[0-6])\b|Pendiente de comprobar|Pendiente de decisi[oó]n|[Ss]oluci[oó]n del instructor|Para el instructor|\bvalidaci[oó]n\b", re.I)
_FRASES_INTERNAS = [r"\s*\*Se espera por el circuito[^*]*\*", r"\s*\*Determinista\*", r"\s*\*Se espera[^*]*\*"]


def limpia_interno(texto):
    """Quita de un texto las frases pensadas solo para el instructor. Devuelve (texto_limpio, lo_quitado)."""
    quitado = []
    for pat in _FRASES_INTERNAS:
        for m in re.finditer(pat, texto):
            quitado.append(m.group(0).strip())
        texto = re.sub(pat, "", texto)
    partes = oraciones(texto)
    if len(partes) <= 1 and not _INTERNO.search(texto):
        return texto, quitado
    quedan = []
    for s in partes:
        if _INTERNO.search(plano(s)):
            quitado.append(s)
        else:
            quedan.append(s)
    return " ".join(quedan).strip(), quitado


def corta(texto, n):
    """Primeras oraciones de un texto Markdown sin pasar de n caracteres visibles. Devuelve (corto, resto)."""
    if len(plano(texto)) <= n:
        return texto, ""
    corto = ""
    for s in oraciones(texto):
        if corto and len(plano(corto + " " + s)) > n:
            break
        corto = (corto + " " + s).strip()
        if len(plano(corto)) > n:
            break
    if not corto or len(plano(corto)) > n * 1.25:
        palabras = texto.split(" ")
        corto = ""
        for w in palabras:
            if len(plano(corto + " " + w)) > n:
                break
            corto = (corto + " " + w).strip()
        corto = corto.rstrip(",;:") + "…"
    resto = texto[len(corto.rstrip("…")):].strip() if texto.startswith(corto.rstrip("…")) else ""
    return corto, resto


# ---------------------------------------------------------------- párrafos con formato
@dataclass
class P:
    texto: str = ""
    pt: float = 22
    color: str = CLARO
    acento: str = DORADO            # color de las **negritas**
    bold: bool = False
    fuente: str = F_CUERPO
    bullet: str = ""                # "" | "•" | "☐" | "num"
    align: str = "l"
    despues: float = 8              # pt de espacio después del párrafo
    italica: bool = False
    interlin: float = 1.0
    sangria: float = 0.42           # pulgadas, solo con bullet
    inicio: int = 1                 # primer número si bullet == "num"
    cod_color: str = ""             # color del `código` en línea (por omisión, el acento)


def _palabras(runs, p):
    """Lista de (palabra, bold, italic, fuente) y señal de espacio, para medir el ajuste de línea."""
    out = []
    for txt, e in runs:
        fuente = F_CODIGO if e.get("c") else p.fuente
        for k, w in enumerate(re.split(r"( +)", txt)):
            if w == "":
                continue
            out.append((w, p.bold or e.get("b", False), e.get("i", False) or p.italica, fuente))
    return out


def lineas_parrafo(p, ancho):
    """Número de líneas que ocupa un párrafo en un cuadro de 'ancho' pulgadas."""
    runs = runs_md(p.texto) if p.texto else []
    disp = ancho - (p.sangria if p.bullet else 0.0)
    disp *= HOLGURA_ANCHO
    if not runs:
        return 1
    lineas, actual = 1, 0.0
    for w, b, i, f in _palabras(runs, p):
        # una palabra se parte en la última línea cuando no cabe sola (URL o código largo)
        ancho_w = ancho_in(w, f, p.pt, b, i)
        if w.strip() == "":
            actual += ancho_w
            continue
        if actual + ancho_w > disp and actual > 0:
            lineas += 1
            actual = 0.0
        while ancho_w > disp:                 # palabra más ancha que la línea
            lineas += 1
            ancho_w -= disp
        actual += ancho_w
    return lineas


def alto_parrafos(ps, ancho):
    total = 0.0
    for p in ps:
        total += lineas_parrafo(p, ancho) * alto_linea_in(p.fuente, p.pt, p.interlin) + p.despues / 72.0
    return total


# ---------------------------------------------------------------- formas y texto
def rgb(h):
    return RGBColor.from_string(h)


def _quita_sombra(shp):
    sp_pr = shp._element.spPr
    for e in sp_pr.findall(qn("a:effectLst")):
        sp_pr.remove(e)
    etree.SubElement(sp_pr, qn("a:effectLst"))


def tarjeta(slide, x, y, w, h, relleno=None, alpha=None, borde=None, borde_w=0.04, radio=0.05, nombre=None, forma=None):
    """Rectángulo redondeado (como las tarjetas de la plantilla). 'alpha' en 0-1: transparencia del relleno."""
    shp = slide.shapes.add_shape(forma or MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    if forma is None:
        shp.adjustments[0] = radio
    if relleno:
        shp.fill.solid()
        shp.fill.fore_color.rgb = rgb(relleno)
        if alpha is not None:
            clr = shp._element.spPr.find(qn("a:solidFill")).find(qn("a:srgbClr"))
            a = etree.SubElement(clr, qn("a:alpha"))
            a.set("val", str(int(alpha * 100000)))
    else:
        shp.fill.background()
    if borde:
        shp.line.color.rgb = rgb(borde)
        shp.line.width = Inches(borde_w)
    else:
        shp.line.fill.background()
    _quita_sombra(shp)
    if nombre:
        shp.name = nombre
    return shp


def _formatea_run(run, p, e, color_base=None):
    f = run.font
    es_codigo = e.get("c", False)
    f.name = F_CODIGO if es_codigo else p.fuente
    f.size = Pt(p.pt)
    f.bold = bool(p.bold or e.get("b", False))
    f.italic = bool(e.get("i", False) or p.italica)
    if es_codigo:
        color = p.cod_color or p.acento
    elif e.get("b", False) and p.acento and not p.bold:
        color = p.acento
    else:
        color = color_base or p.color
    f.color.rgb = rgb(color)
    run._r.get_or_add_rPr().set("lang", "es-MX")


def _bullet(par, p):
    pPr = par._p.get_or_add_pPr()
    for tag in ("a:buNone", "a:buChar", "a:buAutoNum", "a:buClr", "a:buFont", "a:buSzPct"):
        for e in pPr.findall(qn(tag)):
            pPr.remove(e)
    if not p.bullet:
        etree.SubElement(pPr, qn("a:buNone"))
        return
    pPr.set("marL", str(int(Inches(p.sangria))))
    pPr.set("indent", str(-int(Inches(p.sangria))))
    clr = etree.SubElement(pPr, qn("a:buClr"))
    etree.SubElement(clr, qn("a:srgbClr")).set("val", p.acento)
    if p.bullet == "num":
        etree.SubElement(pPr, qn("a:buFont")).set("typeface", p.fuente)
        bu = etree.SubElement(pPr, qn("a:buAutoNum"))
        bu.set("type", "arabicPeriod")
        if p.inicio != 1:
            bu.set("startAt", str(p.inicio))
    else:
        etree.SubElement(pPr, qn("a:buFont")).set("typeface", "Segoe UI Symbol" if p.bullet == "☐" else "Arial")
        etree.SubElement(pPr, qn("a:buChar")).set("char", p.bullet)


def llena_texto(tf, parrafos, anchor="t", margen=(0, 0, 0, 0), ajuste=True):
    tf.word_wrap = ajuste
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left, tf.margin_top, tf.margin_right, tf.margin_bottom = (Inches(m) for m in margen)
    tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[anchor]
    for k, p in enumerate(parrafos):
        par = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        par.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[p.align]
        par.space_after = Pt(p.despues)
        par.space_before = Pt(0)
        par.line_spacing = p.interlin
        _bullet(par, p)
        for txt, e in runs_md(p.texto):
            r = par.add_run()
            r.text = txt
            _formatea_run(r, p, e)
        if not p.texto:
            end = par._p.get_or_add_endParaRPr() if hasattr(par._p, "get_or_add_endParaRPr") else None
            if end is not None:
                end.set("sz", str(int(p.pt * 100)))


def caja_texto(slide, x, y, w, h, parrafos, anchor="t", margen=(0, 0, 0, 0), nombre=None, ajuste=True):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    llena_texto(tb.text_frame, parrafos, anchor, margen, ajuste)
    if nombre:
        tb.name = nombre
    return tb


def texto_en_forma(shp, parrafos, anchor="m", margen=(0.1, 0.05, 0.1, 0.05)):
    llena_texto(shp.text_frame, parrafos, anchor, margen)


# ---------------------------------------------------------------- imágenes
def ajusta_imagen(ruta, max_w, max_h):
    with Image.open(ruta) as im:
        iw, ih = im.size
    esc = min(max_w / iw, max_h / ih)
    return iw * esc, ih * esc, iw / ih


def imagen(slide, ruta, x, y, max_w, max_h, alt="", alinea="l"):
    w, h, _ = ajusta_imagen(ruta, max_w, max_h)
    if alinea == "c":
        x = x + (max_w - w) / 2
    pic = slide.shapes.add_picture(ruta, Inches(x), Inches(y), Inches(w), Inches(h))
    if alt:
        pic._element.nvPicPr.cNvPr.set("descr", alt)
    return pic, x, y, w, h


# ---------------------------------------------------------------- tablas
def _borde_celda(tcPr, color, ancho_pt=0.75):
    for lado in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):
        for e in tcPr.findall(qn(lado)):
            tcPr.remove(e)
    for lado in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):
        ln = etree.SubElement(tcPr, qn(lado))
        ln.set("w", str(int(ancho_pt * 12700)))
        sf = etree.SubElement(ln, qn("a:solidFill"))
        etree.SubElement(sf, qn("a:srgbClr")).set("val", color)
    # los bordes deben ir antes del relleno dentro de a:tcPr
    relleno = tcPr.find(qn("a:solidFill"))
    if relleno is not None:
        tcPr.remove(relleno)
        tcPr.append(relleno)


MARGEN_CELDA = (0.14, 0.07, 0.14, 0.07)


def alto_fila(celdas, anchos, pt, fuente=F_CUERPO, bold=False, minimo=0.0):
    mx = 1
    for txt, w in zip(celdas, anchos):
        n = lineas_parrafo(P(txt, pt=pt, fuente=fuente, bold=bold, despues=0), w - MARGEN_CELDA[0] - MARGEN_CELDA[2])
        mx = max(mx, n)
    return max(minimo, mx * alto_linea_in(fuente, pt) + MARGEN_CELDA[1] + MARGEN_CELDA[3] + 0.04)


def tabla(slide, x, y, anchos, cab, filas, pt=20, estilo="oscuro", pt_cab=None, nombre=None, alinear=None, min_fila=0.5):
    """Tabla nativa. estilo 'oscuro': encabezado vino oscuro y filas blancas (como en la plantilla, para marcos oscuros);
    'claro': encabezado vino y filas rosa pálido/blanco (para marcos claros). Devuelve (forma, alto_total)."""
    pt_cab = pt_cab or pt
    n_cols = len(anchos)
    alto_cab = alto_fila(cab, anchos, pt_cab, bold=True, minimo=0.55)
    altos = [alto_fila(f, anchos, pt, minimo=min_fila) for f in filas]
    total = alto_cab + sum(altos)
    gf = slide.shapes.add_table(1 + len(filas), n_cols, Inches(x), Inches(y), Inches(sum(anchos)), Inches(total))
    if nombre:
        gf.name = nombre
    tbl = gf.table
    tblPr = tbl._tbl.tblPr
    tblPr.set("firstRow", "1")
    tblPr.set("bandRow", "0")
    for k, w in enumerate(anchos):
        tbl.columns[k].width = Inches(w)
    tbl.rows[0].height = Inches(alto_cab)
    for r, h in enumerate(altos):
        tbl.rows[r + 1].height = Inches(h)
    c_cab = VINO_OSC if estilo == "oscuro" else VINO
    c_borde = "D9C7CE"
    for r in range(len(filas) + 1):
        for k in range(n_cols):
            celda = tbl.cell(r, k)
            es_cab = r == 0
            txt = cab[k] if es_cab else filas[r - 1][k]
            if es_cab:
                relleno, color, bold, tam = c_cab, CLARO, True, pt_cab
            else:
                relleno = BLANCO if (estilo == "oscuro" or r % 2 == 1) else ROSA
                color, bold, tam = TEXTO, False, pt
            celda.fill.solid()
            celda.fill.fore_color.rgb = rgb(relleno)
            celda.margin_left, celda.margin_top, celda.margin_right, celda.margin_bottom = (Inches(m) for m in MARGEN_CELDA)
            celda.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = celda.text_frame
            tf.word_wrap = True
            al = (alinear[k] if alinear else "l")
            p = P(txt, pt=tam, color=color, acento=VINO if not es_cab else DORADO, bold=bold, despues=0, align=al, cod_color=VINO)
            par = tf.paragraphs[0]
            par.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER}[al]
            par.space_after = Pt(0)
            for t, e in runs_md(txt):
                run = par.add_run()
                run.text = t
                _formatea_run(run, p, e)
            _borde_celda(celda._tc.get_or_add_tcPr(), c_borde if not es_cab else c_cab)
    return gf, total


# ---------------------------------------------------------------- panel de código
_PALABRAS = r"\b(void|int|long|float|double|byte|bool|boolean|char|unsigned|const|if|else|for|while|do|return|break|continue|switch|case|true|false|static|String|struct|class|include|define)\b"
_CONST = r"\b(HIGH|LOW|INPUT|OUTPUT|INPUT_PULLUP|LED_BUILTIN|A[0-5]|PIN_[A-Z0-9_]+|[A-Z][A-Z0-9_]{2,})\b"


def _colorea(linea):
    """Trozos (texto, color) de una línea de código Arduino: comentarios, palabras clave, constantes, números y cadenas."""
    if "//" in linea:
        k = linea.index("//")
        return _colorea(linea[:k]) + [(linea[k:], "A9C2B0")] if linea[:k] else [(linea, "A9C2B0")]
    trozos, pos = [], 0
    pat = re.compile(r'("(?:[^"\\]|\\.)*")|' + _PALABRAS + "|" + _CONST + r"|(\b\d+(?:\.\d+)?\b)")
    for m in pat.finditer(linea):
        if m.start() > pos:
            trozos.append((linea[pos:m.start()], CLARO))
        if m.group(1):
            trozos.append((m.group(0), "E8C88A"))
        elif m.group(2):
            trozos.append((m.group(0), "F0A5B8"))
        elif m.group(3):
            trozos.append((m.group(0), DORADO))
        else:
            trozos.append((m.group(0), "9FD3E8"))
        pos = m.end()
    if pos < len(linea):
        trozos.append((linea[pos:], CLARO))
    return trozos


def mide_codigo(texto):
    ls = texto.split("\n")
    return len(ls), max((len(l) for l in ls), default=1)


def panel_codigo(slide, x, y, w, h, texto, pt, titulo=None, nombre=None):
    tarjeta(slide, x, y, w, h, relleno=CODIGO_FONDO, radio=0.03, nombre=(nombre or "Panel de código"))
    tb = slide.shapes.add_textbox(Inches(x + 0.3), Inches(y + 0.22), Inches(w - 0.6), Inches(h - 0.44))
    tf = tb.text_frame
    tf.word_wrap = False
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tb.name = "Código"
    for k, linea in enumerate(texto.split("\n")):
        par = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        par.space_after = Pt(0)
        par.space_before = Pt(0)
        par.line_spacing = 1.0
        for t, color in (_colorea(linea) if linea else []):
            r = par.add_run()
            r.text = t
            r.font.name = F_CODIGO
            r.font.size = Pt(pt)
            r.font.color.rgb = rgb(color)
            r._r.get_or_add_rPr().set("lang", "en-US")
        if not linea:
            par._p.get_or_add_pPr()
            end = etree.SubElement(par._p, qn("a:endParaRPr"))
            end.set("sz", str(int(pt * 100)))
    return tb


def ajusta_codigo(texto, ancho, alto, pts=(22, 20, 18, 16, 15, 14)):
    """Mayor tamaño de letra con el que el código cabe en un panel de ancho x alto pulgadas; None si no cabe ni con el menor."""
    n, mx = mide_codigo(texto)
    for pt in pts:
        w = mx * ancho_in("0", F_CODIGO, pt) + 0.6 + 0.1
        h = n * alto_linea_in(F_CODIGO, pt) + 0.44 + 0.05
        if w <= ancho and h <= alto:
            return pt
    return None


# ---------------------------------------------------------------- marcos (láminas modelo de la plantilla)
class Marcos:
    """Cada marco es una lámina de la plantilla de la que se copian solo las piezas fijas (fondo, logotipos, barra lateral)."""

    def __init__(self, ruta_plantilla):
        self.prs = Presentation(ruta_plantilla)
        self.n_original = len(self.prs.slides)
        self.layout = next(l for l in self.prs.slide_layouts if l.name == "Title Only")
        self._prepara_patron_notas()
        s = list(self.prs.slides)
        # lámina de la plantilla, índices de las piezas que se copian
        self.def_marcos = {
            "portada": (s[0], [0, 1, 2, 4, 5, 8], None),           # fondo, barras, rótulo vertical y logotipos; el título y el pie se escriben aparte
            "seccion": (s[4], [0, 1, 2, 3, 5, 6, 7, 8], None),     # sin el cuadro del título
            "oscuro": (s[5], [0, 1, 2, 3], None),
            "claro": (s[2], [0, 1, 2, 3, 4, 5, 6, 7], (4, 6)),     # barra lateral con logotipos; (índices de los textos de la barra)
            "claro_sin_logos": (s[2], [0, 1, 2, 3, 4, 5, 6], (4, 6)),
            "cierre": (s[25], [0, 1, 2], None),
        }

    def _prepara_patron_notas(self):
        """El patrón de notas de la plantilla no trae marcadores; sin ellos no se pueden escribir las notas del orador.
        Se le agregan los estándar: imagen de la lámina y cuerpo de las notas."""
        nm = self.prs.notes_master
        arbol = nm._element.find(qn("p:cSld")).find(qn("p:spTree"))
        if arbol.findall(".//" + qn("p:ph")):
            return
        ns = ('xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
              'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"')
        img = etree.fromstring(
            f'<p:sp {ns}><p:nvSpPr><p:cNvPr id="2" name="Slide Image Placeholder 1"/><p:cNvSpPr><a:spLocks noGrp="1" noRot="1" noChangeAspect="1"/></p:cNvSpPr>'
            '<p:nvPr><p:ph type="sldImg" idx="2"/></p:nvPr></p:nvSpPr><p:spPr><a:xfrm><a:off x="457200" y="685800"/><a:ext cx="5943600" cy="3343275"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln w="12700"><a:solidFill><a:prstClr val="black"/></a:solidFill></a:ln></p:spPr></p:sp>')
        cuerpo = etree.fromstring(
            f'<p:sp {ns}><p:nvSpPr><p:cNvPr id="3" name="Notes Placeholder 2"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
            '<p:nvPr><p:ph type="body" sz="quarter" idx="3"/></p:nvPr></p:nvSpPr><p:spPr><a:xfrm><a:off x="685800" y="4400550"/><a:ext cx="5486400" cy="4343400"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr><p:txBody><a:bodyPr vert="horz" lIns="91440" tIns="45720" rIns="91440" bIns="45720" rtlCol="0"/>'
            '<a:lstStyle/><a:p><a:pPr lvl="0"/><a:r><a:rPr lang="es-MX"/><a:t>Haga clic para modificar el estilo de texto del patrón</a:t></a:r></a:p></p:txBody></p:sp>')
        arbol.append(img)
        arbol.append(cuerpo)

    def _copia(self, slide, proto, indices):
        arbol = slide.shapes._spTree
        piezas = list(proto.shapes)
        nuevos = []
        for i in indices:
            el = copy.deepcopy(piezas[i]._element)
            for blip in el.iter(qn("a:blip")):
                for atr in (qn("r:embed"), qn("r:link")):
                    rid = blip.get(atr)
                    if rid:
                        parte = proto.part.related_part(rid)
                        blip.set(atr, slide.part.relate_to(parte, RT.IMAGE))
            arbol.append(el)
            nuevos.append(el)
        return nuevos

    def nueva(self, marco, barra=("CURSOS", "IPPI")):
        proto, indices, textos_barra = self.def_marcos[marco]
        slide = self.prs.slides.add_slide(self.layout)
        titulo = slide.shapes.title
        el_titulo = titulo._element
        slide.shapes._spTree.remove(el_titulo)                  # se vuelve a poner al final, delante del fondo
        nuevos = self._copia(slide, proto, indices)
        if textos_barra:
            for el, txt in zip([nuevos[indices.index(k)] for k in textos_barra], barra):
                ts = list(el.iter(qn("a:t")))
                ts[0].text = txt
                for extra in ts[1:]:
                    extra.text = ""
        slide.shapes._spTree.append(el_titulo)
        return slide

    def borra_originales(self):
        ids = self.prs.slides._sldIdLst
        for sld in list(ids)[: self.n_original]:
            self.prs.part.drop_rel(sld.rId)
            ids.remove(sld)
        _ = self.prs.slides                                     # renumera las partes de las láminas (slide1.xml, slide2.xml...)


def pon_titulo(slide, texto, x, y, w, h, pt, color, fuente=F_TITULO, align="l", anchor="t"):
    """Escribe el título en el marcador de título de la lámina (sirve para el esquema y la navegación)."""
    t = slide.shapes.title
    t.left, t.top, t.width, t.height = Inches(x), Inches(y), Inches(w), Inches(h)
    llena_texto(t.text_frame, [P(texto, pt=pt, color=color, acento=color, bold=True, fuente=fuente, align=align, despues=0)], anchor)
    t.name = "Título"
    return t


def notas(slide, texto):
    if texto and texto.strip():
        slide.notes_slide.notes_text_frame.text = texto.strip()


def renumera_ids(prs):
    """Da identificadores únicos a las formas de cada lámina (las piezas copiadas de la plantilla repiten los suyos)."""
    for slide in prs.slides:
        n = 1
        for el in slide.shapes._spTree.iter():
            if el.tag in (qn("p:cNvPr"),):
                el.set("id", str(n))
                n += 1


def agrega_secciones(prs, secciones):
    """secciones: [(nombre, [índices de lámina 0-based])]. Escribe la lista de secciones de PowerPoint (p14:sectionLst)."""
    P14 = "http://schemas.microsoft.com/office/powerpoint/2010/main"
    pres = prs.part._element
    ids = [s.get("id") for s in pres.find(qn("p:sldIdLst"))]
    ext_lst = pres.find(qn("p:extLst"))
    if ext_lst is None:
        ext_lst = etree.SubElement(pres, qn("p:extLst"))
    for e in list(ext_lst):
        if e.get("uri") == "{521415D9-36F7-43E2-AB2F-B90AF26B5E84}":
            ext_lst.remove(e)
    ext = etree.SubElement(ext_lst, qn("p:ext"))
    ext.set("uri", "{521415D9-36F7-43E2-AB2F-B90AF26B5E84}")
    lista = etree.SubElement(ext, "{%s}sectionLst" % P14, nsmap={"p14": P14})
    for nombre, idx in secciones:
        sec = etree.SubElement(lista, "{%s}section" % P14)
        sec.set("name", nombre)
        sec.set("id", "{" + str(uuid.uuid4()).upper() + "}")
        sl = etree.SubElement(sec, "{%s}sldIdLst" % P14)
        for k in idx:
            etree.SubElement(sl, "{%s}sldId" % P14).set("id", ids[k])
