/*
  P13 · Servo: posición y barrido                             Sesión 7
  ------------------------------------------------------------------
  Qué hace: el servo va a 90 grados, espera, y luego barre de 0 a 180 y de 180 a 0.

  Conexiones del servo SG90 (3 cables):
    cable café o negro   -> GND
    cable rojo           -> 5 V
    cable naranja o amarillo (señal) -> pin 9

  Ideas clave:
    - Un servo es un motor que gira a un ÁNGULO que tú le pides (0 a 180 grados).
    - Se le habla con pulsos; la librería Servo se encarga (ya viene con el IDE).
    - for repite instrucciones: "para angulo desde 0 hasta 180, de uno en uno".

  Si el Arduino se reinicia o el servo tiembla, la alimentación no alcanza: aliméntalo
  desde el módulo de fuente de 5 V y une su GND con el GND del Arduino.

  Retos:  - Cambia el delay(15) y observa la velocidad.
          - Haz que el servo vaya solo de 45 a 135 grados.
          - Pega una bandera de papel al brazo y haz que salude.
*/

#include <Servo.h>

Servo miServo;                  // objeto que representa al servo
const int PIN_SERVO = 9;

void setup() {
  miServo.attach(PIN_SERVO);
  miServo.write(90);            // posición central
  delay(1000);
}

void loop() {
  for (int angulo = 0; angulo <= 180; angulo++) {
    miServo.write(angulo);
    delay(15);                  // da tiempo al servo para llegar
  }
  for (int angulo = 180; angulo >= 0; angulo--) {
    miServo.write(angulo);
    delay(15);
  }
}
