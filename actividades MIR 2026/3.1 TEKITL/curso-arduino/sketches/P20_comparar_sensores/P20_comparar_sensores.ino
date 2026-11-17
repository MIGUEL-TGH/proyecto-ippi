/*
  P20 · Comparar el termistor con el DHT11 (solución de la parte 2)    Sesión 10
  ------------------------------------------------------------------
  Qué hace: lee la temperatura con los DOS sensores a la vez y escribe las dos, y su diferencia,
  en el Monitor Serie (velocidad 9600) o en el Serial Plotter.

  Conexiones:
    DHT11      S -> pin A0 ; + -> 5 V ; - -> GND   (lee las letras de tu módulo)
    Termistor  5 V -> termistor NTC -> (punto medio) -> resistencia 10 kohm -> GND ;
               el punto medio al pin A1  (OTRO pin: el DHT11 ya usa A0)

  Ideas clave:
    - Dos sensores de temperatura de distinto tipo: el termistor es ANALÓGICO (se calcula con la
      ecuación) y el DHT11 es DIGITAL (el chip manda el número ya hecho, solo en grados enteros).
    - Ninguno es "la verdad": se comparan entre sí y con un termómetro de referencia.
    - Se escribe con nombre y dos puntos (Termistor:24.8,DHT11:25,Diferencia:-0.2) para que el
      Serial Plotter dibuje las líneas.

  Retos:  - Compara los dos con un termómetro de verdad y ajusta AJUSTE_C.
          - Calienta los dos sensores a la vez con la mano. ¿Cuál reacciona más rápido?
*/

#define DHT11_PIN 0                 // pin A0 (bit 0 del puerto C)

bool errorDHT11 = false;                    // se activa si el sensor deja de responder

// Lee un byte (8 bits) del sensor
byte leerByteDHT11() {
  byte resultado = 0;
  for (byte i = 0; i < 8; i++) {
    unsigned int espera = 0;
    while (!(PINC & _BV(DHT11_PIN))) {      // espera que la línea suba
      if (++espera > 20000) { errorDHT11 = true; return 0; }   // evita quedarse colgado
    }
    delayMicroseconds(30);
    if (PINC & _BV(DHT11_PIN)) {
      resultado |= (1 << (7 - i));          // el pulso largo es un 1
    }
    espera = 0;
    while (PINC & _BV(DHT11_PIN)) {         // espera que termine el pulso
      if (++espera > 20000) { errorDHT11 = true; return 0; }
    }
  }
  return resultado;
}

// Devuelve true si la lectura fue buena. Entrega humedad y temperatura enteras.
bool leerDHT11(byte &humedad, byte &temperatura) {
  byte datos[5];
  errorDHT11 = false;

  // Señal de inicio: bajar la línea 18 ms y soltarla
  DDRC |= _BV(DHT11_PIN);
  PORTC |= _BV(DHT11_PIN);
  PORTC &= ~_BV(DHT11_PIN);
  delay(18);
  PORTC |= _BV(DHT11_PIN);
  delayMicroseconds(40);
  DDRC &= ~_BV(DHT11_PIN);
  delayMicroseconds(40);

  if (PINC & _BV(DHT11_PIN)) {              // el sensor debe responder con un 0
    return false;
  }
  delayMicroseconds(80);
  if (!(PINC & _BV(DHT11_PIN))) {           // y luego con un 1
    return false;
  }
  delayMicroseconds(80);

  for (byte i = 0; i < 5; i++) {
    datos[i] = leerByteDHT11();
  }

  DDRC |= _BV(DHT11_PIN);                   // deja la línea en reposo (alta)
  PORTC |= _BV(DHT11_PIN);

  if (errorDHT11) {
    return false;
  }
  byte suma = datos[0] + datos[1] + datos[2] + datos[3];
  if (datos[4] != suma) {                   // verificación de errores
    return false;
  }
  humedad = datos[0];
  temperatura = datos[2];
  return true;
}

const int PIN_TERMISTOR = A1;
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
  byte humedad;
  byte temperaturaDHT;
  float temperaturaNTC = leerTemperatura();

  if (leerDHT11(humedad, temperaturaDHT) && temperaturaNTC > -200.0) {
    Serial.print("Termistor:");
    Serial.print(temperaturaNTC, 1);
    Serial.print(",DHT11:");
    Serial.print(temperaturaDHT);
    Serial.print(",Diferencia:");
    Serial.println(temperaturaNTC - temperaturaDHT, 1);
  } else {
    Serial.println("Sin lectura: revisa las conexiones de los dos sensores");
  }
  delay(2000);                      // el DHT11 necesita al menos 1-2 s entre lecturas
}
