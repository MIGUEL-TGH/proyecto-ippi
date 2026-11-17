"""Diagramas de las sesiones 11 (pantalla LCD), 12 (ventilador automático) y 13 (campo y agua).

Uso:  python s11_s13.py            (genera todos)
      python s11_s13.py P21 P22    (genera solo los de P21 y P22)
Reutiliza el motor de generar_diagramas.py y los módulos s06_s08.py y s09_s10.py.

La pantalla LCD1602 se enchufa en la FILA a del protoboard (columnas 1 a 16), con el cuerpo de la pantalla sobresaliendo por arriba del
protoboard; los cables salen de la fila e. El orden de los pines del programa (RS 12, E 11, D4 10, D5 9, D6 8, D7 7) sigue el orden
de las patas del LCD para que los cables vayan paralelos y no se crucen.
"""
import math
import os
import sys

from diagrama import Arduino, Breadboard, Canvas, Circuit, COL, GRIS_T, TINTA, VINO, LED_COL
from esquema import Esquema, Lienzo
import generar_diagramas as G
import s06_s08 as S
import s09_s10 as T

AQUI = G.AQUI
_leyenda, _lista, _caja_aviso, _flecha, _led_cuerpo = G._leyenda, G._lista, G._caja_aviso, G._flecha, G._led_cuerpo
pie_leyenda = S.pie_leyenda
GOLD_BORDE = G.GOLD_BORDE

