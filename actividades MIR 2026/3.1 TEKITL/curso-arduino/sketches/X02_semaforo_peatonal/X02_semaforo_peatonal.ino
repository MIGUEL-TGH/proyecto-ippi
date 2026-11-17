/*
  X02 · Semáforo con botón para peatones                      Ampliación (reto de las sesiones 2 y 3)
  ------------------------------------------------------------------
  Qué hace: los autos tienen verde. Si un peatón presiona el botón, el semáforo pasa a
  amarillo y luego a rojo; se enciende el LED azul de peatón y suena un pitido mientras
  cruzan. Después vuelve a verde.

  Conexiones (cada LED con resistencia de 220 ohm, pata corta a GND):
    LED rojo -> pin 8   LED amarillo -> pin 9   LED verde -> pin 10   LED azul (peatón) -> pin 11
    Botón: una pata -> pin 2 ; la pata OPUESTA (en diagonal) -> GND
    Zumbador PASIVO: una pata -> pin 12 ; otra pata -> GND   (tone() necesita el pasivo)

  Ideas clave:
    - Mientras se "espera", el programa debe seguir mirando el botón. Por eso usamos
      esperar(): en lugar de delay, revisa el botón todo el tiempo y recuerda la petición
      en la variable peatonSolicita.
    - millis() es el reloj interno: milisegundos desde que se encendió el Arduino.

  Retos:  - Que el LED de peatón parpadee en los últimos 2 segundos.
          - Dibuja primero la máquina de estados en papel (verde, amarillo, rojo + peatón).
*/

const int LED_ROJO = 8;
const int LED_AMARILLO = 9;
const int LED_VERDE = 10;
const int LED_PEATON = 11;
const int PIN_BOTON = 2;
const int PIN_ZUMBADOR = 12;

const unsigned long TIEMPO_VERDE_MINIMO = 5000;
const unsigned long TIEMPO_AMARILLO = 1500;
const int PITIDOS_CRUCE = 10;           // 10 pitidos de 500 ms = 5 segundos

bool peatonSolicita = false;

void luces(int rojo, int amarillo, int verde, int peaton) {
  digitalWrite(LED_ROJO, rojo);
  digitalWrite(LED_AMARILLO, amarillo);
  digitalWrite(LED_VERDE, verde);
  digitalWrite(LED_PEATON, peaton);
}

// Espera "ms" milisegundos sin dejar de mirar el botón
void esperar(unsigned long ms) {
  unsigned long inicio = millis();
  while (millis() - inicio < ms) {
    if (digitalRead(PIN_BOTON) == LOW) {
      peatonSolicita = true;
    }
  }
}

void setup() {
  pinMode(LED_ROJO, OUTPUT);
  pinMode(LED_AMARILLO, OUTPUT);
  pinMode(LED_VERDE, OUTPUT);
  pinMode(LED_PEATON, OUTPUT);
  pinMode(PIN_BOTON, INPUT_PULLUP);
  pinMode(PIN_ZUMBADOR, OUTPUT);
}

void loop() {
  // Autos avanzan: verde al menos 5 segundos
  peatonSolicita = false;
  luces(LOW, LOW, HIGH, LOW);
  esperar(TIEMPO_VERDE_MINIMO);

  // Se queda en verde hasta que alguien pida cruzar
  while (!peatonSolicita) {
    if (digitalRead(PIN_BOTON) == LOW) {
      peatonSolicita = true;
    }
  }

  // Amarillo y luego rojo para autos
  luces(LOW, HIGH, LOW, LOW);
  delay(TIEMPO_AMARILLO);

  // Peatones cruzan, con pitidos
  luces(HIGH, LOW, LOW, HIGH);
  for (int i = 0; i < PITIDOS_CRUCE; i++) {
    tone(PIN_ZUMBADOR, 1500, 200);
    delay(500);
  }
}
