/*
  P10 · Reto: LED que "respira" (solución del instructor)         Sesión 5
  ------------------------------------------------------------------
  Qué hace: el LED sube poco a poco de apagado a su máximo brillo y baja de nuevo, sin
  perilla. Un ciclo dura un poco más de dos segundos.

  Conexiones (solo el LED de P10; la perilla no se usa)
    LED             pin 9 -> resistencia 220 ohm -> LED (pata larga +) ; pata corta -> GND

  Ideas clave:
    - Igual que en la sirena de la Sesión 4, el contador del "for" no cuenta vueltas:
      ES el brillo. Arranca en 0 y sube de PASO en PASO hasta 255.
    - Para bajar se cuenta al revés: arranca en 255, se le RESTA PASO y el "for" sigue
      mientras brillo >= 0.
    - Cada subida o bajada tiene 255 / 5 = 51 pasos de 20 ms, es decir, un poco más de un
      segundo.

  Para jugar: cambia PASO (más grande = a saltos) o PAUSA_MS (más grande = más lento).
*/

const int PIN_LED = 9;
const int PASO = 5;            // cuánto cambia el brillo en cada vuelta
const int PAUSA_MS = 20;       // milisegundos entre un brillo y el siguiente

void setup() {
  pinMode(PIN_LED, OUTPUT);
}

void loop() {
  for (int brillo = 0; brillo <= 255; brillo = brillo + PASO) {     // sube
    analogWrite(PIN_LED, brillo);
    delay(PAUSA_MS);
  }
  for (int brillo = 255; brillo >= 0; brillo = brillo - PASO) {     // baja
    analogWrite(PIN_LED, brillo);
    delay(PAUSA_MS);
  }
}
