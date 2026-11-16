/*
  P02_SOS · Señal de auxilio en código Morse
  ------------------------------------------------------------------
  S = 3 destellos cortos      O = 3 destellos largos      S = 3 destellos cortos

  Reglas del Morse (todo se mide en una "unidad" de tiempo):
    - destello corto    = 1 unidad
    - destello largo    = 3 unidades (el triple del corto)
    - pausa entre destellos de una misma letra = 1 unidad
    - pausa entre letras                       = 3 unidades
    - pausa entre palabras (aquí: antes de repetir SOS) = 7 unidades

  Conexión: igual que P02 (LED con resistencia de 220 ohm en el pin 8).
  Reto:     cambia el valor de "corto" (por ejemplo a 100 o a 400) y mira
            cómo se ve el SOS más rápido o más lento. Ojo: si cambias
            "corto", cambia también los demás para respetar las reglas.
*/

int pinLed = 8;

int corto = 200;           // destello corto (milisegundos)
int largo = 600;           // destello largo = 3 x corto
int pausa = 200;           // pausa entre destellos de la misma letra = 1 x corto
int pausaLetra = 400;      // pausa extra al terminar una letra: 200 + 400 = 600 (3 x corto)
int pausaPalabra = 1200;   // pausa extra al terminar el SOS: 200 + 1200 = 1400 (7 x corto)

void setup() {
  pinMode(pinLed, OUTPUT);
}

void loop() {
  // S = 3 CORTOS ======================================================
  digitalWrite(pinLed, HIGH);
  delay(corto);
  digitalWrite(pinLed, LOW);
  delay(pausa);

  digitalWrite(pinLed, HIGH);
  delay(corto);
  digitalWrite(pinLed, LOW);
  delay(pausa);

  digitalWrite(pinLed, HIGH);
  delay(corto);
  digitalWrite(pinLed, LOW);
  delay(pausa);

  delay(pausaLetra);   // fin de la letra S

  // O = 3 LARGOS ======================================================
  digitalWrite(pinLed, HIGH);
  delay(largo);
  digitalWrite(pinLed, LOW);
  delay(pausa);

  digitalWrite(pinLed, HIGH);
  delay(largo);
  digitalWrite(pinLed, LOW);
  delay(pausa);

  digitalWrite(pinLed, HIGH);
  delay(largo);
  digitalWrite(pinLed, LOW);
  delay(pausa);

  delay(pausaLetra);   // fin de la letra O

  // S = 3 CORTOS ======================================================
  digitalWrite(pinLed, HIGH);
  delay(corto);
  digitalWrite(pinLed, LOW);
  delay(pausa);

  digitalWrite(pinLed, HIGH);
  delay(corto);
  digitalWrite(pinLed, LOW);
  delay(pausa);

  digitalWrite(pinLed, HIGH);
  delay(corto);
  digitalWrite(pinLed, LOW);
  delay(pausa);

  delay(pausaPalabra); // fin de la palabra: espera antes de repetir
}
