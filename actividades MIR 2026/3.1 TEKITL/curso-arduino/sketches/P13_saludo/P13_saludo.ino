/*
  P13 · Reto: la bandera que saluda (solución del instructor)     Sesión 7
  ------------------------------------------------------------------
  Qué hace: el brazo del servo (con una bandera de papel pegada) saluda tres veces, de
  60 a 120 grados, y descansa tres segundos.

  Conexiones: las mismas de P13
    Servo SG90   café -> GND ; rojo -> 5 V ; naranja (señal) -> pin 9

  Ideas clave:
    - Un for dentro de una función: saludar() se escribe una vez y se usa cuando se quiera.
    - Para un movimiento rápido se piden ángulos lejanos con pausas cortas: el servo va a su
      máxima velocidad (según su hoja de datos, unos 0.1 s por cada 60 grados).
*/

#include <Servo.h>

Servo miServo;
const int PIN_SERVO = 9;
const int VECES = 3;               // cuántas veces saluda

void saludar() {
  for (int i = 0; i < VECES; i++) {
    miServo.write(120);
    delay(350);
    miServo.write(60);
    delay(350);
  }
}

void setup() {
  miServo.attach(PIN_SERVO);
  miServo.write(90);
  delay(1000);
}

void loop() {
  saludar();
  miServo.write(90);               // vuelve al centro y descansa
  delay(3000);
}
