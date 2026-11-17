/*
  P23 · Reto: la velocidad sube con la temperatura (solución del instructor)    Sesión 12
  ------------------------------------------------------------------
  Qué hace: el termostato de P23, pero en lugar de encender y apagar, el LED (o el motor) va
  de apagado en el límite al máximo brillo 5 grados por encima, de forma proporcional.

  Conexiones: las de P23 (termistor en A0, perilla del límite en A1, LCD1602 con RS 12, E 11, D4 10,
  D5 9, D6 8, D7 7, y el LED con 220 ohm en el pin 5, que tiene ~ y admite analogWrite).

  Ideas clave:
    - Control proporcional: mientras más lejos del límite, más fuerte la respuesta.
    - (temperatura - limite) x 51 llega a 255 cuando se pasa el límite por 5 grados.
    - Las dos comprobaciones if mantienen la velocidad entre 0 y 255 (en la Sesión 13 se verá
      constrain(), que hace lo mismo en una línea).
    - Aquí ya no hace falta la histéresis: la respuesta cambia poco a poco, no de golpe.
*/

#include <LiquidCrystal.h>

//                RS, E, D4, D5, D6, D7
LiquidCrystal lcd(12, 11, 10, 9, 8, 7);

const int PIN_TERMISTOR = A0;
const int PIN_PERILLA = A1;
const int PIN_MOTOR = 5;
const float HISTERESIS = 1.0;          // grados de margen para apagar

bool ventiladorEncendido = false;

float leerTemperatura() {
  long suma = 0;
  for (int i = 0; i < 10; i++) {
    suma = suma + analogRead(PIN_TERMISTOR);
    delay(2);
  }
  float lectura = suma / 10.0;

  if (lectura < 1.0 || lectura > 1022.0) {
    return -273.0;                     // sensor desconectado
  }
  float resistencia = 10000.0 * (1024.0 / lectura - 1.0);
  float lnR = log(resistencia);
  float tempK = 1.0 / (0.001129148 + (0.000234125 + (0.0000000876741 * lnR * lnR)) * lnR);
  return tempK - 273.15;
}

void setup() {
  pinMode(PIN_MOTOR, OUTPUT);
  lcd.begin(16, 2);
  lcd.print("Ventilador auto");
  delay(1500);
  lcd.clear();
}

void loop() {
  float temperatura = leerTemperatura();
  int limite = map(analogRead(PIN_PERILLA), 0, 1023, 20, 40);

  if (temperatura < -200.0) {
    // sin lectura válida: por seguridad, el ventilador se apaga
    ventiladorEncendido = false;
    digitalWrite(PIN_MOTOR, LOW);
    lcd.setCursor(0, 0);
    lcd.print("Revisa termistor");
    lcd.setCursor(0, 1);
    lcd.print("                ");
    delay(500);
    return;
  }

  // Velocidad proporcional: 0 en el límite y máxima 5 grados por encima
  float exceso = temperatura - limite;
  int velocidad = (int)(exceso * 51.0);        // 5 grados x 51 = 255
  if (velocidad < 0) {
    velocidad = 0;
  }
  if (velocidad > 255) {
    velocidad = 255;
  }
  analogWrite(PIN_MOTOR, velocidad);
  ventiladorEncendido = (velocidad > 0);       // solo para la pantalla

  // Pantalla
  lcd.setCursor(0, 0);
  lcd.print("T:");
  lcd.print(temperatura, 1);
  lcd.print("C Lim:");
  lcd.print(limite);
  lcd.print("  ");
  lcd.setCursor(0, 1);
  if (ventiladorEncendido) {
    lcd.print("Ventilador: ON ");
  } else {
    lcd.print("Ventilador: OFF");
  }
  delay(500);
}
