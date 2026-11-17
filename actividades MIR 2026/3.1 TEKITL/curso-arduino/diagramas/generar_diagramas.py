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


# ------------------------------------------------------------------ Sesión 5: perilla (P09) y brillo con PWM (P10)
# El kit llega desarmado de la visita anterior: el Paso 0 arma un LED en el pin 9 (el de P02, con ~) y P09 agrega el potenciómetro.
# El potenciómetro va a la derecha (columnas 26, 28 y 30): así los cables de 5 V y A0, que rodean la placa por la derecha, no cruzan a los demás.
Y_A0_ABAJO, Y_5V_ABAJO = 0.9, 2.2        # cuánto por debajo del borde de la placa corren los cables de A0 y 5 V
X_A0_DER, X_5V_DER = 35.3, 36.3          # por dónde suben (el de 5 V por fuera)
ARRIBA_A0, ARRIBA_5V = 22.8, 21.6        # a qué altura (desde el borde superior del protoboard) giran hacia el potenciómetro


def _led_pin9(circ, nuevo):
    """LED rojo en el pin 9: los mismos agujeros de P02 (columnas 18 a 23), pero con el cable morado en el pin 9."""
    s = (lambda n: n) if nuevo else (lambda n: None)
    circ.led(anodo=(22, "g"), catodo=(23, "g"), color="rojo", step=s(1), nombre="LED9")
    circ.resistor((18, "h"), (22, "h"), 220, step=s(2), nombre="R9")
    circ.wire(("bb", 23, "j"), ("rail", "B", "-", 23), "negro", step=s(3))
    circ.wire(("ard", "GND"), ("rail", "B", "-", 13), "negro", via=0.45, step=s(4))
    circ.wire(("ard", "D9"), ("bb", 18, "j"), "morado", step=s(5), badge=(21.0, 29.6))


def _pot_cables(circ, bb, ard, nuevo):
    """Potenciómetro en las columnas 26 (extremo a GND), 28 (centro a A0) y 30 (extremo a 5 V). Numerado para armarlo: GND, A0 y al final 5 V."""
    s = (lambda n: n) if nuevo else (lambda n: None)
    circ.potenciometro(26, step=s(1))
    circ.wire(("bb", 26, "j"), ("rail", "B", "-", 26), "negro", step=s(2))
    x_a0, _ = ard.xy("A0")
    x_5v, _ = ard.xy("5V")
    borde = ard.y + ard.H
    xj28 = bb.hole(28, "j")[0]
    xj30 = bb.hole(30, "j")[0]
    circ.wire(("ard", "A0"), ("bb", 28, "j"), "amarillo", step=s(3),
              ruta=[(x_a0, borde + Y_A0_ABAJO), (X_A0_DER, borde + Y_A0_ABAJO), (X_A0_DER, bb.y + ARRIBA_A0), (xj28, bb.y + ARRIBA_A0)],
              badge=(28.0, borde + Y_A0_ABAJO))
    circ.wire(("ard", "5V"), ("bb", 30, "j"), "rojo", step=s(4),
              ruta=[(x_5v, borde + Y_5V_ABAJO), (X_5V_DER, borde + Y_5V_ABAJO), (X_5V_DER, bb.y + ARRIBA_5V), (xj30, bb.y + ARRIBA_5V)],
              badge=(32.0, borde + Y_5V_ABAJO))


def _verificar_pot(circ):
    a, w, b = circ.elems["POT"]
    circ.exigir(("ard", "GND"), a, "el extremo izquierdo del potenciómetro debe llegar a GND")
    circ.exigir(("ard", "A0"), w, "el centro del potenciómetro debe llegar a A0")
    circ.exigir(("ard", "5V"), b, "el extremo derecho del potenciómetro debe llegar a 5 V")
    circ.prohibir(w, ("ard", "5V"), "el centro no puede estar unido a 5 V")
    circ.prohibir(w, ("ard", "GND"), "el centro no puede estar unido a GND")
    circ.prohibir(a, b, "los dos extremos del potenciómetro no pueden estar unidos")
    circ.prohibir(("ard", "A0"), ("ard", "5V"), "A0 y 5 V no pueden tocarse")
    circ.prohibir(("ard", "A0"), ("ard", "GND"), "A0 y GND no pueden tocarse")
    circ.prohibir(("ard", "5V"), ("ard", "GND"), "5 V y GND no pueden tocarse")


