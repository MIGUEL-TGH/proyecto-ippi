/*
  P06 · Reto: parpadear 3 veces cada 5 pulsaciones (solución del instructor)     Sesión 3
  ------------------------------------------------------------------
  Qué hace: como P06 (cada pulsación enciende o apaga el LED y se cuenta en el Monitor Serie),
  pero en la pulsación 5, 10, 15... el LED parpadea 3 veces y después vuelve a como estaba.

  Conexiones: las mismas de P05 y P06
    LED rojo  pin 8 (con su resistencia de 220 ohm)
    Botón     pin 2 y GND, en patas opuestas (en diagonal)

  Ideas clave:
    - El operador % da el RESIDUO de una división: 5 % 5 = 0, 6 % 5 = 1, 10 % 5 = 0.
      Por eso "pulsaciones % 5 == 0" es verdad solo en 5, 10, 15...
    - La función parpadear3() junta las órdenes del parpadeo: las mismas cuatro líneas
      repetidas tres veces. En la Sesión 4 la instrucción "for" permite escribirlas una sola vez.
    - Mientras parpadea, el programa está en delay() y no mira el botón: un toque en ese
      momento se pierde. Se resuelve más adelante con millis().

  Cómo ver los mensajes: Herramientas -> Monitor Serie, velocidad 9600.
*/

const int PIN_BOTON = 2;
const int PIN_LED = 8;
const int TIEMPO_PARPADEO = 200;     // milisegundos encendido y milisegundos apagado

bool ledEncendido = false;           // el LED empieza apagado
int estadoAnterior = HIGH;           // el botón empieza suelto (HIGH por INPUT_PULLUP)
int pulsaciones = 0;                 // cuántas veces se ha presionado

// Parpadea 3 veces y deja el LED como estaba (según ledEncendido)
void parpadear3() {
  digitalWrite(PIN_LED, HIGH);
  delay(TIEMPO_PARPADEO);
  digitalWrite(PIN_LED, LOW);
  delay(TIEMPO_PARPADEO);

  digitalWrite(PIN_LED, HIGH);
  delay(TIEMPO_PARPADEO);
  digitalWrite(PIN_LED, LOW);
  delay(TIEMPO_PARPADEO);

  digitalWrite(PIN_LED, HIGH);
  delay(TIEMPO_PARPADEO);
  digitalWrite(PIN_LED, LOW);
  delay(TIEMPO_PARPADEO);

  if (ledEncendido) {                // devuelve el LED al estado que tenía
    digitalWrite(PIN_LED, HIGH);
  } else {
    digitalWrite(PIN_LED, LOW);
  }
}

void setup() {
  pinMode(PIN_BOTON, INPUT_PULLUP);
  pinMode(PIN_LED, OUTPUT);
  Serial.begin(9600);
  Serial.println("Listo. Presiona el boton.");
}

void loop() {
  int estadoActual = digitalRead(PIN_BOTON);

  if (estadoActual != estadoAnterior) {      // el botón cambió
    delay(30);                               // antirrebote
    estadoActual = digitalRead(PIN_BOTON);   // vuelve a leer

    if (estadoAnterior == HIGH && estadoActual == LOW) {   // acaba de presionarse
      ledEncendido = !ledEncendido;          // invierte el estado
      pulsaciones = pulsaciones + 1;

      if (ledEncendido) {
        digitalWrite(PIN_LED, HIGH);
      } else {
        digitalWrite(PIN_LED, LOW);
      }

      Serial.print("Pulsacion numero ");
      Serial.print(pulsaciones);
      Serial.print(" -> LED ");
      if (ledEncendido) {
        Serial.println("ENCENDIDO");
      } else {
        Serial.println("APAGADO");
      }

      if (pulsaciones % 5 == 0) {            // ¿es múltiplo de 5?
        Serial.println("Cinco pulsaciones: el LED parpadea 3 veces");
        parpadear3();
      }
    }
    estadoAnterior = estadoActual;
  }
}
