"""Diagramas de cableado con pistas físicas (estilo «placa a la izquierda, cables de colores»).

Es el segundo estilo de diagrama del curso, además del de protoboard (diagrama.py):
  - placa a la izquierda, con los pines usados rotulados;
  - cables con el color real del jumper (naranja = señal, negro = GND, rojo = +5 V);
  - rieles como líneas largas, con un punto negro donde se unen tres o más cables;
  - componentes como cajas (resistencia, módulos) o símbolos (LED, diodo);
  - notas en tipografía monoespaciada: «cable negro», «riel GND», «pata larga (+)».

Igual que el motor de protoboard, VERIFICA lo que dibuja: si un cable cruza a otro sin
salto, si un punto cae sobre un cable de otra red, o si no se cumple una conexión pedida
con exigir()/prohibir(), el script se detiene en lugar de dibujar un circuito equivocado.

Unidad de dibujo: 1 U = 24 px en el PNG final (el lienzo se sobremuestrea 3 veces).
"""
import math
import os

from PIL import ImageFont

from diagrama import Canvas, LED_COL, TINTA, _UF, rounded_path

_MONO = {"Mono": "consola.ttf", "MonoBold": "consolab.ttf"}
NOTA = "#6b5d52"          # notas monoespaciadas (café grisáceo)
SUB = "#8a8a8a"           # subtítulos de componentes
CABLE = {"negro": "#262626", "rojo": "#c8202b", "naranja": "#c4690a", "morado": "#7b2cbf",
         "cafe": "#6a3f12", "verde": "#2a9d4a", "azul": "#1d5fd1", "amarillo": "#c99a00", "gris": "#6f7a8d", "rosa": "#c2437a", "celeste": "#1a98c4", "lima": "#7a9a1f"}


class Lienzo(Canvas):
    """Canvas que además sabe escribir con tipografía monoespaciada (Consolas)."""

    def font(self, size_u, weight="Medium"):
        if weight in _MONO:
            key = (round(size_u, 3), weight)
            if key not in self._f:
                ruta = os.path.join("C:\\Windows\\Fonts", _MONO[weight])
                self._f[key] = ImageFont.truetype(ruta, max(8, int(size_u * self.k)))
            return self._f[key]
        return super().font(size_u, weight)


def _sobre(p, a, b, tol=1e-6):
    """¿El punto p está estrictamente dentro del segmento ortogonal a-b (sin tocar los extremos)?"""
    if abs(a[0] - b[0]) < tol and abs(p[0] - a[0]) < tol:
        lo, hi = sorted((a[1], b[1]))
        return lo + tol < p[1] < hi - tol
    if abs(a[1] - b[1]) < tol and abs(p[1] - a[1]) < tol:
        lo, hi = sorted((a[0], b[0]))
        return lo + tol < p[0] < hi + 0 - tol
    return False


