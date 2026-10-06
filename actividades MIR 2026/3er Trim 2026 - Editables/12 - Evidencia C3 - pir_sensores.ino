const int pinPIR = 2; // Pin donde conectas el OUT del PIR
bool detectado = false;
unsigned long tiempoEspera = 3000; // 3 segundos para evitar rebotes
unsigned long ultimaDeteccion = 0;

void setup() {
  Serial.begin(9600);
  pinMode(pinPIR, INPUT);
  
  // Espera a que el PIR se estabilice (calibración)
  delay(2000); 
  Serial.println("LISTO");
}

void loop() {
  int estado = digitalRead(pinPIR);

  // Si detecta movimiento y ya pasó el tiempo de espera
  if (estado == HIGH && (millis() - ultimaDeteccion > tiempoEspera)) {
    Serial.println("5"); // Envía el "1" para que Python reproduzca el primer audio
    ultimaDeteccion = millis();
  }
}