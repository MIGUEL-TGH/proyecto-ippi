# Revisión del kit Arduino y plan de prácticas

**Kit:** REXQualis UNO R3 Complete Starter Kit (53 renglones; inventario completo en `kit-arduino/contenido-kit.png`)
**Carpeta revisada:** `kit-arduino/` (267 archivos, 183 MB) · **Fecha:** 2026-11-15
**Relacionado:** `hallazgos-ajuste-curso.md` · `plan-curso-arduino.md` (secuencia del curso, 16 nov)

> **Actualización 16 nov 2026:** el orden de prácticas del curso ya no es el de la sección 6 sino el de `plan-curso-arduino.md`. Esta revisión sigue valiendo como inventario, como lista de problemas del fabricante (sección 4) y como guía de las lecciones del kit que no entran en la secuencia principal (ampliaciones y proyecto final).

## 1. Conclusiones principales

1. **El kit alcanza para el curso actual**, con dos excepciones: no trae TMP36 ni ventilador de PC (sí trae termistor NTC, DHT11 y motor 3–6 V con aspa).
2. **Trae mucho más de lo que usa el curso:** 31 lecciones con código. Hay sensores con valor para una comunidad rural (humedad de suelo, nivel de agua, temperatura y humedad, movimiento, gas) que hoy no aparecen en ninguno de los materiales.
3. **Usa el código `.ino` y el tutorial en inglés, no el tutorial en español.** El español es traducción automática y corrompe el código impreso (sección 4).
4. **Los 33 sketches del kit compilan sin errores** (verificado el 16 nov con el `arduino-cli` 1.6.0 que trae Arduino IDE 2.x, placa Arduino UNO, núcleo `arduino:avr` 1.8.8, y las 7 librerías del kit). Compilar no prueba el circuito: falta probarlos con la placa conectada. El IDE ya está instalado en la PC de Miguel.
5. **Para varios alumnos se necesita un kit por equipo:** trae una sola placa y un solo módulo de cada sensor. Hay 6 kits; cada uno lo usarán 2–3 alumnos.

## 2. Qué contiene la carpeta `kit-arduino/`

| Carpeta o archivo | Contenido |
|---|---|
| `Tutorial/` | 33 PDF por idioma, en 5 idiomas (Español, English, Deutsch, Français, Italiano): prefacio, 31 lecciones y lista de empaque. Cada lección trae principio, código, diagrama, esquema y foto del circuito armado. Las capturas son del IDE 1.8.5 con interfaz en chino. |
| `Code/` | 33 sketches `.ino` en 31 carpetas (una por lección; la 27 y la 29 tienen dos variantes). Cada `.ino` está dentro de una carpeta con su mismo nombre, como pide el IDE. |
| `Libraries/` | 10 `.zip` (DS3231, HC-SR04, IRremote, Keypad, LedControl, LiquidCrystal, MPU6050, Servo, Stepper, rfid) y la carpeta LedControl suelta. |
| `Datasheets/` | 48 PDF de componentes (LED, DHT11, HC-SR04, PN2222, 74HC595, SG90, MQ2, MFRC522, DS3231, LCD1602A, etc.). |
| `Language Reference.pdf` | Referencia del lenguaje Arduino (2017, en inglés). |
| `Rexqualis UNO R3 , MEGA, DRIVER FAQ for window10.pdf.pdf` y `UNO R3,MEGA 2560 DRIVER FAQ.pdf` | Instalación del IDE y solución de problemas de driver. |
| `Read Me Frist.txt` | Indica cómo usar las carpetas. Soporte: service@rexqualis.com |
| `contenido-kit.png` | Foto escaneada de la lámina con todo el contenido del kit. |

## 3. Inventario del kit

Cruzado entre la lista de empaque del PDF y la foto `contenido-kit.png` (las 120 resistencias suman bien: 10+10+30+10×7).

