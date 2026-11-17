/*
  P16 · Reto: alarma si el objeto se queda más de 5 segundos (solución del instructor)   Sesión 8
  ------------------------------------------------------------------
  Qué hace: la barrera de P16; si algo se queda frente al sensor más de 5 segundos con la
  barrera abierta, el zumbador pita sin parar hasta que el paso quede libre.

  Conexiones: las mismas de P16
    HC-SR04   VCC -> 5 V ; TRIG -> pin 6 ; ECHO -> pin 7 ; GND -> GND
    Servo     café -> GND ; rojo -> 5 V ; naranja (señal) -> pin 9
    Zumbador PASIVO   una pata -> resistencia 220 ohm -> pin 12 ; otra pata -> GND
    LED       pin 8 -> resistencia 220 ohm -> LED (+) ; pata corta -> GND

  Ideas clave:
    - Se mide el tiempo CONTANDO ciclos: cada ciclo del while dura 100 ms, así que 50 ciclos
      seguidos con algo enfrente son 5 segundos.
    - ciclosOcupado se pone en 0 al abrir y solo cuenta mientras hay algo enfrente.
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
const int CICLOS_ALARMA = 50;         // 50 ciclos x 100 ms = 5 segundos con algo enfrente

Servo barrera;

float medirDistancia() {
  digitalWrite(PIN_TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(PIN_TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(PIN_TRIG, LOW);

  long duracion = pulseIn(PIN_ECHO, HIGH, 30000UL);
  if (duracion == 0) {
    return 999.0;
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

    int ciclosLibre = 0;
    int ciclosOcupado = 0;
    while (ciclosLibre < CICLOS_LIBRE) {
      if (medirDistancia() < DISTANCIA_ABRIR) {
        ciclosLibre = 0;
        ciclosOcupado = ciclosOcupado + 1;
        if (ciclosOcupado >= CICLOS_ALARMA) {
          tone(PIN_ZUMBADOR, 2000, 80);     // alarma: un pitido corto en cada ciclo
        }
      } else {
        ciclosLibre = ciclosLibre + 1;
        ciclosOcupado = 0;
      }
      delay(100);
    }
    cerrarBarrera();
  }
  delay(100);
}
