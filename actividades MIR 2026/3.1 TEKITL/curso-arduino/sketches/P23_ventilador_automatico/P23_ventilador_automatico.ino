/*
  P23 · Ventilador automático (termostato con pantalla)       Sesión 12
  ------------------------------------------------------------------
  !! EL MOTOR NO SE ARMA TODAVÍA (16 nov 2026) !!
  El circuito del motor (PN2222 y módulo de fuente) está fuera de especificación si el motor
  consume 0.95 A (ver P17 y plan-curso-arduino.md, V1). HOY EL "VENTILADOR" ES UN LED con
  resistencia de 220 ohm en el pin 5: la lógica (histéresis) y el código son los mismos.
  ------------------------------------------------------------------
  Qué hace: mide la temperatura con el termistor y enciende el motor con aspa cuando
  pasa de un límite. Con la perilla eliges el límite (20 a 40 grados). La pantalla
  muestra la temperatura, el límite y el estado del ventilador.

  Este proyecto reúne lo de las sesiones 5, 9, 10 y 11.

  Conexiones:
    Termistor + 10 kohm   5 V -> termistor -> punto medio -> 10 kohm -> GND ; punto medio -> A0
    Perilla (límite)      extremo -> 5 V ; centro -> A1 ; otro extremo -> GND
    LCD1602               igual que P21 (RS 12, E 11, D4 10, D5 9, D6 8, D7 7) con su
                          potenciómetro de contraste (el otro potenciómetro del kit) y 100 ohm en la luz de fondo
    Ventilador (hoy LED)  pin 5 -> resistencia 220 ohm -> LED (pata larga +) ; pata corta -> GND
                          (con el motor, cuando se destrabe: el circuito de P17 en el pin 5)

  Ideas clave:
    - Sistema de control: MEDIR -> COMPARAR -> ACTUAR.
    - Histéresis: si el ventilador se encendiera y apagara exactamente en el mismo valor,
      "temblaría" por el ruido de la medición. Se enciende al llegar al límite y se apaga
      solo cuando baja 1 grado por debajo (HISTERESIS).
    - Una variable de estado (ventiladorEncendido) recuerda lo que se hizo antes.

  Cómo probar: pon el límite 1 o 2 grados por encima de la temperatura ambiente y calienta el
  termistor con los dedos. Suelta el termistor y espera a que se enfríe. No lo calientes con flama.

  Retos:  - Que el brillo del LED (la "velocidad") suba mientras más caliente esté (analogWrite).
          - Agrega un zumbador que avise si pasa de 35 grados.
          - Pon el límite igual a la temperatura ambiente y quita la histéresis: el LED "tiembla".
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
