/*
  P05 · Botón y LED                                           Sesión 3
  ------------------------------------------------------------------
  Qué hace: el LED se enciende mientras mantienes presionado el botón.

  Conexiones:
    LED     pin 8 -> resistencia 220 ohm -> LED (pata larga +) ; pata corta (-) -> GND
    Botón   una pata -> pin 2 ; la pata OPUESTA (en diagonal) -> GND
            (el botón tiene 4 patas: conecta dos OPUESTAS, en diagonal)

  Idea clave: INPUT_PULLUP mantiene el pin 2 en HIGH mientras nadie lo toca.
  Al presionar, el botón conecta el pin a GND y se lee LOW.
  Por eso "presionado" = LOW. Parece al revés, pero así funciona sin resistencia extra.

  Retos:  - Haz que el LED se apague cuando presionas (lógica contraria).
          - Agrega un segundo LED que haga lo opuesto al primero.
*/

const int PIN_BOTON = 2;
const int PIN_LED = 8;

void setup() {
  pinMode(PIN_BOTON, INPUT_PULLUP);   // entrada con resistencia interna a +5 V
  pinMode(PIN_LED, OUTPUT);
}

void loop() {
  if (digitalRead(PIN_BOTON) == LOW) {   // ¿está presionado?
    digitalWrite(PIN_LED, HIGH);
  } else {
    digitalWrite(PIN_LED, LOW);
  }
}
