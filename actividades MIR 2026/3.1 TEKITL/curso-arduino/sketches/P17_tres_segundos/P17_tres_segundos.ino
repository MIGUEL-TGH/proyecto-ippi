/*
  P17 · Reto: tres segundos encendida y se apaga sola (solución del instructor)    Sesión 9
  ------------------------------------------------------------------
  Qué hace: al presionar el botón la carga (LED o, cuando se destrabe, motor) se enciende
  3 segundos y se apaga sola.

  Conexiones: las mismas de P17
    PN2222   emisor -> GND ; base -> resistencia 330 ohm -> pin 5 ; colector -> carga
    LED      pata larga (+) -> resistencia 220 ohm -> 5 V ; pata corta (-) -> colector
    Botón    una pata -> pin 2 ; la pata opuesta (en diagonal) -> GND

  Ideas clave:
    - Un delay dentro del if: mientras pasan los 3 segundos el programa no hace otra cosa
      (la Sesión 11 enseña a esperar sin detener el programa).
    - TIEMPO_ENCENDIDA es una constante con nombre: un solo lugar para cambiar la duración.
*/

const int PIN_BOTON = 2;
const int PIN_CARGA = 5;
const int TIEMPO_ENCENDIDA = 3000;     // milisegundos

void setup() {
  pinMode(PIN_BOTON, INPUT_PULLUP);
  pinMode(PIN_CARGA, OUTPUT);
}

void loop() {
  if (digitalRead(PIN_BOTON) == LOW) {
    digitalWrite(PIN_CARGA, HIGH);
    delay(TIEMPO_ENCENDIDA);
    digitalWrite(PIN_CARGA, LOW);
  }
}
