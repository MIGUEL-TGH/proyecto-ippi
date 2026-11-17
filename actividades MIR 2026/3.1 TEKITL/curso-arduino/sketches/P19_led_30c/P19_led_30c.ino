/*
  P19 · Reto: un LED que enciende a 30 grados (solución del instructor)    Sesión 10
  ------------------------------------------------------------------
  Qué hace: mide la temperatura con el termistor y enciende un LED si llega a 30 grados.

  Conexiones: las de P19
    5 V -> termistor NTC -> (punto medio) -> resistencia 10 kohm -> GND ; el punto medio al pin A0
    LED   pin 8 -> resistencia 220 ohm -> LED (pata larga +) ; pata corta -> GND

  Ideas clave:
    - Una decisión con umbral, como la lámpara de la Sesión 6, pero con grados en lugar de luz.
    - Si la temperatura anda justo en 30, el LED puede parpadear por el ruido de la lectura:
      la Sesión 12 enseña a evitarlo (histéresis).
    - Prueba: sostén el termistor entre los dedos hasta que pase de 30 grados y suéltalo.
*/

const int PIN_TERMISTOR = A0;
const int PIN_LED = 8;
const float AJUSTE_C = 0.0;       // corrección para igualar con un termómetro real
const float LIMITE_C = 30.0;      // el LED enciende a partir de esta temperatura

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
  pinMode(PIN_LED, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  float temperatura = leerTemperatura();
  if (temperatura < -200.0) {
    digitalWrite(PIN_LED, LOW);
    Serial.println("Revisa la conexion del termistor");
  } else {
    if (temperatura >= LIMITE_C) {
      digitalWrite(PIN_LED, HIGH);
    } else {
      digitalWrite(PIN_LED, LOW);
    }
    Serial.print("Temperatura: ");
    Serial.print(temperatura, 1);
    Serial.println(" C");
  }
  delay(500);
}
