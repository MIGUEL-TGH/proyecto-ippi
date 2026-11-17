/*
  P13 · Servo: posición y barrido                             Sesión 7
  ------------------------------------------------------------------
  Qué hace: el servo va a 90 grados, espera, y luego barre de 0 a 180 y de 180 a 0.

  Conexiones del servo SG90 (3 cables; sus cables de colores terminan en un conector hembra,
  donde entran los cables macho-macho):
    cable café (o negro)         -> GND   (riel azul del protoboard)
    cable rojo                   -> 5 V   (riel rojo del protoboard)
    cable naranja (o amarillo)   -> pin 9 (la señal)

  Ideas clave:
    - Un servo es un motor que gira a un ÁNGULO que tú le pides (0 a 180 grados).
    - Se le habla con pulsos (de 1 a 2 milisegundos, según su hoja de datos); la librería
      Servo se encarga y ya viene con el IDE: no hay que instalar nada.
    - for repite instrucciones: "para angulo desde 0 hasta 180, de uno en uno".
    - Cada grado tarda 15 ms: de 0 a 180 son 180 x 15 ms = 2.7 segundos.

  Si el Arduino se reinicia o el servo tiembla, la alimentación no alcanza: aliméntalo
  desde el módulo de fuente de 5 V y une su GND con el GND del Arduino (ver Sesión 7).
  No fuerces el brazo con la mano mientras está energizado.

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
