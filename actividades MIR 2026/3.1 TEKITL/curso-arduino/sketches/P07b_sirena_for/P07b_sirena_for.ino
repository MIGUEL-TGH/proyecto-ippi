/*
  P07b · Reto: sirena con "for" (solución del instructor)         Sesión 4
  ------------------------------------------------------------------
  Qué hace: el tono sube de 800 a 2400 Hz, baja de nuevo, y descansa 2 segundos.

  Conexiones: las mismas de P07b
    Zumbador PASIVO   una pata -> resistencia de 220 ohm -> pin 12 ; la otra pata -> GND

  Ideas clave:
    - Aquí el contador del "for" no cuenta vueltas: ES la frecuencia. f arranca en
      FREC_BAJA y sube de 20 en 20 hasta llegar a FREC_ALTA.
    - Para bajar se cuenta al revés: f arranca arriba, se le RESTA PASO en cada vuelta
      y el "for" sigue mientras f >= FREC_BAJA.
    - tone(pin, f) sin duración suena hasta que se llame a noTone() o se cambie la nota.
    - Cada subida o bajada tiene (2400 - 800) / 20 = 80 vueltas de 10 ms = 0,8 segundos.

  Para jugar: cambia PASO (más grande = sube a saltos), el delay(10) (más grande = más lenta)
  o los límites FREC_BAJA y FREC_ALTA.
*/

const int PIN_ZUMBADOR = 12;
const int FREC_BAJA = 800;     // Hz
const int FREC_ALTA = 2400;    // Hz
const int PASO = 20;           // Hz que cambia en cada vuelta

void setup() {
  pinMode(PIN_ZUMBADOR, OUTPUT);
}

void loop() {
  for (int f = FREC_BAJA; f <= FREC_ALTA; f = f + PASO) {   // sube
    tone(PIN_ZUMBADOR, f);
    delay(10);
  }
  for (int f = FREC_ALTA; f >= FREC_BAJA; f = f - PASO) {   // baja
    tone(PIN_ZUMBADOR, f);
    delay(10);
  }
  noTone(PIN_ZUMBADOR);
  delay(2000);
}
