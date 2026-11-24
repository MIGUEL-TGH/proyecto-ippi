"""Lee una guía de sesión (Markdown) y la convierte en una estructura de bloques para armar las láminas.

Estructura que devuelve parsear(ruta):
  {"titulo": "Sesión 6 · Luz y decisiones",
   "meta": {"Prácticas y tiempos estimados": "...", "Sketches": "...", ...},     # líneas en negritas del encabezado
   "secciones": [Seccion, ...]}                                                  # un H2 cada una
Seccion = {"nivel": 2, "titulo": "...", "bloques": [...], "hijas": [Seccion(nivel 3), ...]}
Bloque  = {"t": "p"|"ul"|"ol"|"tabla"|"codigo"|"img"|"cita"|"hr", ...}
  p      -> {"t": "p", "texto": "..."}
  ul/ol  -> {"t": "ul", "items": ["...", ...], "casillas": True/False}
  tabla  -> {"t": "tabla", "cab": [...], "filas": [[...], ...]}
  codigo -> {"t": "codigo", "lang": "cpp", "texto": "..."}
  img    -> {"t": "img", "alt": "...", "ruta": "<ruta absoluta>"}
  cita   -> {"t": "cita", "texto": "..."}
El texto conserva el marcado en línea (**negritas**, *cursivas*, `código`): runs_md() de construye.py lo convierte en formato.
"""
import os
import re


def _celdas(linea):
    linea = linea.strip()
    if linea.startswith("|"):
        linea = linea[1:]
    if linea.endswith("|"):
        linea = linea[:-1]
    # las barras dentro de `código` no separan celdas
    partes, actual, en_codigo = [], "", False
    for ch in linea:
        if ch == "`":
            en_codigo = not en_codigo
        if ch == "|" and not en_codigo:
            partes.append(actual.strip())
            actual = ""
        else:
            actual += ch
    partes.append(actual.strip())
    return partes


def _es_separador(linea):
    return bool(re.match(r"^\|?[\s:\-|]+\|?$", linea.strip())) and "-" in linea


def parsear_bloques(lineas, base):
    bloques, i = [], 0
    while i < len(lineas):
        l = lineas[i]
        if not l.strip():
            i += 1
            continue
        if l.startswith("```"):
            lang = l[3:].strip()
            i += 1
            buf = []
            while i < len(lineas) and not lineas[i].startswith("```"):
                buf.append(lineas[i])
                i += 1
            i += 1
            bloques.append({"t": "codigo", "lang": lang, "texto": "\n".join(buf).rstrip("\n")})
            continue
        if re.match(r"^---+\s*$", l):
            bloques.append({"t": "hr"})
            i += 1
            continue
        m = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$", l)
        if m:
            ruta = os.path.normpath(os.path.join(base, m.group(2)))
            bloques.append({"t": "img", "alt": m.group(1), "ruta": ruta})
            i += 1
            continue
        if l.startswith("|") and i + 1 < len(lineas) and _es_separador(lineas[i + 1]):
            cab = _celdas(l)
            i += 2
            filas = []
            while i < len(lineas) and lineas[i].startswith("|"):
                filas.append(_celdas(lineas[i]))
                i += 1
            bloques.append({"t": "tabla", "cab": cab, "filas": filas})
            continue
        if l.startswith(">"):
            buf = []
            while i < len(lineas) and lineas[i].startswith(">"):
                buf.append(re.sub(r"^>\s?", "", lineas[i]))
                i += 1
            bloques.append({"t": "cita", "texto": " ".join(s.strip() for s in buf if s.strip())})
            continue
        m = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", l)
        if m:
            ordenada = m.group(2)[0].isdigit()
            items, casillas = [], False
            while i < len(lineas):
                mm = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", lineas[i])
                if mm:
                    txt = mm.group(3)
                    if re.match(r"^\[[ xX]\]\s", txt):
                        casillas = True
                        txt = txt[4:]
                    items.append(txt.strip())
                    i += 1
                elif lineas[i].startswith("  ") and lineas[i].strip() and items:   # continuación de la viñeta
                    items[-1] += " " + lineas[i].strip()
                    i += 1
                else:
                    break
            bloques.append({"t": "ol" if ordenada else "ul", "items": items, "casillas": casillas})
            continue
        # párrafo: líneas seguidas hasta una línea vacía o un bloque nuevo
        buf = [l.strip()]
        i += 1
        while i < len(lineas) and lineas[i].strip() and not re.match(r"^(```|---+\s*$|!\[|\||>|\s*([-*]|\d+\.)\s)", lineas[i]):
            buf.append(lineas[i].strip())
            i += 1
        bloques.append({"t": "p", "texto": " ".join(buf)})
    return bloques


