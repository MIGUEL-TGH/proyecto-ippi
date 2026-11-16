/*
  P19 · Termómetro con termistor NTC                          Sesión 10
  ------------------------------------------------------------------
  Qué hace: mide la temperatura con el termistor y la muestra en grados Celsius
  en el Monitor Serie.

  Conexiones (divisor de voltaje, igual que el LDR):
    5 V -> termistor NTC -> (punto medio) -> resistencia 10 kohm -> GND
    El punto medio va al pin A0.   (el termistor no tiene polaridad)

  Ideas clave:
    - El NTC baja su resistencia cuando sube la temperatura (NTC = coeficiente negativo).
    - Su resistencia NO cambia en línea recta: por eso se usa la ecuación de
      Steinhart-Hart. Aquí la tratamos como una "caja negra": entra la resistencia,
      sale la temperatura. Estas constantes son las del código del kit (termistor de 10 k).
    - Promediar 10 lecturas reduce el ruido.
    - Calibración: compara con un termómetro de verdad. Si el tuyo marca 2 grados de más,
      escribe -2.0 en AJUSTE_C.

  Pruebas: sostén el termistor entre los dedos (sube), ponlo cerca de un vaso con agua fría
  (baja). No lo mojes ni lo calientes con flama.

  Retos:  - Anota la temperatura ambiente y la de tu dedo.
          - Haz que un LED se encienda si pasa de 30 grados.
*/

const int PIN_TERMISTOR = A0;
const float AJUSTE_C = 0.0;       // corrección para igualar con un termómetro real

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
  if (temperatura < -200.0) {
    Serial.println("Revisa la conexion del termistor");
  } else {
    Serial.print("Temperatura: ");
    Serial.print(temperatura, 1);
    Serial.println(" C");
  }
  delay(500);
}
