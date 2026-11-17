/*
  P19 · Reto: una tabla de temperatura cada minuto (solución del instructor)    Sesión 10
  ------------------------------------------------------------------
  Qué hace: escribe en el Monitor Serie la temperatura una vez por minuto, con su número de minuto:
  "Minuto 0: 24.6 C", "Minuto 1: 24.7 C"... Se copia al cuaderno durante la clase.

  Conexiones: las de P19
    5 V -> termistor NTC -> (punto medio) -> resistencia 10 kohm -> GND ; el punto medio al pin A0

  Ideas clave:
    - Una variable que cuenta: minuto = minuto + 1 en cada vuelta de loop().
    - Un delay largo (60 000 ms = 1 minuto) en lugar de uno corto. Mientras espera, el programa
      no hace otra cosa (la Sesión 11 enseña a esperar sin detenerlo).
*/

const int PIN_TERMISTOR = A0;
const float AJUSTE_C = 0.0;
const unsigned long ESPERA_MS = 60000;     // 1 minuto

int minuto = 0;

float leerTemperatura() {
  long suma = 0;
  for (int i = 0; i < 10; i++) {
    suma = suma + analogRead(PIN_TERMISTOR);
    delay(2);
  }
  float lectura = suma / 10.0;

  if (lectura < 1.0 || lectura > 1022.0) {
    return -273.0;                // sensor desconectado o en corto
  }

  // resistencia del termistor (el termistor va del lado de 5 V)
  float resistencia = 10000.0 * (1024.0 / lectura - 1.0);

  // ecuación de Steinhart-Hart con las constantes del kit
  float lnR = log(resistencia);
  float tempK = 1.0 / (0.001129148 + (0.000234125 + (0.0000000876741 * lnR * lnR)) * lnR);
  return tempK - 273.15 + AJUSTE_C;
}

void setup() {
  Serial.begin(9600);
}

void loop() {
  float temperatura = leerTemperatura();
  Serial.print("Minuto ");
  Serial.print(minuto);
  Serial.print(": ");
  if (temperatura < -200.0) {
    Serial.println("revisa la conexion del termistor");
  } else {
    Serial.print(temperatura, 1);
    Serial.println(" C");
  }
  minuto = minuto + 1;
  delay(ESPERA_MS);
}
