/*
  P18 · Velocidad del motor controlada con la perilla         Sesión 9
  ------------------------------------------------------------------
  !! NO ARMAR TODAVÍA (16 nov 2026) !!
  Se midió que el motor "3-6 V" funciona a partir de 0.95 A, más de lo que aguantan el
  PN2222 (0.6 A) y el módulo de fuente (0.7 A). Ver P17 y plan-curso-arduino.md, V1.
  ------------------------------------------------------------------
  Qué hace: al girar el potenciómetro cambia la velocidad del motor con aspa.

  Conexiones: el circuito del motor es el mismo de P17 (módulo de fuente + PN2222 +
  resistencia de 330 ohm en la base al pin 5 + diodo 1N4007 en paralelo con el motor +
  GND común). Cambia el botón por el potenciómetro:
    Potenciómetro   extremo -> 5 V ; centro -> A0 ; otro extremo -> GND

  Ideas clave:
    - PWM otra vez: analogWrite(5, 0 a 255) enciende y apaga el transistor muy rápido.
      Con más tiempo encendido, el motor recibe más potencia promedio y gira más rápido.
    - El motor tiene un "voltaje de arranque": con valores muy bajos no alcanza a girar.
      Observa a partir de qué número empieza a moverse y anótalo. Ese dato sirve para
      ajustar UMBRAL_ARRANQUE y que la perilla no tenga una zona "muerta".

  Seguridad: no bloquees el aspa. Si el módulo de fuente se calienta, desconéctalo.

  Retos:  - Ajusta UMBRAL_ARRANQUE con tus propias mediciones.
          - Muestra la velocidad en porcentaje en el Monitor Serie.
          - Haz que dos botones suban y bajen la velocidad en pasos de 10 %.
*/

const int PIN_PERILLA = A0;
const int PIN_MOTOR = 5;                // pin con ~ (PWM) hacia la base del transistor
const int UMBRAL_ARRANQUE = 60;         // valor inicial: ajústalo con tus mediciones

void setup() {
  pinMode(PIN_MOTOR, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int lectura = analogRead(PIN_PERILLA);
  int velocidad = map(lectura, 0, 1023, 0, 255);

  if (velocidad < UMBRAL_ARRANQUE) {
    velocidad = 0;                      // por debajo de este valor el motor no arranca
  }
  analogWrite(PIN_MOTOR, velocidad);

  int porcentaje = map(velocidad, 0, 255, 0, 100);
  Serial.print("PWM: ");
  Serial.print(velocidad);
  Serial.print("    Velocidad: ");
  Serial.print(porcentaje);
  Serial.println(" %");
  delay(100);
}