| Categoría | Contenido |
|---|---|
| **Base** | Placa UNO R3 ×1 · cable USB ×1 · protoboard 830 puntos ×1 · placa de expansión con mini protoboard ×1 · módulo de fuente para protoboard (3.3/5 V) ×1 · adaptador 9 V 1 A ×1 · clip de batería con plug DC ×1 (sin pila) · jumpers M-M ×65 · cables Dupont M-F ×20 · CD con tutorial ×1 |
| **Entradas simples** | Botones ×5 · fotorresistor ×2 · termistor NTC ×2 · potenciómetro ×2 (tipo trimmer de 10 kΩ, rotulado B103) · interruptor de inclinación ×1 · joystick ×1 · teclado de membrana 4×4 ×1 · codificador rotatorio ×1 · receptor IR + control remoto ×1 |
| **Sensores** | Ultrasónico HC-SR04 · PIR HC-SR501 · DHT11 (temperatura y humedad) · sonido · nivel de agua · humedad de suelo · gas MQ-2 · acelerómetro/giroscopio MPU-6050 · reloj DS3231 · lector RFID RC522 (uno de cada uno) |
| **Salidas** | LED ×25 (5 de cada color: rojo, verde, azul, amarillo, blanco) · LED RGB ×1 · zumbador activo ×1 · zumbador pasivo ×1 · display 7 segmentos de 1 dígito ×1 y de 4 dígitos ×1 · LCD1602 con pines (sin I2C) ×1 · matriz LED MAX7219 ×1 · servo SG90 ×1 · motor DC 3–6 V ×1 + aspa · motor a pasos 28BYJ-48 + driver ULN2003 ×1 · relé 5 V ×1 |
| **Circuitos integrados y pasivos** | 74HC595 ×1 · L293D ×1 · transistor PN2222 ×5 · diodo 1N4007 ×5 · capacitores 10 µF ×5, 100 µF ×5, 22 pF ×5, 100 nF ×5 · resistencias: 10 Ω, 100 Ω, 330 Ω, 1 kΩ, 2 kΩ, 5.1 kΩ, 10 kΩ, 100 kΩ y 1 MΩ (10 de cada una) y 220 Ω ×30 |

## 4. Problemas del material del fabricante (para tenerlos presentes)

| # | Problema | Qué hacer |
|---|---|---|
| F1 | **El tutorial en español es traducción automática y corrompe el código impreso.** Ej. lección 3: `si (digitalRead…)` en vez de `if`, `leds byte = 0;` en vez de `byte leds = 0;`. Además hay restos de otras marcas («RuiiGuu» en 8 lecciones, «SunFounder» en la 20). La versión en inglés sí trae el código correcto. | Copiar el código del `.ino`, nunca del PDF en español. Usar el inglés como referencia técnica. |
| F2 | **Lección 20 (motor DC)** dice «usando un transistor», pero usa el L293D. | Para el proyecto con transistor se necesita un circuito propio con el PN2222 (sección 6, práctica A10). |
| F3 | **Lección 21 (relé):** el código es el mismo del motor con L293D más `Serial`; no menciona el relé. El diagrama muestra el relé conectado a una salida del L293D, sin explicar qué contacto conmuta. | Tratarla como lección del instructor. Ver seguridad (sección 7). |
| F4 | **Lección 18 (LCD)** maneja la pantalla en 8 bits con 11 líneas de datos y un driver escrito a mano (16 cables). La **lección 19** la usa en 4 bits con la librería LiquidCrystal. | Usar el método de la lección 19 en el curso. |
| F5 | **Lección 7 (fotorresistor)** exige 74HC595 + 8 LED + 14 jumpers para mostrar la luz en barra. Es pesada como primer contacto con un sensor analógico. | Hacer una versión simple (LDR + 10 kΩ + monitor serie) como práctica nueva. |
| F6 | **Librerías antiguas:** 6 de los 10 zip no traen `library.properties` (formato viejo). El IRremote incluido usa la API clásica (clases `IRrecv` y `decode_results`); las versiones nuevas del Gestor de bibliotecas (3.x y 4.x) cambiaron esa API, así que los sketches de las lecciones 15 y 16 probablemente no compilen con ellas. Servo, Stepper y LiquidCrystal ya vienen con el IDE. | Instalar IRremote **solo desde el zip del kit**. No instalar los zip de Servo, Stepper y LiquidCrystal. Si algún zip falla, copiar la carpeta a `Documentos\Arduino\libraries`. |
| F7 | **El FAQ de drivers recomienda «drivethelife»**, un instalador automático de terceros. | No instalarlo. En Windows 11 la placa suele reconocerse sola; si no, usar el driver oficial según el chip que se vea al conectarla. |
| F8 | **Potenciómetros de tipo trimmer** (para destornillador): incómodos para que un alumno los gire a mano. | Valorar comprar potenciómetros con perilla, o usar el joystick (dos ejes analógicos) para la práctica de entrada analógica. |
| F9 | **Lección 14 (DHT11)** usa código propio con acceso directo a puertos (pin A0) y Serial a 19200 baudios. Funciona, pero no es el estilo del resto. | Aceptable; avisar que el monitor serie debe ir a 19200. En el curso se usa la versión adaptada `P20_dht11` (9600 baudios, función reutilizable y límite de espera). |
| F10 | **Tres datos del motor que no coinciden.** `Datasheets/130 DC Motor.pdf` es de un motor de 4.5–9 V (corriente con carga hasta 250 mA, rotor bloqueado hasta 500 mA); la lección 20 describe uno de 3–6 V, 3 V nominales y 0.35–0.4 A; y la prueba de Miguel con fuente de poder dio **0.95 A**. No se sabe cuál es el real. | **Actualización 16 nov:** Miguel probó el motor con una fuente de poder y **funciona a partir de 0.95 A**, un tercer valor distinto. Si ese es su consumo sostenido, el circuito con PN2222 (máx. 600 mA) y módulo de fuente (máx. 700 mA) queda fuera de especificación. **No armar** hasta medir a 5 V (arranque y aspa girando libre). Opciones en `plan-curso-arduino.md`, sección 11 (V1). La resistencia de base de 330 Ω (unos 13 mA) solo es válida si el consumo es ≤ ~0.5 A. |

