"""Genera los diagramas del curso (PNG) en esta misma carpeta.

Uso:  python generar_diagramas.py            (genera todos)
      python generar_diagramas.py P02        (genera solo los de P02)
Requiere Pillow (pip install pillow). Cada circuito se verifica al construirse:
si un cable o componente no coincide con lo esperado, el script se detiene con un mensaje.
"""
import os
import sys

from diagrama import (Arduino, Breadboard, Canvas, Circuit, COL, GRIS_T, TINTA, VINO, LED_COL)
from esquema import Esquema

AQUI = os.path.dirname(os.path.abspath(__file__))


def _leyenda(c, x, y, items):
    """items: [(color_hex, texto)]"""
    c.text(x, y, "Colores de los cables", 0.62, GRIS_T, "SemiBold", anchor="lm")
    for i, (hexcol, txt) in enumerate(items):
        yy = y + 1.4 + i * 1.3
        c.rect(x, yy - 0.3, 2.2, 0.6, fill=hexcol, outline="#1a1a1a", width=0.05, r=0.3)
        c.text(x + 3.0, yy, txt, 0.62, TINTA, "Medium", anchor="lm")


# ------------------------------------------------------------------ P01
def p01():
    c = Canvas(44, 35)
    c.header("P01 · Blink con el LED integrado", "Sin protoboard ni cables: solo la placa y el cable USB")
    ard = Arduino(12.0, 10.5)
    ard.draw(c, used={"D13": "#d98200"}, highlight_L=True)
    # cable USB hacia la computadora
    px, py = ard.x - 1.0, ard.y + 6.8
    c.rect(px - 3.4, py - 1.9, 3.4, 3.8, fill="#2b2b2b", r=0.4)
    c.line([(px - 3.4, py), (3.5, py)], "#2b2b2b", 0.8)
    c.badge(px - 1.7, py - 3.2, 1)
    c.callout(1.0, py + 3.0, ["Cable USB: va a la", "computadora y también", "da la energía"], target=(5.0, py + 0.2), size=0.62)
    # LED L
    lx, ly = ard.xy("D13")[0], ard.y + 5.1
    txt = ["LED integrado «L»:", "está conectado al pin 13"]
    bw = max(c.text_len(t, 0.62, "SemiBold") for t in txt) + 1.2
    c.callout(lx - bw / 2, 4.8, txt, target=(lx, ly - 0.2), size=0.62)
    c.badge(lx + 3.4, ly, 2)
    c.save(os.path.join(AQUI, "P01_blink_led_integrado.png"))
    print("P01 listo")


