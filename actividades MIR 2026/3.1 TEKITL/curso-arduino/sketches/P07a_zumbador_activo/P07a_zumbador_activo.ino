/*
  P07a · Zumbador activo                                      Sesión 4
  ------------------------------------------------------------------
  Qué hace: emite tres pitidos cortos, una pausa y un pitido largo, y se repite.

  Conexiones:
    Zumbador ACTIVO   pata marcada con + (la larga) -> pin 12 ; la otra pata -> GND
    (Un zumbador activo trae su propio circuito: suena con solo darle 5 V.
     El kit trae uno activo y uno pasivo. Para distinguirlos, conecta uno a 5 V y
     GND: el que suena fijo es el activo; el pasivo solo hace un "clic".)

  Idea clave: una FUNCIÓN con parámetro. pitido(100) y pitido(600) hacen lo mismo
  pero con distinta duración.

  Cuidado: no dejes el zumbador sonando mucho tiempo; es molesto y calienta.

  Retos:  - Escribe el patrón de un timbre de puerta.
          - Haz un código "secreto": 2 cortos, 1 largo, 2 cortos.
*/

const int PIN_ZUMBADOR = 12;

void pitido(int duracion) {
  digitalWrite(PIN_ZUMBADOR, HIGH);
  delay(duracion);
  digitalWrite(PIN_ZUMBADOR, LOW);
  delay(150);                     // silencio breve entre pitidos
}

void setup() {
  pinMode(PIN_ZUMBADOR, OUTPUT);
}

void loop() {
  pitido(100);
  pitido(100);
  pitido(100);
  delay(800);
  pitido(600);
  delay(2000);
}
