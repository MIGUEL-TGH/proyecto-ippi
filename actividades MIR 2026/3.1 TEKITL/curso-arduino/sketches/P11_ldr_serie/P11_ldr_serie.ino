/*
  P11 · Sensor de luz (fotorresistencia o LDR)                Sesión 6
  ------------------------------------------------------------------
  Qué hace: lee cuánta luz hay y muestra el número en el Monitor Serie (y en el Serial Plotter).

  Conexiones (divisor de voltaje con una resistencia de 10 kilo-ohm):
    5 V -> LDR -> (punto medio) -> resistencia 10 kohm -> GND
    El punto medio, donde se unen LDR y resistencia, va al pin A0.
  (El LDR no tiene polaridad: puede ir en cualquier sentido.)

  Ideas clave:
    - El LDR es una resistencia que CAMBIA con la luz: con más luz tiene menos resistencia.
    - Como el LDR está del lado de 5 V, más luz = voltaje más alto en A0 = número más alto.
    - Un sensor casi siempre se usa dentro de un divisor de voltaje para que Arduino
      pueda "leer" su cambio de resistencia como voltaje (es el mismo divisor del potenciómetro,
      pero aquí la resistencia cambia sola con la luz).
    - Según su hoja de datos (LXD5537): 18 a 50 kilo-ohm a 10 lux y al menos 2 mega-ohm en la
      oscuridad total. Por eso, con 10 kilo-ohm fijos, la oscuridad da números muy bajos.

  Cómo ver la gráfica: Herramientas -> Serial Plotter (velocidad 9600).

  Retos:  - Anota el valor con la luz del salón, con la mano encima y con la linterna del celular.
          - ¿Qué valor elegirías para decir "está oscuro"?
          - Tapa el LDR con un tubito de cartón. ¿Cambia el valor con la luz del salón?
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
