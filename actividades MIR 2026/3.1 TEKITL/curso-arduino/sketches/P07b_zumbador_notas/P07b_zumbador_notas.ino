/*
  P07b · Zumbador pasivo: notas musicales                     Sesión 4
  ------------------------------------------------------------------
  Qué hace: toca la escala Do-Re-Mi-Fa-Sol-La-Si-Do y se repite.

  Conexiones:
    Zumbador PASIVO   una pata -> resistencia de 220 ohm -> pin 12 ; la otra pata -> GND
    (En el kit es el disco negro liso con un orificio.)

  Por qué lleva resistencia: según su hoja de datos, el pasivo tiene 16 ohm. Con 5 V y sin
  resistencia pediría 5 V / 16 ohm = unos 310 mA como máximo, y un pin del UNO aguanta 40 mA.
  Con la resistencia de 220 ohm el máximo baja a unos 20 mA (como el LED de la Sesión 1).
  El pasivo NO suena solo con 5 V: necesita una señal que vibre. tone() la genera.

  Idea clave: el sonido es vibración. La frecuencia (en Hz) decide qué nota es:
  más Hz = más agudo. tone(pin, frecuencia, duracion) la produce.

  Si suena muy bajito: con la resistencia el volumen baja un poco. Las notas graves se oyen
  menos que las agudas: el manual del kit dice que este zumbador suena mejor con señales de
  2 000 a 5 000 Hz.

  Retos:  - Haz una sirena: sube y baja la frecuencia con un for (P07b_sirena_for).
          - Toca "Cumpleaños feliz" o una canción que conozcas (P07b_cumpleanos).
          - Haz que cada nota dure distinto tiempo.
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
