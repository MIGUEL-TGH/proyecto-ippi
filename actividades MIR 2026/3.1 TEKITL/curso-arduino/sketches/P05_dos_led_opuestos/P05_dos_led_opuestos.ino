/*
  P05 · Reto: dos LED opuestos (solución del instructor)           Sesión 3
  ------------------------------------------------------------------
  Qué hace: mientras presionas el botón se enciende el LED rojo y se apaga el amarillo;
  al soltarlo, al revés. Siempre hay uno encendido y el otro apagado.

  Conexiones: las mismas de P05 (el semáforo de P04 sigue armado; el verde no se usa).
    LED rojo      pin 8  (con su resistencia de 220 ohm)
    LED amarillo  pin 9  (con su resistencia de 220 ohm)
    Botón         pin 2 y GND, en patas opuestas (en diagonal)

  Idea clave: un solo if/else decide qué hacen los DOS LED; los dos digitalWrite de cada
  rama van juntos, así nunca quedan los dos encendidos o los dos apagados.
*/

const int PIN_BOTON = 2;
const int LED_ROJO = 8;
const int LED_AMARILLO = 9;

void setup() {
  pinMode(PIN_BOTON, INPUT_PULLUP);   // entrada con resistencia interna a +5 V
  pinMode(LED_ROJO, OUTPUT);
  pinMode(LED_AMARILLO, OUTPUT);
}

void loop() {
  if (digitalRead(PIN_BOTON) == LOW) {   // presionado
    digitalWrite(LED_ROJO, HIGH);
    digitalWrite(LED_AMARILLO, LOW);
  } else {                               // suelto
    digitalWrite(LED_ROJO, LOW);
    digitalWrite(LED_AMARILLO, HIGH);
  }
}
