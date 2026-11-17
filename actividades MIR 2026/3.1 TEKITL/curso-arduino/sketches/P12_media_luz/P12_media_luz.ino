/*
  P12 · Reto: la lámpara enciende a media luz (solución del instructor)    Sesión 6
  ------------------------------------------------------------------
  Qué hace: igual que P12, pero al oscurecer el LED enciende a la MITAD de su brillo.

  Conexiones: las mismas de P12
    LDR + 10 kohm    5 V -> LDR -> punto medio -> 10 kohm -> GND ; punto medio -> A0
    Potenciómetro    extremo -> 5 V ; centro -> A1 ; otro extremo -> GND
    LED              pin 9 -> resistencia 220 ohm -> LED (+) ; pata corta -> GND

  Ideas clave:
    - Se cambia digitalWrite(PIN_LED, HIGH) por analogWrite(PIN_LED, BRILLO_NOCHE): solo se
      puede en un pin con ~ (el 9). 128 es la mitad de 255.
    - BRILLO_NOCHE es una constante: para cambiar el brillo se cambia un solo lugar.
*/

const int PIN_LDR = A0;
const int PIN_PERILLA = A1;
const int PIN_LED = 9;
const int BRILLO_NOCHE = 128;       // 0 a 255

void setup() {
  pinMode(PIN_LED, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int luz = analogRead(PIN_LDR);
  int umbral = analogRead(PIN_PERILLA);

  if (luz < umbral) {
    analogWrite(PIN_LED, BRILLO_NOCHE);   // oscuro: enciende a media luz
  } else {
    analogWrite(PIN_LED, 0);              // hay luz: apaga
  }

  Serial.print("luz:");
  Serial.print(luz);
  Serial.print(",umbral:");
  Serial.println(umbral);
  delay(100);
}
