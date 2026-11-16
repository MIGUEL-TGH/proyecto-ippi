/*
  P03 · Reto: cada LED con su propio tiempo (solución del instructor)   Sesión 2
  ------------------------------------------------------------------
  Qué hace: igual que P03, pero el LED 1 dura encendido 300 ms y el LED 2 dura 900 ms.
  Para eso una sola variable ya no alcanza: se necesitan dos, una por LED.

  Conexiones: las mismas de P03 (LED 1 en el pin 8, LED 2 en el pin 9, cada uno con 220 ohm).

  Idea clave: cada dato que puede cambiar merece su propia variable con un nombre claro.
*/

const int PIN_LED_1 = 8;
const int PIN_LED_2 = 9;
int tiempoLed1 = 300;           // milisegundos que dura encendido el LED 1
int tiempoLed2 = 900;           // milisegundos que dura encendido el LED 2

void setup() {
  pinMode(PIN_LED_1, OUTPUT);
  pinMode(PIN_LED_2, OUTPUT);
}

void loop() {
  digitalWrite(PIN_LED_1, HIGH);
  digitalWrite(PIN_LED_2, LOW);
  delay(tiempoLed1);            // el LED 1 está encendido tiempoLed1

  digitalWrite(PIN_LED_1, LOW);
  digitalWrite(PIN_LED_2, HIGH);
  delay(tiempoLed2);            // el LED 2 está encendido tiempoLed2
}
