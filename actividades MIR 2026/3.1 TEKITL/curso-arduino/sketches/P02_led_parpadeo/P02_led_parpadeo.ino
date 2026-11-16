/*
  P02 · LED externo que parpadea                              Sesión 1
  ------------------------------------------------------------------
  Qué hace: el LED conectado al pin 8 se enciende un segundo y se apaga otro segundo.

  Conexiones:
    LED       pata larga (+)  -> resistencia de 220 ohm -> pin 8
              pata corta (-)  -> GND
  (La resistencia protege al LED: sin ella se puede quemar.)

  Paso 1: sube el código tal como está y observa.
  Paso 2: quita todo lo que hay dentro de loop() y deja solo digitalWrite(pinLed, HIGH);
          ¿Qué pasa ahora? (el LED queda encendido fijo)
  Retos:  - Haz que parpadee más rápido y más lento.
          - Haz que el LED esté encendido poco tiempo y apagado mucho tiempo.
          - Escribe una señal de SOS (3 cortos, 3 largos, 3 cortos).
*/

int pinLed = 8;   // "pinLed" es un nombre que le damos al número 8

void setup() {
  pinMode(pinLed, OUTPUT);     // el pin 8 va a mandar energía (salida)
}

void loop() {
  digitalWrite(pinLed, HIGH);  // enciende el LED
  delay(1000);                 // espera 1000 milisegundos (1 segundo)
  digitalWrite(pinLed, LOW);   // apaga el LED
  delay(1000);
}
