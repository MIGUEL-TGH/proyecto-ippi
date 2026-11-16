/*
  P10 · Perilla que controla el brillo de un LED              Sesión 5
  ------------------------------------------------------------------
  Qué hace: al girar el potenciómetro, el LED brilla más o menos.

  Conexiones:
    Potenciómetro   extremo -> 5 V ; centro -> A0 ; otro extremo -> GND
    LED             pin 9 -> resistencia 220 ohm -> LED (pata larga +) ; pata corta -> GND
                    (usamos el pin 9 porque tiene el símbolo ~ : permite PWM)

  Ideas clave:
    - Arduino no puede dar 2.5 V en un pin digital. Usa PWM: enciende y apaga el pin
      muy rápido (cientos de veces por segundo). Si pasa más tiempo encendido, el LED
      parece más brillante. analogWrite(pin, 0 a 255) elige qué porción del tiempo
      está encendido.
    - map() cambia un número de una escala a otra: de 0-1023 (lectura) a 0-255 (PWM).

  Retos:  - Haz que la perilla controle el brillo al revés.
          - Cambia el LED por otro color. ¿Se ve igual de brillante?
          - Haz que el LED solo se encienda cuando la perilla pase de la mitad.
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

  Serial.print("Lectura: ");
  Serial.print(lectura);
  Serial.print("    Brillo: ");
  Serial.println(brillo);
  delay(50);
}