def _quita_sangria_de_listas(lineas):
    """Un bloque (tabla, párrafo) con sangría de 2 a 4 espacios debajo de un elemento de lista pertenece a esa lista;
    aquí se le quita la sangría para que se reconozca como bloque propio (la lámina lo muestra después de la lista)."""
    salida, en_lista, en_codigo = [], False, False
    for l in lineas:
        if l.lstrip().startswith("```"):
            en_codigo = not en_codigo
            salida.append(l)
            continue
        if en_codigo:
            salida.append(l)
            continue
        es_item = re.match(r"^\s*([-*]|\d+\.)\s+", l) is not None
        if es_item and not l.startswith(" "):
            en_lista = True
            salida.append(l)
        elif en_lista and l.startswith("  ") and l.strip() and not es_item:
            salida.append(l.lstrip())
        else:
            if l.strip() and not l.startswith(" ") and not es_item:
                en_lista = False
            salida.append(l)
    return salida


def parsear(ruta):
    base = os.path.dirname(os.path.abspath(ruta))
    with open(ruta, encoding="utf-8") as f:
        lineas = f.read().replace("\r\n", "\n").split("\n")
    lineas = _quita_sangria_de_listas(lineas)
    titulo = ""
    cuerpo_ini = 0
    for k, l in enumerate(lineas):
        if l.startswith("# "):
            titulo = l[2:].strip()
            cuerpo_ini = k + 1
            break
    # trozos por encabezado H2/H3
    trozos = []          # (nivel, titulo, [lineas])
    actual = (1, titulo, [])
    en_codigo = False
    for l in lineas[cuerpo_ini:]:
        if l.startswith("```"):
            en_codigo = not en_codigo
        m = re.match(r"^(##|###) (.+)$", l) if not en_codigo else None
        if m:
            trozos.append(actual)
            actual = (len(m.group(1)), m.group(2).strip(), [])
        else:
            actual[2].append(l)
    trozos.append(actual)

    meta, secciones = {}, []
    for nivel, tit, ls in trozos:
        if nivel == 1:
            # el encabezado trae una línea por dato: «**Clave:** valor»
            for l in ls:
                mm = re.match(r"^\*\*(.+?)\*\*:?\s*(.*)$", l.strip())
                if mm:
                    meta[mm.group(1).strip().rstrip(":")] = mm.group(2).strip()
            continue
        sec = {"nivel": nivel, "titulo": tit, "bloques": parsear_bloques(ls, base), "hijas": []}
        if nivel == 2:
            secciones.append(sec)
        elif secciones:
            secciones[-1]["hijas"].append(sec)
    return {"titulo": titulo, "meta": meta, "secciones": secciones}


if __name__ == "__main__":
    import sys
    g = parsear(sys.argv[1])
    print("TÍTULO:", g["titulo"])
    for k, v in g["meta"].items():
        print(f"  meta[{k}] = {v[:90]}")
    for s in g["secciones"]:
        print(f"\n## {s['titulo']}   bloques={[b['t'] for b in s['bloques']]}")
        for h in s["hijas"]:
            print(f"   ### {h['titulo'][:60]:60}  {[b['t'] + (str(len(b.get('items', b.get('filas', [])))) if b['t'] in ('ul','ol','tabla') else '') for b in h['bloques']]}")
