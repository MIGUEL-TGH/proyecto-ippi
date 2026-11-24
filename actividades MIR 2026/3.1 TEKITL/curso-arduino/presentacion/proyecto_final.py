"""Láminas de las Sesiones 14 a 16 (proyecto final) a partir de guias/S14-16-proyecto-final.md.

La guía no sigue el molde de las demás (no hay prácticas P##): trae reglas, banco de retos, mapas de pines y las hojas imprimibles A a D.
Qué se muestra y qué no:
  - se muestran las reglas, el plan de cada sesión, el banco de retos, los pines por reto, el código de la plantilla, y lo que cada hoja pide;
  - no salen en lámina «Cómo leer esta guía», «Cómo ayudar sin resolver» ni «Si un equipo va adelantado» (son para el instructor);
  - de las hojas se muestran las preguntas, las tablas y las listas de revisión; los renglones en blanco para llenar a mano no.
"""
import re

import md_guias as M
from pptx_base import *   # noqa: F401,F403
import construye as C

FIELDS_VACIOS = re.compile(r"^\*\*?(Equipo|Visto bueno|Dos cosas|Una cosa|Preguntas del grupo|Una idea|Lo que descubrimos|Número de kit)\b", re.I)


def _limpia_campo(txt):
    txt = re.sub(r"\*\((.*?)\)\*", r"(\1)", txt)            # cursivas que envuelven negritas: se dejan solo los paréntesis
    txt = re.sub(r"_{3,}", "", txt)
    txt = txt.replace("&nbsp;", "").strip()
    return re.sub(r"\s{2,}", " ", txt)


def _es_campo_vacio(txt):
    if not txt.strip() or txt.strip() == "&nbsp;":
        return True
    if FIELDS_VACIOS.match(txt.strip()):
        return True
    return len(plano(_limpia_campo(txt)).strip(" :☐")) < 3


def _casillas(b):
    """Una lista cuyos elementos empiezan con ☐ se trata como lista de revisión."""
    if b["t"] == "ul" and b["items"] and all(it.lstrip().startswith("☐") for it in b["items"]):
        return {**b, "casillas": True, "items": [it.lstrip()[1:].strip() for it in b["items"]]}
    return b


def hoja(d, ctx, nombre, bloques):
    """Una hoja imprimible: sus preguntas en una lámina de texto y cada tabla o lista de revisión en la suya (en el orden de la guía)."""
    bl = C.filtra_instructor(d, [b for b in bloques if b["t"] != "hr"])
    libres, unidades = [], []          # unidades: {"titulo", "intro", "bloque", "post"}
    i, ultimo_tabla = 0, None
    while i < len(bl):
        b = _casillas(bl[i])
        t = b["t"]
        if t == "p":
            if _es_campo_vacio(b["texto"]):
                i += 1
                continue
            txt = _limpia_campo(b["texto"])
            j = i + 1
            while j < len(bl) and bl[j]["t"] == "p" and _es_campo_vacio(bl[j]["texto"]):
                j += 1
            sig = _casillas(bl[j]) if j < len(bl) else None
            if sig and (sig["t"] == "tabla" or (sig["t"] == "ul" and sig.get("casillas"))):
                corto = len(plano(txt)) <= 90
                u = {"titulo": txt if corto else None, "intro": None if corto else txt, "bloque": sig, "post": []}
                unidades.append(u)
                ultimo_tabla = u if sig["t"] == "tabla" else None
                i = j + 1
                continue
            if ultimo_tabla is not None and not re.match(r"^\*\*\d+\.", txt) and len(plano(txt)) <= 320:
                ultimo_tabla["post"].append(txt)               # nota que acompaña a la tabla anterior
            else:
                libres.append(("p", txt))
                ultimo_tabla = None
        elif t == "ul":
            ultimo_tabla = None
            if b.get("casillas"):
                unidades.append({"titulo": None, "intro": None, "bloque": b, "post": []})
            else:
                libres.extend(("ul", _limpia_campo(x)) for x in b["items"])
        elif t == "tabla":
            u = {"titulo": None, "intro": None, "bloque": b, "post": []}
            unidades.append(u)
            ultimo_tabla = u
        elif t == "cita":
            libres.append(("cita", b["texto"]))
        i += 1
    if libres:
        C.texto_flujo(d, nombre, libres)
    for u in unidades:
        b = u["bloque"]
        etiqueta = nombre + (f" · {plano(u['titulo'])}" if u["titulo"] else "")
        if b["t"] == "ul":
            C.casillas_slide(d, etiqueta, [_limpia_campo(x) for x in b["items"]])
        else:
            if any("Comentario del instructor" in c for c in b["cab"]):
                continue                                  # formulario del instructor: no se proyecta
            cab = [c.replace("**", "") for c in b["cab"]]
            filas = b["filas"] or [[""] * len(cab)] * 2
            C.tabla_slides(d, etiqueta, cab, filas, _pesos(cab), intro=u["intro"], post=u["post"] or None,
                           min_fila=0.75 if _es_blanca(filas) else 0.5)


