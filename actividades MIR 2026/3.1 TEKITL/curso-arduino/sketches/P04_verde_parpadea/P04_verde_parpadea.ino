/*
  P04 · Reto: el verde parpadea antes del amarillo (solución del instructor)   Sesión 2
  ------------------------------------------------------------------
  Qué hace: semáforo como P04, pero al terminar el tiempo del verde, el verde parpadea
  3 veces antes de pasar al amarillo (como avisa un semáforo real).

  Conexiones: las mismas de P04 (rojo pin 8, amarillo pin 9, verde pin 10, cada uno con 220 ohm).

  Ideas clave:
    - La función luces(...) evita escribir tres digitalWrite cada vez.
    - Repetir las mismas líneas seis veces funciona, pero es largo y se presta a errores.
      Más adelante (Sesión 4) la instrucción "for" permite repetir sin copiar y pegar.
*/

const int LED_ROJO = 8;
const int LED_AMARILLO = 9;
const int LED_VERDE = 10;

const int TIEMPO_VERDE = 4000;      // milisegundos
const int TIEMPO_AMARILLO = 1500;
const int TIEMPO_ROJO = 4000;
const int TIEMPO_PARPADEO = 300;    // cada destello (encendido o apagado) del verde

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
  luces(LOW, LOW, HIGH);            // verde fijo
  delay(TIEMPO_VERDE);

  // el verde parpadea 3 veces (apaga-enciende, apaga-enciende, apaga-enciende)
  luces(LOW, LOW, LOW);
  delay(TIEMPO_PARPADEO);
  luces(LOW, LOW, HIGH);
  delay(TIEMPO_PARPADEO);

  luces(LOW, LOW, LOW);
  delay(TIEMPO_PARPADEO);
  luces(LOW, LOW, HIGH);
  delay(TIEMPO_PARPADEO);
  
  luces(LOW, LOW, LOW);
  delay(TIEMPO_PARPADEO);
  luces(LOW, LOW, HIGH);
  delay(TIEMPO_PARPADEO);

  luces(LOW, HIGH, LOW);            // solo amarillo
  delay(TIEMPO_AMARILLO);

  luces(HIGH, LOW, LOW);            // solo rojo
  delay(TIEMPO_ROJO);
}
