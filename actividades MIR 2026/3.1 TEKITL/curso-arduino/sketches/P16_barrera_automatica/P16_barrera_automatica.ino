/*
  P16 · Barrera automática (ultrasonido + servo + zumbador)   Sesión 8
  ------------------------------------------------------------------
  Qué hace: cuando algo se acerca a menos de 20 cm, el servo levanta la barrera con un
  pitido. Cuando el paso queda libre unos segundos, la baja con otro pitido.

  Conexiones:
    HC-SR04   VCC -> 5 V ; TRIG -> pin 6 ; ECHO -> pin 7 ; GND -> GND
    Servo     GND -> GND ; rojo -> 5 V ; señal -> pin 9   (pega un palito de paleta al brazo)
    Zumbador PASIVO   una pata -> resistencia 220 ohm -> pin 12 ; otra pata -> GND   (tone() necesita el pasivo; la resistencia, como en la Sesión 4)
    LED       pin 8 -> resistencia 220 ohm -> LED (+) ; pata corta -> GND
              (LED encendido = barrera abierta)

  Ideas clave:
    - Combina tres cosas que ya sabes: sensor + decisión + actuadores.
    - Una función que devuelve un valor: medirDistancia() "entrega" los centímetros.
    - Se organiza el programa en funciones pequeñas con nombre: abrirBarrera(), cerrarBarrera().

  Si el Arduino se reinicia cuando se mueve el servo, alimenta el servo desde el módulo de
  fuente de 5 V y une los GND.

  Retos:  - Cambia la distancia de activación.
          - Si el objeto se queda más de 5 segundos, haz sonar una alarma.
          - Cuenta cuántos vehículos han pasado y muéstralo en el Monitor Serie.
*/

#include <Servo.h>

const int PIN_TRIG = 6;
const int PIN_ECHO = 7;
const int PIN_SERVO = 9;
const int PIN_ZUMBADOR = 12;
const int PIN_LED = 8;

const int DISTANCIA_ABRIR = 20;       // cm
const int ANGULO_CERRADA = 0;
const int ANGULO_ABIERTA = 90;
const int CICLOS_LIBRE = 20;          // 20 ciclos x 100 ms = 2 segundos sin nadie

Servo barrera;

float medirDistancia() {
  digitalWrite(PIN_TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(PIN_TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(PIN_TRIG, LOW);

  long duracion = pulseIn(PIN_ECHO, HIGH, 30000UL);
  if (duracion == 0) {
    return 999.0;                     // sin eco: no hay nada cerca
  }
  return duracion * 0.0343 / 2.0;
}

void abrirBarrera() {
  tone(PIN_ZUMBADOR, 1000, 200);
  barrera.write(ANGULO_ABIERTA);
  digitalWrite(PIN_LED, HIGH);
  Serial.println("Barrera ABIERTA");
}

void cerrarBarrera() {
  tone(PIN_ZUMBADOR, 500, 400);
  barrera.write(ANGULO_CERRADA);
  digitalWrite(PIN_LED, LOW);
  Serial.println("Barrera CERRADA");
}

void setup() {
  pinMode(PIN_TRIG, OUTPUT);
  pinMode(PIN_ECHO, INPUT);
  pinMode(PIN_LED, OUTPUT);
  pinMode(PIN_ZUMBADOR, OUTPUT);
  barrera.attach(PIN_SERVO);
  barrera.write(ANGULO_CERRADA);
  Serial.begin(9600);
}

void loop() {
  if (medirDistancia() < DISTANCIA_ABRIR) {
    abrirBarrera();

    // Espera a que el paso quede libre durante 2 segundos seguidos
    int ciclosLibre = 0;
    while (ciclosLibre < CICLOS_LIBRE) {
      if (medirDistancia() < DISTANCIA_ABRIR) {
        ciclosLibre = 0;              // hay alguien: reinicia la cuenta
      } else {
        ciclosLibre = ciclosLibre + 1;
      }
      delay(100);
    }
    cerrarBarrera();
  }
  delay(100);
}
