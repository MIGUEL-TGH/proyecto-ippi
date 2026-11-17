/*
  P08 · Reto: alarma completa (solución del instructor)             Sesión 4
  ------------------------------------------------------------------
  Qué hace: junta los retos de la alarma P08.
    1) TIEMPO DE SALIDA: al armar, hay 10 segundos para alejarse del sensor, con un pitido por
       segundo. Sin esto, la mano que presiona el botón ya dispara el sensor.
    2) CÓDIGO DE DESARME: con la alarma armada hay que presionar el botón 3 veces, con no más de
       3 segundos entre una pulsación y la siguiente. Una pulsación suelta no hace nada.
    3) SIRENA QUE NO BLOQUEA: la sirena de P08 se hace con delay() y, mientras suena, el programa
       no mira el botón. Aquí el programa da vueltas de 10 ms y cambia el tono cada 15 vueltas
       (150 ms); así puede seguir contando las pulsaciones del código mientras suena.

  Conexiones: las mismas de P08
    Sensor PIR HC-SR501   VCC -> 5 V ; GND -> GND ; OUT -> pin 7
    Botón                 pin 2 y GND, en patas opuestas (en diagonal)
    LED rojo              pin 8 -> resistencia 220 ohm -> LED (+) ; pata corta -> GND
    Zumbador PASIVO       una pata -> resistencia 220 ohm -> pin 12 ; otra pata -> GND

  Ideas clave:
    - Variables que recuerdan: armada, sonando, pulsaciones, vueltasSinPulsar, vueltasSirena.
    - El reloj de este programa es la vuelta de 10 ms: contar vueltas es contar tiempo
      (300 vueltas x 10 ms = 3 s). En la Sesión 11 millis() hará lo mismo con más precisión.
    - Si el PIR sigue en HIGH al terminar el tiempo de salida (la perilla de retardo larga), la
      sirena empieza en seguida: pon el retardo al mínimo para las pruebas.
    - La sirena suena hasta que se teclee el código. Una alarma real tendría además un límite de tiempo.
*/

const int PIN_PIR = 7;
const int PIN_BOTON = 2;
const int PIN_LED = 8;
const int PIN_ZUMBADOR = 12;

const int SEGUNDOS_CALENTAMIENTO = 60;
const int SEGUNDOS_SALIDA = 10;
const int PULSACIONES_CODIGO = 3;
const int VUELTAS_MAX_ENTRE_PULSACIONES = 300;   // 300 vueltas de 10 ms = 3 segundos
const int VUELTAS_POR_TONO = 15;                 // la sirena cambia de tono cada 150 ms

bool armada = false;
bool sonando = false;
bool tonoAlto = true;
int botonAnterior = HIGH;
int pulsaciones = 0;                // cuántas pulsaciones del código lleva
int vueltasSinPulsar = 0;           // vueltas desde la última pulsación del código
int vueltasSirena = 0;              // vueltas desde el último cambio de tono

// Cuenta regresiva de salida: un pitido por segundo, y al final queda armada
void armar() {
  Serial.print("Armando. Tienes ");
  Serial.print(SEGUNDOS_SALIDA);
  Serial.println(" s para alejarte del sensor...");
  for (int s = SEGUNDOS_SALIDA; s > 0; s--) {
    digitalWrite(PIN_LED, HIGH);
    tone(PIN_ZUMBADOR, 1000, 80);
    delay(100);
    digitalWrite(PIN_LED, LOW);
    delay(900);
  }
  digitalWrite(PIN_LED, HIGH);            // LED encendido = armada
  tone(PIN_ZUMBADOR, 2000, 300);
  delay(300);
  armada = true;
  pulsaciones = 0;
  vueltasSinPulsar = 0;
  Serial.println("Alarma ARMADA");
}

void desarmar() {
  armada = false;
  sonando = false;
  pulsaciones = 0;
  vueltasSinPulsar = 0;
  noTone(PIN_ZUMBADOR);
  digitalWrite(PIN_LED, LOW);
  for (int i = 0; i < 2; i++) {           // dos pitidos: desarmada
    tone(PIN_ZUMBADOR, 2000, 100);
    delay(220);
  }
  Serial.println("Alarma DESARMADA");
}

void setup() {
  pinMode(PIN_PIR, INPUT);
  pinMode(PIN_BOTON, INPUT_PULLUP);
  pinMode(PIN_LED, OUTPUT);
  Serial.begin(9600);

  Serial.print("Calentando el sensor PIR (");
  Serial.print(SEGUNDOS_CALENTAMIENTO);
  Serial.println(" s). No te muevas frente a el.");
  for (int s = SEGUNDOS_CALENTAMIENTO; s > 0; s--) {   // el LED parpadea mientras se calienta
    digitalWrite(PIN_LED, HIGH);
    delay(100);
    digitalWrite(PIN_LED, LOW);
    delay(900);
  }
  Serial.println("Listo. Presiona el boton para armar la alarma.");
}

void loop() {
  int botonActual = digitalRead(PIN_BOTON);
  bool presionaron = (botonAnterior == HIGH && botonActual == LOW);   // acaban de presionar
  botonAnterior = botonActual;
  if (presionaron) {
    delay(30);                            // antirrebote
  }

  if (!armada) {
    if (presionaron) {
      armar();
    }
  } else {
    // --- Código de desarme: 3 pulsaciones seguidas ---
    if (presionaron) {
      pulsaciones = pulsaciones + 1;
      vueltasSinPulsar = 0;
      Serial.print("Codigo: pulsacion ");
      Serial.print(pulsaciones);
      Serial.print(" de ");
      Serial.println(PULSACIONES_CODIGO);
      if (pulsaciones == PULSACIONES_CODIGO) {
        desarmar();
      }
    }
    if (armada && pulsaciones > 0) {      // el código ya empezó: ¿se acabó el tiempo?
      vueltasSinPulsar = vueltasSinPulsar + 1;
      if (vueltasSinPulsar > VUELTAS_MAX_ENTRE_PULSACIONES) {
        pulsaciones = 0;
        vueltasSinPulsar = 0;
        Serial.println("Codigo incompleto: empieza de nuevo");
      }
    }

    // --- Sensor y sirena (sin delay largo: el programa sigue mirando el botón) ---
    if (armada && !sonando && digitalRead(PIN_PIR) == HIGH) {
      sonando = true;
      tonoAlto = true;
      vueltasSirena = 0;
      tone(PIN_ZUMBADOR, 2400);
      Serial.println("MOVIMIENTO DETECTADO");
    }
    if (sonando) {
      vueltasSirena = vueltasSirena + 1;
      if (vueltasSirena >= VUELTAS_POR_TONO) {    // pasaron 150 ms: cambia de tono
        vueltasSirena = 0;
        tonoAlto = !tonoAlto;
        if (tonoAlto) {
          tone(PIN_ZUMBADOR, 2400);
        } else {
          tone(PIN_ZUMBADOR, 1800);
        }
      }
    }
  }
  delay(10);                              // cada vuelta dura unos 10 ms
}
