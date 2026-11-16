/*
  P25 · Indicador de nivel de agua (modelo de tinaco o cisterna)     Sesión 13
  ------------------------------------------------------------------
  Qué hace: mide el nivel de agua en un vaso o botella y lo indica con tres LED.
  Si el nivel está muy bajo, además suena un pitido de aviso.
     LED rojo     = nivel bajo (hay que llenar)
     LED amarillo = nivel medio
     LED verde    = nivel alto (lleno)

  Conexiones:
    Sensor de nivel de agua   + -> 5 V ; - -> GND ; S (señal) -> A0
    LED rojo      pin 8  -> resistencia 220 ohm -> LED (+) ; pata corta -> GND
    LED amarillo  pin 9  -> resistencia 220 ohm -> LED (+) ; pata corta -> GND
    LED verde     pin 10 -> resistencia 220 ohm -> LED (+) ; pata corta -> GND
    Zumbador PASIVO   una pata -> pin 12 ; otra pata -> GND   (tone() necesita el pasivo)

  CALIBRACIÓN: pon el sensor en el vaso con poca, media y mucha agua y anota las lecturas
  en el Monitor Serie. Ajusta NIVEL_BAJO y NIVEL_ALTO con tus números. Los valores que
  dejé son solo un punto de partida.

  Cuidado: moja solo la parte con las pistas (las líneas metálicas). La placa electrónica
  y los cables deben quedar secos. Y todo lejos del Arduino. Agua y electricidad solo
  con los 5 V del kit; nunca conectes nada a la corriente de la casa.

  Ideas clave:
    - Varios niveles con if / else if / else.
    - El mismo principio se usa en un tinaco real, que activa una bomba o una alarma.

  Retos:  - Haz que el zumbador también avise cuando el nivel sea muy alto (se derrama).
          - Agrega un motor (como en P17) que simule la bomba: se enciende con nivel bajo
            y se apaga cuando está lleno (usa histéresis como en la sesión 12).
*/

const int PIN_SENSOR = A0;
const int LED_ROJO = 8;
const int LED_AMARILLO = 9;
const int LED_VERDE = 10;
const int PIN_ZUMBADOR = 12;

const int NIVEL_BAJO = 150;           // menos de esto = bajo   (AJUSTA con tu medición)
const int NIVEL_ALTO = 400;           // más de esto = alto     (AJUSTA con tu medición)

void setup() {
  pinMode(LED_ROJO, OUTPUT);
  pinMode(LED_AMARILLO, OUTPUT);
  pinMode(LED_VERDE, OUTPUT);
  pinMode(PIN_ZUMBADOR, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int nivel = analogRead(PIN_SENSOR);

  digitalWrite(LED_ROJO, LOW);
  digitalWrite(LED_AMARILLO, LOW);
  digitalWrite(LED_VERDE, LOW);

  Serial.print("Lectura: ");
  Serial.print(nivel);
  Serial.print("    ");

  if (nivel < NIVEL_BAJO) {
    digitalWrite(LED_ROJO, HIGH);
    tone(PIN_ZUMBADOR, 800, 100);
    Serial.println("Nivel BAJO");
  } else if (nivel < NIVEL_ALTO) {
    digitalWrite(LED_AMARILLO, HIGH);
    noTone(PIN_ZUMBADOR);
    Serial.println("Nivel medio");
  } else {
    digitalWrite(LED_VERDE, HIGH);
    noTone(PIN_ZUMBADOR);
    Serial.println("Nivel ALTO");
  }
  delay(500);
}
