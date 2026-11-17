/*
  P14 · Reto: servo limitado a 30-150 grados y con el ángulo en pantalla (solución del instructor)
  ------------------------------------------------------------------                Sesión 7
  Qué hace: el servo sigue la perilla, pero solo entre ANGULO_MIN y ANGULO_MAX, y escribe
  el ángulo en el Monitor Serie (velocidad 9600).

  Conexiones: las mismas de P14
    Servo SG90      café -> GND ; rojo -> 5 V ; naranja (señal) -> pin 9
    Potenciómetro   extremo -> 5 V ; centro -> A0 ; otro extremo -> GND

  Ideas clave:
    - Los dos últimos números de map() son el rango de SALIDA: aquí, constantes con nombre.
    - Serial.print del ángulo: ver el número ayuda a entender qué le pide el programa al servo.
*/

#include <Servo.h>

Servo miServo;
const int PIN_SERVO = 9;
const int PIN_PERILLA = A0;
const int ANGULO_MIN = 30;
const int ANGULO_MAX = 150;

void setup() {
  miServo.attach(PIN_SERVO);
  Serial.begin(9600);
}

void loop() {
  int lectura = analogRead(PIN_PERILLA);
  int angulo = map(lectura, 0, 1023, ANGULO_MIN, ANGULO_MAX);
  miServo.write(angulo);

  Serial.print("Angulo: ");
  Serial.println(angulo);
  delay(50);
}
