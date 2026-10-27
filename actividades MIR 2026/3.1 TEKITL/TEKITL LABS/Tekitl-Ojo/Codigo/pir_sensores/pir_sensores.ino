const int pinPIR = 2;       // Pin del sensor PIR
int estadoAnterior = LOW;   // Guarda el estado del ciclo anterior

unsigned long tiempoEspera = 3000; // 3 segundos de bloqueo para no saturar
unsigned long ultimaDeteccion = 0;

void setup() {
  Serial.begin(9600);
  pinMode(pinPIR, INPUT);
  
  // Calibración inicial del PIR
  delay(2000); 
  Serial.println("LISTO");
}

void loop() {
  int estadoActual = digitalRead(pinPIR);
  unsigned long tiempoActual = millis();

  // 1. Detectamos el MOMENTO EXACTO en que empieza el movimiento
  // (Pasa de LOW a HIGH) y verificamos que ya pasaron los 3 segundos
  if (estadoActual == HIGH && estadoAnterior == LOW) {
    if (tiempoActual - ultimaDeteccion >= tiempoEspera) {
      
      Serial.println("5"); // Enviamos el "5" a Python
      ultimaDeteccion = tiempoActual; // Reiniciamos el temporizador de bloqueo
      
    }
  }

  // 2. Guardamos el estado para el próximo ciclo del loop
  estadoAnterior = estadoActual;
}