/*
  P10 · Reto: brillo entre 20 y 200 (solución del instructor)     Sesión 5
  ------------------------------------------------------------------
  Qué hace: el LED nunca se apaga del todo ni llega al máximo: el brillo va de 20 a 200
  mientras la perilla recorre todo su giro.

  Conexiones: las mismas de P10
    Potenciómetro   extremo -> 5 V ; centro -> A0 ; otro extremo -> GND
    LED             pin 9 -> resistencia 220 ohm -> LED (pata larga +) ; pata corta -> GND

  Ideas clave:
    - Los dos últimos números de map() son el rango de SALIDA y pueden ser cualesquiera
      entre 0 y 255: aquí BRILLO_MIN y BRILLO_MAX, constantes con nombre.
    - Es la misma idea de "un cambio, un solo lugar" de la Sesión 2: para cambiar el
      rango se cambia una constante, no la fórmula.

  Para jugar: prueba BRILLO_MAX en 255 y BRILLO_MIN en 0. Debe verse como P10.
*/

const int PIN_PERILLA = A0;
const int PIN_LED = 9;
const int BRILLO_MIN = 20;
const int BRILLO_MAX = 200;

void setup() {
  pinMode(PIN_LED, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int lectura = analogRead(PIN_PERILLA);                              // 0 a 1023
  int brillo = map(lectura, 0, 1023, BRILLO_MIN, BRILLO_MAX);         // 0 -> 20 y 1023 -> 200
  analogWrite(PIN_LED, brillo);

  Serial.print("Lectura:");
  Serial.print(lectura);
  Serial.print(",Brillo:");
  Serial.println(brillo);
  delay(50);
}
