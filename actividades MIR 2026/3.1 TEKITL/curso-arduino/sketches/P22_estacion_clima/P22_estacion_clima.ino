/*
  P22 · Estación de clima con pantalla LCD                    Sesión 11
  ------------------------------------------------------------------
  Qué hace: muestra la temperatura y la humedad del DHT11 en la pantalla LCD.

  Conexiones:
    LCD1602   igual que en P21 (RS 7, E 8, D4 9, D5 10, D6 11, D7 12, contraste con potenciómetro)
    DHT11     S -> pin A0 ; + -> 5 V ; - -> GND

  Ideas clave:
    - Juntamos dos "cajas negras": el sensor (leerDHT11) y la pantalla (LiquidCrystal).
    - Si el sensor falla, el programa avisa en la pantalla en lugar de mostrar datos falsos.

  Retos:  - Muestra también la temperatura que mide el termistor (P19) y compara las dos.
          - Alterna cada 3 segundos entre temperatura/humedad y un mensaje de tu equipo.
          - Agrega un LED que se encienda si la humedad pasa de 70 %.
*/

#include <LiquidCrystal.h>

#define DHT11_PIN 0                 // pin A0 (bit 0 del puerto C)

//                RS, E, D4, D5, D6, D7
LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

bool errorDHT11 = false;                    // se activa si el sensor deja de responder

byte leerByteDHT11() {
  byte resultado = 0;
  for (byte i = 0; i < 8; i++) {
    unsigned int espera = 0;
    while (!(PINC & _BV(DHT11_PIN))) {
      if (++espera > 20000) { errorDHT11 = true; return 0; }   // evita quedarse colgado
    }
    delayMicroseconds(30);
    if (PINC & _BV(DHT11_PIN)) {
      resultado |= (1 << (7 - i));
    }
    espera = 0;
    while (PINC & _BV(DHT11_PIN)) {
      if (++espera > 20000) { errorDHT11 = true; return 0; }
    }
  }
  return resultado;
}

bool leerDHT11(byte &humedad, byte &temperatura) {
  byte datos[5];
  errorDHT11 = false;

  DDRC |= _BV(DHT11_PIN);
  PORTC |= _BV(DHT11_PIN);
  PORTC &= ~_BV(DHT11_PIN);
  delay(18);
  PORTC |= _BV(DHT11_PIN);
  delayMicroseconds(40);
  DDRC &= ~_BV(DHT11_PIN);
  delayMicroseconds(40);

  if (PINC & _BV(DHT11_PIN)) {
    return false;
  }
  delayMicroseconds(80);
  if (!(PINC & _BV(DHT11_PIN))) {
    return false;
  }
  delayMicroseconds(80);

  for (byte i = 0; i < 5; i++) {
    datos[i] = leerByteDHT11();
  }

  DDRC |= _BV(DHT11_PIN);
  PORTC |= _BV(DHT11_PIN);

  if (errorDHT11) {
    return false;
  }
  byte suma = datos[0] + datos[1] + datos[2] + datos[3];
  if (datos[4] != suma) {
    return false;
  }
  humedad = datos[0];
  temperatura = datos[2];
  return true;
}

void setup() {
  lcd.begin(16, 2);
  lcd.print("Estacion clima");
  delay(1500);
  lcd.clear();
}

void loop() {
  byte humedad;
  byte temperatura;

  if (leerDHT11(humedad, temperatura)) {
    lcd.setCursor(0, 0);
    lcd.print("Temp: ");
    lcd.print(temperatura);
    lcd.print(" C     ");
    lcd.setCursor(0, 1);
    lcd.print("Humedad: ");
    lcd.print(humedad);
    lcd.print(" %   ");
  } else {
    lcd.setCursor(0, 0);
    lcd.print("Error del sensor");
    lcd.setCursor(0, 1);
    lcd.print("Revisa cables   ");
  }
  delay(2000);                      // el DHT11 necesita al menos 1-2 s entre lecturas
}
