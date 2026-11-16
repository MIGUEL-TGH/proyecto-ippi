/*
  P09 · La perilla y los números                              Sesión 5
  ------------------------------------------------------------------
  Qué hace: lee la posición del potenciómetro y muestra el valor (0 a 1023) y el
  voltaje en el Monitor Serie.

  Conexiones (potenciómetro de 3 patas):
    pata de un extremo  -> 5 V
    pata del centro     -> pin A0
    pata del otro extremo -> GND
  (Si al girar el valor sube al revés, intercambia las patas de los extremos.)

  Ideas clave:
    - Una señal ANALÓGICA puede tomar muchos valores, no solo HIGH o LOW.
    - analogRead() convierte de 0 a 5 V en un número de 0 a 1023 (10 bits).
    - El potenciómetro es un "divisor de voltaje": gira y el voltaje del centro cambia.

  Cómo ver los números: Herramientas -> Monitor Serie, velocidad 9600.
  Prueba también Herramientas -> Serial Plotter para ver una gráfica.

  Retos:  - Anota qué número sale en el extremo izquierdo, en el centro y en el derecho.
          - Comprueba con una regla de tres que el voltaje coincide con la lectura.
*/

const int PIN_PERILLA = A0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int lectura = analogRead(PIN_PERILLA);        // número de 0 a 1023
  float voltaje = lectura * 5.0 / 1023.0;       // lo convertimos a volts

  Serial.print("Lectura: ");
  Serial.print(lectura);
  Serial.print("    Voltaje: ");
  Serial.print(voltaje, 2);                     // 2 decimales
  Serial.println(" V");
  delay(200);
}
