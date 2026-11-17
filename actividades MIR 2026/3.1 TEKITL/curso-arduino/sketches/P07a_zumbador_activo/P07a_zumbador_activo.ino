/*
  P07a · Zumbador activo                                      Sesión 4
  ------------------------------------------------------------------
  Qué hace: emite tres pitidos cortos, una pausa y un pitido largo, y se repite.

  Conexiones:
    Zumbador ACTIVO   pata marcada con + (la larga) -> pin 12 ; la otra pata -> GND
    (En el kit es el que trae una etiqueta blanca con el signo +. El pasivo es un disco
     negro liso con un orificio: ese NO se conecta así, ver P07b.)

  Un zumbador activo trae su propio circuito: suena con solo darle 5 V, siempre con el
  mismo tono. Su hoja de datos pide menos de 25 mA y un pin del UNO aguanta hasta 40 mA,
  así que va directo al pin, sin resistencia.

  Idea clave: una FUNCIÓN con parámetro. pitido(100) y pitido(600) hacen lo mismo
  pero con distinta duración.

  Cuidado: no lo dejes sonando mucho tiempo; es molesto y calienta.

  Retos:  - Las tres líneas pitido(100) se repiten: reemplázalas con un "for".
          - Escribe el patrón de un timbre de puerta.
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
