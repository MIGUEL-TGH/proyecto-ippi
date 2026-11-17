/*
  P23 · Reto: un zumbador que avisa si pasa de 35 grados (solución del instructor)    Sesión 12
  ------------------------------------------------------------------
  Qué hace: el termostato de P23 y, además, un zumbador PASIVO que da un pitido corto en cada
  ciclo mientras la temperatura sea de 35 grados o más.

  Conexiones: las de P23, y
    Zumbador PASIVO   una pata -> resistencia 220 ohm -> pin 4 ; otra pata -> GND
                      (los pines 7 a 12 son de la pantalla y el 5 del ventilador: el zumbador va al 4)

  Ideas clave:
    - Dos decisiones independientes con la misma lectura: una para el ventilador (con histéresis)
      y otra para la alarma (con un umbral fijo).
    - El zumbador pasivo se maneja con tone() (Sesión 4) y siempre lleva su resistencia de 220 ohm.
*/

#include <LiquidCrystal.h>

//                RS, E, D4, D5, D6, D7
LiquidCrystal lcd(12, 11, 10, 9, 8, 7);

const int PIN_TERMISTOR = A0;
const int PIN_PERILLA = A1;
const int PIN_MOTOR = 5;
const int PIN_ZUMBADOR = 4;
const float TEMPERATURA_ALARMA = 35.0;
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
  pinMode(PIN_ZUMBADOR, OUTPUT);
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

  // Decisión con histéresis
  if (!ventiladorEncendido && temperatura >= limite) {
    ventiladorEncendido = true;
  } else if (ventiladorEncendido && temperatura <= limite - HISTERESIS) {
    ventiladorEncendido = false;
  }

  if (ventiladorEncendido) {
    digitalWrite(PIN_MOTOR, HIGH);
  } else {
    digitalWrite(PIN_MOTOR, LOW);
  }

  // Alarma: un pitido corto en cada ciclo mientras haga demasiado calor
  if (temperatura >= TEMPERATURA_ALARMA) {
    tone(PIN_ZUMBADOR, 2000, 200);
  }

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
