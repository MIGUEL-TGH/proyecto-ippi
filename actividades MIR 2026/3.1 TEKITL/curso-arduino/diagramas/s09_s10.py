"""Diagramas de las sesiones 9 (transistor y motor) y 10 (temperatura).

Uso:  python s09_s10.py            (genera todos)
      python s09_s10.py P17 P18    (genera solo los de P17 y P18)
Reutiliza el motor de generar_diagramas.py y de s06_s08.py.

Sesión 9: el motor está BLOQUEADO (plan, V1). Los diagramas muestran la versión con LED (la que se arma hoy).
El circuito del motor no se dibuja hasta resolver V1: puede cambiar el motor o el transistor.
"""
import math
import os
import sys

from diagrama import Arduino, Breadboard, Canvas, Circuit, COL, GRIS_T, TINTA, VINO, LED_COL
from esquema import Esquema, Lienzo
import generar_diagramas as G
import s06_s08 as S

AQUI = G.AQUI
_leyenda, _lista, _caja_aviso, _flecha, _led_cuerpo = G._leyenda, G._lista, G._caja_aviso, G._flecha, G._led_cuerpo
pie_leyenda, cables_derecha = S.pie_leyenda, S.cables_derecha
GOLD_BORDE = G.GOLD_BORDE


# ====================================================================== SESIÓN 9
def _d_to92(c, xm, cy, r=1.5):
    """Cuerpo del transistor TO-92 visto desde arriba: círculo con la cara plana hacia abajo. Devuelve la y del borde plano."""
    ang0 = math.asin(0.6)
    pts = []
    n = 24
    t0, t1 = math.pi - ang0, 2 * math.pi + ang0
    for k in range(n + 1):
        t = t0 + (t1 - t0) * k / n
        pts.append((xm + r * math.cos(t), cy + r * math.sin(t)))
    c.poly(pts, fill="#1d1d1f", outline="#000000", width=0.06)
    return cy + 0.6 * r


def dibujar_pn2222(c, bb, col, step=None):
    """PN2222 enchufado en la fila f: patas en las columnas col, col+1 y col+2 (de izquierda a derecha: emisor, base, colector), cara plana hacia abajo."""
    xs = [bb.hole(col + k, "f")[0] for k in range(3)]
    yf = bb.hole(col, "f")[1]
    xm = xs[1]
    cy = yf - 2.7
    borde = _d_to92(c, xm, cy)
    for xx, letra in zip(xs, ("E", "B", "C")):
        c.line([(xx, borde), (xx, yf)], "#b8b8b8", 0.2, ends=True)
        c.text(xx, yf - 0.95, letra, 0.42, TINTA, "Bold")
    c.text(xm, cy - 0.2, "PN2222", 0.3, "#9a9a9a", "Bold")
    if step:
        c.badge(xm, cy - 2.4, step)


def _transistor_en_circuito(circ, bb, col, step):
    for k in range(3):
        circ._occupy(("bb", col + k, "f"), "Q")
    circ.elems["Q"] = [("bb", col + k, "f") for k in range(3)]       # emisor, base, colector
    circ.dibujo(lambda c: dibujar_pn2222(c, bb, col, step))


def _carga_led(circ, bb, ard, nuevo):
    """Transistor en f22 a f24 (E, B, C); base con 330 Ω al pin 5; colector a un LED con 220 Ω hacia 5 V. Pasos: 1 a 8."""
    s = (lambda n: n) if nuevo else (lambda n: None)
    _transistor_en_circuito(circ, bb, 22, s(1))
    circ.resistor((23, "i"), (20, "i"), 330, step=s(2), nombre="RB")
    circ.wire(("ard", "D5"), ("bb", 20, "j"), "naranja", step=s(3))
    circ.wire(("bb", 22, "j"), ("rail", "B", "-", 22), "negro", step=s(4))
    circ.wire(("bb", 24, "j"), ("bb", 26, "j"), "azul", step=s(5))
    circ.led(anodo=(27, "g"), catodo=(26, "g"), color="rojo", step=s(6), nombre="LEDC")
    circ.resistor((27, "h"), (29, "h"), 220, step=s(7), nombre="RC")
    circ.wire(("bb", 29, "j"), ("rail", "B", "+", 29), "rojo", step=s(8))


def _verificar_carga_led(circ):
    e, b, c = circ.elems["Q"]
    rb_a, rb_b = circ.elems["RB"]
    l_a, l_k = circ.elems["LEDC"]
    rc_a, rc_b = circ.elems["RC"]
    circ.exigir(e, ("ard", "GND"), "el emisor debe llegar a GND")
    circ.exigir(("ard", "D5"), rb_b, "el pin 5 debe llegar a la resistencia de la base")
    circ.exigir(rb_a, b, "la resistencia debe llegar a la base")
    circ.exigir(c, l_k, "el colector debe llegar a la pata corta (−) del LED")
    circ.exigir(l_a, rc_a, "la pata larga (+) del LED debe llegar a la resistencia de 220 Ω")
    circ.exigir(rc_b, ("ard", "5V"), "la resistencia de 220 Ω debe llegar a 5 V")
    circ.prohibir(("ard", "D5"), b, "el pin 5 no debe llegar a la base sin pasar por la resistencia")
    circ.prohibir(e, c, "emisor y colector no pueden estar unidos")
    circ.prohibir(e, b, "emisor y base no pueden estar unidos")
    circ.prohibir(c, ("ard", "5V"), "el colector no puede llegar a 5 V sin pasar por el LED y su resistencia")
    circ.prohibir(c, ("ard", "GND"), "el colector no puede estar unido a GND")
    circ.prohibir(("ard", "D5"), ("ard", "5V"), "el pin 5 y 5 V no pueden tocarse")
    circ.prohibir(("ard", "D5"), ("ard", "GND"), "el pin 5 y GND no pueden tocarse")
    circ.prohibir(("ard", "5V"), ("ard", "GND"), "5 V y GND no pueden tocarse")


def _rieles_s9(circ, bb, ard, nuevo):
    """GND de la placa al riel azul y 5 V al riel rojo por la izquierda (lo mismo que en la Sesión 7)."""
    s = (lambda n: n) if nuevo else (lambda n: None)
    borde = ard.y + ard.H
    x5 = ard.xy("5V")[0]
    circ.wire(("ard", "GND"), ("rail", "B", "-", 13), "negro", via=0.45, step=s(None))
    circ.wire(("ard", "5V"), ("rail", "B", "+", 2), "rojo", step=s(None),
              ruta=[(x5, borde + 2.0), (1.8, borde + 2.0), (1.8, bb.y + 21.4), (bb.rail_hole("B", "+", 2)[0], bb.y + 21.4)], badge=(10.0, borde + 2.0))


