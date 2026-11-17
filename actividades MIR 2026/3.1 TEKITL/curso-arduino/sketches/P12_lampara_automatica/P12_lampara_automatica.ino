/*
  P12 · Lámpara nocturna automática                           Sesión 6
  ------------------------------------------------------------------
  Qué hace: el LED se enciende solo cuando hay poca luz. Una perilla ajusta
  qué tan oscuro debe estar para que se encienda (el UMBRAL).

  Conexiones:
    LDR + 10 kohm    5 V -> LDR -> punto medio -> 10 kohm -> GND ; punto medio -> A0
    Potenciómetro    extremo -> 5 V ; centro -> A1 ; otro extremo -> GND
    LED              pin 9 -> resistencia 220 ohm -> LED (+) ; pata corta -> GND
                     (el mismo LED de la Sesión 5; el pin 9 tiene ~ y sirve para el reto del medio brillo)

  Ideas clave:
    - Decisión con umbral: si luz < umbral, enciende; si no, apaga.
    - La perilla permite calibrar el sistema sin cambiar el código.
    - Cuidado con la retroalimentación: si el LED ilumina al LDR, el sistema se apaga
      y se vuelve a encender sin parar. Separa el LED del sensor o ponle un tubito de
      cartón al LDR. Eso mismo le pasa a cualquier sistema real.
    - Si la luz anda cerca del umbral, el LED puede parpadear por el ruido de la lectura.
      La Sesión 12 enseña cómo evitarlo (histéresis).

  Abre el Serial Plotter para ver las dos líneas: "luz" y "umbral".

  Retos:  - Haz que el LED encienda a la mitad del brillo (analogWrite en lugar de digitalWrite).
          - Agrega un botón de paro: un toque apaga la lámpara aunque esté oscuro y otro toque
            la vuelve a dejar en automático.
*/

const int PIN_LDR = A0;
const int PIN_PERILLA = A1;
const int PIN_LED = 9;

void setup() {
  pinMode(PIN_LED, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int luz = analogRead(PIN_LDR);
  int umbral = analogRead(PIN_PERILLA);

  if (luz < umbral) {
    digitalWrite(PIN_LED, HIGH);    // está oscuro: enciende
  } else {
    digitalWrite(PIN_LED, LOW);     // hay luz: apaga
  }

  Serial.print("luz:");
  Serial.print(luz);
  Serial.print(",umbral:");
  Serial.println(umbral);
  delay(100);
}