## 5. Cobertura del kit frente al curso actual

### Proyectos del PowerPoint

| Proyecto del PPT | Lección equivalente en el kit | Viable con el kit |
|---|---|---|
| P1 Conectando LED | Lección 1 (varios LED en paralelo con resistencia) | Sí |
| P2 LED con pulsador | Lección 3 | Sí |
| P3 Sensor de distancia + buzzer | Lecciones 11 + 4/5 | Sí |
| P4 Servomotor | Lección 17 | Sí |
| P5 Semáforo | Sin lección propia (3 LED, extiende la 1) | Sí, sketch nuevo |
| P6 Dado digital | Lección 8 (display 1 dígito) o 7 LED + botón | Sí, sketch nuevo |
| P7 Ventilador | Lección 20 (L293D) o circuito PN2222 + 1N4007 | **Rehacer** (hallazgo H3) |
| P8 Potenciómetro | Sin lección propia; joystick (lección 12) como alternativa | Sí, sketch nuevo |

### Capítulos del Word

| Del Word | En el kit |
|---|---|
| Práctica 1: LED con botón | Lección 3 |
| Práctica 2: LED con sensor de luz | Lección 7 (simplificar, F5) |
| Práctica 3: LED con potenciómetro | Sin lección propia (sketch nuevo) |
| Proyecto 1: alumbrado nocturno (LDR) | LDR + LED, sketch nuevo |
| Proyecto 2: indicador tricolor | Lección 2 (RGB) o 3 LED |
| Proyecto 3: botón de paro + LDR | Lecciones 3 + 7 |
| Cap. 9: barrera con zumbador, ultrasonido y servo | Lecciones 11 + 17 + 4 |
| Cap. 10: termostato LCD con **TMP36** | Lección 19 (LCD 4 bits + **termistor NTC**) |

### Lo que el kit ofrece y el curso no usa todavía

Lecciones 6, 8, 9 (registro 74HC595 y displays), 12 (joystick), 13 (teclado), 14 (DHT11), 15–16 (IR), 22 (matriz LED), 23 (MPU-6050), 24 (PIR), 25 (nivel de agua), 26 (reloj RTC), 27 (sonido), 28 (motor a pasos con encoder), 29 (RFID), 30 (gas MQ-2), 31 (humedad de suelo).

