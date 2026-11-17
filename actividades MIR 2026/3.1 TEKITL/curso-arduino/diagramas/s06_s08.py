"""Diagramas de las sesiones 6 (luz y decisiones), 7 (servo) y 8 (distancia y barrera).

Uso:  python s06_s08.py            (genera todos)
      python s06_s08.py P11 P12    (genera solo los de P11 y P12)
Reutiliza el motor de generar_diagramas.py. Igual que allí, cada circuito se verifica al construirse.

Zonas del protoboard que se repiten en el curso (columnas 1 a 30):
  - Zona analógica A (derecha, columnas 26, 28 y 30): cable negro de la columna 26 al riel de GND, cable de la columna 28 a A0 y
    cable de 5 V a la columna 30. Sobre ella se pone, en cada sesión, el componente que toque (potenciómetro, LDR + 10 kΩ, termistor + 10 kΩ).
  - Zona analógica B (izquierda, columnas 5, 7 y 9): potenciómetro con GND en la columna 5, centro (A1) en la 7 y 5 V en la 9 desde el riel rojo.
"""
import math
import os
import sys

from diagrama import Arduino, Breadboard, Canvas, Circuit, COL, GRIS_T, TINTA, VINO, LED_COL
from esquema import Esquema, Lienzo
import generar_diagramas as G

AQUI = G.AQUI
_leyenda, _lista, _caja_aviso, _flecha, _led_cuerpo, _verificar_grupo, _led_pin9, _rama, _riel = (
    G._leyenda, G._lista, G._caja_aviso, G._flecha, G._led_cuerpo, G._verificar_grupo, G._led_pin9, G._rama, G._riel)
GOLD_BORDE = G.GOLD_BORDE


def cables_derecha(circ, bb, ard, items):
    """Cables que salen de la hilera de abajo de la placa (5V, A0, A1...), rodean la placa por la derecha y entran por la fila j.
    items: [(pin, columna, color, paso)] en el orden en que aparecen los pines de izquierda a derecha en la placa.
    El cable del pin más a la izquierda va por fuera, y su columna debe quedar a la derecha de la de los demás: así no se cruzan entre sí."""
    n = len(items)
    borde = ard.y + ard.H
    for i, (pin, col, color, paso) in enumerate(items):
        px = ard.xy(pin)[0]
        tx = bb.hole(col, "j")[0]
        y_ab = borde + 0.9 + 1.3 * (n - 1 - i)
        x_der = 35.3 + 1.0 * (n - 1 - i)
        y_ar = bb.y + 21.6 + 1.2 * i
        circ.wire(("ard", pin), ("bb", col, "j"), color, step=paso,
                  ruta=[(px, y_ab), (x_der, y_ab), (x_der, y_ar), (tx, y_ar)], badge=(x_der - 3.0, y_ab))


def pie_leyenda(c, ard, n_cables, items):
    _leyenda(c, ard.x + 0.5, ard.y + ard.H + 1.8 + 1.3 * n_cables, items)


def medida_etiqueta(c, lineas, size):
    """Ancho y alto del cuadro que dibuja Canvas.callout (sirve para calcular dónde empieza cada guía antes de dibujarlo)."""
    return max(c.text_len(s, size, "SemiBold") for s in lineas) + 1.2, len(lineas) * size * 1.55 + 0.7


def etiqueta_guias(c, x, y, lineas, guias, size=0.54):
    """Cuadro de texto con una o varias guías rectas. Cada guía es (x_ini, y_ini, x_fin, y_fin): la línea se dibuja primero y el cuadro
    encima, así que basta con que 'ini' quede dentro del cuadro. Se usa cuando la guía de Canvas.callout (que sale del centro del cuadro)
    cruzaría una insignia, un número de columna o un componente."""
    for (x0, y0, x1, y1) in guias:
        c.line([(x0, y0), (x1, y1)], VINO, 0.12, ends=False)
        c.circle(x1, y1, 0.22, fill=VINO)
    return c.callout(x, y, lineas, target=None, size=size)


def borde_circulo(cx, cy, r, x, dentro=0.25):
    """y del borde de arriba de un círculo en la vertical x, más 'dentro' hacia el interior (para que el punto de la guía quede sobre el cuerpo)."""
    return cy - math.sqrt(max(r * r - (x - cx) ** 2, 0.0)) + dentro


# ====================================================================== SESIÓN 6
def _zona_a_ldr(circ, nuevo):
    s = (lambda n: n) if nuevo else (lambda n: None)
    circ.sensor2(28, "ldr", step=s(1), nombre="LDR")                        # patas en f28 (punto medio) y f30 (5 V)
    circ.resistor((28, "h"), (26, "h"), 10000, step=s(2), nombre="RF")      # 10 kΩ del punto medio (col. 28) a la col. 26 (GND)


def _verificar_ldr(circ):
    l_m, l_5 = circ.elems["LDR"]
    r_m, r_g = circ.elems["RF"]
    circ.exigir(("ard", "5V"), l_5, "el 5 V debe llegar a una pata de la fotorresistencia")
    circ.exigir(("ard", "A0"), l_m, "A0 debe llegar a la otra pata de la fotorresistencia")
    circ.exigir(("ard", "A0"), r_m, "A0 debe llegar a la resistencia de 10 kΩ")
    circ.exigir(r_g, ("ard", "GND"), "la resistencia de 10 kΩ debe llegar a GND")
    circ.prohibir(l_5, l_m, "las patas de la fotorresistencia no pueden estar unidas")
    circ.prohibir(("ard", "A0"), ("ard", "5V"), "A0 y 5 V no pueden tocarse")
    circ.prohibir(("ard", "A0"), ("ard", "GND"), "A0 y GND no pueden tocarse")
    circ.prohibir(("ard", "5V"), ("ard", "GND"), "5 V y GND no pueden tocarse")


