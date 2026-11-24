"""Arma la presentación del curso de Arduino a partir de las guías (curso-arduino/guias) sobre la plantilla cursos-arduino.pptx.

Uso:   python construye.py                  (todas las sesiones)
       python construye.py S06 S07          (solo esas sesiones; sirve para probar)
Salida: curso-arduino/presentacion/Curso-Arduino-presentacion.pptx   (o ...-prueba.pptx si se piden sesiones sueltas)

Reglas generales (la guía es la fuente; la lámina muestra lo que ven los alumnos):
  - Cada bloque de la guía (párrafo, viñetas, tabla, código, imagen, cita) se convierte en lámina(s) según su tipo y su sección.
  - Lo que es solo para el instructor («Para el instructor», soluciones de los retos, claves de validación V1-V16, pendientes)
    no sale en la lámina: va a las notas del orador. Las notas también traen el texto completo de la sección de la guía.
  - Nada de lo que es para los alumnos se recorta en silencio: si no cabe, se reparte en otra lámina.
  - La letra se elige lo más grande posible para que el salón la lea (se mide el texto con las fuentes reales).
"""
import glob
import os
import re
import sys

import md_guias as M
from pptx_base import *   # noqa: F401,F403
from pptx_base import _INTERNO, _FRASES_INTERNAS

RAIZ = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
PLANTILLA = os.path.join(RAIZ, "cursos-arduino.pptx")
GUIAS = os.path.join(RAIZ, "curso-arduino", "guias")
SALIDA = os.path.join(RAIZ, "curso-arduino", "presentacion", "Curso-Arduino-presentacion.pptx")

# zonas de contenido (x, y, ancho, alto) en pulgadas
OSCURO = (1.2, 3.35, 17.9, 6.8)
DIAG = (4.7, 0.35, 14.7, 10.55)

OMITIR_H2 = ("Cómo leer los diagramas", "Tu práctica", "Para recompilar", "Versión con motor", "Cómo ayudar sin resolver", "Si un equipo va adelantado")
OMITIR_H3 = ("¿Por qué el motor sigue bloqueado",)
RE_PRACTICA = re.compile(r"^(P\d+[a-z]?|Paso \d+)\s*·\s*(.+?)(?:\s*\((?:≈\s*)?(\d+)\s*min[^)]*\))?\s*$")
PTS_TEXTO = (32, 30, 28, 26, 24, 22, 20, 18)
RE_ENCABEZADO = re.compile(r"^\*\*(.{2,40}?)\*\*$")


class Ctx:
    def __init__(self, sesion="", practica="", practica_titulo=""):
        self.sesion, self.practica, self.practica_titulo = sesion, practica, practica_titulo

    @property
    def migas(self):
        partes = [self.sesion.split("·")[0].strip()]
        if self.practica:
            partes.append(self.practica + (" " + self.practica_titulo if self.practica_titulo else ""))
        return " · ".join(p for p in partes if p)


def fusiona_texto(bloques):
    """Texto plano de unos bloques (para las notas del orador); el código no se repite."""
    out = []
    for b in bloques:
        t = b["t"]
        if t in ("p", "cita"):
            out.append(plano(b["texto"]))
        elif t in ("ul", "ol"):
            out.extend(("- " if t == "ul" else f"{k + 1}. ") + plano(x) for k, x in enumerate(b["items"]))
        elif t == "tabla":
            out.append(" | ".join(plano(c) for c in b["cab"]))
            out.extend(" | ".join(plano(c) for c in f) for f in b["filas"])
        elif t == "img":
            out.append(f"[Imagen: {b['alt']}]")
    return "\n".join(out)


class Deck:
    def __init__(self):
        self.m = Marcos(PLANTILLA)
        self.prs = self.m.prs
        self.n = 0
        self.secciones = []          # (nombre, [índices])
        self.sec_actual = None
        self.ctx = Ctx()
        self.nota_sec = ""
        self.nota_usada = True
        self.titulo_sec = ""
        self.extra_notas = []
        self.avisos = []

    def aviso(self, msg):
        self.avisos.append(f"{self.ctx.migas}: {msg}")

    # ---- secciones de PowerPoint
    def abre_seccion(self, nombre):
        self.sec_actual = (nombre, [])
        self.secciones.append(self.sec_actual)

    def registra(self):
        self.n += 1
        if self.sec_actual is not None:
            self.sec_actual[1].append(len(self.prs.slides) - 1)

    # ---- notas
    def define_notas(self, titulo, bloques, extra=None):
        self.titulo_sec = titulo
        self.nota_sec = f"{self.ctx.migas} › {titulo}\n\n" + fusiona_texto(bloques)
        self.extra_notas = list(extra or [])
        self.nota_usada = False

    # ---- láminas
    def nueva(self, marco, titulo, pos_titulo=None, pt_titulo=None, color_titulo=None):
        s = self.m.nueva(marco)
        if marco == "oscuro":
            pt = pt_titulo or next((p for p in (34, 32, 28, 24) if ancho_in(titulo, F_TITULO, p) < 17.2), 24)
            pon_titulo(s, titulo, 1.2, 2.05, 17.9, 1.1, pt, color_titulo or DORADO, anchor="m")
            if self.ctx.migas:
                caja_texto(s, 1.2, 10.5, 17.9, 0.4, [P(self.ctx.migas, pt=15, color=CLARO_SUAVE, despues=0)], nombre="Migas")
        elif marco == "claro_sin_logos":
            x, y, w, h = pos_titulo or (-14.0, 0.4, 12.0, 1.0)            # por omisión, fuera de la lámina (solo para el esquema)
            pon_titulo(s, titulo, x, y, w, h, pt_titulo or 28, color_titulo or VINO, anchor="t" if pos_titulo else "m")
        nota = ""
        if not self.nota_usada:
            nota = self.nota_sec
            if self.extra_notas:
                nota += "\n\n(Solo instructor)\n" + "\n".join(plano(x) for x in self.extra_notas)
            self.nota_usada = True
        elif self.titulo_sec:
            nota = f"{self.ctx.migas} › {self.titulo_sec} (continúa)"
        notas(s, nota)
        self.registra()
        return s

    def limpia(self, texto):
        t, q = limpia_interno(texto)
        self.extra_notas.extend(q)
        return t