def _es_blanca(filas):
    celdas = [c for f in filas for c in f]
    return sum(1 for c in celdas if c.strip()) <= len(celdas) * 0.35


def _pesos(cab):
    n = len(cab)
    if cab[0] in ("#",):
        return [0.3] + [1.0] * (n - 1)
    if cab[0] in ("Pin",):
        return [0.5, 1.4, 0.5, 1.4] if n == 4 else [1.0] * n
    if cab[0] in ("Componente",):
        return [1.7, 0.7, 1.7, 0.7]
    if cab[0] in ("Minuto",):
        return [0.8, 2.6, 0.9]
    if cab[0] in ("Rol",):
        return [1.4, 1.0, 1.0, 1.0]
    if cab[0] in ("Criterio",):
        return [1.0, 1.4, 1.8, 1.8]
    return [1.0] * n


def plan(d, ctx, h3):
    cab, filas = None, None
    post = []
    for b in h3["bloques"]:
        if b["t"] == "tabla":
            cab, filas = b["cab"], b["filas"]
        elif b["t"] == "p":
            post.append(b["texto"])
    if cab:
        C.tabla_slides(d, "Plan de la sesión · 120 min", cab, filas, [0.6, 1.2, 4.0], post=post[:1])


def portada_sesion(d, nombre, subtitulo):
    s = d.m.nueva("seccion")
    pon_titulo(s, nombre, 3.53, 3.3, 12.4, 3.0, 44, CLARO, anchor="b")
    caja_texto(s, 3.53, 6.55, 12.4, 2.6, [P(subtitulo, pt=28, color=DORADO, bold=True, despues=0)])
    notas(s, nombre)
    d.registra()
    return s