def p11():
    c = Canvas(38.5, 66.5)
    c.header("P11 · Sensor de luz", "La fotorresistencia y una resistencia de 10 kΩ ocupan el lugar del potenciómetro (vista desde arriba)")
    bb = Breadboard(3.0, 4.6, cols=30)
    ard = Arduino(bb.x + 2.6, bb.y + bb.H + 6.2)
    circ = Circuit(c, ard, bb)
    _led_pin9(circ, nuevo=False)
    circ.wire(("bb", 26, "j"), ("rail", "B", "-", 26), "negro")
    cables_derecha(circ, bb, ard, [("5V", 30, "rojo", None), ("A0", 28, "amarillo", None)])
    _zona_a_ldr(circ, nuevo=True)
    _verificar_grupo(circ, 9, "D9")
    _verificar_ldr(circ)
    circ.draw()
    lx, ly = _led_cuerpo(bb, 22, 23)
    c.callout(bb.x + 1.6, bb.y + 4.2, ["LED del pin 9: sigue", "armado, hoy no se usa"], target=(lx - 1.0, ly - 1.6), size=0.54)
    xl = bb.hole(29, "f")[0]
    c.callout(bb.x + 11.6, bb.y + 4.2, ["LDR (sin polaridad) y resistencia de", "10 kΩ (café · negro · naranja)"], target=(xl, bb.hole(28, "f")[1] - 3.3), size=0.54)
    pie_leyenda(c, ard, 2, [(COL["negro"], "GND  (−, tierra)"), (COL["morado"], "Señal del pin 9 (ya está)"),
                            (COL["amarillo"], "Punto medio del divisor a A0 (ya está)"), (COL["rojo"], "+5 V a la fotorresistencia (ya está)")])
    c.text(c.w_u - 1.2, c.h_u - 1.2, "Los números 1 y 2 son lo único nuevo: los tres cables de la zona de la derecha son los de la Sesión 5.", 0.5, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P11_ldr_serie.png"))
    print("P11 listo")


def cableado_p11():
    E = Esquema(36, 25.8)
    E.titulo("P11 · Sensor de luz", "esquema de conexiones · un divisor de voltaje: la resistencia de arriba cambia con la luz")
    E.placa(1.5, 5.0, 7.5, 17.5, "Arduino\nUNO R3", [("5V", "5V", 8.5), ("A0", "A0", 14.5), ("GND", "GND", 20.5)])
    E.resistencia_v("LDR", 22.0, 8.5, 14.5, marca="luz")
    E.resistencia_v("RF", 22.0, 14.5, 20.5)
    E.union_interna("LDR.b", "RF.a")
    E.puntos.add("LDR.b")
    E.cable("rojo", "5V", "LDR.a")
    E.cable("amarillo", "A0", "LDR.b")
    E.cable("negro", "GND", "RF.b")
    E.nota(9.5, 7.05, "5 V · cable rojo")
    E.nota(9.5, 13.05, "A0 (entrada) · cable amarillo")
    E.nota(9.5, 19.05, "cable negro")
    E.etiqueta(27.0, 9.0, "Fotorresistencia", "LDR · más luz, menos Ω", anchor="mm")
    E.etiqueta(27.0, 17.0, "Resistencia", "10 kΩ", anchor="mm")
    E.nota(16.0, 14.5, "punto medio", anchor="rm")
    E.nota(1.5, 24.6, "Con más luz el LDR deja pasar mejor la corriente: baja su resistencia y sube el voltaje en A0.", color="#8a8a8a")
    E.exigir("5V", "LDR.a", "5 V debe llegar a la fotorresistencia")
    E.exigir("A0", "LDR.b", "A0 debe llegar al punto medio")
    E.exigir("A0", "RF.a", "A0 debe llegar a la resistencia de 10 kΩ")
    E.exigir("RF.b", "GND", "la resistencia de 10 kΩ debe llegar a GND")
    E.prohibir("5V", "GND", "5V y GND no pueden tocarse")
    E.prohibir("A0", "5V", "A0 y 5V no pueden tocarse")
    E.prohibir("A0", "GND", "A0 y GND no pueden tocarse")
    E.dibujar(os.path.join(AQUI, "P11_ldr_serie_cableado.png"))
    print("P11 cableado listo")


def p12():
    c = Canvas(40.5, 69.5)
    c.header("P12 · Lámpara nocturna automática", "A la fotorresistencia de P11 agrega el potenciómetro del umbral en la zona de la izquierda (vista desde arriba)")
    bb = Breadboard(3.0, 4.6, cols=30)
    ard = Arduino(bb.x + 2.6, bb.y + bb.H + 6.2)
    circ = Circuit(c, ard, bb)
    _led_pin9(circ, nuevo=False)
    circ.wire(("bb", 26, "j"), ("rail", "B", "-", 26), "negro")
    _zona_a_ldr(circ, nuevo=False)
    # lo nuevo: potenciómetro del umbral (zona B), con 5 V desde el riel rojo
    circ.potenciometro(5, step=1, nombre="POT")                                     # patas en f5 (GND), f7 (centro) y f9 (5 V)
    circ.wire(("bb", 5, "j"), ("rail", "B", "-", 5), "negro", step=2)
    cables_derecha(circ, bb, ard, [("5V", 30, "rojo", None), ("A0", 28, "amarillo", None), ("A1", 7, "azul", 3)])
    circ.wire(("bb", 30, "i"), ("rail", "B", "+", 29), "rojo", step=4)
    circ.wire(("rail", "B", "+", 9), ("bb", 9, "j"), "rojo", step=5)
    _verificar_grupo(circ, 9, "D9")
    _verificar_ldr(circ)
    a, w, b = circ.elems["POT"]
    circ.exigir(("ard", "GND"), a, "el extremo izquierdo del potenciómetro debe llegar a GND")
    circ.exigir(("ard", "A1"), w, "el centro del potenciómetro debe llegar a A1")
    circ.exigir(("ard", "5V"), b, "el extremo derecho del potenciómetro debe llegar a 5 V")
    circ.prohibir(w, ("ard", "5V"), "el centro no puede estar unido a 5 V")
    circ.prohibir(w, ("ard", "GND"), "el centro no puede estar unido a GND")
    circ.prohibir(a, b, "los extremos del potenciómetro no pueden estar unidos")
    circ.prohibir(("ard", "A1"), ("ard", "A0"), "A1 y A0 no pueden tocarse")
    circ.prohibir(("ard", "A1"), ("ard", "5V"), "A1 y 5 V no pueden tocarse")
    circ.prohibir(("ard", "D9"), ("ard", "A1"), "el pin 9 y A1 no pueden tocarse")
    circ.draw()
    lx, ly = _led_cuerpo(bb, 22, 23)
    c.callout(bb.x + 8.8, bb.row_y["g"] - 0.3, ["LED del pin 9"], target=(lx - 1.4, ly + 1.0), size=0.54)
    c.callout(bb.x + 15.6, bb.y + 4.2, ["LDR y 10 kΩ: ya", "armados en P11"], target=(bb.hole(29, "f")[0], bb.hole(28, "f")[1] - 3.3), size=0.54)
    c.callout(bb.x + 1.2, bb.y + 8.8, ["Potenciómetro del umbral:", "el centro va a A1"], target=(bb.hole(7, "f")[0], bb.hole(7, "f")[1] - 3.6), size=0.54)
    pie_leyenda(c, ard, 3, [(COL["negro"], "GND  (−, tierra)"), (COL["morado"], "Señal del pin 9 (ya está)"),
                            (COL["amarillo"], "LDR a A0 (ya está)"), (COL["azul"], "Centro del potenciómetro a A1 (nuevo)"),
                            (COL["rojo"], "+5 V: a la zona de la derecha y, por el riel rojo, al potenciómetro")])
    c.text(c.w_u - 1.2, c.h_u - 1.2, "Del 1 al 5 es lo nuevo. Los cables pueden cruzarse por encima sin tocarse: solo importa dónde empieza y dónde termina cada uno.", 0.5, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P12_lampara_automatica.png"))
    print("P12 listo")
    for fila in sorted((f for f in circ.table if f[0]), key=lambda t: t[0]):
        print("  ", fila)


def cableado_p12():
    E = Esquema(40, 46.5)
    E.titulo("P12 · Lámpara nocturna automática", "esquema de conexiones · el LDR y la perilla entran por A0 y A1; el LED sale por el pin 9")
    E.placa(1.5, 5.0, 7.5, 40.0, "Arduino\nUNO R3", [("5V", "5V", 8.5), ("A1", "A1", 15.0), ("A0", "A0", 22.5), ("GND", "GND", 33.0), ("D9", "D9", 40.0)])
    E.terminal("TAP5", 20.0, 8.5)
    E.potenciometro("P", 32.0, 8.5, 21.5)
    E.resistencia_v("LDR", 20.0, 16.5, 22.5, marca="luz")
    E.resistencia_v("RF", 20.0, 22.5, 28.5)
    E.union_interna("LDR.b", "RF.a")
    E.puntos.update({"LDR.b", "TAP5"})
    E.cable("rojo", "5V", "TAP5")
    E.cable("rojo", "TAP5", "P.a")
    E.cable("rojo", "TAP5", "LDR.a")
    E.cable("azul", "A1", "P.w")
    E.cable("amarillo", "A0", "LDR.b")
    E.terminal("TAPR", 20.0, 33.0)
    E.terminal("TAPP", 32.0, 33.0)
    E.cable("negro", "RF.b", "TAPR")
    E.cable("negro", "P.b", "TAPP")
    _rama(E, 40.0, 9, "rojo", "LED rojo", "D9", 37.0, 33.0)
    _riel(E, 33.0, ["TAPR", "TAPP", "TAP9"])
    E.nota(9.5, 7.05, "5 V · cable rojo")
    E.nota(9.5, 13.55, "A1 (umbral) · cable azul")
    E.nota(9.5, 21.05, "A0 (luz) · cable amarillo")
    E.nota(9.5, 31.55, "cable negro (riel GND)")
    E.etiqueta(27.0, 18.4, "LDR", None, anchor="mm")
    E.etiqueta(27.0, 25.4, "10 kΩ", None, anchor="mm")
    E.etiqueta(35.5, 15.0, "Perilla", "umbral", anchor="mm")
    E.nota(24.0, 13.6, "centro (cursor)", anchor="mm")
    E.nota(36.4, 36.5, "cable negro", anchor="rm")
    E.nota(23.0, 34.4, "riel GND: la tira azul (−)", anchor="lm")
    E.nota(10.5, 44.6, "El LED se enciende cuando A0 (luz) queda por debajo de A1 (umbral).", color="#8a8a8a")
    E.exigir("5V", "LDR.a", "5 V debe llegar a la fotorresistencia")
    E.exigir("A0", "LDR.b", "A0 debe llegar al punto medio del divisor")
    E.exigir("RF.b", "GND", "la resistencia de 10 kΩ debe llegar a GND")
    E.exigir("5V", "P.a", "5 V debe llegar a un extremo de la perilla")
    E.exigir("A1", "P.w", "A1 debe llegar al centro de la perilla")
    E.exigir("P.b", "GND", "el otro extremo de la perilla debe llegar a GND")
    E.exigir("D9", "R9.a", "el pin 9 debe llegar a la resistencia del LED")
    E.exigir("LED9.k", "GND", "la pata corta del LED debe llegar a GND")
    for a, b in (("5V", "GND"), ("A0", "A1"), ("A0", "5V"), ("A1", "5V"), ("A1", "GND"), ("A0", "GND"), ("D9", "GND"), ("D9", "A0")):
        E.prohibir(a, b, f"{a} y {b} no pueden tocarse")
    E.dibujar(os.path.join(AQUI, "P12_lampara_automatica_cableado.png"))
    print("P12 cableado listo")


def ldr_conoce():
    """La fotorresistencia por fuera y como divisor de voltaje, con valores estimados."""
    c = Lienzo(72, 47)
    c.header("P11 · Conoce tu fotorresistencia (LDR)", "Una resistencia que baja sola cuando le llega luz; con una resistencia fija forma un divisor de voltaje")
    # ---- por fuera
    c.text(11.5, 5.5, "Por fuera", 0.85, TINTA, "Bold")
    cx, cy, r = 11.5, 12.0, 4.3
    for px_ in (cx - 1.6, cx + 1.6):
        c.line([(px_, cy + 2.5), (px_, cy + 9.0)], "#b8b8b8", 0.34, ends=True)
    c.circle(cx, cy, r, fill="#d9b779", outline="#6b4a12", width=0.12)
    ys = [cy - 2.6 + k * 0.95 for k in range(6)]
    for k, yy in enumerate(ys):
        c.line([(cx - 2.8, yy), (cx + 2.8, yy)], "#7a4a10", 0.2, ends=False)
    for k in range(5):
        xx = cx + 2.8 if k % 2 == 0 else cx - 2.8
        c.line([(xx, ys[k]), (xx, ys[k + 1])], "#7a4a10", 0.2, ends=False)
    c.text(cx, cy + 10.4, "2 patas, sin polaridad", 0.55, VINO, "Bold")
    _lista(c, 1.5, 24.6, ["Hoja de datos (LXD5537):", "· 18 a 50 kΩ con 10 lux (poca luz)", "· 2 MΩ o más en total oscuridad",
                          "· responde en unos 20 a 30 ms", "· fórmula entre 10 y 100 lux:", "  R = R(10 lux) × (10 ÷ lux)^0,7"], 0.5, 1.2, GRIS_T)
    # ---- divisor
    c.text(48.0, 5.5, "Como divisor de voltaje (con 10 kΩ fijos)", 0.85, TINTA, "Bold")
    x = 38.0
    c.line([(x, 8.0), (x, 10.0)], "#c8202b", 0.16, ends=False)
    c.text(x + 0.9, 8.2, "5 V", 0.6, "#c8202b", "Bold", anchor="lm")
    _zig(c, x, 10.0, 15.0, marca="luz")
    c.line([(x, 15.0), (x, 16.0)], TINTA, 0.16, ends=False)
    c.circle(x, 16.0, 0.3, fill=TINTA)
    c.line([(x, 16.0), (x - 4.5, 16.0)], "#c99a00", 0.16, ends=False)
    c.text(x - 5.0, 16.0, "A0", 0.7, TINTA, "Bold", anchor="rm")
    c.line([(x, 16.0), (x, 17.0)], TINTA, 0.16, ends=False)
    _zig(c, x, 17.0, 22.0)
    c.line([(x, 22.0), (x, 24.0)], "#1d5fd1", 0.16, ends=False)
    c.text(x + 0.9, 23.6, "GND", 0.6, "#1d5fd1", "Bold", anchor="lm")
    c.text(x + 2.6, 12.5, "LDR", 0.7, TINTA, "Bold", anchor="lm")
    c.text(x + 2.6, 19.5, "10 kΩ", 0.7, TINTA, "Bold", anchor="lm")
    c.text(47.0, 10.0, "Más luz", 0.62, VINO, "Bold", anchor="lm")
    _lista(c, 47.0, 11.5, ["El LDR baja de resistencia,", "A0 recibe más voltaje y", "analogRead da un número más alto."], 0.55, 1.3, TINTA)
    c.text(47.0, 16.8, "Menos luz", 0.62, VINO, "Bold", anchor="lm")
    _lista(c, 47.0, 18.3, ["El LDR sube de resistencia,", "A0 recibe menos voltaje y", "analogRead da un número más bajo."], 0.55, 1.3, TINTA)
    # ---- tabla de valores estimados
    cols = [("Situación", 1.5, 24.0), ("Resistencia del LDR (estimada)", 25.5, 21.0), ("Lectura en A0 con 10 kΩ (estimada)", 46.5, 24.0)]
    filas = [("Oscuridad (tapado)", "2 MΩ o más", "cerca de 5"),
             ("Poca luz (10 lux)", "18 a 50 kΩ", "unos 170 a 365"),
             ("Salón con luz (varios cientos de lux)", "unos 2 a 5 kΩ (extrapolado)", "unos 700 a 880"),
             ("Linterna del celular muy cerca", "1 kΩ o menos (extrapolado)", "más de 900")]
    yt = 33.5
    c.text(1.5, yt - 1.0, "Lo que se espera (estimaciones con la hoja de datos: se miden en la validación V6)", 0.62, VINO, "Bold", anchor="lm")
    for (t, xx, w) in cols:
        c.rect(xx, yt, w, 1.7, fill=VINO, outline="#ffffff", width=0.05)
        c.text(xx + w / 2, yt + 0.88, t, 0.5, "#ffffff", "Bold")
    for r_, fila in enumerate(filas):
        yy = yt + 1.7 + r_ * 1.7
        for (t, xx, w), v in zip(cols, fila):
            c.rect(xx, yy, w, 1.7, fill="#ffffff", outline="#cfc9b8", width=0.05)
            c.text(xx + 0.5, yy + 0.9, v, 0.5, TINTA, "SemiBold" if xx == 1.5 else "Medium", anchor="lm")
    c.text(c.w_u - 1.0, c.h_u - 0.8, "Lectura = 1023 × 10 kΩ ÷ (10 kΩ + R del LDR). Los lux del salón y de la linterna son aproximados: tu sensor puede salir distinto.", 0.48, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P11_ldr_conoce.png"))
    print("P11 conoce listo")


def _zig(c, x, y0, y1, marca=None):
    n = 8
    ya, yb = y0 + 0.7, y1 - 0.7
    seg = (yb - ya) / n
    pts = [(x, y0), (x, ya)]
    for i in range(n):
        pts.append((x + (-0.85 if i % 2 == 0 else 0.85), ya + seg * (i + 0.5)))
    pts += [(x, yb), (x, y1)]
    c.line(pts, TINTA, 0.16, ends=False)
    if marca == "luz":
        ym = (y0 + y1) / 2
        for dy in (-0.9, 0.5):
            a = (x + 3.4, ym + dy - 1.2)
            b = (x + 1.4, ym + dy)
            c.line([a, b], "#d98200", 0.13, ends=False)
            c.poly([b, (b[0] + 0.55, b[1] - 0.2), (b[0] + 0.25, b[1] - 0.6)], fill="#d98200")


def umbral_diagrama():
    """Decisión con umbral: la lámpara enciende cuando la luz queda por debajo del umbral (ilustración)."""
    c = Canvas(60, 34)
    c.header("P12 · Decidir con un umbral", "Si luz < umbral, el LED se enciende. La perilla sube o baja la línea del umbral")
    x0, y0, W, H = 6.0, 6.0, 50.0, 15.0
    c.rect(x0, y0, W, H, fill="#fbfaf6", outline="#cfc9b8", width=0.08)
    esc_y = H / 1023.0

    def yv(v):
        return y0 + H - v * esc_y
    for v in (0, 256, 512, 768, 1023):
        c.line([(x0, yv(v)), (x0 + W, yv(v))], "#ebe7da", 0.05, ends=False)
        c.text(x0 - 0.4, yv(v), str(v), 0.45, GRIS_T, "SemiBold", anchor="rm")
    umbral = 480
    c.line([(x0, yv(umbral)), (x0 + W, yv(umbral))], "#c8202b", 0.16, ends=False)
    c.text(x0 + W - 0.3, yv(umbral) - 0.7, "umbral (la perilla)", 0.55, "#c8202b", "Bold", anchor="rm")
    pts = [(0, 800), (5, 780), (10, 700), (14, 420), (18, 150), (24, 120), (30, 330), (35, 700), (40, 780), (50, 790)]
    base = []
    for (ta, va), (tb, vb) in zip(pts, pts[1:]):
        for k in range(10):
            u = k / 10
            base.append((ta + (tb - ta) * u, va + (vb - va) * u))
    base.append(pts[-1])
    curva = [(x0 + t, yv(v)) for t, v in base]
    c.line(curva, "#2a6fdb", 0.2, ends=False)
    c.text(x0 + 3.0, yv(820) - 0.6, "luz (A0)", 0.55, "#2a6fdb", "Bold", anchor="lm")
    # cruces con el umbral
    def cruce(t0, t1):
        for (ta, va), (tb, vb) in zip(base, base[1:]):
            if ta >= t0 and tb <= t1 and (va - umbral) * (vb - umbral) <= 0:
                return ta + (tb - ta) * (umbral - va) / (vb - va)
    t1 = cruce(10, 18)
    t2 = cruce(30, 36)
    yb = y0 + H + 3.0
    c.text(x0 - 0.4, yb + 0.9, "LED", 0.6, TINTA, "Bold", anchor="rm")
    c.rect(x0, yb, W, 1.8, fill="#ece8dc", outline="#cfc9b8", width=0.06)
    c.rect(x0 + t1, yb, t2 - t1, 1.8, fill="#f2b705", outline="#8a6a00", width=0.06)
    c.text(x0 + (t1 + t2) / 2, yb + 0.92, "encendido", 0.6, TINTA, "Bold")
    c.text(x0 + t1 / 2, yb + 0.92, "apagado", 0.55, GRIS_T, "SemiBold")
    c.text(x0 + (t2 + W) / 2, yb + 0.92, "apagado", 0.55, GRIS_T, "SemiBold")
    for tt in (t1, t2):
        c.line([(x0 + tt, yv(umbral)), (x0 + tt, yb)], "#8a8a8a", 0.08, ends=False)
    c.text(x0 + 12.0, y0 + H + 1.4, "se oscurece", 0.5, GRIS_T, "SemiBold")
    c.text(x0 + 33.0, y0 + H + 1.4, "amanece", 0.5, GRIS_T, "SemiBold")
    c.text(30.0, yb + 3.6, "Un umbral más ALTO hace que la lámpara encienda antes (con más luz); uno más BAJO, que espere a que esté más oscuro.", 0.55, VINO, "Bold")
    c.text(30.0, yb + 4.8, "En el programa: si luz < umbral, enciende; si no, apaga.", 0.55, TINTA, "Medium")
    c.text(c.w_u - 1.0, c.h_u - 0.5, "Ilustración con datos inventados.", 0.48, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P12_umbral.png"))
    print("P12 umbral listo")


def retro_diagrama():
    """Retroalimentación: el LED ilumina al LDR y el sistema parpadea (ilustración)."""
    c = Canvas(62, 34)
    c.header("P12 · Retroalimentación: cuando el LED ilumina a su propio sensor", "Por eso el LED y el LDR se separan, o se le pone un tubito de cartón al LDR")
    cajas = [(3.0, "Oscuro:\nluz < umbral", "#e7e9ef"), (17.0, "El LED\nenciende", "#fff3bf"), (31.0, "La luz del LED\nllega al LDR", "#ffe4c2"), (45.0, "luz ≥ umbral:\nel LED apaga", "#e7e9ef")]
    y = 6.0
    for x, txt, col in cajas:
        c.rect(x, y, 12.0, 5.0, fill=col, outline=TINTA, width=0.1, r=0.5)
        for i, s in enumerate(txt.split("\n")):
            c.text(x + 6.0, y + 1.9 + i * 1.3, s, 0.6, TINTA, "Bold")
    for xa in (15.0, 29.0, 43.0):
        _flecha(c, (xa, y + 2.5), (xa + 2.0, y + 2.5), VINO, 0.16, 0.7)
    c.line([(51.0, y + 5.0), (51.0, y + 8.0), (9.0, y + 8.0), (9.0, y + 5.0)], VINO, 0.16, ends=False)
    _flecha(c, (9.0, y + 6.2), (9.0, y + 5.0), VINO, 0.16, 0.7)
    c.text(30.0, y + 9.2, "…y al apagarse, la luz baja otra vez y todo vuelve a empezar", 0.58, VINO, "Bold")
    # señal resultante
    x0, esc = 6.0, 0.9
    ya, yb = 21.0, 24.0
    c.text(1.5, ya + 1.5, "LED", 0.6, TINTA, "Bold", anchor="lm")
    pts = [(x0, yb)]
    t = 0.0
    nivel = "bajo"
    while t < 52:
        pts += [(x0 + t * esc, yb), (x0 + t * esc, ya)] if nivel == "bajo" else [(x0 + t * esc, ya), (x0 + t * esc, yb)]
        nivel = "alto" if nivel == "bajo" else "bajo"
        t += 3.2
    pts.append((x0 + 52 * esc, ya if nivel == "alto" else yb))
    c.line(pts, VINO, 0.2, ends=False)
    c.text(x0 + 26.0, ya - 1.0, "el LED parpadea sin parar aunque nadie cambie la luz del cuarto", 0.55, "#b00020", "Bold")
    _caja_aviso(c, 1.5, 27.0, 59.0, 5.4, "Cómo arreglarlo",
                ["Separa el LED del LDR, o tápale al LDR el lado del LED con un tubito de cartón o cinta negra. Los sistemas reales (una lámpara de calle)",
                 "tienen el sensor mirando al cielo y la lámpara hacia el suelo, por la misma razón."], 0.52)
    c.text(c.w_u - 1.0, c.h_u - 0.4, "Ilustración con datos inventados.", 0.48, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P12_retroalimentacion.png"))
    print("P12 retroalimentación listo")


# ====================================================================== SESIÓN 7
def dibujar_servo(c, x, y):
    """Servo SG90 visto desde arriba. (x, y) = centro del conector de 3 agujeros (café, rojo, naranja), a la izquierda; el cuerpo y el brazo van a la derecha."""
    xb, w, h = x + 4.2, 8.8, 4.6
    cables = (("#7b4a12", -1.0), ("#d62828", 0.0), ("#f77f00", 1.0))
    for col, dy in cables:
        c.line([(x + 0.8, y + dy), (xb, y + dy * 0.5)], col, 0.2, ends=False)
    c.rect(x - 0.9, y - 1.7, 1.8, 3.4, fill="#1e1e1e", r=0.2)                     # conector hembra
    for col, dy in cables:
        c.circle(x, y + dy, 0.28, fill="#5a5a5a")
    c.rect(xb - 1.1, y - 0.7, 1.2, 1.4, fill="#2c7be5", outline="#14407f", width=0.06)    # orejas
    c.rect(xb + w - 0.1, y - 0.7, 1.2, 1.4, fill="#2c7be5", outline="#14407f", width=0.06)
    c.rect(xb, y - h / 2, w, h, fill="#2c7be5", outline="#14407f", width=0.1, r=0.3)
    c.rect(xb + 0.6, y - h / 2 + 0.6, w - 1.2, 0.7, fill="#7fb2f0", r=0.2)
    xs = xb + w - 2.0
    c.rect(xs - 0.2, y - 0.7, 8.0, 1.4, fill="#f2f2f2", outline="#9a9a9a", width=0.06, r=0.7)   # brazo (horn)
    c.circle(xs, y, 1.0, fill="#f2f2f2", outline="#9a9a9a", width=0.08)
    c.circle(xs, y, 0.3, fill="#7a7a7a")
    c.text(xb + w / 2, y + h / 2 + 1.3, "Servo SG90", 0.55, TINTA, "Bold")


def _servo_en_circuito(circ, x, y):
    """Registra el servo como módulo con sus tres agujeros (de arriba abajo: GND, 5V, señal) y lo dibuja."""
    circ.modulo("SERVO", {"GND": (x, y - 1.0), "5V": (x, y), "SIG": (x, y + 1.0)})
    circ.dibujo(lambda c: dibujar_servo(c, x, y))


def _base_s7(circ, bb, ard, nuevo, extra_ruta=True):
    """Rieles: GND de la placa al riel azul y 5 V al riel rojo (por la izquierda de la placa); y el servo con sus tres cables macho-macho.
    Pasos: 1 GND, 2 servo GND, 3 servo señal al pin 9, 4 5 V al riel, 5 servo 5 V al riel (el 5 V se conecta al final)."""
    s = (lambda n: n) if nuevo else (lambda n: None)
    borde = ard.y + ard.H
    x5 = ard.xy("5V")[0]
    circ.wire(("ard", "GND"), ("rail", "B", "-", 13), "negro", via=0.45, step=s(1))
    sx, sy = 40.0, bb.y + 29.4
    _servo_en_circuito(circ, sx, sy)
    circ.wire(("mod", "SERVO", "GND"), ("rail", "B", "-", 29), "negro", step=s(2),
              ruta=[(38.5, sy - 1.0), (38.5, bb.y + 21.6), (bb.rail_hole("B", "-", 29)[0], bb.y + 21.6)], badge=(38.5, sy - 3.5))
    circ.wire(("mod", "SERVO", "SIG"), ("ard", "D9"), "morado", step=s(3),
              ruta=[(36.5, sy + 1.0), (36.5, bb.y + 24.9), (ard.xy("D9")[0], bb.y + 24.9)], badge=(30.0, bb.y + 24.9))
    # el 5 V entra al riel rojo por su extremo izquierdo (columna 2)
    circ.wire(("ard", "5V"), ("rail", "B", "+", 2), "rojo", step=s(4),
              ruta=[(x5, borde + 2.0), (1.8, borde + 2.0), (1.8, bb.y + 21.4), (bb.rail_hole("B", "+", 2)[0], bb.y + 21.4)], badge=(10.0, borde + 2.0))
    circ.wire(("mod", "SERVO", "5V"), ("rail", "B", "+", 27), "rojo", step=s(5),
              ruta=[(37.5, sy), (37.5, bb.y + 22.8), (bb.rail_hole("B", "+", 27)[0], bb.y + 22.8)], badge=(37.5, sy - 3.0))


def _verificar_servo(circ):
    circ.exigir(("ard", "D9"), ("mod", "SERVO", "SIG"), "el pin 9 debe llegar a la señal del servo")
    circ.exigir(("ard", "5V"), ("mod", "SERVO", "5V"), "5 V debe llegar al cable rojo del servo")
    circ.exigir(("ard", "GND"), ("mod", "SERVO", "GND"), "GND debe llegar al cable café del servo")
    circ.prohibir(("mod", "SERVO", "5V"), ("mod", "SERVO", "GND"), "5 V y GND del servo no pueden tocarse")
    circ.prohibir(("ard", "D9"), ("ard", "5V"), "el pin 9 y 5 V no pueden tocarse")
    circ.prohibir(("ard", "D9"), ("ard", "GND"), "el pin 9 y GND no pueden tocarse")
    circ.prohibir(("ard", "5V"), ("ard", "GND"), "5 V y GND no pueden tocarse")


def p13():
    c = Canvas(61, 64.5)
    c.header("P13 · Servo: posición y barrido", "El protoboard solo reparte 5 V y GND; el servo se conecta con tres cables macho-macho (vista desde arriba)")
    bb = Breadboard(3.0, 4.6, cols=30)
    ard = Arduino(bb.x + 2.6, bb.y + bb.H + 6.2)
    circ = Circuit(c, ard, bb)
    _base_s7(circ, bb, ard, nuevo=True)
    _verificar_servo(circ)
    circ.draw()
    c.callout(bb.x + 2.4, bb.y + 4.4, ["Riel rojo (+) = 5 V", "Riel azul (−) = GND"], target=(bb.rail_hole("B", "+", 2)[0] + 3.0, bb.rail_hole("B", "+", 2)[1] - 0.2), size=0.6)
    c.callout(40.4, 41.5, ["Los cables del servo:", "café = GND", "rojo = 5 V", "naranja = señal"], size=0.54)
    pie_leyenda(c, ard, 2, [(COL["negro"], "GND  (−, tierra)"), (COL["rojo"], "+5 V (al riel rojo y al servo)"), (COL["morado"], "Señal del servo: pin 9")])
    c.text(c.w_u - 1.2, c.h_u - 1.2, "Los números del 1 al 5 son el orden de armado: el 5 V se conecta al final.", 0.5, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P13_servo_barrido.png"))
    print("P13 listo")
    for fila in sorted((f for f in circ.table if f[0]), key=lambda t: t[0]):
        print("  ", fila)


def cableado_p13():
    E = Esquema(36, 25.5)
    E.titulo("P13 · Servo: posición y barrido", "esquema de conexiones · tres cables: señal, 5 V y GND")
    E.placa(1.5, 5.0, 7.5, 17.5, "Arduino\nUNO R3", [("D9", "D9", 8.5), ("5V", "5V", 14.5), ("GND", "GND", 20.5)])
    E.bloque("SV", 21.0, 6.0, 10.0, 16.0, "Servo", "SG90",
             terminales=[("sig", "izq", 2.5, "SEÑAL"), ("vcc", "izq", 8.5, "5 V"), ("gnd", "izq", 14.5, "GND")])
    E.cable("morado", "D9", "SV.sig")
    E.cable("rojo", "5V", "SV.vcc")
    E.cable("negro", "GND", "SV.gnd")
    E.nota(9.5, 7.05, "pin 9 (salida) · cable morado")
    E.nota(9.5, 13.05, "5 V · cable rojo")
    E.nota(9.5, 19.05, "GND · cable negro")
    E.nota(26.0, 24.2, "cable naranja · cable rojo · cable café del servo", anchor="mm")
    E.exigir("D9", "SV.sig", "el pin 9 debe llegar a la señal del servo")
    E.exigir("5V", "SV.vcc", "5 V debe llegar al servo")
    E.exigir("GND", "SV.gnd", "GND debe llegar al servo")
    for a, b in (("D9", "5V"), ("D9", "GND"), ("5V", "GND")):
        E.prohibir(a, b, f"{a} y {b} no pueden tocarse")
    E.dibujar(os.path.join(AQUI, "P13_servo_barrido_cableado.png"))
    print("P13 cableado listo")


def _zona_a_pot_s7(circ, bb, ard, nuevo):
    """Potenciómetro en la zona analógica A, con el 5 V tomado del riel rojo."""
    s = (lambda n: n) if nuevo else (lambda n: None)
    circ.potenciometro(26, step=s(1))
    circ.wire(("bb", 26, "j"), ("rail", "B", "-", 26), "negro", step=s(2))
    circ.wire(("rail", "B", "+", 29), ("bb", 30, "j"), "rojo", step=s(3))
    x_a0 = ard.xy("A0")[0]
    xj28 = bb.hole(28, "j")[0]
    borde = ard.y + ard.H
    circ.wire(("ard", "A0"), ("bb", 28, "j"), "amarillo", step=s(4),
              ruta=[(x_a0, borde + 0.9), (35.3, borde + 0.9), (35.3, bb.y + 23.7), (xj28, bb.y + 23.7)], badge=(32.0, borde + 0.9))


def p14():
    c = Canvas(61, 65.5)
    c.header("P14 · Servo controlado con la perilla", "Sobre P13, el potenciómetro en la zona de la derecha (centro a A0) y su 5 V desde el riel rojo (vista desde arriba)")
    bb = Breadboard(3.0, 4.6, cols=30)
    ard = Arduino(bb.x + 2.6, bb.y + bb.H + 6.2)
    circ = Circuit(c, ard, bb)
    _base_s7(circ, bb, ard, nuevo=False)
    _zona_a_pot_s7(circ, bb, ard, nuevo=True)
    _verificar_servo(circ)
    a, w, b = circ.elems["POT"]
    circ.exigir(("ard", "GND"), a, "el extremo izquierdo del potenciómetro debe llegar a GND")
    circ.exigir(("ard", "A0"), w, "el centro del potenciómetro debe llegar a A0")
    circ.exigir(("ard", "5V"), b, "el extremo derecho del potenciómetro debe llegar a 5 V")
    circ.prohibir(w, ("ard", "5V"), "el centro no puede estar unido a 5 V")
    circ.prohibir(w, ("ard", "GND"), "el centro no puede estar unido a GND")
    circ.prohibir(a, b, "los extremos del potenciómetro no pueden estar unidos")
    circ.prohibir(("ard", "A0"), ("ard", "D9"), "A0 y el pin 9 no pueden tocarse")
    circ.draw()
    xp = bb.hole(28, "f")[0]
    c.callout(bb.x + 2.4, bb.y + 4.4, ["El servo y los rieles ya están", "armados (P13)"], target=(bb.rail_hole("B", "+", 2)[0] + 3.0, bb.rail_hole("B", "+", 2)[1] - 0.2), size=0.54)
    c.callout(bb.x + 16.0, bb.y + 4.2, ["Potenciómetro: el centro va a A0"], target=(xp - 1.4, bb.hole(28, "f")[1] - 3.6), size=0.54)
    pie_leyenda(c, ard, 2, [(COL["negro"], "GND  (−, tierra)"), (COL["rojo"], "+5 V (riel rojo, servo y potenciómetro)"),
                            (COL["morado"], "Señal del servo: pin 9 (ya está)"), (COL["amarillo"], "Centro del potenciómetro a A0 (nuevo)")])
    c.text(c.w_u - 1.2, c.h_u - 1.2, "Del 1 al 4 es lo nuevo. Los cables pueden cruzarse por encima sin tocarse.", 0.5, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P14_servo_perilla.png"))
    print("P14 listo")


def cableado_p14():
    E = Esquema(38, 33.5)
    E.titulo("P14 · Servo controlado con la perilla", "esquema de conexiones · la perilla entra por A0 y el servo se mueve por el pin 9")
    E.placa(1.5, 5.0, 7.5, 26.5, "Arduino\nUNO R3", [("D9", "D9", 8.5), ("5V", "5V", 12.5), ("A0", "A0", 23.5), ("GND", "GND", 29.5)])
    E.bloque("SV", 24.0, 7.0, 9.0, 9.0, "Servo", "SG90",
             terminales=[("sig", "izq", 1.5, "SEÑAL"), ("vcc", "izq", 5.5, "5 V"), ("gnd", "izq", 7.5, "GND")])
    E.terminal("TAP5", 19.0, 12.5)
    E.potenciometro("P", 31.0, 18.5, 28.5)
    E.terminal("TAPS", 22.0, 29.5)
    E.terminal("TAPP", 31.0, 29.5)
    E.puntos.update({"TAP5"})
    E.cable("morado", "D9", "SV.sig")
    E.cable("rojo", "5V", "TAP5")
    E.cable("rojo", "TAP5", "SV.vcc")
    E.cable("rojo", "TAP5", "P.a", via=[(19.0, 18.5)])
    E.cable("amarillo", "A0", "P.w")
    E.cable("negro", "SV.gnd", "TAPS", via=[(22.0, 14.5)])
    E.cable("negro", "P.b", "TAPP")
    _riel(E, 29.5, ["TAPS", "TAPP"])
    E.nota(9.5, 7.05, "pin 9 · cable morado")
    E.nota(9.5, 11.05, "5 V · cable rojo")
    E.nota(9.5, 22.05, "A0 (entrada) · cable amarillo")
    E.nota(9.5, 28.05, "cable negro")
    E.etiqueta(35.0, 22.0, "Perilla", None, anchor="lm")
    E.nota(26.0, 25.0, "centro", anchor="mm")
    E.nota(25.0, 31.0, "riel GND: la tira azul (−)", anchor="lm")
    E.nota(1.5, 32.6, "El ángulo del servo sigue a la perilla: 0 → 0 grados y 1023 → 180 grados (map).", color="#8a8a8a")
    E.exigir("D9", "SV.sig", "el pin 9 debe llegar al servo")
    E.exigir("5V", "SV.vcc", "5 V debe llegar al servo")
    E.exigir("5V", "P.a", "5 V debe llegar a un extremo de la perilla")
    E.exigir("A0", "P.w", "A0 debe llegar al centro de la perilla")
    E.exigir("SV.gnd", "GND", "el servo debe llegar a GND")
    E.exigir("P.b", "GND", "la perilla debe llegar a GND")
    for a, b in (("D9", "5V"), ("D9", "GND"), ("5V", "GND"), ("A0", "5V"), ("A0", "GND"), ("A0", "D9")):
        E.prohibir(a, b, f"{a} y {b} no pueden tocarse")
    E.dibujar(os.path.join(AQUI, "P14_servo_perilla_cableado.png"))
    print("P14 cableado listo")


def servo_conoce():
    """El servo: partes, cables y cómo el ancho del pulso decide el ángulo."""
    c = Lienzo(66, 40)
    c.header("P13 · Conoce tu servo SG90", "Un motor que va al ÁNGULO que le pides: se le habla con pulsos y el ancho del pulso decide el ángulo")
    dibujar_servo(c, 6.0, 12.0)
    c.callout(1.5, 5.2, ["Conector hembra:", "café · rojo · naranja"], target=(6.0, 11.2), size=0.5)
    c.callout(14.0, 5.2, ["Brazo (horn): ahí se pega", "la bandera o la barrera"], target=(20.5, 11.3), size=0.5)
    c.text(14.0, 18.0, "Café = GND (tierra)", 0.55, "#7b4a12", "Bold", anchor="lm")
    c.text(14.0, 19.3, "Rojo = 5 V (alimentación)", 0.55, "#d62828", "Bold", anchor="lm")
    c.text(14.0, 20.6, "Naranja = señal (pin 9)", 0.55, "#c4690a", "Bold", anchor="lm")
    _lista(c, 1.5, 23.2, ["Hoja de datos del kit (SG90):", "· gira unos 180°, alimentación de 4,8 V (≈ 5 V)", "· velocidad 0,1 s por cada 60°",
                          "· par de 1,8 kgf·cm · 9 g · se pueden usar los 3 brazos", "· pulsos: ~1 ms a un extremo, 1,5 ms al centro, ~2 ms al otro"], 0.5, 1.2, GRIS_T)
    # pulsos
    x0, esc = 30.0, 1.0
    filas = [("≈ 1 ms", 1.0, "un extremo", 0.0), ("1,5 ms", 1.5, "el centro", 90.0), ("≈ 2 ms", 2.0, "el otro extremo", 180.0)]
    c.text(48.0, 5.5, "El ancho del pulso decide el ángulo", 0.8, TINTA, "Bold")
    for i, (txt, ms, donde, ang) in enumerate(filas):
        yt = 7.5 + i * 8.0
        ya, yb = yt + 1.0, yt + 4.0
        c.line([(x0, ya), (x0 + 20, ya)], "#e2ddd0", 0.06, ends=False)
        c.line([(x0, yb), (x0 + 20, yb)], "#e2ddd0", 0.06, ends=False)
        pts = [(x0, yb)]
        for k in range(2):
            xa = x0 + 0.5 + k * 10.0
            pts += [(xa, yb), (xa, ya), (xa + ms * 3.2, ya), (xa + ms * 3.2, yb)]
        pts.append((x0 + 20, yb))
        c.line(pts, VINO, 0.22, ends=False)
        c.text(x0 + 0.5 + ms * 1.6, ya - 0.7, txt, 0.55, VINO, "Bold")
        c.text(x0 - 0.5, ya, "HIGH", 0.4, GRIS_T, "SemiBold", anchor="rm")
        c.text(x0 - 0.5, yb, "LOW", 0.4, GRIS_T, "SemiBold", anchor="rm")
        # dial
        dx, dy = 57.0, yt + 2.8
        c.circle(dx, dy, 2.3, fill="#f4f1e8", outline="#9a9a9a", width=0.1)
        a = math.radians(180.0 + ang)
        c.line([(dx, dy), (dx + 2.0 * math.cos(a), dy + 2.0 * math.sin(a))], VINO, 0.25, ends=True)
        c.text(dx + 3.2, dy, donde, 0.52, TINTA, "SemiBold", anchor="lm")
    c.text(48.0, 31.8, "Cada pulso se repite unas 50 veces por segundo (cada 20 ms): la librería Servo se encarga.", 0.52, GRIS_T, "Medium")
    _caja_aviso(c, 1.5, 33.3, 63.0, 5.1, "Servo frente a motor de corriente continua",
                ["El servo va a un ÁNGULO (se queda ahí). El motor de corriente continua da vueltas con una VELOCIDAD y no sabe dónde está (Sesión 9)."], 0.55)
    c.save(os.path.join(AQUI, "P13_servo_conoce.png"))
    print("P13 conoce listo")


def barrido_diagrama():
    """El barrido de P13: ángulo en el tiempo, con el cálculo de la duración."""
    c = Canvas(60, 30)
    c.header("P13 · El barrido, paso a paso", "for repite: el servo sube un grado cada 15 ms y luego baja otro tanto")
    x0, y0, W, H = 8.0, 6.0, 48.0, 13.0
    c.rect(x0, y0, W, H, fill="#fbfaf6", outline="#cfc9b8", width=0.08)
    for ang in (0, 90, 180):
        yy = y0 + H - ang / 180 * (H - 1) - 0.5
        c.line([(x0, yy), (x0 + W, yy)], "#ebe7da", 0.05, ends=False)
        c.text(x0 - 0.4, yy, f"{ang}°", 0.5, GRIS_T, "SemiBold", anchor="rm")
    pts = []
    t = 0.0
    paso = W / 4.0
    for k in range(5):
        pts.append((x0 + k * paso, y0 + H - 0.5 - (0 if k % 2 == 0 else (H - 1))))
    c.line(pts, VINO, 0.24, ends=False)
    for k in range(4):
        c.text(x0 + (k + 0.5) * paso, y0 + H + 1.2, "sube 2,7 s" if k % 2 == 0 else "baja 2,7 s", 0.55, TINTA, "SemiBold")
    c.text(30.0, y0 + H + 3.0, "Cada vuelta del for mueve el servo 1 grado y espera 15 ms:   180 grados × 15 ms = 2 700 ms = 2,7 segundos.", 0.58, VINO, "Bold")
    c.text(30.0, y0 + H + 4.3, "Si el delay vale menos, el servo va más rápido; si vale 0, el servo no alcanza a llegar y solo «tiembla».", 0.55, TINTA, "Medium")
    c.text(c.w_u - 1.0, c.h_u - 0.5, "Ilustración; el servo real tarda unos 0,3 s en recorrer 180° a su máxima velocidad (0,1 s por cada 60°).", 0.48, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P13_barrido.png"))
    print("P13 barrido listo")


# ====================================================================== SESIÓN 8
# Se vuelve a armar sobre los rieles y el servo de la Sesión 7 (el potenciómetro se retira).
# El sensor HC-SR04 se enchufa en la fila a, columnas 20 a 23, mirando hacia afuera; visto desde arriba, sus patas quedan (de izquierda a derecha):
# GND, ECHO, TRIG, VCC (al revés de como se leen sus letras mirándolo de frente).
COL_SONAR = 20


def dibujar_sonar(c, bb, col, step=None):
    x0, ya = bb.hole(col, "a")
    x3, _ = bb.hole(col + 3, "a")
    xc = (x0 + x3) / 2
    for k, nombre in enumerate(("GND", "ECHO", "TRIG", "VCC")):
        xx, _ = bb.hole(col + k, "a")
        c.rect(xx - 0.15, ya - 1.0, 0.3, 1.3, fill="#c9a227")
        c.text(xx, ya + 0.62, nombre, 0.34, TINTA, "Bold")
    c.rect(xc - 8.85, ya - 1.6, 17.7, 0.75, fill="#1b5c8a", outline="#0f3b5c", width=0.06)               # la placa, vista de canto
    for sx, letra in ((-4.45, "T"), (4.45, "R")):
        c.rect(xc + sx - 3.15, ya - 6.6, 6.3, 5.0, fill="#c9ced4", outline="#6b7178", width=0.08, r=0.7)  # los dos «ojos»
        c.circle(xc + sx, ya - 4.1, 1.9, fill="#8e969e", outline="#5a6068", width=0.06)
        c.text(xc + sx, ya - 4.1, letra, 0.6, "#ffffff", "Bold")
    if step:
        c.badge(xc - 10.2, ya - 1.2, step)


def _sonar(circ, bb, ard, nuevo):
    """HC-SR04 y sus 4 cables macho-macho: 1 sensor, 2 GND, 3 ECHO al pin 7, 4 TRIG al pin 6, 5 VCC (el 5 V al final)."""
    s = (lambda n: n) if nuevo else (lambda n: None)
    col = COL_SONAR
    for k in range(4):
        circ._occupy(("bb", col + k, "a"), "SONAR")
    circ.elems["SONAR"] = [("bb", col + k, "a") for k in range(4)]
    circ.dibujo(lambda c: dibujar_sonar(c, bb, col, s(1)))
    circ.wire(("bb", col, "e"), ("rail", "B", "-", col), "negro", step=s(2))
    xe, ye = bb.hole(col + 1, "e")
    xt, yt = bb.hole(col + 2, "e")
    circ.wire(("bb", col + 1, "e"), ("ard", "D7"), "gris", step=s(3), ruta=[(xe, bb.y + 23.4), (ard.xy("D7")[0], bb.y + 23.4)], badge=(xe, bb.y + 16.5))
    circ.wire(("bb", col + 2, "e"), ("ard", "D6"), "cafe", step=s(4), ruta=[(xt, bb.y + 22.4), (ard.xy("D6")[0], bb.y + 22.4)], badge=(xt, bb.y + 17.8))
    circ.wire(("bb", col + 3, "e"), ("rail", "B", "+", col + 3), "rojo", step=s(5))


def _verificar_sonar(circ):
    gnd, echo, trig, vcc = circ.elems["SONAR"]
    circ.exigir(("ard", "GND"), gnd, "la pata GND del sensor debe llegar a GND")
    circ.exigir(("ard", "D7"), echo, "el pin 7 debe llegar a la pata ECHO")
    circ.exigir(("ard", "D6"), trig, "el pin 6 debe llegar a la pata TRIG")
    circ.exigir(("ard", "5V"), vcc, "5 V debe llegar a la pata VCC")
    circ.prohibir(vcc, gnd, "VCC y GND del sensor no pueden tocarse")
    circ.prohibir(echo, trig, "ECHO y TRIG no pueden tocarse")
    circ.prohibir(echo, ("ard", "GND"), "ECHO no puede estar unido a GND")
    circ.prohibir(trig, ("ard", "5V"), "TRIG no puede estar unido a 5 V")


def _lista_s8_base(circ, bb, ard):
    """Lo de la Sesión 7 que se queda: rieles y servo (sin números)."""
    _base_s7(circ, bb, ard, nuevo=False)


def p15():
    c = Canvas(61, 71)
    c.header("P15 · Medidor de distancia", "Sobre los rieles y el servo de la Sesión 7, el sensor HC-SR04 se enchufa arriba y mira hacia afuera (vista desde arriba)")
    bb = Breadboard(3.0, 10.8, cols=30)
    ard = Arduino(bb.x + 2.6, bb.y + bb.H + 6.2)
    circ = Circuit(c, ard, bb)
    _lista_s8_base(circ, bb, ard)
    _sonar(circ, bb, ard, nuevo=True)
    _verificar_servo(circ)
    _verificar_sonar(circ)
    circ.prohibir(("ard", "D7"), ("ard", "D9"), "los pines 7 y 9 no pueden tocarse")
    circ.draw()
    c.callout(bb.x + 1.6, bb.y + 3.6, ["HC-SR04 enchufado en la fila a: de izquierda", "a derecha, sus patas son GND · ECHO · TRIG · VCC", "(vistas desde arriba, con el sensor mirando hacia afuera)"],
              target=(bb.hole(COL_SONAR, "a")[0] - 0.6, bb.hole(COL_SONAR, "a")[1] - 0.6), size=0.5)
    c.callout(40.4, bb.y + 36.9, ["El servo y los rieles siguen", "como en la Sesión 7:", "hoy el servo no se usa"], size=0.54)
    pie_leyenda(c, ard, 2, [(COL["negro"], "GND  (−, tierra)"), (COL["rojo"], "+5 V (rieles, servo y sensor)"), (COL["morado"], "Señal del servo (ya está)"),
                            (COL["gris"], "ECHO al pin 7 (nuevo)"), (COL["cafe"], "TRIG al pin 6 (nuevo)")])
    c.text(c.w_u - 1.2, c.h_u - 1.2, "Los números del 1 al 5 son lo nuevo. Lee las letras de TU sensor: GND, ECHO, TRIG y VCC se ven al revés mirándolo por delante.", 0.5, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P15_distancia.png"))
    print("P15 listo")
    for fila in sorted((f for f in circ.table if f[0]), key=lambda t: t[0]):
        print("  ", fila)


def cableado_p15():
    E = Esquema(36, 27.0)
    E.titulo("P15 · Medidor de distancia", "esquema de conexiones · TRIG manda el chirrido y ECHO dura lo que tarda en volver")
    E.placa(1.5, 5.0, 7.5, 19.5, "Arduino\nUNO R3", [("5V", "5V", 8.5), ("D6", "D6", 12.5), ("D7", "D7", 16.5), ("GND", "GND", 20.5)])
    E.bloque("SR", 20.0, 6.0, 10.0, 17.0, "HC-SR04", "ultrasonido",
             terminales=[("vcc", "izq", 2.5, "VCC"), ("trig", "izq", 6.5, "TRIG"), ("echo", "izq", 10.5, "ECHO"), ("gnd", "izq", 14.5, "GND")])
    E.cable("rojo", "5V", "SR.vcc")
    E.cable("cafe", "D6", "SR.trig")
    E.cable("gris", "D7", "SR.echo")
    E.cable("negro", "GND", "SR.gnd")
    E.nota(9.5, 7.05, "5 V · cable rojo")
    E.nota(9.5, 11.05, "pin 6 (salida) · cable café")
    E.nota(9.5, 15.05, "pin 7 (entrada) · cable gris")
    E.nota(9.5, 19.05, "cable negro")
    E.nota(1.5, 26.0, "La placa manda un pulso de 10 µs por TRIG y mide cuánto dura ECHO: ese tiempo es la distancia (ida y vuelta).", color="#8a8a8a")
    E.exigir("5V", "SR.vcc", "5 V debe llegar al sensor")
    E.exigir("D6", "SR.trig", "el pin 6 debe llegar a TRIG")
    E.exigir("D7", "SR.echo", "el pin 7 debe llegar a ECHO")
    E.exigir("SR.gnd", "GND", "GND debe llegar al sensor")
    for a, b in (("5V", "GND"), ("D6", "D7"), ("D6", "GND"), ("D7", "GND"), ("D7", "5V"), ("D6", "5V")):
        E.prohibir(a, b, f"{a} y {b} no pueden tocarse")
    E.dibujar(os.path.join(AQUI, "P15_distancia_cableado.png"))
    print("P15 cableado listo")


def _led8_y_zumbador(circ, bb, ard, nuevo):
    """LED rojo en el pin 8 (columnas 12 a 17) y zumbador pasivo con su resistencia (columnas 2 a 7).
    Pasos: 1 LED, 2 resistencia, 3 cable negro, 4 cable naranja al pin 8; 5 zumbador, 6 resistencia, 7 cable azul al pin 12, 8 cable negro."""
    s = (lambda n: n) if nuevo else (lambda n: None)
    circ.led(anodo=(13, "g"), catodo=(12, "g"), color="rojo", step=s(1), nombre="LED8")
    circ.resistor((17, "h"), (13, "h"), 220, step=s(2), nombre="R8")
    circ.wire(("bb", 12, "j"), ("rail", "B", "-", 11), "negro", step=s(3))
    circ.wire(("ard", "D8"), ("bb", 17, "j"), "naranja", step=s(4), badge=(21.9, bb.y + 25.0))
    circ.zumbador(4, "pasivo", step=s(5))                                        # patas en f4 y f7
    circ.resistor((2, "i"), (4, "i"), 220, step=s(6), nombre="R12")
    px = ard.xy("D12")[0]
    xc = bb.hole(2, "j")[0]
    yc = bb.y + 22.4
    circ.wire(("ard", "D12"), ("bb", 2, "j"), "azul", step=s(7), ruta=[(px, yc), (xc, yc)], badge=(12.0, yc))
    circ.wire(("bb", 7, "j"), ("rail", "B", "-", 7), "negro", step=s(8))


def _verificar_led8_zumbador(circ):
    _verificar_grupo(circ, 8, "D8")
    r_a, r_b = circ.elems["R12"]
    a, b = circ.elems["BZ"]
    circ.exigir(("ard", "D12"), r_a, "el pin 12 debe llegar a la resistencia del zumbador")
    circ.exigir(r_b, a, "la resistencia debe llegar al zumbador")
    circ.exigir(b, ("ard", "GND"), "la otra pata del zumbador debe llegar a GND")
    circ.prohibir(("ard", "D12"), a, "el pin 12 no debe llegar al zumbador sin pasar por la resistencia")
    circ.prohibir(("ard", "D12"), ("ard", "GND"), "pin 12 y GND no pueden tocarse")
    circ.prohibir(("ard", "D8"), ("ard", "D12"), "los pines 8 y 12 no pueden tocarse")


def p16():
    c = Canvas(61, 76)
    c.header("P16 · Barrera automática", "Sobre P15, el LED de «barrera abierta» y el zumbador con su resistencia, a la izquierda (vista desde arriba)")
    bb = Breadboard(3.0, 10.8, cols=30)
    ard = Arduino(bb.x + 2.6, bb.y + bb.H + 6.2)
    circ = Circuit(c, ard, bb)
    _lista_s8_base(circ, bb, ard)
    _sonar(circ, bb, ard, nuevo=False)
    _led8_y_zumbador(circ, bb, ard, nuevo=True)
    _verificar_servo(circ)
    _verificar_sonar(circ)
    _verificar_led8_zumbador(circ)
    circ.draw()
    # Las dos etiquetas van en la zona libre de arriba (filas a a c, columnas 1 a 13), debajo de los números de las columnas. Sus guías son
    # verticales y bajan entre dos columnas (a media posición) para no tapar números ni insignias; terminan sobre el cuerpo de la pieza.
    sz = 0.54
    t_zumb, t_led = ["Zumbador PASIVO", "y su resistencia de 220 Ω"], ["LED rojo:", "barrera abierta"]
    bw_z, bh_z = medida_etiqueta(c, t_zumb, sz)
    bw_l, bh_l = medida_etiqueta(c, t_led, sz)
    y_et = bb.y + 3.95
    x_z = bb.x + 1.6                                                  # a la derecha de las letras de las filas (a, b, c)
    x_l = x_z + bw_z + 0.6
    cxz = (bb.hole(4, "f")[0] + bb.hole(7, "f")[0]) / 2
    cyz = bb.hole(4, "f")[1]
    xg_z = bb.hole(3, "a")[0] + 0.5                                   # entre las columnas 3 y 4
    etiqueta_guias(c, x_z, y_et, t_zumb, [(xg_z, y_et + bh_z - 0.1, xg_z, borde_circulo(cxz, cyz, 2.36, xg_z))], sz)
    lx, ly = _led_cuerpo(bb, 13, 12)
    xg_l = bb.hole(11, "a")[0] + 0.5                                  # entre las columnas 11 y 12
    etiqueta_guias(c, x_l, y_et, t_led, [(xg_l, y_et + bh_l - 0.1, xg_l, borde_circulo(lx, ly, 1.55, xg_l, 0.3))], sz)
    c.callout(40.4, bb.y + 36.9, ["Servo, rieles y sensor:", "ya armados (P13 y P15)"], size=0.54)
    pie_leyenda(c, ard, 2, [(COL["negro"], "GND  (−, tierra)"), (COL["rojo"], "+5 V (rieles, servo y sensor)"), (COL["morado"], "Señal del servo: pin 9 (ya está)"),
                            (COL["gris"], "ECHO al pin 7 (ya está)"), (COL["cafe"], "TRIG al pin 6 (ya está)"),
                            (COL["naranja"], "Señal del LED: pin 8 (nuevo)"), (COL["azul"], "Señal del zumbador: pin 12 (nuevo)")])
    c.text(c.w_u - 1.2, c.h_u - 1.2, "Del 1 al 4, el LED; del 5 al 8, el zumbador. Los cables cruzan por encima sin tocarse.", 0.5, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P16_barrera_automatica.png"))
    print("P16 listo")
    for fila in sorted((f for f in circ.table if f[0]), key=lambda t: t[0]):
        print("  ", fila)


def cableado_p16():
    E = Esquema(46, 57.0)
    E.titulo("P16 · Barrera automática", "esquema de conexiones · todo lo de «5 V» va al riel rojo y todo lo de «GND» al riel azul")
    E.placa(1.5, 5.0, 7.5, 51.0, "Arduino\nUNO R3", [("D6", "D6", 12.5), ("D7", "D7", 16.5), ("D9", "D9", 28.5), ("D8", "D8", 41.0), ("D12", "D12", 47.0),
                                                     ("5V", "5V", 52.0), ("GND", "GND", 54.5)])
    # sensor
    E.bloque("SR", 22.0, 6.0, 10.0, 17.0, "HC-SR04", "ultrasonido",
             terminales=[("vcc", "izq", 2.5, "VCC"), ("trig", "izq", 6.5, "TRIG"), ("echo", "izq", 10.5, "ECHO"), ("gnd", "izq", 14.5, "GND")])
    E.cable("cafe", "D6", "SR.trig")
    E.cable("gris", "D7", "SR.echo")
    E.etiqueta_red("SR.vcc", "5V", "5 V", "rojo")
    E.etiqueta_red("SR.gnd", "GND", "GND", "negro")
    # servo
    E.bloque("SV", 22.0, 26.0, 10.0, 11.0, "Servo", "SG90",
             terminales=[("sig", "izq", 2.5, "SEÑAL"), ("vcc", "izq", 6.5, "5 V"), ("gnd", "izq", 10.5, "GND")])
    E.cable("morado", "D9", "SV.sig")
    E.etiqueta_red("SV.vcc", "5V", "5 V", "rojo")
    E.etiqueta_red("SV.gnd", "GND", "GND", "negro")
    # LED
    E.resistencia("R8", 15.0, 41.0, "220 Ω")
    E.led("LED8", 23.0, 41.0, "rojo")
    E.cable("naranja", "D8", "R8.a")
    E.cable("naranja", "R8.b", "LED8.a")
    E.etiqueta_red("LED8.k", "GND", "GND", "negro", lado="der")
    # zumbador pasivo
    E.resistencia("R12", 15.0, 47.0, "220 Ω")
    E.bloque("BZ", 23.0, 45.0, 8.0, 4.0, "Zumbador", "pasivo", terminales=[("p", "izq", 2.0, ""), ("n", "der", 2.0, "")])
    E.cable("azul", "D12", "R12.a")
    E.cable("azul", "R12.b", "BZ.p")
    E.etiqueta_red("BZ.n", "GND", "GND", "negro", lado="der")
    # los pines de la placa que reparten energía
    E.nota(9.8, 50.6, "5 V al riel rojo (+)", anchor="lm", color="#c8202b", negrita=True)
    E.nota(9.8, 53.1, "GND al riel azul (−)", anchor="lm", color="#262626", negrita=True)
    E.nota(10.0, 14.6, "pin 6 · cable café", anchor="lm")
    E.nota(10.0, 18.6, "pin 7 · cable gris", anchor="lm")
    E.nota(10.0, 30.6, "pin 9 · cable morado", anchor="lm")
    E.nota(10.0, 39.4, "pin 8 · cable naranja", anchor="lm")
    E.nota(10.0, 45.4, "pin 12 · cable azul", anchor="lm")
    E.nota(33.0, 41.0, "enciende al abrir", anchor="lm", color="#8a8a8a")
    E.nota(33.0, 15.0, "15 mA · 2 cm a 4 m", anchor="lm", color="#8a8a8a")
    E.exigir("D6", "SR.trig", "el pin 6 debe llegar a TRIG")
    E.exigir("D7", "SR.echo", "el pin 7 debe llegar a ECHO")
    E.exigir("5V", "SR.vcc", "5 V debe llegar al sensor")
    E.exigir("GND", "SR.gnd", "GND debe llegar al sensor")
    E.exigir("D9", "SV.sig", "el pin 9 debe llegar al servo")
    E.exigir("5V", "SV.vcc", "5 V debe llegar al servo")
    E.exigir("GND", "SV.gnd", "GND debe llegar al servo")
    E.exigir("D8", "R8.a", "el pin 8 debe llegar a la resistencia del LED")
    E.exigir("LED8.k", "GND", "la pata corta del LED debe llegar a GND")
    E.exigir("D12", "R12.a", "el pin 12 debe llegar a la resistencia del zumbador")
    E.exigir("BZ.n", "GND", "el zumbador debe llegar a GND")
    E.prohibir("D12", "BZ.p", "el pin 12 no debe llegar al zumbador sin pasar por la resistencia")
    for a, b in (("5V", "GND"), ("D6", "D7"), ("D8", "D9"), ("D9", "D12"), ("D6", "GND"), ("D7", "GND"), ("D9", "GND"), ("D8", "GND"), ("D12", "GND")):
        E.prohibir(a, b, f"{a} y {b} no pueden tocarse")
    E.dibujar(os.path.join(AQUI, "P16_barrera_automatica_cableado.png"))
    print("P16 cableado listo")


def eco_diagrama():
    """HC-SR04: tiempo de vuelo del eco y la cuenta de la distancia."""
    c = Lienzo(66, 42)
    c.header("P15 · Cómo mide la distancia el HC-SR04", "Manda un chirrido que nadie oye (40 kHz), espera el eco y mide cuánto tardó: el tiempo es la distancia")
    # esquema físico
    c.rect(2.0, 11.0, 4.0, 8.0, fill="#1b5c8a", outline="#0f3b5c", width=0.1, r=0.4)
    c.rect(6.0, 11.8, 2.2, 2.6, fill="#c9ced4", outline="#6b7178", width=0.06, r=0.4)
    c.rect(6.0, 15.6, 2.2, 2.6, fill="#c9ced4", outline="#6b7178", width=0.06, r=0.4)
    c.text(4.0, 20.6, "HC-SR04", 0.55, TINTA, "Bold")
    c.rect(32.0, 8.0, 1.6, 14.0, fill="#9a7b4f", outline="#6b5231", width=0.08, r=0.3)
    c.text(32.8, 23.2, "objeto", 0.55, TINTA, "Bold")
    _flecha(c, (8.6, 13.1), (31.6, 13.1), "#c4690a", 0.16, 0.7)
    _flecha(c, (31.6, 17.0), (8.6, 17.0), "#2a6fdb", 0.16, 0.7)
    c.text(20.0, 11.9, "TRIG: sale el chirrido", 0.55, "#c4690a", "Bold")
    c.text(20.0, 18.6, "ECHO: vuelve el eco", 0.55, "#2a6fdb", "Bold")
    c.line([(8.6, 26.0), (31.6, 26.0)], TINTA, 0.1, ends=False)
    c.line([(8.6, 25.4), (8.6, 26.6)], TINTA, 0.1, ends=False)
    c.line([(31.6, 25.4), (31.6, 26.6)], TINTA, 0.1, ends=False)
    c.text(20.0, 27.4, "distancia d", 0.6, VINO, "Bold")
    # señales
    x0, y_a, y_b = 40.0, 9.0, 12.0
    c.text(52.0, 5.6, "Las señales (con un objeto a 20 cm)", 0.7, TINTA, "Bold")
    c.text(x0 - 0.5, y_a + 1.5, "TRIG", 0.6, "#c4690a", "Bold", anchor="rm")
    c.line([(x0, y_b), (x0 + 3.0, y_b), (x0 + 3.0, y_a), (x0 + 3.6, y_a), (x0 + 3.6, y_b), (x0 + 24.0, y_b)], "#c4690a", 0.2, ends=False)
    c.text(x0 + 3.3, y_a - 0.8, "10 µs", 0.5, "#c4690a", "Bold")
    y2a, y2b = 17.0, 20.0
    c.text(x0 - 0.5, y2a + 1.5, "ECHO", 0.6, "#2a6fdb", "Bold", anchor="rm")
    c.line([(x0, y2b), (x0 + 6.0, y2b), (x0 + 6.0, y2a), (x0 + 16.0, y2a), (x0 + 16.0, y2b), (x0 + 24.0, y2b)], "#2a6fdb", 0.2, ends=False)
    _flecha(c, (x0 + 6.0, y2a - 1.0), (x0 + 16.0, y2a - 1.0), VINO, 0.12, 0.5)
    _flecha(c, (x0 + 16.0, y2a - 1.0), (x0 + 6.0, y2a - 1.0), VINO, 0.12, 0.5)
    c.text(x0 + 11.0, y2a - 2.0, "≈ 1 166 µs: lo que dura ECHO", 0.5, VINO, "Bold")
    # cuenta
    c.rect(2.0, 30.0, 62.0, 4.0, fill="#1e1e24", r=0.5)
    c.text(33.0, 31.0, "distancia en cm = duración en µs × 0,0343 ÷ 2", 0.8, "#f2f2f2", "MonoBold")
    c.text(33.0, 32.9, "(÷ 2 porque el sonido va hasta el objeto y regresa)", 0.5, "#c9c9d0", "Medium")
    cols = [("Distancia", 2.0, 13.0), ("Duración de ECHO", 15.0, 18.0), ("Qué pasa", 33.0, 31.0)]
    filas = [("10 cm", f"{round(10 * 2 / 0.0343)} µs", "ECHO dura poco"), ("20 cm", f"{round(20 * 2 / 0.0343)} µs", "el ejemplo de arriba"),
             ("50 cm", f"{round(50 * 2 / 0.0343)} µs", "tres veces más que a 20 cm"), ("4 m (el máximo)", f"{round(400 * 2 / 0.0343)} µs", "unos 23 ms")]
    yt = 35.2
    for (t, xx, w) in cols:
        c.rect(xx, yt, w, 1.2, fill=VINO, outline="#ffffff", width=0.05)
        c.text(xx + w / 2, yt + 0.62, t, 0.46, "#ffffff", "Bold")
    for r_, fila in enumerate(filas):
        yy = yt + 1.2 + r_ * 1.0
        for (t, xx, w), v in zip(cols, fila):
            c.rect(xx, yy, w, 1.0, fill="#ffffff", outline="#cfc9b8", width=0.05)
            c.text(xx + 0.5, yy + 0.52, v, 0.46, TINTA, "SemiBold" if xx == 2.0 else "Medium", anchor="lm")
    c.text(c.w_u - 1.0, c.h_u - 0.3, "El programa espera el eco hasta 30 ms (unos 5 m); si no llega, escribe «Sin eco». Alcance de la hoja de datos: 2 cm a 4 m, ángulo de unos 15°.", 0.46, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P15_eco.png"))
    print("P15 eco listo")


def estados_barrera():
    """Estados de la barrera automática y qué los cambia."""
    c = Canvas(56, 30)
    c.header("P16 · Los estados de la barrera", "Una sola medición decide si abrir; para cerrar hace falta que el paso esté libre 2 segundos seguidos")
    ya, r = 14.0, 5.6
    est = [(12.0, "CERRADA", ["servo en 0°", "LED apagado"], "#eceae4", "#8a8a8a"), (44.0, "ABIERTA", ["servo en 90°", "LED encendido"], "#fff3bf", "#c99a00")]
    for cx, nombre, lineas, fondo, borde in est:
        c.circle(cx, ya, r, fill=fondo, outline=borde, width=0.14)
        c.text(cx, ya - 1.6, nombre, 0.85, TINTA, "Bold")
        for i, s in enumerate(lineas):
            c.text(cx, ya + 0.2 + i * 1.15, s, 0.56, GRIS_T, "SemiBold")
    G._arco(c, (12.0 + r - 0.6, ya - 2.4), (44.0 - r + 0.6, ya - 2.4), -3.4, VINO)
    c.text(28.0, 6.4, "algo a menos de 20 cm", 0.68, VINO, "Bold")
    c.text(28.0, 7.5, "abre y suena un pitido agudo", 0.5, GRIS_T, "SemiBold")
    G._arco(c, (44.0 - r + 0.6, ya + 2.4), (12.0 + r - 0.6, ya + 2.4), 3.4, GRIS_T)
    c.text(28.0, 21.6, "paso libre 2 s seguidos (20 ciclos de 100 ms)", 0.62, GRIS_T, "Bold")
    c.text(28.0, 22.7, "cierra y suena un pitido grave", 0.5, GRIS_T, "SemiBold")
    c.text(28.0, 26.6, "Mientras está abierta, si vuelve a haber algo enfrente, la cuenta de «libre» vuelve a cero.", 0.55, VINO, "Bold")
    c.text(28.0, 28.0, "En el programa: la variable ciclosLibre cuenta de 0 a 20 y se reinicia si el sensor ve algo.", 0.5, GRIS_T, "Medium")
    c.save(os.path.join(AQUI, "P16_estados.png"))
    print("P16 estados listo")


TODOS = {"P11": [ldr_conoce, p11, cableado_p11],
         "P12": [umbral_diagrama, retro_diagrama, p12, cableado_p12],
         "P13": [servo_conoce, barrido_diagrama, p13, cableado_p13],
         "P14": [p14, cableado_p14],
         "P15": [eco_diagrama, p15, cableado_p15],
         "P16": [p16, cableado_p16, estados_barrera]}

if __name__ == "__main__":
    pedidos = sys.argv[1:] or list(TODOS)
    for clave in pedidos:
        for f in TODOS[clave]:
            f()
