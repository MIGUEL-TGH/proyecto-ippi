/*
  P21 · Pantalla LCD 16x2: primer mensaje                     Sesión 11
  ------------------------------------------------------------------
  Qué hace: escribe un mensaje en la primera línea y un contador de segundos en la segunda.

  Conexiones del LCD1602 (16 pines, de izquierda a derecha):
    1  VSS -> GND
    2  VDD -> 5 V
    3  V0  -> centro de un potenciómetro (ajusta el contraste); extremos a 5 V y GND
    4  RS  -> pin 7
    5  RW  -> GND
    6  E   -> pin 8
    11 D4  -> pin 9
    12 D5  -> pin 10
    13 D6  -> pin 11
    14 D7  -> pin 12
    15 A   -> 5 V (luz de fondo)
    16 K   -> GND
    (Los pines 7 a 10, D0 a D3, no se usan: trabajamos en modo de 4 bits.)
  Mismo conexionado que la lección 19 del kit; si la pantalla no muestra nada,
  gira el potenciómetro de contraste.

  Ideas clave:
    - #include trae una LIBRERÍA: código ya hecho por otras personas. LiquidCrystal
      ya viene con el IDE; no hay que instalar nada.
    - lcd.setCursor(columna, fila) elige dónde escribir; lcd.print() escribe.
    - La pantalla no muestra acentos ni ñ: usa letras sin acento.

  Retos:  - Muestra tu nombre en la fila 1 y el nombre de tu equipo en la fila 2.
          - Haz que un texto se desplace de derecha a izquierda (lcd.scrollDisplayLeft()).
*/

#include <LiquidCrystal.h>

//                RS, E, D4, D5, D6, D7
LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

void setup() {
  lcd.begin(16, 2);               // 16 columnas, 2 filas
  lcd.setCursor(0, 0);
  lcd.print("Hola, IPPI!");
}

void loop() {
  lcd.setCursor(0, 1);
  lcd.print("Segundos: ");
  lcd.print(millis() / 1000);     // segundos desde que se encendió
  lcd.print("   ");               // borra restos de números más largos
}
