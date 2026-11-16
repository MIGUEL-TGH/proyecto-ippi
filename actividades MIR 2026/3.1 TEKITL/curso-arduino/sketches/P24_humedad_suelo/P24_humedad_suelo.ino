/*
  P24 · Aviso de riego con el sensor de humedad de suelo      Sesión 13
  ------------------------------------------------------------------
  Qué hace: mide qué tan húmeda está la tierra y lo indica con tres LED y el Monitor Serie:
     LED rojo     = tierra seca, hay que regar
     LED verde    = humedad adecuada
     LED amarillo = muy mojada, no regar

  Conexiones:
    Sensor de humedad de suelo    VCC -> 5 V ; GND -> GND ; AO (salida analógica) -> A0
    LED rojo      pin 8  -> resistencia 220 ohm -> LED (+) ; pata corta -> GND
    LED amarillo  pin 9  -> resistencia 220 ohm -> LED (+) ; pata corta -> GND
    LED verde     pin 10 -> resistencia 220 ohm -> LED (+) ; pata corta -> GND

  CALIBRACIÓN (lo más importante): cada sensor y cada tierra es distinta.
    1) Con el sensor al aire (o en tierra muy seca), anota la lectura -> VALOR_SECO.
    2) Con la sonda metida en un vaso con agua, anota la lectura -> VALOR_MOJADO.
    3) Escribe esos números abajo, sube el código y comprueba con tierra seca y húmeda.
  Los valores que dejé son solo un punto de partida.

  Ideas clave:
    - Una medición solo significa algo después de calibrarla.
    - map() convierte la lectura en porcentaje; constrain() lo mantiene entre 0 y 100.

  Cuidado: mete en el agua o la tierra solo la parte con las pistas, nunca la electrónica.
  Las sondas se oxidan si pasan días conectadas: desconecta el sensor al terminar.

  Retos:  - Mide una maceta antes y después de regarla y compara los porcentajes.
          - Agrega un zumbador que avise cuando esté seca.
          - ¿Qué tanto cambia la lectura con tierra de distinto tipo?
*/

const int PIN_SENSOR = A0;
const int LED_ROJO = 8;
const int LED_AMARILLO = 9;
const int LED_VERDE = 10;

const int VALOR_SECO = 1000;          // lectura con el sensor seco  (AJUSTA con tu medición)
const int VALOR_MOJADO = 350;         // lectura con el sensor en agua (AJUSTA con tu medición)
const int PORCENTAJE_BAJO = 30;       // menos de esto = seco
const int PORCENTAJE_ALTO = 70;       // más de esto = muy mojado

void setup() {
  pinMode(LED_ROJO, OUTPUT);
  pinMode(LED_AMARILLO, OUTPUT);
  pinMode(LED_VERDE, OUTPUT);
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
