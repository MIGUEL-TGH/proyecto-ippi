/*
  P10a · PWM "a mano": cómo se logra un brillo intermedio     Sesión 5
  ------------------------------------------------------------------
  Qué hace: enciende y apaga el LED con digitalWrite y delay, y la perilla reparte el
  ciclo entre "encendido" y "apagado". Es lo que hace analogWrite por dentro, pero
  despacio, para que se vea.

  Conexiones (las de P10):
    Potenciómetro   extremo -> 5 V ; centro -> A0 ; otro extremo -> GND
    LED             pin 9 -> resistencia 220 ohm -> LED (pata larga +) ; pata corta -> GND

  Ideas clave:
    - Un ciclo dura PERIODO_MS. Dentro del ciclo el LED está encendido "encendido"
      milisegundos y apagado el resto. La perilla decide cuánto de cada uno.
    - Con un ciclo largo (1000 ms) se ve el parpadeo: es el Blink de la Sesión 1 con
      la perilla decidiendo cuánto dura cada parte.
    - Con un ciclo corto (20 ms o menos) el ojo ya no ve el parpadeo: ve un brillo
      intermedio. Eso es PWM.
    - analogWrite hace lo mismo unas 490 veces por segundo, con un circuito propio del
      chip y SIN ocupar el programa. Aquí el programa no puede hacer otra cosa.
    - Este programa no escribe nada en el Monitor Serie: cada línea tardaría tanto como
      el propio ciclo y estropearía el efecto.

  Para jugar: cambia PERIODO_MS por 1000, 200, 100, 20 y 10, sube el programa cada vez,
  gira la perilla y anota en qué valor deja de verse el parpadeo.
*/

const int PIN_PERILLA = A0;
const int PIN_LED = 9;
const int PERIODO_MS = 1000;      // duración de un ciclo completo, en milisegundos

void setup() {
  pinMode(PIN_LED, OUTPUT);
}

void loop() {
  int lectura = analogRead(PIN_PERILLA);                    // 0 a 1023
  int encendido = map(lectura, 0, 1023, 0, PERIODO_MS);     // milisegundos con el LED prendido
  int apagado = PERIODO_MS - encendido;                     // el resto del ciclo

  digitalWrite(PIN_LED, HIGH);
  delay(encendido);
  digitalWrite(PIN_LED, LOW);
  delay(apagado);
}
