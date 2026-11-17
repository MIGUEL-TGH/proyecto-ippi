/*
  P09 · La perilla y los números                              Sesión 5
  ------------------------------------------------------------------
  Qué hace: lee la posición del potenciómetro y muestra el valor (0 a 1023) y el
  voltaje en el Monitor Serie.

  Conexiones (potenciómetro de 10 kilo-ohm, rotulado B103, 3 patas):
    pata de un extremo     -> 5 V
    pata del CENTRO        -> pin A0      (el centro SOLO va a A0: nunca a 5 V ni a GND)
    pata del otro extremo  -> GND
  (Si al girar el valor sube al revés, intercambia los cables de los extremos.)

  Ideas clave:
    - Una señal ANALÓGICA puede tomar muchos valores, no solo HIGH o LOW.
    - analogRead() convierte de 0 a 5 V en un número de 0 a 1023 (10 bits = 1024 niveles).
    - El potenciómetro es un "divisor de voltaje": gira y el voltaje del centro cambia.
    - Se lee con los pines A0 a A5. No hace falta pinMode para leer una entrada analógica.

  Cómo ver los números: Herramientas -> Monitor Serie, velocidad 9600.
  La gráfica (Serial Plotter) está en el sketch P09a.

  Retos:  - Anota qué número sale en los dos extremos y en el centro. ¿Llega a 0 y a 1023?
          - Con una regla de tres, calcula el voltaje de tres lecturas y compáralo con
            lo que muestra el Monitor Serie.
          - Haz que también escriba el porcentaje de giro (0 a 100 %).
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