# ====================================================================== piezas de lámina
def _tarjeta_nota(s, x, y, w, texto, pt, oscuro=True):
    p = P(texto, pt=pt, color=CLARO if oscuro else TEXTO, acento=DORADO if oscuro else VINO, despues=0)
    hh = alto_parrafos([p], w - 0.6)
    tarjeta(s, x, y, w, hh + 0.5, relleno="000000" if oscuro else VINO, alpha=0.22 if oscuro else 0.07, radio=0.08)
    caja_texto(s, x + 0.3, y + 0.25, w - 0.6, hh + 0.05, [p])
    return hh + 0.5


def texto_flujo(d, titulo, items, pts=PTS_TEXTO, min_pt=22):
    """items: [("p"|"ul"|"ol"|"cita", texto)]. Elige la letra más grande con la que cabe en una lámina; si no cabe con 'min_pt' o más,
    reparte en varias láminas (mejor más láminas que letra chica para el salón)."""
    x, y, w, h = OSCURO

    def parrafos(lista, pt):
        out, num = [], 1
        for tipo, txt in lista:
            if tipo == "ul":
                out.append(P(txt, pt=pt, bullet="•", despues=pt * 0.6, sangria=0.45))
            elif tipo == "ol":
                out.append(P(txt, pt=pt, bullet="num", despues=pt * 0.6, inicio=num, sangria=0.6))
                num += 1
            else:
                out.append(P(txt, pt=pt, despues=pt * 0.75))
        return out

    def alto(lista, pt):
        total = 0.0
        for tipo, txt in lista:
            if tipo == "cita":
                total += alto_parrafos([P(txt, pt=pt - 2, despues=0)], w - 0.6) + 0.5 + 0.2
            else:
                total += alto_parrafos(parrafos([(tipo, txt)], pt), w)
        return total

    for pt in [p for p in pts if p >= min_pt]:
        if alto(items, pt) <= h:
            return [_pinta_flujo(d, titulo, items, pt, parrafos)]
    pt = min(min_pt, max(p for p in pts))
    while any(alto([it], pt) > h for it in items) and pt > 16:
        pt -= 1
    paginas, actual = [], []
    for it in items:
        if actual and alto(actual + [it], pt) > h:
            paginas.append(actual)
            actual = []
        actual.append(it)
    if actual:
        paginas.append(actual)
    # reparte parejo: si quedó una última lámina con muy poco, se equilibran las dos últimas
    return [_pinta_flujo(d, titulo if k == 0 else f"{titulo} (cont.)", pg, pt, parrafos) for k, pg in enumerate(paginas)]


def _pinta_flujo(d, titulo, items, pt, parrafos):
    x, y, w, h = OSCURO
    s = d.nueva("oscuro", titulo)
    yy, seguidos = y, []

    def vuelca():
        nonlocal yy, seguidos
        if not seguidos:
            return
        ps = parrafos(seguidos, pt)
        hh = alto_parrafos(ps, w)
        caja_texto(s, x, yy, w, hh + 0.05, ps)
        yy += hh
        seguidos = []

    for tipo, txt in items:
        if tipo == "cita":
            vuelca()
            yy += _tarjeta_nota(s, x, yy, w, txt, pt - 2) + 0.2
        else:
            seguidos.append((tipo, txt))
    vuelca()
    return s


def reparte_filas(anchos, cab, filas, pt, disp, min_fila=0.5):
    """Páginas de filas que caben en 'disp' pulgadas; None si alguna fila no cabe sola."""
    alto_cab = alto_fila(cab, anchos, pt, bold=True, minimo=0.55)
    paginas, actual, hh = [], [], alto_cab
    for f in filas:
        hf = alto_fila(f, anchos, pt, minimo=min_fila)
        if alto_cab + hf > disp:
            return None
        if actual and hh + hf > disp:
            paginas.append(actual)
            actual, hh = [], alto_cab
        actual.append(f)
        hh += hf
    if actual:
        paginas.append(actual)
    return paginas


def tabla_slides(d, titulo, cab, filas, pesos, pts=(28, 26, 24, 22, 20), intro=None, post=None, min_fila=0.5):
    """Tabla en las láminas que haga falta (repite el encabezado), con la letra más grande que dé el menor número de láminas.
    'post': citas cortas que se agregan debajo si caben."""
    x, y, w, h = OSCURO
    anchos = [w * p / sum(pesos) for p in pesos]
    y0 = y
    p_intro = None
    if intro:
        p_intro = P(intro, pt=24, color=CLARO, acento=DORADO, despues=0)
        y0 += alto_parrafos([p_intro], w) + 0.3
    disp = y + h - y0
    altos_post = [alto_parrafos([P(tx, pt=22, despues=0)], w - 0.6) + 0.5 + 0.2 for tx in (post or [])]
    mejor = None
    for pt in pts:
        pg = reparte_filas(anchos, cab, filas, pt, disp, min_fila)
        if pg is None:
            continue
        usado = alto_fila(cab, anchos, pt, bold=True, minimo=0.55) + sum(alto_fila(f, anchos, pt, minimo=min_fila) for f in pg[-1]) + 0.25
        cabe_post = usado + sum(altos_post) <= disp + 0.1
        clave = (len(pg), 0 if cabe_post else 1)
        if mejor is None or clave < mejor[0]:
            mejor = (clave, pt, pg, cabe_post)
    if mejor is None:
        for pt in (18, 16, 14):
            pg = reparte_filas(anchos, cab, filas, pt, disp, min_fila)
            if pg:
                break
        pg = pg or [[f] for f in filas]
        mejor = ((len(pg), 1), pt, pg, False)
        d.aviso(f"tabla «{titulo}» con letra de {pt} pt")
    _, pt, paginas, cabe_post = mejor
    out = []
    for k, pg in enumerate(paginas):
        t = titulo if len(paginas) == 1 else f"{titulo} ({k + 1}/{len(paginas)})"
        s = d.nueva("oscuro", t)
        yy = y
        if p_intro and k == 0:
            caja_texto(s, x, yy, w, alto_parrafos([p_intro], w) + 0.05, [p_intro])
            yy += alto_parrafos([p_intro], w) + 0.3
        gf, total = tabla(s, x, yy, anchos, cab, pg, pt=pt, estilo="oscuro", min_fila=min_fila)
        yy += total + 0.25
        if post and cabe_post and k == len(paginas) - 1:
            for txt in post:
                yy += _tarjeta_nota(s, x, yy, w, txt, 22) + 0.2
        out.append(s)
    if post and not cabe_post:
        out += texto_flujo(d, f"{titulo} · nota", [("cita", tx) for tx in post])
    return out