def proyecto(d, ruta):
    g = M.parsear(ruta)
    por = {C.plano(s["titulo"]): s for s in g["secciones"]}

    def sec(prefijo):
        return next((s for t, s in por.items() if t.startswith(prefijo)), None)

    # ---------------------------------------------------------------- material común del proyecto
    d.abre_seccion("Proyecto final · reglas, retos y pines")
    d.ctx = C.Ctx("Sesiones 14 a 16 · Proyecto final")
    portada_sesion(d, "Sesiones 14 a 16 · Proyecto final", "Diseñar  ·  juntar  ·  probar  ·  mejorar  ·  explicar")
    ideas = [
        "**Diseñar.** Pasar de seguir instrucciones a diseñar: del problema a las entradas, el proceso y las salidas, y de ahí a los componentes y los pines.",
        "**Juntar.** Unir partes de varios programas sin que choquen sus pines ni sus nombres.",
        "**Probar con criterio.** Decir de antemano qué debe pasar y con qué número.",
        "**Mejorar en ciclos.** Probar, corregir y repetir.",
        "**Explicar.** Contar a otras personas lo que se hizo.",
    ]
    d.define_notas("Ideas del proyecto", [{"t": "p", "texto": g["meta"].get("Ideas nuevas de las sesiones", "")}])
    C.ideas_slide(d, "Ideas del proyecto", ideas)

    reglas = sec("Reglas del proyecto")
    if reglas:
        d.define_notas("Reglas del proyecto", reglas["bloques"])
        cuerpo = C.filtra_instructor(d, reglas["bloques"])
        items = [(b["t"], x) for b in cuerpo if b["t"] in ("ul", "ol") for x in b["items"]]
        C.texto_flujo(d, "Reglas del proyecto", items, pts=(26, 24, 22, 20, 18))

    for prefijo in ("Banco de retos", "Mapa de pines"):
        s = sec(prefijo)
        if not s:
            continue
        d.define_notas(prefijo, s["bloques"])
        C.compone(d, d.ctx, prefijo, s["bloques"], "generico")
        for h in s["hijas"]:
            d.define_notas(C.titulo_corto(h["titulo"]), h["bloques"])
            C.compone(d, d.ctx, h["titulo"], h["bloques"], "generico")

    pines = sec("Pines por reto")
    if pines:
        # cada reto: título (párrafo) + tabla + nota; la nota va debajo de la tabla
        bl, nuevos = [b for b in pines["bloques"] if b["t"] != "hr"], []
        for k, b in enumerate(bl):
            if b["t"] == "p" and k > 0 and bl[k - 1]["t"] == "tabla" and len(plano(b["texto"])) <= 320:
                nuevos.append({"t": "cita", "texto": b["texto"]})
            else:
                nuevos.append(b)
        d.define_notas("Pines por reto", pines["bloques"])
        C.compone(d, d.ctx, "Pines por reto", nuevos, "generico")

    for prefijo in ("Cómo juntar dos sketches", "La plantilla"):
        s = sec(prefijo)
        if s:
            d.define_notas(C.titulo_corto(s["titulo"]), s["bloques"])
            C.compone(d, d.ctx, s["titulo"], s["bloques"], "generico")

    # ---------------------------------------------------------------- las tres sesiones
    plan_h = {C.plano(h["titulo"])[:9]: h for h in (sec("Plan de las tres sesiones") or {"hijas": []})["hijas"]}
    guion = {}
    for clave, nombre, subt, hojas in (
        ("Sesión 14", "Sesión 14 · Diseño y armado", "Hoja A · diseño del proyecto", ["Hoja A"]),
        ("Sesión 15", "Sesión 15 · Pruebas y mejora", "Hoja B · pruebas con criterio", ["Hoja B"]),
        ("Sesión 16", "Sesión 16 · Exhibición y cierre", "Hojas C y D · exhibición, rúbrica y entrega", ["Hoja C", "Hoja D"]),
    ):
        d.abre_seccion(nombre)
        d.ctx = C.Ctx(nombre)
        portada_sesion(d, nombre, subt)
        h = plan_h.get(clave)
        if h:
            d.define_notas("Plan de la sesión", h["bloques"])
            plan(d, d.ctx, h)
        for hj in hojas:
            s = sec(hj)
            if not s:
                continue
            titulo_hoja = re.sub(r"\s*\*\(.*?\)\*\s*$", "", s["titulo"]).strip()
            titulo_hoja = C.titulo_corto(titulo_hoja)
            if s["bloques"]:
                d.define_notas(titulo_hoja, s["bloques"])
                hoja(d, d.ctx, titulo_hoja, s["bloques"])
            for h3 in s["hijas"]:
                d.define_notas(C.titulo_corto(h3["titulo"]), h3["bloques"])
                hoja(d, d.ctx, titulo_hoja + " · " + re.sub(r"\s*\*\(.*?\)\*\s*$", "", C.titulo_corto(h3["titulo"])).strip(), h3["bloques"])
        if clave == "Sesión 16":
            s = sec("Qué sigue")
            if s:
                d.define_notas("Qué sigue", s["bloques"])
                items = [(b["t"], x) for b in C.filtra_instructor(d, s["bloques"]) if b["t"] in ("ul", "ol") for x in b["items"]]
                C.texto_flujo(d, "Qué sigue", items, pts=(30, 28, 26, 24, 22, 20))
