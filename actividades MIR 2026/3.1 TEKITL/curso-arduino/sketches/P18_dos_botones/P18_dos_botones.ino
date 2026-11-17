/*
  P18 · Reto: dos botones suben y bajan la intensidad de 10 en 10 % (solución del instructor)   Sesión 9
  ------------------------------------------------------------------
  Qué hace: el botón del pin 2 SUBE la intensidad 10 % y el botón del pin 3 la BAJA 10 %
  (de 0 a 100 %). Se ve en el Monitor Serie (velocidad 9600).

  Conexiones: las de P18 y dos botones, en lugar del potenciómetro
    PN2222   emisor -> GND ; base -> resistencia 330 ohm -> pin 5 ; colector -> carga
    LED      pata larga (+) -> resistencia 220 ohm -> 5 V ; pata corta (-) -> colector
    Botón SUBIR  una pata -> pin 2 ; la pata opuesta (en diagonal) -> GND
    Botón BAJAR  una pata -> pin 3 ; la pata opuesta (en diagonal) -> GND

  Ideas clave:
    - Una variable "porcentaje" que sube y baja de 10 en 10, y constrain() que la mantiene
      entre 0 y 100 (si no, bajaría de 0 o pasaría de 100).
    - map() lleva el porcentaje (0 a 100) a PWM (0 a 255), como en P10.
    - Cada botón se detecta en el MOMENTO en que se presiona, para que un toque largo no
      cuente varias veces.
*/

const int PIN_SUBIR = 2;
const int PIN_BAJAR = 3;
const int PIN_CARGA = 5;
const int PASO = 10;                    // cuánto sube o baja cada toque, en %

int porcentaje = 0;
int subirAnterior = HIGH;
int bajarAnterior = HIGH;

void setup() {
  pinMode(PIN_SUBIR, INPUT_PULLUP);
  pinMode(PIN_BAJAR, INPUT_PULLUP);
  pinMode(PIN_CARGA, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int subirActual = digitalRead(PIN_SUBIR);
  int bajarActual = digitalRead(PIN_BAJAR);

  if (subirAnterior == HIGH && subirActual == LOW) {
    porcentaje = porcentaje + PASO;
  }
  if (bajarAnterior == HIGH && bajarActual == LOW) {
    porcentaje = porcentaje - PASO;
  }
  subirAnterior = subirActual;
  bajarAnterior = bajarActual;

  porcentaje = constrain(porcentaje, 0, 100);
  int pwm = map(porcentaje, 0, 100, 0, 255);
  analogWrite(PIN_CARGA, pwm);

  Serial.print("Intensidad: ");
  Serial.print(porcentaje);
  Serial.println(" %");
  delay(30);                             // también evita el rebote de los botones
}
