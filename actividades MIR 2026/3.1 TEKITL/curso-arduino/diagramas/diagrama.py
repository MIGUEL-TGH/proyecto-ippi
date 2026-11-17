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
    "cafe": "#7b4a12", "gris": "#8d99ae", "rosa": "#e5739b", "celeste": "#4cc9f0", "lima": "#a7c957",
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
                if col in ("#f2b705", "#e5e5e5"):          # colores claros: letra oscura para que se lea
                    color = "#222222"
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


# ---------------------------------------------------------------- Sensor PIR HC-SR501 (módulo fuera del protoboard)
def dibujar_pir(c, x, y):
    """Módulo visto por el lado de la cúpula, girado 90°: las patas salen por la izquierda.
    Placa de 9.4 x 12.6 U (24 x 32 mm); arriba GND, en medio OUT, abajo VCC; conectores de cables macho-hembra."""
    yc = y + 6.3
    c.rect(x, y, 9.4, 12.6, fill="#2f8f55", outline="#1b5c37", width=0.1, r=0.5)
    for (hx, hy) in ((x + 0.8, y + 0.8), (x + 8.6, y + 0.8), (x + 0.8, y + 11.8), (x + 8.6, y + 11.8)):
        c.circle(hx, hy, 0.38, fill="#e9e9e0", outline="#1b5c37", width=0.05)
    # cúpula (lente de Fresnel)
    c.circle(x + 5.0, yc, 4.1, fill="#f5f5f2", outline="#cfcfc8", width=0.08)
    c.circle(x + 5.0, yc, 2.9, outline="#dcdcd5", width=0.05)
    for k in range(6):
        a = k * math.pi / 3
        c.line([(x + 5.0 + math.cos(a) * 1.0, yc + math.sin(a) * 1.0), (x + 5.0 + math.cos(a) * 2.9, yc + math.sin(a) * 2.9)],
               "#dcdcd5", 0.05, ends=False)
    c.circle(x + 5.0, yc, 1.0, fill="#ffffff", outline="#dcdcd5", width=0.05)
    # patas y conectores
    for nombre, dy in (("GND", -1.0), ("OUT", 0.0), ("VCC", 1.0)):
        yy = yc + dy
        c.rect(x - 0.9, yy - 0.12, 1.2, 0.24, fill="#c9a227")
        c.rect(x - 3.6, yy - 0.46, 2.8, 0.92, fill="#1e1e1e", r=0.15)
        c.text(x - 2.2, yy + 0.02, nombre, 0.46, "#ffffff", "Bold")


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
        self.mods = {}        # módulos fuera del protoboard: nombre -> {pin: (x, y)}
        self._unions = []     # uniones de los cables (para rehacer la verificación con otras hipótesis)
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
        if kind == "mod":
            return ("M", ref[1], ref[2])
        raise ValueError(ref)

    def _xy(self, ref):
        kind = ref[0]
        if kind == "ard":
            return self.ard.xy(ref[1])
        if kind == "bb":
            return self.bb.hole(ref[1], ref[2])
        if kind == "rail":
            return self.bb.rail_hole(ref[1], ref[2], ref[3])
        if kind == "mod":
            return self.mods[ref[1]][ref[2]]
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
        if kind == "mod":
            return f"pata {ref[2]} del sensor {ref[1]}"
        raise ValueError(ref)

    def _occupy(self, ref, quien):
        if ref[0] in ("bb", "rail"):
            key = (ref[0],) + ref[1:]
            if key in self.used_holes:
                raise ValueError(f"{quien}: el agujero {key} ya lo ocupa {self.used_holes[key]}")
            self.used_holes[key] = quien

    # ---- cables
    def wire(self, a, b, color, via=0.5, step=None, nombre=None, badge=None, ruta=None):
        """Cable de a a b. Por omisión sale en vertical, corre por un canal horizontal y entra en vertical;
        con 'ruta' (lista de puntos intermedios) se dibuja el camino indicado."""
        a = ("ard", "GND_T") if a == ("ard", "GND") else a
        b = ("ard", "GND_T") if b == ("ard", "GND") else b
        self._occupy(a, f"cable {color}")
        self._occupy(b, f"cable {color}")
        self.uf.union(self._node(a), self._node(b))
        self._unions.append((self._node(a), self._node(b)))
        for r in (a, b):
            if r[0] == "ard":
                self.used_pins[r[1]] = COL[color]
        pa, pb = self._xy(a), self._xy(b)
        if ruta is not None:
            pts = [pa, *ruta, pb]
        else:
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

    def boton(self, col, step=None, nombre="B"):
        """Botón de 4 patas (6 x 6 mm) cruzando el canal central: patas en las columnas col y col+2,
        filas e (arriba del canal) y f (abajo). Devuelve las cuatro patas [(col,e), (col+2,e), (col,f), (col+2,f)]."""
        patas = [(col, "e"), (col + 2, "e"), (col, "f"), (col + 2, "f")]
        for p in patas:
            self._occupy(("bb",) + p, nombre)
        self.elems[nombre] = [("bb",) + p for p in patas]
        self.items.append(("boton", col, step))
        self.table.append((step, "Botón (4 patas)", f"arriba del canal: {fmt_hole(col, 'e')} y {fmt_hole(col + 2, 'e')}",
                           f"abajo del canal: {fmt_hole(col, 'f')} y {fmt_hole(col + 2, 'f')}"))
        return patas

    def zumbador(self, col, tipo, step=None, nombre="BZ"):
        """Zumbador de dos patas separadas 3 agujeros (7,6 mm), en las columnas col y col+3 de la fila f
        (abajo del canal). tipo: 'activo' (pata + a la izquierda) o 'pasivo'. Devuelve las dos patas."""
        a, b = (col, "f"), (col + 3, "f")
        for p in (a, b):
            self._occupy(("bb",) + p, nombre)
        self.elems[nombre] = [("bb",) + a, ("bb",) + b]
        self.items.append(("zumbador", col, tipo, step))
        izq = "pata + (la larga, con el signo +)" if tipo == "activo" else "una pata"
        self.table.append((step, f"Zumbador {tipo}", f"{izq}: {fmt_hole(*a)}", f"la otra pata: {fmt_hole(*b)}"))
        return [a, b]

    def potenciometro(self, col, step=None, nombre="POT"):
        """Potenciómetro de 10 kΩ (trimmer) con sus 3 patas en línea, separadas 2 agujeros (5 mm), en las columnas
        col, col+2 y col+4 de la fila f. Devuelve [extremo izquierdo, centro (cursor), extremo derecho]."""
        patas = [(col, "f"), (col + 2, "f"), (col + 4, "f")]
        for p in patas:
            self._occupy(("bb",) + p, nombre)
        self.elems[nombre] = [("bb",) + p for p in patas]
        self.items.append(("pot", col, step))
        self.table.append((step, "Potenciómetro (3 patas)", f"extremos: {fmt_hole(*patas[0])} y {fmt_hole(*patas[2])}",
                           f"centro (cursor): {fmt_hole(*patas[1])}"))
        return patas

    def sensor2(self, col, tipo, step=None, nombre="SENS"):
        """Sensor resistivo de dos patas (fotorresistencia 'ldr' o termistor 'ntc') en la fila f, patas en las columnas col y col+2.
        Devuelve las dos patas. No tiene polaridad."""
        patas = [(col, "f"), (col + 2, "f")]
        for p in patas:
            self._occupy(("bb",) + p, nombre)
        self.elems[nombre] = [("bb",) + p for p in patas]
        self.items.append(("sensor2", col, tipo, step))
        et = "Fotorresistencia (LDR)" if tipo == "ldr" else "Termistor NTC"
        self.table.append((step, et, f"una pata: {fmt_hole(*patas[0])}", f"la otra pata: {fmt_hole(*patas[1])}"))
        return patas

    def pir(self, x, y):
        """Sensor PIR HC-SR501 visto por el lado de la cúpula y girado: sus 3 patas salen por la izquierda
        (arriba GND, en medio OUT, abajo VCC). (x, y) = esquina superior izquierda de la placa (9.4 x 12.6 U).
        Los terminales están en el extremo izquierdo de los conectores de los cables macho-hembra."""
        yc = y + 6.3
        self.modulo("PIR", {"GND": (x - 3.6, yc - 1.0), "OUT": (x - 3.6, yc), "VCC": (x - 3.6, yc + 1.0)})
        self.items.append(("pir", x, y))

    def modulo(self, nombre, pines):
        self.mods[nombre] = pines

    def dibujo(self, fn):
        """Dibujo propio (un módulo fuera del protoboard): fn(canvas) se ejecuta antes de dibujar los cables."""
        self.items.append(("fn", fn))

    def comprobar_boton(self, nombre, a, b, msg):
        """Comprueba que el botón NO une a con b cuando está suelto y SÍ los une cuando se presiona,
        con las dos formas posibles de venir unidas las patas por dentro:
          A) las dos patas de una misma columna (de lado a lado del canal) están unidas; al presionar se unen las dos columnas;
          B) las dos patas de un mismo lado del canal están unidas; al presionar se unen los dos lados.
        Así el circuito funciona sin importar cuál sea la del botón real."""
        c1e, c2e, c1f, c2f = self.elems[nombre]
        hipotesis = {
            "A (patas de lado a lado unidas)": ([(c1e, c1f), (c2e, c2f)], (c1e, c2e)),
            "B (patas del mismo lado unidas)": ([(c1e, c2e), (c1f, c2f)], (c1e, c1f)),
        }
        for etiqueta, (internas, contacto) in hipotesis.items():
            base = self._unions + [(self._node(p), self._node(q)) for p, q in internas]
            suelto = self._uf_con(base)
            if suelto.find(self._node(a)) == suelto.find(self._node(b)):
                raise AssertionError(f"Con el botón suelto (hipótesis {etiqueta}) ya están unidos: {msg}")
            pres = self._uf_con(base + [(self._node(contacto[0]), self._node(contacto[1]))])
            if pres.find(self._node(a)) != pres.find(self._node(b)):
                raise AssertionError(f"Con el botón presionado (hipótesis {etiqueta}) no se unen: {msg}")

    def _uf_con(self, uniones):
        uf = _UF()
        for g in self.ard.gnd_names:
            uf.union(("A", "GND"), ("A", g))
        for p, q in uniones:
            uf.union(p, q)
        return uf

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
            elif it[0] == "boton":
                _, col, step = it
                self._draw_boton(col, step)
            elif it[0] == "zumbador":
                _, col, tipo, step = it
                self._draw_zumbador(col, tipo, step)
            elif it[0] == "pot":
                _, col, step = it
                self._draw_potenciometro(col, step)
            elif it[0] == "sensor2":
                _, col, tipo, step = it
                self._draw_sensor2(col, tipo, step)
            elif it[0] == "fn":
                it[1](self.c)
            elif it[0] == "pir":
                _, px_, py_ = it
                dibujar_pir(self.c, px_, py_)
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

    def _draw_boton(self, col, step):
        """Botón de 6 x 6 mm visto desde arriba, con sus cuatro patas en los agujeros."""
        c = self.c
        x1, ye = self.bb.hole(col, "e")
        x2, _ = self.bb.hole(col + 2, "e")
        _, yf = self.bb.hole(col, "f")
        cx, cy = (x1 + x2) / 2, (ye + yf) / 2
        for px_, py_ in ((x1, ye), (x2, ye), (x1, yf), (x2, yf)):
            c.line([(px_, py_), (px_, cy)], "#b8b8b8", 0.26, ends=True)
        c.rect(cx - 1.35, cy - 1.1, 2.7, 2.2, fill="#2e2e2e", outline="#111111", width=0.08, r=0.35)
        c.circle(cx, cy, 0.78, fill="#4b4b4b", outline="#111111", width=0.06)
        c.circle(cx - 0.22, cy - 0.22, 0.25, fill="#808080")
        if step:
            c.badge(cx, yf + 1.9, step)

    def _draw_zumbador(self, col, tipo, step):
        """Zumbador de 12 mm visto desde arriba; sus patas quedan debajo del cuerpo, en los agujeros."""
        c = self.c
        x1, yf = self.bb.hole(col, "f")
        x2, _ = self.bb.hole(col + 3, "f")
        cx, cy, r = (x1 + x2) / 2, yf, 2.36
        if tipo == "activo":
            c.circle(cx, cy, r, fill="#1f2733", outline="#0b0f14", width=0.08)
            c.circle(cx, cy, r - 0.35, outline="#35435a", width=0.06)
            c.circle(cx, cy, 1.55, fill="#f4f4f1", outline="#c9c9c2", width=0.05)          # etiqueta blanca
            c.circle(cx - 0.75, cy, 0.55, outline="#2a4d9b", width=0.07)                     # signo + (lado de la pata +)
            c.line([(cx - 1.0, cy), (cx - 0.5, cy)], "#2a4d9b", 0.09, ends=False)
            c.line([(cx - 0.75, cy - 0.25), (cx - 0.75, cy + 0.25)], "#2a4d9b", 0.09, ends=False)
        else:
            c.circle(cx, cy, r, fill="#161616", outline="#050505", width=0.08)
            c.circle(cx, cy, r - 0.3, outline="#2c2c2c", width=0.06)
            c.circle(cx, cy, 0.5, fill="#5b5b5b", outline="#0a0a0a", width=0.05)             # orificio
            c.circle(cx - 0.9, cy - 0.9, 0.25, fill="#3a3a3a")
        if step:
            c.badge(cx, cy - r - 0.9, step)

    def _draw_potenciometro(self, col, step):
        """Potenciómetro trimmer visto desde arriba: cuerpo negro con la ranura del rotor; las patas quedan debajo, en la fila f."""
        c = self.c
        x_c, yf = self.bb.hole(col + 2, "f")
        w, h = 5.9, 5.5
        x0, y0 = x_c - w / 2, yf + 0.85 - h
        c.rect(x0, y0, w, h, fill="#1f1f22", outline="#050505", width=0.08, r=1.4)
        for sx in (-1, 1):                                                  # topes del cuerpo
            c.circle(x_c + sx * (w / 2 - 0.55), yf + 0.2, 0.28, fill="#3a3a3f")
        cy = y0 + 3.0
        c.circle(x_c, cy, 1.75, fill="#2b2b30", outline="#4d4d55", width=0.07)          # rotor
        c.circle(x_c, cy, 1.4, outline="#3d3d44", width=0.05)
        c.line([(x_c - 1.25, cy + 0.55), (x_c + 1.25, cy - 0.55)], "#8e8e96", 0.36, ends=False)   # ranura del desarmador
        c.rect(x_c - 1.3, y0 + 0.45, 2.6, 0.95, fill="#0f0f12", r=0.15)
        c.text(x_c, y0 + 0.93, "B103", 0.5, "#d9d9d9", "Bold")
        if step:
            c.badge(x_c, y0 - 0.9, step)

    def _draw_sensor2(self, col, tipo, step):
        """Fotorresistencia (disco con pista en zigzag) o termistor NTC (gota de epoxi), vistos desde arriba; las patas entran en la fila f."""
        c = self.c
        x1, yf = self.bb.hole(col, "f")
        x2, _ = self.bb.hole(col + 2, "f")
        xm = (x1 + x2) / 2
        cy = yf - 1.7
        for px_ in (x1, x2):
            c.line([(px_, yf), (px_, cy + 0.6)], "#b8b8b8", 0.22, ends=True)
        if tipo == "ldr":
            r = 1.55
            c.circle(xm, cy, r, fill="#d9b779", outline="#6b4a12", width=0.08)
            zz = [(xm - 0.95, cy - 0.7), (xm + 0.95, cy - 0.7), (xm - 0.95, cy - 0.25), (xm + 0.95, cy - 0.25),
                  (xm - 0.95, cy + 0.2), (xm + 0.95, cy + 0.2), (xm - 0.95, cy + 0.65), (xm + 0.95, cy + 0.65)]
            for k in range(0, len(zz), 2):
                c.line([zz[k], zz[k + 1]], "#7a4a10", 0.1, ends=False)
            for k in range(1, len(zz) - 1, 2):
                c.line([zz[k], zz[k + 1]], "#7a4a10", 0.1, ends=False)
            top = cy - r
        else:
            c.circle(xm, cy, 1.2, fill="#2b2b2b", outline="#050505", width=0.07)
            c.circle(xm - 0.35, cy - 0.35, 0.3, fill="#5a5a5a")
            top = cy - 1.2
        if step:
            c.badge(xm, top - 0.9, step)

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
