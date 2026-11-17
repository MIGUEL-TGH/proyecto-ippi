/*
  P06 · Reto de cierre: semáforo con botón para peatones (solución del instructor)   Sesión 3
  ------------------------------------------------------------------
  Qué hace: los autos tienen verde. Si alguien presiona el botón, el semáforo pasa a amarillo,
  luego a rojo para que crucen los peatones, y después vuelve a verde.

  Conexiones: las de P05 (el semáforo de P04 más el botón)
    LED rojo pin 8 · LED amarillo pin 9 · LED verde pin 10  (cada uno con su resistencia de 220 ohm)
    Botón    pin 2 y GND, en patas opuestas (en diagonal)

  Ideas clave:
    - Junta lo de la Sesión 2 (la función luces) con lo de la Sesión 3 (leer el botón con if).
    - Limitación: durante la secuencia el programa está en delay() y no mira el botón. Un toque
      mientras el semáforo está en amarillo o en rojo se pierde. La ampliación X02_semaforo_peatonal
      lo resuelve con millis(): es buena pregunta para el grupo ("¿por qué no hizo caso?").
    - Si se mantiene presionado el botón, la secuencia se repite al terminar.
*/

const int LED_ROJO = 8;
const int LED_AMARILLO = 9;
const int LED_VERDE = 10;
const int PIN_BOTON = 2;

const int TIEMPO_AMARILLO = 1500;   // milisegundos
const int TIEMPO_ROJO = 5000;

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
  pinMode(PIN_BOTON, INPUT_PULLUP);
}

void loop() {
  luces(LOW, LOW, HIGH);                  // verde fijo: pasan los autos

  if (digitalRead(PIN_BOTON) == LOW) {    // alguien pidió cruzar
    luces(LOW, HIGH, LOW);                // amarillo: aviso
    delay(TIEMPO_AMARILLO);

    luces(HIGH, LOW, LOW);                // rojo: cruzan los peatones
    delay(TIEMPO_ROJO);
  }
}