def imagen_slide(d, titulo, ruta, alt, textos=None):
    """Diagrama a pantalla grande; si hay texto breve y sobra ancho, va a la derecha (si no, debajo)."""
    x, y, w, h = DIAG
    textos = textos or []
    if not textos:
        s = d.nueva("claro_sin_logos", titulo)
        imagen(s, ruta, x, y, w, h, alt, alinea="c")
        return s
    iw1, ih1, _ = ajusta_imagen(ruta, min(w * 0.62, 9.6), h)
    ancho_t = w - iw1 - 0.5
    if ancho_t >= 4.6:
        for pt in (30, 28, 26, 24, 22, 20):
            ps = [P(t, pt=pt, color=TEXTO, acento=VINO, despues=pt * 0.6) for t in textos]
            if alto_parrafos(ps, ancho_t) <= h - 2.4:
                s = d.nueva("claro_sin_logos", titulo, pos_titulo=(x + iw1 + 0.5, 0.6, ancho_t, 1.4), pt_titulo=28)
                imagen(s, ruta, x, y, iw1, h, alt)
                caja_texto(s, x + iw1 + 0.5, 2.15, ancho_t, h - 2.0, ps)
                return s
    iw2, ih2, _ = ajusta_imagen(ruta, w, h - 3.0)
    for pt in (26, 24, 22, 20):
        ps = [P(t, pt=pt, color=TEXTO, acento=VINO, despues=pt * 0.5) for t in textos]
        if alto_parrafos(ps, w) <= 2.5:
            break
    s = d.nueva("claro_sin_logos", titulo, pos_titulo=(x, 0.35, w, 0.8), pt_titulo=26)
    imagen(s, ruta, x, 1.2, iw2, ih2, alt, alinea="c")
    caja_texto(s, x, 1.2 + ih2 + 0.25, w, 2.6, ps)
    return s


def _ps_paso(fila, pq, pd):
    _, que, de, a = (list(fila) + ["", "", "", ""])[:4]
    ps = [P(que, pt=pq, bold=True, color=VINO, acento=VINO, despues=3, cod_color=VINO)]
    if de.strip():
        ps.append(P("**De:** " + de, pt=pd, color=TEXTO, acento=VINO, despues=1, cod_color=VINO))
    if a.strip():
        ps.append(P("**A:** " + a, pt=pd, color=TEXTO, acento=VINO, despues=0, cod_color=VINO))
    return ps


def armar_slides(d, titulo, ruta, alt, cab, filas):
    """Diagrama del protoboard a la izquierda (grande) y los pasos en tarjetas a la derecha; repite el diagrama si los pasos no caben."""
    x, y, w, h = DIAG
    iw, ih, _ = ajusta_imagen(ruta, 8.0, h)
    tx = x + iw + 0.45
    tw = x + w - tx
    y_ini, y_fin = 2.0, 10.85
    ancho_txt = tw - 1.15

    def tarjeta_alto(fila, pq, pd):
        return alto_parrafos(_ps_paso(fila, pq, pd), ancho_txt) + 0.35

    def reparte(pq, pd):
        pag, act, hh = [], [], 0.0
        for f in filas:
            hf = tarjeta_alto(f, pq, pd)
            if act and hh + hf + 0.15 > y_fin - y_ini:
                pag.append(act)
                act, hh = [], 0.0
            act.append(f)
            hh += hf + 0.15
        if act:
            pag.append(act)
        return pag

    mejor = None
    for pq, pd in ((26, 22), (24, 20), (22, 19), (20, 18)):
        pag = reparte(pq, pd)
        if mejor is None or len(pag) < len(mejor[2]):
            mejor = (pq, pd, pag)
    pq, pd, paginas = mejor
    out, primero = [], 1
    for pg in paginas:
        n0, n1 = primero, primero + len(pg) - 1
        rango = f"pasos {n0} a {n1}" if n1 > n0 else f"paso {n0}"
        t = titulo + (f" · {rango}" if len(paginas) > 1 else "")
        s = d.nueva("claro_sin_logos", t, pos_titulo=(tx, 0.45, tw, 1.4), pt_titulo=26)
        imagen(s, ruta, x, y, iw, h, alt)
        yy = y_ini
        for f in pg:
            ps = _ps_paso(f, pq, pd)
            hh = alto_parrafos(ps, ancho_txt) + 0.35
            tarjeta(s, tx, yy, tw, hh, relleno=ROSA, borde="E2CFD6", borde_w=0.02, radio=0.08)
            c = tarjeta(s, tx + 0.18, yy + 0.18, 0.62, 0.62, relleno=VINO, forma=MSO_SHAPE.OVAL)
            texto_en_forma(c, [P(plano(f[0]).strip() or str(primero), pt=20, color=BLANCO, bold=True, fuente=F_TITULO, align="c", despues=0)], "m", (0, 0, 0, 0))
            caja_texto(s, tx + 1.05, yy + 0.17, ancho_txt, hh - 0.2, ps)
            yy += hh + 0.15
        primero = n1 + 1
        out.append(s)
    return out


