/*
  P07a · Reto: tres pitidos con "for" (solución del instructor)   Sesión 4
  ------------------------------------------------------------------
  Qué hace: lo mismo que P07a_zumbador_activo (tres pitidos cortos, pausa, un pitido largo),
  pero los tres pitidos cortos se escriben UNA sola vez y se repiten con un "for".

  Conexiones: las mismas de P07a
    Zumbador ACTIVO   pata + (la larga) -> pin 12 ; la otra pata -> GND

  Ideas clave:
    for (int i = 0; i < PITIDOS_CORTOS; i++) { ... }
         |          |                  |
         |          |                  +-- después de cada vuelta, suma 1 a i (i++ es i = i + 1)
         |          +-- mientras esto sea verdad, da otra vuelta
         +-- al empezar, i vale 0
    Con PITIDOS_CORTOS = 3 las vueltas son con i = 0, 1 y 2: tres vueltas.
    Para cambiar el número de pitidos se toca un solo lugar: la constante de arriba.
*/

const int PIN_ZUMBADOR = 12;
const int PITIDOS_CORTOS = 3;

void pitido(int duracion) {
  digitalWrite(PIN_ZUMBADOR, HIGH);
  delay(duracion);
  digitalWrite(PIN_ZUMBADOR, LOW);
  delay(150);                     // silencio breve entre pitidos
}

void setup() {
  pinMode(PIN_ZUMBADOR, OUTPUT);
}

void loop() {
  for (int i = 0; i < PITIDOS_CORTOS; i++) {   // repite lo de las llaves 3 veces
    pitido(100);
  }
  delay(800);
  pitido(600);
  delay(2000);
}
