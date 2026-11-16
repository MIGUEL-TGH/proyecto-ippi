/*
  P06 · Botón con memoria (un toque enciende, otro toque apaga)     Sesión 3
  ------------------------------------------------------------------
  Qué hace: cada vez que PRESIONAS el botón, el LED cambia de estado
  (encendido <-> apagado) y se cuenta la pulsación en el Monitor Serie.

  Conexiones: iguales a P05
    LED     pin 8 -> resistencia 220 ohm -> LED (pata larga +) ; pata corta (-) -> GND
    Botón   una pata -> pin 2 ; la pata del lado contrario -> GND

  Ideas clave:
    - Una variable de ESTADO (ledEncendido) recuerda lo que pasó antes.
    - Detectamos el MOMENTO en que el botón pasa de suelto a presionado
      comparando el estado anterior con el actual.
    - Antirrebote: al presionar, los contactos "rebotan" unos milisegundos.
      Esperamos 30 ms y volvemos a leer para no contar pulsaciones falsas.

  Cómo ver los mensajes: Herramientas -> Monitor Serie, velocidad 9600.

  Retos:  - Quita el delay(30) y presiona varias veces. ¿Qué pasa con el contador?
          - Que el LED parpadee 3 veces cada 5 pulsaciones.
*/

const int PIN_BOTON = 2;
const int PIN_LED = 8;

bool ledEncendido = false;   // el LED empieza apagado
int estadoAnterior = HIGH;   // el botón empieza suelto (HIGH por INPUT_PULLUP)
int pulsaciones = 0;         // cuántas veces se ha presionado

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
    }
    estadoAnterior = estadoActual;
  }
}