def codigo_slide(d, titulo, pre, codigo, post):
    """Panel de código con la indicación antes y la explicación después; prueba varias distribuciones y se queda con la de letra más grande."""
    x, y, w, h = OSCURO
    n_lin, mx = mide_codigo(codigo)
    pre_ps = [P(t, pt=24, despues=10) for t in pre]
    alto_pre = alto_parrafos(pre_ps, w) + 0.2 if pre_ps else 0.0
    y_cod = y + alto_pre
    h_disp = h - alto_pre

    def dibuja_pre(s):
        if pre_ps:
            caja_texto(s, x, y, w, alto_pre, pre_ps)

    # A: código arriba (todo el ancho) y explicación debajo
    for pt_c in (28, 26, 24, 22, 20, 18, 16, 14):
        ancho_nec = mx * ancho_in("0", F_CODIGO, pt_c) + 0.75
        alto_c = n_lin * alto_linea_in(F_CODIGO, pt_c) + 0.6
        if ancho_nec > w or alto_c > h_disp:
            continue
        if not post:
            s = d.nueva("oscuro", titulo)
            dibuja_pre(s)
            panel_codigo(s, x, y_cod, w, alto_c, codigo, pt_c)
            return [s]
        resto = h_disp - alto_c - 0.35
        for pt_b in (26, 24, 22, 20, 18):
            post_ps = [P(t, pt=pt_b, bullet="•", despues=pt_b * 0.5, sangria=0.45) for t in post]
            if alto_parrafos(post_ps, w) <= resto and pt_c >= 20:
                s = d.nueva("oscuro", titulo)
                dibuja_pre(s)
                panel_codigo(s, x, y_cod, w, alto_c, codigo, pt_c)
                caja_texto(s, x, y_cod + alto_c + 0.35, w, resto, post_ps)
                return [s]
    # B: código a la izquierda y explicación a la derecha
    if post:
        for ancho_c in (11.0, 10.0, 9.0):
            for pt_c in (24, 22, 20, 18, 16, 14):
                ancho_nec = mx * ancho_in("0", F_CODIGO, pt_c) + 0.75
                alto_c = n_lin * alto_linea_in(F_CODIGO, pt_c) + 0.6
                if ancho_nec > ancho_c or alto_c > h_disp:
                    continue
                ancho_t = w - ancho_c - 0.5
                for pt_b in (24, 22, 20, 18):
                    post_ps = [P(t, pt=pt_b, bullet="•", despues=pt_b * 0.5, sangria=0.45) for t in post]
                    if alto_parrafos(post_ps, ancho_t) <= h_disp:
                        s = d.nueva("oscuro", titulo)
                        dibuja_pre(s)
                        panel_codigo(s, x, y_cod, ancho_c, min(h_disp, max(alto_c, 4.0)), codigo, pt_c)
                        caja_texto(s, x + ancho_c + 0.5, y_cod + 0.1, ancho_t, h_disp, post_ps)
                        return [s]
    # C: el código solo (lo más grande posible, no menos de 18 pt) y la explicación en otra lámina
    out = []
    pt_c = next((p for p in (24, 22, 20, 18) if mx * ancho_in("0", F_CODIGO, p) + 0.75 <= w and n_lin * alto_linea_in(F_CODIGO, p) + 0.6 <= h_disp), None)
    if pt_c:
        alto_c = n_lin * alto_linea_in(F_CODIGO, pt_c) + 0.6
        s = d.nueva("oscuro", titulo)
        dibuja_pre(s)
        panel_codigo(s, x, y_cod, w, alto_c, codigo, pt_c)
        out.append(s)
    else:
        # se parte por líneas en tantas láminas como hagan falta con letra de 18 pt (o la mayor que quepa en el ancho)
        pt_c = next((p for p in (20, 18, 16, 14) if mx * ancho_in("0", F_CODIGO, p) + 0.75 <= w), 14)
        ls = codigo.split("\n")
        por = max(1, int((h - 0.6) / alto_linea_in(F_CODIGO, pt_c)))
        n = -(-len(ls) // por)
        por = -(-len(ls) // n)                                   # reparto parejo
        trozos = [ls[i:i + por] for i in range(0, len(ls), por)]
        d.aviso(f"código de {n_lin} líneas en {len(trozos)} láminas")
        for k, tr in enumerate(trozos):
            s = d.nueva("oscuro", f"{titulo} ({k + 1}/{len(trozos)})")
            if k == 0 and pre_ps:
                caja_texto(s, x, y, w, alto_pre, pre_ps)
                panel_codigo(s, x, y_cod, w, h - alto_pre, "\n".join(tr), pt_c)
            else:
                panel_codigo(s, x, y, w, h, "\n".join(tr), pt_c)
            out.append(s)
    if post:
        out += texto_flujo(d, titulo + " · qué hace", [("ul", t) for t in post])
    return out


def casillas_slide(d, titulo, items):
    """Lista de revisión con casillas ☐ en tarjetas."""
    x, y, w, h = OSCURO
    n = len(items)
    pt = 32
    while pt > 18 and sum(alto_parrafos([P(t, pt=pt, despues=0)], w - 1.7) + 0.5 for t in items) + (n - 1) * 0.2 > h:
        pt -= 2
    s = d.nueva("oscuro", titulo)
    yy = y
    for t in items:
        p = P(t, pt=pt, despues=0, acento=DORADO)
        hh = alto_parrafos([p], w - 1.7)
        tarjeta(s, x, yy, w, hh + 0.5, relleno="000000", alpha=0.22, radio=0.1)
        caja_texto(s, x + 0.3, yy + 0.18, 0.9, hh + 0.2, [P("☐", pt=pt + 8, color=DORADO, fuente="Segoe UI Symbol", despues=0)])
        caja_texto(s, x + 1.3, yy + 0.25, w - 1.7, hh + 0.05, [p])
        yy += hh + 0.5 + 0.2
    return s


def tarjetas_slide(d, titulo, items, etiquetas):
    """Una tarjeta por elemento (retos o evidencias). Máximo tres por lámina; se elige entre columnas y filas la distribución con letra más grande."""
    x, y, w, h = OSCURO
    n = len(items)
    if n > 3:
        k = 2 if n == 4 else 3
        out = []
        for i, (it, et) in enumerate(((items[:k], etiquetas[:k]), (items[k:], etiquetas[k:]))):
            out.append(tarjetas_slide(d, f"{titulo} ({i + 1}/2)", it, et))
        return out[-1]
    hueco = 0.35
    # --- columnas
    cw = (w - hueco * (n - 1)) / n
    pt_col = 30
    while pt_col > 16 and not all(alto_parrafos([P(t, pt=pt_col, despues=0)], cw - 0.7) + 1.4 <= h for t in items):
        pt_col -= 1
    # --- filas
    pw = max(1.2, max(ancho_in(e, F_TITULO, 22) + 0.7 for e in etiquetas))
    tw = w - pw - 1.3

    def altos_filas(pt):
        return [max(1.1, alto_parrafos([P(t, pt=pt, despues=0)], tw) + 0.5) for t in items]

    pt_fil = 30
    while pt_fil > 16 and sum(altos_filas(pt_fil)) + hueco * (n - 1) > h:
        pt_fil -= 1
    s = d.nueva("oscuro", titulo)
    if pt_fil > pt_col + 2:
        yy = y
        for t, et, hh in zip(items, etiquetas, altos_filas(pt_fil)):
            tarjeta(s, x, yy, w, hh, relleno="000000", alpha=0.22, radio=0.08)
            pill = tarjeta(s, x + 0.3, yy + 0.25, pw, 0.7, relleno=DORADO, radio=0.5)
            texto_en_forma(pill, [P(et, pt=22, color=VINO_OSC, bold=True, fuente=F_TITULO, align="c", despues=0)], "m", (0.05, 0, 0.05, 0))
            caja_texto(s, x + 0.3 + pw + 0.4, yy + 0.25, tw, hh - 0.3, [P(t, pt=pt_fil, despues=0)])
            yy += hh + hueco
        return s
    ch = min(h, max(alto_parrafos([P(t, pt=pt_col, despues=0)], cw - 0.7) for t in items) + 1.7)
    for k, t in enumerate(items):
        cx = x + k * (cw + hueco)
        tarjeta(s, cx, y, cw, ch, relleno="000000", alpha=0.22, radio=0.05)
        et = etiquetas[k]
        pill = tarjeta(s, cx + 0.3, y + 0.3, max(1.2, ancho_in(et, F_TITULO, 22) + 0.7), 0.7, relleno=DORADO, radio=0.5)
        texto_en_forma(pill, [P(et, pt=22, color=VINO_OSC, bold=True, fuente=F_TITULO, align="c", despues=0)], "m", (0.05, 0, 0.05, 0))
        caja_texto(s, cx + 0.35, y + 1.3, cw - 0.7, ch - 1.4, [P(t, pt=pt_col, despues=0)])
    return s


def ideas_slide(d, titulo, items, inicio=1, sobras=None):
    """Ideas numeradas (cada una: frase en negritas + explicación corta); lo que sobra va a las notas.
    Si con las ideas juntas la letra bajaría de 20 pt, se reparten en dos láminas."""
    x, y, w, h = OSCURO
    n = len(items)
    filas, resto_notas = [], []
    for it in items:
        m = re.match(r"^\*\*(.+?)\*\*\s*(.*)$", it, re.S)
        cab, resto = (m.group(1), m.group(2)) if m else ("", it)
        corto, sobra = corta(resto, 190) if resto else ("", "")
        if sobra:
            resto_notas.append(sobra)
        filas.append((cab, corto))
    ancho_t = w - 1.6

    def altos(pt):
        return [alto_parrafos(([P(c, pt=pt, bold=True, despues=2)] if c else []) + ([P(r, pt=pt - 2, despues=0)] if r else []), ancho_t) + 0.4 for c, r in filas]

    pt = 30
    while pt > 16 and sum(altos(pt)) + (n - 1) * 0.15 > h:
        pt -= 1
    if pt < 20 and n > 3:                      # mejor dos láminas con letra legible que una con letra chica
        k = (n + 1) // 2
        ideas_slide(d, f"{titulo} (1/2)", items[:k], inicio)
        return ideas_slide(d, f"{titulo} (2/2)", items[k:], inicio + k)
    d.extra_notas.extend(resto_notas)
    hs = altos(pt)
    s = d.nueva("oscuro", titulo)
    yy = y
    for k, ((cab, resto), hh) in enumerate(zip(filas, hs)):
        tarjeta(s, x, yy, w, hh, relleno="000000", alpha=0.22, radio=0.08)
        c = tarjeta(s, x + 0.25, yy + (hh - 0.7) / 2, 0.7, 0.7, relleno=DORADO, forma=MSO_SHAPE.OVAL)
        texto_en_forma(c, [P(str(inicio + k), pt=22, color=VINO_OSC, bold=True, fuente=F_TITULO, align="c", despues=0)], "m", (0, 0, 0, 0))
        ps = ([P(cab, pt=pt, bold=True, color=DORADO, despues=2)] if cab else []) + ([P(resto, pt=pt - 2, despues=0)] if resto else [])
        caja_texto(s, x + 1.25, yy + 0.2, ancho_t, hh - 0.3, ps)
        yy += hh + 0.15
    return s


def barras_slide(d, titulo, filas):
    """Plan de la sesión: una fila por actividad con sus minutos y una barra proporcional."""
    x, y, w, h = OSCURO
    s = d.nueva("oscuro", titulo)
    n = len(filas)
    alto_f = min(1.05, h / n)
    mx = max(m for _, m in filas)
    ancho_barra = 5.2
    x_et = x + 2.0
    ancho_et = w - 2.0 - ancho_barra - 0.5
    pt = 28
    while pt > 16 and any(alto_parrafos([P(t, pt=pt, despues=0)], ancho_et) > alto_f - 0.1 for t, _ in filas):
        pt -= 1
    for k, (txt, mins) in enumerate(filas):
        yy = y + k * alto_f
        pill = tarjeta(s, x, yy + 0.1, 1.75, alto_f - 0.2, relleno=DORADO, radio=0.4)
        texto_en_forma(pill, [P(f"{mins} min", pt=22, color=VINO_OSC, bold=True, fuente=F_TITULO, align="c", despues=0)], "m", (0, 0, 0, 0))
        caja_texto(s, x_et, yy, ancho_et, alto_f, [P(txt, pt=pt, despues=0)], anchor="m")
        bx = x_et + ancho_et + 0.4
        tarjeta(s, bx, yy + alto_f / 2 - 0.13, ancho_barra, 0.26, relleno="000000", alpha=0.22, radio=0.5)
        tarjeta(s, bx, yy + alto_f / 2 - 0.13, max(0.3, ancho_barra * mins / mx), 0.26, relleno=DORADO, radio=0.5)
    return s


# ====================================================================== composición de secciones
def clasifica(titulo):
    t = plano(titulo).lower()
    for pref, tipo in (("idea de la práctica", "idea"), ("conexión", "conexion"), ("modifica", "retos"), ("rompe", "rompe"),
                       ("si no funciona", "falla"), ("evidencia", "evidencia"), ("código", "codigo"), ("repetir con", "codigo")):
        if t.startswith(pref):
            return tipo
    return "generico"


def titulo_corto(t):
    t = plano(t)
    t = re.sub(r"\s*\((?:≈\s*)?\d+\s*min[^)]*\)", "", t)
    return t.strip()


def _interno_en(txt):
    return bool(_INTERNO.search(plano(txt))) or any(re.search(p, txt) for p in _FRASES_INTERNAS)


def _items_texto(pend):
    out = []
    for b in pend:
        if b["t"] in ("p", "cita"):
            out.append((b["t"], b["texto"]))
        else:
            out.extend((b["t"], x) for x in b["items"])
    return out


def filtra_instructor(d, bloques):
    """Quita de los bloques lo que es solo para el instructor (pasa a las notas del orador)."""
    nuevos = []
    for b in bloques:
        t = b["t"]
        if t == "cita" and re.match(r"^\*\*Para el instructor", b["texto"]):
            d.extra_notas.append(b["texto"])
            continue
        if t in ("p", "cita"):
            txt = d.limpia(b["texto"])
            if not txt.strip():
                continue
            b = {**b, "texto": txt}
        elif t in ("ul", "ol"):
            items = []
            for it in b["items"]:
                if re.search(r"[Ss]oluci[oó]n del instructor", it):
                    d.extra_notas.append(it)
                    cuerpo, _ = limpia_interno(it)
                    if cuerpo.strip():
                        items.append(cuerpo)
                else:
                    t2 = d.limpia(it)
                    if t2.strip():
                        items.append(t2)
            if not items:
                continue
            b = {**b, "items": items}
        elif t == "tabla":
            b = {**b, "filas": [[d.limpia(c) if _interno_en(c) else c for c in f] for f in b["filas"]]}
        nuevos.append(b)
    return nuevos


def compone(d, ctx, titulo, bloques, tipo=None):
    """Convierte los bloques de una sección en láminas siguiendo el orden de la guía."""
    tipo = tipo or clasifica(titulo)
    bl = filtra_instructor(d, [b for b in bloques if b["t"] != "hr"])
    titulo_t = titulo_corto(titulo)
    cod = f"{ctx.practica} · " if ctx.practica else ""
    i, pend = 0, []

    def vuelca(nombre=None):
        if pend:
            texto_flujo(d, cod + (nombre or titulo_t), _items_texto(pend))
        pend.clear()

    while i < len(bl):
        b = bl[i]
        t = b["t"]
        if t in ("p", "ul", "ol", "cita"):
            if t == "ul" and b.get("casillas"):                       # lista de revisión
                titulo_lista = "Revisa antes de conectar el USB"
                if pend and pend[-1]["t"] == "p" and re.search(r"[Rr]evis", plano(pend[-1]["texto"])) and len(plano(pend[-1]["texto"])) <= 110:
                    titulo_lista = plano(pend.pop()["texto"]).rstrip(":")
                vuelca("Ojo con la conexión" if tipo == "conexion" else None)
                casillas_slide(d, cod + titulo_lista, b["items"])
                i += 1
                continue
            if t == "ol" and tipo == "retos":                          # retos en tarjetas
                vuelca()
                ets, cuerpos = [], []
                for it in b["items"]:
                    m = re.match(r"^\*\*(.+?):?\*\*:?\s*(.*)$", it, re.S)
                    if m and len(m.group(1)) < 16:
                        ets.append(m.group(1).strip(": "))
                        cuerpos.append(m.group(2))
                    elif m and len(m.group(1)) < 48 and "(" in m.group(1):
                        etiqueta, aclara = m.group(1).split("(", 1)         # «Básico (predice y comprueba)»: la etiqueta es la primera palabra
                        ets.append(etiqueta.strip(": "))
                        cuerpos.append(f"*({aclara.strip(': ')})* {m.group(2)}".replace(")):", "):"))
                    else:
                        ets.append(f"Reto {len(ets) + 1}")
                        cuerpos.append(it)
                tarjetas_slide(d, cod + "Retos: modifica el programa", cuerpos, ets)
                i += 1
                continue
            if t == "ul" and tipo == "evidencia":
                vuelca()
                tarjetas_slide(d, cod + "Para tu bitácora", b["items"], [f"Evidencia {k + 1}" for k in range(len(b["items"]))])
                i += 1
                continue
            pend.append(b)
            i += 1
            continue
        if t == "codigo":
            pre = []
            while pend and pend[-1]["t"] == "p" and len(pre) < 2 and len(plano(pend[-1]["texto"])) <= 330:
                pre.insert(0, pend.pop()["texto"])
            vuelca()
            post, j = [], i + 1
            while j < len(bl) and bl[j]["t"] == "ul" and not bl[j].get("casillas") and len(post) < 8:
                post.extend(bl[j]["items"])
                j += 1
            codigo_slide(d, cod + titulo_t, pre, b["texto"], post)
            i = j
            continue
        if t == "img":
            antes = []
            if tipo != "conexion" and pend and pend[-1]["t"] == "p" and len(plano(pend[-1]["texto"])) <= 420 and not RE_ENCABEZADO.match(pend[-1]["texto"].strip()):
                antes.append(pend.pop()["texto"])               # el párrafo que presenta a la imagen va a su lado
            vuelca("Antes de armar" if tipo == "conexion" else None)
            j, sig = i + 1, list(antes)
            while j < len(bl) and bl[j]["t"] in ("p", "cita") and len(sig) < 2 and len(plano(bl[j]["texto"])) <= 520 and not RE_ENCABEZADO.match(bl[j]["texto"].strip()):
                sig.append(bl[j]["texto"])
                j += 1
            if j < len(bl) and bl[j]["t"] == "tabla" and tipo == "conexion" and not sig and len(bl[j]["cab"]) == 4:
                armar_slides(d, cod + "Armamos paso a paso", b["ruta"], b["alt"], bl[j]["cab"], bl[j]["filas"])
                i = j + 1
                continue
            imagen_slide(d, cod + titulo_t, b["ruta"], b["alt"], sig)
            i = j
            continue
        if t == "tabla":
            intro = None
            if pend and pend[-1]["t"] == "p" and len(plano(pend[-1]["texto"])) <= 230:
                intro = pend.pop()["texto"]
            vuelca("Antes de armar" if tipo == "conexion" else None)
            post, j = [], i + 1
            while j < len(bl) and bl[j]["t"] == "cita" and len(plano(bl[j]["texto"])) <= 320 and len(post) < 2:
                post.append(bl[j]["texto"])
                j += 1
            cab = b["cab"]
            pesos = {2: [1.0, 1.0], 3: [1.0, 1.1, 1.2]}.get(len(cab), [1] * len(cab))
            if cab and cab[0] == "Cantidad":
                pesos = [0.14, 0.86]
            elif cab and cab[0] == "Pin":
                pesos = [0.14, 0.4, 0.46]
            elif len(cab) == 2 and cab[0].startswith("Síntoma"):
                pesos = [0.38, 0.62]
            elif len(cab) == 2 and cab[0].startswith("Qué probar"):
                pesos = [0.42, 0.58]
            elif len(cab) == 4 and cab[0] == "Paso":
                pesos = [0.6, 2.4, 1.6, 1.6]
            elif cab and cab[0] == "#":
                pesos = [0.3] + [1.0] * (len(cab) - 1)
            elif cab and cab[0] == "Pieza":
                pesos = [1.0, 1.0, 1.0]
            elif cab and cab[0] == "Pin" and len(cab) == 4:
                pesos = [0.5, 1.2, 1.3, 1.6]
            titulo_tab = cod + ("Rompe y arregla" if tipo == "rompe" else titulo_t)
            tabla_slides(d, titulo_tab, cab, b["filas"], pesos, intro=intro, post=post)
            i = j
            continue
        i += 1
    vuelca("Ojo con la conexión" if tipo == "conexion" else None)


# ====================================================================== sesiones
def practica(d, ctx0, sec):
    m = RE_PRACTICA.match(plano(sec["titulo"]))
    pid, ptit, mins = (m.group(1), m.group(2), m.group(3)) if m else ("", titulo_corto(sec["titulo"]), None)
    ctx = Ctx(ctx0.sesion, pid, ptit)
    d.ctx = ctx
    hijas = [h for h in sec["hijas"] if not h["titulo"].startswith(OMITIR_H3)]
    idea = next((h for h in hijas if clasifica(h["titulo"]) == "idea"), None)
    bloques_idea = list(idea["bloques"]) if idea else []
    directos = [b for b in sec["bloques"] if b["t"] != "hr"]
    ps_idea = []
    d.define_notas(f"{pid} {ptit}", [])
    fuente_idea = bloques_idea if idea else directos
    while fuente_idea and fuente_idea[0]["t"] == "p" and len(ps_idea) < 2:
        ps_idea.append(d.limpia(fuente_idea.pop(0)["texto"]))
    d.nota_sec = f"{ctx.migas} › {pid} {ptit}\n\n" + (f"Duración estimada: {mins} min\n\n" if mins else "") + "\n\n".join(plano(x) for x in ps_idea)
    portada_practica(d, ctx, pid, ptit, mins, ps_idea)
    if bloques_idea:
        d.define_notas("Idea de la práctica", bloques_idea)
        compone(d, ctx, "Idea de la práctica", bloques_idea, "idea")
    if directos:
        grupos = [(ptit, [])]
        for b in directos:
            if b["t"] == "p" and RE_ENCABEZADO.match(b["texto"].strip()):
                grupos.append((plano(b["texto"]).strip(": "), []))
            else:
                grupos[-1][1].append(b)
        for tit, bl in grupos:
            if bl:
                d.define_notas(tit, bl)
                compone(d, ctx, tit, bl, "generico")
    for h in hijas:
        if h is idea:
            continue
        bl = [b for b in h["bloques"] if b["t"] != "hr"]
        d.define_notas(titulo_corto(h["titulo"]), bl)
        compone(d, ctx, h["titulo"], bl)


def portada_practica(d, ctx, pid, ptit, mins, ps_idea):
    x, y, w, h = OSCURO
    s = d.nueva("oscuro", ptit)
    tarjeta(s, x, y, 6.2, h, relleno="000000", alpha=0.22, radio=0.04)
    pt_id = 110 if len(pid) <= 3 else (84 if len(pid) <= 4 else 60)
    caja_texto(s, x + 0.35, y + 0.55, 5.6, 2.4, [P(pid or "·", pt=pt_id, color=DORADO, fuente=F_TITULO, bold=True, despues=0)], anchor="m")
    ps = []
    if mins:
        ps.append(P(f"≈ {mins} minutos", pt=30, bold=True, despues=12))
    ps.append(P(ctx.sesion, pt=24, color=CLARO_SUAVE, despues=0))
    caja_texto(s, x + 0.35, y + 3.35, 5.5, 3.0, ps)
    textos = ps_idea or ["(sin descripción en la guía)"]
    ancho = w - 6.5 - 0.9
    for pt in (34, 32, 30, 28, 26, 24, 22, 20):
        pp = [P(t, pt=pt, despues=pt * 0.8) for t in textos]
        if alto_parrafos(pp, ancho) + 1.25 <= h:
            break
    tarjeta(s, x + 6.5, y, w - 6.5, h, relleno="000000", alpha=0.22, radio=0.04)
    caja_texto(s, x + 6.95, y + 0.4, ancho, 0.7, [P("De qué se trata", pt=28, color=DORADO, fuente=F_TITULO, bold=True, despues=0)])
    caja_texto(s, x + 6.95, y + 1.3, ancho, h - 1.4, pp)


def etiqueta_plan(t):
    t = t[0].upper() + t[1:]
    return re.sub(r"^(P\d+[a-z]?|Paso \d+)\s+(?!·)", r"\1 · ", t)


def plan_sesion(d, meta):
    clave = next((k for k in meta if k.startswith("Prácticas y tiempos")), None)
    if not clave:
        return
    total = re.search(r"\((\d+) min\)", clave)
    texto = re.sub(r"\.?\s*Anota los tiempos reales.*$", "", meta[clave])
    filas = []
    for trozo in texto.split(" · "):
        m = re.match(r"^(.*?)\s+(\d+)\s*$", trozo.strip())
        if m:
            filas.append((etiqueta_plan(m.group(1)), int(m.group(2))))
    if not filas:
        return
    d.define_notas("Plan de la sesión", [{"t": "p", "texto": meta[clave]}])
    barras_slide(d, f"Plan de la sesión · {total.group(1) if total else sum(m for _, m in filas)} min", filas)


def _titulo_datos(resto):
    for b in resto:
        if b["t"] == "p":
            m = re.match(r"^\*\*(.+?)\*\*", b["texto"])
            if m:
                return m.group(1)
    return "Datos de apoyo"


def sesion(d, ruta):
    g = M.parsear(ruta)
    nombre = g["titulo"]
    ctx = Ctx(nombre)
    d.ctx = ctx
    d.abre_seccion(nombre)
    practicas = [titulo_corto(s["titulo"]) for s in g["secciones"] if RE_PRACTICA.match(plano(s["titulo"])) and not s["titulo"].startswith("Paso")]
    s = d.m.nueva("seccion")
    pon_titulo(s, nombre, 3.53, 3.3, 12.4, 3.0, 44, CLARO, anchor="b")
    sub = "  ·  ".join(practicas)
    caja_texto(s, 3.53, 6.55, 12.4, 2.6, [P(sub, pt=28, color=DORADO, bold=True, despues=0)] if sub else [P("", pt=20)])
    notas(s, f"{nombre}\n\n" + "\n".join(f"{k}: {plano(v)}" for k, v in g["meta"].items() if not k.startswith("Guía")))
    d.registra()
    plan_sesion(d, g["meta"])
    for sec in g["secciones"]:
        tit = plano(sec["titulo"])
        if tit.startswith(OMITIR_H2):
            continue
        d.ctx = Ctx(nombre)
        bl = [b for b in sec["bloques"] if b["t"] != "hr"]
        if tit.startswith("Materiales"):
            d.define_notas("Materiales", bl)
            cuerpo = filtra_instructor(d, bl)
            citas = [x["texto"] for x in cuerpo if x["t"] == "cita"][:1]
            for b in cuerpo:
                if b["t"] == "tabla":
                    tabla_slides(d, "Materiales", b["cab"], b["filas"], [0.15, 0.85], post=citas)
            for h in sec["hijas"]:
                d.define_notas(titulo_corto(h["titulo"]), h["bloques"])
                compone(d, d.ctx, h["titulo"], h["bloques"])
        elif tit.startswith("La idea de la sesión"):
            d.define_notas("Ideas de la sesión", bl)
            cuerpo = filtra_instructor(d, bl)
            ol = next((b for b in cuerpo if b["t"] == "ol"), None)
            if ol:
                ideas_slide(d, "Ideas de la sesión", ol["items"])
            resto = [b for b in cuerpo if b is not ol]
            if resto:
                tdatos = titulo_corto(_titulo_datos(resto))
                resto = [({**b, "texto": re.sub(r"^\*\*" + re.escape(tdatos) + r"\*\*\s*", "", b["texto"])} if b["t"] == "p" and b["texto"].startswith("**" + tdatos) else b) for b in resto]
                d.define_notas(tdatos, resto)
                compone(d, d.ctx, tdatos, resto, "generico")
        elif RE_PRACTICA.match(tit):
            practica(d, d.ctx, sec)
        elif tit.startswith("Cierre"):
            d.define_notas(titulo_corto(tit), bl)
            items = []
            for b in filtra_instructor(d, bl):
                items += _items_texto([b])
            texto_flujo(d, titulo_corto(tit), items, pts=(30, 28, 26, 24, 22, 20))
        else:
            d.define_notas(titulo_corto(tit), bl)
            if bl or not sec["hijas"]:
                compone(d, d.ctx, tit, bl, "generico")
            for h in sec["hijas"]:
                d.define_notas(titulo_corto(h["titulo"]), h["bloques"])
                compone(d, d.ctx, h["titulo"], h["bloques"])


# ====================================================================== curso completo
def portada_curso(d):
    d.abre_seccion("Presentación del curso")
    s = d.m.nueva("portada")
    caja_texto(s, 0.0, 4.5, 15.29, 3.3, [
        P("CURSO DE ELECTRÓNICA", pt=44, color=CLARO, bold=True, fuente=F_TITULO, align="r", interlin=1.2, despues=0),
        P("CON ARDUINO", pt=44, color=CLARO, bold=True, fuente=F_TITULO, align="r", interlin=1.2, despues=14),
        P("16 SESIONES DE 2 HORAS · KIT ARDUINO UNO R3", pt=22, color=CLARO, bold=True, fuente=F_TITULO, align="r", despues=0),
    ])
    caja_texto(s, 1.9, 7.9, 13.4, 1.4, [
        P("Subdirección de Desarrollo de Tecnologías de la Información", pt=20, color=CLARO, bold=True, align="r", despues=6),
        P("San Juan Atzingo, San Gabriel Chilac, Puebla", pt=20, color=CLARO, bold=True, align="r", despues=0),
    ])
    pon_titulo(s, "Curso de electrónica con Arduino", -14, 0.4, 12, 1, 20, CLARO)
    notas(s, "Portada del curso. Material generado a partir de las guías de las sesiones (curso-arduino/guias).")
    d.registra()


def mapa_curso(d, guias):
    """Una lámina con las sesiones y sus prácticas (sale de los títulos de las guías), en dos columnas."""
    filas = []
    for ruta in guias:
        g = M.parsear(ruta)
        ids = []
        for s in g["secciones"]:
            m = RE_PRACTICA.match(plano(s["titulo"]))
            if m and not s["titulo"].startswith("Paso"):
                ids.append(m.group(1))
        filas.append((g["titulo"], ids))
    d.ctx = Ctx("")
    d.nota_usada = True
    d.titulo_sec = ""
    x, y, w, h = OSCURO
    s = d.nueva("oscuro", "Mapa del curso")
    hueco = 0.3
    por_col = (len(filas) + 1) // 2
    cw = (w - hueco) / 2
    alto_f = h / por_col
    for k, (t, ids) in enumerate(filas):
        cx = x + (k // por_col) * (cw + hueco)
        cy = y + (k % por_col) * alto_f
        tarjeta(s, cx, cy + 0.06, cw, alto_f - 0.12, relleno="000000", alpha=0.22, radio=0.12)
        partes = re.match(r"^(Sesi[oó]nes? [\d ay]+?)\s*·\s*(.+)$", t)
        cab, nombre = (partes.group(1), partes.group(2)) if partes else ("", t)
        ps = [P((f"**{cab}** · " if cab else "") + nombre, pt=22, acento=DORADO, despues=0)]
        if ids:
            ps.append(P(" · ".join(ids), pt=20, color=CLARO_SUAVE, despues=0))
        caja_texto(s, cx + 0.3, cy + 0.06, cw - 0.6, alto_f - 0.12, ps, anchor="m")
    notas(s, "El curso se organiza en 16 sesiones de 2 horas: de encender un LED a un proyecto final propio.")


def cierre_curso(d):
    d.abre_seccion("Cierre")
    s = d.m.nueva("cierre")
    pon_titulo(s, "Gracias", -14, 0.4, 12, 1, 20, CLARO)
    d.registra()


def main(pedidas):
    d = Deck()
    todas = sorted(glob.glob(os.path.join(GUIAS, "S*.md")))
    sel = [r for r in todas if not pedidas or os.path.basename(r)[:3] in pedidas]
    if not pedidas:
        portada_curso(d)
        mapa_curso(d, todas)
    for ruta in sel:
        if os.path.basename(ruta).startswith("S14-16"):
            import proyecto_final          # el proyecto final no sigue el molde de las demás guías
            proyecto_final.proyecto(d, ruta)
        else:
            sesion(d, ruta)
    if not pedidas:
        cierre_curso(d)
    d.m.borra_originales()
    renumera_ids(d.prs)
    agrega_secciones(d.prs, [(n, [k - d.m.n_original for k in ix]) for n, ix in d.secciones])
    salida = SALIDA if not pedidas else SALIDA.replace(".pptx", "-prueba.pptx")
    d.prs.save(salida)
    print(f"{len(d.prs.slides)} láminas → {salida}")
    for a in d.avisos:
        print("  AVISO:", a)
    return d


if __name__ == "__main__":
    main(set(sys.argv[1:]))
