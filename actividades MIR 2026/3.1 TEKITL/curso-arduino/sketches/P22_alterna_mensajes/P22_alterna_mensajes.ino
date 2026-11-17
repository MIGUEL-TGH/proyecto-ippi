/*
  P22 · Reto: alternar entre los datos y un mensaje del equipo (solución del instructor)    Sesión 11
  ------------------------------------------------------------------
  Qué hace: cada 3 lecturas del DHT11 (unos 6 segundos) alterna entre temperatura y humedad
  y un mensaje del equipo en la pantalla.

  Conexiones: las de P22
    LCD1602   RS 12, E 11, D4 10, D5 9, D6 8, D7 7, contraste con potenciómetro, luz de fondo con 100 ohm
    DHT11     S -> pin A0 ; + -> 5 V ; - -> GND

  Ideas clave:
    - Una variable que cuenta vueltas (vuelta) y la pregunta "vuelta % 2": el resto de dividir
      entre 2 es 0 en las vueltas pares y 1 en las impares. Es el operador % (resto).
    - Cada vuelta dura 3 segundos, así que el mensaje cambia cada 3 s.
*/

#include <LiquidCrystal.h>

#define DHT11_PIN 0                 // pin A0 (bit 0 del puerto C)

//                RS, E, D4, D5, D6, D7
LiquidCrystal lcd(12, 11, 10, 9, 8, 7);

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

int vuelta = 0;

void setup() {
  lcd.begin(16, 2);
  lcd.print("Estacion clima");
  delay(1500);
  lcd.clear();
}

void loop() {
  byte humedad;
  byte temperatura;

  if (vuelta % 2 == 0) {                  // vueltas pares: los datos del sensor
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
  } else {                                // vueltas impares: el mensaje del equipo
    lcd.setCursor(0, 0);
    lcd.print("Equipo 1        ");
    lcd.setCursor(0, 1);
    lcd.print("Curso de Arduino");
  }
  vuelta = vuelta + 1;
  delay(3000);
}
