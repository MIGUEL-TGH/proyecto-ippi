/*
  P21 · Reto: un texto que se desplaza (solución del instructor)    Sesión 11
  ------------------------------------------------------------------
  Qué hace: escribe un mensaje largo en la fila 1 y lo desplaza hacia la izquierda, como un
  letrero. En la fila 2 deja el nombre del equipo quieto.

  Conexiones: las mismas de P21 (RS 12, E 11, D4 10, D5 9, D6 8, D7 7; contraste con potenciómetro;
  luz de fondo con 100 ohm).

  Ideas clave:
    - lcd.scrollDisplayLeft() mueve TODO lo que hay en pantalla una columna a la izquierda.
      Como la fila 2 también se movería, el nombre del equipo se escribe corto y se acepta que
      se mueva con el mensaje (o se usa otra técnica en un proyecto).
    - La pantalla tiene 40 posiciones por fila aunque solo muestre 16: por eso se puede
      desplazar un texto largo sin que se pierda.
*/

#include <LiquidCrystal.h>

//                RS, E, D4, D5, D6, D7
LiquidCrystal lcd(12, 11, 10, 9, 8, 7);

void setup() {
  lcd.begin(16, 2);
  lcd.setCursor(0, 0);
  lcd.print("Hola, soy el equipo 1 del curso de Arduino!");
}

void loop() {
  lcd.scrollDisplayLeft();
  delay(300);
}
