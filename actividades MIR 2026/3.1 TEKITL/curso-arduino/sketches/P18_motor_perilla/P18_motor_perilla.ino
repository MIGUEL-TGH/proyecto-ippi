/*
  P18 · Intensidad de la carga controlada con la perilla      Sesión 9
  ------------------------------------------------------------------
  El nombre del sketch dice "motor" porque ese es el destino. HOY SE ARMA CON UN LED.

  !! EL MOTOR NO SE ARMA TODAVÍA (16 nov 2026) !!
  Se midió que el motor "3-6 V" funciona a partir de 0.95 A, más de lo que aguantan el
  PN2222 (0.6 A) y el módulo de fuente (0.7 A). Ver P17 y plan-curso-arduino.md, V1.
  ------------------------------------------------------------------
  Qué hace: al girar el potenciómetro cambia el brillo del LED (o la velocidad del motor,
  cuando se destrabe) a través del transistor.

  Conexiones: el circuito del transistor es el mismo de P17 (resistencia de 330 ohm en la base
  al pin 5; carga en el colector). Cambia el botón por el potenciómetro:
    Potenciómetro   extremo -> 5 V ; centro -> A0 ; otro extremo -> GND

  Ideas clave:
    - PWM otra vez: analogWrite(5, 0 a 255) enciende y apaga el transistor muy rápido.
      Con más tiempo encendido, la carga recibe más potencia promedio.
    - Un motor tiene un "voltaje de arranque": con valores muy bajos no alcanza a girar.
      Con el motor, se mide a partir de qué número empieza a moverse y se anota. Ese dato sirve
      para ajustar UMBRAL_ARRANQUE y que la perilla no tenga una zona "muerta".
    - Con el LED no hay zona muerta de verdad. El valor de 60 hace que el LED también se
      apague en la primera cuarta parte de la perilla: así se ve cómo se sentiría con el motor.
      Pon UMBRAL_ARRANQUE en 0 para quitar esa zona.

  Seguridad: con el motor, no bloquees el aspa. Si el módulo de fuente se calienta, desconéctalo.

  Retos:  - Ajusta UMBRAL_ARRANQUE (con el LED, prueba con 0 y con 100).
          - Muestra la velocidad en porcentaje en el Monitor Serie.
          - Haz que dos botones suban y bajen la intensidad en pasos de 10 %.
*/

const int PIN_PERILLA = A0;
const int PIN_CARGA = 5;                // pin con ~ (PWM) hacia la base del transistor
const int UMBRAL_ARRANQUE = 60;         // valor inicial: ajústalo con tus mediciones

void setup() {
  pinMode(PIN_CARGA, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int lectura = analogRead(PIN_PERILLA);
  int velocidad = map(lectura, 0, 1023, 0, 255);

  if (velocidad < UMBRAL_ARRANQUE) {
    velocidad = 0;                      // por debajo de este valor el motor no arranca
  }
  analogWrite(PIN_CARGA, velocidad);

  int porcentaje = map(velocidad, 0, 255, 0, 100);
  Serial.print("PWM: ");
  Serial.print(velocidad);
  Serial.print("    Intensidad: ");
  Serial.print(porcentaje);
  Serial.println(" %");
  delay(100);
}
