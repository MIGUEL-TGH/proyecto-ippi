/*
  P15 · Medidor de distancia con ultrasonido (HC-SR04)        Sesión 8
  ------------------------------------------------------------------
  Qué hace: mide la distancia a un objeto y la muestra en centímetros en el Monitor Serie.

  Conexiones del HC-SR04 (4 pines):
    VCC  -> 5 V
    TRIG -> pin 6
    ECHO -> pin 7
    GND  -> GND

  Ideas clave:
    - El sensor manda un "chirrido" ultrasónico (TRIG) y mide cuánto tarda en volver (ECHO).
    - distancia = tiempo x velocidad del sonido / 2   (va y regresa, por eso se divide entre 2)
    - La velocidad del sonido es unos 343 m/s = 0.0343 cm por microsegundo.
    - Este código NO necesita instalar ninguna librería.

  Alcance del sensor: de 2 cm a 4 m aproximadamente. Las telas y superficies inclinadas
  devuelven mal el eco.

  Retos:  - Compara la medida con una regla en 10, 20 y 50 cm.
          - Prueba con distintos materiales (libro, tela, mano). ¿Cuál se mide peor?
*/

const int PIN_TRIG = 6;
const int PIN_ECHO = 7;

void setup() {
  pinMode(PIN_TRIG, OUTPUT);
  pinMode(PIN_ECHO, INPUT);
  Serial.begin(9600);
}

void loop() {
  // 1) manda un pulso de 10 microsegundos
  digitalWrite(PIN_TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(PIN_TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(PIN_TRIG, LOW);

  // 2) mide cuánto tarda el eco (máximo 30 ms de espera = unos 5 m)
  long duracion = pulseIn(PIN_ECHO, HIGH, 30000UL);

  // 3) convierte a centímetros
  if (duracion == 0) {
    Serial.println("Sin eco (fuera de alcance)");
  } else {
    float distanciaCm = duracion * 0.0343 / 2.0;
    Serial.print("Distancia: ");
    Serial.print(distanciaCm, 1);
    Serial.println(" cm");
  }
  delay(300);
}
