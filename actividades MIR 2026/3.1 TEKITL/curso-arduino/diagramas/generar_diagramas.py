"""Genera los diagramas del curso (PNG) en esta misma carpeta.

Uso:  python generar_diagramas.py            (genera todos)
      python generar_diagramas.py P02        (genera solo los de P02)
Requiere Pillow (pip install pillow). Cada circuito se verifica al construirse:
si un cable o componente no coincide con lo esperado, el script se detiene con un mensaje.
"""
import math
import os
import sys

from diagrama import (Arduino, Breadboard, Canvas, Circuit, COL, GRIS_T, TINTA, VINO, LED_COL, dibujar_pir)
from esquema import Esquema, Lienzo

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
CABLE_PIN = {8: "naranja", 9: "morado", 10: "cafe", 2: "verde", 12: "azul", 7: "gris"}


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
    E.nota(9.5, y + 1.45, f"cable {'café' if cab == 'cafe' else cab}")
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
    # al riel entra por la columna 11: en la 12 el riel tiene el hueco entre grupos de cinco agujeros
    circ.wire(("bb", 12, "j"), ("rail", "B", "-", 11), "negro", step=s(3))
    circ.wire(("ard", "D9"), ("bb", 17, "j"), "morado", step=s(4))


def _grupo_p04(circ, bb, ard, nuevo):
    """LED verde en pin 10 (cols 5-10), a la izquierda del amarillo. Con números solo si es lo nuevo de la práctica."""
    s = (lambda n: n) if nuevo else (lambda n: None)
    circ.led(anodo=(6, "g"), catodo=(5, "g"), color="verde", step=s(1), nombre="LED10")
    circ.resistor((10, "h"), (6, "h"), 220, step=s(2), nombre="R10")
    circ.wire(("bb", 5, "j"), ("rail", "B", "-", 5), "negro", step=s(3))
    pin_y = ard.xy("D10")[1]
    hole_y = bb.hole(10, "j")[1]
    y_canal = bb.y + 22.5
    circ.wire(("ard", "D10"), ("bb", 10, "j"), "cafe", via=(pin_y - y_canal) / (pin_y - hole_y), step=s(4),
              badge=(bb.hole(10, "j")[0] + 1.6, y_canal))


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
    _grupo_p04(circ, bb, ard, nuevo=True)      # LED verde en pin 10 (cols 5-10): lo nuevo
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


# ------------------------------------------------------------------ Sesión 3: botón (P05 y P06)
def p05():
    """Botón en el pin 2, sobre el semáforo de P04. El botón cruza el canal y sus dos cables van a patas OPUESTAS."""
    c = Canvas(38.5, 63.4)
    c.header("P05 · Botón y LED", "Sobre el semáforo agrega un botón en el pin 2 (vista desde arriba, parte izquierda del protoboard)")
    bb = Breadboard(3.0, 4.6, cols=30)
    ard = Arduino(bb.x + 2.6, bb.y + bb.H + 6.2)
    circ = Circuit(c, ard, bb)
    _grupo_p02(circ)
    _grupo_p03(circ, nuevo=False)
    _grupo_p04(circ, bb, ard, nuevo=False)

    # lo nuevo: botón en las columnas 26 y 28, cruzando el canal central
    circ.boton(26, step=1)
    # pin 2 -> pata de abajo a la izquierda (columna 26, mitad de abajo)
    circ.wire(("ard", "D2"), ("bb", 26, "j"), "verde", step=2)
    # GND -> pata de arriba a la derecha (columna 28, mitad de arriba): cable largo que sube por la columna 29
    x29 = bb.rail_hole("B", "-", 29)[0]
    y_a = bb.hole(28, "a")[1]
    circ.wire(("rail", "B", "-", 29), ("bb", 28, "a"), "negro", step=3, ruta=[(x29, y_a)],
              badge=(x29, bb.y + 13.0))

    for pin, nombre in ((8, "D8"), (9, "D9"), (10, "D10")):
        _verificar_grupo(circ, pin, nombre)
    circ.prohibir(("ard", "D2"), ("ard", "GND"), "el pin 2 y GND no pueden estar unidos sin presionar el botón")
    circ.prohibir(("ard", "D8"), ("ard", "D9"), "pin 8 y pin 9 no pueden tocarse")
    circ.prohibir(("ard", "D9"), ("ard", "D10"), "pin 9 y pin 10 no pueden tocarse")
    circ.prohibir(("ard", "5V"), ("ard", "GND"), "5V y GND no pueden tocarse")
    circ.comprobar_boton("B", ("ard", "D2"), ("ard", "GND"), "el botón debe unir el pin 2 con GND solo al presionarlo")
    circ.draw()

    x2, y2 = _led_cuerpo(bb, 13, 12)
    bx = (bb.hole(26, "e")[0] + bb.hole(28, "e")[0]) / 2
    by = (bb.hole(26, "e")[1] + bb.hole(26, "f")[1]) / 2
    c.callout(bb.x + 6.0, bb.y + 4.6, ["Semáforo de P02 a P04:", "ya armado, no se toca"], target=(x2 + 0.6, y2 - 1.6), size=0.58)
    c.callout(bb.x + 16.0, bb.y + 4.6, ["Botón nuevo: cruza el canal.", "Cables en patas OPUESTAS"], target=(bx - 0.9, by - 1.0), size=0.58)
    _leyenda(c, ard.x + 0.5, ard.y + ard.H + 2.0, [(COL["negro"], "GND  (−, tierra)"), (COL["naranja"], "Señal del pin 8 (ya está)"),
                                                  (COL["morado"], "Señal del pin 9 (ya está)"), (COL["cafe"], "Señal del pin 10 (ya está)"),
                                                  (COL["verde"], "Señal del pin 2: el botón (nuevo)")])
    c.text(c.w_u - 1.2, c.h_u - 1.2, "Los números del 1 al 3 son lo nuevo; lo demás ya lo tienes de P02, P03 y P04", 0.5, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P05_boton_led.png"))
    print("P05 listo")
    for fila in sorted((f for f in circ.table if f[0]), key=lambda t: t[0]):
        print("  ", fila)


def cableado_p05():
    E = Esquema(38, 42.0)
    E.titulo("P05 · Botón y LED", "esquema de conexiones · el botón va entre el pin 2 y GND")
    E.placa(1.5, 5.0, 7.5, 33.8, "Arduino\nUNO R3", [("D8", "D8", 8.5), ("D9", "D9", 15.5), ("D10", "D10", 22.5),
                                                   ("D2", "D2", 29.5), ("GND", "GND", 36.5)])
    _rama(E, 8.5, 8, "rojo", "LED rojo", "D8", 33.0, 36.5)
    _rama(E, 15.5, 9, "amarillo", "LED amarillo", "D9", 31.0, 36.5)
    _rama(E, 22.5, 10, "verde", "LED verde", "D10", 29.0, 36.5)
    # el botón: pin 2 -> botón -> GND
    E.boton("B", 15.0, 29.5, w=6.0)
    E.terminal("TAP2", 27.0, 36.5)
    E.cable("verde", "D2", "B.a")
    E.cable("negro", "B.b", "TAP2", via=[(27.0, 29.5)])
    E.nota(9.5, 28.05, "pin 2 (entrada)")
    E.nota(9.5, 30.95, "cable verde")
    E.etiqueta(18.0, 25.8, "Botón")
    E.nota(18.0, 32.0, "4 patas: usa dos opuestas", anchor="mm")
    E.nota(24.0, 28.05, "cable negro", anchor="mm")
    _riel(E, 36.5, ["TAP2", "TAP10", "TAP9", "TAP8"])
    E.nota(33.6, 12.0, "cable negro")
    E.nota(28.4, 26.5, "cable negro", anchor="rm")
    E.nota(9.5, 38.0, "cable negro", anchor="lm")
    E.nota(20.5, 38.0, "riel GND: la tira azul (−)", anchor="lm")
    E.nota(1.5, 40.6, "Hoy el programa usa el LED rojo y el botón; amarillo y verde siguen armados para los retos.", color="#8a8a8a")
    for p in (8, 9, 10):
        E.exigir(f"D{p}", f"R{p}.a", f"el pin {p} debe llegar a su resistencia")
        E.exigir(f"R{p}.b", f"LED{p}.a", f"la resistencia del pin {p} debe llegar a la pata larga (+)")
        E.exigir(f"LED{p}.k", "GND", f"la pata corta (−) del LED del pin {p} debe llegar a GND")
    E.exigir("D2", "B.a", "el pin 2 debe llegar a una pata del botón")
    E.exigir("B.b", "GND", "la otra pata del botón debe llegar a GND")
    E.prohibir("B.a", "B.b", "con el botón suelto, el pin 2 no debe estar unido a GND")
    E.prohibir("D2", "GND", "pin 2 y GND no pueden tocarse sin presionar el botón")
    E.prohibir("D8", "D9", "pin 8 y pin 9 no pueden tocarse")
    E.prohibir("D9", "D10", "pin 9 y pin 10 no pueden tocarse")
    E.prohibir("D10", "D2", "pin 10 y pin 2 no pueden tocarse")
    E.dibujar(os.path.join(AQUI, "P05_boton_led_cableado.png"))
    print("P05 cableado listo")


def _flecha(c, p, q, color, w=0.14, tam=0.75):
    """Línea de p a q con punta de flecha en q."""
    c.line([p, q], color, w, ends=False)
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy) or 1.0
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    c.poly([q, (q[0] - ux * tam + nx * tam * 0.5, q[1] - uy * tam + ny * tam * 0.5),
            (q[0] - ux * tam - nx * tam * 0.5, q[1] - uy * tam - ny * tam * 0.5)], fill=color)


def _sym_resistor_v(c, x, y0, y1, color=TINTA, w=0.16):
    n = 6
    seg = (y1 - y0 - 2.0) / n
    pts = [(x, y0), (x, y0 + 1.0)]
    for i in range(n):
        pts.append((x + (-0.8 if i % 2 == 0 else 0.8), y0 + 1.0 + seg * (i + 0.5)))
    pts += [(x, y1 - 1.0), (x, y1)]
    c.line(pts, color, w, ends=False)


