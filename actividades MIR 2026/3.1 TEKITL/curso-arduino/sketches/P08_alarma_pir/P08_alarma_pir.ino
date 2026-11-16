/*
  P08 · Alarma de movimiento (PIR + botón de armado + sirena)       Sesión 4
  ------------------------------------------------------------------
  Qué hace: un botón arma y desarma la alarma. Si está armada y el sensor PIR
  detecta movimiento, suena una sirena.

  Conexiones:
    Sensor PIR HC-SR501   VCC -> 5 V ; GND -> GND ; OUT -> pin 7
    Botón                 una pata -> pin 2 ; la pata del lado contrario -> GND
    LED                   pin 8 -> resistencia 220 ohm -> LED (+) ; pata corta -> GND
                          (LED encendido = alarma armada)
    Zumbador PASIVO       una pata -> pin 12 ; otra pata -> GND
                          (con tone() solo el pasivo cambia de tono; el activo suena siempre igual)

  Ideas clave:
    - Combina lo aprendido: variable de estado (como el botón con memoria) + sensor digital.
    - Según el fabricante, el PIR necesita casi un minuto para inicializarse al encender
      y en ese tiempo puede dar falsas detecciones. Por eso el programa espera 60 s.
      No te muevas frente a él. Mientras haces pruebas puedes bajar
      SEGUNDOS_CALENTAMIENTO, sabiendo que habrá falsas alarmas.
    - El módulo trae dos perillas pequeñas (sensibilidad y tiempo de retardo); pruébalas.
      Con retardo largo, la salida del PIR se queda en HIGH y la sirena se repite.
    - Para desarmar mientras suena, mantén presionado el botón hasta que calle.

  Retos:  - Cambia la sirena por otro sonido.
          - Agrega un código de 3 pulsaciones para desarmar (más difícil de burlar).
*/

const int PIN_PIR = 7;
const int PIN_BOTON = 2;
const int PIN_LED = 8;
const int PIN_ZUMBADOR = 12;
const int SEGUNDOS_CALENTAMIENTO = 60;

bool armada = false;
int botonAnterior = HIGH;

void pitidos(int cantidad) {
  for (int i = 0; i < cantidad; i++) {
    tone(PIN_ZUMBADOR, 2000, 100);
    delay(220);
  }
}

void sirena() {
  for (int i = 0; i < 6; i++) {
    if (digitalRead(PIN_BOTON) == LOW) {   // si presionan el botón, deja de sonar
      break;
    }
    tone(PIN_ZUMBADOR, 1500);
    delay(150);
    tone(PIN_ZUMBADOR, 900);
    delay(150);
  }
  noTone(PIN_ZUMBADOR);
}

void setup() {
  pinMode(PIN_PIR, INPUT);
  pinMode(PIN_BOTON, INPUT_PULLUP);
  pinMode(PIN_LED, OUTPUT);
  Serial.begin(9600);

  Serial.print("Calentando el sensor PIR (");
  Serial.print(SEGUNDOS_CALENTAMIENTO);
  Serial.println(" s). No te muevas frente a el.");
  for (int s = SEGUNDOS_CALENTAMIENTO; s > 0; s--) {   // el LED parpadea mientras se calienta
    digitalWrite(PIN_LED, HIGH);
    delay(100);
    digitalWrite(PIN_LED, LOW);
    delay(900);
  }
  Serial.println("Listo. Presiona el boton para armar la alarma.");
}

void loop() {
  // 1) El botón arma o desarma
  int botonActual = digitalRead(PIN_BOTON);
  if (botonAnterior == HIGH && botonActual == LOW) {
    armada = !armada;
    if (armada) {
      digitalWrite(PIN_LED, HIGH);
      pitidos(1);
      Serial.println("Alarma ARMADA");
    } else {
      digitalWrite(PIN_LED, LOW);
      pitidos(2);
      Serial.println("Alarma DESARMADA");
    }
    delay(30);                           // antirrebote
  }
  botonAnterior = botonActual;

  // 2) Si está armada y el PIR detecta movimiento, suena la sirena
  if (armada && digitalRead(PIN_PIR) == HIGH) {
    Serial.println("MOVIMIENTO DETECTADO");
    sirena();
  }
}
