/*
  X01 · Dado electrónico con 6 LED                            Ampliación
  ------------------------------------------------------------------
  Qué hace: al presionar el botón, los LED "giran" unos segundos y se queda encendida
  una cantidad de LED igual al número que salió (1 a 6).

  Conexiones (6 LED, cada uno con su resistencia de 220 ohm y la pata corta a GND):
    LED 1 -> pin 8     LED 2 -> pin 9     LED 3 -> pin 10
    LED 4 -> pin 11    LED 5 -> pin 12    LED 6 -> pin 13
    Botón: una pata -> pin 2 ; la pata OPUESTA (en diagonal) -> GND

  Ideas clave:
    - Un ARREGLO (LEDS[]) guarda varios valores bajo un mismo nombre: así un for
      puede recorrer todos los LED.
    - random(1, 7) da un número al azar del 1 al 6. randomSeed() con una lectura de un pin
      sin conectar (A5) hace que no salga siempre la misma secuencia.

  Retos:  - Cambia la animación de giro.
          - Haz que se muestre la cara real de un dado con los puntos (necesitas 7 LED).
          - Agrega un zumbador que haga "tic tic tic" mientras gira.
*/

const int LEDS[] = {8, 9, 10, 11, 12, 13};
const int NUM_LEDS = 6;
const int PIN_BOTON = 2;

void mostrar(int cantidad) {
  for (int i = 0; i < NUM_LEDS; i++) {
    if (i < cantidad) {
      digitalWrite(LEDS[i], HIGH);
    } else {
      digitalWrite(LEDS[i], LOW);
    }
  }
}

void setup() {
  for (int i = 0; i < NUM_LEDS; i++) {
    pinMode(LEDS[i], OUTPUT);
  }
  pinMode(PIN_BOTON, INPUT_PULLUP);
  randomSeed(analogRead(A5));
  mostrar(0);
}

void loop() {
  if (digitalRead(PIN_BOTON) == LOW) {
    int resultado = 1;
    for (int i = 0; i < 12; i++) {          // animación: cada vez más lento
      resultado = random(1, 7);
      mostrar(resultado);
      delay(60 + i * 15);
    }
    mostrar(resultado);                      // se queda el último número
    delay(300);
    while (digitalRead(PIN_BOTON) == LOW) {  // espera a que suelten el botón
      delay(10);
    }
  }
}