def _sym_boton_v(c, x, y0, y1, cerrado, color=TINTA, w=0.16):
    """Pulsador vertical entre (x,y0) y (x,y1). Abierto: lámina inclinada. Cerrado: lámina recta."""
    for yy in (y0, y1):
        c.circle(x, yy, 0.28, fill="#ffffff", outline=color, width=0.12)
    if cerrado:
        c.line([(x, y0), (x, y1)], color, w, ends=False)
    else:
        c.line([(x, y0), (x + 1.4, y1 - 0.7)], color, w, ends=False)
    ym = (y0 + y1) / 2
    xc = x + (1.3 if cerrado else 2.4)                    # el émbolo está más metido al presionar
    c.line([(x + (0.15 if cerrado else 0.9), ym), (xc, ym)], color, 0.14, ends=False)
    c.line([(xc, ym - 1.0), (xc, ym + 1.0)], color, 0.2, ends=False)


def _panel_pullup(c, x0, cerrado):
    y0 = 4.4
    colr = VINO if cerrado else "#8a8a8a"
    c.rect(x0, y0, 19.0, 23.0, fill="#fbfaf6", outline="#cfc9b8", width=0.1, r=0.6)
    c.text(x0 + 9.5, y0 + 1.5, "Botón PRESIONADO" if cerrado else "Botón SUELTO", 0.95, TINTA, "Bold")
    xw = x0 + 5.5                                          # columna donde está el circuito
    ycorr = VINO if cerrado else TINTA
    # +5 V
    c.line([(xw - 1.6, y0 + 4.2), (xw + 1.6, y0 + 4.2)], TINTA, 0.2, ends=False)
    c.text(xw - 2.2, y0 + 4.2, "+5 V", 0.7, TINTA, "Bold", anchor="rm")
    c.line([(xw, y0 + 4.2), (xw, y0 + 5.2)], ycorr, 0.16 if not cerrado else 0.26, ends=False)
    # resistencia interna
    _sym_resistor_v(c, xw, y0 + 5.2, y0 + 9.6, ycorr, 0.16 if not cerrado else 0.26)
    c.text(xw + 1.7, y0 + 7.0, "resistencia interna", 0.55, GRIS_T, "SemiBold", anchor="lm")
    c.text(xw + 1.7, y0 + 7.9, "(pull-up) 20 a 50 kΩ", 0.55, GRIS_T, "SemiBold", anchor="lm")
    # nodo y pin 2
    yn = y0 + 10.8
    c.line([(xw, y0 + 9.6), (xw, yn)], ycorr, 0.16 if not cerrado else 0.26, ends=False)
    c.circle(xw, yn, 0.3, fill=TINTA)
    c.line([(xw, yn), (xw + 4.0, yn)], TINTA, 0.16, ends=False)
    c.rect(xw + 4.0, yn - 1.6, 8.6, 3.2, fill=VINO, r=0.5)
    c.text(xw + 8.3, yn - 0.45, "Pin 2", 0.85, "#ffffff", "Bold")
    c.text(xw + 8.3, yn + 0.8, "lee LOW (0 V)" if cerrado else "lee HIGH (5 V)", 0.6, "#f0d9a0", "SemiBold")
    # botón y tierra
    c.line([(xw, yn), (xw, yn + 1.4)], ycorr, 0.16 if not cerrado else 0.26, ends=False)
    _sym_boton_v(c, xw, yn + 1.4, yn + 4.6, cerrado, ycorr, 0.16 if not cerrado else 0.26)
    c.line([(xw, yn + 4.6), (xw, yn + 5.4)], ycorr, 0.16 if not cerrado else 0.26, ends=False)
    _sym_gnd(c, xw, yn + 5.4)
    c.text(xw + 1.8, yn + 6.4, "GND (0 V)", 0.6, TINTA, "SemiBold", anchor="lm")
    c.text(xw + 4.5, yn + 3.0, "botón", 0.6, GRIS_T, "SemiBold", anchor="lm")
    if cerrado:
        _flecha(c, (xw - 1.7, y0 + 5.6), (xw - 1.7, y0 + 8.4), VINO, 0.14, 0.6)      # el sentido de la corriente
        _flecha(c, (xw - 1.7, yn + 1.6), (xw - 1.7, yn + 4.0), VINO, 0.14, 0.6)
        c.text(x0 + 9.5, y0 + 20.6, "pasa un hilo de corriente:", 0.6, VINO, "Bold")
        c.text(x0 + 9.5, y0 + 21.8, "5 V ÷ (20 a 50 kΩ) = 0,1 a 0,25 mA", 0.6, VINO, "SemiBold")
    else:
        c.text(x0 + 9.5, y0 + 20.6, "el botón abierto no deja pasar corriente:", 0.6, GRIS_T, "Bold")
        c.text(x0 + 9.5, y0 + 21.8, "el pin queda en 5 V", 0.6, GRIS_T, "SemiBold")


def esquema_pullup():
    c = Canvas(44, 33.0)
    c.header("P05 · ¿Por qué «presionado» se lee LOW?", "pinMode(PIN_BOTON, INPUT_PULLUP) conecta una resistencia dentro del Arduino entre el pin y +5 V")
    _panel_pullup(c, 1.5, cerrado=False)
    _panel_pullup(c, 23.5, cerrado=True)
    c.text(22.0, 29.6, "Por eso el programa pregunta  digitalRead(PIN_BOTON) == LOW  para saber si el botón está presionado.", 0.7, VINO, "Bold")
    c.text(22.0, 31.2, "La lógica parece al revés, pero así no hace falta ninguna resistencia externa: solo el botón y un cable a GND.", 0.58, GRIS_T, "Medium")
    c.save(os.path.join(AQUI, "P05_pullup_esquema.png"))
    print("P05 pull-up listo")


def boton_patas():
    """Las cuatro patas del botón de 6 x 6 mm y por qué se conecta en diagonal."""
    c = Canvas(45, 25)
    c.header("P05 · Conoce tu botón", "Botón de 4 patas (6 × 6 mm): las patas van unidas por pares")
    azul, naranja = "#1d5fd1", "#d98200"

    def dibujo(cx, cy, escala=1.0, diag=False):
        s = escala
        for sx in (-1, 1):
            for sy in (-1, 1):
                px_, py_ = cx + sx * 4.0 * s, cy + sy * 3.2 * s
                c.line([(px_, py_), (cx + sx * 2.2 * s, py_)], "#b8b8b8", 0.5 * s, ends=False)
                c.rect(px_ - 0.55 * s, py_ - 0.4 * s, 1.1 * s, 0.8 * s, fill="#b8b8b8", r=0.1)
        c.rect(cx - 3.0 * s, cy - 3.0 * s, 6.0 * s, 6.0 * s, fill="#2e2e2e", outline="#111111", width=0.1, r=0.7 * s)
        c.circle(cx, cy, 1.7 * s, fill="#4b4b4b", outline="#111111", width=0.08)
        c.circle(cx - 0.5 * s, cy - 0.5 * s, 0.5 * s, fill="#808080")
        return cx, cy

    # izquierda: el botón con sus pares
    cx, cy = 10.5, 12.8
    dibujo(cx, cy, 1.15)
    s = 1.15
    pa, pb, pc, pd = (cx - 4.0 * s, cy - 3.2 * s), (cx + 4.0 * s, cy - 3.2 * s), (cx - 4.0 * s, cy + 3.2 * s), (cx + 4.0 * s, cy + 3.2 * s)
    c.line([pa, pc], azul, 0.3, ends=True)                     # par izquierdo unido por dentro
    c.line([pb, pd], naranja, 0.3, ends=True)                  # par derecho unido por dentro
    for (px_, py_), n in ((pa, "A"), (pb, "B"), (pc, "C"), (pd, "D")):
        sx = -1 if n in "AC" else 1
        c.circle(px_ + sx * 1.0, py_, 0.55, fill="#ffffff", outline="#555", width=0.07)
        c.text(px_ + sx * 1.0, py_ + 0.03, n, 0.7, TINTA, "Bold")
    c.text(cx, 6.0, "Vista desde arriba, como queda en el protoboard", 0.6, GRIS_T, "SemiBold")
    c.text(cx - 6.4, cy, "unidas", 0.55, azul, "SemiBold", anchor="rm")
    c.text(cx + 6.4, cy, "unidas", 0.55, naranja, "SemiBold", anchor="lm")
    # el ejemplo de P05: pin 2 en C y GND en B
    for yy, col, txt in ((19.4, COL["verde"], "C = pin 2 (cable verde)"), (20.8, COL["negro"], "B = GND (cable negro)")):
        c.rect(3.0, yy - 0.3, 2.2, 0.6, fill=col, outline="#1a1a1a", width=0.05, r=0.3)
        c.text(6.0, yy, txt, 0.6, TINTA, "SemiBold", anchor="lm")
    c.text(3.0, 22.2, "(así queda en el diagrama de P05)", 0.52, GRIS_T, "Medium", anchor="lm")

    # derecha: qué pasa por dentro
    c.text(19.0, 6.0, "Qué pasa por dentro", 0.85, TINTA, "Bold", anchor="lm")
    filas = [("Suelto", "A–C están unidas entre sí y B–D también, pero el par azul no toca al naranja."),
             ("Presionado", "una lámina interna une el par azul con el naranja: el circuito se cierra.")]
    for i, (t, d) in enumerate(filas):
        yy = 8.3 + i * 2.8
        c.text(19.0, yy, t, 0.7, VINO, "Bold", anchor="lm")
        c.text(19.0, yy + 1.15, d, 0.58, TINTA, "Medium", anchor="lm")
    c.text(19.0, 14.2, "Fuente: hoja de datos del botón del kit (Datasheets/Botton.pdf).", 0.52, GRIS_T, "Medium", anchor="lm")
    c.text(19.0, 15.2, "Compruébalo con el multímetro en continuidad: dos pares deben sonar siempre.", 0.52, GRIS_T, "Medium", anchor="lm")

    # abajo a la derecha: la regla para conectarlo
    c.rect(18.0, 17.0, 25.4, 6.6, fill="#fbf3e2", outline=GOLD_BORDE, width=0.1, r=0.5)
    c.text(19.0, 18.4, "Regla para conectarlo: una pata a cada par, en DIAGONAL", 0.78, VINO, "Bold", anchor="lm")
    c.text(19.0, 19.9, "Pin 2 en una pata y GND en la pata opuesta (A con D, o B con C).", 0.6, TINTA, "Medium", anchor="lm")
    c.text(19.0, 21.1, "Funciona aunque tu botón venga unido al revés de lo que dice la hoja de datos.", 0.58, TINTA, "Medium", anchor="lm")
    c.text(19.0, 22.4, "Con dos cables en patas que no son opuestas, el resultado depende de cómo", 0.52, GRIS_T, "Medium", anchor="lm")
    c.text(19.0, 23.1, "venga tu botón: puede quedar siempre «presionado» o funcionar de casualidad.", 0.52, GRIS_T, "Medium", anchor="lm")
    c.save(os.path.join(AQUI, "P05_boton_patas.png"))
    print("P05 patas listo")


