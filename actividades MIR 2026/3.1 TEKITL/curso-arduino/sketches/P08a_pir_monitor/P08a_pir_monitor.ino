/*
  P08a · Ver lo que "siente" el sensor PIR                         Sesión 4
  ------------------------------------------------------------------
  Qué hace: lee el sensor PIR, enciende el LED mientras detecta movimiento y escribe en el
  Monitor Serie el segundo en que empezó y en que terminó cada detección.

  Conexiones:
    Sensor PIR HC-SR501   VCC -> 5 V ; GND -> GND ; OUT -> pin 7   (3 cables macho-hembra;
                          lee las letras impresas en TU módulo: el orden cambia entre fabricantes)
    LED rojo              pin 8 -> resistencia 220 ohm -> LED (+) ; pata corta -> GND

  Idea clave: el PIR se lee como un botón, con digitalRead: HIGH = hay movimiento, LOW = no hay.
  La diferencia es que el sensor decide solo. Para ver cuánto dura cada detección se anota la hora
  con millis(), que cuenta los milisegundos desde que arrancó el programa (se estudia a fondo en
  la Sesión 11; hoy solo se usa para poner la hora).

  Qué observar:
    - Al conectar el USB el sensor necesita casi un minuto para estabilizarse (manual del kit).
      En ese tiempo puede dar falsas detecciones aunque nadie se mueva.
    - Cuánto tiempo se queda en HIGH después de un movimiento (lo decide la perilla del retardo).
    - Que después de volver a LOW pasan unos 3 segundos sin detectar (manual del kit).
    - Qué cambia al girar la perilla de sensibilidad y al mover el puente de disparo.

  Monitor Serie a 9600 baudios.
*/

const int PIN_PIR = 7;
const int PIN_LED = 8;

int estadoAnterior = LOW;            // el sensor empieza sin detectar nada

void setup() {
  pinMode(PIN_PIR, INPUT);
  pinMode(PIN_LED, OUTPUT);
  Serial.begin(9600);
  Serial.println("Sensor PIR listo. En el primer minuto puede dar falsas detecciones.");
}

void loop() {
  int estado = digitalRead(PIN_PIR);
  digitalWrite(PIN_LED, estado);               // el LED copia lo que dice el sensor

  if (estado != estadoAnterior) {              // el sensor cambió
    Serial.print(millis() / 1000);             // segundos desde que arrancó el programa
    if (estado == HIGH) {
      Serial.println(" s: MOVIMIENTO");
    } else {
      Serial.println(" s: sin movimiento");
    }
    estadoAnterior = estado;
  }
  delay(20);
}