class Esquema:
    def __init__(self, w_u, h_u, px=24):
        self.c = Lienzo(w_u, h_u, px)
        self.T = {}              # terminal o nodo -> (x, y)
        self.uf = _UF()
        self.cables = []         # {color, pts, a, b}
        self.grado = {}          # cuántos cables llegan a cada terminal
        self.puntos = set()      # terminales que siempre llevan punto negro
        self._post = []          # dibujos que van encima de los cables

    # ------------------------------------------------------------ terminales y cables
    def terminal(self, nombre, x, y, punto=False):
        if nombre in self.T:
            raise ValueError(f"terminal repetida: {nombre}")
        self.T[nombre] = (x, y)
        self.uf.find(("n", nombre))
        if punto:
            self.puntos.add(nombre)

    def cable(self, color, a, b, via=()):
        """Cable de 'a' a 'b' (nombres de terminal) pasando por los puntos 'via'. Solo tramos horizontales o verticales."""
        pts = [self.T[a], *via, self.T[b]]
        for p, q in zip(pts, pts[1:]):
            if abs(p[0] - q[0]) > 1e-6 and abs(p[1] - q[1]) > 1e-6:
                raise ValueError(f"tramo diagonal en el cable {a} -> {b}: {p} -> {q}")
        self.cables.append({"color": color, "pts": pts, "a": a, "b": b})
        self.uf.union(("n", a), ("n", b))
        for t in (a, b):
            self.grado[t] = self.grado.get(t, 0) + 1

    def union_interna(self, a, b):
        """Une dos terminales que son el mismo punto eléctrico sin cable (p. ej. una resistencia y un LED en la misma columna)."""
        self.uf.union(("n", a), ("n", b))

    # ------------------------------------------------------------ verificación
    def conectados(self, a, b):
        return self.uf.find(("n", a)) == self.uf.find(("n", b))

    def exigir(self, a, b, msg):
        if not self.conectados(a, b):
            raise AssertionError("Falta conexión: " + msg)

    def prohibir(self, a, b, msg):
        if self.conectados(a, b):
            raise AssertionError("Cortocircuito: " + msg)

    def _revisar_geometria(self):
        """Busca cruces (los pone como saltos) y toques indebidos. Devuelve {(cable, tramo): [x...]}."""
        segs = []
        for ci, cab in enumerate(self.cables):
            for si, (p, q) in enumerate(zip(cab["pts"], cab["pts"][1:])):
                segs.append((ci, si, p, q))
        # 1. un terminal no puede caer en medio de un cable que no llega a él
        for nombre, p in self.T.items():
            for ci, si, a, b in segs:
                cab = self.cables[ci]
                if nombre in (cab["a"], cab["b"]):
                    continue
                if _sobre(p, a, b):
                    raise AssertionError(f"El terminal {nombre} cae sobre un cable ({cab['a']} -> {cab['b']}): "
                                         f"parte el cable en ese punto con un nodo")
        # 2. cruces entre cables distintos
        saltos = {}
        for i, (ci, si, p, q) in enumerate(segs):
            for cj, sj, r, s in segs[i + 1:]:
                if ci == cj:
                    continue
                horiz1, horiz2 = abs(p[1] - q[1]) < 1e-6, abs(r[1] - s[1]) < 1e-6
                if horiz1 == horiz2:
                    # paralelos: no pueden solaparse
                    if horiz1 and abs(p[1] - r[1]) < 1e-6:
                        a0, a1 = sorted((p[0], q[0]))
                        b0, b1 = sorted((r[0], s[0]))
                        if min(a1, b1) - max(a0, b0) > 1e-6:
                            raise AssertionError(f"Dos cables se montan uno sobre otro en y={p[1]}")
                    if (not horiz1) and abs(p[0] - r[0]) < 1e-6:
                        a0, a1 = sorted((p[1], q[1]))
                        b0, b1 = sorted((r[1], s[1]))
                        if min(a1, b1) - max(a0, b0) > 1e-6:
                            raise AssertionError(f"Dos cables se montan uno sobre otro en x={p[0]}")
                    continue
                (hc, hs, h0, h1), (vc, vs, v0, v1) = ((ci, si, p, q), (cj, sj, r, s)) if horiz1 else ((cj, sj, r, s), (ci, si, p, q))
                x, y = v0[0], h0[1]
                if _sobre((x, y), h0, h1) and _sobre((x, y), v0, v1):
                    na = ("n", self.cables[hc]["a"])
                    nb = ("n", self.cables[vc]["a"])
                    if self.uf.find(na) == self.uf.find(nb):
                        raise AssertionError(f"Dos cables de la misma red se cruzan en ({x}, {y}) sin nodo")
                    saltos.setdefault((hc, hs), []).append(x)
        return saltos

    # ------------------------------------------------------------ dibujo
    def _ruta(self, ci, saltos, r=0.6):
        pts = self.cables[ci]["pts"]
        out = [pts[0]]
        for si, (p, q) in enumerate(zip(pts, pts[1:])):
            sgn = 1 if q[0] > p[0] else -1
            for xc in sorted(saltos.get((ci, si), []), key=lambda v: v * sgn):
                for t in range(13):
                    th = math.pi * t / 12
                    out.append((xc - sgn * r * math.cos(th), p[1] - r * math.sin(th)))
            out.append(q)
        return rounded_path(out, 0.4)

    def dibujar(self, ruta_png):
        c = self.c
        saltos = self._revisar_geometria()
        for ci, cab in enumerate(self.cables):
            c.line(self._ruta(ci, saltos), CABLE[cab["color"]], 0.17, ends=True)
        for fn in self._post:
            fn()
        for nombre, g in self.grado.items():
            if g >= 3 or nombre in self.puntos:
                x, y = self.T[nombre]
                c.circle(x, y, 0.3, fill=TINTA)
        return c.save(ruta_png)

    # ------------------------------------------------------------ texto
    def titulo(self, texto, sub=None, x=1.5, y=1.3):
        c = self.c
        c.text(x, y, texto, 0.95, TINTA, "Bold", anchor="lm")
        if sub:
            c.text(x, y + 1.35, sub, 0.58, NOTA, "Mono", anchor="lm")

    def nota(self, x, y, texto, anchor="lm", color=NOTA, size=0.58, negrita=False):
        self.c.text(x, y, texto, size, color, "MonoBold" if negrita else "Mono", anchor=anchor)

    def etiqueta(self, x, y, nombre, sub=None, anchor="mm", color=TINTA):
        """Nombre en negrita y, debajo, una línea gris en monoespaciada."""
        self.c.text(x, y, nombre, 0.72, color, "Bold", anchor=anchor)
        if sub:
            self.c.text(x, y + 1.0, sub, 0.55, SUB, "Mono", anchor=anchor)

    # ------------------------------------------------------------ componentes
    def placa(self, x, y, w, h, nombre, pines):
        """Caja de la placa. pines = [(etiqueta, terminal, y)]; los pines salen por el borde derecho."""
        for etiqueta, term, py in pines:
            self.terminal(term, x + w, py)

        def dibujar():
            c = self.c
            c.rect(x, y, w, h, fill="#ffffff", outline=TINTA, width=0.12, r=0.8)
            lineas = nombre.split("\n")
            cx = x + (w - 2.4) / 2
            for i, s in enumerate(lineas):
                c.text(cx, y + h / 2 + (i - (len(lineas) - 1) / 2) * 1.2, s, 0.85, TINTA, "Bold")
            for etiqueta, term, py in pines:
                c.text(x + w - 0.8, py, etiqueta, 0.66, TINTA, "Bold", anchor="rm")
                c.circle(x + w, py, 0.26, fill=TINTA)
        self._post.append(dibujar)

    def resistencia(self, nombre, x, y, texto, w=4.6, h=1.7):
        """Caja horizontal con el valor dentro. Terminales nombre.a (izquierda) y nombre.b (derecha)."""
        self.terminal(nombre + ".a", x, y)
        self.terminal(nombre + ".b", x + w, y)

        def dibujar():
            self.c.rect(x, y - h / 2, w, h, fill="#ffffff", outline=TINTA, width=0.11, r=0.5)
            self.c.text(x + w / 2, y + 0.02, texto, 0.64, TINTA, "MonoBold")
        self._post.append(dibujar)

    def led(self, nombre, x, y, color, w=3.6):
        """LED horizontal: ánodo (+) a la izquierda, cátodo (−) a la derecha. Terminales nombre.a y nombre.k."""
        self.terminal(nombre + ".a", x, y)
        self.terminal(nombre + ".k", x + w, y)

        def dibujar():
            c = self.c
            x0, x1 = x + 0.8, x + w - 0.8
            c.line([(x, y), (x0, y)], TINTA, 0.17, ends=False)
            c.line([(x1, y), (x + w, y)], TINTA, 0.17, ends=False)
            c.poly([(x0, y - 1.15), (x0, y + 1.15), (x1, y)], fill=LED_COL[color], outline=TINTA, width=0.12)
            c.line([(x1, y - 1.15), (x1, y + 1.15)], TINTA, 0.17, ends=False)
            for dx in (0.15, 1.0):                      # flechitas de luz
                a = (x0 + 0.35 + dx, y - 1.45 - dx * 0.2)
                b = (a[0] + 0.85, a[1] - 0.85)
                c.line([a, b], TINTA, 0.11, ends=False)
                c.poly([b, (b[0] - 0.42, b[1] + 0.12), (b[0] - 0.12, b[1] + 0.42)], fill=TINTA)
        self._post.append(dibujar)

    def boton(self, nombre, x, y, w=6.0):
        """Pulsador horizontal (símbolo): contacto abierto y émbolo con tapa. Terminales nombre.a (izquierda) y nombre.b (derecha)."""
        self.terminal(nombre + ".a", x, y)
        self.terminal(nombre + ".b", x + w, y)

        def dibujar():
            c = self.c
            xa, xb = x + 1.5, x + w - 1.5
            c.line([(x, y), (xa, y)], TINTA, 0.17, ends=False)
            c.line([(xb, y), (x + w, y)], TINTA, 0.17, ends=False)
            for px_ in (xa, xb):
                c.circle(px_, y, 0.28, fill="#ffffff", outline=TINTA, width=0.12)
            c.line([(xa, y - 0.15), (xb - 0.25, y - 1.25)], TINTA, 0.17, ends=False)      # lámina levantada (abierto)
            xm = (xa + xb) / 2 - 0.1
            c.line([(xm, y - 0.7), (xm, y - 2.3)], TINTA, 0.14, ends=False)                # émbolo
            c.line([(xm - 1.0, y - 2.3), (xm + 1.0, y - 2.3)], TINTA, 0.2, ends=False)     # tapa
        self._post.append(dibujar)

    def potenciometro(self, nombre, x, y0, y1, largo_cursor=4.0):
        """Potenciómetro vertical (símbolo de divisor de voltaje): extremo de arriba nombre.a, extremo de abajo nombre.b
        y cursor (flecha) por la izquierda nombre.w, a media altura."""
        ym = (y0 + y1) / 2
        self.terminal(nombre + ".a", x, y0)
        self.terminal(nombre + ".b", x, y1)
        self.terminal(nombre + ".w", x - largo_cursor, ym)

        def dibujar():
            c = self.c
            n = 8
            ya, yb = y0 + 1.0, y1 - 1.0
            seg = (yb - ya) / n
            pts = [(x, y0), (x, ya)]
            for i in range(n):
                pts.append((x + (-0.85 if i % 2 == 0 else 0.85), ya + seg * (i + 0.5)))
            pts += [(x, yb), (x, y1)]
            c.line(pts, TINTA, 0.16, ends=False)
            xp = x - largo_cursor
            c.line([(xp, ym), (x - 1.35, ym)], TINTA, 0.16, ends=False)                  # cursor
            c.poly([(x - 0.85, ym), (x - 1.75, ym - 0.5), (x - 1.75, ym + 0.5)], fill=TINTA)
        self._post.append(dibujar)

    def etiqueta_red(self, terminal, red, texto, color, lado="izq", largo=2.4):
        """Une un terminal con una red que se reparte por el riel (el pin 5V o el GND de la placa) sin dibujar el cable completo:
        un trozo corto con el nombre de la red («5 V», «GND»). 'red' es el nombre del terminal del pin de la placa.
        Cuenta como conexión para exigir() y prohibir()."""
        x, y = self.T[terminal]
        dx = -largo if lado == "izq" else largo
        self.union_interna(terminal, red)

        def dibujar():
            self.c.line([(x, y), (x + dx, y)], CABLE[color], 0.17, ends=False)
            self.c.text(x + dx + (-0.3 if dx < 0 else 0.3), y, texto, 0.62, CABLE[color], "MonoBold", anchor="rm" if dx < 0 else "lm")
        self._post.append(dibujar)

    def resistencia_v(self, nombre, x, y0, y1, marca=None):
        """Resistencia vertical (zigzag). Terminales nombre.a (arriba) y nombre.b (abajo).
        marca: None, 'luz' (flechas de luz: fotorresistencia) o 'calor' (signo de temperatura: termistor)."""
        self.terminal(nombre + ".a", x, y0)
        self.terminal(nombre + ".b", x, y1)

        def dibujar():
            c = self.c
            n = 8
            ya, yb = y0 + 1.0, y1 - 1.0
            seg = (yb - ya) / n
            pts = [(x, y0), (x, ya)]
            for i in range(n):
                pts.append((x + (-0.85 if i % 2 == 0 else 0.85), ya + seg * (i + 0.5)))
            pts += [(x, yb), (x, y1)]
            c.line(pts, TINTA, 0.16, ends=False)
            ym = (y0 + y1) / 2
            if marca == "luz":
                for dy in (-0.9, 0.5):
                    a = (x + 3.6, ym + dy - 1.2)
                    b = (x + 1.5, ym + dy)
                    c.line([a, b], "#d98200", 0.13, ends=False)
                    c.poly([b, (b[0] + 0.55, b[1] - 0.2), (b[0] + 0.25, b[1] - 0.6)], fill="#d98200")
            elif marca == "calor":
                c.line([(x - 2.2, ym + 1.6), (x - 1.2, ym + 1.6), (x + 1.2, ym - 1.6), (x + 2.2, ym - 1.6)], TINTA, 0.12, ends=False)
                c.text(x + 3.0, ym - 1.6, "t°", 0.6, TINTA, "Mono", anchor="lm")
        self._post.append(dibujar)

    def bloque(self, nombre, x, y, w, h, titulo, sub=None, terminales=()):
        """Caja genérica (módulo, transistor...). terminales = [(nombre, 'izq'|'der'|'sup'|'inf', posición_en_U, rótulo)]."""
        pos = {}
        for tn, lado, d, _ in terminales:
            px, py = {"izq": (x, y + d), "der": (x + w, y + d), "sup": (x + d, y), "inf": (x + d, y + h)}[lado]
            self.terminal(nombre + "." + tn, px, py)
            pos[tn] = (px, py, lado)

        def dibujar():
            c = self.c
            c.rect(x, y, w, h, fill="#ffffff", outline=TINTA, width=0.11, r=0.6)
            c.text(x + w / 2, y + h / 2 - (0.5 if sub else 0), titulo, 0.78, TINTA, "Bold")
            if sub:
                c.text(x + w / 2, y + h / 2 + 0.6, sub, 0.55, SUB, "Mono")
            for tn, lado, d, rot in terminales:
                px, py, _ = pos[tn]
                dx, dy = {"izq": (0.5, 0), "der": (-0.5, 0), "sup": (0, 0.7), "inf": (0, -0.7)}[lado]
                an = {"izq": "lm", "der": "rm", "sup": "mt", "inf": "mb"}[lado]
                c.text(px + dx, py + dy, rot, 0.6, TINTA, "Bold", anchor=an)
        self._post.append(dibujar)
