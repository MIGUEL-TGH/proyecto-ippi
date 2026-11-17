/*
  P10 · Reto: el LED solo enciende pasada la mitad (solución del instructor)   Sesión 5
  ------------------------------------------------------------------
  Qué hace: en la primera mitad del giro el LED está apagado. Al pasar la mitad empieza
  a encender y llega al máximo en el tope.

  Conexiones: las mismas de P10
    Potenciómetro   extremo -> 5 V ; centro -> A0 ; otro extremo -> GND
    LED             pin 9 -> resistencia 220 ohm -> LED (pata larga +) ; pata corta -> GND

  Ideas clave:
    - map() puede usar solo una parte de la escala de entrada: aquí de 512 a 1023.
    - map() no recorta: con una lectura menor que 512 daría un número NEGATIVO. Por eso
      primero se pregunta con if si la lectura llegó a la mitad.
    - No es lo mismo que "encender o apagar según un umbral" (todo o nada): aquí el
      brillo sube poco a poco. El umbral se ve en la Sesión 6.
*/

const int PIN_PERILLA = A0;
const int PIN_LED = 9;
const int MITAD = 512;

void setup() {
  pinMode(PIN_LED, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int lectura = analogRead(PIN_PERILLA);           // 0 a 1023
  int brillo;                                      // se llena según el caso

  if (lectura < MITAD) {
    brillo = 0;                                    // antes de la mitad: apagado
  } else {
    brillo = map(lectura, MITAD, 1023, 0, 255);    // de la mitad al tope: de 0 a 255
  }
  analogWrite(PIN_LED, brillo);

  Serial.print("Lectura:");
  Serial.print(lectura);
  Serial.print(",Brillo:");
  Serial.println(brillo);
  delay(50);
}
