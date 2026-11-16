"""Motor de diagramas para el curso de Arduino (vista de protoboard y esquemas).

Dibuja con Pillow (sobremuestreado para que quede suave) y comprueba las conexiones:
cada circuito se arma con cables y componentes puestos en agujeros concretos del
protoboard, y el motor verifica que lo dibujado coincide con lo esperado (por ejemplo,
que el LED queda entre el pin 8 y GND). Si algo no coincide, falla en lugar de dibujar
un circuito equivocado.

Unidad de dibujo: 1 U = 2.54 mm (la separación entre agujeros de un protoboard).
Tipografía: Montserrat si está instalada; si no, Segoe UI.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

SS = 3  # sobremuestreo

# ---------------------------------------------------------------- colores
COL = {
    "negro": "#1d1d1f", "rojo": "#d62828", "naranja": "#f77f00", "amarillo": "#f2b705",
    "verde": "#2a9d4a", "azul": "#277da1", "morado": "#7b2cbf", "blanco": "#e5e5e5",
    "cafe": "#7b4a12", "gris": "#8d99ae",
}
LED_COL = {"rojo": "#e63946", "amarillo": "#ffd60a", "verde": "#38b000", "azul": "#1d70f5", "blanco": "#f4f4f4"}
BAND = ["#111111", "#7b3f00", "#d00000", "#f77f00", "#ffd60a", "#2a9d4a", "#1d70f5", "#7b2cbf", "#8d99ae", "#f1f1f1"]
GOLD = "#c9a227"
VINO = "#731F35"       # color institucional de la plantilla
TINTA = "#222222"
GRIS_T = "#666666"

_FONT_DIR = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "Windows", "Fonts")
_WEIGHTS = {"Regular": "Montserrat-Regular.otf", "Medium": "Montserrat-Medium.otf",
            "SemiBold": "Montserrat-SemiBold.otf", "Bold": "Montserrat-Bold.otf"}
_FALLBACK = {"Regular": "segoeui.ttf", "Medium": "segoeui.ttf", "SemiBold": "segoeuib.ttf", "Bold": "segoeuib.ttf"}


def _font_file(weight):
    p = os.path.join(_FONT_DIR, _WEIGHTS[weight])
    if os.path.exists(p):
        return p
    return os.path.join("C:\\Windows\\Fonts", _FALLBACK[weight])


def _lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def rounded_path(pts, r=1.0, n=10):
    """Convierte una poligonal en una trayectoria con las esquinas redondeadas."""
    out = [pts[0]]
    for i in range(1, len(pts) - 1):
        p0, p1, p2 = pts[i - 1], pts[i], pts[i + 1]
        l1 = math.dist(p0, p1)
        l2 = math.dist(p1, p2)
        if l1 == 0 or l2 == 0:
            continue
        d = min(r, l1 / 2, l2 / 2)
        a = _lerp(p1, p0, d / l1)
        b = _lerp(p1, p2, d / l2)
        for k in range(n + 1):
            t = k / n
            q0 = _lerp(a, p1, t)
            q1 = _lerp(p1, b, t)
            out.append(_lerp(q0, q1, t))
    out.append(pts[-1])
    return out


class Canvas:
    def __init__(self, w_u, h_u, px=32, bg="#FFFFFF"):
        self.k = px * SS
        self.w_u, self.h_u, self.px = w_u, h_u, px
        self.img = Image.new("RGB", (int(w_u * self.k), int(h_u * self.k)), bg)
        self.d = ImageDraw.Draw(self.img)
        self._f = {}

    # ---- utilidades
    def P(self, p):
        return (p[0] * self.k, p[1] * self.k)

    def font(self, size_u, weight="Medium"):
        key = (round(size_u, 3), weight)
        if key not in self._f:
            self._f[key] = ImageFont.truetype(_font_file(weight), max(8, int(size_u * self.k)))
        return self._f[key]

    # ---- primitivas
    def rect(self, x, y, w, h, fill=None, outline=None, width=0.08, r=0.0):
        self.d.rounded_rectangle([x * self.k, y * self.k, (x + w) * self.k, (y + h) * self.k],
                                 radius=r * self.k, fill=fill, outline=outline,
                                 width=max(1, int(width * self.k)) if outline else 0)

    def circle(self, cx, cy, r, fill=None, outline=None, width=0.08):
        self.d.ellipse([(cx - r) * self.k, (cy - r) * self.k, (cx + r) * self.k, (cy + r) * self.k],
                       fill=fill, outline=outline, width=max(1, int(width * self.k)) if outline else 0)

    def line(self, pts, color, width=0.2, ends=True):
        px = [self.P(p) for p in pts]
        w = max(1, int(width * self.k))
        self.d.line(px, fill=color, width=w, joint="curve")
        if ends:
            for p in (pts[0], pts[-1]):
                self.circle(p[0], p[1], width / 2, fill=color)

    def poly(self, pts, fill=None, outline=None, width=0.08):
        self.d.polygon([self.P(p) for p in pts], fill=fill, outline=None)
        if outline:
            self.line(list(pts) + [pts[0]], outline, width, ends=False)

    def text(self, x, y, s, size=0.8, color=TINTA, weight="Medium", anchor="mm"):
        self.d.text((x * self.k, y * self.k), s, font=self.font(size, weight), fill=color, anchor=anchor)

    def text_len(self, s, size=0.8, weight="Medium"):
        return self.font(size, weight).getlength(s) / self.k

    def vtext(self, x, y_start, s, size=0.6, color="#ffffff", weight="Medium", down=True):
        """Texto vertical que empieza en y_start y se centra en x."""
        f = self.font(size, weight)
        L = int(f.getlength(s)) + 4
        H = int(size * self.k * 1.4)
        mask = Image.new("L", (L, H), 0)
        ImageDraw.Draw(mask).text((2, H / 2), s, font=f, fill=255, anchor="lm")
        mask = mask.rotate(-90 if down else 90, expand=True)
        w, h = mask.size
        cx = int(x * self.k - w / 2)
        cy = int(y_start * self.k) if down else int(y_start * self.k - h)
        self.img.paste(color, (cx, cy), mask)

    def badge(self, x, y, n, color=VINO, r=0.62):
        self.circle(x, y, r + 0.12, fill="#ffffff")
        self.circle(x, y, r, fill=color)
        self.text(x, y + 0.02, str(n), size=r * 1.25, color="#ffffff", weight="Bold")

    def callout(self, box_x, box_y, lines, target=None, color=VINO, size=0.62, w=None):
        """Cuadro de texto; la línea sale del borde del cuadro hacia 'target'."""
        lines = [lines] if isinstance(lines, str) else lines
        tw = max(self.text_len(s, size, "SemiBold") for s in lines)
        bw = w or (tw + 1.2)
        bh = len(lines) * size * 1.55 + 0.7
        if target is not None:
            cx, cy = box_x + bw / 2, box_y + bh / 2
            dx, dy = target[0] - cx, target[1] - cy
            k = min((bw / 2) / abs(dx) if dx else 1e9, (bh / 2) / abs(dy) if dy else 1e9)
            self.line([(cx + dx * k, cy + dy * k), target], color, 0.12, ends=False)
            self.circle(target[0], target[1], 0.22, fill=color)
        self.rect(box_x, box_y, bw, bh, fill="#ffffff", outline=color, width=0.1, r=0.35)
        for i, s in enumerate(lines):
            self.text(box_x + bw / 2, box_y + 0.35 + size * 0.78 + i * size * 1.55, s, size, TINTA, "SemiBold")
        return bw, bh

    def header(self, titulo, subtitulo=None):
        self.rect(0, 0, self.w_u, 3.3 if subtitulo else 2.6, fill=VINO)
        self.text(1.2, 1.25 if subtitulo else 1.3, titulo, 1.15, "#ffffff", "Bold", anchor="lm")
        if subtitulo:
            self.text(1.2, 2.5, subtitulo, 0.62, "#f0d9a0", "Medium", anchor="lm")

    def save(self, path):
        out = self.img.resize((self.img.width // SS, self.img.height // SS), Image.LANCZOS)
        out.save(path, optimize=True)
        return out.size


# ---------------------------------------------------------------- union-find para verificar
class _UF:
    def __init__(self):
        self.p = {}

    def find(self, a):
        self.p.setdefault(a, a)
        while self.p[a] != a:
            self.p[a] = self.p[self.p[a]]
            a = self.p[a]
        return a

    def union(self, a, b):
        self.p[self.find(a)] = self.find(b)


# ---------------------------------------------------------------- Arduino UNO (vista superior, USB a la izquierda)
class Arduino:
    W, H = 27.0, 21.0
    # posición (pulgadas desde el borde izquierdo) de cada pin en las dos barras superiores
    TOP = (["SCL", "SDA", "AREF", "GND", "D13", "D12", "D11", "D10", "D9", "D8"],
           ["D7", "D6", "D5", "D4", "D3", "D2", "D1", "D0"])
    BOT = (["NC", "IOREF", "RESET", "3V3", "5V", "GND", "GND", "VIN"], ["A0", "A1", "A2", "A3", "A4", "A5"])
    PWM = {"D3", "D5", "D6", "D9", "D10", "D11"}

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.pos = {}   # nombre -> (x, y, lado)
        top_x = [0.74 + 0.10 * i for i in range(10)] + [1.90 + 0.10 * i for i in range(8)]
        for name, xi in zip(self.TOP[0] + self.TOP[1], top_x):
            self.pos[name] = (x + xi * 10, y + 1.3, "T")
        bot_names = self.BOT[0] + self.BOT[1]
        bot_x = [1.00 + 0.10 * i for i in range(8)] + [1.90 + 0.10 * i for i in range(6)]
        for i, (name, xi) in enumerate(zip(bot_names, bot_x)):
            key = name if name not in self.pos else f"{name}_{i}"
            self.pos[key] = (x + xi * 10, y + self.H - 1.3, "B")
        self.pos["GND_T"] = self.pos.pop("GND")  # el GND de la barra superior
        # los GND de la barra inferior
        gnds = [k for k in self.pos if k.startswith("GND_") and k != "GND_T"]
        # los nombres duplicados "GND" de la barra inferior quedaron como GND_5 y GND_6
        self.gnd_names = ["GND_T"] + gnds
        self.pos["GND"] = self.pos["GND_T"]  # alias cómodo

    def xy(self, name):
        return self.pos[name][:2]

    def node(self, name):
        if name in self.gnd_names or name == "GND":
            return "GND"
        return name

    def draw(self, c, used=None, highlight_L=False):
        used = used or {}
        x, y, W, H = self.x, self.y, self.W, self.H
        # tarjeta
        c.rect(x, y, W, H, fill="#1b6aa5", outline="#0f4c7a", width=0.15, r=0.9)
        # USB tipo B y conector de alimentación
        c.rect(x - 1.0, y + 4.4, 6.6, 4.8, fill="#c9ced4", outline="#8b9299", width=0.1, r=0.2)
        c.rect(x - 1.0, y + 12.8, 5.8, 5.4, fill="#2b2b2b", outline="#111", width=0.1, r=0.3)
        # reset (esquina superior izquierda)
        c.rect(x + 0.8, y + 0.6, 2.6, 2.6, fill="#d9d9d9", outline="#8b9299", width=0.08, r=0.3)
        c.circle(x + 2.1, y + 1.9, 0.8, fill="#d62828")
        # cristal, chip principal y nombre
        c.rect(x + 8.0, y + 9.6, 3.0, 1.2, fill="#c9ced4", outline="#8b9299", width=0.06, r=0.5)
        c.rect(x + 11.0, y + 10.9, 13.5, 3.0, fill="#1c1c1c", outline="#000", width=0.06, r=0.2)
        c.text(x + 17.7, y + 12.4, "ATMEGA328P", 0.6, "#bdbdbd", "Medium")
        c.text(x + 17.5, y + 8.0, "ARDUINO UNO", 1.4, "#ffffff", "Bold")
        # LED integrado "L" (pin 13), justo debajo de la etiqueta del 13
        lx, ly = self.xy("D13")[0], y + 5.1
        if highlight_L:
            c.circle(lx, ly, 1.7, fill="#ffe08a")
        c.rect(lx - 0.5, ly - 0.35, 1.0, 0.7, fill="#ffb703" if highlight_L else "#caa24a", outline="#7a5b00", width=0.05)
        c.text(lx + 1.3, ly, "L", 0.7, "#ffffff", "Bold")
        # barras de pines (hembras)
        for (x0, x1, yy) in ((self.xy("SCL")[0], self.xy("D8")[0], y + 1.3), (self.xy("D7")[0], self.xy("D0")[0], y + 1.3),
                             (self.xy("NC")[0], self.xy("VIN")[0], y + H - 1.3), (self.xy("A0")[0], self.xy("A5")[0], y + H - 1.3)):
            c.rect(x0 - 0.5, yy - 0.62, (x1 - x0) + 1.0, 1.24, fill="#222222", r=0.1)
        for name, (px_, py_, side) in self.pos.items():
            if name == "GND":
                continue
            c.rect(px_ - 0.2, py_ - 0.2, 0.4, 0.4, fill="#8a8a8a", r=0.06)
        # etiquetas
        for name, (px_, py_, side) in self.pos.items():
            if name == "GND":
                continue
            base = name.split("_")[0]
            label = {"D13": "13", "D12": "12", "D11": "~11", "D10": "~10", "D9": "~9", "D8": "8", "D7": "7", "D6": "~6",
                     "D5": "~5", "D4": "4", "D3": "~3", "D2": "2", "D1": "1", "D0": "0", "3V3": "3.3V"}.get(base, base)
            if base == "NC":
                continue
            color = "#ffffff"
            if name in used:
                col = used[name]
                if side == "T":
                    c.rect(px_ - 0.5, py_ + 0.75, 1.0, c.text_len(label, 0.62, "Bold") + 0.9, fill=col, r=0.3)
                else:
                    c.rect(px_ - 0.5, py_ - 0.75 - c.text_len(label, 0.62, "Bold") - 0.9, 1.0, c.text_len(label, 0.62, "Bold") + 0.9, fill=col, r=0.3)
            if side == "T":
                c.vtext(px_, py_ + 1.2, label, 0.62, color, "Bold" if name in used else "Medium", down=True)
            else:
                c.vtext(px_, py_ - 1.2, label, 0.62, color, "Bold" if name in used else "Medium", down=False)


# ---------------------------------------------------------------- Protoboard (vista parcial, 'cols' columnas)
class Breadboard:
    TOP_ROWS, BOT_ROWS = "abcde", "fghij"

    def __init__(self, x, y, cols=30):
        self.x, self.y, self.cols = x, y, cols
        self.W, self.H = cols + 4.0, 20.6
        ry = {"a": 4.5, "b": 5.5, "c": 6.5, "d": 7.5, "e": 8.5, "f": 11.5, "g": 12.5, "h": 13.5, "i": 14.5, "j": 15.5}
        self.row_y = {k: y + v for k, v in ry.items()}
        self.rails = {("T", "+"): y + 0.9, ("T", "-"): y + 1.9, ("B", "-"): y + 18.2, ("B", "+"): y + 19.2}

    def hole(self, col, row):
        return (self.x + 2.0 + (col - 1) * 1.0, self.row_y[row])

    def rail_hole(self, side, kind, col):
        return (self.x + 2.0 + (col - 1) * 1.0, self.rails[(side, kind)])

    def node(self, col, row):
        return ("S", col, "T" if row in self.TOP_ROWS else "B")

    def rail_node(self, side, kind):
        return ("R", side, kind)

    def draw(self, c):
        x, y, W, H = self.x, self.y, self.W, self.H
        c.rect(x, y, W, H, fill="#ece8dc", outline="#b3ae9c", width=0.12, r=0.5)
        c.rect(x + 1.2, y + 9.45, W - 2.4, 1.1, fill="#d6d1c0", r=0.2)          # canal central
        # rieles
        for (side, kind), yy in self.rails.items():
            colr = "#d62828" if kind == "+" else "#1d5fd1"
            c.rect(x + 1.2, yy - 0.5, W - 2.4, 0.14, fill=colr)
            c.text(x + 0.75, yy, kind.replace("-", "\u2212"), 0.7, colr, "Bold")
            c.text(x + W - 0.75, yy, kind.replace("-", "\u2212"), 0.7, colr, "Bold")
            for col in range(1, self.cols + 1):
                if col % 6 == 0:
                    continue
                hx, hy = self.rail_hole(side, kind, col)
                c.rect(hx - 0.17, hy - 0.17, 0.34, 0.34, fill="#33322c", r=0.05)
        # agujeros y rotulos
        for row in self.TOP_ROWS + self.BOT_ROWS:
            for col in range(1, self.cols + 1):
                hx, hy = self.hole(col, row)
                c.rect(hx - 0.17, hy - 0.17, 0.34, 0.34, fill="#33322c", r=0.05)
            c.text(x + 0.9, self.row_y[row], row, 0.62, GRIS_T, "SemiBold")
            c.text(x + W - 0.9, self.row_y[row], row, 0.62, GRIS_T, "SemiBold")
        for col in range(1, self.cols + 1):
            hx, _ = self.hole(col, "a")
            c.text(hx, y + 3.3, str(col), 0.5, GRIS_T, "SemiBold")
            c.text(hx, y + 10.0, str(col), 0.5, "#8d8671", "SemiBold")


# ---------------------------------------------------------------- Circuito
def fmt_hole(col, row):
    return f"{row}{col}"


class Circuit:
    def __init__(self, canvas, ard, bb):
        self.c, self.ard, self.bb = canvas, ard, bb
        self.uf = _UF()
        self.used_holes = {}
        self.used_pins = {}
        self.items = []       # dibujos diferidos
        self.table = []       # filas (paso, texto)
        self.elems = {}       # nombre -> terminales
        for g in self.ard.gnd_names:
            self.uf.union(("A", "GND"), ("A", g))

    # nodos
    def _node(self, ref):
        kind = ref[0]
        if kind == "ard":
            return ("A", self.ard.node(ref[1]))
        if kind == "bb":
            return self.bb.node(ref[1], ref[2])
        if kind == "rail":
            return self.bb.rail_node(ref[1], ref[2])
        raise ValueError(ref)

    def _xy(self, ref):
        kind = ref[0]
        if kind == "ard":
            return self.ard.xy(ref[1])
        if kind == "bb":
            return self.bb.hole(ref[1], ref[2])
        if kind == "rail":
            return self.bb.rail_hole(ref[1], ref[2], ref[3])
        raise ValueError(ref)

    def _name(self, ref):
        kind = ref[0]
        if kind == "ard":
            n = self.ard.node(ref[1])
            return {"D13": "pin 13"}.get(n, f"pin {n[1:]}" if n.startswith("D") else ("GND de la placa" if n == "GND" else n))
        if kind == "bb":
            return f"agujero {fmt_hole(ref[1], ref[2])}"
        if kind == "rail":
            return "riel \u2212 (azul)" if ref[2] == "-" else "riel + (rojo)"
        raise ValueError(ref)

    def _occupy(self, ref, quien):
        if ref[0] in ("bb", "rail"):
            key = (ref[0],) + ref[1:]
            if key in self.used_holes:
                raise ValueError(f"{quien}: el agujero {key} ya lo ocupa {self.used_holes[key]}")
            self.used_holes[key] = quien

    # ---- cables
    def wire(self, a, b, color, via=0.5, step=None, nombre=None, badge=None):
        a = ("ard", "GND_T") if a == ("ard", "GND") else a
        b = ("ard", "GND_T") if b == ("ard", "GND") else b
        self._occupy(a, f"cable {color}")
        self._occupy(b, f"cable {color}")
        self.uf.union(self._node(a), self._node(b))
        for r in (a, b):
            if r[0] == "ard":
                self.used_pins[r[1]] = COL[color]
        pa, pb = self._xy(a), self._xy(b)
        # el cable sale de la placa en vertical, corre por un canal horizontal y entra en vertical
        y_ch = pa[1] - (pa[1] - pb[1]) * via if abs(pa[1] - pb[1]) > 3 else (pa[1] + pb[1]) / 2
        pts = [pa, (pa[0], y_ch), (pb[0], y_ch), pb] if pa[0] != pb[0] else [pa, pb]
        self.items.append(("wire", pts, COL[color], step, badge))
        self.table.append((step, f"Cable {color}", f"{self._name(a)}", f"{self._name(b)}"))

    # ---- componentes
    def resistor(self, a, b, ohms, step=None, nombre="R"):
        self._occupy(("bb",) + a, nombre)
        self._occupy(("bb",) + b, nombre)
        self.elems[nombre] = (("bb",) + a, ("bb",) + b)
        self.items.append(("resistor", self.bb.hole(*a), self.bb.hole(*b), ohms, step))
        self.table.append((step, f"Resistencia {ohms} \u03a9", self._name(("bb",) + a), self._name(("bb",) + b)))

    def led(self, anodo, catodo, color, step=None, nombre="LED"):
        self._occupy(("bb",) + anodo, nombre)
        self._occupy(("bb",) + catodo, nombre)
        self.elems[nombre] = (("bb",) + anodo, ("bb",) + catodo)
        self.items.append(("led", self.bb.hole(*anodo), self.bb.hole(*catodo), LED_COL[color], step))
        self.table.append((step, f"LED {color}", f"pata larga (+): {self._name(('bb',) + anodo)}", f"pata corta (\u2212): {self._name(('bb',) + catodo)}"))

    # ---- verificación
    def conectados(self, a, b):
        return self.uf.find(self._node(a)) == self.uf.find(self._node(b))

    def exigir(self, a, b, msg):
        if not self.conectados(a, b):
            raise AssertionError("Falta conexión: " + msg)

    def prohibir(self, a, b, msg):
        if self.conectados(a, b):
            raise AssertionError("Cortocircuito: " + msg)

    # ---- dibujo
    def draw(self):
        c = self.c
        self.bb.draw(c)
        self.ard.draw(c, used={k: v for k, v in self.used_pins.items()})
        for it in self.items:
            if it[0] == "resistor":
                _, pa, pb, ohms, step = it
                self._draw_resistor(pa, pb, ohms, step)
            elif it[0] == "led":
                _, pa, pb, color, step = it
                self._draw_led(pa, pb, color, step)
        for it in self.items:
            if it[0] == "wire":
                _, pts, color, step, badge = it
                path = rounded_path(pts, 1.1)
                c.line(path, "#1a1a1a", 0.5, ends=True)
                c.line(path, color, 0.34, ends=True)
                for p in (pts[0], pts[-1]):
                    c.circle(p[0], p[1], 0.26, fill="#d9d9d9", outline="#555", width=0.05)
                if step:
                    if badge:
                        bx, by = badge
                    elif len(pts) == 4:
                        bx, by = (pts[1][0] + pts[2][0]) / 2, pts[1][1]
                    else:
                        bx, by = (pts[0][0] + pts[1][0]) / 2, (pts[0][1] + pts[1][1]) / 2
                    c.badge(bx, by, step)

    def _draw_resistor(self, pa, pb, ohms, step):
        c = self.c
        c.line([pa, pb], "#b0b0b0", 0.16, ends=True)
        cx, cy = (pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2
        length = min(3.0, max(2.2, abs(pb[0] - pa[0]) - 1.2))
        c.rect(cx - length / 2, cy - 0.55, length, 1.1, fill="#e5c79a", outline="#9a7b4f", width=0.06, r=0.5)
        digits = self._bands(ohms)
        for i, col in enumerate(digits + [GOLD]):
            bx = cx - length / 2 + 0.55 + i * (length - 1.1) / 3.2
            c.rect(bx - 0.11, cy - 0.55, 0.22, 1.1, fill=col)
        if step:
            c.badge(cx, cy + 1.6, step)

    @staticmethod
    def _bands(ohms):
        s = str(int(ohms))
        mult = len(s) - 2
        return [BAND[int(s[0])], BAND[int(s[1])], BAND[mult]]

    def _draw_led(self, pa, pb, color, step):
        c = self.c
        # patas: anodo (larga) en pa, catodo (corta) en pb
        cx = (pa[0] + pb[0]) / 2
        cy = min(pa[1], pb[1]) - 2.5
        c.line([pa, (pa[0], cy + 1.0)], "#c8c8c8", 0.2, ends=True)
        c.line([pb, (pb[0], cy + 1.0)], "#c8c8c8", 0.2, ends=True)
        c.circle(cx, cy, 1.55, fill=color, outline="#3a3a3a", width=0.07)
        side = 1 if pb[0] > pa[0] else -1          # el lado plano va del lado del catodo
        c.rect(cx + side * 1.38 - 0.09, cy - 0.9, 0.18, 1.8, fill="#f2f2f2")
        c.circle(cx - 0.5, cy - 0.5, 0.28, fill="#ffffff")
        my = (cy + 1.55 + pa[1]) / 2 + 0.1
        izq = pa[0] < pb[0]                        # ánodo a la izquierda (lo normal) o cátodo a la izquierda
        for (px_, sign, colr) in ((pa[0], "+", VINO), (pb[0], "−", "#1d5fd1")):
            es_anodo = px_ == pa[0]
            ox = (-0.95 if es_anodo else 0.95) * (1 if izq else -1)
            c.circle(px_ + ox, my, 0.5, fill=colr)
            c.text(px_ + ox, my + 0.02, sign, 0.8, "#ffffff", "Bold")
        if step:
            c.badge(cx, cy - 2.5, step)