def p17():
    c = Canvas(38.5, 69.0)
    c.header("P17 · Transistor como interruptor (versión con LED)", "El pin 5 enciende un LED a través de un PN2222; el botón del pin 2 manda (vista desde arriba)")
    bb = Breadboard(3.0, 4.6, cols=30)
    ard = Arduino(bb.x + 2.6, bb.y + bb.H + 6.2)
    circ = Circuit(c, ard, bb)
    _rieles_s9(circ, bb, ard, nuevo=False)
    _carga_led(circ, bb, ard, nuevo=True)
    # botón (pasos 9 a 11): cruza el canal en las columnas 8 y 10
    circ.boton(8, step=9)
    circ.wire(("ard", "D2"), ("bb", 8, "j"), "verde", step=10, via=0.35)
    circ.wire(("rail", "B", "-", 11), ("bb", 10, "a"), "negro", step=11, ruta=[(bb.rail_hole("B", "-", 11)[0], bb.hole(10, "a")[1])], badge=(bb.rail_hole("B", "-", 11)[0], bb.y + 13.0))
    _verificar_carga_led(circ)
    circ.prohibir(("ard", "D2"), ("ard", "GND"), "el pin 2 y GND no pueden estar unidos sin presionar el botón")
    circ.comprobar_boton("B", ("ard", "D2"), ("ard", "GND"), "el botón debe unir el pin 2 con GND solo al presionarlo")
    circ.draw()
    xq = bb.hole(23, "f")[0]
    c.callout(bb.x + 11.4, bb.y + 3.4, ["PN2222: cara plana hacia abajo,", "patas E · B · C de izquierda a derecha"], target=(xq, bb.hole(22, "f")[1] - 4.0), size=0.5)
    c.callout(bb.x + 1.0, bb.y + 12.6, ["Botón: cruza el canal;", "cables en patas OPUESTAS"], target=(bb.hole(9, "e")[0] - 1.0, bb.hole(8, "f")[1] - 1.6), size=0.5)
    pie_leyenda(c, ard, 2, [(COL["negro"], "GND  (−, tierra)"), (COL["rojo"], "+5 V (riel rojo, a la carga)"), (COL["naranja"], "Señal del pin 5 a la base (330 Ω)"),
                            (COL["azul"], "Colector al LED"), (COL["verde"], "Señal del pin 2: el botón")])
    c.text(c.w_u - 1.2, c.h_u - 1.2, "Del 1 al 8 es el transistor con su LED; del 9 al 11, el botón. Los cables cruzan por encima sin tocarse.", 0.5, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P17_transistor_led.png"))
    print("P17 listo")
    for fila in sorted((f for f in circ.table if f[0]), key=lambda t: t[0]):
        print("  ", fila)


def _esq_transistor(E, dy, con_boton=False):
    """Parte del transistor del esquema; dy desplaza todo hacia abajo. Pin D5 -> 330 Ω -> base; colector -> LED -> 220 Ω -> 5 V; emisor a GND."""
    yb = 16.5 + dy
    E.resistencia("RB", 13.0, yb, "330 Ω")
    E.bloque("Q", 22.0, yb - 2.0, 7.0, 6.0, "PN2222", "E · B · C", terminales=[("b", "izq", 2.0, "B"), ("c", "sup", 3.5, "C"), ("e", "inf", 3.5, "E")])
    E.cable("naranja", "D5", "RB.a")
    E.cable("naranja", "RB.b", "Q.b")
    E.resistencia("RC", 14.0, yb - 5.0, "220 Ω")
    E.led("LEDC", 21.9, yb - 5.0, "rojo")
    E.cable("azul", "RC.b", "LEDC.a")
    E.cable("azul", "LEDC.k", "Q.c")
    E.etiqueta_red("RC.a", "5V", "5 V", "rojo")
    E.terminal("TAPE", 25.5, yb + 7.5)
    E.cable("negro", "Q.e", "TAPE")
    E.etiqueta_red("TAPE", "GND", "GND", "negro", lado="der")
    E.nota(9.5, yb - 1.45, "pin 5 (salida)")
    E.nota(9.5, yb + 1.45, "cable naranja")
    E.nota(30.0, yb - 5.0, "carga (LED)", anchor="lm", color="#8a8a8a")


def cableado_p17():
    E = Esquema(38, 34.0)
    E.titulo("P17 · Transistor como interruptor (versión con LED)", "esquema de conexiones · una corriente pequeña en la base abre el camino de la carga")
    E.placa(1.5, 5.0, 7.5, 27.0, "Arduino\nUNO R3", [("D2", "D2", 8.5), ("D5", "D5", 22.5), ("5V", "5V", 28.0), ("GND", "GND", 30.5)])
    # botón: pin 2 -> botón -> GND
    E.boton("B", 14.0, 8.5, w=6.0)
    E.cable("verde", "D2", "B.a")
    E.etiqueta_red("B.b", "GND", "GND", "negro", lado="der")
    E.nota(9.5, 7.05, "pin 2 (entrada)")
    E.nota(9.5, 9.95, "cable verde")
    _esq_transistor(E, 6.0)
    E.nota(9.8, 27.1, "5 V al riel rojo (+)", anchor="lm", color="#c8202b", negrita=True)
    E.nota(9.8, 29.6, "GND al riel azul (−)", anchor="lm", color="#262626", negrita=True)
    E.exigir("D5", "RB.a", "el pin 5 debe llegar a la resistencia de la base")
    E.exigir("RB.b", "Q.b", "la resistencia debe llegar a la base")
    E.exigir("Q.e", "GND", "el emisor debe llegar a GND")
    E.exigir("Q.c", "LEDC.k", "el colector debe llegar al LED")
    E.exigir("RC.a", "5V", "la resistencia de 220 Ω debe llegar a 5 V")
    E.exigir("D2", "B.a", "el pin 2 debe llegar al botón")
    E.exigir("B.b", "GND", "el botón debe llegar a GND")
    for a, b in (("5V", "GND"), ("D5", "GND"), ("D5", "5V"), ("Q.c", "GND"), ("Q.c", "5V"), ("D2", "D5")):
        E.prohibir(a, b, f"{a} y {b} no pueden tocarse")
    E.dibujar(os.path.join(AQUI, "P17_transistor_led_cableado.png"))
    print("P17 cableado listo")


def p18():
    c = Canvas(38.5, 69.0)
    c.header("P18 · La perilla regula la carga (versión con LED)", "En lugar del botón, el potenciómetro de la izquierda (centro a A0); el pin 5 regula el brillo por PWM (vista desde arriba)")
    bb = Breadboard(3.0, 4.6, cols=30)
    ard = Arduino(bb.x + 2.6, bb.y + bb.H + 6.2)
    circ = Circuit(c, ard, bb)
    _rieles_s9(circ, bb, ard, nuevo=False)
    _carga_led(circ, bb, ard, nuevo=False)
    circ.potenciometro(5, step=1, nombre="POT")                         # f5 (GND), f7 (centro), f9 (5 V)
    circ.wire(("bb", 5, "j"), ("rail", "B", "-", 5), "negro", step=2)
    borde = ard.y + ard.H
    xa0 = ard.xy("A0")[0]
    xj7 = bb.hole(7, "j")[0]
    circ.wire(("ard", "A0"), ("bb", 7, "j"), "amarillo", step=3,
              ruta=[(xa0, borde + 0.9), (35.3, borde + 0.9), (35.3, bb.y + 23.6), (xj7, bb.y + 23.6)], badge=(32.0, borde + 0.9))
    circ.wire(("rail", "B", "+", 9), ("bb", 9, "j"), "rojo", step=4)
    _verificar_carga_led(circ)
    a, w, b = circ.elems["POT"]
    circ.exigir(("ard", "GND"), a, "el extremo izquierdo del potenciómetro debe llegar a GND")
    circ.exigir(("ard", "A0"), w, "el centro del potenciómetro debe llegar a A0")
    circ.exigir(("ard", "5V"), b, "el extremo derecho del potenciómetro debe llegar a 5 V")
    circ.prohibir(w, ("ard", "5V"), "el centro no puede estar unido a 5 V")
    circ.prohibir(w, ("ard", "GND"), "el centro no puede estar unido a GND")
    circ.prohibir(a, b, "los extremos del potenciómetro no pueden estar unidos")
    circ.prohibir(("ard", "A0"), ("ard", "D5"), "A0 y el pin 5 no pueden tocarse")
    circ.draw()
    xq = bb.hole(23, "f")[0]
    c.callout(bb.x + 11.4, bb.y + 3.4, ["Transistor y LED: ya armados", "en P17 (el botón se retira)"], target=(xq, bb.hole(22, "f")[1] - 4.0), size=0.5)
    c.callout(bb.x + 1.0, bb.y + 12.8, ["Potenciómetro:", "el centro va a A0"], target=(bb.hole(7, "f")[0], bb.hole(7, "f")[1] - 3.6), size=0.5)
    pie_leyenda(c, ard, 1, [(COL["negro"], "GND  (−, tierra)"), (COL["rojo"], "+5 V (riel rojo)"), (COL["naranja"], "Señal del pin 5 a la base (ya está)"),
                            (COL["azul"], "Colector al LED (ya está)"), (COL["amarillo"], "Centro del potenciómetro a A0 (nuevo)")])
    c.text(c.w_u - 1.2, c.h_u - 1.2, "Del 1 al 4 es lo nuevo: el potenciómetro. El transistor y el LED siguen como en P17.", 0.5, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P18_transistor_perilla.png"))
    print("P18 listo")


def cableado_p18():
    E = Esquema(38, 40.0)
    E.titulo("P18 · La perilla regula la carga (versión con LED)", "esquema de conexiones · la perilla entra por A0 y el pin 5 regula el brillo con PWM")
    E.placa(1.5, 5.0, 7.5, 33.0, "Arduino\nUNO R3", [("A0", "A0", 10.0), ("D5", "D5", 28.5), ("5V", "5V", 34.0), ("GND", "GND", 36.5)])
    E.potenciometro("P", 18.0, 6.0, 14.0)
    E.etiqueta_red("P.a", "5V", "5 V", "rojo", lado="der", largo=3.0)
    E.etiqueta_red("P.b", "GND", "GND", "negro", lado="der", largo=3.0)
    E.cable("amarillo", "A0", "P.w")
    E.nota(9.5, 8.55, "A0 (entrada)")
    E.nota(9.5, 11.45, "cable amarillo")
    E.etiqueta(24.0, 10.0, "Perilla", None, anchor="lm")
    _esq_transistor(E, 12.0)
    E.nota(9.8, 33.1, "5 V al riel rojo (+)", anchor="lm", color="#c8202b", negrita=True)
    E.nota(9.8, 35.6, "GND al riel azul (−)", anchor="lm", color="#262626", negrita=True)
    E.exigir("A0", "P.w", "A0 debe llegar al centro de la perilla")
    E.exigir("P.a", "5V", "un extremo de la perilla debe llegar a 5 V")
    E.exigir("P.b", "GND", "el otro extremo de la perilla debe llegar a GND")
    E.exigir("D5", "RB.a", "el pin 5 debe llegar a la resistencia de la base")
    E.exigir("RB.b", "Q.b", "la resistencia debe llegar a la base")
    E.exigir("Q.e", "GND", "el emisor debe llegar a GND")
    E.exigir("Q.c", "LEDC.k", "el colector debe llegar al LED")
    for a, b in (("5V", "GND"), ("A0", "D5"), ("A0", "5V"), ("A0", "GND"), ("D5", "GND"), ("D5", "5V")):
        E.prohibir(a, b, f"{a} y {b} no pueden tocarse")
    E.dibujar(os.path.join(AQUI, "P18_transistor_perilla_cableado.png"))
    print("P18 cableado listo")


def _simbolo_npn(c, x, y, tam=3.0):
    """Símbolo del transistor NPN: base a la izquierda, colector arriba y emisor abajo (con flecha). (x, y) = centro del círculo."""
    c.circle(x, y, tam, outline=TINTA, width=0.14)
    c.line([(x - 0.8, y - tam * 0.62), (x - 0.8, y + tam * 0.62)], TINTA, 0.22, ends=False)
    c.line([(x - tam - 1.6, y), (x - 0.8, y)], TINTA, 0.16, ends=False)
    c.line([(x - 0.8, y - 0.9), (x + 1.4, y - tam + 0.3), (x + 1.4, y - tam - 1.4)], TINTA, 0.16, ends=False)
    c.line([(x - 0.8, y + 0.9), (x + 1.4, y + tam - 0.3), (x + 1.4, y + tam + 1.4)], TINTA, 0.16, ends=False)
    ex, ey = x + 1.4, y + tam - 0.3
    c.poly([(ex, ey), (ex - 0.25, ey - 1.05), (ex - 1.0, ey - 0.45)], fill=TINTA)


def transistor_conoce():
    """El PN2222 como interruptor: patas, corrientes y por qué se necesita."""
    c = Lienzo(74, 46)
    c.header("P17 · El transistor como interruptor (PN2222)", "Una corriente pequeña en la base abre el paso a una corriente grande entre colector y emisor")
    # ---- por fuera
    c.text(10.0, 5.5, "Por fuera", 0.85, TINTA, "Bold")
    xm, cy = 10.0, 11.0
    borde = _d_to92(c, xm, cy, r=4.2)
    for k, (dx, letra, nom) in enumerate(((-2.54, "1", "Emisor (E)"), (0.0, "2", "Base (B)"), (2.54, "3", "Colector (C)"))):
        c.line([(xm + dx * 1.1, borde), (xm + dx * 1.1, borde + 6.0)], "#b8b8b8", 0.4, ends=True)
        c.text(xm + dx * 1.1, borde + 7.4, letra, 0.8, VINO, "Bold")
        c.text(xm + dx * 1.1, borde + 8.6, nom.split(" ")[0], 0.5, TINTA, "SemiBold")
    c.text(xm, cy - 0.3, "PN2222", 0.7, "#cfcfcf", "Bold")
    c.text(xm, borde + 11.0, "Con la cara plana hacia ti y las patas hacia abajo,", 0.46, GRIS_T, "Medium")
    c.text(xm, borde + 12.1, "de izquierda a derecha: emisor, base, colector.", 0.46, GRIS_T, "Medium")
    c.text(xm, borde + 13.5, "(Hoja de datos del kit. Otros fabricantes numeran", 0.46, "#b00020", "SemiBold")
    c.text(xm, borde + 14.6, "las patas al revés: se comprueba con el multímetro.)", 0.46, "#b00020", "SemiBold")
    # ---- símbolo y corrientes
    c.text(36.0, 5.5, "En el circuito", 0.85, TINTA, "Bold")
    sx, sy = 36.0, 18.0
    _simbolo_npn(c, sx, sy)
    c.text(sx - 6.6, sy - 1.2, "B", 0.7, VINO, "Bold")
    c.text(sx + 2.8, sy - 6.2, "C", 0.7, VINO, "Bold")
    c.text(sx + 2.8, sy + 6.9, "E", 0.7, VINO, "Bold")
    c.line([(sx - 10.0, sy), (sx - 4.6, sy)], "#c4690a", 0.16, ends=False)
    c.text(sx - 10.3, sy - 1.4, "pin 5", 0.55, "#c4690a", "Bold", anchor="rm")
    c.text(sx - 10.3, sy + 0.2, "con 330 Ω", 0.5, "#c4690a", "SemiBold", anchor="rm")
    _flecha(c, (sx - 8.2, sy - 2.3), (sx - 5.6, sy - 2.3), "#c4690a", 0.12, 0.5)
    c.text(sx - 7.0, sy - 3.4, "I base ≈ 13 mA", 0.5, "#c4690a", "Bold")
    _flecha(c, (sx + 1.4, sy - 11.0), (sx + 1.4, sy - 8.0), "#2a6fdb", 0.12, 0.5)
    c.text(sx + 3.0, sy - 9.6, "I carga: de 13 mA (LED)", 0.5, "#2a6fdb", "Bold", anchor="lm")
    c.text(sx + 3.0, sy - 8.4, "a cientos de mA (motor)", 0.5, "#2a6fdb", "Bold", anchor="lm")
    c.line([(sx + 1.4, sy + 4.6), (sx + 1.4, sy + 9.0)], "#1d5fd1", 0.16, ends=False)
    c.text(sx + 1.4, sy + 9.9, "GND", 0.6, "#1d5fd1", "Bold")
    # ---- números
    c.text(61.0, 5.5, "Los números", 0.85, TINTA, "Bold")
    _lista(c, 52.0, 7.8, ["Un pin del UNO aguanta 40 mA como", "máximo (UNO.pdf).", "",
                          "PN2222 (hoja de datos del kit):", "· hasta 600 mA por el colector", "· ganancia de 100 a 300 con 150 mA",
                          "· 30 V entre colector y emisor", "", "Base: (5 V − 0,7 V) ÷ 330 Ω ≈ 13 mA", "LED: (5 − 2 − 0,2 V) ÷ 220 Ω ≈ 13 mA"], 0.48, 1.25, TINTA)
    # ---- tabla de cargas
    cols = [("Carga", 1.5, 26.0), ("Corriente que pide", 27.5, 20.0), ("¿La aguanta un pin?", 47.5, 12.0), ("¿La aguanta el PN2222?", 59.5, 13.0)]
    filas = [("1 LED con 220 Ω", "unos 13 mA", "sí", "sí"), ("4 LED en paralelo", "unos 50 mA", "no (máx. 40)", "sí"),
             ("Motor 3 a 6 V (tu medición)", "0,95 A o más", "no", "no (máx. 600 mA)")]
    yt = 33.0
    c.text(1.5, yt - 1.0, "Por qué hace falta el transistor, y por qué el motor sigue bloqueado", 0.62, VINO, "Bold", anchor="lm")
    for (t, xx, w) in cols:
        c.rect(xx, yt, w, 1.7, fill=VINO, outline="#ffffff", width=0.05)
        c.text(xx + w / 2, yt + 0.88, t, 0.46, "#ffffff", "Bold")
    for r_, fila in enumerate(filas):
        yy = yt + 1.7 + r_ * 1.7
        for (t, xx, w), v in zip(cols, fila):
            c.rect(xx, yy, w, 1.7, fill="#ffffff" if not v.startswith("no") else "#fbe3e3", outline="#cfc9b8", width=0.05)
            c.text(xx + (0.5 if xx == 1.5 else w / 2), yy + 0.9, v, 0.46, TINTA, "SemiBold", anchor="lm" if xx == 1.5 else "mm")
    _caja_aviso(c, 1.5, 41.0, 71.0, 3.9, "GND común", ["Todo lo que se une con el transistor comparte GND: el emisor, la carga y la placa. Sin GND común, la señal del pin 5 no tiene referencia."], 0.52)
    c.save(os.path.join(AQUI, "P17_transistor.png"))
    print("P17 transistor listo")


def zona_muerta():
    """P18: la lectura de la perilla, la salida PWM y la zona muerta que impone UMBRAL_ARRANQUE (ilustración con los valores del sketch)."""
    c = Canvas(60, 34)
    c.header("P18 · La zona muerta del arranque", "Un motor necesita un mínimo de PWM para empezar a girar: por debajo de UMBRAL_ARRANQUE el programa manda 0")
    x0, y0, W, H = 8.0, 6.0, 46.0, 17.0
    c.rect(x0, y0, W, H, fill="#fbfaf6", outline="#cfc9b8", width=0.08)
    for v in (0, 64, 128, 192, 255):
        yy = y0 + H - v / 255 * H
        c.line([(x0, yy), (x0 + W, yy)], "#ebe7da", 0.05, ends=False)
        c.text(x0 - 0.4, yy, str(v), 0.45, GRIS_T, "SemiBold", anchor="rm")
    for lect in (0, 256, 512, 768, 1023):
        xx = x0 + lect / 1023 * W
        c.text(xx, y0 + H + 1.0, str(lect), 0.45, GRIS_T, "SemiBold")
    c.text(x0 + W / 2, y0 + H + 2.4, "lectura de la perilla (analogRead)", 0.55, TINTA, "SemiBold")
    c.text(3.0, y0 + H / 2, "PWM", 0.6, TINTA, "Bold")

    def y_pwm(v):
        return y0 + H - v / 255 * H
    # sin umbral: la recta de map
    # con umbral 60
    xu = x0 + 241 / 1023 * W
    c.line([(x0, y_pwm(0)), (xu, y_pwm(0)), (xu, y_pwm(60)), (x0 + W, y_pwm(255))], VINO, 0.24, ends=False)
    c.rect(x0, y0, xu - x0, H, fill="#fbe3e3")
    c.text((x0 + xu) / 2, y0 + 3.0, "zona muerta", 0.62, "#b00020", "Bold")
    c.text((x0 + xu) / 2, y0 + 4.2, "el programa manda 0", 0.5, "#b00020", "SemiBold")
    c.text((x0 + xu) / 2, y0 + 5.3, "(lecturas de 0 a 240)", 0.46, "#b00020", "SemiBold")
    c.text(x0 + 24.0, y_pwm(150), "con UMBRAL_ARRANQUE = 60", 0.55, VINO, "Bold", anchor="lm")
    c.text(30.0, y0 + H + 5.2, "Con el motor, el umbral se mide: se sube la perilla poco a poco y se anota a qué PWM empieza a girar (V3).", 0.55, VINO, "Bold")
    c.text(30.0, y0 + H + 6.6, "Con el LED no hay zona muerta de verdad: se deja el 60 para sentir cómo sería, o se pone en 0 para quitarla.", 0.52, GRIS_T, "Medium")
    c.text(c.w_u - 1.0, c.h_u - 0.5, "Ilustración con los valores del sketch: map(240) da 59 y map(241) da 60.", 0.48, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P18_zona_muerta.png"))
    print("P18 zona muerta listo")


# ====================================================================== SESIÓN 10
def _ntc_R(T):
    """Resistencia del termistor (en Ω) a la temperatura T (°C), según la ecuación de Steinhart-Hart con las constantes del sketch P19."""
    A, B, C = 0.001129148, 0.000234125, 0.0000000876741
    lo, hi = 100.0, 2e6
    for _ in range(100):
        mid = (lo + hi) / 2
        lnr = math.log(mid)
        t_mid = 1 / (A + (B + C * lnr * lnr) * lnr) - 273.15
        if t_mid > T:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def _zona_a_ntc(circ, bb, ard, nuevo):
    """Zona analógica A con el termistor: NTC en f28 y f30 (30 = 5 V), 10 kΩ de la columna 28 a la 26 (GND). Pasos: 1 a 5."""
    s = (lambda n: n) if nuevo else (lambda n: None)
    circ.sensor2(28, "ntc", step=s(1), nombre="NTC")
    circ.resistor((28, "h"), (26, "h"), 10000, step=s(2), nombre="RF")
    circ.wire(("bb", 26, "j"), ("rail", "B", "-", 26), "negro", step=s(3))
    borde = ard.y + ard.H
    x_a0 = ard.xy("A0")[0]
    xj28 = bb.hole(28, "j")[0]
    circ.wire(("ard", "A0"), ("bb", 28, "j"), "amarillo", step=s(4),
              ruta=[(x_a0, borde + 0.9), (35.3, borde + 0.9), (35.3, bb.y + 23.7), (xj28, bb.y + 23.7)], badge=(32.0, borde + 0.9))
    circ.wire(("rail", "B", "+", 29), ("bb", 30, "j"), "rojo", step=s(5))


def _verificar_ntc(circ, pin="A0", clave="NTC"):
    n_m, n_5 = circ.elems[clave]
    r_m, r_g = circ.elems["RF" if clave == "NTC" else "RFB"]
    circ.exigir(("ard", "5V"), n_5, "el 5 V debe llegar a una pata del termistor")
    circ.exigir(("ard", pin), n_m, f"{pin} debe llegar a la otra pata del termistor")
    circ.exigir(("ard", pin), r_m, f"{pin} debe llegar a la resistencia de 10 kΩ")
    circ.exigir(r_g, ("ard", "GND"), "la resistencia de 10 kΩ debe llegar a GND")
    circ.prohibir(n_5, n_m, "las patas del termistor no pueden estar unidas")
    circ.prohibir(("ard", pin), ("ard", "5V"), f"{pin} y 5 V no pueden tocarse")
    circ.prohibir(("ard", pin), ("ard", "GND"), f"{pin} y GND no pueden tocarse")
    circ.prohibir(("ard", "5V"), ("ard", "GND"), "5 V y GND no pueden tocarse")


def p19():
    c = Canvas(40.5, 66.5)
    c.header("P19 · Termómetro con termistor NTC", "Sobre los rieles, el termistor y una resistencia de 10 kΩ forman un divisor de voltaje en la zona de la derecha (vista desde arriba)")
    bb = Breadboard(3.0, 4.6, cols=30)
    ard = Arduino(bb.x + 2.6, bb.y + bb.H + 6.2)
    circ = Circuit(c, ard, bb)
    _rieles_s9(circ, bb, ard, nuevo=False)
    _zona_a_ntc(circ, bb, ard, nuevo=True)
    _verificar_ntc(circ)
    circ.draw()
    xl = bb.hole(29, "f")[0]
    c.callout(bb.x + 3.4, bb.y + 4.2, ["Termistor NTC (sin polaridad) y resistencia de", "10 kΩ (café · negro · naranja), cada pata en su columna"], target=(xl, bb.hole(28, "f")[1] - 3.3), size=0.54)
    pie_leyenda(c, ard, 1, [(COL["negro"], "GND  (−, tierra)"), (COL["rojo"], "+5 V (riel rojo y termistor)"), (COL["amarillo"], "Punto medio del divisor a A0")])
    c.text(c.w_u - 1.2, c.h_u - 1.2, "Del 1 al 5 es lo nuevo. Los rieles se arman como en las Sesiones 7 y 9.", 0.5, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P19_termistor_ntc.png"))
    print("P19 listo")
    for fila in sorted((f for f in circ.table if f[0]), key=lambda t: t[0]):
        print("  ", fila)


def cableado_p19():
    E = Esquema(36, 25.8)
    E.titulo("P19 · Termómetro con termistor NTC", "esquema de conexiones · el mismo divisor del LDR: la resistencia de arriba cambia con la temperatura")
    E.placa(1.5, 5.0, 7.5, 17.5, "Arduino\nUNO R3", [("5V", "5V", 8.5), ("A0", "A0", 14.5), ("GND", "GND", 20.5)])
    E.resistencia_v("NTC", 22.0, 8.5, 14.5, marca="calor")
    E.resistencia_v("RF", 22.0, 14.5, 20.5)
    E.union_interna("NTC.b", "RF.a")
    E.puntos.add("NTC.b")
    E.cable("rojo", "5V", "NTC.a")
    E.cable("amarillo", "A0", "NTC.b")
    E.cable("negro", "GND", "RF.b")
    E.nota(9.5, 7.05, "5 V · cable rojo")
    E.nota(9.5, 13.05, "A0 (entrada) · cable amarillo")
    E.nota(9.5, 19.05, "cable negro")
    E.etiqueta(28.0, 9.0, "Termistor NTC", "10 kΩ a 25 °C", anchor="mm")
    E.etiqueta(27.5, 17.0, "Resistencia", "10 kΩ", anchor="mm")
    E.nota(16.0, 14.5, "punto medio", anchor="rm")
    E.nota(1.5, 24.6, "Con más calor el NTC baja de resistencia: sube el voltaje en A0 y sube la lectura.", color="#8a8a8a")
    E.exigir("5V", "NTC.a", "5 V debe llegar al termistor")
    E.exigir("A0", "NTC.b", "A0 debe llegar al punto medio")
    E.exigir("A0", "RF.a", "A0 debe llegar a la resistencia de 10 kΩ")
    E.exigir("RF.b", "GND", "la resistencia de 10 kΩ debe llegar a GND")
    for a, b in (("5V", "GND"), ("A0", "5V"), ("A0", "GND")):
        E.prohibir(a, b, f"{a} y {b} no pueden tocarse")
    E.dibujar(os.path.join(AQUI, "P19_termistor_ntc_cableado.png"))
    print("P19 cableado listo")


def dibujar_dht11(c, x, y):
    """Módulo DHT11 de 3 pines visto desde arriba. (x, y) = centro del conector de 3 agujeros (de arriba abajo: −, +, S); el módulo va a la derecha."""
    xb = x + 1.6
    c.rect(x - 0.9, y - 1.7, 1.8, 3.4, fill="#1e1e1e", r=0.2)
    for dy, letra in ((-1.0, "−"), (0.0, "+"), (1.0, "S")):
        c.circle(x, y + dy, 0.28, fill="#5a5a5a")
    c.rect(xb, y - 3.2, 8.0, 6.4, fill="#2f7fd1", outline="#1a4f8a", width=0.1, r=0.4)
    c.rect(xb + 2.2, y - 2.4, 4.8, 4.8, fill="#4fb3e8", outline="#2d7aa8", width=0.08, r=0.3)
    for k in range(5):
        c.line([(xb + 2.8, y - 1.6 + k * 0.8), (xb + 6.4, y - 1.6 + k * 0.8)], "#2d7aa8", 0.08, ends=False)
    c.text(xb + 1.0, y - 2.5, "DHT", 0.34, "#ffffff", "Bold")
    for dy, letra in ((-1.0, "−"), (0.0, "+"), (1.0, "S")):
        c.text(xb + 0.5, y + dy, letra, 0.42, "#ffffff", "Bold")
    c.text(xb + 4.0, y + 4.4, "Módulo DHT11", 0.55, TINTA, "Bold")


def _dht11_en_circuito(circ, bb, ard, nuevo):
    """DHT11 con tres cables macho-hembra: 1 GND (−), 2 señal S a A0, 3 5 V (+) al final."""
    s = (lambda n: n) if nuevo else (lambda n: None)
    sx, sy = 40.0, bb.y + 29.4
    circ.modulo("DHT", {"GND": (sx, sy - 1.0), "5V": (sx, sy), "SIG": (sx, sy + 1.0)})
    circ.dibujo(lambda c: dibujar_dht11(c, sx, sy))
    borde = ard.y + ard.H
    circ.wire(("mod", "DHT", "GND"), ("rail", "B", "-", 29), "negro", step=s(1),
              ruta=[(38.5, sy - 1.0), (38.5, bb.y + 21.6), (bb.rail_hole("B", "-", 29)[0], bb.y + 21.6)], badge=(38.5, sy - 3.8))
    circ.wire(("mod", "DHT", "SIG"), ("ard", "A0"), "amarillo", step=s(2),
              ruta=[(36.5, sy + 1.0), (36.5, borde + 2.2), (ard.xy("A0")[0], borde + 2.2)], badge=(31.0, borde + 2.2))
    circ.wire(("mod", "DHT", "5V"), ("rail", "B", "+", 27), "rojo", step=s(3),
              ruta=[(37.5, sy), (37.5, bb.y + 22.8), (bb.rail_hole("B", "+", 27)[0], bb.y + 22.8)], badge=(37.5, sy - 3.2))


def _verificar_dht11(circ):
    circ.exigir(("ard", "A0"), ("mod", "DHT", "SIG"), "A0 debe llegar a la señal del DHT11")
    circ.exigir(("ard", "5V"), ("mod", "DHT", "5V"), "5 V debe llegar a la pata + del DHT11")
    circ.exigir(("ard", "GND"), ("mod", "DHT", "GND"), "GND debe llegar a la pata − del DHT11")
    circ.prohibir(("mod", "DHT", "5V"), ("mod", "DHT", "GND"), "5 V y GND del DHT11 no pueden tocarse")
    circ.prohibir(("ard", "A0"), ("ard", "5V"), "A0 y 5 V no pueden tocarse")
    circ.prohibir(("ard", "A0"), ("ard", "GND"), "A0 y GND no pueden tocarse")
    circ.prohibir(("ard", "5V"), ("ard", "GND"), "5 V y GND no pueden tocarse")


def _ntc_zona_b(circ, bb, ard, nuevo):
    """Termistor en la zona B (A1): NTC en f7 y f9 (9 = 5 V), 10 kΩ de la columna 7 a la 5 (GND). Pasos: 4 a 8."""
    s = (lambda n: n) if nuevo else (lambda n: None)
    circ.sensor2(7, "ntc", step=s(4), nombre="NTCB")
    circ.resistor((7, "h"), (5, "h"), 10000, step=s(5), nombre="RFB")
    circ.wire(("bb", 5, "j"), ("rail", "B", "-", 5), "negro", step=s(6))
    borde = ard.y + ard.H
    xa1 = ard.xy("A1")[0]
    xj7 = bb.hole(7, "j")[0]
    circ.wire(("ard", "A1"), ("bb", 7, "j"), "azul", step=s(7),
              ruta=[(xa1, borde + 0.9), (35.3, borde + 0.9), (35.3, bb.y + 23.4), (xj7, bb.y + 23.4)], badge=(29.0, borde + 0.9))
    circ.wire(("rail", "B", "+", 9), ("bb", 9, "j"), "rojo", step=s(8))


def p20():
    c = Canvas(56, 68)
    c.header("P20 · Temperatura y humedad con el DHT11", "Los tres cables del módulo (pasos 1 a 3) y, para comparar, el termistor en la zona de la izquierda (pasos 4 a 8)")
    bb = Breadboard(3.0, 4.6, cols=30)
    ard = Arduino(bb.x + 2.6, bb.y + bb.H + 6.2)
    circ = Circuit(c, ard, bb)
    _rieles_s9(circ, bb, ard, nuevo=False)
    _dht11_en_circuito(circ, bb, ard, nuevo=True)
    _ntc_zona_b(circ, bb, ard, nuevo=True)
    _verificar_dht11(circ)
    _verificar_ntc(circ, pin="A1", clave="NTCB")
    circ.prohibir(("ard", "A0"), ("ard", "A1"), "A0 y A1 no pueden tocarse")
    circ.draw()
    c.callout(bb.x + 1.4, bb.y + 4.2, ["Termistor y 10 kΩ en la zona B", "(solo para la parte 2: comparar)"], target=(bb.hole(8, "f")[0], bb.hole(7, "f")[1] - 3.3), size=0.54)
    c.callout(41.0, bb.y + 36.0, ["Lee las letras de TU módulo:", "S (señal) · + · −. El orden puede", "ser otro; los cables siguen sus letras"], size=0.5)
    pie_leyenda(c, ard, 2, [(COL["negro"], "GND  (−, tierra)"), (COL["rojo"], "+5 V (rieles, DHT11 y termistor)"), (COL["amarillo"], "Señal del DHT11 a A0 (parte 1)"),
                            (COL["azul"], "Punto medio del termistor a A1 (parte 2)")])
    c.text(c.w_u - 1.2, c.h_u - 1.2, "Parte 1: DHT11 (1 a 3). Parte 2: se agrega el termistor (4 a 8). A0 y A1 son pines distintos para que los dos sensores convivan.", 0.5, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P20_dht11.png"))
    print("P20 listo")
    for fila in sorted((f for f in circ.table if f[0]), key=lambda t: t[0]):
        print("  ", fila)


def cableado_p20():
    E = Esquema(40, 49.0)
    E.titulo("P20 · Temperatura y humedad (y comparar con el termistor)", "esquema de conexiones · el DHT11 entra por A0 y el termistor por A1")
    E.placa(1.5, 5.0, 7.5, 43.0, "Arduino\nUNO R3", [("A0", "A0", 8.5), ("A1", "A1", 28.5), ("5V", "5V", 42.0), ("GND", "GND", 44.5)])
    E.bloque("DH", 22.0, 6.0, 10.0, 11.0, "DHT11", "temperatura y humedad",
             terminales=[("s", "izq", 2.5, "S"), ("vcc", "izq", 6.5, "+"), ("gnd", "izq", 10.5, "−")])
    E.cable("amarillo", "A0", "DH.s")
    E.etiqueta_red("DH.vcc", "5V", "5 V", "rojo")
    E.etiqueta_red("DH.gnd", "GND", "GND", "negro")
    E.resistencia_v("NTC", 22.0, 22.5, 28.5, marca="calor")
    E.resistencia_v("RF", 22.0, 28.5, 34.5)
    E.union_interna("NTC.b", "RF.a")
    E.puntos.add("NTC.b")
    E.cable("azul", "A1", "NTC.b")
    E.etiqueta_red("NTC.a", "5V", "5 V", "rojo")
    E.etiqueta_red("RF.b", "GND", "GND", "negro")
    E.nota(9.8, 7.05, "A0 · cable amarillo", anchor="lm")
    E.nota(9.8, 27.05, "A1 · cable azul", anchor="lm")
    E.etiqueta(28.5, 24.4, "Termistor NTC", None, anchor="lm")
    E.etiqueta(28.5, 31.5, "10 kΩ", None, anchor="lm")
    E.nota(9.8, 40.6, "5 V al riel rojo (+)", anchor="lm", color="#c8202b", negrita=True)
    E.nota(9.8, 43.1, "GND al riel azul (−)", anchor="lm", color="#262626", negrita=True)
    E.exigir("A0", "DH.s", "A0 debe llegar a la señal del DHT11")
    E.exigir("5V", "DH.vcc", "5 V debe llegar al DHT11")
    E.exigir("GND", "DH.gnd", "GND debe llegar al DHT11")
    E.exigir("A1", "NTC.b", "A1 debe llegar al punto medio del termistor")
    E.exigir("A1", "RF.a", "A1 debe llegar a la resistencia de 10 kΩ")
    E.exigir("NTC.a", "5V", "el termistor debe llegar a 5 V")
    E.exigir("RF.b", "GND", "la resistencia de 10 kΩ debe llegar a GND")
    for a, b in (("5V", "GND"), ("A0", "A1"), ("A0", "5V"), ("A1", "5V"), ("A1", "GND"), ("A0", "GND")):
        E.prohibir(a, b, f"{a} y {b} no pueden tocarse")
    E.dibujar(os.path.join(AQUI, "P20_dht11_cableado.png"))
    print("P20 cableado listo")


def termistor_conoce():
    """El NTC: cómo cambia su resistencia con la temperatura (con la ecuación del sketch) y qué lectura da con 10 kΩ."""
    c = Lienzo(74, 46)
    c.header("P19 · Conoce tu termistor NTC", "Una resistencia que BAJA cuando sube la temperatura, y no en línea recta: por eso se usa una ecuación")
    # por fuera
    c.text(10.0, 5.5, "Por fuera", 0.85, TINTA, "Bold")
    c.circle(10.0, 12.0, 2.6, fill="#2b2b2b", outline="#050505", width=0.1)
    c.circle(9.0, 11.0, 0.7, fill="#5a5a5a")
    for dx in (-0.9, 0.9):
        c.line([(10.0 + dx, 14.4), (10.0 + dx, 20.5)], "#b8b8b8", 0.4, ends=True)
    c.text(10.0, 22.0, "2 patas, sin polaridad", 0.55, VINO, "Bold")
    _lista(c, 1.5, 24.8, ["NTC = coeficiente negativo:", "más calor, menos resistencia.", "10 kΩ a 25 °C (la ecuación del", "programa da 10 kΩ a 25 °C).",
                          "El kit trae 2."], 0.5, 1.2, GRIS_T)
    # divisor
    c.text(36.0, 5.5, "En el divisor de voltaje", 0.85, TINTA, "Bold")
    x = 30.0
    c.line([(x, 8.0), (x, 10.0)], "#c8202b", 0.16, ends=False)
    c.text(x + 0.9, 8.2, "5 V", 0.6, "#c8202b", "Bold", anchor="lm")
    S._zig(c, x, 10.0, 15.0)
    c.text(x + 2.4, 12.5, "NTC", 0.7, TINTA, "Bold", anchor="lm")
    c.line([(x, 15.0), (x, 16.0)], TINTA, 0.16, ends=False)
    c.circle(x, 16.0, 0.3, fill=TINTA)
    c.line([(x, 16.0), (x - 4.5, 16.0)], "#c99a00", 0.16, ends=False)
    c.text(x - 5.0, 16.0, "A0", 0.7, TINTA, "Bold", anchor="rm")
    c.line([(x, 16.0), (x, 17.0)], TINTA, 0.16, ends=False)
    S._zig(c, x, 17.0, 22.0)
    c.line([(x, 22.0), (x, 24.0)], "#1d5fd1", 0.16, ends=False)
    c.text(x + 0.9, 23.6, "GND", 0.6, "#1d5fd1", "Bold", anchor="lm")
    c.text(x + 2.4, 19.5, "10 kΩ", 0.7, TINTA, "Bold", anchor="lm")
    _lista(c, 38.5, 9.5, ["Más calor: el NTC baja de", "resistencia, sube el voltaje en A0", "y sube la lectura.", "", "Menos calor: la lectura baja."], 0.52, 1.3, TINTA)
    # curva R(T)
    gx, gy, gw, gh = 53.0, 8.5, 18.0, 12.0
    c.text(gx + gw / 2, 6.6, "Resistencia según la temperatura", 0.62, TINTA, "Bold")
    c.rect(gx, gy, gw, gh, fill="#fbfaf6", outline="#cfc9b8", width=0.08)
    puntos = []
    for T in range(0, 61, 3):
        R = _ntc_R(T) / 1000
        puntos.append((gx + T / 60 * gw, gy + gh - min(R, 35) / 35 * gh))
    c.line(puntos, VINO, 0.2, ends=False)
    for T in (0, 20, 40, 60):
        c.text(gx + T / 60 * gw, gy + gh + 0.9, f"{T} °C", 0.42, GRIS_T, "SemiBold")
    for R in (0, 10, 20, 30):
        c.text(gx - 0.3, gy + gh - R / 35 * gh, f"{R} kΩ", 0.42, GRIS_T, "SemiBold", anchor="rm")
    # tabla
    cols = [("Temperatura", 1.5, 14.0), ("Resistencia del NTC (ecuación del programa)", 15.5, 31.0), ("Lectura en A0 con 10 kΩ", 46.5, 26.0)]
    yt = 33.0
    c.text(1.5, yt - 1.0, "Lo que se espera (calculado con la ecuación del sketch P19: se mide y se calibra con un termómetro)", 0.6, VINO, "Bold", anchor="lm")
    for (t, xx, w) in cols:
        c.rect(xx, yt, w, 1.6, fill=VINO, outline="#ffffff", width=0.05)
        c.text(xx + w / 2, yt + 0.82, t, 0.46, "#ffffff", "Bold")
    for r_, T in enumerate((0, 10, 20, 25, 30, 37, 50)):
        yy = yt + 1.6 + r_ * 1.4
        R = _ntc_R(T)
        adc = round(1023 * 10000 / (10000 + R))
        vals = [f"{T} °C", f"{G._coma(R / 1000, 1)} kΩ", str(adc)]
        for (t, xx, w), v in zip(cols, vals):
            c.rect(xx, yy, w, 1.4, fill="#ffffff", outline="#cfc9b8", width=0.05)
            c.text(xx + 0.5, yy + 0.72, v, 0.48, TINTA, "SemiBold" if xx == 1.5 else "Medium", anchor="lm")
    c.text(c.w_u - 1.0, c.h_u - 0.4, "Lectura = 1023 × 10 kΩ ÷ (10 kΩ + R del NTC). Cerca de 25 °C la lectura cambia unos 11 números por grado.", 0.48, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P19_termistor_conoce.png"))
    print("P19 conoce listo")


def dht11_conoce():
    """El DHT11: un sensor digital que manda 5 datos de 8 bits; comparación con el termistor."""
    c = Lienzo(72, 42)
    c.header("P20 · Conoce tu sensor DHT11", "Un sensor DIGITAL: tiene su propio chip, mide y manda el resultado ya hecho, en números enteros")
    dibujar_dht11(c, 5.0, 11.0)
    c.text(11.0, 18.0, "3 pines: S · + · −", 0.55, VINO, "Bold")
    _lista(c, 1.5, 20.6, ["Hoja del kit (lección 14):", "· 3,3 a 5,5 V", "· temperatura de −20 a 60 °C, ± 2 °C",
                          "· humedad de 5 a 95 %, ± 5 %", "· una sola lectura cada 1 o 2 segundos", "· un solo cable de datos (S)"], 0.5, 1.2, GRIS_T)
    # trama
    c.text(44.0, 5.5, "Qué manda el DHT11: 5 datos de 8 bits (40 bits)", 0.8, TINTA, "Bold")
    byt = [("humedad", "entera", "#d9ecf8"), ("humedad", "decimal", "#eaf4fb"), ("temperatura", "entera", "#fde5cf"), ("temperatura", "decimal", "#fef0e2"), ("suma de", "verificación", "#e6e6e6")]
    ej = ["45", "0", "24", "0", "69"]
    for i, ((a, b, col), v) in enumerate(zip(byt, ej)):
        x = 22.0 + i * 10.0
        c.rect(x, 8.0, 9.4, 6.0, fill=col, outline=TINTA, width=0.1, r=0.4)
        c.text(x + 4.7, 9.6, a, 0.5, TINTA, "Bold")
        c.text(x + 4.7, 10.7, b, 0.5, TINTA, "Bold")
        c.text(x + 4.7, 12.9, v, 0.8, VINO, "Bold")
    c.text(44.0, 15.7, "ejemplo con valores inventados: 45 % de humedad y 24 °C (la suma 45 + 0 + 24 + 0 = 69 comprueba que no hubo errores)", 0.5, GRIS_T, "Medium")
    c.rect(22.0, 18.0, 49.0, 4.2, fill="#1e1e24", r=0.5)
    c.text(46.5, 19.2, "leerDHT11(humedad, temperatura)", 0.8, "#f2f2f2", "MonoBold")
    c.text(46.5, 20.9, "devuelve true si la suma coincide: si no, la lectura se descarta", 0.5, "#c9c9d0", "Medium")
    # comparación
    cols = [("", 1.5, 18.0), ("Termistor NTC (P19)", 19.5, 25.0), ("DHT11 (P20)", 44.5, 26.5)]
    filas = [("Tipo", "analógico: A0 lee voltaje", "digital: manda números"), ("Cómo se obtiene el dato", "con una ecuación (Steinhart-Hart)", "ya viene hecho (función leerDHT11)"),
             ("Resolución", "decimales (el programa da 0,1 °C)", "1 °C y 1 % (enteros)"), ("Precisión (hoja del kit)", "depende de la calibración (AJUSTE_C)", "± 2 °C y ± 5 %"),
             ("Mide además", "solo temperatura", "temperatura y humedad"), ("Ritmo de lectura", "cuando quieras", "una vez cada 1 o 2 s")]
    yt = 25.0
    c.text(1.5, yt - 1.0, "Dos sensores de temperatura de distinto tipo", 0.7, VINO, "Bold", anchor="lm")
    for (t, xx, w) in cols:
        c.rect(xx, yt, w, 1.6, fill=VINO if t else "#ffffff", outline="#ffffff", width=0.05)
        c.text(xx + w / 2, yt + 0.82, t, 0.5, "#ffffff", "Bold")
    for r_, fila in enumerate(filas):
        yy = yt + 1.6 + r_ * 1.5
        for (t, xx, w), v in zip(cols, fila):
            c.rect(xx, yy, w, 1.5, fill="#ffffff", outline="#cfc9b8", width=0.05)
            c.text(xx + 0.5, yy + 0.78, v, 0.46, TINTA, "SemiBold" if xx == 1.5 else "Medium", anchor="lm")
    c.text(c.w_u - 1.0, c.h_u - 0.4, "Ninguno es «la verdad»: se comparan entre sí y con un termómetro de referencia (ver P20, parte 2).", 0.48, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P20_dht11_conoce.png"))
    print("P20 conoce listo")


TODOS = {"P17": [transistor_conoce, p17, cableado_p17],
         "P18": [p18, cableado_p18, zona_muerta],
         "P19": [termistor_conoce, p19, cableado_p19],
         "P20": [dht11_conoce, p20, cableado_p20]}

if __name__ == "__main__":
    pedidos = sys.argv[1:] or list(TODOS)
    for clave in pedidos:
        for f in TODOS[clave]:
            f()
