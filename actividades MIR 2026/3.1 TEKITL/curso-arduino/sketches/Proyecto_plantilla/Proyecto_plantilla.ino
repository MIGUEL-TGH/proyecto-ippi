/*
  PROYECTO FINAL · Plantilla                                   Sesiones 14 a 16
  ------------------------------------------------------------------
  Equipo: ______________________      Proyecto: ______________________
  Integrantes: ______________________________________________________

  Qué problema resuelve:   ____________________________________________
  ENTRADA  (qué mide):      ____________________________________________
  PROCESO  (qué decide):    ____________________________________________
  SALIDA   (qué hace o muestra): _______________________________________

  Conexiones (llénalas al armar; son las mismas de tu hoja de diseño):
    ______________________  ->  ______________________
    ______________________  ->  ______________________
    ______________________  ->  ______________________

  CÓMO SE USA ESTA PLANTILLA
  Ya funciona tal cual, para que veas la estructura: con una perilla en A0 y un LED con
  resistencia de 220 ohm en el pin 5, el LED se enciende cuando la perilla pasa de UMBRAL y se
  apaga cuando baja de UMBRAL - HISTERESIS. Para tu proyecto:
    1) Cambia los pines de la sección 1 por los tuyos (mira el mapa de pines de la guía).
    2) Cambia medir() por la lectura de tu sensor (analogRead, la función del DHT11, etc.).
    3) Cambia decidir() por tus reglas (umbrales, zonas, estados).
    4) Cambia actuar() por lo que tu proyecto hace (LED, zumbador, servo, motor...).
    5) Cambia mostrar() por lo que verás en el Monitor Serie (y en la pantalla, si la usas).
  Para juntar partes de otros sketches del curso: copia sus constantes, su setup() y sus
  funciones, sin repetir ningún nombre. Prueba después de CADA parte que agregues.

  Ideas clave:
    - Un proyecto es un ciclo que se repite: MEDIR -> DECIDIR -> ACTUAR -> MOSTRAR.
    - Los pines y los valores que se ajustan van ARRIBA, con nombre: así se cambian en un solo lugar.
    - Una variable de estado (encendido) recuerda lo que pasó antes (Sesión 3 y Sesión 12).
    - Una tarea por función: si algo falla, sabes en cuál buscar (¿mide mal? ¿decide mal? ¿actúa mal?).
    - Si tu sensor puede fallar (como el termistor), apaga la salida y avisa en lugar de seguir con un
      dato falso (Sesión 12).

  Prueba que dejas por escrito (hoja de pruebas): qué haces, qué debe pasar y qué pasó de verdad.
*/

// ---- 1. PINES (todos juntos, cada uno con su nombre)
const int PIN_ENTRADA = A0;            // el sensor (aquí, una perilla)
const int PIN_SALIDA = 5;              // lo que se enciende (aquí, un LED con 220 ohm)

// ---- 2. VALORES QUE SE AJUSTAN (calibración y umbrales)
const int UMBRAL = 600;                // por encima de esto se enciende      (AJUSTA con tu medición)
const int HISTERESIS = 40;             // margen para apagar, evita el "temblor" (Sesión 12)
const int ESPERA_MS = 200;             // pausa de cada vuelta, en milisegundos

// ---- 3. VARIABLES QUE RECUERDAN
bool encendido = false;

// ---- 4. TAREAS (una por función)
int medir() {
  return analogRead(PIN_ENTRADA);
}

void decidir(int valor) {
  if (!encendido && valor >= UMBRAL) {
    encendido = true;
  } else if (encendido && valor <= UMBRAL - HISTERESIS) {
    encendido = false;
  }
}

void actuar() {
  if (encendido) {
    digitalWrite(PIN_SALIDA, HIGH);
  } else {
    digitalWrite(PIN_SALIDA, LOW);
  }
}

void mostrar(int valor) {
  Serial.print("Valor:");
  Serial.print(valor);
  Serial.print(",Estado:");
  if (encendido) {
    Serial.println(1);
  } else {
    Serial.println(0);
  }
}

void setup() {
  pinMode(PIN_SALIDA, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int valor = medir();                 // 1. MEDIR
  decidir(valor);                      // 2. DECIDIR
  actuar();                            // 3. ACTUAR
  mostrar(valor);                      // 4. MOSTRAR
  delay(ESPERA_MS);
}
