/*
  P10 · Reto: brillo invertido (solución del instructor)      Sesión 5
  ------------------------------------------------------------------
  Qué hace: al girar la perilla hacia donde antes subía el brillo, ahora baja.

  Conexiones: las mismas de P10
    Potenciómetro   extremo -> 5 V ; centro -> A0 ; otro extremo -> GND
    LED             pin 9 -> resistencia 220 ohm -> LED (pata larga +) ; pata corta -> GND

  Ideas clave:
    - map() acepta rangos "al revés": solo se cambia el orden de los dos últimos números.
      map(lectura, 0, 1023, 255, 0)  convierte 0 en 255 y 1023 en 0.
    - Es la segunda solución del fallo "los extremos del potenciómetro están cambiados":
      la primera era intercambiar los cables; esta lo arregla en el programa.
*/

const int PIN_PERILLA = A0;
const int PIN_LED = 9;

void setup() {
  pinMode(PIN_LED, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int lectura = analogRead(PIN_PERILLA);           // 0 a 1023
  int brillo = map(lectura, 0, 1023, 255, 0);      // 0 -> 255 y 1023 -> 0
  analogWrite(PIN_LED, brillo);

  Serial.print("Lectura:");
  Serial.print(lectura);
  Serial.print(",Brillo:");
  Serial.println(brillo);
  delay(50);
}
