/*
  P17 · Reto: un toque enciende y otro apaga (solución del instructor)    Sesión 9
  ------------------------------------------------------------------
  Qué hace: un toque al botón enciende la carga (LED o, cuando se destrabe, motor) y el
  siguiente toque la apaga. Es el LED con memoria de la Sesión 3, pero a través del transistor.

  Conexiones: las mismas de P17
    PN2222   emisor -> GND ; base -> resistencia 330 ohm -> pin 5 ; colector -> carga
    LED      pata larga (+) -> resistencia 220 ohm -> 5 V ; pata corta (-) -> colector
    Botón    una pata -> pin 2 ; la pata opuesta (en diagonal) -> GND

  Ideas clave:
    - La variable de estado "encendida" recuerda si la carga está prendida (Sesión 3).
    - Se detecta el MOMENTO en que se presiona el botón (de HIGH a LOW).
*/

const int PIN_BOTON = 2;
const int PIN_CARGA = 5;

bool encendida = false;
int botonAnterior = HIGH;

void setup() {
  pinMode(PIN_BOTON, INPUT_PULLUP);
  pinMode(PIN_CARGA, OUTPUT);
}

void loop() {
  int botonActual = digitalRead(PIN_BOTON);
  if (botonAnterior == HIGH && botonActual == LOW) {   // acaban de presionarlo
    encendida = !encendida;
    delay(30);                                         // antirrebote sencillo
  }
  botonAnterior = botonActual;

  if (encendida) {
    digitalWrite(PIN_CARGA, HIGH);
  } else {
    digitalWrite(PIN_CARGA, LOW);
  }
}
