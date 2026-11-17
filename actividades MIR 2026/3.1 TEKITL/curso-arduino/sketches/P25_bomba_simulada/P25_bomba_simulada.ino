/*
  P25 · Reto: una bomba simulada con histéresis (solución del instructor)    Sesión 13
  ------------------------------------------------------------------
  Qué hace: el modelo de tinaco de P25 y una "bomba" (un LED en el pin 5): se enciende cuando el
  nivel está BAJO y se apaga solo cuando llega a ALTO. Entre los dos valores se queda como estaba.

  Conexiones: las de P25
    Sensor de nivel de agua   + -> 5 V ; - -> GND ; S (señal) -> A0
    LED rojo      pin 8  -> resistencia 220 ohm -> LED (+) ; pata corta -> GND   (nivel bajo)
    LED amarillo  pin 9  -> resistencia 220 ohm -> LED (+) ; pata corta -> GND   (nivel medio)
    LED verde     pin 10 -> resistencia 220 ohm -> LED (+) ; pata corta -> GND   (nivel alto)
    Bomba (un LED)  pin 5 -> resistencia 220 ohm -> LED (+) ; pata corta -> GND
                    (con el motor, cuando se destrabe: el circuito de la Sesión 9 en el pin 5)

  Ideas clave:
    - Es la misma histéresis de la Sesión 12, pero con el nivel del agua en lugar de la temperatura:
      la bomba enciende con poca agua y apaga solo cuando el tinaco ya está lleno, no apenas sube.
    - La variable de estado bombaEncendida recuerda si ya se estaba llenando.
    - Calibra NIVEL_BAJO y NIVEL_ALTO con tus lecturas, como en P25.
*/

const int PIN_SENSOR = A0;
const int LED_ROJO = 8;
const int LED_AMARILLO = 9;
const int LED_VERDE = 10;
const int PIN_BOMBA = 5;

const int NIVEL_BAJO = 150;           // por debajo de esto, la bomba enciende  (AJUSTA con tu medición)
const int NIVEL_ALTO = 400;           // por encima de esto, la bomba apaga     (AJUSTA con tu medición)

bool bombaEncendida = false;

void setup() {
  pinMode(LED_ROJO, OUTPUT);
  pinMode(LED_AMARILLO, OUTPUT);
  pinMode(LED_VERDE, OUTPUT);
  pinMode(PIN_BOMBA, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int nivel = analogRead(PIN_SENSOR);

  // La bomba, con histéresis
  if (!bombaEncendida && nivel < NIVEL_BAJO) {
    bombaEncendida = true;
  } else if (bombaEncendida && nivel > NIVEL_ALTO) {
    bombaEncendida = false;
  }
  if (bombaEncendida) {
    digitalWrite(PIN_BOMBA, HIGH);
  } else {
    digitalWrite(PIN_BOMBA, LOW);
  }

  // Los tres LED del nivel
  digitalWrite(LED_ROJO, LOW);
  digitalWrite(LED_AMARILLO, LOW);
  digitalWrite(LED_VERDE, LOW);
  if (nivel < NIVEL_BAJO) {
    digitalWrite(LED_ROJO, HIGH);
  } else if (nivel < NIVEL_ALTO) {
    digitalWrite(LED_AMARILLO, HIGH);
  } else {
    digitalWrite(LED_VERDE, HIGH);
  }

  Serial.print("Lectura:");
  Serial.print(nivel);
  Serial.print(",Bomba:");
  if (bombaEncendida) {
    Serial.println(1);
  } else {
    Serial.println(0);
  }
  delay(500);
}
