/*
  P24 · Reto: un zumbador que avisa cuando la tierra está seca (solución del instructor)    Sesión 13
  ------------------------------------------------------------------
  Qué hace: el aviso de riego de P24 y, además, un zumbador PASIVO que da un pitido corto en cada
  ciclo mientras la tierra esté seca.

  Conexiones: las de P24, y
    Zumbador PASIVO   una pata -> resistencia 220 ohm -> pin 12 ; otra pata -> GND

  Ideas clave:
    - El aviso sonoro se agrega en el mismo if que enciende el LED rojo: lo que pasa cuando la
      humedad es baja queda junto.
    - Recuerda calibrar VALOR_SECO y VALOR_MOJADO con tu propio sensor (ver P24).
*/

const int PIN_SENSOR = A0;
const int LED_ROJO = 8;
const int LED_AMARILLO = 9;
const int LED_VERDE = 10;
const int PIN_ZUMBADOR = 12;

const int VALOR_SECO = 1000;          // lectura con el sensor seco  (AJUSTA con tu medición)
const int VALOR_MOJADO = 350;         // lectura con el sensor en agua (AJUSTA con tu medición)
const int PORCENTAJE_BAJO = 30;       // menos de esto = seco
const int PORCENTAJE_ALTO = 70;       // más de esto = muy mojado

void setup() {
  pinMode(LED_ROJO, OUTPUT);
  pinMode(LED_AMARILLO, OUTPUT);
  pinMode(LED_VERDE, OUTPUT);
  pinMode(PIN_ZUMBADOR, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int lectura = analogRead(PIN_SENSOR);
  int humedad = map(lectura, VALOR_SECO, VALOR_MOJADO, 0, 100);   // más mojado = lectura menor
  humedad = constrain(humedad, 0, 100);

  digitalWrite(LED_ROJO, LOW);
  digitalWrite(LED_AMARILLO, LOW);
  digitalWrite(LED_VERDE, LOW);

  Serial.print("Lectura: ");
  Serial.print(lectura);
  Serial.print("    Humedad: ");
  Serial.print(humedad);
  Serial.print(" %    ");

  if (humedad < PORCENTAJE_BAJO) {
    digitalWrite(LED_ROJO, HIGH);
    tone(PIN_ZUMBADOR, 800, 100);          // pitido de aviso
    Serial.println("SECA: hay que regar");
  } else if (humedad > PORCENTAJE_ALTO) {
    digitalWrite(LED_AMARILLO, HIGH);
    Serial.println("MUY MOJADA: no regar");
  } else {
    digitalWrite(LED_VERDE, HIGH);
    Serial.println("Humedad adecuada");
  }
  delay(500);
}
