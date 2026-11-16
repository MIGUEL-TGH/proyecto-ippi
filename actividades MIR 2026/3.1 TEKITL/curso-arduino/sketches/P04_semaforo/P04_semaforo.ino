/*
  P04 · Semáforo                                              Sesión 2
  ------------------------------------------------------------------
  Qué hace: simula un semáforo: verde, amarillo y rojo, cada uno con su tiempo.

  Conexiones (cada LED con su resistencia de 220 ohm, y la pata corta a GND):
    LED rojo      -> pin 8
    LED amarillo  -> pin 9
    LED verde     -> pin 10

  Ideas clave:
    - Las constantes con nombre (TIEMPO_VERDE...) hacen el programa fácil de leer y de cambiar.
    - Una FUNCIÓN es una receta con nombre. luces(...) enciende o apaga los tres LED
      de una sola vez, así no repetimos tres líneas cada vez.

  Retos:  - Cambia los tiempos para que el rojo dure el doble que el verde.
          - Haz que el verde parpadee 3 veces antes de pasar al amarillo.
          - Dibuja en tu cuaderno el diagrama de tiempos antes de programar.
*/

const int LED_ROJO = 8;
const int LED_AMARILLO = 9;
const int LED_VERDE = 10;

const int TIEMPO_VERDE = 4000;      // milisegundos
const int TIEMPO_AMARILLO = 1500;
const int TIEMPO_ROJO = 4000;

// Enciende (HIGH) o apaga (LOW) cada color
void luces(int rojo, int amarillo, int verde) {
  digitalWrite(LED_ROJO, rojo);
  digitalWrite(LED_AMARILLO, amarillo);
  digitalWrite(LED_VERDE, verde);
}

void setup() {
  pinMode(LED_ROJO, OUTPUT);
  pinMode(LED_AMARILLO, OUTPUT);
  pinMode(LED_VERDE, OUTPUT);
}

void loop() {
  luces(LOW, LOW, HIGH);        // solo verde
  delay(TIEMPO_VERDE);

  luces(LOW, HIGH, LOW);        // solo amarillo
  delay(TIEMPO_AMARILLO);

  luces(HIGH, LOW, LOW);        // solo rojo
  delay(TIEMPO_ROJO);
}