# ------------------------------------------------------------------ P02
def p02():
    c = Canvas(38.5, 58.0)
    c.header("P02 · LED externo que parpadea", "Conexión en protoboard (vista desde arriba, parte izquierda del protoboard)")
    bb = Breadboard(3.0, 4.6, cols=30)
    ard = Arduino(bb.x + 2.6, bb.y + bb.H + 6.2)
    circ = Circuit(c, ard, bb)

    # paso 1: LED (pata larga en 22g, pata corta en 23g)
    circ.led(anodo=(22, "g"), catodo=(23, "g"), color="rojo", step=1)
    # paso 2: resistencia de 220 ohm entre 18h y 22h
    circ.resistor((18, "h"), (22, "h"), 220, step=2)
    # paso 3: cable negro de la pata corta al riel azul (-)
    circ.wire(("bb", 23, "j"), ("rail", "B", "-", 23), "negro", step=3)
    # paso 4: cable negro de GND de la placa al riel azul (-)
    circ.wire(("ard", "GND"), ("rail", "B", "-", 13), "negro", via=0.45, step=4)
    # paso 5: cable naranja del pin 8 a la columna de la resistencia
    circ.wire(("ard", "D8"), ("bb", 18, "j"), "naranja", step=5, badge=(bb.hole(18, "j")[0] + 1.3, ard.y - 2.0))

    # verificación del circuito: pin 8 -> R -> LED -> GND, sin cortos
    r_a, r_b = circ.elems["R"]
    l_a, l_c = circ.elems["LED"]
    circ.exigir(("ard", "D8"), r_a, "el pin 8 debe llegar a la resistencia")
    circ.exigir(r_b, l_a, "la resistencia debe llegar a la pata larga (+) del LED")
    circ.exigir(l_c, ("ard", "GND"), "la pata corta (-) del LED debe llegar a GND")
    circ.prohibir(r_a, r_b, "la resistencia no puede estar en corto")
    circ.prohibir(l_a, l_c, "el LED no puede estar en corto")
    circ.prohibir(("ard", "D8"), ("ard", "GND"), "pin 8 y GND no pueden tocarse")
    circ.prohibir(("ard", "5V"), ("ard", "GND"), "5V y GND no pueden tocarse")
    circ.draw()

    # llamadas de atención (en las zonas vacías del protoboard)
    ax, ay = bb.hole(22, "g")
    kx, ky = bb.hole(23, "g")
    cy_led = min(ay, ky) - 2.5
    my = (cy_led + 1.55 + ay) / 2 + 0.1
    c.callout(bb.x + 7.5, bb.y + 5.0, ["Pata larga (+)", "va hacia la resistencia"], target=(ax - 0.95 - 0.5, my), size=0.6)
    c.callout(kx + 1.6, bb.y + 5.0, ["Pata corta (−)", "lado plano del LED"], target=(kx + 0.95 + 0.5, my), size=0.6)
    rx, ry = bb.hole(22, "h")[0] + 0.0, bb.hole(22, "h")[1]
    c.callout(kx + 0.6, bb.row_y["h"] - 0.5, ["Resistencia 220 Ω", "rojo · rojo · café · dorado"],
              target=(rx - 1.4, ry), size=0.55)

    _leyenda(c, ard.x + 0.5, ard.y + ard.H + 2.0, [(COL["negro"], "GND  (−, tierra)"), (COL["naranja"], "Señal del pin 8")])
    c.text(c.w_u - 1.2, c.h_u - 1.2, "Los números y letras son las coordenadas de cada agujero", 0.5, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P02_led_parpadeo.png"))
    print("P02 listo")
    for fila in sorted(circ.table, key=lambda t: t[0] or 99):
        print("  ", fila)


# ------------------------------------------------------------------ símbolos para esquemas
def _sym_gnd(c, x, y):
    c.line([(x, y), (x, y + 1.0)], TINTA, 0.16, ends=False)
    for i, w in enumerate((2.2, 1.4, 0.6)):
        c.line([(x - w / 2, y + 1.0 + i * 0.5), (x + w / 2, y + 1.0 + i * 0.5)], TINTA, 0.16, ends=False)


def _sym_resistor(c, x0, x1, y, etiqueta):
    n = 6
    seg = (x1 - x0 - 2.0) / n
    pts = [(x0, y), (x0 + 1.0, y)]
    for i in range(n):
        pts.append((x0 + 1.0 + seg * (i + 0.5), y + (-0.8 if i % 2 == 0 else 0.8)))
    pts += [(x1 - 1.0, y), (x1, y)]
    c.line(pts, TINTA, 0.16, ends=False)
    c.text((x0 + x1) / 2, y - 1.8, etiqueta, 0.8, TINTA, "SemiBold")


def _sym_led(c, x, y, color):
    # triángulo hacia la derecha y barra (cátodo)
    c.poly([(x, y - 1.3), (x, y + 1.3), (x + 2.2, y)], fill=color, outline=TINTA, width=0.14)
    c.line([(x + 2.2, y - 1.3), (x + 2.2, y + 1.3)], TINTA, 0.16, ends=False)
    for dy in (-1.9, -1.0):
        c.line([(x + 0.6, y + dy), (x + 1.7, y + dy - 0.9)], TINTA, 0.12, ends=False)
        c.poly([(x + 1.7, y + dy - 0.9), (x + 1.25, y + dy - 0.75), (x + 1.55, y + dy - 0.4)], fill=TINTA)


def esquema_p02():
    c = Canvas(34, 17)
    c.header("P02 · Esquema eléctrico", "El mismo circuito, dibujado como símbolos")
    y = 9.5
    # terminal del pin 8
    c.rect(1.5, y - 1.7, 5.6, 3.4, fill=VINO, r=0.5)
    c.text(4.3, y - 0.45, "Pin 8", 0.9, "#ffffff", "Bold")
    c.text(4.3, y + 0.75, "salida", 0.55, "#f0d9a0", "Medium")
    c.line([(7.1, y), (10.0, y)], TINTA, 0.16, ends=False)
    _sym_resistor(c, 10.0, 16.0, y, "220 Ω")
    c.line([(16.0, y), (19.0, y)], TINTA, 0.16, ends=False)
    _sym_led(c, 19.0, y, LED_COL["rojo"])
    c.text(20.4, y - 3.2, "LED", 0.8, TINTA, "SemiBold")
    c.line([(21.2, y), (27.0, y), (27.0, y + 3.0)], TINTA, 0.16, ends=False)
    _sym_gnd(c, 27.0, y + 3.0)
    c.text(27.0, y + 6.0, "GND", 0.8, TINTA, "SemiBold")
    # flecha de corriente
    c.line([(8.2, y + 3.4), (21.0, y + 3.4)], VINO, 0.14, ends=False)
    c.poly([(21.0, y + 3.4 - 0.45), (21.0, y + 3.4 + 0.45), (21.9, y + 3.4)], fill=VINO)
    c.text(14.6, y + 4.6, "corriente cuando el pin 8 está en HIGH (5 V)", 0.58, VINO, "SemiBold")
    # lecturas
    c.callout(10.3, 4.1, ["Limita la corriente", "(protege al LED)"], target=(13.0, y - 1.0), size=0.55)
    c.callout(22.0, 4.1, ["Ánodo (+) a la izquierda", "cátodo (−) a la derecha"], target=(21.2, y - 1.4), size=0.55)
    c.text(1.5, 15.3, "I = (5 V − 2 V del LED) ÷ 220 Ω ≈ 14 mA", 0.62, GRIS_T, "SemiBold", anchor="lm")
    c.save(os.path.join(AQUI, "P02_led_parpadeo_esquema.png"))
    print("P02 esquema listo")


# ------------------------------------------------------------------ estilo «cableado» (esquema.py)
# Colores de cable por pin (los mismos en el diagrama de protoboard y en el de cableado)
CABLE_PIN = {8: "naranja", 9: "morado", 10: "cafe"}


def _rama(E, y, pin, color_led, nombre_led, rotulo_pin, x_tap, y_riel, con_pata=False, primera=False):
    """Una fila: pin -> resistencia 220 Ω -> LED -> (cable negro) -> riel GND. Devuelve nada; registra todo en E."""
    cab = CABLE_PIN[pin]
    r, led, tap = f"R{pin}", f"LED{pin}", f"TAP{pin}"
    E.resistencia(r, 15.0, y, "220 Ω")
    E.led(led, 23.0, y, color_led)
    E.terminal(tap, x_tap, y_riel)
    E.cable(cab, f"D{pin}", r + ".a")
    E.cable(cab, r + ".b", led + ".a")
    E.cable("negro", led + ".k", tap, via=[(x_tap, y)])
    E.nota(9.5, y - 1.45, f"pin {pin} (salida)")
    E.nota(9.5, y + 1.45, f"cable {cab}")
    E.etiqueta(17.3, y - 2.3, "Resistencia")
    E.nota(17.3, y + 1.9, "rojo · rojo · café", anchor="mm")
    E.etiqueta(24.8, y - 3.7, nombre_led)
    if con_pata:
        E.nota(24.8, y + 3.0, "pata larga (+) a la izquierda", anchor="mm")
        E.nota(24.8, y + 4.0, "pata corta (−), lado plano", anchor="mm")


def _riel(E, y_riel, taps, x_ini=9.0):
    """Riel GND: desde el pin GND de la placa hasta el último tap. taps = nombres de terminal de izquierda a derecha."""
    previo = "GND"
    for t in taps:
        E.cable("negro", previo, t)
        previo = t


def cableado_p02():
    E = Esquema(36, 19.8)
    E.titulo("P02 · LED que parpadea", "esquema de conexiones · el mismo circuito del diagrama de protoboard")
    E.placa(1.5, 5.0, 7.5, 11.8, "Arduino\nUNO R3", [("D8", "D8", 8.5), ("GND", "GND", 14.5)])
    _rama(E, 8.5, 8, "rojo", "LED rojo", "D8", 31.0, 14.5, con_pata=True)
    _riel(E, 14.5, ["TAP8"])
    E.nota(31.6, 11.6, "cable negro")
    E.nota(9.5, 16.0, "cable negro", anchor="lm")
    E.nota(20.5, 16.0, "riel GND: la tira azul (−)", anchor="lm")
    E.nota(1.5, 18.8, "Con el pin 8 en HIGH (5 V):   I = (5 V − 2 V del LED) ÷ 220 Ω ≈ 14 mA", color="#8a8a8a")
    # verificación
    E.exigir("D8", "R8.a", "el pin 8 debe llegar a la resistencia")
    E.exigir("R8.b", "LED8.a", "la resistencia debe llegar a la pata larga (+) del LED")
    E.exigir("LED8.k", "GND", "la pata corta (−) del LED debe llegar a GND")
    E.prohibir("D8", "GND", "pin 8 y GND no pueden tocarse")
    E.prohibir("R8.a", "R8.b", "la resistencia no puede estar en corto")
    E.prohibir("LED8.a", "LED8.k", "el LED no puede estar en corto")
    E.dibujar(os.path.join(AQUI, "P02_led_parpadeo_cableado.png"))
    print("P02 cableado listo")


def cableado_p03():
    E = Esquema(36, 27.8)
    E.titulo("P03 · Dos LED que se alternan", "esquema de conexiones · cada LED lleva su propia resistencia")
    E.placa(1.5, 5.0, 7.5, 19.8, "Arduino\nUNO R3", [("D8", "D8", 8.5), ("D9", "D9", 15.5), ("GND", "GND", 22.5)])
    _rama(E, 8.5, 8, "rojo", "LED 1 (rojo)", "D8", 31.0, 22.5)
    _rama(E, 15.5, 9, "amarillo", "LED 2 (amarillo)", "D9", 29.0, 22.5)
    _riel(E, 22.5, ["TAP9", "TAP8"])
    E.nota(31.6, 12.0, "cable negro")
    E.nota(28.4, 19.5, "cable negro", anchor="rm")
    E.nota(9.5, 24.0, "cable negro", anchor="lm")
    E.nota(20.5, 24.0, "riel GND: la tira azul (−)", anchor="lm")
    E.nota(1.5, 26.8, "Los dos LED comparten el riel GND, pero cada uno tiene su pin y su resistencia.", color="#8a8a8a")
    for p in (8, 9):
        E.exigir(f"D{p}", f"R{p}.a", f"el pin {p} debe llegar a su resistencia")
        E.exigir(f"R{p}.b", f"LED{p}.a", f"la resistencia del pin {p} debe llegar a la pata larga (+)")
        E.exigir(f"LED{p}.k", "GND", f"la pata corta (−) del LED del pin {p} debe llegar a GND")
    E.prohibir("D8", "D9", "pin 8 y pin 9 no pueden tocarse")
    E.prohibir("D9", "GND", "pin 9 y GND no pueden tocarse")
    E.dibujar(os.path.join(AQUI, "P03_dos_led_alternados_cableado.png"))
    print("P03 cableado listo")


def cableado_p04():
    E = Esquema(38, 33.8)
    E.titulo("P04 · Semáforo", "esquema de conexiones · tres LED, tres pines, un solo riel GND")
    E.placa(1.5, 5.0, 7.5, 26.8, "Arduino\nUNO R3", [("D8", "D8", 8.5), ("D9", "D9", 15.5), ("D10", "D10", 22.5), ("GND", "GND", 29.5)])
    _rama(E, 8.5, 8, "rojo", "LED rojo", "D8", 33.0, 29.5)
    _rama(E, 15.5, 9, "amarillo", "LED amarillo", "D9", 31.0, 29.5)
    _rama(E, 22.5, 10, "verde", "LED verde", "D10", 29.0, 29.5)
    _riel(E, 29.5, ["TAP10", "TAP9", "TAP8"])
    E.nota(33.6, 12.0, "cable negro")
    E.nota(28.4, 26.5, "cable negro", anchor="rm")
    E.nota(9.5, 31.0, "cable negro", anchor="lm")
    E.nota(20.5, 31.0, "riel GND: la tira azul (−)", anchor="lm")
    E.nota(1.5, 33.0, "Arriba rojo, en medio amarillo, abajo verde: el mismo orden que un semáforo.", color="#8a8a8a")
    for p in (8, 9, 10):
        E.exigir(f"D{p}", f"R{p}.a", f"el pin {p} debe llegar a su resistencia")
        E.exigir(f"R{p}.b", f"LED{p}.a", f"la resistencia del pin {p} debe llegar a la pata larga (+)")
        E.exigir(f"LED{p}.k", "GND", f"la pata corta (−) del LED del pin {p} debe llegar a GND")
    E.prohibir("D8", "D9", "pin 8 y pin 9 no pueden tocarse")
    E.prohibir("D9", "D10", "pin 9 y pin 10 no pueden tocarse")
    E.prohibir("D10", "GND", "pin 10 y GND no pueden tocarse")
    E.dibujar(os.path.join(AQUI, "P04_semaforo_cableado.png"))
    print("P04 cableado listo")


# ------------------------------------------------------------------ P03 y P04 en protoboard (se arman sobre lo anterior)
def _grupo_p02(circ, step_base=None):
    """Lo que dejó la Sesión 1: LED rojo en pin 8 (cols 18-23), sin números porque ya está armado."""
    circ.led(anodo=(22, "g"), catodo=(23, "g"), color="rojo", nombre="LED8")
    circ.resistor((18, "h"), (22, "h"), 220, nombre="R8")
    circ.wire(("bb", 23, "j"), ("rail", "B", "-", 23), "negro")
    circ.wire(("ard", "GND"), ("rail", "B", "-", 13), "negro", via=0.45)
    circ.wire(("ard", "D8"), ("bb", 18, "j"), "naranja")


def _grupo_p03(circ, nuevo):
    """LED amarillo en pin 9 (cols 12-17), a la izquierda del rojo. Con números solo si es lo nuevo de la práctica."""
    s = (lambda n: n) if nuevo else (lambda n: None)
    circ.led(anodo=(13, "g"), catodo=(12, "g"), color="amarillo", step=s(1), nombre="LED9")
    circ.resistor((17, "h"), (13, "h"), 220, step=s(2), nombre="R9")
    circ.wire(("bb", 12, "j"), ("rail", "B", "-", 12), "negro", step=s(3))
    circ.wire(("ard", "D9"), ("bb", 17, "j"), "morado", step=s(4))


def _verificar_grupo(circ, pin, ard_pin):
    r_a, r_b = circ.elems[f"R{pin}"]
    l_a, l_k = circ.elems[f"LED{pin}"]
    circ.exigir(("ard", ard_pin), r_a, f"el pin {pin} debe llegar a su resistencia")
    circ.exigir(r_b, l_a, f"la resistencia del pin {pin} debe llegar a la pata larga (+)")
    circ.exigir(l_k, ("ard", "GND"), f"la pata corta (−) del LED del pin {pin} debe llegar a GND")
    circ.prohibir(r_a, r_b, f"la resistencia del pin {pin} no puede estar en corto")
    circ.prohibir(l_a, l_k, f"el LED del pin {pin} no puede estar en corto")
    circ.prohibir(("ard", ard_pin), ("ard", "GND"), f"pin {pin} y GND no pueden tocarse")


def _led_cuerpo(bb, col_a, col_k):
    """Centro (x, y) del cuerpo de un LED puesto en la fila g (para apuntar las llamadas)."""
    ax, ay = bb.hole(col_a, "g")
    kx, _ = bb.hole(col_k, "g")
    return (ax + kx) / 2, ay - 2.5


def p03():
    c = Canvas(38.5, 60.2)
    c.header("P03 · Dos LED que se alternan", "Sobre el circuito de P02 agrega un segundo LED (vista desde arriba, parte izquierda del protoboard)")
    bb = Breadboard(3.0, 4.6, cols=30)
    ard = Arduino(bb.x + 2.6, bb.y + bb.H + 6.2)
    circ = Circuit(c, ard, bb)
    _grupo_p02(circ)
    _grupo_p03(circ, nuevo=True)
    _verificar_grupo(circ, 8, "D8")
    _verificar_grupo(circ, 9, "D9")
    circ.prohibir(("ard", "D8"), ("ard", "D9"), "pin 8 y pin 9 no pueden tocarse")
    circ.prohibir(("ard", "5V"), ("ard", "GND"), "5V y GND no pueden tocarse")
    circ.draw()

    x1, y1 = _led_cuerpo(bb, 22, 23)
    x2, y2 = _led_cuerpo(bb, 13, 12)
    c.callout(x1 - 5.6, bb.y + 4.6, ["Ya armado en", "la Sesión 1 (P02)"], target=(x1, y1 - 1.6), size=0.6)
    c.callout(bb.x + 3.0, bb.y + 4.6, ["LED nuevo: la pata larga (+)", "del lado de la resistencia"], target=(x2 - 1.3, y2 - 1.0), size=0.58)
    _leyenda(c, ard.x + 0.5, ard.y + ard.H + 2.0, [(COL["negro"], "GND  (−, tierra)"), (COL["naranja"], "Señal del pin 8 (ya está)"),
                                                  (COL["morado"], "Señal del pin 9 (nuevo)")])
    c.text(c.w_u - 1.2, c.h_u - 1.2, "Los números del 1 al 4 son lo nuevo; lo demás ya lo tienes de P02", 0.5, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P03_dos_led_alternados.png"))
    print("P03 listo")
    for fila in sorted((f for f in circ.table if f[0]), key=lambda t: t[0]):
        print("  ", fila)


def p04():
    c = Canvas(38.5, 61.5)
    c.header("P04 · Semáforo", "Sobre el circuito de P03 agrega el LED verde (vista desde arriba, parte izquierda del protoboard)")
    bb = Breadboard(3.0, 4.6, cols=30)
    ard = Arduino(bb.x + 2.6, bb.y + bb.H + 6.2)
    circ = Circuit(c, ard, bb)
    _grupo_p02(circ)
    _grupo_p03(circ, nuevo=False)
    # LED verde en pin 10 (cols 5-10): lo nuevo
    circ.led(anodo=(6, "g"), catodo=(5, "g"), color="verde", step=1, nombre="LED10")
    circ.resistor((10, "h"), (6, "h"), 220, step=2, nombre="R10")
    circ.wire(("bb", 5, "j"), ("rail", "B", "-", 5), "negro", step=3)
    pin_y = ard.xy("D10")[1]
    hole_y = bb.hole(10, "j")[1]
    y_canal = bb.y + 22.5
    circ.wire(("ard", "D10"), ("bb", 10, "j"), "cafe", via=(pin_y - y_canal) / (pin_y - hole_y), step=4,
              badge=(bb.hole(10, "j")[0] + 1.6, y_canal))
    for pin, nombre in ((8, "D8"), (9, "D9"), (10, "D10")):
        _verificar_grupo(circ, pin, nombre)
    circ.prohibir(("ard", "D8"), ("ard", "D9"), "pin 8 y pin 9 no pueden tocarse")
    circ.prohibir(("ard", "D9"), ("ard", "D10"), "pin 9 y pin 10 no pueden tocarse")
    circ.prohibir(("ard", "5V"), ("ard", "GND"), "5V y GND no pueden tocarse")
    circ.draw()

    x2, y2 = _led_cuerpo(bb, 13, 12)
    x3, y3 = _led_cuerpo(bb, 6, 5)
    c.callout(bb.x + 11.0, bb.y + 4.6, ["Estos dos LED ya los tienes", "armados (P02 y P03)"], target=(x2 + 0.6, y2 - 1.6), size=0.58)
    c.callout(bb.x + 2.2, bb.y + 4.6, ["LED nuevo (verde)"], target=(x3 - 0.3, y3 - 1.5), size=0.58)
    _leyenda(c, ard.x + 0.5, ard.y + ard.H + 2.0, [(COL["negro"], "GND  (−, tierra)"), (COL["naranja"], "Señal del pin 8 (ya está)"),
                                                  (COL["morado"], "Señal del pin 9 (ya está)"), (COL["cafe"], "Señal del pin 10 (nuevo)")])
    c.text(c.w_u - 1.2, c.h_u - 1.2, "Los números del 1 al 4 son lo nuevo; lo demás ya lo tienes de P02 y P03", 0.5, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P04_semaforo.png"))
    print("P04 listo")
    for fila in sorted((f for f in circ.table if f[0]), key=lambda t: t[0]):
        print("  ", fila)


TODOS = {"P01": [p01], "P02": [p02, esquema_p02, cableado_p02], "P03": [p03, cableado_p03], "P04": [p04, cableado_p04]}

if __name__ == "__main__":
    pedidos = sys.argv[1:] or list(TODOS)
    for clave in pedidos:
        for f in TODOS[clave]:
            f()
