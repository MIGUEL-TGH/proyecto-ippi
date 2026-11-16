/*
  P03 · Dos LED que se alternan                               Sesión 2
  ------------------------------------------------------------------
  Qué hace: cuando un LED está encendido, el otro está apagado, y luego se invierten.

  Conexiones (cada LED lleva su propia resistencia de 220 ohm):
    LED 1   pin 8 -> resistencia 220 ohm -> LED (pata larga +) ; pata corta (-) -> GND
    LED 2   pin 9 -> resistencia 220 ohm -> LED (pata larga +) ; pata corta (-) -> GND

  Idea clave: una VARIABLE es una caja con nombre donde guardamos un dato.
  Aquí "tiempoEncendido" guarda cuántos milisegundos dura cada paso.
  Si la cambias en UN solo lugar, cambia todo el programa.

  Retos:  - Cambia tiempoEncendido a 200 y luego a 1500.
          - Que el LED 1 dure 300 ms y el LED 2 dure 900 ms (necesitas dos variables).
          - Agrega un tercer LED y haz que se enciendan uno por uno.
*/

const int PIN_LED_1 = 8;        // const = valor que no cambia mientras corre el programa
const int PIN_LED_2 = 9;
int tiempoEncendido = 500;      // milisegundos

void setup() {
  pinMode(PIN_LED_1, OUTPUT);
  pinMode(PIN_LED_2, OUTPUT);
}

void loop() {
  digitalWrite(PIN_LED_1, HIGH);
  digitalWrite(PIN_LED_2, LOW);
  delay(tiempoEncendido);

  digitalWrite(PIN_LED_1, LOW);
  digitalWrite(PIN_LED_2, HIGH);
  delay(tiempoEncendido);
}
