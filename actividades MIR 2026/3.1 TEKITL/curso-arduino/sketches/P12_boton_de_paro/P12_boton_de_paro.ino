/*
  P12 · Reto: botón de paro (solución del instructor)         Sesión 6
  ------------------------------------------------------------------
  Qué hace: la lámpara de P12, con un botón: un toque la apaga aunque esté oscuro ("paro")
  y otro toque la deja otra vez en automático.

  Conexiones: las de P12 y un botón
    LDR + 10 kohm    5 V -> LDR -> punto medio -> 10 kohm -> GND ; punto medio -> A0
    Potenciómetro    extremo -> 5 V ; centro -> A1 ; otro extremo -> GND
    LED              pin 9 -> resistencia 220 ohm -> LED (+) ; pata corta -> GND
    Botón            una pata -> pin 2 ; la pata OPUESTA (en diagonal) -> GND

  Ideas clave:
    - Es la variable de estado de la Sesión 3: "automatico" recuerda en qué modo está la lámpara.
    - Se detecta el MOMENTO en que se presiona el botón (de HIGH a LOW), igual que en P06,
      para que un toque largo no cambie el modo varias veces.
    - Une las Sesiones 3 y 6 (es el "proyecto 3" del manual: botón de paro + LDR).
*/

const int PIN_LDR = A0;
const int PIN_PERILLA = A1;
const int PIN_LED = 9;
const int PIN_BOTON = 2;

bool automatico = true;             // true = la lámpara decide sola; false = parada
int botonAnterior = HIGH;           // con INPUT_PULLUP, HIGH = suelto

void setup() {
  pinMode(PIN_LED, OUTPUT);
  pinMode(PIN_BOTON, INPUT_PULLUP);
  Serial.begin(9600);
}

void loop() {
  int botonActual = digitalRead(PIN_BOTON);
  if (botonAnterior == HIGH && botonActual == LOW) {   // acaban de presionarlo
    automatico = !automatico;
    if (automatico) {
      Serial.println("Modo AUTOMATICO");
    } else {
      Serial.println("Modo PARO");
    }
    delay(30);                                         // antirrebote sencillo
  }
  botonAnterior = botonActual;

  int luz = analogRead(PIN_LDR);
  int umbral = analogRead(PIN_PERILLA);

  if (automatico && luz < umbral) {
    digitalWrite(PIN_LED, HIGH);
  } else {
    digitalWrite(PIN_LED, LOW);
  }
  delay(20);
}
