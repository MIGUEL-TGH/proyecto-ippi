/*
  P17 · Transistor como interruptor: encender una carga con un botón      Sesión 9
  ------------------------------------------------------------------
  El nombre del sketch dice "motor" porque ese es el destino de la sesión. HOY SE ARMA CON UN LED.

  !! EL MOTOR NO SE ARMA TODAVÍA (16 nov 2026) !!
  Se midió que el motor "3-6 V" funciona a partir de 0.95 A. El circuito del motor (PN2222 y
  módulo de fuente) solo aguanta 0.6 A y 0.7 A. Hasta confirmar cuánto consume el motor a 5 V
  (ver plan-curso-arduino.md, sección 11, V1) ese circuito está fuera de especificación.
  El código sirve igual con el LED y, más adelante, con el motor.
  ------------------------------------------------------------------
  Qué hace: la carga (el LED, o el motor cuando se destrabe) se enciende mientras mantienes
  presionado el botón.

  ¡NUNCA conectes una carga grande directo a un pin del Arduino! Un pin entrega máximo 40 mA
  (en la práctica, unos 20 mA) y un motor pide cientos de mA. Por eso se usa un TRANSISTOR
  como interruptor: una corriente pequeña en la base (pin 5) deja pasar una corriente grande
  entre colector y emisor.

  Conexiones de la VERSIÓN CON LED (la que se arma hoy):
    PN2222 (flat hacia ti, patas hacia abajo; según la hoja de datos del kit):
      pata 1 (izquierda) = EMISOR   -> GND (riel azul)
      pata 2 (centro)    = BASE     -> resistencia 330 ohm -> pin 5
      pata 3 (derecha)   = COLECTOR -> pata corta (-) del LED
    LED:  pata larga (+) -> resistencia 220 ohm -> 5 V (riel rojo)
    Botón: una pata -> pin 2 ; la pata OPUESTA (en diagonal) -> GND

  Conexiones de la VERSIÓN CON MOTOR (BLOQUEADA hasta resolver V1):
    Módulo de fuente en el protoboard con el + en el riel rojo y el - en el azul; jumpers de ambos
    lados en 5 V; adaptador de 9 V. GND común: el riel azul se une a un GND del Arduino.
    El motor reemplaza al LED: un cable al colector y el otro al +5 V del módulo.
    Diodo 1N4007 en paralelo con el motor: la raya (cátodo) hacia +5 V y el otro extremo al
    colector. Protege al transistor de los picos que genera el motor al apagarse.

  Ideas clave:
    - El transistor es un interruptor controlado por una corriente pequeña (la de la base)
      que deja pasar una corriente grande (la de la carga).
    - Toda la electrónica comparte la misma referencia: el GND común.
    - Revisa el dibujo de patas en la hoja de datos del PN2222 antes de conectar (1=E, 2=B, 3=C).
      Otros fabricantes de transistores parecidos numeran las patas al revés: se comprueba (V2).
    - Con el LED la carga pide unos 13 mA y la base unos 13 mA: los dos números son pequeños.
      Con un motor, la carga pedirá cientos de mA y la base seguirá pidiendo los mismos 13 mA.

  Seguridad: si el transistor se calienta, desconecta el USB. Con el motor: no bloquees el aspa;
  el módulo de fuente se calienta si el motor se traba.

  Retos:  - Con un solo toque enciende y con otro apaga (como la sesión 3).
          - Haz que la carga encienda 3 segundos al presionar y luego se apague sola.
          - Agrega más LED en paralelo (cada uno con su resistencia de 220 ohm): cuatro LED
            piden unos 50 mA, más de lo que aguanta un pin. ¿Los aguanta el transistor?
*/

const int PIN_BOTON = 2;
const int PIN_CARGA = 5;      // va a la base del transistor (con resistencia de 330 ohm)

void setup() {
  pinMode(PIN_BOTON, INPUT_PULLUP);
  pinMode(PIN_CARGA, OUTPUT);
}

void loop() {
  if (digitalRead(PIN_BOTON) == LOW) {
    digitalWrite(PIN_CARGA, HIGH);     // el transistor deja pasar corriente a la carga
  } else {
    digitalWrite(PIN_CARGA, LOW);
  }
}
