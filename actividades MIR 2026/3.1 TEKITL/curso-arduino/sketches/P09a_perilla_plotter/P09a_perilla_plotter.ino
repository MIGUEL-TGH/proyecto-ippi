/*
  P09a · La perilla como gráfica (Serial Plotter)             Sesión 5
  ------------------------------------------------------------------
  Qué hace: manda la lectura de la perilla en un formato que el Serial Plotter
  convierte en una gráfica. Gira la perilla despacio y mira cómo se mueve la línea.

  Conexiones: las mismas de P09
    Potenciómetro   extremo -> 5 V ; centro -> A0 ; otro extremo -> GND

  Cómo verla: sube el programa y abre Herramientas -> Serial Plotter (velocidad 9600).
  Cierra antes el Monitor Serie: los dos usan el mismo puerto.

  Ideas clave:
    - El Serial Plotter entiende líneas con el formato  nombre:valor  separadas por comas.
      Cada nombre es una línea de color en la gráfica.
    - "Min" y "Max" son dos líneas fijas (0 y 1023). Sirven de marco: así la gráfica
      no cambia de escala mientras giras la perilla.
    - Un solo println por vuelta: cada vuelta del loop es un punto de la gráfica.

  Retos:  - Quita las líneas Min y Max. ¿Qué pasa con la escala de la gráfica?
          - Gira la perilla lo más rápido que puedas. ¿La línea la sigue?
          - Deja la perilla quieta. ¿La línea es completamente plana?
*/

const int PIN_PERILLA = A0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int lectura = analogRead(PIN_PERILLA);          // 0 a 1023

  Serial.print("Min:0,Max:1023,Lectura:");
  Serial.println(lectura);
  delay(50);                                      // unos 20 puntos por segundo
}