COL_LCD = 1                      # columna de la pata 1 (VSS)
PINES_LCD = ["VSS", "VDD", "V0", "RS", "RW", "E", "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "A", "K"]
# pin de la placa de cada señal del LCD, en el orden de las patas del LCD
SENALES_LCD = [("RS", 4, "D12", "azul"), ("E", 6, "D11", "verde"), ("D4", 11, "D10", "cafe"), ("D5", 12, "D9", "morado"), ("D6", 13, "D8", "naranja"), ("D7", 14, "D7", "gris")]


# ====================================================================== SESIÓN 11
def dibujar_lcd(c, bb, col1, step=None):
    """LCD1602 visto desde arriba: placa de 80 x 36 mm que sobresale por arriba del protoboard; sus 16 patas entran en la fila a."""
    x1, ya = bb.hole(col1, "a")
    w, h = 31.5, 14.2
    x0 = x1 - 2.95
    yb = ya - 0.9
    y0 = yb - h
    c.rect(x0, y0, w, h, fill="#1f6b46", outline="#0f3d27", width=0.1, r=0.4)
    vx, vy = x0 + (w - 25.4) / 2, y0 + 2.4
    c.rect(vx, vy, 25.4, 5.8, fill="#2a62d6", outline="#173a82", width=0.08, r=0.3)
    for r in range(2):
        for k in range(16):
            c.rect(vx + 0.6 + k * 1.5, vy + 0.6 + r * 2.5, 1.1, 1.9, fill="#1b49a8")
    for k, nombre in enumerate(PINES_LCD):
        xx = x1 + k
        c.rect(xx - 0.15, yb - 0.5, 0.3, 1.7, fill="#c9a227")
        c.vtext(xx, yb - 0.7, nombre, 0.4, "#ffffff", "Bold", down=False)
    c.text(x0 + w - 4.0, y0 + 0.9, "LCD1602", 0.5, "#cfe9d9", "Bold")
    if step:
        c.badge(x0 - 1.0, yb - 1.0, step)


def _lcd_en_circuito(circ, bb, ard, nuevo):
    """LCD enchufado y todos sus cables. Pasos: 1 LCD, 2 VSS, 3 RW, 4 K (a GND), 5 VDD (a 5 V), 6 resistencia de 100 Ω, 7 cable rojo de la luz de fondo,
    8 potenciómetro del contraste, 9 y 10 sus extremos, 11 cable de V0 al centro, 12 a 17 las seis señales (RS, E, D4, D5, D6, D7)."""
    s = (lambda n: n) if nuevo else (lambda n: None)
    col = COL_LCD
    for k in range(16):
        circ._occupy(("bb", col + k, "a"), "LCD")
    circ.elems["LCD"] = {nombre: ("bb", col + k, "a") for k, nombre in enumerate(PINES_LCD)}
    circ.dibujo(lambda c: dibujar_lcd(c, bb, col, s(1)))
    circ.wire(("bb", 1, "e"), ("rail", "B", "-", 1), "negro", step=s(2))                  # VSS
    circ.wire(("bb", 5, "e"), ("rail", "B", "-", 5), "negro", step=s(3))                  # RW
    circ.wire(("bb", 16, "e"), ("rail", "B", "-", 16), "negro", step=s(4))                # K
    circ.wire(("bb", 2, "e"), ("rail", "B", "+", 2), "rojo", step=s(5))                   # VDD
    circ.resistor((15, "d"), (19, "d"), 100, step=s(6), nombre="RA")                      # A -> 100 Ω
    circ.wire(("bb", 19, "e"), ("rail", "B", "+", 19), "rojo", step=s(7))
    # potenciómetro del contraste en la zona de la derecha
    circ.potenciometro(26, step=s(8), nombre="POT")
    circ.wire(("bb", 26, "j"), ("rail", "B", "-", 26), "negro", step=s(9))
    circ.wire(("rail", "B", "+", 29), ("bb", 30, "j"), "rojo", step=s(10))
    xb, yb_ = bb.hole(3, "b")
    xg, yg = bb.hole(28, "g")
    circ.wire(("bb", 3, "b"), ("bb", 28, "g"), "rosa", step=s(11), ruta=[(28.0, yb_), (28.0, yg)], badge=(18.0, yb_))
    # señales
    borde = ard.y + ard.H
    orden_prof = {"D7": 0, "D6": 1, "D5": 2, "D4": 3, "E": 4, "RS": 5}          # la de más a la derecha, la más arriba
    for n, (nombre, colu, pin, color) in enumerate(SENALES_LCD):
        yk = bb.y + 21.5 + 0.95 * orden_prof[nombre]
        xc = bb.hole(colu, "e")[0]
        circ.wire(("bb", colu, "e"), ("ard", pin), color, step=s(12 + n), ruta=[(xc, yk), (ard.xy(pin)[0], yk)],
                  badge=(xc, bb.y + 18.5 + 0.0 * n))
    # rieles: el GND sale de los pines de abajo y rodea la placa por la derecha; el 5 V, por la izquierda
    xg5 = ard.xy("GND_5")[0]
    circ.wire(("ard", "GND_5"), ("rail", "B", "-", 29), "negro",
              ruta=[(xg5, borde + 1.4), (36.2, borde + 1.4), (36.2, bb.y + 21.4), (bb.rail_hole("B", "-", 29)[0], bb.y + 21.4)])
    x5 = ard.xy("5V")[0]
    circ.wire(("ard", "5V"), ("rail", "B", "+", 3), "rojo",
              ruta=[(x5, borde + 2.0), (1.8, borde + 2.0), (1.8, bb.y + 21.4), (bb.rail_hole("B", "+", 3)[0], bb.y + 21.4)])


def _verificar_lcd(circ):
    L = circ.elems["LCD"]
    circ.exigir(L["VSS"], ("ard", "GND"), "VSS debe llegar a GND")
    circ.exigir(L["RW"], ("ard", "GND"), "RW debe llegar a GND")
    circ.exigir(L["K"], ("ard", "GND"), "K debe llegar a GND")
    circ.exigir(L["VDD"], ("ard", "5V"), "VDD debe llegar a 5 V")
    ra_a, ra_b = circ.elems["RA"]
    circ.exigir(L["A"], ra_a, "A debe llegar a la resistencia de 100 Ω")
    circ.exigir(ra_b, ("ard", "5V"), "la resistencia de 100 Ω debe llegar a 5 V")
    circ.prohibir(L["A"], ("ard", "5V"), "A no puede llegar a 5 V sin pasar por la resistencia de 100 Ω")
    a, w, b = circ.elems["POT"]
    circ.exigir(L["V0"], w, "V0 debe llegar al centro del potenciómetro")
    circ.exigir(a, ("ard", "GND"), "un extremo del potenciómetro debe llegar a GND")
    circ.exigir(b, ("ard", "5V"), "el otro extremo del potenciómetro debe llegar a 5 V")
    circ.prohibir(w, ("ard", "5V"), "el centro no puede estar unido a 5 V")
    circ.prohibir(w, ("ard", "GND"), "el centro no puede estar unido a GND")
    circ.prohibir(a, b, "los extremos del potenciómetro no pueden estar unidos")
    for nombre, colu, pin, color in SENALES_LCD:
        circ.exigir(L[nombre], ("ard", pin), f"{nombre} debe llegar al pin {pin[1:]}")
        circ.prohibir(L[nombre], ("ard", "GND"), f"{nombre} no puede estar unido a GND")
        circ.prohibir(L[nombre], ("ard", "5V"), f"{nombre} no puede estar unido a 5 V")
    circ.prohibir(("ard", "5V"), ("ard", "GND"), "5 V y GND no pueden tocarse")
    circ.prohibir(("ard", "D12"), ("ard", "D11"), "los pines 12 y 11 no pueden tocarse")


def p21():
    c = Canvas(40.5, 80.0)
    c.header("P21 · Pantalla LCD: primer mensaje", "La pantalla se enchufa en la fila a (arriba); los cables salen de la fila e (vista desde arriba)")
    bb = Breadboard(3.0, 15.0, cols=30)
    ard = Arduino(bb.x + 2.6, bb.y + bb.H + 6.2)
    circ = Circuit(c, ard, bb)
    _lcd_en_circuito(circ, bb, ard, nuevo=True)
    _verificar_lcd(circ)
    circ.draw()
    c.callout(bb.x + 22.0, bb.y + 5.0, ["Contraste: gira el", "centro del potenciómetro"], target=(bb.hole(29, "f")[0] - 1.0, bb.hole(28, "f")[1] - 3.6), size=0.5)
    pie_leyenda(c, ard, 1, [(COL["negro"], "GND  (−, tierra)"), (COL["rojo"], "+5 V"), (COL["rosa"], "V0: contraste (centro del potenciómetro)"),
                            (COL["azul"], "RS: pin 12"), (COL["verde"], "E: pin 11"), (COL["cafe"], "D4: pin 10"), (COL["morado"], "D5: pin 9"),
                            (COL["naranja"], "D6: pin 8"), (COL["gris"], "D7: pin 7")])
    c.text(c.w_u - 1.2, c.h_u - 1.2, "Del 1 al 17: la pantalla, GND y 5 V, la luz de fondo, el contraste y las 6 señales. Cada cable sale de la columna de la pata de su misma letra.", 0.5, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P21_lcd_hola.png"))
    print("P21 listo")
    for fila in sorted((f for f in circ.table if f[0]), key=lambda t: t[0]):
        print("  ", fila)


def _esq_lcd(E):
    """El LCD del esquema (bloque con 12 terminales) y todos sus cables; los pines de la placa deben estar en las alturas indicadas."""
    E.bloque("LCD", 22.0, 6.0, 12.0, 26.0, "LCD1602", "16 × 2",
             terminales=[("vss", "izq", 2.0, "VSS"), ("vdd", "izq", 4.0, "VDD"), ("rs", "izq", 8.0, "RS"), ("rw", "izq", 10.0, "RW"), ("e", "izq", 12.0, "E"),
                         ("d4", "izq", 14.0, "D4"), ("d5", "izq", 16.0, "D5"), ("d6", "izq", 18.0, "D6"), ("d7", "izq", 20.0, "D7"),
                         ("a", "izq", 22.0, "A"), ("k", "izq", 24.0, "K"), ("v0", "der", 12.0, "V0")])
    E.cable("azul", "D12", "LCD.rs")
    E.cable("verde", "D11", "LCD.e")
    E.cable("cafe", "D10", "LCD.d4")
    E.cable("morado", "D9", "LCD.d5")
    E.cable("naranja", "D8", "LCD.d6")
    E.cable("gris", "D7", "LCD.d7")
    for t in ("vss", "rw", "k"):
        E.etiqueta_red("LCD." + t, "GND", "GND", "negro")
    E.etiqueta_red("LCD.vdd", "5V", "5 V", "rojo")
    E.resistencia("RA", 14.0, 28.0, "100 Ω")
    E.etiqueta_red("RA.a", "5V", "5 V", "rojo")
    E.cable("rojo", "RA.b", "LCD.a")
    E.potenciometro("P", 41.0, 12.0, 24.0)
    E.etiqueta_red("P.a", "5V", "5 V", "rojo", lado="der", largo=3.0)
    E.etiqueta_red("P.b", "GND", "GND", "negro", lado="der", largo=3.0)
    E.cable("rosa", "LCD.v0", "P.w")
    E.nota(9.5, 12.55, "pin 12 · RS", anchor="lm")
    E.nota(9.5, 16.55, "pin 11 · E", anchor="lm")
    E.nota(9.5, 19.4, "pin 10 · D4", anchor="lm")
    E.nota(9.5, 21.4, "pin 9 · D5", anchor="lm")
    E.nota(9.5, 23.4, "pin 8 · D6", anchor="lm")
    E.nota(9.5, 25.4, "pin 7 · D7", anchor="lm")
    E.nota(38.5, 9.6, "contraste", anchor="mm", color="#8a8a8a")
    E.nota(15.0, 26.4, "luz de fondo", anchor="mm", color="#8a8a8a")


def _esq_lcd_verificar(E):
    for t, pin in (("rs", "D12"), ("e", "D11"), ("d4", "D10"), ("d5", "D9"), ("d6", "D8"), ("d7", "D7")):
        E.exigir(pin, "LCD." + t, f"el pin {pin[1:]} debe llegar a su pata del LCD")
    for t in ("vss", "rw", "k"):
        E.exigir("LCD." + t, "GND", f"{t.upper()} debe llegar a GND")
    E.exigir("LCD.vdd", "5V", "VDD debe llegar a 5 V")
    E.exigir("RA.a", "5V", "la resistencia de 100 Ω debe llegar a 5 V")
    E.exigir("RA.b", "LCD.a", "la resistencia de 100 Ω debe llegar a la pata A")
    E.exigir("LCD.v0", "P.w", "V0 debe llegar al centro del potenciómetro")
    E.exigir("P.a", "5V", "un extremo del potenciómetro debe llegar a 5 V")
    E.exigir("P.b", "GND", "el otro extremo del potenciómetro debe llegar a GND")
    for a, b in (("5V", "GND"), ("D12", "D11"), ("D10", "D9"), ("D8", "D7"), ("D12", "GND"), ("D7", "5V")):
        E.prohibir(a, b, f"{a} y {b} no pueden tocarse")


def cableado_p21():
    E = Esquema(48, 41.0)
    E.titulo("P21 · Pantalla LCD: primer mensaje", "esquema de conexiones · seis señales de datos, la alimentación y el contraste")
    E.placa(1.5, 5.0, 7.5, 33.0, "Arduino\nUNO R3", [("D12", "D12", 14.0), ("D11", "D11", 18.0), ("D10", "D10", 20.0), ("D9", "D9", 22.0),
                                                    ("D8", "D8", 24.0), ("D7", "D7", 26.0), ("5V", "5V", 33.0), ("GND", "GND", 35.5)])
    _esq_lcd(E)
    E.nota(9.8, 31.6, "5 V al riel rojo (+)", anchor="lm", color="#c8202b", negrita=True)
    E.nota(9.8, 34.1, "GND al riel azul (−)", anchor="lm", color="#262626", negrita=True)
    E.nota(1.5, 39.8, "El LCD solo recibe 4 bits de datos a la vez (D4 a D7): por eso hay 6 señales y no 11.", color="#8a8a8a")
    _esq_lcd_verificar(E)
    E.dibujar(os.path.join(AQUI, "P21_lcd_hola_cableado.png"))
    print("P21 cableado listo")


def p22():
    c = Canvas(58.0, 80.0)
    c.header("P22 · Estación de clima", "Sobre la pantalla de P21, el módulo DHT11 con tres cables macho-hembra (vista desde arriba)")
    bb = Breadboard(3.0, 15.0, cols=30)
    ard = Arduino(bb.x + 2.6, bb.y + bb.H + 6.2)
    circ = Circuit(c, ard, bb)
    _lcd_en_circuito(circ, bb, ard, nuevo=False)
    sx, sy = 41.0, bb.y + 29.4
    circ.modulo("DHT", {"GND": (sx, sy - 1.0), "5V": (sx, sy), "SIG": (sx, sy + 1.0)})
    circ.dibujo(lambda cc: T.dibujar_dht11(cc, sx, sy))
    borde = ard.y + ard.H
    circ.wire(("mod", "DHT", "GND"), ("rail", "B", "-", 27), "negro", step=1,
              ruta=[(39.2, sy - 1.0), (39.2, bb.y + 22.8), (bb.rail_hole("B", "-", 27)[0], bb.y + 22.8)], badge=(39.2, sy - 3.8))
    circ.wire(("mod", "DHT", "SIG"), ("ard", "A0"), "amarillo", step=2,
              ruta=[(37.6, sy + 1.0), (37.6, borde + 2.8), (ard.xy("A0")[0], borde + 2.8)], badge=(31.0, borde + 2.8))
    circ.wire(("mod", "DHT", "5V"), ("rail", "B", "+", 26), "rojo", step=3,
              ruta=[(38.4, sy), (38.4, bb.y + 24.0), (bb.rail_hole("B", "+", 26)[0], bb.y + 24.0)], badge=(38.4, sy - 3.2))
    _verificar_lcd(circ)
    T._verificar_dht11(circ)
    circ.draw()
    c.callout(41.5, bb.y + 36.0, ["Lee las letras de TU módulo:", "S (señal) · + · −. Los cables", "siguen sus letras"], size=0.5)
    c.callout(bb.x + 22.0, bb.y + 5.0, ["Pantalla y contraste:", "ya armados en P21"], target=(bb.hole(29, "f")[0] - 1.0, bb.hole(28, "f")[1] - 3.6), size=0.5)
    pie_leyenda(c, ard, 2, [(COL["negro"], "GND  (−, tierra)"), (COL["rojo"], "+5 V"), (COL["rosa"], "V0: contraste"), (COL["amarillo"], "Señal del DHT11 a A0 (nuevo)"),
                            (COL["azul"], "RS pin 12 · E pin 11 (verde) · D4 a D7: pines 10 a 7 (ya están)")])
    c.text(c.w_u - 1.2, c.h_u - 1.2, "Los números 1 a 3 son lo nuevo: el DHT11, con el 5 V al final. La pantalla ya está como en P21.", 0.5, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P22_estacion_clima.png"))
    print("P22 listo")


def cableado_p22():
    E = Esquema(48, 53.0)
    E.titulo("P22 · Estación de clima", "esquema de conexiones · la pantalla muestra lo que lee el DHT11 por A0")
    E.placa(1.5, 5.0, 7.5, 45.0, "Arduino\nUNO R3", [("D12", "D12", 14.0), ("D11", "D11", 18.0), ("D10", "D10", 20.0), ("D9", "D9", 22.0), ("D8", "D8", 24.0),
                                                    ("D7", "D7", 26.0), ("A0", "A0", 38.0), ("5V", "5V", 45.0), ("GND", "GND", 47.5)])
    _esq_lcd(E)
    E.bloque("DH", 22.0, 35.0, 12.0, 9.0, "DHT11", "temperatura y humedad",
             terminales=[("s", "izq", 3.0, "S"), ("vcc", "izq", 5.5, "+"), ("gnd", "izq", 7.5, "−")])
    E.cable("amarillo", "A0", "DH.s")
    E.etiqueta_red("DH.vcc", "5V", "5 V", "rojo")
    E.etiqueta_red("DH.gnd", "GND", "GND", "negro")
    E.nota(9.8, 36.6, "A0 · cable amarillo", anchor="lm")
    E.nota(9.8, 43.6, "5 V al riel rojo (+)", anchor="lm", color="#c8202b", negrita=True)
    E.nota(9.8, 46.1, "GND al riel azul (−)", anchor="lm", color="#262626", negrita=True)
    _esq_lcd_verificar(E)
    E.exigir("A0", "DH.s", "A0 debe llegar a la señal del DHT11")
    E.exigir("DH.vcc", "5V", "el DHT11 debe llegar a 5 V")
    E.exigir("DH.gnd", "GND", "el DHT11 debe llegar a GND")
    E.prohibir("A0", "5V", "A0 y 5V no pueden tocarse")
    E.prohibir("A0", "GND", "A0 y GND no pueden tocarse")
    E.dibujar(os.path.join(AQUI, "P22_estacion_clima_cableado.png"))
    print("P22 cableado listo")


def lcd_conoce():
    """El LCD1602: sus 16 pines, cómo se conecta aquí, el modo de 4 bits, el contraste y la luz de fondo."""
    c = Lienzo(78, 46)
    c.header("P21 · Conoce tu pantalla LCD1602", "16 columnas por 2 filas; con solo 4 cables de datos se le puede escribir cualquier letra")
    x0, y0 = 2.0, 6.0
    c.rect(x0, y0, 31.5, 13.0, fill="#1f6b46", outline="#0f3d27", width=0.1, r=0.4)
    c.rect(x0 + 3.0, y0 + 2.0, 25.4, 6.4, fill="#2a62d6", outline="#173a82", width=0.08, r=0.3)
    for r in range(2):
        for k in range(16):
            c.rect(x0 + 3.6 + k * 1.5, y0 + 2.7 + r * 2.8, 1.1, 2.0, fill="#1b49a8")
    c.text(x0 + 15.7, y0 + 11.3, "16 columnas × 2 filas", 0.55, "#cfe9d9", "Bold")
    for k, nombre in enumerate(PINES_LCD):
        xx = x0 + 4.2 + k * 1.4
        c.rect(xx - 0.15, y0 + 13.0, 0.3, 1.6, fill="#c9a227")
        c.text(xx, y0 + 15.2, str(k + 1), 0.36, GRIS_T, "SemiBold")
    c.text(x0 + 15.7, y0 - 1.0, "Pines 1 a 16 (de izquierda a derecha)", 0.5, GRIS_T, "SemiBold")
    # tabla de pines
    cols = [("Pin", 1.5, 5.0), ("Nombre", 6.5, 5.5), ("Qué hace", 12.0, 17.0), ("Va a…", 29.0, 14.0)]
    filas = [("1", "VSS", "tierra", "GND"), ("2", "VDD", "alimentación", "5 V"), ("3", "V0", "contraste", "centro del potenciómetro"), ("4", "RS", "datos o comando", "pin 12"),
             ("5", "RW", "solo escribir", "GND"), ("6", "E", "«ya puedes leer»", "pin 11"), ("7 a 10", "D0 a D3", "no se usan", "—"),
             ("11", "D4", "dato bit 4", "pin 10"), ("12", "D5", "dato bit 5", "pin 9"), ("13", "D6", "dato bit 6", "pin 8"),
             ("14", "D7", "dato bit 7", "pin 7"), ("15", "A", "luz de fondo (+)", "100 Ω a 5 V"), ("16", "K", "luz de fondo (−)", "GND")]
    yt = 24.0
    for (t, xx, w) in cols:
        c.rect(xx, yt, w, 1.4, fill=VINO, outline="#ffffff", width=0.05)
        c.text(xx + w / 2, yt + 0.72, t, 0.46, "#ffffff", "Bold")
    for r_, fila in enumerate(filas):
        yy = yt + 1.4 + r_ * 1.15
        for (t, xx, w), v in zip(cols, fila):
            c.rect(xx, yy, w, 1.15, fill="#ffffff" if r_ % 2 == 0 else "#fbf8f0", outline="#cfc9b8", width=0.05)
            c.text(xx + 0.4, yy + 0.6, v, 0.42, TINTA, "SemiBold" if xx < 12 else "Medium", anchor="lm")
    # explicaciones a la derecha
    xr = 47.0
    c.text(xr, 5.5, "Cómo se escribe en la pantalla", 0.8, TINTA, "Bold", anchor="lm")
    c.text(xr, 7.6, "lcd.setCursor(columna, fila)", 0.62, VINO, "MonoBold", anchor="lm")
    c.text(xr, 8.9, "Las columnas van de 0 a 15 y las filas de 0 a 1:", 0.5, GRIS_T, "Medium", anchor="lm")
    for r in range(2):
        for k in range(16):
            c.rect(xr + k * 1.9, 10.0 + r * 2.4, 1.7, 2.2, fill="#2a62d6" if (r, k) != (1, 3) else "#f2b705", outline="#173a82", width=0.04)
    c.text(xr + 3 * 1.9 + 0.85, 14.7, "setCursor(3, 1)", 0.5, "#8a6a00", "MonoBold")
    _lista(c, xr, 16.3, ["· La pantalla no muestra acentos ni ñ.", "· Cada print() escribe desde el cursor.", "· Para borrar restos se escriben espacios (\"   \")."], 0.5, 1.25, TINTA)
    c.text(xr, 21.4, "Contraste (pin V0)", 0.7, TINTA, "Bold", anchor="lm")
    _lista(c, xr, 23.0, ["La hoja de datos pide VDD − V0 de unos 4,5 V:", "o sea, V0 de unos 0,5 V (cerca de GND).", "· Pantalla vacía: V0 demasiado alto.",
                          "· Cuadros negros en la fila 1: V0 demasiado bajo."], 0.5, 1.25, TINTA)
    c.text(xr, 28.8, "Luz de fondo (pines A y K)", 0.7, TINTA, "Bold", anchor="lm")
    _lista(c, xr, 30.4, ["Su LED cae unos 4,2 V y la hoja da 110 mA de", "referencia: sin resistencia, con 5 V sería mucha corriente.", "Con 100 Ω: (5 − 4,2) ÷ 100 ≈ 8 mA (más tenue,",
                          "pero segura). Se mide con el multímetro (V10)."], 0.5, 1.25, TINTA)
    _caja_aviso(c, 1.5, 40.8, 75.0, 4.2, "Por qué solo 4 bits de datos",
                ["La pantalla puede recibir 8 bits (D0 a D7), pero también acepta cada letra en dos tandas de 4 bits (D4 a D7). La librería LiquidCrystal hace el trabajo: con 4 cables basta."], 0.5)
    c.save(os.path.join(AQUI, "P21_lcd_conoce.png"))
    print("P21 conoce listo")


# ====================================================================== SESIÓN 12
# El protoboard se usa con 46 columnas (como el MB-102 completo). A la izquierda queda lo de la Sesión 11 (pantalla y contraste); a la derecha, lo nuevo.
# Si los rieles del protoboard se dividen a la mitad, se unen con un cable en cada riel (los «puentes»).
def _s12_circuito(circ, bb, ard, nuevo):
    """Pantalla (S11, sin números) y, nuevo: 1-4 LED del ventilador en el pin 5; 5-8 perilla del límite (A1); 9-13 termistor (A0); 14-15 puentes de los rieles."""
    s = (lambda n: n) if nuevo else (lambda n: None)
    _lcd_en_circuito(circ, bb, ard, nuevo=False)
    borde = ard.y + ard.H
    # puentes de los rieles
    circ.wire(("rail", "B", "-", 28), ("rail", "B", "-", 34), "negro", step=s(14),
              ruta=[(bb.rail_hole("B", "-", 28)[0], bb.y + 21.2), (bb.rail_hole("B", "-", 34)[0], bb.y + 21.2)], badge=(bb.rail_hole("B", "-", 31)[0], bb.y + 21.2))
    circ.wire(("rail", "B", "+", 28), ("rail", "B", "+", 34), "rojo", step=s(15),
              ruta=[(bb.rail_hole("B", "+", 28)[0], bb.y + 24.8), (bb.rail_hole("B", "+", 34)[0], bb.y + 24.8)], badge=(bb.rail_hole("B", "+", 31)[0], bb.y + 24.8))
    # ventilador (LED) en el pin 5: columnas 20 a 25
    circ.led(anodo=(21, "g"), catodo=(20, "g"), color="rojo", step=s(1), nombre="LEDV")
    circ.resistor((25, "h"), (21, "h"), 220, step=s(2), nombre="RV")
    circ.wire(("bb", 20, "j"), ("rail", "B", "-", 20), "negro", step=s(3))
    circ.wire(("ard", "D5"), ("bb", 25, "j"), "lima", step=s(4), badge=(26.6, bb.y + 24.2))
    # perilla del límite (zona C): GND en la columna 33, centro (A1) en la 35, 5 V en la 37
    circ.potenciometro(33, step=s(5), nombre="POTL")
    circ.wire(("bb", 33, "j"), ("rail", "B", "-", 33), "negro", step=s(6))
    circ.wire(("rail", "B", "+", 37), ("bb", 37, "j"), "rojo", step=s(7))
    xa1 = ard.xy("A1")[0]
    xj35 = bb.hole(35, "j")[0]
    circ.wire(("ard", "A1"), ("bb", 35, "j"), "celeste", step=s(8), ruta=[(xa1, borde + 0.9), (xj35, borde + 0.9)], badge=(31.0, borde + 0.9))
    # termistor (zona D): 10 kΩ de la columna 42 a la 39 (GND), NTC en f42 y f44 (44 = 5 V)
    circ.sensor2(42, "ntc", step=s(9), nombre="NTC")
    circ.resistor((42, "h"), (39, "h"), 10000, step=s(10), nombre="RF")
    circ.wire(("bb", 39, "j"), ("rail", "B", "-", 39), "negro", step=s(11))
    circ.wire(("rail", "B", "+", 44), ("bb", 44, "j"), "rojo", step=s(12))
    xa0 = ard.xy("A0")[0]
    xj42 = bb.hole(42, "j")[0]
    circ.wire(("ard", "A0"), ("bb", 42, "j"), "amarillo", step=s(13), ruta=[(xa0, borde + 2.2), (xj42, borde + 2.2)], badge=(30.0, borde + 2.2))


def _s12_verificar(circ):
    _verificar_lcd(circ)
    l_a, l_k = circ.elems["LEDV"]
    r_a, r_b = circ.elems["RV"]
    circ.exigir(l_k, ("ard", "GND"), "la pata corta del LED debe llegar a GND")
    circ.exigir(l_a, r_b, "la pata larga del LED debe llegar a la resistencia")
    circ.exigir(("ard", "D5"), r_a, "el pin 5 debe llegar a la resistencia del LED")
    circ.prohibir(("ard", "D5"), l_k, "el pin 5 no debe llegar a la pata corta sin pasar por el LED")
    a, w, b = circ.elems["POTL"]
    circ.exigir(a, ("ard", "GND"), "un extremo de la perilla debe llegar a GND")
    circ.exigir(w, ("ard", "A1"), "el centro de la perilla debe llegar a A1")
    circ.exigir(b, ("ard", "5V"), "el otro extremo de la perilla debe llegar a 5 V")
    circ.prohibir(w, ("ard", "5V"), "el centro de la perilla no puede estar unido a 5 V")
    circ.prohibir(w, ("ard", "GND"), "el centro de la perilla no puede estar unido a GND")
    n_m, n_5 = circ.elems["NTC"]
    r_m, r_g = circ.elems["RF"]
    circ.exigir(("ard", "5V"), n_5, "el 5 V debe llegar al termistor")
    circ.exigir(("ard", "A0"), n_m, "A0 debe llegar al punto medio del termistor")
    circ.exigir(("ard", "A0"), r_m, "A0 debe llegar a la resistencia de 10 kΩ")
    circ.exigir(r_g, ("ard", "GND"), "la resistencia de 10 kΩ debe llegar a GND")
    circ.prohibir(n_5, n_m, "las patas del termistor no pueden estar unidas")
    for a_, b_ in (("A0", "A1"), ("A0", "5V"), ("A1", "5V"), ("A0", "GND"), ("A1", "GND"), ("D5", "A0"), ("D5", "A1")):
        circ.prohibir(("ard", a_), ("ard", b_), f"{a_} y {b_} no pueden tocarse")


def p23():
    c = Canvas(58.0, 82.0)
    c.header("P23 · Ventilador automático (termostato con pantalla)", "Sobre la pantalla de P21: el LED del «ventilador», la perilla del límite y el termistor, a la derecha (vista desde arriba)")
    bb = Breadboard(3.0, 15.0, cols=46)
    ard = Arduino(bb.x + 2.6, bb.y + bb.H + 6.2)
    circ = Circuit(c, ard, bb)
    _s12_circuito(circ, bb, ard, nuevo=True)
    _s12_verificar(circ)
    circ.draw()
    # Las tres etiquetas van en el espacio blanco de arriba, a la derecha de la pantalla (así no tapan la resistencia de la luz de fondo, los cables
    # de la pantalla, las perillas ni el termistor). Las guías son verticales y bajan entre dos columnas (a media posición) para no tapar números
    # de columna ni insignias. La de la pantalla tiene dos guías: una a la pantalla y otra a la perilla del contraste.
    sz = 0.5
    t_a, t_b, t_c = ["Pantalla y contraste:", "ya armados (Sesión 11)"], ["Perilla del límite:", "el centro va a A1"], ["Termistor y 10 kΩ:", "el punto medio va a A0"]
    bw_a, bh = S.medida_etiqueta(c, t_a, sz)
    y_a, y_bc = bb.y - 6.0, bb.y - 3.0                                   # la A, un piso más arriba para que no choque con la B
    x_lcd = bb.hole(COL_LCD, "a")[0] - 2.95 + 31.5                       # borde derecho de la placa de la pantalla
    x_a = x_lcd + 0.4

    def borde_perilla(col_centro, x):                                    # y del borde de arriba de la perilla en la vertical x (esquinas redondeadas de 1.4 U)
        xc, yf = bb.hole(col_centro, "f")
        r = 1.4
        dx = max(abs(x - xc) - (2.95 - r), 0.0)
        return yf + 0.85 - 5.5 + r - math.sqrt(max(r * r - dx * dx, 0.0))

    xg_a = bb.hole(30, "a")[0] + 0.5                                     # entre las columnas 30 y 31 → perilla del contraste (columna central 28)
    S.etiqueta_guias(c, x_a, y_a, t_a, [(x_a + 0.1, y_a + bh / 2, x_lcd - 0.5, y_a + bh / 2),
                                        (xg_a, y_a + bh - 0.1, xg_a, borde_perilla(28, xg_a) + 0.4)], sz)
    xg_b = bb.hole(36, "a")[0] + 0.5                                     # entre las columnas 36 y 37 → perilla del límite (columna central 35)
    S.etiqueta_guias(c, xg_b - 2.1, y_bc, t_b, [(xg_b, y_bc + bh - 0.1, xg_b, borde_perilla(35, xg_b) + 0.5)], sz)
    xg_c = bb.hole(44, "a")[0] + 0.5                                     # entre las columnas 44 y 45 → al lado del termistor
    S.etiqueta_guias(c, xg_c - 2.5, y_bc, t_c, [(xg_c, y_bc + bh - 0.1, xg_c, bb.hole(43, "f")[1] - 1.7)], sz)
    pie_leyenda(c, ard, 2, [(COL["negro"], "GND  (−, tierra)"), (COL["rojo"], "+5 V"), (COL["lima"], "Pin 5: el «ventilador» (LED)"), (COL["celeste"], "Centro de la perilla a A1"),
                            (COL["amarillo"], "Punto medio del termistor a A0"), (COL["rosa"], "V0 (contraste) y las 6 señales de la pantalla: ya están")])
    c.text(c.w_u - 1.2, c.h_u - 1.2, "Los números 14 y 15 son los puentes de los rieles: solo si tus rieles están divididos a la mitad (pruébalo con el multímetro o con un LED).", 0.5, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P23_ventilador_automatico.png"))
    print("P23 listo")
    for fila in sorted((f for f in circ.table if f[0]), key=lambda t: t[0]):
        print("  ", fila)


def cableado_p23():
    E = Esquema(56, 66.0)
    E.titulo("P23 · Ventilador automático (termostato con pantalla)", "esquema de conexiones · medir con el termistor, comparar con la perilla y actuar sobre el LED")
    E.placa(1.5, 5.0, 7.5, 59.0, "Arduino\nUNO R3", [("D12", "D12", 14.0), ("D11", "D11", 18.0), ("D10", "D10", 20.0), ("D9", "D9", 22.0), ("D8", "D8", 24.0), ("D7", "D7", 26.0),
                                                    ("D5", "D5", 33.0), ("A0", "A0", 41.0), ("A1", "A1", 52.0), ("5V", "5V", 60.0), ("GND", "GND", 62.5)])
    _esq_lcd(E)
    # ventilador (LED)
    E.resistencia("RV", 14.0, 33.0, "220 Ω")
    E.led("LEDV", 23.0, 33.0, "rojo")
    E.cable("lima", "D5", "RV.a")
    E.cable("lima", "RV.b", "LEDV.a")
    E.etiqueta_red("LEDV.k", "GND", "GND", "negro", lado="der")
    E.nota(9.5, 31.55, "pin 5 · «ventilador»")
    E.nota(27.0, 34.9, "hoy un LED; luego el motor", anchor="lm", color="#8a8a8a")
    # termistor
    E.resistencia_v("NTC", 22.0, 35.0, 41.0, marca="calor")
    E.resistencia_v("RF", 22.0, 41.0, 47.0)
    E.union_interna("NTC.b", "RF.a")
    E.puntos.add("NTC.b")
    E.cable("amarillo", "A0", "NTC.b")
    E.etiqueta_red("NTC.a", "5V", "5 V", "rojo")
    E.etiqueta_red("RF.b", "GND", "GND", "negro")
    E.etiqueta(28.0, 37.5, "Termistor NTC", None, anchor="lm")
    E.etiqueta(28.0, 44.5, "10 kΩ", None, anchor="lm")
    E.nota(9.5, 39.55, "A0 · cable amarillo")
    # perilla del límite
    E.potenciometro("PL", 44.0, 46.0, 58.0)
    E.etiqueta_red("PL.a", "5V", "5 V", "rojo", lado="der", largo=3.0)
    E.etiqueta_red("PL.b", "GND", "GND", "negro", lado="der", largo=3.0)
    E.cable("celeste", "A1", "PL.w")
    E.etiqueta(50.5, 52.0, "Perilla", "del límite", anchor="mm")
    E.nota(9.5, 50.55, "A1 · cable celeste")
    E.nota(9.8, 58.6, "5 V al riel rojo (+)", anchor="lm", color="#c8202b", negrita=True)
    E.nota(9.8, 61.1, "GND al riel azul (−)", anchor="lm", color="#262626", negrita=True)
    _esq_lcd_verificar(E)
    E.exigir("D5", "RV.a", "el pin 5 debe llegar a la resistencia del LED")
    E.exigir("LEDV.k", "GND", "la pata corta del LED debe llegar a GND")
    E.exigir("A0", "NTC.b", "A0 debe llegar al punto medio del termistor")
    E.exigir("NTC.a", "5V", "el termistor debe llegar a 5 V")
    E.exigir("RF.b", "GND", "la resistencia de 10 kΩ debe llegar a GND")
    E.exigir("A1", "PL.w", "A1 debe llegar al centro de la perilla")
    E.exigir("PL.a", "5V", "un extremo de la perilla debe llegar a 5 V")
    E.exigir("PL.b", "GND", "el otro extremo de la perilla debe llegar a GND")
    for a, b in (("A0", "A1"), ("A0", "5V"), ("A1", "5V"), ("A0", "GND"), ("A1", "GND"), ("D5", "A0"), ("D5", "GND")):
        E.prohibir(a, b, f"{a} y {b} no pueden tocarse")
    E.dibujar(os.path.join(AQUI, "P23_ventilador_automatico_cableado.png"))
    print("P23 cableado listo")


def control_diagrama():
    """Lazo de control (medir, comparar, actuar) y por qué hace falta la histéresis (ilustración con datos inventados)."""
    c = Lienzo(70, 44)
    c.header("P23 · Medir, comparar, actuar, y la histéresis", "Un termostato repite este ciclo cada medio segundo; la histéresis evita que el ventilador «tiemble»")
    cajas = [(2.0, "1 · MEDIR", ["el termistor da la", "temperatura (A0)"], "#e7f1fb"), (19.0, "2 · COMPARAR", ["con el límite que fija", "la perilla (A1)"], "#fff3bf"), (36.0, "3 · ACTUAR", ["enciende o apaga", "el ventilador (pin 5)"], "#fde5cf")]
    for x, tit, lineas, col in cajas:
        c.rect(x, 5.8, 14.0, 6.6, fill=col, outline=TINTA, width=0.1, r=0.5)
        c.text(x + 7.0, 7.3, tit, 0.62, VINO, "Bold")
        for i, s_ in enumerate(lineas):
            c.text(x + 7.0, 9.1 + i * 1.2, s_, 0.5, TINTA, "Medium")
    for xa in (16.4, 33.4):
        _flecha(c, (xa, 9.1), (xa + 2.2, 9.1), VINO, 0.16, 0.7)
    c.rect(53.0, 5.8, 15.0, 6.6, fill="#eef7ee", outline=TINTA, width=0.1, r=0.5)
    c.text(60.5, 7.3, "…y se muestra", 0.6, VINO, "Bold")
    for i, s_ in enumerate(["en la pantalla LCD:", "T, límite y estado"]):
        c.text(60.5, 9.1 + i * 1.2, s_, 0.5, TINTA, "Medium")
    _flecha(c, (50.4, 9.1), (52.6, 9.1), VINO, 0.16, 0.7)
    c.line([(43.0, 12.4), (43.0, 14.4), (9.0, 14.4), (9.0, 12.4)], VINO, 0.14, ends=False)
    _flecha(c, (9.0, 13.6), (9.0, 12.4), VINO, 0.14, 0.6)
    c.text(26.0, 15.5, "y otra vez, cada 0,5 segundos", 0.5, VINO, "SemiBold")
    # histéresis
    x0, y0, W, H = 8.0, 20.0, 56.0, 12.0
    c.text(36.0, 18.6, "Con histéresis: se enciende al llegar al límite y se apaga solo 1 grado por debajo", 0.6, TINTA, "Bold")
    c.rect(x0, y0, W, H, fill="#fbfaf6", outline="#cfc9b8", width=0.08)
    lim = 27.0
    def yt(T):
        return y0 + H - (T - 24.5) / 4.0 * H
    c.line([(x0, yt(lim)), (x0 + W, yt(lim))], "#c8202b", 0.14, ends=False)
    c.line([(x0, yt(lim - 1)), (x0 + W, yt(lim - 1))], "#1d5fd1", 0.14, ends=False)
    c.text(x0 + W + 0.3, yt(lim), "límite: enciende", 0.46, "#c8202b", "Bold", anchor="lm")
    c.text(x0 + W + 0.3, yt(lim - 1), "límite − 1: apaga", 0.46, "#1d5fd1", "Bold", anchor="lm")
    puntos = [(0, 25.2), (6, 25.4), (12, 26.2), (17, 26.9), (19, 27.15), (22, 27.3), (27, 27.1), (30, 26.7), (33, 26.2), (36, 25.9), (42, 25.6), (48, 25.3), (56, 25.0)]
    base = []
    for (ta, va), (tb, vb) in zip(puntos, puntos[1:]):
        for k in range(8):
            u = k / 8
            base.append((ta + (tb - ta) * u, va + (vb - va) * u))
    base.append(puntos[-1])
    c.line([(x0 + t, yt(v)) for t, v in base], "#2a6fdb", 0.2, ends=False)
    c.text(x0 + 2.0, y0 + 1.2, "temperatura", 0.5, "#2a6fdb", "Bold", anchor="lm")
    yb = y0 + H + 1.2
    c.rect(x0, yb, W, 1.6, fill="#ece8dc", outline="#cfc9b8", width=0.06)
    c.rect(x0 + 18.5, yb, 15.5, 1.6, fill="#f2b705", outline="#8a6a00", width=0.06)
    c.text(x0 + 26.2, yb + 0.84, "ventilador ENCENDIDO", 0.5, TINTA, "Bold")
    c.text(x0 + 9.0, yb + 0.84, "apagado", 0.46, GRIS_T, "SemiBold")
    c.text(x0 + 45.0, yb + 0.84, "apagado", 0.46, GRIS_T, "SemiBold")
    c.text(36.0, y0 + H + 4.6, "Sin histéresis, con la temperatura rondando el límite, el ruido de la lectura lo encendería y apagaría muchas veces seguidas.", 0.52, "#b00020", "Bold")
    _caja_aviso(c, 1.5, 39.0, 67.0, 4.6, "En el programa",
                ["if (!ventiladorEncendido && temperatura >= limite)  enciende      ·      else if (ventiladorEncendido && temperatura <= limite - HISTERESIS)  apaga", ], 0.5)
    c.text(c.w_u - 1.0, c.h_u - 0.3, "Ilustración con datos inventados (límite de 27 °C, histéresis de 1 °C).", 0.46, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P23_control.png"))
    print("P23 control listo")


# ====================================================================== SESIÓN 13
# El semáforo (tres LED, pines 8, 9 y 10) se arma como en la Sesión 2 (P04). El sensor de campo es un módulo fuera del protoboard que se conecta DIRECTO a la placa
# con tres cables macho-hembra, como en las lecciones 25 y 31 del kit: VCC (o +) al pin 5V, GND (o −) a un GND de la hilera de abajo (el pegado al 5V) y la señal a A0.
# El orden de las patas es el de las fotos del kit, girado para que las patas queden a la izquierda: suelo, de arriba abajo, AO · DO · GND · VCC; agua, − · + · S.
def dibujar_suelo(c, x, y):
    """Módulo de humedad de suelo con 4 pines (AO, DO, GND y VCC de arriba abajo; DO no se usa) y su sonda. (x, y) = centro del conector de los cables."""
    nombres = ("AO", "DO", "GND", "VCC")
    xb = x + 1.7
    for k in range(4):
        c.rect(x, y - 1.5 + k - 0.12, 2.4, 0.24, fill="#c9a227")                     # patitas del módulo
    c.rect(xb, y - 3.6, 6.4, 7.2, fill="#2f6fb5", outline="#1a4478", width=0.1, r=0.4)
    c.rect(xb + 3.0, y - 3.0, 2.8, 2.2, fill="#2b2b2b", r=0.15)                      # chip comparador
    c.circle(xb + 4.4, y + 1.9, 0.95, fill="#3b82d6", outline="#1a4478", width=0.08)  # perilla de sensibilidad (solo afecta a DO)
    for k, nombre in enumerate(nombres):
        c.text(xb + 0.45, y - 1.5 + k, nombre, 0.34, "#ffffff", "Bold", anchor="lm")
    c.rect(x - 0.9, y - 2.4, 1.8, 4.8, fill="#1e1e1e", r=0.2)                       # conector de los cables macho-hembra
    for k in range(4):
        c.circle(x, y - 1.5 + k, 0.28, fill="#5a5a5a")
    xs = xb + 9.4
    c.line([(xb + 6.4, y - 0.4), (xs, y - 0.4)], "#222222", 0.28, ends=False)         # cable plano entre el módulo y la sonda
    c.line([(xb + 6.4, y + 0.4), (xs, y + 0.4)], "#8a1c1c", 0.28, ends=False)
    c.rect(xs, y - 2.0, 7.0, 4.0, fill="#1a1a1a", r=0.3)                             # la sonda: dos pistas metálicas
    c.rect(xs + 7.0, y - 1.5, 3.2, 1.1, fill="#caa24a")
    c.rect(xs + 7.0, y + 0.4, 3.2, 1.1, fill="#caa24a")
    c.text(xs + 3.5, y, "sonda", 0.45, "#cccccc", "Bold")
    c.text(xb + 9.0, y + 4.9, "Sensor de humedad de suelo", 0.5, TINTA, "Bold")


def dibujar_agua(c, x, y):
    """Sensor de nivel de agua: placa roja con pistas y 3 pines (−, + y S de arriba abajo). (x, y) = centro del conector de los cables."""
    xb = x + 1.7
    for dy in (-1.0, 0.0, 1.0):
        c.rect(x, y + dy - 0.12, 2.4, 0.24, fill="#c9a227")
    c.rect(xb, y - 2.6, 12.0, 5.2, fill="#b3262c", outline="#6b1418", width=0.1, r=0.3)
    for k in range(7):
        c.rect(xb + 3.6 + k * 1.2, y - 2.2, 0.55, 4.4, fill="#f1d9a8")
    for dy, letra in ((-1.0, "−"), (0.0, "+"), (1.0, "S")):
        c.text(xb + 0.7, y + dy, letra, 0.42, "#ffffff", "Bold")
    c.rect(x - 0.9, y - 1.7, 1.8, 3.4, fill="#1e1e1e", r=0.2)                       # conector de los cables macho-hembra
    for dy in (-1.0, 0.0, 1.0):
        c.circle(x, y + dy, 0.28, fill="#5a5a5a")
    c.text(xb + 6.0, y + 4.2, "Sensor de nivel de agua", 0.5, TINTA, "Bold")
    c.text(xb + 9.0, y - 3.5, "solo las pistas se mojan", 0.4, "#8a8a8a", "SemiBold")


def _semaforo(circ, bb, ard):
    """Los tres LED de la Sesión 2 (sin números: son el Paso 0)."""
    G._grupo_p02(circ)
    G._grupo_p03(circ, nuevo=False)
    G._grupo_p04(circ, bb, ard, nuevo=False)


def _sensor_campo(circ, bb, ard, tipo, p0):
    """El sensor de campo y sus tres cables macho-hembra, directo a la placa: p0 GND (al GND de la hilera de abajo), p0+1 señal (a A0), p0+2 VCC o + (al 5V, al final).
    p0=None: sin números."""
    s = (lambda n: p0 + n) if p0 else (lambda n: None)
    sx, sy = 40.0, bb.y + 29.4
    borde = ard.y + ard.H
    if tipo == "suelo":
        y_pin = {"SIG": sy - 1.5, "GND": sy + 0.5, "VCC": sy + 1.5}
        circ.dibujo(lambda c: dibujar_suelo(c, sx, sy))
    else:
        y_pin = {"GND": sy - 1.0, "VCC": sy, "SIG": sy + 1.0}
        circ.dibujo(lambda c: dibujar_agua(c, sx, sy))
    circ.modulo("CAMPO", {k: (sx, v) for k, v in y_pin.items()})
    # cada cable baja de la hilera de abajo de la placa, corre bajo ella y sube por la derecha; el de A0 va por dentro y el del 5V por fuera, para que no se crucen entre sí
    corredor = {"SIG": 34.6, "GND": 35.6, "VCC": 36.6}
    canal = {"SIG": borde + 1.0, "GND": borde + 2.3, "VCC": borde + 3.6}
    pin_placa = {"SIG": "A0", "GND": "GND_5", "VCC": "5V"}
    color = {"SIG": "amarillo", "GND": "negro", "VCC": "rojo"}
    paso = {"GND": s(0), "SIG": s(1), "VCC": s(2)}
    badge_x = {"SIG": 30.0, "GND": 28.0, "VCC": 26.0}
    for k in ("GND", "SIG", "VCC"):
        px = ard.xy(pin_placa[k])[0]
        circ.wire(("mod", "CAMPO", k), ("ard", pin_placa[k]), color[k], step=paso[k],
                  ruta=[(corredor[k], y_pin[k]), (corredor[k], canal[k]), (px, canal[k])], badge=(badge_x[k], canal[k]))


def _verificar_campo(circ):
    circ.exigir(("ard", "A0"), ("mod", "CAMPO", "SIG"), "A0 debe llegar a la señal del sensor")
    circ.exigir(("ard", "5V"), ("mod", "CAMPO", "VCC"), "5 V debe llegar a VCC del sensor")
    circ.exigir(("ard", "GND"), ("mod", "CAMPO", "GND"), "GND debe llegar a GND del sensor")
    circ.prohibir(("mod", "CAMPO", "VCC"), ("mod", "CAMPO", "GND"), "VCC y GND del sensor no pueden tocarse")
    circ.prohibir(("mod", "CAMPO", "SIG"), ("ard", "5V"), "la señal no puede estar unida a 5 V")
    circ.prohibir(("mod", "CAMPO", "SIG"), ("ard", "GND"), "la señal no puede estar unida a GND")
    circ.prohibir(("ard", "5V"), ("ard", "GND"), "5 V y GND no pueden tocarse")


def _verificar_semaforo(circ):
    for pin, nombre in ((8, "D8"), (9, "D9"), (10, "D10")):
        G._verificar_grupo(circ, pin, nombre)
    circ.prohibir(("ard", "D8"), ("ard", "D9"), "pin 8 y pin 9 no pueden tocarse")
    circ.prohibir(("ard", "D9"), ("ard", "D10"), "pin 9 y pin 10 no pueden tocarse")


def p24():
    c = Canvas(63.0, 72.4)
    c.header("P24 · Aviso de riego con el sensor de humedad de suelo", "El semáforo de la Sesión 2 y, a la derecha, el módulo del sensor conectado directo a la placa con tres cables macho-hembra (vista desde arriba)")
    bb = Breadboard(3.0, 4.6, cols=30)
    ard = Arduino(bb.x + 2.6, bb.y + bb.H + 6.2)
    circ = Circuit(c, ard, bb)
    _semaforo(circ, bb, ard)
    _sensor_campo(circ, bb, ard, "suelo", 1)
    _verificar_semaforo(circ)
    _verificar_campo(circ)
    circ.draw()
    lx, ly = _led_cuerpo(bb, 13, 12)
    c.callout(bb.x + 8.0, bb.y + 4.4, ["Paso 0: el semáforo de la Sesión 2:", "rojo (pin 8), amarillo (pin 9), verde (pin 10)"], target=(lx, ly - 1.6), size=0.5)
    c.callout(41.0, bb.y + 38.0, ["Lee las letras de TU módulo: AO, DO, GND y VCC.", "Se usan AO, GND y VCC; DO no se conecta"], size=0.5)
    pie_leyenda(c, ard, 3, [(COL["negro"], "GND  (−, tierra)"), (COL["rojo"], "+5 V al sensor (al final)"), (COL["naranja"], "LED rojo: pin 8 (Paso 0)"), (COL["morado"], "LED amarillo: pin 9 (Paso 0)"),
                            (COL["cafe"], "LED verde: pin 10 (Paso 0)"), (COL["amarillo"], "Salida AO del sensor a A0")])
    c.text(c.w_u - 1.2, c.h_u - 1.2, "Números 1 a 3: el sensor, con el 5 V al final. Los LED son el Paso 0 (como en P04).", 0.5, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P24_humedad_suelo.png"))
    print("P24 listo")
    for fila in sorted((f for f in circ.table if f[0]), key=lambda t: t[0]):
        print("  ", fila)


def _esq_semaforo(E, y_rail, x_taps=(33.0, 31.0, 29.0)):
    """Tres ramas LED (pines 8, 9 y 10) con su riel de GND en y_rail, como en el cableado de P04."""
    G._rama(E, 8.5, 8, "rojo", "LED rojo", "D8", x_taps[0], y_rail)
    G._rama(E, 15.5, 9, "amarillo", "LED amarillo", "D9", x_taps[1], y_rail)
    G._rama(E, 22.5, 10, "verde", "LED verde", "D10", x_taps[2], y_rail)
    G._riel(E, y_rail, ["TAP10", "TAP9", "TAP8"])
    E.nota(x_taps[0] + 0.6, 12.0, "cable negro")
    E.nota(x_taps[2] - 0.6, y_rail - 3.0, "cable negro", anchor="rm")
    E.nota(9.5, y_rail + 1.5, "cable negro", anchor="lm")
    E.nota(20.5, y_rail + 1.5, "riel GND: la tira azul (−)", anchor="lm")
    for p in (8, 9, 10):
        E.exigir(f"D{p}", f"R{p}.a", f"el pin {p} debe llegar a su resistencia")
        E.exigir(f"R{p}.b", f"LED{p}.a", f"la resistencia del pin {p} debe llegar a la pata larga (+)")
        E.exigir(f"LED{p}.k", "GND", f"la pata corta (−) del LED del pin {p} debe llegar a GND")
    E.prohibir("D8", "D9", "pin 8 y pin 9 no pueden tocarse")
    E.prohibir("D9", "D10", "pin 9 y pin 10 no pueden tocarse")


def cableado_p24():
    E = Esquema(44, 47.0)
    E.titulo("P24 · Aviso de riego con el sensor de humedad de suelo", "esquema de conexiones · el sensor entra por A0; tres LED dicen seca, adecuada o muy mojada")
    E.placa(1.5, 5.0, 7.5, 40.5, "Arduino\nUNO R3", [("D8", "D8", 8.5), ("D9", "D9", 15.5), ("D10", "D10", 22.5), ("GND", "GND", 29.5), ("A0", "A0", 37.0), ("GND", "GND2", 39.75), ("5V", "5V", 42.5)])
    E.union_interna("GND2", "GND")
    _esq_semaforo(E, 29.5)
    E.bloque("SU", 22.0, 35.5, 15.0, 9.0, "Humedad de suelo", None,
             terminales=[("ao", "izq", 1.5, "AO"), ("gnd", "izq", 4.25, "GND"), ("vcc", "izq", 7.0, "VCC")])
    E.cable("amarillo", "A0", "SU.ao")
    E.cable("negro", "GND2", "SU.gnd")
    E.cable("rojo", "5V", "SU.vcc")
    E.nota(9.5, 35.55, "A0 · cable amarillo")
    E.nota(9.5, 38.3, "GND · cable negro")
    E.nota(9.5, 41.05, "5 V · cable rojo")
    E.nota(22.0, 45.9, "más húmedo = lectura más baja", anchor="lm", color="#8a8a8a")
    E.exigir("A0", "SU.ao", "A0 debe llegar a la salida AO del sensor")
    E.exigir("SU.vcc", "5V", "VCC del sensor debe llegar a 5 V")
    E.exigir("SU.gnd", "GND", "GND del sensor debe llegar a GND")
    for a, b in (("5V", "GND"), ("A0", "5V"), ("A0", "GND"), ("A0", "D8")):
        E.prohibir(a, b, f"{a} y {b} no pueden tocarse")
    E.dibujar(os.path.join(AQUI, "P24_humedad_suelo_cableado.png"))
    print("P24 cableado listo")


def p25():
    c = Canvas(60.0, 73.7)
    c.header("P25 · Indicador de nivel de agua (modelo de tinaco)", "El semáforo, el zumbador pasivo con su resistencia y el sensor de nivel conectado directo a la placa con tres cables macho-hembra (vista desde arriba)")
    bb = Breadboard(3.0, 4.6, cols=30)
    ard = Arduino(bb.x + 2.6, bb.y + bb.H + 6.2)
    circ = Circuit(c, ard, bb)
    _semaforo(circ, bb, ard)
    circ.zumbador(26, "pasivo", step=1, nombre="BZ")                            # patas en f26 y f29
    circ.resistor((24, "i"), (26, "i"), 220, step=2, nombre="R12")
    circ.wire(("bb", 29, "j"), ("rail", "B", "-", 29), "negro", step=3)
    px = ard.xy("D12")[0]
    xj24 = bb.hole(24, "j")[0]
    yc = bb.y + 22.4
    circ.wire(("ard", "D12"), ("bb", 24, "j"), "azul", step=4, ruta=[(px, yc), (xj24, yc)], badge=(24.0, yc))
    _sensor_campo(circ, bb, ard, "agua", 5)
    _verificar_semaforo(circ)
    _verificar_campo(circ)
    r_a, r_b = circ.elems["R12"]
    a, b = circ.elems["BZ"]
    circ.exigir(("ard", "D12"), r_a, "el pin 12 debe llegar a la resistencia del zumbador")
    circ.exigir(r_b, a, "la resistencia debe llegar a una pata del zumbador")
    circ.exigir(b, ("ard", "GND"), "la otra pata del zumbador debe llegar a GND")
    circ.prohibir(("ard", "D12"), a, "el pin 12 no debe llegar al zumbador sin pasar por la resistencia")
    circ.prohibir(("ard", "D12"), ("ard", "GND"), "pin 12 y GND no pueden tocarse")
    circ.draw()
    lx, ly = _led_cuerpo(bb, 13, 12)
    c.callout(bb.x + 8.0, bb.y + 4.4, ["Paso 0: el semáforo de la Sesión 2.", "Hoy: rojo = nivel bajo, amarillo = medio, verde = alto"], target=(lx, ly - 1.6), size=0.5)
    c.callout(41.0, bb.y + 38.0, ["Lee las letras de TU módulo:", "− (GND), + (VCC) y S (señal).", "Los cables se cruzan porque las patas están", "en otro orden: no importa"], size=0.5)
    pie_leyenda(c, ard, 3, [(COL["negro"], "GND  (−, tierra)"), (COL["rojo"], "+5 V al sensor (al final)"), (COL["naranja"], "LED rojo: pin 8 (Paso 0)"), (COL["morado"], "LED amarillo: pin 9 (Paso 0)"),
                            (COL["cafe"], "LED verde: pin 10 (Paso 0)"), (COL["azul"], "Zumbador pasivo: pin 12"), (COL["amarillo"], "Señal S del sensor a A0")])
    c.text(c.w_u - 1.2, c.h_u - 1.2, "Números 1 a 4: el zumbador; 5 a 7: el sensor, con el 5 V al final. Los LED son el Paso 0 (como en P04).", 0.5, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P25_nivel_agua.png"))
    print("P25 listo")
    for fila in sorted((f for f in circ.table if f[0]), key=lambda t: t[0]):
        print("  ", fila)


def cableado_p25():
    E = Esquema(44, 52.0)
    E.titulo("P25 · Indicador de nivel de agua (modelo de tinaco)", "esquema de conexiones · el sensor entra por A0; tres LED dicen el nivel y el zumbador avisa si está bajo")
    E.placa(1.5, 5.0, 7.5, 45.5, "Arduino\nUNO R3", [("D8", "D8", 8.5), ("D9", "D9", 15.5), ("D10", "D10", 22.5), ("D12", "D12", 29.5), ("GND", "GND", 35.0),
                                                    ("A0", "A0", 41.0), ("GND", "GND2", 43.75), ("5V", "5V", 46.5)])
    E.union_interna("GND2", "GND")
    _esq_semaforo(E, 35.0, x_taps=(37.5, 35.5, 33.5))
    E.resistencia("R12", 15.0, 29.5, "220 Ω")
    E.bloque("BZ", 21.5, 27.5, 6.0, 4.0, "Zumbador", "pasivo", terminales=[("p", "izq", 2.0, ""), ("n", "der", 2.0, "")])
    E.cable("azul", "D12", "R12.a")
    E.cable("azul", "R12.b", "BZ.p")
    E.etiqueta_red("BZ.n", "GND", "GND", "negro", lado="der", largo=1.8)
    E.nota(9.5, 28.05, "pin 12 · cable azul")
    E.etiqueta(17.3, 27.2, "Resistencia")
    E.nota(17.3, 31.4, "rojo · rojo · café", anchor="mm")
    E.bloque("AG", 22.0, 39.5, 13.0, 9.0, "Nivel de agua", None,
             terminales=[("s", "izq", 1.5, "S"), ("gnd", "izq", 4.25, "−"), ("vcc", "izq", 7.0, "+")])
    E.cable("amarillo", "A0", "AG.s")
    E.cable("negro", "GND2", "AG.gnd")
    E.cable("rojo", "5V", "AG.vcc")
    E.nota(9.5, 39.55, "A0 · cable amarillo")
    E.nota(9.5, 42.3, "GND · cable negro")
    E.nota(9.5, 45.05, "5 V · cable rojo")
    E.nota(22.0, 49.6, "más agua = lectura más alta", anchor="lm", color="#8a8a8a")
    E.exigir("A0", "AG.s", "A0 debe llegar a la señal del sensor")
    E.exigir("AG.vcc", "5V", "el sensor debe llegar a 5 V")
    E.exigir("AG.gnd", "GND", "el sensor debe llegar a GND")
    E.exigir("D12", "R12.a", "el pin 12 debe llegar a la resistencia del zumbador")
    E.exigir("R12.b", "BZ.p", "la resistencia debe llegar al zumbador")
    E.exigir("BZ.n", "GND", "el zumbador debe llegar a GND")
    for a, b in (("5V", "GND"), ("A0", "5V"), ("A0", "GND"), ("D12", "GND"), ("D12", "D10"), ("D12", "A0")):
        E.prohibir(a, b, f"{a} y {b} no pueden tocarse")
    E.dibujar(os.path.join(AQUI, "P25_nivel_agua_cableado.png"))
    print("P25 cableado listo")


def calibracion_diagrama():
    """P24: de la lectura al porcentaje de humedad y a los tres colores (valores del sketch como punto de partida)."""
    c = Lienzo(68, 40)
    c.header("P24 · Calibrar: de la lectura a un porcentaje", "Una medición solo significa algo después de calibrarla: la lectura en seco y la lectura en agua fijan la escala")
    x0, y0, W, H = 10.0, 6.0, 36.0, 17.0
    c.rect(x0, y0, W, H, fill="#fbfaf6", outline="#cfc9b8", width=0.08)
    seco, mojado = 1000, 350

    def xl(v):
        return x0 + (v - 300) / 750 * W

    def yh(p):
        return y0 + H - p / 100 * H
    c.rect(x0, yh(30), W, yh(0) - yh(30), fill="#fbe3e3")
    c.rect(x0, yh(70), W, yh(30) - yh(70), fill="#e3f4e6")
    c.rect(x0, yh(100), W, yh(70) - yh(100), fill="#fff4cf")
    for p, txt in ((15, "SECA: hay que regar"), (50, "humedad adecuada"), (85, "MUY MOJADA: no regar")):
        c.text(x0 + W - 0.4, yh(p), txt, 0.5, TINTA, "SemiBold", anchor="rm")
    for p in (0, 30, 70, 100):
        c.line([(x0, yh(p)), (x0 + W, yh(p))], "#d9d3c0", 0.05, ends=False)
        c.text(x0 - 0.4, yh(p), f"{p} %", 0.45, GRIS_T, "SemiBold", anchor="rm")
    c.line([(xl(seco), yh(0)), (xl(mojado), yh(100))], VINO, 0.24, ends=False)
    for v, p, txt in ((seco, 0, "seco: 1000"), (mojado, 100, "en agua: 350")):
        c.circle(xl(v), yh(p), 0.5, fill=VINO)
        c.text(xl(v), y0 + H + 1.2, txt, 0.5, VINO, "Bold")
    c.text(x0 + W / 2, y0 + H + 2.8, "lectura de A0 (más húmedo = lectura más baja)", 0.5, GRIS_T, "SemiBold")
    c.text(4.5, y0 + H / 2, "% de humedad", 0.5, TINTA, "Bold")
    c.rect(49.0, 6.0, 17.0, 17.0, fill="#1e1e24", r=0.5)
    for i, linea in enumerate(["map(lectura,", "    VALOR_SECO,", "    VALOR_MOJADO,", "    0, 100)", "", "constrain(", "    humedad,", "    0, 100)"]):
        c.text(50.4, 7.6 + i * 1.8, linea, 0.6, "#f2f2f2", "Mono", anchor="lm")
    c.text(57.5, 24.6, "map lleva la lectura a 0–100 %;", 0.46, TINTA, "SemiBold")
    c.text(57.5, 25.6, "constrain evita pasarse de 0 o de 100", 0.46, TINTA, "SemiBold")
    cols = [("Situación", 1.5, 24.0), ("Lectura (anótala en la actividad)", 25.5, 22.0), ("Humedad calculada", 47.5, 19.0)]
    filas = [("Sensor al aire o en tierra muy seca", "se espera cerca de VALOR_SECO", "0 %"), ("Tierra húmeda", "entre las dos", "50 % aprox."), ("Sonda metida en un vaso con agua", "se espera cerca de VALOR_MOJADO", "100 %")]
    yt = 29.0
    for (t, xx, w) in cols:
        c.rect(xx, yt, w, 1.5, fill=VINO, outline="#ffffff", width=0.05)
        c.text(xx + w / 2, yt + 0.78, t, 0.46, "#ffffff", "Bold")
    for r_, fila in enumerate(filas):
        yy = yt + 1.5 + r_ * 1.5
        for (t, xx, w), v in zip(cols, fila):
            c.rect(xx, yy, w, 1.5, fill="#ffffff", outline="#cfc9b8", width=0.05)
            c.text(xx + 0.5, yy + 0.78, v, 0.46, TINTA, "Medium", anchor="lm")
    c.text(c.w_u - 1.0, c.h_u - 0.4, "1000 y 350 son los valores de partida del sketch: cada sensor y cada tierra darán los suyos (V7).", 0.48, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P24_calibracion.png"))
    print("P24 calibración listo")


def niveles_diagrama():
    """P25: el tinaco con tres niveles y lo que indica cada LED (valores del sketch como punto de partida)."""
    c = Lienzo(66, 38)
    c.header("P25 · El modelo de tinaco: tres niveles", "Más agua toca más pistas del sensor, la lectura sube; los umbrales dividen el rango en tres")
    for xc, nivel, col_led, txt, lect in ((10.0, 0.18, "#e63946", "BAJO", "lectura < 150"), (26.0, 0.55, "#ffd60a", "MEDIO", "de 150 a 400"), (42.0, 0.9, "#38b000", "ALTO", "más de 400")):
        c.rect(xc - 5.0, 8.0, 10.0, 14.0, fill="#f6fbff", outline=TINTA, width=0.12, r=0.3)
        yt = 22.0 - nivel * 14.0
        c.rect(xc - 4.88, yt, 9.76, 22.0 - yt - 0.12, fill="#9ed2f2")
        c.rect(xc - 1.2, 7.0, 2.4, 14.0, fill="#b3262c", outline="#6b1418", width=0.06)
        for j in range(5):
            c.rect(xc - 0.9 + j * 0.45, 12.0, 0.2, 9.0, fill="#f1d9a8")
        c.circle(xc, 25.5, 1.1, fill=col_led, outline="#3a3a3a", width=0.08)
        c.text(xc, 27.7, txt, 0.65, TINTA, "Bold")
        c.text(xc, 28.9, lect, 0.46, GRIS_T, "SemiBold")
    c.text(26.0, 5.4, "Sensor de nivel dentro del recipiente (solo las pistas, nunca la placa electrónica)", 0.52, VINO, "Bold")
    c.text(58.0, 9.5, "En el programa", 0.62, TINTA, "Bold")
    for i, linea in enumerate(["if (nivel < NIVEL_BAJO)", "   rojo + pitido", "else if (nivel < NIVEL_ALTO)", "   amarillo", "else", "   verde"]):
        c.text(50.0, 11.4 + i * 1.3, linea, 0.5, TINTA, "Mono", anchor="lm")
    _caja_aviso(c, 1.5, 31.2, 63.0, 5.4, "Cuidado con el agua",
                ["Solo se mojan las pistas del sensor. La placa, los cables y el Arduino se mantienen secos y lejos del recipiente. Solo 5 V: nunca conectes nada a la corriente de la casa."], 0.52)
    c.text(c.w_u - 1.0, c.h_u - 0.3, "NIVEL_BAJO = 150 y NIVEL_ALTO = 400 son valores de partida: se calibran con el sensor y el agua reales (V7).", 0.46, GRIS_T, "Medium", anchor="rm")
    c.save(os.path.join(AQUI, "P25_niveles.png"))
    print("P25 niveles listo")


TODOS = {"P21": [lcd_conoce, p21, cableado_p21],
         "P22": [p22, cableado_p22],
         "P23": [control_diagrama, p23, cableado_p23],
         "P24": [calibracion_diagrama, p24, cableado_p24],
         "P25": [niveles_diagrama, p25, cableado_p25]}

if __name__ == "__main__":
    pedidos = sys.argv[1:] or list(TODOS)
    for clave in pedidos:
        for f in TODOS[clave]:
            f()
