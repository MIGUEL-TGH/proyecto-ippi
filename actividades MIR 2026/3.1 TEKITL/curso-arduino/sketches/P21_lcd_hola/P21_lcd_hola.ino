/*
  P21 · Pantalla LCD 16x2: primer mensaje                     Sesión 11
  ------------------------------------------------------------------
  Qué hace: escribe un mensaje en la primera línea y un contador de segundos en la segunda.

  Conexiones del LCD1602 (16 pines, de izquierda a derecha, enchufado en la fila a del protoboard):
    1  VSS -> GND
    2  VDD -> 5 V
    3  V0  -> centro de un potenciómetro (ajusta el contraste); extremos a 5 V y GND
    4  RS  -> pin 12
    5  RW  -> GND
    6  E   -> pin 11
    11 D4  -> pin 10
    12 D5  -> pin 9
    13 D6  -> pin 8
    14 D7  -> pin 7
    15 A   -> resistencia de 100 ohm -> 5 V (luz de fondo)
    16 K   -> GND
    (Los pines 7 a 10, D0 a D3, no se usan: trabajamos en modo de 4 bits.)
  Los pines 12, 11, 10, 9, 8 y 7 siguen el orden de las patas del LCD, así los cables van
  paralelos y no se cruzan. La lección 19 del kit usa otros pines; este orden es el del curso.
  Si la pantalla no muestra nada, gira el potenciómetro de contraste.

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
LiquidCrystal lcd(12, 11, 10, 9, 8, 7);

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
