/*
  P14 · Servo controlado con la perilla                       Sesión 7
  ------------------------------------------------------------------
  Qué hace: el ángulo del servo sigue la posición del potenciómetro.

  Conexiones:
    Servo SG90      GND -> GND ; rojo -> 5 V ; señal -> pin 9
    Potenciómetro   extremo -> 5 V ; centro -> A0 ; otro extremo -> GND

  Idea clave: es la misma conversión de la sesión 5, pero ahora la escala de salida
  es 0 a 180 grados: map(lectura, 0, 1023, 0, 180).

  Retos:  - Limita el movimiento a 30-150 grados.
          - Muestra el ángulo en el Monitor Serie.
          - Haz que el servo se mueva al revés respecto a la perilla.
*/

#include <Servo.h>

Servo miServo;
const int PIN_SERVO = 9;
const int PIN_PERILLA = A0;

void setup() {
  miServo.attach(PIN_SERVO);
}

void loop() {
  int lectura = analogRead(PIN_PERILLA);
  int angulo = map(lectura, 0, 1023, 0, 180);
  miServo.write(angulo);
  delay(15);
}
