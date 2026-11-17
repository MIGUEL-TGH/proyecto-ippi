/*
  P13 · Reto: barrido solo de 45 a 135 grados (solución del instructor)    Sesión 7
  ------------------------------------------------------------------
  Qué hace: igual que P13, pero el servo solo se mueve entre ANGULO_MIN y ANGULO_MAX.

  Conexiones: las mismas de P13
    Servo SG90   café -> GND ; rojo -> 5 V ; naranja (señal) -> pin 9

  Ideas clave:
    - Los límites del for son constantes con nombre: para cambiar el rango se cambia un
      solo lugar (como en la Sesión 2).
    - Un rango más corto es más suave para el servo: no llega a sus topes.
*/

#include <Servo.h>

Servo miServo;
const int PIN_SERVO = 9;
const int ANGULO_MIN = 45;
const int ANGULO_MAX = 135;

void setup() {
  miServo.attach(PIN_SERVO);
  miServo.write(ANGULO_MIN);
  delay(1000);
}

void loop() {
  for (int angulo = ANGULO_MIN; angulo <= ANGULO_MAX; angulo++) {
    miServo.write(angulo);
    delay(15);
  }
  for (int angulo = ANGULO_MAX; angulo >= ANGULO_MIN; angulo--) {
    miServo.write(angulo);
    delay(15);
  }
}
