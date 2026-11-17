/*
  P10 · Perilla que controla el brillo de un LED              Sesión 5
  ------------------------------------------------------------------
  Qué hace: al girar el potenciómetro, el LED brilla más o menos.

  Conexiones (las de P09 y el LED del Paso 0):
    Potenciómetro   extremo -> 5 V ; centro -> A0 ; otro extremo -> GND
    LED             pin 9 -> resistencia 220 ohm -> LED (pata larga +) ; pata corta -> GND
                    (usamos el pin 9 porque tiene el símbolo ~ : permite PWM)

  Ideas clave:
    - Arduino no puede dar 2.5 V en un pin digital. Usa PWM: enciende y apaga el pin
      muy rápido (unas 490 veces por segundo). Si pasa más tiempo encendido, el LED
      parece más brillante. analogWrite(pin, 0 a 255) elige qué porción del tiempo
      está encendido.
    - Solo los pines con ~ hacen PWM en el UNO: 3, 5, 6, 9, 10 y 11.
    - analogWrite no tiene nada que ver con los pines analógicos A0 a A5: esos solo LEEN.
    - map() cambia un número de una escala a otra: de 0-1023 (lectura) a 0-255 (PWM).
      map(valor, desdeMin, desdeMax, haciaMin, haciaMax)

  Cómo verlo: Herramientas -> Serial Plotter (velocidad 9600) dibuja dos líneas:
  "Lectura" (0 a 1023) y "Brillo" (0 a 255). Tienen la misma forma, en distinta escala.
  También se lee bien en el Monitor Serie.

  Retos:  - Haz que la perilla controle el brillo al revés.
          - Haz que el LED solo se encienda cuando la perilla pase de la mitad.
          - Haz que el brillo nunca baje de 20 ni suba de 200.
          - Cambia el LED por otro color. ¿Se ve igual de brillante?
          - Desafío: un LED que "respira" solo, sin perilla (con for).
*/

const int PIN_PERILLA = A0;
const int PIN_LED = 9;          // pin con ~ (PWM)

void setup() {
  pinMode(PIN_LED, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int lectura = analogRead(PIN_PERILLA);          // 0 a 1023
  int brillo = map(lectura, 0, 1023, 0, 255);     // 0 a 255
  analogWrite(PIN_LED, brillo);

  Serial.print("Lectura:");                       // formato nombre:valor, para el Serial Plotter
  Serial.print(lectura);
  Serial.print(",Brillo:");
  Serial.println(brillo);
  delay(50);
}
