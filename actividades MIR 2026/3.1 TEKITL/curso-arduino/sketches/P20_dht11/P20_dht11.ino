/*
  P20 · Temperatura y humedad con el sensor DHT11             Sesión 10
  ------------------------------------------------------------------
  Qué hace: lee temperatura y humedad relativa cada 2 segundos y las muestra en el
  Monitor Serie (velocidad 9600).

  Conexiones (módulo DHT11 de 3 pines; lee las letras impresas en TU módulo):
    S (señal) -> pin A0
    + (medio) -> 5 V   (riel rojo)
    - -> GND           (riel azul)

  Ideas clave:
    - El DHT11 es un sensor DIGITAL con su propio chip: manda los datos como una
      secuencia de pulsos que Arduino debe leer con mucha precisión de tiempo.
    - Esa lectura la hace la función leerDHT11() (adaptada del código del kit,
      lección 14): la usamos como "caja negra".
    - Manda 5 datos de 8 bits: humedad (entera y decimal), temperatura (entera y decimal) y una
      suma de verificación. Este programa usa solo las partes enteras.
    - Hoja del kit: temperatura de -20 a 60 grados con +-2 grados de precisión; humedad de 5 a 95 %
      con +-5 % de precisión.
    - No se puede leer más de una vez cada ~1-2 segundos.

  Pruebas: sopla suavemente al sensor (sube la humedad) y compáralo con el termistor (P19).

  Retos:  - Anota cuánto tarda en volver la humedad a su valor normal.
          - Calcula el promedio de 5 lecturas.
          - Compara con el termistor (P20_comparar_sensores: el termistor va en A1).
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

void setup() {
  Serial.begin(9600);
  Serial.println("DHT11 listo");
}

void loop() {
  byte humedad;
  byte temperatura;

  if (leerDHT11(humedad, temperatura)) {
    Serial.print("Temperatura: ");
    Serial.print(temperatura);
    Serial.print(" C    Humedad: ");
    Serial.print(humedad);
    Serial.println(" %");
  } else {
    Serial.println("Error al leer el DHT11. Revisa las conexiones.");
  }
  delay(2000);
}
