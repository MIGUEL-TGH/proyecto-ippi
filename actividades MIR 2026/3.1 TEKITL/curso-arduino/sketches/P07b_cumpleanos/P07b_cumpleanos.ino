/*
  P07b · Reto: "Cumpleaños feliz" (solución del instructor)        Sesión 4
  ------------------------------------------------------------------
  Qué hace: toca la melodía completa (unos 13 segundos) y la repite después de 5 segundos de pausa.

  Conexiones: las mismas de P07b
    Zumbador PASIVO   una pata -> resistencia de 220 ohm -> pin 12 ; la otra pata -> GND

  Ideas clave:
    - Cada nota es una llamada nota(FRECUENCIA, DURACION). La melodía es una lista de llamadas
      en orden, como una partitura.
    - La duración se escribe con nombres (CORTA, MEDIA, LARGA): para tocar más rápido o más
      lento se cambia un solo número. Es "un cambio, un solo lugar", como en la Sesión 2.
    - SIB (si bemol) es una nota nueva: 466 Hz, entre LA (440) y SI (494).
    - Notas más agudas = más Hz. DO_ALTO es el Do una octava arriba (523 Hz, casi el doble de DO).
    - Es una versión simplificada del ritmo: lo importante es que se reconozca.
*/

const int PIN_ZUMBADOR = 12;

const int DO = 262;
const int RE = 294;
const int MI = 330;
const int FA = 349;
const int SOL = 392;
const int LA = 440;
const int SIB = 466;
const int DO_ALTO = 523;

const int CORTA = 200;     // milisegundos
const int MEDIA = 400;
const int LARGA = 800;

void nota(int frecuencia, int duracion) {
  tone(PIN_ZUMBADOR, frecuencia, duracion);
  delay(duracion + duracion / 3);        // pausa breve entre notas
}

void setup() {
  pinMode(PIN_ZUMBADOR, OUTPUT);
}

void loop() {
  // "Cum-plea-ños fe-liz"
  nota(DO, CORTA);
  nota(DO, CORTA);
  nota(RE, MEDIA);
  nota(DO, MEDIA);
  nota(FA, MEDIA);
  nota(MI, LARGA);

  // "Cum-plea-ños fe-liz"
  nota(DO, CORTA);
  nota(DO, CORTA);
  nota(RE, MEDIA);
  nota(DO, MEDIA);
  nota(SOL, MEDIA);
  nota(FA, LARGA);

  // "Cum-plea-ños que-ri-do/a"
  nota(DO, CORTA);
  nota(DO, CORTA);
  nota(DO_ALTO, MEDIA);
  nota(LA, MEDIA);
  nota(FA, MEDIA);
  nota(MI, MEDIA);
  nota(RE, LARGA);

  // "Cum-plea-ños fe-liz"
  nota(SIB, CORTA);
  nota(SIB, CORTA);
  nota(LA, MEDIA);
  nota(FA, MEDIA);
  nota(SOL, MEDIA);
  nota(FA, LARGA);

  delay(5000);
}