def p09_paso0():
    c = Canvas(38.5, 58.0)
    c.header("Paso 0 · LED en el pin 9", "El circuito de P02, pero con el cable de señal en el pin 9, que lleva el símbolo ~ (vista desde arriba, parte izquierda)")
    bb = Breadboard(3.0, 4.6, cols=30)
    ard = Arduino(bb.x + 2.6, bb.y + bb.H + 6.2)
    circ = Circuit(c, ard, bb)
    _led_pin9(circ, nuevo=True)
    _verificar_grupo(circ, 9, "D9")
    circ.prohibir(("ard", "5V"), ("ard", "GND"), "5V y GND no pueden tocarse")
    circ.draw()
    ax, ay = bb.hole(22, "g")
    kx, ky = bb.hole(23, "g")
    cy_led = min(ay, ky) - 2.5
    my = (cy_led + 1.55 + ay) / 2 + 0.1
    c.callout(bb.x + 7.5, bb.y + 5.0, ["Pata larga (+)", "va hacia la resistencia"], target=(ax - 0.95 - 0.5, my), size=0.6)
    c.callout(kx + 1.6, bb.y + 5.0, ["Pata corta (−)", "lado plano del LED"], target=(kx + 0.95 + 0.5, my), size=0.6)
    rx, ry = bb.hole(22, "h")
    c.callout(kx + 0.6, bb.row_y["h"] - 0.5, ["Resistencia 220 Ω", "rojo · rojo · café"], target=(rx - 1.4, ry), size=0.55)
    _leyenda(c, ard.x + 0.5, ard.y + ard.H + 2.0, [(COL["negro"], "GND  (−, tierra)"), (COL["morado"], "Señal del pin 9 (con ~)")])
    c.text(c.w_u - 1.2, c.h_u - 1.2, "Mismo montaje de P02, con el cable en el pin 9", 0.5, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P09_paso0_led_pin9.png"))
    print("Paso 0 listo")
    for fila in sorted((f for f in circ.table if f[0]), key=lambda t: t[0]):
        print("  ", fila)


def p09():
    c = Canvas(38.5, 66.5)
    c.header("P09 · La perilla y los números", "Sobre el LED del pin 9 agrega el potenciómetro: GND, A0 y al final 5 V (vista desde arriba, parte izquierda)")
    bb = Breadboard(3.0, 4.6, cols=30)
    ard = Arduino(bb.x + 2.6, bb.y + bb.H + 6.2)
    circ = Circuit(c, ard, bb)
    _led_pin9(circ, nuevo=False)
    _pot_cables(circ, bb, ard, nuevo=True)
    _verificar_grupo(circ, 9, "D9")
    _verificar_pot(circ)
    circ.draw()
    lx, ly = _led_cuerpo(bb, 22, 23)
    c.callout(bb.x + 1.6, bb.y + 4.2, ["LED del pin 9:", "ya armado en el Paso 0"], target=(lx - 1.0, ly - 1.6), size=0.54)
    xp = bb.hole(28, "f")[0]
    c.callout(bb.x + 16.0, bb.y + 4.2, ["Cada pata en su columna.", "El CENTRO va a A0"], target=(xp - 1.4, bb.hole(28, "f")[1] - 3.6), size=0.54)
    _leyenda(c, ard.x + 0.5, ard.y + ard.H + 5.0, [(COL["negro"], "GND  (−, tierra)"), (COL["morado"], "Señal del pin 9 (ya está)"),
                                                  (COL["amarillo"], "Centro del potenciómetro a A0 (nuevo)"), (COL["rojo"], "+5 V al extremo del potenciómetro (nuevo)")])
    c.text(c.w_u - 1.2, c.h_u - 1.2, "Los números del 1 al 4 son lo nuevo. El cable amarillo va al CENTRO; el rojo, a un extremo.", 0.5, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P09_perilla_serie.png"))
    print("P09 listo")
    for fila in sorted((f for f in circ.table if f[0]), key=lambda t: t[0]):
        print("  ", fila)


def p10():
    c = Canvas(38.5, 66.5)
    c.header("P10 · Perilla y brillo", "El mismo montaje de P09, con el LED del pin 9: no hay nada nuevo que conectar (vista desde arriba)")
    bb = Breadboard(3.0, 4.6, cols=30)
    ard = Arduino(bb.x + 2.6, bb.y + bb.H + 6.2)
    circ = Circuit(c, ard, bb)
    _led_pin9(circ, nuevo=False)
    _pot_cables(circ, bb, ard, nuevo=False)
    _verificar_grupo(circ, 9, "D9")
    _verificar_pot(circ)
    circ.prohibir(("ard", "D9"), ("ard", "A0"), "el pin 9 y A0 no pueden tocarse")
    circ.draw()
    lx, ly = _led_cuerpo(bb, 22, 23)
    c.callout(bb.x + 1.6, bb.y + 4.2, ["LED en el pin 9: este pin", "tiene el símbolo ~ (PWM)"], target=(lx - 1.0, ly - 1.6), size=0.54)
    xp = bb.hole(28, "f")[0]
    c.callout(bb.x + 16.0, bb.y + 4.2, ["Potenciómetro: gira el", "rotor con el desarmador"], target=(xp - 1.4, bb.hole(28, "f")[1] - 3.6), size=0.54)
    _leyenda(c, ard.x + 0.5, ard.y + ard.H + 5.0, [(COL["negro"], "GND  (−, tierra)"), (COL["morado"], "Pin 9: salida PWM (el LED)"),
                                                  (COL["amarillo"], "Centro del potenciómetro a A0 (entrada)"), (COL["rojo"], "+5 V al extremo del potenciómetro")])
    c.text(c.w_u - 1.2, c.h_u - 1.2, "Lo que cambia hoy es el programa. Pin 9 = salida (LED); A0 = entrada (perilla).", 0.5, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P10_perilla_brillo.png"))
    print("P10 listo")


def cableado_p09():
    E = Esquema(36, 25.8)
    E.titulo("P09 · La perilla y los números", "esquema de conexiones · el potenciómetro reparte los 5 V: lo que sale por el centro va a A0")
    E.placa(1.5, 5.0, 7.5, 17.5, "Arduino\nUNO R3", [("5V", "5V", 8.5), ("A0", "A0", 14.5), ("GND", "GND", 20.5)])
    E.potenciometro("P", 22.0, 8.5, 20.5)
    E.cable("rojo", "5V", "P.a")
    E.cable("amarillo", "A0", "P.w")
    E.cable("negro", "GND", "P.b")
    E.nota(9.5, 7.05, "5 V · cable rojo")
    E.nota(9.5, 13.05, "A0 (entrada) · cable amarillo")
    E.nota(9.5, 19.05, "cable negro")
    E.etiqueta(27.5, 12.2, "Potenciómetro")
    E.nota(27.5, 14.2, "10 kΩ (B103)", anchor="mm")
    E.nota(23.4, 8.5, "extremo", anchor="lm")
    E.nota(23.4, 20.5, "extremo", anchor="lm")
    E.nota(14.4, 16.3, "centro (cursor)", anchor="mm")
    E.nota(1.5, 24.6, "El centro SOLO va a A0. Corriente por el potenciómetro: 5 V ÷ 10 kΩ = 0,5 mA.", color="#8a8a8a")
    E.exigir("5V", "P.a", "5 V debe llegar a un extremo del potenciómetro")
    E.exigir("A0", "P.w", "A0 debe llegar al centro del potenciómetro")
    E.exigir("GND", "P.b", "GND debe llegar al otro extremo del potenciómetro")
    E.prohibir("5V", "GND", "5V y GND no pueden tocarse")
    E.prohibir("A0", "5V", "A0 y 5V no pueden tocarse")
    E.prohibir("A0", "GND", "A0 y GND no pueden tocarse")
    E.dibujar(os.path.join(AQUI, "P09_perilla_serie_cableado.png"))
    print("P09 cableado listo")


def cableado_p10():
    E = Esquema(38, 40.0)
    E.titulo("P10 · Perilla y brillo", "esquema de conexiones · la perilla entra por A0 y el LED sale por el pin 9 (el que tiene ~)")
    E.placa(1.5, 5.0, 7.5, 31.5, "Arduino\nUNO R3", [("D9", "D9", 8.5), ("5V", "5V", 16.5), ("A0", "A0", 23.5), ("GND", "GND", 30.5)])
    _rama(E, 8.5, 9, "rojo", "LED rojo", "D9", 33.0, 30.5)
    E.nota(27.0, 11.7, "brillo según la perilla", anchor="mm")
    E.potenciometro("P", 22.0, 16.5, 30.5)
    E.cable("rojo", "5V", "P.a")
    E.cable("amarillo", "A0", "P.w")
    E.cable("negro", "GND", "P.b")
    E.cable("negro", "P.b", "TAP9")
    E.nota(9.5, 15.05, "5 V · cable rojo")
    E.nota(9.5, 22.05, "A0 (entrada) · cable amarillo")
    E.nota(9.5, 29.05, "cable negro (riel GND)")
    E.etiqueta(27.5, 21.0, "Potenciómetro")
    E.nota(27.5, 23.0, "10 kΩ (B103)", anchor="mm")
    E.nota(14.4, 24.3, "centro (cursor)", anchor="mm")
    E.nota(33.6, 13.0, "cable negro", anchor="rm")
    E.nota(27.0, 31.8, "riel GND: la tira azul (−)", anchor="lm")
    E.nota(1.5, 38.6, "Entrada analógica (A0) y salida PWM (pin 9) comparten el GND y nada más.", color="#8a8a8a")
    E.puntos.add("P.b")
    E.exigir("D9", "R9.a", "el pin 9 debe llegar a la resistencia del LED")
    E.exigir("R9.b", "LED9.a", "la resistencia debe llegar a la pata larga (+) del LED")
    E.exigir("LED9.k", "GND", "la pata corta (−) del LED debe llegar a GND")
    E.exigir("5V", "P.a", "5 V debe llegar a un extremo del potenciómetro")
    E.exigir("A0", "P.w", "A0 debe llegar al centro del potenciómetro")
    E.exigir("GND", "P.b", "GND debe llegar al otro extremo del potenciómetro")
    E.prohibir("5V", "GND", "5V y GND no pueden tocarse")
    E.prohibir("A0", "5V", "A0 y 5V no pueden tocarse")
    E.prohibir("A0", "GND", "A0 y GND no pueden tocarse")
    E.prohibir("D9", "A0", "el pin 9 y A0 no pueden tocarse")
    E.prohibir("D9", "GND", "el pin 9 y GND no pueden tocarse")
    E.dibujar(os.path.join(AQUI, "P10_perilla_brillo_cableado.png"))
    print("P10 cableado listo")


# ------------------------------------------------------------------ Sesión 5: diagramas de ideas
def _cdiv(a, b):
    """División entera como la hace Arduino (C): trunca hacia cero."""
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q


def _amap(x, a, b, c, d):
    """map() de Arduino con su aritmética entera."""
    return _cdiv((x - a) * (d - c), (b - a)) + c


def _coma(x, dec=1):
    """Número con coma decimal y sin ceros sobrantes: 7.5 -> '7,5', 5.0 -> '5'."""
    s = f"{x:.{dec}f}".rstrip("0").rstrip(".")
    return s.replace(".", ",")


def perilla_conoce():
    """El potenciómetro por fuera y por dentro: un divisor de voltaje."""
    c = Canvas(73, 41.6)
    c.header("P09 · Conoce tu potenciómetro", "Una resistencia de 10 kΩ con una tercera pata, el cursor, que se desliza por ella y reparte el voltaje")
    # ---- por fuera (dibujo grande de la vista de arriba)
    c.text(12.5, 5.5, "Por fuera", 0.85, TINTA, "Bold")
    s = 2.0
    cx, y0 = 12.5, 8.0
    w, h = 5.9 * s, 5.5 * s
    c.rect(cx - w / 2, y0, w, h, fill="#1f1f22", outline="#050505", width=0.1, r=2.4)
    for sx in (-1, 1):
        c.circle(cx + sx * (w / 2 - 1.1), y0 + h - 0.8, 0.5, fill="#3a3a3f")
    ry = y0 + 3.0 * s
    c.circle(cx, ry, 1.75 * s, fill="#2b2b30", outline="#4d4d55", width=0.1)
    c.circle(cx, ry, 1.4 * s, outline="#3d3d44", width=0.07)
    c.line([(cx - 1.25 * s, ry + 0.55 * s), (cx + 1.25 * s, ry - 0.55 * s)], "#8e8e96", 0.7, ends=False)
    c.rect(cx - 1.3 * s, y0 + 0.45 * s, 2.6 * s, 0.95 * s, fill="#0f0f12", r=0.3)
    c.text(cx, y0 + 0.93 * s, "B103", 0.95, "#d9d9d9", "Bold")
    # flecha curva: el rotor gira (menos de una vuelta)
    arco = [(cx + 4.7 * math.cos(math.radians(a)), ry + 4.7 * math.sin(math.radians(a))) for a in range(20, 161, 10)]
    c.line(arco, VINO, 0.16, ends=False)
    pa, pb = arco[-2], arco[-1]
    ang = math.atan2(pb[1] - pa[1], pb[0] - pa[0])
    c.poly([pb, (pb[0] - 0.7 * math.cos(ang - 0.45), pb[1] - 0.7 * math.sin(ang - 0.45)),
            (pb[0] - 0.7 * math.cos(ang + 0.45), pb[1] - 0.7 * math.sin(ang + 0.45))], fill=VINO)
    # patas
    yp = y0 + h
    for dx, nombre, sub in ((-4.0, "extremo", ""), (0.0, "centro", "(cursor)"), (4.0, "extremo", "")):
        c.rect(cx + dx - 0.18, yp - 0.2, 0.36, 3.0, fill="#c9a227")
        c.circle(cx + dx, yp + 2.8, 0.34, fill="#c9a227")
        c.text(cx + dx, yp + 4.2, nombre, 0.5, TINTA, "SemiBold")
        if sub:
            c.text(cx + dx, yp + 5.1, sub, 0.5, VINO, "Bold")
    c.text(cx, ry + 1.9, "ranura", 0.5, "#c9c9d0", "SemiBold")
    _lista(c, 1.5, 28.0, ["Se gira con un desarmador plano pequeño:", "la punta entra en la ranura del rotor.",
                          "B103: el 103 es 10 × 10³ = 10 000 Ω = 10 kΩ.", "Gira menos de una vuelta (240° a 280°, según",
                          "las hojas de datos del kit).", "Va en el protoboard con cada pata en una", "columna distinta."], 0.5, 1.2, GRIS_T)
    # ---- por dentro: cinco posiciones del cursor
    c.text(48.0, 5.5, "Por dentro: un divisor de voltaje (cinco posiciones del cursor)", 0.85, TINTA, "Bold")
    yt, yb = 11.2, 23.7
    for i in range(5):
        f = i / 4
        x0 = 27.0 + i * 9.0
        tx, tw = x0 + 3.4, 1.5
        yw = yb - f * (yb - yt)
        c.rect(tx, yt, tw, yw - yt + 0.001, fill="#f6d0d0")
        if f > 0:
            c.rect(tx, yw, tw, yb - yw, fill="#cfdcf3")
        c.rect(tx, yt, tw, yb - yt, outline=TINTA, width=0.1)
        c.line([(tx + tw / 2, yt - 1.5), (tx + tw / 2, yt)], "#c8202b", 0.14, ends=False)
        c.text(tx + tw / 2, yt - 2.2, "5 V", 0.55, "#c8202b", "Bold")
        c.line([(tx + tw / 2, yb), (tx + tw / 2, yb + 1.2)], "#1d5fd1", 0.14, ends=False)
        c.text(tx + tw / 2, yb + 1.9, "GND", 0.55, "#1d5fd1", "Bold")
        r_ar, r_ab = 10.0 * (1 - f), 10.0 * f
        c.text(tx - 0.3, yt + max((yw - yt) / 2, 0.6), f"{_coma(r_ar)} kΩ", 0.5, "#a02020", "SemiBold", anchor="rm")
        c.text(tx - 0.3, yb - max((yb - yw) / 2, 0.6), f"{_coma(r_ab)} kΩ", 0.5, "#1d4fa0", "SemiBold", anchor="rm")
        c.poly([(tx + tw, yw), (tx + tw + 1.0, yw - 0.5), (tx + tw + 1.0, yw + 0.5)], fill=TINTA)
        c.line([(tx + tw + 1.0, yw), (tx + tw + 2.2, yw)], TINTA, 0.14, ends=False)
        c.text(tx + tw + 2.5, yw, "A0", 0.55, TINTA, "Bold", anchor="lm")
        v = 5.0 * f
        c.text(x0 + 4.5, 27.0, f"cursor al {int(f * 100)} %", 0.5, GRIS_T, "SemiBold")
        c.text(x0 + 4.5, 28.3, f"{_coma(v, 2)} V", 0.8, VINO, "Bold")
        c.text(x0 + 4.5, 29.6, f"lectura ≈ {round(v / 5 * 1023)}", 0.5, TINTA, "SemiBold")
    c.text(27.0, 7.2, "Rojo = parte de la resistencia entre el cursor y 5 V (R arriba). Azul = entre el cursor y GND (R abajo).", 0.5, GRIS_T, "Medium", anchor="lm")
    c.rect(27.0, 32.2, 45.0, 4.6, fill="#ffffff", outline="#cfc9b8", width=0.08, r=0.4)
    c.text(49.5, 33.7, "V del centro = 5 V × R abajo ÷ (R arriba + R abajo)", 0.72, VINO, "Bold")
    c.text(49.5, 35.3, "analogRead ≈ V ÷ 5 V × 1023     (la suma R arriba + R abajo siempre da 10 kΩ)", 0.55, TINTA, "Medium")
    _caja_aviso(c, 1.5, 36.9, 70.0, 3.9, "Antes de conectar",
                ["Las patas de los extremos van una a 5 V y otra a GND. El CENTRO solo va a A0: si lo conectas a 5 V o a GND, al girar se haría un cortocircuito."], 0.55)
    c.save(os.path.join(AQUI, "P09_perilla_conoce.png"))
    print("P09 conoce listo")


def lectura_adc():
    """De volts a números: analogRead convierte 0 a 5 V en 0 a 1023."""
    c = Lienzo(66, 40)
    c.header("P09 · De volts a números", "analogRead convierte el voltaje de un pin analógico en un número entero de 0 a 1023")
    # barra vertical de voltaje con su escala numérica
    bx, by0, by1 = 17.0, 7.0, 31.0
    c.text(bx - 5.0, 5.4, "Voltaje en A0", 0.7, TINTA, "Bold")
    c.text(bx + 8.0, 5.4, "Número que devuelve", 0.7, TINTA, "Bold")
    c.rect(bx, by0, 2.2, by1 - by0, fill="#e7e1d2", outline=TINTA, width=0.1)
    for i in range(5):
        f = i / 4
        yy = by1 - f * (by1 - by0)
        v = 5.0 * f
        n = round(v / 5 * 1023)
        c.line([(bx - 1.0, yy), (bx + 2.2 + 1.0, yy)], TINTA, 0.1, ends=False)
        c.text(bx - 1.4, yy, f"{_coma(v, 2)} V", 0.7, VINO, "Bold", anchor="rm")
        c.text(bx + 4.2, yy, f"{n}", 0.9, TINTA, "Bold", anchor="lm")
    # escalones: un acercamiento
    ex, ey = 36.0, 8.0
    c.text(ex + 11.0, 5.4, "Un acercamiento: cada escalón", 0.7, TINTA, "Bold")
    c.rect(ex, ey, 22.0, 12.0, fill="#fbf8f0", outline="#cfc9b8", width=0.08, r=0.3)
    pts = [(ex + 1.0, ey + 11.0)]
    for k in range(6):
        xa = ex + 1.0 + k * 3.4
        ya = ey + 11.0 - k * 1.5
        pts += [(xa, ya), (xa, ya - 1.5)]
        pts.append((xa + 3.4, ya - 1.5))
    c.line(pts, VINO, 0.2, ends=False)
    c.line([(ex + 1.0, ey + 11.0), (ex + 1.0 + 6 * 3.4, ey + 11.0 - 6 * 1.5)], "#b3ae9c", 0.1, ends=False)
    c.text(ex + 11.0, ey + 13.2, "cada número cubre unos 4,9 mV de voltaje", 0.52, GRIS_T, "SemiBold")
    c.text(ex + 11.0, ey + 14.3, "(5 V ÷ 1024 niveles)", 0.52, GRIS_T, "SemiBold")
    # digitalRead frente a analogRead
    yy = 25.2
    c.text(ex + 11.0, yy, "digitalRead  frente a  analogRead", 0.7, TINTA, "Bold")
    c.rect(ex, yy + 1.0, 10.5, 3.6, fill="#ffffff", outline=TINTA, width=0.08, r=0.4)
    c.text(ex + 5.25, yy + 2.2, "digitalRead", 0.55, VINO, "Bold")
    c.text(ex + 5.25, yy + 3.5, "2 valores: HIGH o LOW", 0.5, TINTA, "Medium")
    c.rect(ex + 11.5, yy + 1.0, 10.5, 3.6, fill="#ffffff", outline=TINTA, width=0.08, r=0.4)
    c.text(ex + 16.75, yy + 2.2, "analogRead", 0.55, VINO, "Bold")
    c.text(ex + 16.75, yy + 3.5, "1024 valores: 0 a 1023", 0.5, TINTA, "Medium")
    # código y regla de tres
    c.rect(1.5, 33.4, 34.0, 5.2, fill="#1e1e24", r=0.5)
    c.text(2.7, 35.0, "int lectura = analogRead(A0);", 0.62, "#f2f2f2", "MonoBold", anchor="lm")
    c.text(2.7, 36.6, "float voltaje = lectura * 5.0 / 1023.0;", 0.62, "#f2f2f2", "MonoBold", anchor="lm")
    c.text(37.5, 34.6, "Regla de tres, con lectura = 600:", 0.55, TINTA, "Bold", anchor="lm")
    c.text(37.5, 36.0, "600 × 5 ÷ 1023 = 2,93 V", 0.7, VINO, "Bold", anchor="lm")
    c.text(37.5, 37.4, "Un pin analógico (A0 a A5) tarda unos 100 µs en leerse.", 0.5, GRIS_T, "Medium", anchor="lm")
    c.text(c.w_u - 1.0, c.h_u - 0.7, "El programa supone 5,0 V. Si tu USB da 4,8 V, el voltaje calculado se desvía un poco.", 0.5, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P09_lectura.png"))
    print("P09 lectura listo")


def plotter_ilustracion():
    """Ilustración de la ventana del Serial Plotter con P09a (datos de ejemplo)."""
    c = Canvas(64, 34.5)
    c.header("P09a · La perilla como gráfica", "Ilustración con datos de ejemplo: tus colores, tu escala y tu gráfica se verán un poco distintos")
    x0, y0, W, H = 2.0, 5.0, 60.0, 24.5
    c.rect(x0, y0, W, H, fill="#f3f4f6", outline="#9aa0a6", width=0.1, r=0.6)
    c.rect(x0, y0, W, 2.2, fill="#dfe3e8", outline="#9aa0a6", width=0.1, r=0.6)
    c.text(x0 + 1.0, y0 + 1.15, "Serial Plotter", 0.6, TINTA, "Bold", anchor="lm")
    c.text(x0 + W - 1.0, y0 + 1.15, "9600 baud", 0.5, GRIS_T, "SemiBold", anchor="rm")
    # área de la gráfica
    gx, gy, gw, gh = x0 + 5.5, y0 + 4.2, 42.0, 18.5
    c.rect(gx, gy, gw, gh, fill="#ffffff", outline="#cfd2d6", width=0.08)
    for v in (0, 250, 500, 750, 1000):
        yy = gy + gh - v / 1100 * gh - 1.0
        c.line([(gx, yy), (gx + gw, yy)], "#e6e8eb", 0.06, ends=False)
        c.text(gx - 0.4, yy, str(v), 0.45, GRIS_T, "SemiBold", anchor="rm")

    def yv(v):
        return gy + gh - v / 1100 * gh - 1.0
    c.line([(gx, yv(1023)), (gx + gw, yv(1023))], "#e08a00", 0.14, ends=False)
    c.line([(gx, yv(0)), (gx + gw, yv(0))], "#3a9d5d", 0.14, ends=False)
    pts = [(0, 3), (3, 3), (9, 260), (15, 610), (20, 1000), (24, 1022), (29, 1020), (33, 780), (38, 420), (42, 300), (60, 300)]
    base = []
    for (ta, va), (tb, vb) in zip(pts, pts[1:]):
        for k in range(8):
            u = k / 8
            base.append((ta + (tb - ta) * u, va + (vb - va) * u))
    base.append(pts[-1])
    ruido = [0, 2, -1, 1, -2, 1, 0, -1, 2, -1, 1, 0, -2, 2]
    curva = []
    for i, (tt, vv) in enumerate(base):
        curva.append((gx + 1.0 + tt / 60 * (gw - 2.0), yv(vv + ruido[i % len(ruido)] * 1.0)))
    c.line(curva, "#2a6fdb", 0.2, ends=False)
    # leyenda
    lx = gx + gw + 1.5
    for i, (nombre, col) in enumerate((("Min", "#3a9d5d"), ("Max", "#e08a00"), ("Lectura", "#2a6fdb"))):
        c.rect(lx, gy + 1.0 + i * 1.8, 1.4, 0.45, fill=col)
        c.text(lx + 2.0, gy + 1.22 + i * 1.8, nombre, 0.55, TINTA, "SemiBold", anchor="lm")
    # anotaciones
    c.callout(x0 + 8.5, y0 + 6.0, ["1 · Giras la perilla:", "la línea sube"], target=(gx + 1.0 + 15 / 60 * (gw - 2.0), yv(610)), size=0.5)
    c.callout(x0 + 21.0, y0 + 16.8, ["2 · En el tope:", "se queda arriba, cerca de Max"], target=(gx + 1.0 + 27 / 60 * (gw - 2.0), yv(1021)), size=0.5)
    c.callout(x0 + 33.0, y0 + 8.0, ["3 · Perilla quieta: la línea es", "casi plana (baila 1 o 2 números)"], target=(gx + 1.0 + 50 / 60 * (gw - 2.0), yv(300)), size=0.5)
    c.text(lx, gy + 7.4, "Min y Max son líneas", 0.5, GRIS_T, "Medium", anchor="lm")
    c.text(lx, gy + 8.5, "fijas: sirven de marco", 0.5, GRIS_T, "Medium", anchor="lm")
    c.text(lx, gy + 9.6, "para que la escala", 0.5, GRIS_T, "Medium", anchor="lm")
    c.text(lx, gy + 10.7, "no cambie.", 0.5, GRIS_T, "Medium", anchor="lm")
    c.text(c.w_u - 1.2, c.h_u - 0.8, "Se abre con Herramientas > Serial Plotter. Cierra antes el Monitor Serie: los dos usan el mismo puerto.", 0.5, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P09_plotter.png"))
    print("P09 plotter listo")


def _pwm(c, x0, y_alto, y_bajo, periodo, duty, n, color=VINO, w=0.22):
    """n ciclos de PWM de ancho 'periodo' (en unidades de dibujo); el pin está en HIGH la fracción 'duty' al inicio de cada ciclo."""
    if duty <= 0:
        c.line([(x0, y_bajo), (x0 + n * periodo, y_bajo)], color, w, ends=False)
        return
    if duty >= 1:
        c.line([(x0, y_alto), (x0 + n * periodo, y_alto)], color, w, ends=False)
        return
    pts = []
    for k in range(n):
        xa = x0 + k * periodo
        pts += [(xa, y_bajo), (xa, y_alto), (xa + duty * periodo, y_alto), (xa + duty * periodo, y_bajo), (xa + periodo, y_bajo)]
    c.line(pts, color, w, ends=False)


def _led_vista(c, x, y, brillo, r=1.3):
    """LED visto de frente; 'brillo' de 0 a 1 se pinta como lo percibe el ojo (no es lineal)."""
    b = brillo ** 0.5
    base, luz = (58, 36, 36), (255, 84, 84)
    col = "#%02x%02x%02x" % tuple(int(base[i] + (luz[i] - base[i]) * b) for i in range(3))
    if brillo > 0.05:
        c.circle(x, y, r + 0.55 * b, fill="#ffe3e3")
    c.circle(x, y, r, fill=col, outline="#3a3a3a", width=0.08)


def pwm_a_mano():
    """El mismo reparto del ciclo (50 % encendido) con ciclos de distinta duración: lo que se ve."""
    c = Canvas(62, 38)
    c.header("P10a · PWM a mano: el mismo reparto, ciclos más y más cortos", "La perilla decide cuánto del ciclo está encendido; PERIODO_MS decide qué tan largo es el ciclo")
    filas = [(5.8, "Ciclo de 1 000 ms (1 s)", "1 parpadeo por segundo", "Se ve prender y apagar: es el Blink de la Sesión 1", [1.0, 0.0, 1.0]),
             (14.0, "Ciclo de 100 ms", "10 parpadeos por segundo", "Parpadeo rápido: se ve titilar, pero ya no se alcanza a contar", [0.55, 0.55, 0.55]),
             (22.2, "Ciclo de 20 ms", "50 por segundo", "Se espera un brillo medio: el parpadeo casi no se nota", [0.5])]
    x0, per, n = 3.0, 5.0, 3
    for yt, titulo, sub, que, leds in filas:
        c.text(1.5, yt + 0.3, titulo, 0.8, TINTA, "Bold", anchor="lm")
        c.text(1.5, yt + 1.5, sub, 0.55, GRIS_T, "SemiBold", anchor="lm")
        ya, yb = yt + 3.0, yt + 6.0
        c.line([(x0, ya), (x0 + 26, ya)], "#e2ddd0", 0.06, ends=False)
        c.line([(x0, yb), (x0 + 26, yb)], "#e2ddd0", 0.06, ends=False)
        c.text(x0 - 0.3, ya, "HIGH", 0.4, GRIS_T, "SemiBold", anchor="rm")
        c.text(x0 - 0.3, yb, "LOW", 0.4, GRIS_T, "SemiBold", anchor="rm")
        _pwm(c, x0 + 1.0, ya, yb, per, 0.5, n)
        xa, xb = x0 + 1.0, x0 + 1.0 + per
        yy = yt + 2.1
        c.line([(xa, yy), (xb, yy)], "#1d5fd1", 0.1, ends=False)
        c.line([(xa, yy - 0.25), (xa, yy + 0.25)], "#1d5fd1", 0.1, ends=False)
        c.line([(xb, yy - 0.25), (xb, yy + 0.25)], "#1d5fd1", 0.1, ends=False)
        c.text(xb + 0.4, yy, "1 ciclo", 0.45, "#1d5fd1", "SemiBold", anchor="lm")
        c.text(34.5, yt + 1.3, "Lo que se espera ver", 0.5, GRIS_T, "SemiBold", anchor="lm")
        for i, b in enumerate(leds):
            _led_vista(c, 36.5 + i * 4.0, yt + 4.4, b)
        c.text(34.5, yt + 7.0, que, 0.52, TINTA, "Medium", anchor="lm")
    c.rect(1.5, 31.0, 59.0, 5.6, fill="#fbf3e2", outline=GOLD_BORDE, width=0.1, r=0.5)
    c.text(2.4, 32.4, "analogWrite hace lo mismo, pero con ciclos de unos 2 ms (490 por segundo)", 0.7, VINO, "Bold", anchor="lm")
    c.text(2.4, 33.8, "y lo hace un circuito del chip por su cuenta: el programa queda libre para hacer otra cosa.", 0.55, TINTA, "Medium", anchor="lm")
    c.text(2.4, 35.1, "En P10a el programa no puede hacer nada más: está ocupado con los delay().", 0.55, TINTA, "Medium", anchor="lm")
    c.text(c.w_u - 1.0, c.h_u - 0.7, "Los LED dibujados son una ilustración de lo que se espera: anota lo que ves en el tuyo.", 0.5, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P10_pwm_a_mano.png"))
    print("P10 pwm a mano listo")


def pwm_ciclos():
    """analogWrite: el valor 0 a 255 decide la fracción del ciclo en HIGH."""
    c = Lienzo(64, 41.4)
    c.header("P10 · PWM: lo que hace analogWrite", "El valor de 0 a 255 decide qué parte de cada ciclo (unos 2 ms) está el pin en HIGH")
    c.text(1.5, 5.2, "Instrucción", 0.65, GRIS_T, "Bold", anchor="lm")
    c.text(22.0, 5.2, "Tres ciclos del pin 9 (cada uno dura unos 2 ms)", 0.65, GRIS_T, "Bold", anchor="lm")
    c.text(45.0, 5.2, "Voltaje promedio", 0.65, GRIS_T, "Bold", anchor="lm")
    c.text(58.0, 5.2, "Se ve", 0.65, GRIS_T, "Bold", anchor="lm")
    x0, per = 22.0, 6.0
    for i, val in enumerate((0, 64, 128, 191, 255)):
        yt = 7.0 + i * 5.6
        duty = val / 255
        c.rect(1.0, yt - 0.3, 62.0, 5.2, fill="#fbf8f0" if i % 2 == 0 else "#ffffff", outline=None)
        c.text(1.5, yt + 1.2, f"analogWrite(9, {val})", 0.75, TINTA, "MonoBold", anchor="lm")
        c.text(1.5, yt + 2.9, f"encendido el {round(duty * 100)} % del ciclo", 0.55, GRIS_T, "SemiBold", anchor="lm")
        ya, yb = yt + 0.7, yt + 3.9
        _pwm(c, x0, ya, yb, per, duty, 3)
        c.text(45.0, yt + 2.2, f"{_coma(5 * duty, 2)} V", 0.85, VINO, "Bold", anchor="lm")
        _led_vista(c, 60.0, yt + 2.2, duty, r=1.1)
    c.text(22.0, 35.6, "HIGH = 5 V, LOW = 0 V. El LED recibe pulsos tan rápidos que el ojo solo percibe el promedio.", 0.5, GRIS_T, "Medium", anchor="lm")
    _caja_aviso(c, 1.0, 36.6, 62.0, 3.9, "Lo que hay que saber",
                ["Solo los pines con ~ hacen PWM en el UNO: 3, 5, 6, 9, 10 y 11. Los demás solo dan HIGH o LOW. Frecuencia: unos 490 Hz (pines 5 y 6: 980 Hz)."], 0.52)
    c.text(c.w_u - 1.0, c.h_u - 0.4, "Los LED son ilustración: el ojo no responde en línea recta, a la mitad ya parece bastante brillante.", 0.46, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P10_pwm.png"))
    print("P10 pwm listo")


def map_diagrama():
    """map(): cambiar un número de una escala a otra."""
    c = Lienzo(64, 45.5)
    c.header("P10 · map(): cambiar de escala", "El mismo punto de la perilla, escrito en dos escalas: la lectura (0 a 1023) y el brillo (0 a 255)")
    x0, x1 = 6.0, 58.0
    ya, yb = 11.0, 19.0
    c.text(1.5, 7.4, "lectura  (analogRead): de 0 a 1023", 0.7, TINTA, "Bold", anchor="lm")
    c.text(1.5, yb + 4.2, "brillo  (analogWrite): de 0 a 255", 0.7, TINTA, "Bold", anchor="lm")
    c.rect(x0, ya - 0.5, x1 - x0, 1.0, fill="#e7e1d2", outline=TINTA, width=0.08)
    c.rect(x0, yb - 0.5, x1 - x0, 1.0, fill="#e7e1d2", outline=TINTA, width=0.08)
    for v in (0, 256, 512, 768, 1023):
        xa = x0 + v / 1023 * (x1 - x0)
        b = _amap(v, 0, 1023, 0, 255)
        xb = x0 + b / 255 * (x1 - x0)
        c.line([(xa, ya + 0.5), (xb, yb - 0.5)], VINO, 0.14, ends=False)
        c.circle(xa, ya, 0.35, fill=VINO)
        c.circle(xb, yb, 0.35, fill=VINO)
        c.text(xa, ya - 1.3, str(v), 0.75, TINTA, "Bold")
        c.text(xb, yb + 1.4, str(b), 0.75, TINTA, "Bold")
    # la llamada y sus cinco partes
    tam = 1.1
    trozos = ["int brillo = map(", "lectura", ", ", "0", ", ", "1023", ", ", "0", ", ", "255", ");"]
    cw = c.text_len("M", tam, "MonoBold")
    total = sum(len(s) for s in trozos) * cw
    xi = 32.0 - total / 2
    c.rect(xi - 2.0, 25.0, total + 4.0, 3.6, fill="#1e1e24", r=0.5)
    c.text(xi, 26.85, "".join(trozos), tam, "#f2f2f2", "MonoBold", anchor="lm")
    pos, acum = [], 0
    for s in trozos:
        pos.append(xi + (acum + len(s) / 2) * cw)
        acum += len(s)
    centros = [pos[1], pos[3], pos[5], pos[7], pos[9]]
    rotulos = [("el número", "que se convierte", 30.6), ("de: mínimo", "de la entrada", 33.6), ("de: máximo", "de la entrada", 30.6),
               ("a: mínimo", "de la salida", 33.6), ("a: máximo", "de la salida", 30.6)]
    for xp, (a, b, yy) in zip(centros, rotulos):
        c.line([(xp, 28.6), (xp, yy - 0.6)], "#d9a83f", 0.12, ends=False)
        c.text(xp, yy, a, 0.5, VINO, "Bold")
        c.text(xp, yy + 0.95, b, 0.42, GRIS_T, "SemiBold")
    # tabla de ejemplos
    cols = [("lectura", 1.5, 7.5), ("map(lectura, 0, 1023, 0, 255)", 9.0, 17.0), ("map(…, 255, 0)  invertido", 26.0, 13.0),
            ("map(…, 20, 200)", 39.0, 11.0), ("solo pasada la mitad", 50.0, 12.5)]
    yh = 37.0
    for (t, xx, w) in cols:
        c.rect(xx, yh, w, 1.5, fill=VINO, outline="#ffffff", width=0.05)
        c.text(xx + w / 2, yh + 0.78, t, 0.5, "#ffffff", "Bold")
    for r, L in enumerate((0, 256, 512, 768, 1023)):
        yy = yh + 1.5 + r * 1.1
        vals = [str(L), str(_amap(L, 0, 1023, 0, 255)), str(_amap(L, 0, 1023, 255, 0)), str(_amap(L, 0, 1023, 20, 200)),
                str(0 if L < 512 else _amap(L, 512, 1023, 0, 255))]
        for (t, xx, w), v in zip(cols, vals):
            c.rect(xx, yy, w, 1.1, fill="#ffffff", outline="#cfc9b8", width=0.05)
            c.text(xx + w / 2, yy + 0.57, v, 0.5, TINTA, "SemiBold")
    c.text(c.w_u - 1.0, c.h_u - 0.4, "map() usa números enteros: recorta los decimales, no redondea (por eso 512 da 127 y no 128).", 0.48, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P10_map.png"))
    print("P10 map listo")


TODOS = {"P01": [p01], "P02": [p02, esquema_p02, cableado_p02], "P03": [p03, cableado_p03], "P04": [p04, cableado_p04],
         "P05": [p05, cableado_p05, esquema_pullup, boton_patas], "P06": [rebote_p06, estados_p06],
         "P07": [zumbadores, frecuencia, p07a, cableado_p07a, p07b, cableado_p07b, for_diagrama],
         "P08": [pir_conoce, pir_senal, p08, cableado_p08, alarma_estados],
         "P09": [perilla_conoce, lectura_adc, p09_paso0, p09, cableado_p09, plotter_ilustracion],
         "P10": [pwm_a_mano, pwm_ciclos, map_diagrama, p10, cableado_p10]}

if __name__ == "__main__":
    pedidos = sys.argv[1:] or list(TODOS)
    for clave in pedidos:
        for f in TODOS[clave]:
            f()
