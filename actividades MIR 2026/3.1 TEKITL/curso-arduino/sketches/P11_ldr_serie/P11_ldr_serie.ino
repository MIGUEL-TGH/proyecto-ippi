/*
  P11 · Sensor de luz (fotorresistencia o LDR)                Sesión 6
  ------------------------------------------------------------------
  Qué hace: lee cuánta luz hay y muestra el número en el Monitor Serie.

  Conexiones (divisor de voltaje con una resistencia de 10 kilo-ohm):
    5 V -> LDR -> (punto medio) -> resistencia 10 kohm -> GND
    El punto medio, donde se unen LDR y resistencia, va al pin A0.
  (El LDR no tiene polaridad: puede ir en cualquier sentido.)

  Ideas clave:
    - El LDR es una resistencia que CAMBIA con la luz: con más luz tiene menos resistencia.
    - Como el LDR está del lado de 5 V, más luz = voltaje más alto en A0 = número más alto.
    - Un sensor casi siempre se usa dentro de un divisor de voltaje para que Arduino
      pueda "leer" su cambio de resistencia como voltaje.

  Cómo ver la gráfica: Herramientas -> Serial Plotter (velocidad 9600).

  Retos:  - Anota el valor con la luz del salón, con la mano encima y con la linterna del celular.
          - ¿Qué valor elegirías para decir "está oscuro"?
*/

const int PIN_LDR = A0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int luz = analogRead(PIN_LDR);
  Serial.println(luz);              // un solo número por línea para el Serial Plotter
  delay(100);
}