GOLD_BORDE = "#c9a227"


def _senal(c, x_t0, y_alto, y_bajo, t_ini, t_fin, cambios, esc=1.0, color=VINO, w=0.22, nivel0="alto"):
    """Dibuja una señal digital: empieza en 'nivel0' y cambia de nivel en cada tiempo de 'cambios' (en ms)."""
    nivel = nivel0
    x = x_t0 + t_ini * esc
    pts = [(x, y_alto if nivel == "alto" else y_bajo)]
    for t in cambios:
        xt = x_t0 + t * esc
        pts.append((xt, y_alto if nivel == "alto" else y_bajo))
        nivel = "bajo" if nivel == "alto" else "alto"
        pts.append((xt, y_alto if nivel == "alto" else y_bajo))
    pts.append((x_t0 + t_fin * esc, y_alto if nivel == "alto" else y_bajo))
    c.line(pts, color, w, ends=False)


def rebote_p06():
    c = Canvas(58, 37.5)
    c.header("P06 · El rebote del botón", "Lo que lee el pin 2 en los primeros milisegundos al presionar (ilustración, no es una medición)")
    x0, esc = 17.0, 1.0                                    # x del instante 0 y unidades por milisegundo
    t_ini, t_fin = -6, 38
    bounce = [0.0, 1.0, 1.8, 2.6, 3.2]                     # H->L, L->H, H->L, L->H, H->L (queda en LOW)
    azul = "#1d5fd1"
    paneles = [("Lo que imaginamos", 5.6), ("Lo que pasa en realidad", 14.6), ("Con antirrebote: delay(30)", 24.0)]
    for titulo, ytop in paneles:
        c.text(1.5, ytop, titulo, 0.8, TINTA, "Bold", anchor="lm")
        ya, yb = ytop + 2.2, ytop + 6.2
        c.text(x0 - 1.0 + t_ini * esc, ya, "HIGH", 0.55, GRIS_T, "SemiBold", anchor="rm")
        c.text(x0 - 1.0 + t_ini * esc, yb, "LOW", 0.55, GRIS_T, "SemiBold", anchor="rm")
        c.line([(x0 + t_ini * esc, ya), (x0 + t_fin * esc, ya)], "#e2ddd0", 0.06, ends=False)
        c.line([(x0 + t_ini * esc, yb), (x0 + t_fin * esc, yb)], "#e2ddd0", 0.06, ends=False)
    # 1) ideal
    _senal(c, x0, 7.8, 11.8, t_ini, t_fin, [0.0], esc)
    c.text(x0 + 1.2, 12.9, "se presiona: una sola caída", 0.55, VINO, "SemiBold", anchor="lm")
    # 2) real, con rebote
    _senal(c, x0, 16.8, 20.8, t_ini, t_fin, bounce, esc)
    for n, t in enumerate([bounce[0], bounce[2], bounce[4]], start=1):
        xt = x0 + t * esc
        _flecha(c, (xt, 14.9), (xt, 16.5), azul, 0.14, 0.55)
        c.badge(xt + (-0.9 if n == 1 else (0.0 if n == 2 else 0.9)), 14.1 if n != 2 else 13.7, n, color=azul, r=0.5)
    c.text(x0 + 8.0, 17.3, "Cada caída de HIGH a LOW (flechas azules) parece un toque nuevo:", 0.6, azul, "SemiBold", anchor="lm")
    c.text(x0 + 8.0, 18.4, "sin antirrebote el programa cuenta 3 pulsaciones por un solo toque.", 0.6, azul, "SemiBold", anchor="lm")
    c.text(x0 + 8.0, 19.9, "Los rebotes duran unos pocos milisegundos; su forma cambia de botón a botón.", 0.55, GRIS_T, "Medium", anchor="lm")
    # 3) con antirrebote: banda de 30 ms
    ya, yb = 26.2, 30.2
    c.rect(x0, ya - 1.0, 30 * esc, (yb - ya) + 2.0, fill="#fbefc9", outline=None)
    _senal(c, x0, ya, yb, t_ini, t_fin, bounce, esc)
    c.text(x0 + 15.0 * esc, ya + 1.5, "delay(30): el programa espera", 0.65, "#8a6a00", "Bold")
    c.text(x0 + 15.0 * esc, ya + 2.7, "los rebotes quedan dentro de la espera y se ignoran", 0.58, "#8a6a00", "Medium")
    _flecha(c, (x0 + 30 * esc, ya - 2.4), (x0 + 30 * esc, ya - 1.2), azul, 0.14, 0.55)
    c.badge(x0 + 30 * esc, ya - 3.2, 1, color=azul, r=0.5)
    c.text(x0 + 29.0 * esc, ya - 3.2, "al terminar, vuelve a leer: sigue en LOW, cuenta 1 pulsación", 0.55, azul, "SemiBold", anchor="rm")
    # eje del tiempo
    ye = 33.6
    c.line([(x0 + t_ini * esc, ye), (x0 + t_fin * esc, ye)], TINTA, 0.1, ends=False)
    for t in (0, 10, 20, 30):
        xt = x0 + t * esc
        c.line([(xt, ye - 0.3), (xt, ye + 0.3)], TINTA, 0.1, ends=False)
        c.text(xt, ye + 1.1, f"{t} ms", 0.55, TINTA, "SemiBold")
    c.text(x0 + t_fin * esc, ye + 1.1, "tiempo", 0.55, GRIS_T, "SemiBold", anchor="rm")
    c.text(c.w_u - 1.2, c.h_u - 0.9, "Ilustración con valores típicos: no es una medición de tu botón. Para medirlo hace falta un osciloscopio.", 0.5, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P06_rebote.png"))
    print("P06 rebote listo")


def _arco(c, a, b, alto, color, w=0.2, n=24):
    """Flecha curva de a a b (arco hacia arriba si alto<0, hacia abajo si alto>0)."""
    pts = []
    for i in range(n + 1):
        t = i / n
        x = a[0] + (b[0] - a[0]) * t
        y = a[1] + (b[1] - a[1]) * t + alto * 4 * t * (1 - t)
        pts.append((x, y))
    c.line(pts, color, w, ends=False)
    p, q = pts[-2], pts[-1]
    _flecha(c, p, q, color, w, 0.8)


def estados_p06():
    c = Canvas(44, 25)
    c.header("P06 · Qué recuerda el programa", "La variable ledEncendido guarda el estado; cada pulsación lo invierte")
    ya = 13.0
    for cx, titulo, var, relleno, borde in ((9.5, "LED apagado", "ledEncendido = false", "#eceae4", "#8a8a8a"),
                                            (34.5, "LED encendido", "ledEncendido = true", "#fff3bf", "#c99a00")):
        c.circle(cx, ya, 5.3, fill=relleno, outline=borde, width=0.14)
        c.text(cx, ya - 0.6, titulo, 0.95, TINTA, "Bold")
        c.text(cx, ya + 1.0, var, 0.6, GRIS_T, "SemiBold")
    _arco(c, (14.7, ya - 2.4), (29.3, ya - 2.4), -3.0, VINO)
    _arco(c, (29.3, ya + 2.4), (14.7, ya + 2.4), 3.0, VINO)
    c.text(22.0, 5.3, "Presionas el botón", 0.8, VINO, "Bold")
    c.text(22.0, 6.5, "(pasa de HIGH a LOW)", 0.6, VINO, "SemiBold")
    c.text(22.0, 19.6, "Presionas el botón otra vez", 0.8, VINO, "Bold")
    c.text(22.0, 20.8, "(pasa de HIGH a LOW)", 0.6, VINO, "SemiBold")
    c.text(22.0, ya - 0.2, "ledEncendido = !ledEncendido", 0.6, TINTA, "SemiBold")
    c.text(22.0, ya + 0.9, "el signo ! significa «lo contrario»", 0.52, GRIS_T, "Medium")
    c.text(22.0, 23.4, "Soltar el botón no cambia nada: solo se actualiza estadoAnterior.", 0.62, GRIS_T, "Medium")
    c.save(os.path.join(AQUI, "P06_estados.png"))
    print("P06 estados listo")


# ------------------------------------------------------------------ Sesión 4: zumbadores (P07) y alarma con PIR (P08)
# Antes de la sesión se retiran el LED amarillo y el verde: quedan el LED rojo (pin 8) y el botón (pin 2).
# El zumbador va en la parte de abajo-izquierda del protoboard (columnas 5 a 11), donde quedó el espacio.
Y_CANAL_12 = 22.4          # el cable del pin 12 corre en horizontal a bb.y + 22.4


def _base_s4(circ, bb):
    """Lo que queda armado de la Sesión 3: LED rojo con su resistencia (pin 8) y botón (pin 2)."""
    _grupo_p02(circ)
    circ.boton(26)
    circ.wire(("ard", "D2"), ("bb", 26, "j"), "verde")
    x29 = bb.rail_hole("B", "-", 29)[0]
    y_a = bb.hole(28, "a")[1]
    circ.wire(("rail", "B", "-", 29), ("bb", 28, "a"), "negro", ruta=[(x29, y_a)])


def _cable_pin12(circ, bb, ard, col, step):
    """Cable azul del pin 12 a la columna col (fila j). Corre por debajo del protoboard."""
    px = ard.xy("D12")[0]
    xc = bb.hole(col, "j")[0]
    yc = bb.y + Y_CANAL_12
    circ.wire(("ard", "D12"), ("bb", col, "j"), "azul", step=step, ruta=[(px, yc), (xc, yc)])


def _verificar_base_s4(circ):
    _verificar_grupo(circ, 8, "D8")
    circ.prohibir(("ard", "D2"), ("ard", "GND"), "el pin 2 y GND no pueden estar unidos sin presionar el botón")
    circ.comprobar_boton("B", ("ard", "D2"), ("ard", "GND"), "el botón debe unir el pin 2 con GND solo al presionarlo")
    circ.prohibir(("ard", "5V"), ("ard", "GND"), "5V y GND no pueden tocarse")
    circ.prohibir(("ard", "D8"), ("ard", "D2"), "pin 8 y pin 2 no pueden tocarse")


def _leyenda_s4(c, ard, y0, extra):
    _leyenda(c, ard.x + 0.5, y0, [(COL["negro"], "GND  (−, tierra)"), (COL["naranja"], "Señal del pin 8 (ya está)"),
                                  (COL["verde"], "Señal del pin 2: el botón (ya está)")] + extra)


def p07a():
    c = Canvas(38.5, 62.5)
    c.header("P07a · Zumbador activo", "Sobre el LED rojo y el botón, agrega un zumbador activo en el pin 12 (vista desde arriba, parte izquierda)")
    bb = Breadboard(3.0, 4.6, cols=30)
    ard = Arduino(bb.x + 2.6, bb.y + bb.H + 6.2)
    circ = Circuit(c, ard, bb)
    _base_s4(circ, bb)
    circ.zumbador(8, "activo", step=1)                                        # patas en f8 (+) y f11
    _cable_pin12(circ, bb, ard, 8, 2)                                         # pin 12 -> pata + (columna 8)
    circ.wire(("rail", "B", "-", 11), ("bb", 11, "j"), "negro", step=3)       # otra pata -> riel GND
    _verificar_base_s4(circ)
    a, b = circ.elems["BZ"]
    circ.exigir(("ard", "D12"), a, "el pin 12 debe llegar a la pata + del zumbador")
    circ.exigir(b, ("ard", "GND"), "la otra pata del zumbador debe llegar a GND")
    circ.prohibir(a, b, "las patas del zumbador no pueden estar unidas")
    circ.prohibir(("ard", "D12"), ("ard", "GND"), "pin 12 y GND no pueden tocarse")
    circ.draw()

    cx = (bb.hole(8, "f")[0] + bb.hole(11, "f")[0]) / 2
    cy = bb.hole(8, "f")[1]
    c.callout(bb.x + 2.2, bb.y + 4.2, ["Pata + (con el signo en la", "etiqueta) hacia la IZQUIERDA"], target=(cx - 1.6, cy - 0.2), size=0.56)
    lx, ly = _led_cuerpo(bb, 22, 23)
    c.callout(bb.x + 16.2, bb.y + 4.2, ["Sigue armado de la", "Sesión 3: LED rojo y botón"], target=(lx, ly - 1.6), size=0.56)
    _leyenda_s4(c, ard, ard.y + ard.H + 2.0, [(COL["azul"], "Señal del pin 12 (nuevo)")])
    c.text(c.w_u - 1.2, c.h_u - 1.2, "Los números del 1 al 3 son lo nuevo. El LED amarillo y el verde ya se retiraron.", 0.5, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P07a_zumbador_activo.png"))
    print("P07a listo")
    for fila in sorted((f for f in circ.table if f[0]), key=lambda t: t[0]):
        print("  ", fila)


def _zumbador_pasivo(circ, bb, ard, nuevo):
    s = (lambda n: n) if nuevo else (lambda n: None)
    circ.zumbador(8, "pasivo", step=s(1))
    circ.resistor((5, "i"), (8, "i"), 220, step=s(2), nombre="R12")
    _cable_pin12(circ, bb, ard, 5, s(3))
    circ.wire(("rail", "B", "-", 11), ("bb", 11, "j"), "negro")


def _verificar_zumbador_pasivo(circ):
    r_a, r_b = circ.elems["R12"]
    a, b = circ.elems["BZ"]
    circ.exigir(("ard", "D12"), r_a, "el pin 12 debe llegar a la resistencia")
    circ.exigir(r_b, a, "la resistencia debe llegar a una pata del zumbador")
    circ.exigir(b, ("ard", "GND"), "la otra pata del zumbador debe llegar a GND")
    circ.prohibir(r_a, r_b, "la resistencia no puede estar en corto")
    circ.prohibir(a, b, "las patas del zumbador no pueden estar unidas")
    circ.prohibir(("ard", "D12"), a, "el pin 12 no debe llegar al zumbador sin pasar por la resistencia")
    circ.prohibir(("ard", "D12"), ("ard", "GND"), "pin 12 y GND no pueden tocarse")


def p07b():
    c = Canvas(38.5, 62.5)
    c.header("P07b · Zumbador pasivo", "Cambia el zumbador y agrega una resistencia de 220 Ω en el camino del pin 12 (vista desde arriba, parte izquierda)")
    bb = Breadboard(3.0, 4.6, cols=30)
    ard = Arduino(bb.x + 2.6, bb.y + bb.H + 6.2)
    circ = Circuit(c, ard, bb)
    _base_s4(circ, bb)
    _zumbador_pasivo(circ, bb, ard, nuevo=True)
    _verificar_base_s4(circ)
    _verificar_zumbador_pasivo(circ)
    circ.draw()

    cx = (bb.hole(8, "f")[0] + bb.hole(11, "f")[0]) / 2
    cy = bb.hole(8, "f")[1]
    c.callout(bb.x + 9.0, bb.y + 4.2, ["Zumbador PASIVO:", "disco negro con orificio"], target=(cx + 0.4, cy - 1.6), size=0.56)
    rx = (bb.hole(5, "i")[0] + bb.hole(8, "i")[0]) / 2
    ry = bb.hole(5, "i")[1]
    c.callout(bb.x + 1.8, bb.y + 4.2, ["Resistencia 220 Ω", "rojo · rojo · café"], target=(rx - 0.4, ry - 0.45), size=0.54)
    lx, ly = _led_cuerpo(bb, 22, 23)
    c.callout(bb.x + 18.2, bb.y + 4.2, ["Sigue armado de la", "Sesión 3: LED rojo y botón"], target=(lx, ly - 1.6), size=0.56)
    _leyenda_s4(c, ard, ard.y + ard.H + 2.0, [(COL["azul"], "Señal del pin 12 (movido a la col. 5)")])
    c.text(c.w_u - 1.2, c.h_u - 1.2, "Los números del 1 al 3 son lo nuevo; el cable negro del zumbador ya estaba de P07a.", 0.5, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P07b_zumbador_pasivo.png"))
    print("P07b listo")
    for fila in sorted((f for f in circ.table if f[0]), key=lambda t: t[0]):
        print("  ", fila)


def p08():
    c = Canvas(52.5, 68.0)
    c.header("P08 · Alarma de movimiento", "Agrega el sensor PIR con tres cables macho-hembra directo a la placa (vista desde arriba)")
    bb = Breadboard(3.0, 4.6, cols=30)
    ard = Arduino(bb.x + 2.6, bb.y + bb.H + 6.2)
    circ = Circuit(c, ard, bb)
    _base_s4(circ, bb)
    _zumbador_pasivo(circ, bb, ard, nuevo=False)
    px, py = 41.0, 38.0
    circ.pir(px, py)
    x5, y5 = ard.xy("5V")
    xg, yg = ard.xy("GND_5")
    x7, y7 = ard.xy("D7")
    yO = circ.mods["PIR"]["OUT"][1]
    yG = circ.mods["PIR"]["GND"][1]
    yV = circ.mods["PIR"]["VCC"][1]
    # los tres cables dan la vuelta por la derecha de la placa; el de OUT cruza al de GND una sola vez
    circ.wire(("ard", "5V"), ("mod", "PIR", "VCC"), "rojo", step=1, ruta=[(x5, 54.3), (36.5, 54.3), (36.5, yV)], badge=(30.0, 54.3))
    circ.wire(("ard", "GND_5"), ("mod", "PIR", "GND"), "negro", step=2, ruta=[(xg, 53.0), (35.0, 53.0), (35.0, yG)], badge=(25.0, 53.0))
    circ.wire(("ard", "D7"), ("mod", "PIR", "OUT"), "gris", step=3, ruta=[(x7, 30.3), (34.0, 30.3), (34.0, yO)], badge=(28.0, 30.3))
    _verificar_base_s4(circ)
    _verificar_zumbador_pasivo(circ)
    circ.exigir(("ard", "D7"), ("mod", "PIR", "OUT"), "el pin 7 debe llegar a la pata OUT del sensor")
    circ.exigir(("ard", "5V"), ("mod", "PIR", "VCC"), "5V debe llegar a la pata VCC del sensor")
    circ.exigir(("ard", "GND"), ("mod", "PIR", "GND"), "GND debe llegar a la pata GND del sensor")
    circ.prohibir(("mod", "PIR", "VCC"), ("mod", "PIR", "GND"), "VCC y GND del sensor no pueden tocarse")
    circ.prohibir(("mod", "PIR", "OUT"), ("ard", "GND"), "OUT no puede estar unido a GND")
    circ.prohibir(("mod", "PIR", "OUT"), ("ard", "5V"), "OUT no puede estar unido a 5V")
    circ.prohibir(("ard", "D7"), ("ard", "D12"), "pin 7 y pin 12 no pueden tocarse")
    circ.draw()

    c.callout(px - 3.4, py - 5.6, ["Sensor PIR visto por el lado de la cúpula.", "Las letras de TUS patas mandan:", "lee VCC, OUT y GND antes de conectar"], target=(px + 5.0, py - 0.3), size=0.54)
    cx = (bb.hole(8, "f")[0] + bb.hole(11, "f")[0]) / 2
    cy = bb.hole(8, "f")[1]
    c.callout(bb.x + 1.6, bb.y + 4.2, ["Zumbador pasivo y su resistencia:", "ya armados en P07b"], target=(cx - 0.3, cy - 1.0), size=0.54)
    lx, ly = _led_cuerpo(bb, 22, 23)
    c.callout(bb.x + 16.2, bb.y + 4.2, ["LED rojo y botón:", "ya armados (Sesión 3)"], target=(lx, ly - 1.6), size=0.54)
    c.callout(px - 3.6, 12.0, ["Los tres cables del sensor van directo", "a la placa: no usan el protoboard.", "Son macho-hembra: el extremo hembra", "(con funda negra) va a las patas del sensor"], size=0.54)
    _leyenda(c, ard.x + 0.5, 57.4, [(COL["negro"], "GND  (−, tierra)"), (COL["naranja"], "Señal del pin 8 (ya está)"),
                                    (COL["verde"], "Señal del pin 2 (ya está)"), (COL["azul"], "Señal del pin 12 (ya está)"),
                                    (COL["gris"], "Señal del pin 7: salida OUT del PIR (nuevo)"), (COL["rojo"], "+5 V para el sensor (nuevo)")])
    c.text(c.w_u - 1.2, c.h_u - 1.2, "Los números del 1 al 3 son lo nuevo. Los cables del sensor son macho-hembra: el lado hembra va al sensor.", 0.5, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P08_alarma_pir.png"))
    print("P08 listo")
    for fila in sorted((f for f in circ.table if f[0]), key=lambda t: t[0]):
        print("  ", fila)


def cableado_p07a():
    E = Esquema(36, 19.8)
    E.titulo("P07a · Zumbador activo", "esquema de conexiones · va directo al pin 12, sin resistencia")
    y = 8.5
    E.placa(1.5, 5.0, 7.5, 11.0, "Arduino\nUNO R3", [("D12", "D12", y), ("GND", "GND", 13.5)])
    E.bloque("BZ", 17.0, y - 2.0, 9.0, 4.0, "Zumbador", "activo", terminales=[("p", "izq", 2.0, "+"), ("n", "der", 2.0, "−")])
    E.terminal("TAP12", 29.0, 13.5)
    E.cable("azul", "D12", "BZ.p")
    E.cable("negro", "BZ.n", "TAP12", via=[(29.0, y)])
    _riel(E, 13.5, ["TAP12"])
    E.nota(9.5, y - 1.45, "pin 12 (salida)")
    E.nota(9.5, y + 1.45, "cable azul")
    E.nota(21.5, y + 3.6, "pata larga (+): la de la etiqueta con +", anchor="mm")
    E.nota(29.6, 11.0, "cable negro")
    E.nota(9.5, 15.0, "cable negro", anchor="lm")
    E.nota(20.5, 15.0, "riel GND: la tira azul (−)", anchor="lm")
    E.nota(1.5, 18.8, "Pide menos de 25 mA (hoja de datos) y un pin del UNO aguanta hasta 40 mA.", color="#8a8a8a")
    E.exigir("D12", "BZ.p", "el pin 12 debe llegar a la pata + del zumbador")
    E.exigir("BZ.n", "GND", "la otra pata del zumbador debe llegar a GND")
    E.prohibir("D12", "GND", "pin 12 y GND no pueden tocarse")
    E.prohibir("BZ.p", "BZ.n", "el zumbador no puede estar en corto")
    E.dibujar(os.path.join(AQUI, "P07a_zumbador_activo_cableado.png"))
    print("P07a cableado listo")


def cableado_p07b():
    E = Esquema(36, 19.8)
    E.titulo("P07b · Zumbador pasivo", "esquema de conexiones · la resistencia de 220 Ω va en serie, entre el pin 12 y el zumbador")
    y = 8.5
    E.placa(1.5, 5.0, 7.5, 11.0, "Arduino\nUNO R3", [("D12", "D12", y), ("GND", "GND", 13.5)])
    E.resistencia("R12", 15.0, y, "220 Ω")
    E.bloque("BZ", 22.5, y - 2.0, 9.0, 4.0, "Zumbador", "pasivo", terminales=[("p", "izq", 2.0, ""), ("n", "der", 2.0, "")])
    E.terminal("TAP12", 34.0, 13.5)
    E.cable("azul", "D12", "R12.a")
    E.cable("azul", "R12.b", "BZ.p")
    E.cable("negro", "BZ.n", "TAP12", via=[(34.0, y)])
    _riel(E, 13.5, ["TAP12"])
    E.nota(9.5, y - 1.45, "pin 12 (salida)")
    E.nota(9.5, y + 1.45, "cable azul")
    E.etiqueta(17.3, y - 2.3, "Resistencia")
    E.nota(17.3, y + 1.9, "rojo · rojo · café", anchor="mm")
    E.nota(27.0, y + 3.6, "si trae +, ese lado va al pin 12", anchor="mm")
    E.nota(33.4, 11.0, "cable negro", anchor="rm")
    E.nota(9.5, 15.0, "cable negro", anchor="lm")
    E.nota(20.5, 15.0, "riel GND: la tira azul (−)", anchor="lm")
    E.nota(1.5, 18.8, "Con la resistencia: 5 V ÷ (16 Ω + 220 Ω) ≈ 21 mA, bien por debajo de los 40 mA del pin.", color="#8a8a8a")
    E.exigir("D12", "R12.a", "el pin 12 debe llegar a la resistencia")
    E.exigir("R12.b", "BZ.p", "la resistencia debe llegar al zumbador")
    E.exigir("BZ.n", "GND", "la otra pata del zumbador debe llegar a GND")
    E.prohibir("D12", "BZ.p", "el pin 12 no debe llegar al zumbador sin pasar por la resistencia")
    E.prohibir("D12", "GND", "pin 12 y GND no pueden tocarse")
    E.dibujar(os.path.join(AQUI, "P07b_zumbador_pasivo_cableado.png"))
    print("P07b cableado listo")


def cableado_p08():
    E = Esquema(38, 47.0)
    E.titulo("P08 · Alarma de movimiento", "esquema de conexiones · LED rojo, botón, zumbador pasivo y sensor PIR")
    E.placa(1.5, 5.0, 7.5, 35.5, "Arduino\nUNO R3", [("D8", "D8", 8.5), ("D2", "D2", 15.5), ("D12", "D12", 22.5),
                                                    ("D7", "D7", 29.0), ("5V", "5V", 31.5), ("GND", "GND", 38.0)])
    # fila 1: LED rojo (indica «armada»)
    _rama(E, 8.5, 8, "rojo", "LED rojo", "D8", 34.0, 38.0)
    E.nota(24.8, 10.9, "se enciende: alarma armada", anchor="mm")
    # fila 2: botón (arma y desarma)
    E.boton("B", 15.0, 15.5, w=6.0)
    E.terminal("TAP2", 32.0, 38.0)
    E.cable("verde", "D2", "B.a")
    E.cable("negro", "B.b", "TAP2", via=[(32.0, 15.5)])
    E.nota(9.5, 14.05, "pin 2 (entrada)")
    E.nota(9.5, 16.95, "cable verde")
    E.etiqueta(18.0, 12.6, "Botón")
    E.nota(18.0, 18.0, "arma y desarma", anchor="mm")
    E.nota(26.5, 14.1, "cable negro", anchor="mm")
    # fila 3: zumbador pasivo con su resistencia
    E.resistencia("R12", 13.0, 22.5, "220 Ω")
    E.bloque("BZ", 21.0, 20.5, 8.0, 4.0, "Zumbador", "pasivo", terminales=[("p", "izq", 2.0, ""), ("n", "der", 2.0, "")])
    E.terminal("TAP12", 31.0, 38.0)
    E.cable("azul", "D12", "R12.a")
    E.cable("azul", "R12.b", "BZ.p")
    E.cable("negro", "BZ.n", "TAP12", via=[(31.0, 22.5)])
    E.nota(9.5, 21.05, "pin 12 (salida)")
    E.nota(9.5, 23.95, "cable azul")
    # fila 4: sensor PIR (macho-hembra directo a la placa)
    E.bloque("PIR", 17.0, 26.5, 9.0, 8.5, "Sensor PIR", "HC-SR501",
             terminales=[("out", "izq", 2.5, "OUT"), ("vcc", "izq", 5.0, "VCC"), ("gnd", "izq", 7.5, "GND")])
    E.terminal("TAPPIR", 13.0, 38.0)
    E.cable("gris", "D7", "PIR.out")
    E.cable("rojo", "5V", "PIR.vcc")
    E.cable("negro", "PIR.gnd", "TAPPIR", via=[(13.0, 34.0)])
    E.nota(9.5, 27.55, "pin 7 (entrada)")
    E.nota(9.5, 30.35, "cable gris")
    E.nota(9.5, 32.9, "5 V · cable rojo")
    E.nota(21.5, 36.3, "3 cables macho-hembra", anchor="mm")
    _riel(E, 38.0, ["TAPPIR", "TAP12", "TAP2", "TAP8"])
    E.nota(33.4, 12.0, "cable negro", anchor="rm")
    E.nota(9.5, 39.5, "cable negro", anchor="lm")
    E.nota(20.5, 39.5, "riel GND: la tira azul (−)", anchor="lm")
    E.nota(1.5, 45.6, "El LED amarillo y el verde ya no están. Hoy el sensor, el botón y el zumbador comparten solo el GND.", color="#8a8a8a")
    E.exigir("D8", "R8.a", "el pin 8 debe llegar a la resistencia del LED")
    E.exigir("R8.b", "LED8.a", "la resistencia debe llegar a la pata larga (+) del LED")
    E.exigir("LED8.k", "GND", "la pata corta (−) del LED debe llegar a GND")
    E.exigir("D2", "B.a", "el pin 2 debe llegar a una pata del botón")
    E.exigir("B.b", "GND", "la otra pata del botón debe llegar a GND")
    E.prohibir("B.a", "B.b", "con el botón suelto, el pin 2 no debe estar unido a GND")
    E.exigir("D12", "R12.a", "el pin 12 debe llegar a la resistencia")
    E.exigir("R12.b", "BZ.p", "la resistencia debe llegar al zumbador")
    E.exigir("BZ.n", "GND", "la otra pata del zumbador debe llegar a GND")
    E.exigir("D7", "PIR.out", "el pin 7 debe llegar a OUT")
    E.exigir("5V", "PIR.vcc", "5V debe llegar a VCC")
    E.exigir("PIR.gnd", "GND", "la pata GND del sensor debe llegar a GND")
    E.prohibir("5V", "GND", "5V y GND no pueden tocarse")
    E.prohibir("PIR.vcc", "PIR.gnd", "VCC y GND del sensor no pueden tocarse")
    E.prohibir("D7", "GND", "pin 7 y GND no pueden tocarse")
    E.prohibir("D12", "BZ.p", "el pin 12 no debe llegar al zumbador sin pasar por la resistencia")
    for a, b in (("D8", "D2"), ("D2", "D12"), ("D12", "D7"), ("D8", "D7")):
        E.prohibir(a, b, f"{a} y {b} no pueden tocarse")
    E.dibujar(os.path.join(AQUI, "P08_alarma_pir_cableado.png"))
    print("P08 cableado listo")


# ------------------------------------------------------------------ Sesión 4: diagramas de ideas
def _lista(c, x, y, lineas, size=0.58, paso=1.3, color=TINTA):
    for i, s in enumerate(lineas):
        c.text(x, y + i * paso, s, size, color, "Medium", anchor="lm")


def _caja_aviso(c, x, y, w, h, titulo, lineas, size=0.6):
    c.rect(x, y, w, h, fill="#fbf3e2", outline=GOLD_BORDE, width=0.1, r=0.5)
    c.text(x + 0.9, y + 1.1, titulo, 0.78, VINO, "Bold", anchor="lm")
    for i, s in enumerate(lineas):
        c.text(x + 0.9, y + 2.5 + i * 1.25, s, size, TINTA, "Medium", anchor="lm")


def zumbadores():
    """Los dos zumbadores del kit: cómo se reconocen y cómo se conectan."""
    c = Canvas(58, 34)
    c.header("P07 · Conoce tus dos zumbadores", "El kit trae uno activo y uno pasivo: se parecen, pero se conectan y se programan distinto")
    azul = "#2a4d9b"
    for x0, titulo, col in ((1.5, "ACTIVO", azul), (30.0, "PASIVO", VINO)):
        c.rect(x0, 4.4, 26.5, 21.6, fill="#fbfaf6", outline="#cfc9b8", width=0.1, r=0.6)
        c.text(x0 + 13.25, 6.0, f"Zumbador {titulo}", 1.0, col, "Bold")
    # activo
    cx, cy = 7.5, 12.6
    c.circle(cx, cy, 4.6, fill="#1f2733", outline="#0b0f14", width=0.1)
    c.circle(cx, cy, 4.05, outline="#35435a", width=0.07)
    c.circle(cx, cy, 2.7, fill="#f4f4f1", outline="#c9c9c2", width=0.06)
    c.circle(cx + 0.2, cy - 0.2, 1.0, outline=azul, width=0.11)
    c.line([(cx - 0.35, cy - 0.2), (cx + 0.75, cy - 0.2)], azul, 0.11, ends=False)
    c.line([(cx + 0.2, cy - 0.75), (cx + 0.2, cy + 0.35)], azul, 0.11, ends=False)
    c.text(cx, cy + 6.2, "etiqueta blanca con el signo +", 0.52, GRIS_T, "SemiBold")
    _lista(c, 13.4, 9.0, ["• Trae un oscilador adentro", "• Con 5 V suena solo,", "   siempre con el mismo tono", "   (unos 2 300 Hz)", "• 3,5 a 5,5 V · menos de 25 mA"], 0.56, 1.35)
    # pasivo
    cx2 = 36.0
    c.circle(cx2, cy, 4.6, fill="#161616", outline="#050505", width=0.1)
    c.circle(cx2, cy, 4.05, outline="#2c2c2c", width=0.07)
    c.circle(cx2, cy, 1.0, fill="#5b5b5b", outline="#0a0a0a", width=0.06)
    c.circle(cx2 - 2.0, cy - 2.0, 0.4, fill="#3a3a3a")
    c.text(cx2, cy + 6.2, "disco negro liso con un orificio", 0.52, GRIS_T, "SemiBold")
    _lista(c, 41.9, 9.0, ["• No tiene oscilador: es una", "   bocina diminuta (una bobina)", "• Con 5 V fijos solo hace un clic;", "   hay que hacerlo vibrar (tone)", "• 3 a 12 V · bobina de 16 Ω"], 0.56, 1.35)
    # cómo se conectan
    c.text(3.0, 20.6, "Se conecta así", 0.7, azul, "Bold", anchor="lm")
    _lista(c, 3.0, 22.2, ["Pin 12 a la pata + · la otra pata a GND", "Sin resistencia. Se programa con digitalWrite."], 0.56, 1.3)
    c.text(31.5, 20.6, "Se conecta así", 0.7, VINO, "Bold", anchor="lm")
    _lista(c, 31.5, 22.2, ["Pin 12, resistencia de 220 Ω, una pata · la", "otra pata a GND. Se programa con tone()."], 0.56, 1.3)
    _caja_aviso(c, 1.5, 26.9, 55.0, 5.4, "Cuidado con el pasivo",
                ["Nunca va directo a un pin con digitalWrite(HIGH), ni a 5 V: con 16 Ω pediría 5 V ÷ 16 Ω ≈ 310 mA,",
                 "y un pin del UNO aguanta 40 mA como máximo (UNO.pdf). Con 220 Ω en serie: unos 20 mA."], 0.58)
    c.text(c.w_u - 1.0, c.h_u - 0.7, "Dibujos basados en las fotos del manual del fabricante: compáralos con tus piezas.", 0.5, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P07_zumbadores.png"))
    print("P07 zumbadores listo")


def _onda(c, x0, esc, t_max, periodo_ms, y_alto, y_bajo, color=VINO, w=0.22):
    """Onda cuadrada que empieza en HIGH en t=0. Tiempo en ms, esc = unidades por ms."""
    pts = [(x0, y_alto)]
    t, nivel = 0.0, "alto"
    while t < t_max - 1e-9:
        t_sig = min(t + periodo_ms / 2.0, t_max)
        y = y_alto if nivel == "alto" else y_bajo
        pts.append((x0 + t_sig * esc, y))
        if t_sig < t_max:
            nivel = "bajo" if nivel == "alto" else "alto"
            pts.append((x0 + t_sig * esc, y_alto if nivel == "alto" else y_bajo))
        t = t_sig
    c.line(pts, color, w, ends=False)


def frecuencia():
    """tone(): una frecuencia es cuántas veces por segundo el pin cambia entre HIGH y LOW."""
    c = Canvas(58, 36)
    c.header("P07 · El sonido es vibración", "tone(PIN, frecuencia) cambia el pin entre HIGH y LOW esa cantidad de veces por segundo")
    x0, esc, t_max = 15.0, 4.0, 10.0
    filas = [("Do", 262, 6.2), ("Do alto", 523, 14.2), ("Un tono agudo", 2000, 22.2)]
    for nombre, hz, yt in filas:
        ya, yb = yt + 1.6, yt + 5.0
        c.text(1.5, yt + 2.2, nombre, 0.85, TINTA, "Bold", anchor="lm")
        c.text(1.5, yt + 3.5, f"{hz} Hz", 0.75, VINO, "Bold", anchor="lm")
        c.text(1.5, yt + 4.7, f"{hz} ciclos por segundo", 0.5, GRIS_T, "Medium", anchor="lm")
        c.line([(x0, ya), (x0 + t_max * esc, ya)], "#e2ddd0", 0.06, ends=False)
        c.line([(x0, yb), (x0 + t_max * esc, yb)], "#e2ddd0", 0.06, ends=False)
        c.text(x0 - 0.5, ya, "HIGH", 0.46, GRIS_T, "SemiBold", anchor="rm")
        c.text(x0 - 0.5, yb, "LOW", 0.46, GRIS_T, "SemiBold", anchor="rm")
        per = 1000.0 / hz
        _onda(c, x0, esc, t_max, per, ya, yb)
        # un ciclo
        xa, xb = x0, x0 + per * esc
        yy = yt + 0.5
        c.line([(xa, yy), (xb, yy)], "#1d5fd1", 0.12, ends=False)
        c.line([(xa, yy - 0.3), (xa, yy + 0.3)], "#1d5fd1", 0.12, ends=False)
        c.line([(xb, yy - 0.3), (xb, yy + 0.3)], "#1d5fd1", 0.12, ends=False)
        c.text(xb + 0.5, yy, f"1 ciclo = {per:.1f} ms".replace(".", ","), 0.5, "#1d5fd1", "SemiBold", anchor="lm")
    ye = 29.2
    c.line([(x0, ye), (x0 + t_max * esc, ye)], TINTA, 0.1, ends=False)
    for t in range(0, 11, 2):
        xt = x0 + t * esc
        c.line([(xt, ye - 0.3), (xt, ye + 0.3)], TINTA, 0.1, ends=False)
        c.text(xt, ye + 1.1, f"{t} ms", 0.5, TINTA, "SemiBold")
    c.text(x0 + t_max * esc + 0.6, ye, "tiempo", 0.5, GRIS_T, "SemiBold", anchor="lm")
    c.text(29.0, 32.0, "Más Hz = más vibraciones por segundo = nota más aguda. Do alto (523 Hz) es el doble de Do (262 Hz): una octava.", 0.6, VINO, "Bold")
    c.text(29.0, 33.5, "Un zumbador pasivo suena porque su bobina sigue estos cambios. Ventana de 10 ms; el oído oye 20 a 20 000 ciclos por segundo.", 0.52, GRIS_T, "Medium")
    c.save(os.path.join(AQUI, "P07_frecuencia.png"))
    print("P07 frecuencia listo")


def for_diagrama():
    """Anatomía de un for y su tabla de vueltas."""
    c = Lienzo(62, 36)
    c.header("P07 · Repetir con for", "Lo que está entre llaves se repite; el for decide cuántas veces con un contador")
    azul, naranja, verde = "#4aa3ff", "#ffb347", "#6bd68a"
    # código
    c.rect(1.5, 4.7, 30.0, 7.0, fill="#1e1e24", r=0.6)
    linea1 = "for (int i = 0; i < 3; i++) {"
    cw = c.text_len("M", 0.85, "MonoBold")
    xc = 3.0
    for texto, color, fondo, i0 in (("int i = 0", azul, "#1d3a5c", linea1.index("int i = 0")), ("i < 3", naranja, "#5c3f10", linea1.index("i < 3")),
                                    ("i++", verde, "#1d4d31", linea1.index("i++"))):
        c.rect(xc + i0 * cw - 0.1, 6.55, len(texto) * cw + 0.2, 1.55, fill=fondo, outline=color, width=0.07, r=0.2)
    c.text(xc, 7.4, linea1, 0.85, "#f2f2f2", "MonoBold", anchor="lm")
    c.text(xc, 9.2, "  pitido(100);", 0.85, "#f2f2f2", "MonoBold", anchor="lm")
    c.text(xc, 11.0, "}", 0.85, "#f2f2f2", "MonoBold", anchor="lm")
    # explicación de las tres partes
    for i, (col, tit, txt) in enumerate(((azul, "int i = 0", "Se hace UNA sola vez, al empezar: i es el contador."),
                                         (naranja, "i < 3", "Se pregunta ANTES de cada vuelta; si es falso, el for termina."),
                                         (verde, "i++", "Se hace al terminar cada vuelta: suma 1 a i (igual que i = i + 1)."))):
        yy = 14.2 + i * 2.5
        c.badge(2.6, yy, i + 1, color={0: "#2a7de1", 1: "#d98200", 2: "#2f9e57"}[i], r=0.62)
        c.text(4.0, yy - 0.5, tit, 0.7, TINTA, "MonoBold", anchor="lm")
        c.text(4.0, yy + 0.65, txt, 0.55, GRIS_T, "Medium", anchor="lm")
    # tabla de vueltas
    ytab = 22.2
    c.text(1.5, ytab, "Las vueltas, una por una  (cuando i vale 3 ya no se cumple i < 3)", 0.7, VINO, "Bold", anchor="lm")
    cols = [("Vuelta", 1.5, 4.8), ("i vale", 6.3, 4.4), ("¿i < 3?", 10.7, 5.0), ("Qué pasa", 15.7, 15.8)]
    filas = [("1", "0", "sí", "suena el pitido 1"), ("2", "1", "sí", "suena el pitido 2"), ("3", "2", "sí", "suena el pitido 3"), ("fin", "3", "no", "el for termina y sigue el programa")]
    yh = ytab + 1.0
    for (t, x, w) in cols:
        c.rect(x, yh, w, 1.8, fill=VINO, outline="#ffffff", width=0.05)
        c.text(x + w / 2, yh + 0.92, t, 0.58, "#ffffff", "Bold")
    for r, fila in enumerate(filas):
        yy = yh + 1.8 + r * 1.8
        for (t, x, w), v in zip(cols, fila):
            c.rect(x, yy, w, 1.8, fill="#fbf3e2" if r == 3 else "#ffffff", outline="#cfc9b8", width=0.05)
            c.text(x + w / 2, yy + 0.92, v, 0.58, "#b00020" if (r == 3 and v == "no") else TINTA, "SemiBold")
    c.text(1.5, 33.6, "Para cambiar cuántos pitidos: cambia el 3 (mejor, una constante como PITIDOS_CORTOS).", 0.56, GRIS_T, "Medium", anchor="lm")
    # diagrama de flujo
    xc2 = 46.0
    c.text(xc2 + 4.5, 4.9, "Cómo piensa el Arduino", 0.7, VINO, "Bold")
    c.rect(xc2 - 6.5, 6.4, 13.0, 2.6, fill="#dbeeff", outline="#2a7de1", width=0.1, r=0.5)
    c.text(xc2, 7.7, "int i = 0", 0.7, TINTA, "MonoBold")
    c.badge(xc2 - 6.5, 6.4, 1, color="#2a7de1", r=0.55)
    _flecha(c, (xc2, 9.0), (xc2, 11.2), TINTA, 0.14, 0.6)
    yd = 13.7
    c.poly([(xc2 - 6.5, yd), (xc2, yd - 2.5), (xc2 + 6.5, yd), (xc2, yd + 2.5)], fill="#ffeacc", outline="#d98200", width=0.1)
    c.text(xc2, yd, "¿i < 3?", 0.7, TINTA, "MonoBold")
    c.badge(xc2 - 3.6, yd - 1.7, 2, color="#d98200", r=0.55)
    _flecha(c, (xc2, yd + 2.5), (xc2, 18.0), TINTA, 0.14, 0.6)
    c.text(xc2 + 0.7, yd + 3.6, "sí", 0.6, "#2f9e57", "Bold", anchor="lm")
    c.rect(xc2 - 6.5, 18.0, 13.0, 2.6, fill="#ffffff", outline=TINTA, width=0.1, r=0.5)
    c.text(xc2, 19.3, "pitido(100);", 0.7, TINTA, "MonoBold")
    _flecha(c, (xc2, 20.6), (xc2, 22.8), TINTA, 0.14, 0.6)
    c.rect(xc2 - 6.5, 22.8, 13.0, 2.6, fill="#d9f5e3", outline="#2f9e57", width=0.1, r=0.5)
    c.text(xc2, 24.1, "i++", 0.7, TINTA, "MonoBold")
    c.badge(xc2 - 5.6, 22.8, 3, color="#2f9e57", r=0.55)
    # regreso al «¿i < 3?»
    c.line([(xc2 - 6.5, 24.1), (xc2 - 9.0, 24.1), (xc2 - 9.0, yd)], VINO, 0.14, ends=False)
    _flecha(c, (xc2 - 9.0, yd), (xc2 - 6.5, yd), VINO, 0.14, 0.6)
    c.text(xc2 - 9.5, 19.0, "otra vuelta", 0.52, VINO, "SemiBold", anchor="rm")
    # salida «no»
    _flecha(c, (xc2 + 6.5, yd), (xc2 + 9.3, yd), "#b00020", 0.14, 0.6)
    c.text(xc2 + 7.9, yd - 1.0, "no", 0.6, "#b00020", "Bold")
    c.rect(xc2 + 9.3, yd - 2.3, 5.9, 4.6, fill="#f1efe8", outline="#8a8a8a", width=0.1, r=0.5)
    for i, s in enumerate(("sigue con", "lo que viene", "después")):
        c.text(xc2 + 12.25, yd - 1.1 + i * 1.1, s, 0.5, TINTA, "Medium")
    c.save(os.path.join(AQUI, "P07_for.png"))
    print("P07 for listo")


def pir_conoce():
    """El módulo PIR HC-SR501: vista de la cúpula, vista de atrás con los controles, y qué hace cada cosa."""
    c = Canvas(62, 46)
    c.header("P08 · Conoce tu sensor PIR (HC-SR501)", "PIR = infrarrojo pasivo: detecta cambios de calor al moverse un cuerpo; es pasivo porque no emite nada, solo escucha")
    verde = "#2f8f55"
    s = 1.5
    ancho, alto = 12.6 * s, 9.4 * s          # 32 x 24 mm
    # --- vista de la cúpula
    x, y = 3.0, 10.6
    c.text(x + ancho / 2, 5.8, "Por la cúpula", 0.85, TINTA, "Bold")
    c.text(x + ancho / 2, 7.3, "lente que reparte el calor en zonas", 0.52, GRIS_T, "SemiBold")
    c.text(x + ancho / 2, 8.4, "cono de 110° · alcance de 3 a 7 m", 0.52, GRIS_T, "SemiBold")
    c.rect(x, y, ancho, alto, fill=verde, outline="#1b5c37", width=0.12, r=0.6)
    for (hx, hy) in ((x + 1.0, y + 1.0), (x + ancho - 1.0, y + 1.0), (x + 1.0, y + alto - 1.0), (x + ancho - 1.0, y + alto - 1.0)):
        c.circle(hx, hy, 0.5, fill="#e9e9e0", outline="#1b5c37", width=0.06)
    xm, ym = x + ancho / 2, y + alto / 2
    c.circle(xm, ym, 6.5, fill="#f5f5f2", outline="#cfcfc8", width=0.1)
    c.circle(xm, ym, 4.5, outline="#dcdcd5", width=0.06)
    for k in range(6):
        a = k * math.pi / 3
        c.line([(xm + math.cos(a) * 1.5, ym + math.sin(a) * 1.5), (xm + math.cos(a) * 4.5, ym + math.sin(a) * 4.5)], "#dcdcd5", 0.06, ends=False)
    c.circle(xm, ym, 1.5, fill="#ffffff", outline="#dcdcd5", width=0.06)
    for k in range(3):
        c.rect(xm - 1.2 + k * 1.2, y + alto, 0.35, 1.4, fill="#c9a227")
    c.text(xm + 2.6, y + alto + 0.8, "las 3 patas salen por abajo", 0.52, GRIS_T, "Medium", anchor="lm")
    # --- vista de atrás (lado de las patas y los controles), como en el manual del kit
    xb, yb = 27.0, 10.6
    c.text(xb + ancho / 2, 5.8, "Por atrás (el lado de las letras)", 0.85, TINTA, "Bold")
    c.rect(xb, yb, ancho, alto, fill=verde, outline="#1b5c37", width=0.12, r=0.6)
    for (hx, hy) in ((xb + 1.0, yb + 1.0), (xb + ancho - 1.0, yb + 1.0), (xb + 1.0, yb + alto - 1.0), (xb + ancho - 1.0, yb + alto - 1.0)):
        c.circle(hx, hy, 0.5, fill="#e9e9e0", outline="#1b5c37", width=0.06)
    c.rect(xb + 11.0, yb + 4.2, 3.6, 4.8, fill="#1c1c1c", r=0.15)           # componentes decorativos
    for k in range(6):
        c.rect(xb + 3.0 + k * 1.2, yb + 3.4, 0.7, 0.5, fill="#cfc9a8")
    c.rect(xb + 3.0, yb + 10.0, 2.0, 1.2, fill="#2a2a2a", r=0.1)
    pots = {"Tx": xb + 4.8, "Sx": xb + 8.4}
    for nombre, px_ in pots.items():                                         # perillas
        c.rect(px_ - 1.2, yb + 0.5, 2.4, 2.3, fill="#e8e8e8", outline="#8a8a8a", width=0.06, r=0.2)
        c.circle(px_, yb + 1.65, 0.8, fill="#e58a1f", outline="#8a4a00", width=0.05)
        c.line([(px_ - 0.45, yb + 1.65), (px_ + 0.45, yb + 1.65)], "#7a3a00", 0.09, ends=False)
        c.line([(px_, yb + 1.2), (px_, yb + 2.1)], "#7a3a00", 0.09, ends=False)
    c.rect(xb + ancho - 2.4, yb + 0.7, 1.8, 2.6, fill="#f2b705", outline="#8a6a00", width=0.06, r=0.2)   # puente de disparo
    for k, nombre in enumerate(("VCC", "OUT", "GND")):                       # patas
        px_ = xb + 8.0 + k * 1.5
        c.rect(px_ - 0.16, yb + alto - 1.6, 0.32, 1.4, fill="#c9a227")
        c.circle(px_, yb + alto - 0.5, 0.42, fill="#c9a227")
        c.text(px_, yb + alto - 2.1, nombre, 0.4, "#ffffff", "Bold")
    c.callout(xb + 0.4, 7.2, ["Tx · retardo"], target=(pots["Tx"], yb + 0.9), size=0.52)
    c.callout(xb + 7.4, 7.2, ["Sx · sensibilidad"], target=(pots["Sx"] + 0.4, yb + 0.9), size=0.52)
    c.callout(xb + ancho + 1.4, yb + 2.2, ["Puente:", "disparo único o repetible"], target=(xb + ancho - 1.5, yb + 2.4), size=0.52)
    c.callout(xb + ancho + 1.4, yb + 8.0, ["Patas: VCC · OUT · GND", "(orden del manual del kit)"], target=(xb + 11.0, yb + alto - 0.5), size=0.52)
    # --- tabla
    yt = 28.4
    cols = [("Control o pata", 1.5, 11.0), ("Qué hace", 12.5, 30.0), ("Datos del manual del kit", 42.5, 18.0)]
    filas = [("Retardo (Tx)", "cuánto tiempo se queda OUT en HIGH después de detectar", "de unos 3-5 s hasta 5 min"),
             ("Sensibilidad (Sx)", "qué tan lejos ve: más sensible = más alcance", "de 3 a 7 metros"),
             ("Puente de disparo", "un solo disparo, o disparos que se repiten con el movimiento", "dos posiciones"),
             ("VCC · GND", "alimentación del sensor (5 V) y tierra", "VCC de 5 a 20 V"),
             ("OUT", "la salida que lee el Arduino: HIGH = movimiento", "3,3 V cuando detecta")]
    for (t, xx, w) in cols:
        c.rect(xx, yt, w, 1.8, fill=VINO, outline="#ffffff", width=0.05)
        c.text(xx + w / 2, yt + 0.92, t, 0.58, "#ffffff", "Bold")
    for r, fila in enumerate(filas):
        yy = yt + 1.8 + r * 1.75
        for (t, xx, w), v in zip(cols, fila):
            c.rect(xx, yy, w, 1.75, fill="#ffffff", outline="#cfc9b8", width=0.05)
            c.text(xx + 0.5, yy + 0.9, v, 0.5, TINTA, "SemiBold" if xx == 1.5 else "Medium", anchor="lm")
    _caja_aviso(c, 1.5, 40.2, 59.0, 4.4, "Antes de conectar",
                ["Voltea el módulo y lee las letras junto a las 3 patas. El orden VCC · OUT · GND puede ser distinto en tu módulo: si lo conectas al revés, puede dañarse."], 0.56)
    c.save(os.path.join(AQUI, "P08_pir_conoce.png"))
    print("P08 conoce listo")


def _segmentos(c, x0, esc, y_alto, y_bajo, segs, t_max, color=VINO, w=0.22):
    """Señal digital que vale HIGH en los intervalos 'segs' [(t0, t1), ...] y LOW fuera de ellos."""
    pts = [(x0, y_bajo)]
    for t0, t1 in segs:
        pts += [(x0 + t0 * esc, y_bajo), (x0 + t0 * esc, y_alto), (x0 + t1 * esc, y_alto), (x0 + t1 * esc, y_bajo)]
    pts.append((x0 + t_max * esc, y_bajo))
    c.line(pts, color, w, ends=False)


def pir_senal():
    """Lo que hace OUT en el tiempo: calentamiento, disparo único y disparo repetible (ilustración)."""
    c = Canvas(62, 44)
    c.header("P08 · Qué hace la salida OUT del PIR en el tiempo", "Ilustración con valores de ejemplo (retardo de 6 s): el tuyo depende de la perilla Tx y del puente de disparo")
    naranja, gris = "#d98200", "#dcd8cc"
    x0 = 15.0
    # --- 1) calentamiento
    esc1, tmax1 = 0.5, 90
    c.text(1.5, 5.6, "1 · Al recibir 5 V: calentamiento", 0.8, TINTA, "Bold", anchor="lm")
    ya, yb = 8.0, 11.2
    c.rect(x0, ya - 1.0, 60 * esc1, (yb - ya) + 2.0, fill="#fbe3e3", r=0.2)
    c.text(x0 + 15.0, ya - 1.7, "casi 1 minuto: pueden aparecer falsas detecciones", 0.55, "#b00020", "SemiBold")
    c.text(x0 - 0.5, ya, "HIGH", 0.46, GRIS_T, "SemiBold", anchor="rm")
    c.text(x0 - 0.5, yb, "LOW", 0.46, GRIS_T, "SemiBold", anchor="rm")
    _segmentos(c, x0, esc1, ya, yb, [(5, 9), (16, 18), (27, 35), (48, 50), (72, 80)], tmax1)
    c.text(x0 + 76 * esc1, ya - 1.7, "movimiento real", 0.52, VINO, "SemiBold")
    ye = 13.2
    c.line([(x0, ye), (x0 + tmax1 * esc1, ye)], TINTA, 0.08, ends=False)
    for t in range(0, 91, 10):
        xt = x0 + t * esc1
        c.line([(xt, ye - 0.25), (xt, ye + 0.25)], TINTA, 0.08, ends=False)
        c.text(xt, ye + 1.0, f"{t} s", 0.46, TINTA, "SemiBold")
    # --- 2) y 3) disparo único / repetible
    esc, tmax = 1.4, 32
    movs = [(3, 4), (8, 9), (20, 21)]

    def panel(ytop, titulo, high, bloqueos):
        c.text(1.5, ytop, titulo, 0.8, TINTA, "Bold", anchor="lm")
        ym0 = ytop + 1.6
        c.text(x0 - 0.5, ym0 + 0.6, "movimiento", 0.46, GRIS_T, "SemiBold", anchor="rm")
        for t0, t1 in movs:
            c.rect(x0 + t0 * esc, ym0, (t1 - t0) * esc, 1.2, fill=naranja, r=0.15)
        ya_, yb_ = ytop + 4.6, ytop + 7.8
        for t0, t1 in bloqueos:
            c.rect(x0 + t0 * esc, ya_ - 0.8, (t1 - t0) * esc, (yb_ - ya_) + 1.6, fill=gris, r=0.15)
            c.text(x0 + (t0 + t1) / 2 * esc, (ya_ + yb_) / 2 - 0.5, "≈ 3 s", 0.46, GRIS_T, "Bold")
            c.text(x0 + (t0 + t1) / 2 * esc, (ya_ + yb_) / 2 + 0.5, "sin detectar", 0.4, GRIS_T, "SemiBold")
        c.text(x0 - 0.5, ya_, "HIGH", 0.46, GRIS_T, "SemiBold", anchor="rm")
        c.text(x0 - 0.5, yb_, "LOW", 0.46, GRIS_T, "SemiBold", anchor="rm")
        c.text(x0 - 4.2, (ya_ + yb_) / 2, "OUT", 0.55, VINO, "Bold", anchor="rm")
        _segmentos(c, x0, esc, ya_, yb_, high, tmax)
        return ya_, yb_
    ya2, yb2 = panel(16.6, "2 · Disparo único: el retardo no se reinicia", [(3, 9), (20, 26)], [(9, 12), (26, 29)])
    c.text(x0 + 6 * esc, ya2 - 0.6, "retardo = 6 s", 0.48, VINO, "SemiBold")
    c.text(x0 + 3 * esc, yb2 + 1.7, "El movimiento de 8 a 9 s no cambia nada: OUT ya estaba en HIGH, y el retardo no se reinicia.", 0.5, "#6b5d52", "Medium", anchor="lm")
    ya3, yb3 = panel(28.4, "3 · Disparo repetible: cada movimiento reinicia el retardo", [(3, 15), (20, 27)], [(15, 18), (27, 30)])
    c.text(x0 + 9 * esc, ya3 - 0.6, "6 s después del último movimiento", 0.48, VINO, "SemiBold")
    c.text(x0 + 3 * esc, yb3 + 1.7, "El movimiento de 8 a 9 s reinicia el retardo: OUT sigue en HIGH hasta 6 s después de él (a los 15 s).", 0.5, "#6b5d52", "Medium", anchor="lm")
    ye = 40.2
    c.line([(x0, ye), (x0 + tmax * esc, ye)], TINTA, 0.08, ends=False)
    for t in range(0, 33, 4):
        xt = x0 + t * esc
        c.line([(xt, ye - 0.25), (xt, ye + 0.25)], TINTA, 0.08, ends=False)
        c.text(xt, ye + 1.0, f"{t} s", 0.46, TINTA, "SemiBold")
    c.text(c.w_u - 1.2, c.h_u - 0.6, "El manual del kit: tras el retardo, OUT baja a LOW unos 3 s y en ese tiempo no detecta nada. Los tiempos de aquí son de ejemplo.", 0.48, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P08_pir_senal.png"))
    print("P08 señal listo")


def alarma_estados():
    """Estados de la alarma P08 y qué los cambia."""
    c = Canvas(54, 32)
    c.header("P08 · Los estados de la alarma", "Dos variables lo deciden: armada (botón) y el valor que lee el pin 7 (PIR)")
    ya, r = 14.0, 5.3
    est = [(9.5, "DESARMADA", ["LED apagado", "no vigila"], "#eceae4", "#8a8a8a"),
           (27.0, "ARMADA", ["LED encendido", "vigila el PIR"], "#fff3bf", "#c99a00"),
           (44.5, "SONANDO", ["sirena de 1,8 s", "(6 vueltas)"], "#fbe3e3", "#b00020")]
    for cx, nombre, lineas, fondo, borde in est:
        c.circle(cx, ya, r, fill=fondo, outline=borde, width=0.14)
        c.text(cx, ya - 1.6, nombre, 0.85, TINTA, "Bold")
        for i, s in enumerate(lineas):
            c.text(cx, ya + 0.2 + i * 1.15, s, 0.56, GRIS_T, "SemiBold")
    dy = 2.4
    _arco(c, (9.5 + r - 0.6, ya - dy), (27.0 - r + 0.6, ya - dy), -2.8, VINO)
    c.text(18.25, 7.8, "botón", 0.7, VINO, "Bold")
    _arco(c, (27.0 + r - 0.6, ya - dy), (44.5 - r + 0.6, ya - dy), -2.8, "#b00020")
    c.text(35.75, 7.4, "PIR en HIGH", 0.7, "#b00020", "Bold")
    c.text(35.75, 8.5, "(y la alarma está armada)", 0.5, GRIS_T, "SemiBold")
    _arco(c, (27.0 - r + 0.6, ya + dy), (9.5 + r - 0.6, ya + dy), 2.8, VINO)
    c.text(18.25, 20.1, "botón", 0.7, VINO, "Bold")
    _arco(c, (44.5 - r + 0.6, ya + dy), (27.0 + r - 0.6, ya + dy), 2.8, GRIS_T)
    c.text(35.75, 20.1, "termina la sirena", 0.62, GRIS_T, "Bold")
    c.text(35.75, 21.2, "si el PIR sigue en HIGH, vuelve a sonar", 0.5, GRIS_T, "SemiBold")
    _arco(c, (44.5, ya + r), (9.5, ya + r), 7.6, VINO)
    c.text(27.0, 28.3, "botón presionado mientras suena: se desarma", 0.64, VINO, "Bold")
    c.text(27.0, 30.0, "En el programa, armada = !armada cada vez que el botón pasa de HIGH a LOW.", 0.52, GRIS_T, "Medium")
    c.save(os.path.join(AQUI, "P08_estados.png"))
    print("P08 estados listo")


TODOS = {"P01": [p01], "P02": [p02, esquema_p02, cableado_p02], "P03": [p03, cableado_p03], "P04": [p04, cableado_p04],
         "P05": [p05, cableado_p05, esquema_pullup, boton_patas], "P06": [rebote_p06, estados_p06],
         "P07": [zumbadores, frecuencia, p07a, cableado_p07a, p07b, cableado_p07b, for_diagrama],
         "P08": [pir_conoce, pir_senal, p08, cableado_p08, alarma_estados]}

if __name__ == "__main__":
    pedidos = sys.argv[1:] or list(TODOS)
    for clave in pedidos:
        for f in TODOS[clave]:
            f()
