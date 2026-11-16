/*
  P17 · Motor con transistor: encender con un botón           Sesión 9
  ------------------------------------------------------------------
  !! NO ARMAR TODAVÍA (16 nov 2026) !!
  Se midió que el motor "3-6 V" funciona a partir de 0.95 A. Este circuito (PN2222 y
  módulo de fuente) solo aguanta 0.6 A y 0.7 A. Hasta confirmar cuánto consume el motor
  a 5 V (ver plan-curso-arduino.md, sección 11, V1) este circuito está fuera de
  especificación. El código sí es válido para cualquier carga bien conectada.
  ------------------------------------------------------------------
  Qué hace: el motor con aspa gira mientras mantienes presionado el botón.

  ¡NUNCA conectes el motor directo a un pin del Arduino! Un pin entrega máximo ~20 mA
  y el motor pide cientos de mA. Por eso usamos un TRANSISTOR como interruptor y una
  fuente aparte (el módulo de fuente del kit con el adaptador de 9 V).

  Conexiones:
    Módulo de fuente   en el protoboard con el + en el riel rojo y el - en el azul.
                       Jumper de ambos lados en 5 V. Enchufa el adaptador de 9 V.
    GND común          une el riel azul (GND del módulo) con un GND del Arduino.
    Transistor PN2222  (de frente, patas hacia abajo, lado plano hacia ti):
                         pata 1 (izquierda) = EMISOR   -> riel azul (GND)
                         pata 2 (centro)    = BASE     -> resistencia 330 ohm -> pin 5
                         pata 3 (derecha)   = COLECTOR -> un cable del motor
    Motor              el otro cable del motor -> riel rojo (+5 V)
    Diodo 1N4007       en paralelo con el motor: la raya (cátodo) hacia +5 V y el otro
                       extremo al colector. Protege al transistor de los picos que genera
                       el motor al apagarse.
    Botón              una pata -> pin 2 ; la pata del lado contrario -> GND

  Ideas clave:
    - El transistor es un interruptor controlado por una corriente pequeña (base)
      que deja pasar una corriente grande (motor).
    - Toda la electrónica comparte la misma referencia: el GND común.
    - Revisa el dibujo de patas en el datasheet del PN2222 antes de conectar (1=E, 2=B, 3=C).

  Seguridad: no bloquees el aspa con la mano mientras gira; el módulo de fuente se
  calienta si el motor se traba. Si algo se calienta, desconecta el adaptador.

  Retos:  - Con un solo toque enciende y con otro apaga (como la sesión 3).
          - Haz que el motor gire 3 segundos al presionar y luego se detenga solo.
*/

const int PIN_BOTON = 2;
const int PIN_MOTOR = 5;      // va a la base del transistor (con resistencia de 330 ohm)

void setup() {
  pinMode(PIN_BOTON, INPUT_PULLUP);
  pinMode(PIN_MOTOR, OUTPUT);
}

void loop() {
  if (digitalRead(PIN_BOTON) == LOW) {
    digitalWrite(PIN_MOTOR, HIGH);     // el transistor deja pasar corriente al motor
  } else {
    digitalWrite(PIN_MOTOR, LOW);
  }
}
