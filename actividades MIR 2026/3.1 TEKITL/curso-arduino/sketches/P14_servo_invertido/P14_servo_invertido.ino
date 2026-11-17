/*
  P14 · Reto: servo al revés respecto a la perilla (solución del instructor)    Sesión 7
  ------------------------------------------------------------------
  Qué hace: al girar la perilla hacia donde antes el servo subía, ahora baja.

  Conexiones: las mismas de P14
    Servo SG90      café -> GND ; rojo -> 5 V ; naranja (señal) -> pin 9
    Potenciómetro   extremo -> 5 V ; centro -> A0 ; otro extremo -> GND

  Idea clave: igual que en la Sesión 5, map() acepta rangos "al revés": map(lectura, 0, 1023, 180, 0).
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
  int angulo = map(lectura, 0, 1023, 180, 0);      // 0 -> 180 y 1023 -> 0
  miServo.write(angulo);
  delay(15);
}
