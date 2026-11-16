/*
  P07b · Zumbador pasivo: notas musicales                     Sesión 4
  ------------------------------------------------------------------
  Qué hace: toca la escala Do-Re-Mi-Fa-Sol-La-Si-Do y se repite.

  Conexiones:
    Zumbador PASIVO   una pata -> pin 12 ; la otra pata -> GND
    (El pasivo NO suena solo con 5 V: necesita una señal que vibre.
     tone() genera esa señal a la frecuencia que le pidas.)

  Idea clave: el sonido es vibración. La frecuencia (en Hz) decide qué nota es:
  más Hz = más agudo. tone(pin, frecuencia, duracion) la produce.

  Retos:  - Toca "Cumpleaños feliz" o una canción que conozcas (busca las frecuencias).
          - Haz que cada nota dure distinto tiempo.
          - Haz una sirena: sube y baja la frecuencia con un for.
*/

const int PIN_ZUMBADOR = 12;

const int DO = 262;
const int RE = 294;
const int MI = 330;
const int FA = 349;
const int SOL = 392;
const int LA = 440;
const int SI = 494;
const int DO_ALTO = 523;

// Toca una nota y espera un poco más para dejar un silencio entre notas
void nota(int frecuencia, int duracion) {
  tone(PIN_ZUMBADOR, frecuencia, duracion);
  delay(duracion + duracion / 3);
}

void setup() {
  pinMode(PIN_ZUMBADOR, OUTPUT);
}

void loop() {
  nota(DO, 400);
  nota(RE, 400);
  nota(MI, 400);
  nota(FA, 400);
  nota(SOL, 400);
  nota(LA, 400);
  nota(SI, 400);
  nota(DO_ALTO, 800);
  delay(2000);
}