**Idea a valorar, no decidida:** proyectos con pertinencia local: aviso de riego con el sensor de humedad de suelo (31), nivel de agua de un tinaco (25), temperatura y humedad ambiente con DHT11 y LCD (14 + 19), alarma de movimiento con PIR (24; conecta con el sistema «Centinela» de Tekitl), alarma de gas con MQ-2 (30). Requiere que tú decidas el nivel y el tiempo disponible.

## 6. Plan de prácticas para ti

Cada práctica se hace con los archivos de `kit-arduino/Code/` (código) y el PDF de la lección en `Tutorial/English/` (diagrama). Anota en la última columna lo que necesites para ajustar el curso: tiempo real, dudas, errores y qué cambiarías.

### Sesión 0. Preparación (una sola vez)

- [x] **Arduino IDE 2.x instalado** (16 nov). Los 33 sketches del kit compilan con él, así que la versión 2.x no da problema con el código del kit.
- [ ] Conectar la placa y confirmar el puerto COM en el Administrador de dispositivos. Anotar qué chip USB aparece. Si no aparece, ver el FAQ de driver (y recordar F7).
- [ ] Subir `Archivo → Ejemplos → 01.Basics → Blink` (parpadea el LED integrado del pin 13). Con eso queda comprobada la placa, el cable y el puerto.
- [ ] Probar el **Monitor Serie** (lección 0 del tutorial).
- [ ] Instalar desde `Libraries/` solo estos zip, y **solo si vas a probar las lecciones del kit que las necesitan** (ampliaciones): **HC-SR04, Keypad, IRremote, LedControl, DS3231, MPU6050 y rfid** (`Sketch → Incluir biblioteca → Añadir biblioteca .ZIP`). No instalar Servo, Stepper ni LiquidCrystal (F6). **Los sketches de la secuencia principal del curso no necesitan ninguna librería externa** (Servo y LiquidCrystal ya vienen con el IDE).
- [ ] Copiar la carpeta `Code/` a `Documentos\Arduino\` para trabajar sobre una copia y no modificar la carpeta del repositorio.
- [ ] Revisar la etiqueta del adaptador de 9 V (entrada y polaridad del plug) antes de enchufarlo. La clavija es de tipo americano, compatible con los contactos de México.
- [ ] Tener a la mano un multímetro, si hay, para comprobar el transistor (práctica A10).

### Bloque A. Núcleo del curso

| # | Práctica | Fuente | Conexiones clave | Qué verificar | Anota |
|---|---|---|---|---|---|
| A1 | LED parpadeante | Lección 1 | LED en D8 con 220 Ω a GND | Parpadea cada segundo. Cambia `delay` y cambia el color del LED. | |
| A2 | LED con dos botones | Lección 3 | LED D5; botones D9 y D8 (`INPUT_PULLUP`, otro extremo a GND) | Un botón enciende, el otro apaga. Entender por qué la lógica es «invertida». | |
| A3 | LED RGB | Lección 2 | R D3, G D5, B D6 (PWM) con 220 Ω; cátodo común a GND | Rojo, verde, azul, blanco y púrpura. Probar otros valores 0–255. | |
| A4 | Zumbador activo y pasivo | Lecciones 4 y 5 | Zumbador en D12 (el activo suena con 5 V; el pasivo necesita `tone()`) | Distinguir uno de otro. Tocar las notas Do a Do agudo. | |
| A5 | Detector de movimiento PIR | Lección 24 | Sensor en D7; LED en D13; 3 cables M-F | Necesita casi un minuto para inicializar. Probar los dos potenciómetros del módulo (sensibilidad 3–7 m y tiempo de retardo). | |
| A6 | Medidor de distancia | Lección 11 | TRIG en D12, ECHO en D11; 4 cables M-F; monitor serie a 9600 | Distancia coherente con una regla. Probar con distintos materiales. | |
| A7 | Servo | Lección 17 | Señal en D9; 5 V y GND | Barrido de 0° a 180°. Probar mover a un ángulo fijo. | |
| A8 | Sensor de luz (versión simple) | **Sketch nuevo** (basado en lección 7) | LDR + 10 kΩ como divisor en A0; monitor serie | Valores cambian al tapar con la mano. Luego encender un LED por umbral. | |
| A9 | Entrada analógica con perilla | **Sketch nuevo** | Potenciómetro a A0; LED en pin PWM | Valor 0–1023 en el serie; brillo del LED cambia. Comparar con joystick (lección 12) por si el trimmer es incómodo (F8). | |
| A10 | Motor con transistor | **Circuito y sketch nuevos** | PN2222 + 1N4007 + motor 3–6 V con aspa; resistencia de 330 Ω en la base al pin 5 (esquema completo en el encabezado de `curso-arduino/sketches/P17_motor_boton`) | **Antes de armar:** comprobar el pinout con el datasheet (1 = emisor, 2 = base, 3 = colector, vista plana de frente) y, si hay multímetro, con prueba de diodo. El diodo va en paralelo con el motor, con la raya (cátodo) hacia +5 V. El motor consume unos 0.35–0.4 A según la lección 20: alimentarlo con el módulo de fuente, no con el pin de 5 V de la placa. | |
| A11 | Motor con L293D | Lección 20 | E1 D5, I1 D3, I2 D4; módulo de fuente a 5 V con el adaptador de 9 V | Alinear el módulo de fuente con los rieles (+ rojo, – azul). Solo se usa media mitad del L293D. Comparar con A10. | |
| A12 | Semáforo | **Sketch nuevo** | 3 LED + 3 resistencias de 220 Ω | Secuencia con tiempos distintos por color. | |
| A13 | Dado digital | Lección 8 (display) + **sketch nuevo** | 74HC595 + display 1 dígito + botón | Número aleatorio al pulsar. Decidir con este circuito si el dado del curso es de display o de 7 LED (H7). | |

### Bloque B. Pantallas y registro de desplazamiento

| # | Práctica | Fuente | Conexiones clave | Qué verificar | Anota |
|---|---|---|---|---|---|
| B1 | Ocho LED con 74HC595 | Lección 6 | Latch D4, clock D5, data D2; 14 cables M-M | Barrido de LED. Entender entradas y salidas en serie. | |
| B2 | Display de 7 segmentos (1 dígito) | Lección 8 | Latch D9, clock D10, data D8; 26 cables M-M | Cuenta de 0 a 15. Contar cuántos cables y cuánto tarda armarlo. | |
| B3 | Display de 4 dígitos | Lección 9 | Latch D9, clock D10, data D8; 23 cables | Anotar si es un buen reto o demasiado cableado para prepa. | |
| B4 | Termómetro con LCD | Lección 19 | LCD RS D7, E D8, datos D9–D12; termistor en A0 con 10 kΩ; potenciómetro para contraste | Temperatura en pantalla. Comparar con un termómetro. Es el reemplazo del TMP36 del Word. | |

### Bloque C. Sensores con pertinencia local

| # | Práctica | Fuente | Conexiones clave | Qué verificar | Anota |
|---|---|---|---|---|---|
| C1 | Temperatura y humedad (DHT11) | Lección 14 | Pin A0; 3 cables M-F; monitor serie a **19200** | Lecturas estables. Probar con aliento en el sensor. | |
| C2 | Humedad de suelo | Lección 31 | Sensor en A0; LED verde D6, rojo D7 | Calibrar con tierra seca, húmeda y agua. | |
| C3 | Nivel de agua | Lección 25 | Sensor en A0 | Lecturas con distinta profundidad. Mojar solo la parte con pistas; la electrónica del módulo debe quedar seca. | |
| C4 | Gas MQ-2 | Lección 30 | Sensor en A5; LED rojo D12, verde D11, zumbador D10 | Suele necesitar precalentamiento (ver `Datasheets/MQ2.pdf`); el sensor se calienta. Probar con el humo de un fósforo, a distancia, en un lugar ventilado. | |
| C5 | Sensor de sonido | Lección 27 | A0 (analógico) o D3 (digital); LED D13 | Respuesta a una palmada; ajustar el potenciómetro del módulo. | |

### Bloque D. Opcionales y avanzadas (solo si el tiempo alcanza)

| # | Práctica | Fuente | Nota |
|---|---|---|---|
| D1 | Joystick | Lección 12 | SW D3, X A0, Y A1. Alternativa a la perilla (F8). |
| D2 | Teclado de membrana | Lección 13 | Filas D9–D6, columnas D5–D2. Librería Keypad. |
| D3 | Receptor IR | Lección 15 | D11. Solo con el IRremote del zip del kit (F6). |
| D4 | Interruptor de inclinación | Lección 10 | LED D8; el sensor entra por A5. |
| D5 | Matriz LED MAX7219 | Lección 22 | DIN D12, CLK D10, CS D11. Librería LedControl. |
| D6 | Reloj RTC DS3231 | Lección 26 | I2C. Librerías Wire y DS3231. |
| D7 | MPU-6050 | Lección 23 | I2C, dirección 0x68. |
| D8 | RFID RC522 | Lección 29 | RST D9, SS D10 y bus SPI. La lección sobrescribe tarjetas regrabables: usar con cuidado. |
| D9 | Motor a pasos con control remoto | Lección 16 | Pines 8–11 + IR D12. Necesita fuente externa. |
| D10 | Motor a pasos con encoder | Lección 28 | CLK D2, DT D3, SW D4. Necesita fuente externa. |
| D11 | Relé | Lección 21 | Ver F3 y la sección 7. |

### Sketches nuevos que hay que preparar

Para A8, A9, A10, A12 y A13 no existe código en el kit. **Ya están escritos y compilados** (16 nov) dentro de la secuencia del curso, en `curso-arduino/sketches/` (66 sketches, 0 errores, 0 avisos). Equivalencias: A8 → `P11`/`P12`, A9 → `P09`/`P10`, A10 → `P17`/`P18`, A12 → `P04` (y `X02`), A13 → `X01` (dado con 6 LED en lugar de display). Para recompilar tras editar: `curso-arduino/compilar-sketches.ps1`. Falta probarlos con la placa y el circuito; ver `plan-curso-arduino.md`, sección 11.

## 7. Seguridad (para las prácticas y para el aula)

- **Todo LED lleva resistencia** (220 Ω en el kit).
- **Nunca conectar motores ni el motor a pasos a un pin del Arduino.** Se alimentan con el módulo de fuente o con el L293D (lecciones 16, 20, 28). El módulo de fuente debe quedar con el **+ alineado al riel rojo y el – al azul**; un montaje invertido puede dañar el proyecto. Dejar el jumper en 5 V para estos motores.
- **Relé:** los contactos del SRD-05VDC soportan hasta 10 A a 250 VCA. En clase se usa **solo con bajo voltaje** (el motor). **Prohibido conectarlo a la red eléctrica.**
- **MQ-2:** se calienta al usarse; no tocarlo durante la práctica. Probar con humo siempre en un lugar ventilado y a distancia.
- **Sensor de nivel de agua y de humedad de suelo:** mojar solo el extremo de la sonda, con la placa lejos del agua.
- **Antes de energizar:** revisar polaridad, que ninguna pata de componente toque otra y que el Arduino no esté sobre una superficie metálica.
- **Adaptador de 9 V:** confirmar en su etiqueta que acepta el voltaje de la red local antes de enchufarlo.

## 8. Pendientes

- [x] ~~Instalar Arduino IDE (o arduino-cli) para compilar los sketches~~ → hecho; se usa el `arduino-cli` incluido en el IDE.
- [x] ~~Compilar los sketches del kit y los nuevos~~ → 33/33 del kit y 44/44 nuevos (30 de la secuencia y 14 soluciones de retos) sin errores.
- [ ] Probar con la placa y anotar tiempos y dudas (ahora en el orden del curso: `plan-curso-arduino.md`, sección 11).
- [x] ~~Decidir qué práctica de los bloques B y C entran al curso~~ → decidido en el plan (humedad de suelo, nivel de agua, DHT11, LCD y PIR entran; el resto queda como ampliación).
- [ ] Confirmar si habrá computadoras e internet (H9 en `hallazgos-ajuste-curso.md`). Ya se sabe que son 6 kits con 2–3 alumnos cada uno.
- [ ] Decidir si se compran potenciómetros con perilla (F8); el plan los recomienda (sección 10).
