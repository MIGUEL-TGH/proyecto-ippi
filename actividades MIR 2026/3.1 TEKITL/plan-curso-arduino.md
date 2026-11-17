# Plan del curso: Electrónica y programación con Arduino

**Destino:** alumnos de preparatoria, San Juan Atzingo, San Gabriel Chilac, Puebla
**Versión:** 1 (propuesta para revisión) · **Fecha:** 2026-11-16
**Escrito para:** Miguel, como instructor responsable del curso. No es material para los alumnos: de aquí salen la presentación, las fichas y la bitácora.
**Relacionado:** `hallazgos-ajuste-curso.md` · `revision-kit-arduino.md` · `curso-arduino/sketches/` (38 sketches compilados)

## 1. Resumen

- **El curso completo es de 16 sesiones de 2 horas (32 h)** y va de «prender un LED» a un proyecto final propio, con **25 prácticas** y 2 de ampliación. Miguel decidió el 16 nov **conservar las 32 h**: no cabe todo en la primera visita, y lo que falte se imparte **en otras fechas**. La sección 3b propone cómo repartirlo en visitas de 8 h.
- Cada sesión introduce **una idea nueva** y termina con algo que funciona. El orden cuida que nada use un concepto que todavía no se vio.
- Se **omiten el sensor TMP36 y el ventilador de PC**. El «ventilador» es el motor 3–6 V con aspa del kit, controlado con transistor; la temperatura se mide con el termistor NTC y el DHT11.
- Se **incorporan los sensores del kit que no se usaban**: humedad de suelo, nivel de agua, DHT11, PIR y pantalla LCD, con situaciones cercanas a la comunidad (riego, tinaco, alarma, calor).
- **No hay que instalar librerías ni usar internet:** Servo y LiquidCrystal ya vienen con el Arduino IDE; el sensor de distancia y el DHT11 se leen con código propio.
- Los **38 sketches** (28 de la secuencia y 10 soluciones de retos) están en `curso-arduino/sketches/`. **Compilan sin errores ni avisos**, pero **ninguno se ha probado en la placa**. Eso es lo que sigue (sección 11).
- **La primera visita es de dos días de 4 horas (8 h) = las sesiones 1 a 4**, y termina con una alarma de movimiento. Las visitas siguientes están por definir (sección 3b).
- **Motor:** la medición de Miguel (el motor «3–6 V» funciona a partir de **0.95 A**) deja fuera de especificación el circuito con PN2222 y módulo de fuente. **No se arma hasta resolverlo** (sesión 9 y sección 11, V1).
- **Confirmado el 16 nov:** hay 6 computadoras (una por kit) y los retos del proyecto final están bien.

## 2. Premisas y supuestos

| Tema | Premisa | Origen |
|---|---|---|
| Equipo | 6 kits; cada kit lo usan 2–3 alumnos, así que **12 a 18 alumnos por curso** | Miguel, 16 nov |
| Materiales omitidos | Sensor TMP36 y ventilador de PC | Miguel, 16 nov |
| Software | Arduino IDE 2.x. Nada de Tinkercad ni de internet durante el curso | Decisión de este plan |
| Computadoras | Una por kit (6) | Miguel, 16 nov (confirmado) |
| Nivel de partida | Sin experiencia previa en electrónica ni programación | **Supuesto** |
| Duración | **Curso completo: 32 h (16 sesiones de 2 h).** Primera visita: dos días de 4 horas; el resto, en otras fechas por definir. Un día de 4 h cabe con dos sesiones | Miguel, 16 nov |
| Motor | Funciona a partir de 0.95 A (medido con una fuente de poder; condiciones por aclarar) | Miguel, 16 nov |
| Instructores | Uno, ideal un apoyo (docente o alumno avanzado) para 6 equipos | **Supuesto** |

## 3. Línea de tiempo

| Etapa | Sesión | Título | Prácticas | Al terminar, el equipo muestra… | Visita |
|---|---|---|---|---|---|
| **1. Salidas y tiempo** | 1 | Hola, Arduino | P01 Blink · P02 LED externo | Un LED propio que parpadea | 1 |
| | 2 | Luces con tiempos | P03 dos LED alternados · P04 semáforo | Un semáforo con tiempos elegidos por ellos | 1 |
| **2. Entradas digitales** | 3 | Botones | P05 botón y LED · P06 botón con memoria | Un LED que se prende y apaga con cada toque y cuenta las pulsaciones | 1 |
| | 4 | Sonido y alarma de movimiento | P07 zumbadores · P08 alarma PIR | Una alarma que se arma con un botón y suena con movimiento | 1 |
| **3. Entradas analógicas** | 5 | Perilla y brillo | P09 perilla y números · P10 perilla y brillo | Un LED regulable con la perilla | 2 |
| | 6 | Luz y decisiones | P11 sensor de luz · P12 lámpara nocturna | Una lámpara que enciende sola en la oscuridad | 2 |
| **4. Movimiento** | 7 | Servo | P13 barrido · P14 servo con perilla | Un servo que sigue la perilla | 2 |
| | 8 | Distancia y barrera | P15 medidor · P16 barrera automática | Una barrera que se abre al acercar un objeto | 2 |
| | 9 | Motor y transistor | P17 motor con botón · **P18 velocidad con perilla** | Un motor con aspa cuya velocidad regulan ellos | 3 |
| **5. Datos y sistemas** | 10 | Temperatura | P19 termistor · P20 DHT11 | Dos sensores de temperatura comparados con un termómetro | 3 |
| | 11 | Pantalla LCD | P21 primer mensaje · P22 estación de clima | Temperatura y humedad en pantalla | 3 |
| | 12 | Ventilador automático | P23 termostato | Un ventilador que enciende solo al calentarse, con límite ajustable | 3 |
| | 13 | Campo y agua | P24 aviso de riego · P25 nivel de agua | Calibración con tierra y agua reales | 4 |
| **6. Proyecto** | 14 | Proyecto: diseño y armado | Reto elegido | Diseño en papel y primer circuito funcionando | 4 |
| | 15 | Proyecto: pruebas y mejora | Reto elegido | Proyecto probado y documentado | 4 |
| | 16 | Exhibición y cierre | Presentaciones | Demostración de 5 minutos por equipo | 4 |

**Tu secuencia de ejemplo cabe así:** 1. prender un LED → sesión 1 · 2. dos LED con tiempos → sesión 2 · 3. LED con botón apoyado en variables → sesión 3 · 4. velocidad del motor con potenciómetro → **sesión 9** (antes hay que ver la perilla, la señal analógica y el PWM, y entender por qué el motor no se conecta directo al pin).

**Respaldo, solo si el tiempo se acorta. Recorte a 13 sesiones (26 h):** se omiten la sesión 4 y la sesión 8, y las sesiones 14 y 15 se unen en una. Lo omitido no es requisito de lo que sigue. Dos ajustes: el zumbador (P07) se hace en 20 minutos al inicio de la sesión 13, y el servo (sesión 7) queda sin la barrera.
**Recorte a 11 sesiones (22 h):** además se omiten la sesión 7 (servo) y la sesión 10; el DHT11 se ve dentro de la sesión 11 y el termistor en los primeros 30 minutos de la 12. Con menos de 11 sesiones habría que renunciar al proyecto final o a la integración de la sesión 12.

### 3b. Cómo se reparte en visitas

Decisión de Miguel (16 nov): **se conserva el curso completo de 16 sesiones (32 h)**. La primera visita son **dos días de 4 horas** y no alcanza para todo; lo que falte se imparte **en otras fechas**. Propuesta de reparto en visitas de 8 h (2 días × 4 h), con dos sesiones por día. **Cada visita termina con algo que funciona**, de modo que lo aprendido sirve completo aunque no haya más visitas:

| Visita | Día 1 | Día 2 | Termina con |
|---|---|---|---|
| **1** | Sesión 1 Hola, Arduino + sesión 2 Luces con tiempos | Sesión 3 Botones + sesión 4 Sonido y alarma | **Alarma de movimiento** |
| **2** | Sesión 5 Perilla y brillo + sesión 6 Luz y decisiones | Sesión 7 Servo + sesión 8 Distancia y barrera | **Barrera automática** |
| **3** | Sesión 9 Motor y transistor + sesión 10 Temperatura | Sesión 11 Pantalla LCD + sesión 12 Ventilador automático | **Ventilador automático** |
| **4** | Sesión 13 Campo y agua + sesión 14 Proyecto: diseño y armado | Sesión 15 Proyecto: pruebas + sesión 16 Exhibición y cierre | **Proyecto final** |

Cuántas visitas habrá y cuándo es lo que **falta definir**. Si las visitas duran otra cosa, el corte se mueve, pero la regla es la misma: cerrar cada visita con una demostración.

**Un día de 4 horas con dos sesiones** (la apertura y el cierre se comparten, por eso cada sesión queda en unos 95 minutos de trabajo en lugar de los 120 de la sección 6):

| Min | Actividad |
|---|---|
| 0–15 | Apertura: inventario del kit, repaso, bitácora |
| 15–110 | Primera sesión del día (idea 15 min, práctica 1, práctica 2 y retos) |
| 110–125 | Descanso |
| 125–220 | Segunda sesión del día |
| 220–240 | Cierre: bitácora, visto bueno, guardar los kits |

**Qué cuidar por volver en otras fechas**

- **Repaso práctico al inicio de cada visita (15 min):** cada equipo reconstruye en 10 minutos un circuito de la visita anterior. Recupera la destreza y, de paso, se revisa que el kit esté completo.
- **Dónde se guardan los kits y las computadoras entre visitas** (y quién cuenta las piezas al terminar). **Por definir con la escuela.** Cada kit lleva su hoja de inventario.
- **Sketches y bitácoras:** los sketches de `curso-arduino/sketches/` se copian a cada computadora en la primera visita y se confirma en cada regreso que siguen ahí. La bitácora puede quedarse en una carpeta del equipo.
- **Alumnos que faltan o se suman:** cada guía de sesión permite ponerse al corriente solo, y el repaso práctico nivela en parte.
- **Entre visitas (opcional, sin computadora ni internet):** un reto en papel, por ejemplo dibujar el diagrama de tiempos o el esquema del circuito que se verá después.
- **Motor:** la visita 3 empieza con el motor. Hay tiempo antes de esa fecha para resolver el consumo (V1, sección 11).
- **Preparación:** para la visita 1 ya están las guías de las sesiones 1 a 4 (`curso-arduino/guias/S01-*.md` a `S04-*.md`), con dos diagramas por circuito: protoboard (para armar) y cableado con colores de cable (para entender). La sesión 3 agrega diagramas de pull-up, rebote y estados; la 4, de zumbadores, frecuencia, `for`, el módulo PIR, su señal en el tiempo y los estados de la alarma. Falta que Miguel las practique y dé retroalimentación (sesión por sesión).

## 4. Escalera de conceptos

Cada fila solo usa lo de las filas de arriba.

| Sesión | Electrónica | Programación | Instrucciones o ideas nuevas |
|---|---|---|---|
| 1 | Circuito cerrado, polaridad del LED, resistencia limitadora, protoboard | Estructura `setup`/`loop`, subir un programa, comentarios | `pinMode`, `digitalWrite`, `delay`, `HIGH`/`LOW` |
| 2 | Varias salidas, GND común | Variables, constantes y funciones propias | `int`, `const`, `void luces(...)` |
| 3 | Entrada digital, resistencia pull-up, lógica invertida | Decisiones, variable de estado, antirrebote | `digitalRead`, `INPUT_PULLUP`, `if/else`, `==` vs `=`, `bool`, `!`, `&&`, `!=`, `Serial.print`; `%` solo en un reto |
| 4 | Sonido como vibración, límite de corriente de un pin, sensor digital (PIR) | Repetir con `for`, funciones con parámetros, salir con `break` | `tone`, `noTone`, `for`, `break`; `millis()` solo para poner la hora en el Monitor Serie |
| 5 | Señal analógica, divisor de voltaje, PWM | Cambiar de escala | `analogRead`, `analogWrite`, `map`, `float` |
| 6 | Sensor resistivo (LDR), calibración | Umbral y comparaciones | `<`, `>`, combinar dos lecturas |
| 7 | Servo: se pide un ángulo | `for` con contador, librerías y objetos | `#include <Servo.h>`, `attach`, `write` |
| 8 | Ultrasonido: tiempo de vuelo | Funciones que devuelven un valor, `while` | `pulseIn`, funciones con retorno |
| 9 | Corriente de un pin vs corriente de un motor, transistor, diodo, fuente externa | PWM sobre una carga de potencia, zona muerta | `analogWrite` sobre el transistor |
| 10 | NTC (no lineal), sensor digital con chip propio, precisión | Función como caja negra, promedios | `log`, `float`, `byte` |
| 11 | Pantalla LCD en 4 bits | Librerías de terceros | `LiquidCrystal`, `setCursor`, `print`, `millis` |
| 12 | Sistema de control: medir, comparar, actuar | Histéresis, variable de estado + integración | condiciones con `&&`, `else if` |
| 13 | Sensores de campo, corrosión de sondas | Calibrar con datos, niveles | `map` invertido, `constrain` |
| 14–16 | Diseño de un sistema | Planear, depurar, documentar | todo lo anterior |

## 5. Fichas por sesión

Cada ficha trae: objetivo, prácticas con su sketch, teoría breve (≈15 min), retos, un fallo para «rompe y arregla» y qué evidencia entrega el equipo. «Word» indica qué capítulo del manual sirve de lectura de apoyo.

### Sesión 1 · Hola, Arduino
- **Objetivo:** subir un programa a la placa y encender un LED externo.
- **Prácticas:** P01 `Archivo → Ejemplos → 01.Basics → Blink` (sin cables: prueba placa, cable y puerto). P02 `P02_led_parpadeo`.
- **Teoría:** circuito cerrado; polaridad del LED; por qué la resistencia (5 V − 2 V ÷ 220 Ω ≈ 14 mA); filas y rieles del protoboard. *Word, cap. 1 y 2.*
- **Retos:** LED fijo (quitar el contenido de `loop`), parpadeo rápido y lento, señal de SOS.
- **Rompe y arregla:** el cable de señal en el pin 7 en lugar del 8: el LED no parpadea y el equipo relaciona el número del código con el pin físico. **No se planea el LED al revés:** el datasheet del kit da 5 V como máximo en inversa y el pin entrega 5 V, sin margen.
- **Evidencia:** LED parpadeando y dos cambios anotados en la bitácora.
- **Cuidado:** primero solo USB; el adaptador de 9 V no se usa todavía. Guía de práctica con diagramas: `curso-arduino/guias/S01-hola-arduino.md`.

### Sesión 2 · Luces con tiempos
- **Objetivo:** controlar varias salidas y cambiar el comportamiento modificando un solo número.
- **Prácticas:** `P03_dos_led_alternados` (variable `tiempoEncendido`) · `P04_semaforo` (constantes y la función `luces`).
- **Teoría:** variable = caja con nombre; constante; ejecución en orden; «un cambio, un solo lugar». *Word, cap. 3.*
- **Retos:** tiempos distintos por color; verde que parpadea antes del amarillo; dibujar el diagrama de tiempos en el cuaderno antes de programar.
- **Rompe y arregla:** el instructor quita un `;` o cambia un nombre; el equipo aprende a leer el mensaje rojo del IDE.
- **Evidencia:** semáforo con tiempos propios.

### Sesión 3 · Botones
- **Objetivo:** leer una entrada y recordar un estado (tu ejemplo 3: prender y apagar con un botón apoyado en variables).
- **Prácticas:** `P05_boton_led` (enciende mientras se presiona) · `P06_boton_toggle` (un toque enciende, otro apaga; cuenta pulsaciones en el Monitor Serie).
- **Teoría:** entrada vs salida; pull-up y lógica «invertida»; `if/else`; variable de estado; rebote de contactos. *Word, cap. 3 («Controlar el LED mediante un botón» y «Probar, observar y corregir»).*
- **Retos:** LED amarillo opuesto al rojo (`P05_dos_led_opuestos`); quitar el antirrebote y ver qué pasa; parpadear 3 veces cada 5 pulsaciones (`P06_parpadeo_cada_5`). **Reto de cierre:** semáforo con botón para peatones (`P06_semaforo_con_boton`), que une las sesiones 2 y 3 y responde a la pregunta con que cierra la sesión 2. La ampliación `X02_semaforo_peatonal` (con `millis()`, sesión 11) y `X01_dado_leds` quedan para más adelante.
- **Rompe y arregla:** (a) quitar el cable de GND del botón: el LED nunca enciende; (b) `=` en lugar de `==`: error `lvalue required as left operand of assignment`; (c) `INPUT` en lugar de `INPUT_PULLUP`: pin flotante, LED errático (no probado en placa). **Se cambió el fallo «botón girado 90°, siempre presionado»:** qué patas del botón van unidas por dentro depende de cómo venga el botón (la hoja de datos dice que las de lado a lado del canal; sin comprobar con el botón real), así que ese fallo no es predecible. En su lugar el circuito se arma con los dos cables en patas **opuestas (diagonal)**, que funciona con cualquiera de las dos formas.
- **Evidencia:** foto o captura del Monitor Serie mostrando las pulsaciones.
- **Guía de práctica con diagramas:** `curso-arduino/guias/S03-botones.md` (protoboard, cableado, patas del botón, pull-up, rebote y estados).

### Sesión 4 · Sonido y alarma de movimiento
- **Objetivo:** producir sonido, repetir con `for`, usar un sensor digital y combinarlo con lo anterior.
- **Prácticas:** `P07a_zumbador_activo` (empieza con el paso 0: retirar el LED amarillo y el verde) · `P07b_zumbador_notas` (zumbador pasivo con 220 Ω en serie y `tone`) · `P08a_pir_monitor` (ver al sensor en el Monitor Serie: calentamiento, retardo, bloqueo) · `P08_alarma_pir` (botón que arma, PIR que detecta, sirena).
- **Teoría:** el sonido es vibración y la frecuencia decide la nota; el PIR se lee como un botón, pero según el fabricante necesita casi un minuto para inicializarse (con falsas detecciones mientras tanto). **PIR** significa *Passive InfraRed* (infrarrojo pasivo): detecta los cambios de calor infrarrojo que emite un cuerpo al moverse frente a él; es «pasivo» porque no emite nada, solo «escucha».
- **Retos:** `for` en los pitidos (`P07a_pitidos_con_for`); timbre de puerta y código secreto; sirena con `for` (`P07b_sirena_for`); «Cumpleaños feliz» (`P07b_cumpleanos`); tiempo de salida y desarme con 3 pulsaciones (`P08_alarma_completa`, que además hace que la sirena no bloquee el programa).
- **Rompe y arregla:** cable del zumbador en el pin 11 (no suena); `i <= 3` (cuatro pitidos, sin mensaje de error); errores del IDE dentro del `for` (`;` que falta, nombre mal escrito, llave que falta, con los mensajes comprobados compilando); P07a con el pasivo conectado (solo clics, seguro por la resistencia); cable OUT del PIR en el pin 6 (la alarma nunca suena); retardo del PIR al tope largo (la sirena se repite). **No se planta ningún fallo que deje el pasivo sin su resistencia.** Se cambió el fallo «el PIR no responde porque no se esperó el calentamiento»: depende del azar. El calentamiento se **observa y se mide** en P08a.
- **Evidencia:** captura del Monitor Serie con detecciones del PIR y el retardo medido; alarma que se arma, detecta y se desarma.
- **Cuidado:** sonidos cortos; el zumbador **pasivo** es el que cambia de tono con `tone`. **El pasivo (16 Ω según su hoja de datos) lleva una resistencia de 220 Ω en serie:** sin ella pediría unos 310 mA y un pin aguanta 40 mA. El activo (menos de 25 mA) va directo al pin. El PIR se alimenta con 5 V: se leen las letras de sus patas antes de conectarlo (VCC y GND al revés pueden dañarlo). P16 y P25 usan el mismo zumbador y su encabezado ya pide la resistencia.
- **Decisión de armado:** al empezar se retiran el LED amarillo y el verde (hace falta el espacio y las piezas se vuelven a usar). El zumbador va en las columnas 5 a 11, dentro de la primera mitad del protoboard: los rieles pueden venir divididos en el centro y así el GND siempre llega.
- **Guía de práctica con diagramas:** `curso-arduino/guias/S04-sonido-y-alarma.md` (zumbadores, frecuencia, `for`, módulo PIR, señal del PIR y estados de la alarma; protoboard y cableado de P07a, P07b y P08). Pendiente de comprobar con el kit: separación de las patas de los zumbadores, corriente y volumen del pasivo, orden de las patas del PIR y sentido de sus perillas (V8, V12 y V13).

### Sesión 5 · Perilla y brillo
- **Objetivo:** pasar de HIGH/LOW a una escala de valores.
- **Prácticas:** `P09_perilla_serie` (0–1023 y volts en el Monitor Serie) · `P10_perilla_brillo` (`map` y PWM).
- **Teoría:** señal analógica vs digital; divisor de voltaje; 1024 niveles; qué hace el PWM (el símbolo `~`). *Word, cap. 4 y 5.*
- **Retos:** brillo invertido; que el LED solo encienda pasada la mitad; otros rangos con `map`.
- **Rompe y arregla:** extremos del potenciómetro cambiados (gira al revés): se resuelve conectando distinto o con `map(…, 1023, 0, …)`; dos soluciones, dos aprendizajes.
- **Evidencia:** gráfica del **Serial Plotter** al girar la perilla.
- **Nota:** los potenciómetros del kit son de tipo trimmer (F8). Alcanza con un desarmador pequeño, pero conviene comprar perillas (sección 10).

### Sesión 6 · Luz y decisiones
- **Objetivo:** convertir una lectura en una decisión.
- **Prácticas:** `P11_ldr_serie` · `P12_lampara_automatica` (el umbral se ajusta con la perilla).
- **Teoría:** sensor resistivo; umbral; calibración; retroalimentación (el LED que ilumina su propio sensor). *Word, cap. 5, práctica 2 y proyecto 1.*
- **Retos:** encender a medio brillo (LED al pin 9); modo manual con botón; «botón de paro + LDR» (proyecto 3 del Word).
- **Rompe y arregla:** el LED apuntando al LDR: el sistema parpadea; se separa o se tapa el sensor.
- **Evidencia:** valores anotados con luz del salón, con la mano encima y con la linterna del celular.

### Sesión 7 · Servo
- **Objetivo:** controlar un ángulo y usar una librería.
- **Prácticas:** `P13_servo_barrido` · `P14_servo_perilla`.
- **Teoría:** servo (ángulo) vs motor de corriente continua (velocidad); `for`; alimentación (señal, 5 V, GND). *Word, cap. 9.*
- **Retos:** rango de 45° a 135°; bandera de papel que saluda.
- **Rompe y arregla:** señal en otro pin; GND sin conectar.
- **Evidencia:** servo siguiendo la perilla.
- **Cuidado:** si el Arduino se reinicia al moverse el servo, se alimenta desde el módulo de fuente.

### Sesión 8 · Distancia y barrera automática
- **Objetivo:** integrar un sensor y dos actuadores en un sistema.
- **Prácticas:** `P15_distancia` (en cm por el Monitor Serie) · `P16_barrera_automatica` (HC-SR04 + servo + zumbador + LED).
- **Teoría:** tiempo de vuelo del eco; distancia = tiempo × velocidad del sonido ÷ 2; funciones que devuelven un valor. *Word, cap. 9 («barrera automática»).*
- **Retos:** cambiar la distancia de activación; contador de vehículos; alarma si algo se queda más de 5 s.
- **Rompe y arregla:** TRIG y ECHO intercambiados: el sensor responde «sin eco».
- **Evidencia:** comparación con una regla en 10, 20 y 50 cm.

### Sesión 9 · Motor y transistor
- **ALTO: no armar todavía.** Miguel midió con una fuente de poder que el motor «3–6 V» **funciona a partir de 0.95 A** (por aclarar: a qué voltaje y si es corriente de arranque o con el aspa girando). Si ese es su consumo, el circuito de esta sesión queda **fuera de especificación**: el PN2222 soporta 600 mA, el módulo de fuente 700 mA y el adaptador de 9 V entrega 1 A en total. Opciones en la sección 11 (V1). Mientras tanto, el «actuador controlado con perilla» se hace con el servo (P13 y P14). Los sketches P17, P18 y P23 ya llevan un aviso en el encabezado.
- **Objetivo:** mover una carga de potencia desde un pin que no la aguanta, y controlar su velocidad (tu ejemplo 4).
- **Prácticas:** `P17_motor_boton` · `P18_motor_perilla`.
- **Teoría:** un pin entrega ~20 mA y el motor pide cientos; el transistor como interruptor (emisor, base, colector); diodo de protección; fuente externa y GND común. **El Word no cubre este tema: capítulo nuevo.**
- **Antes de energizar (el instructor revisa cada equipo):** pinout del PN2222 (1 emisor, 2 base, 3 colector), diodo con la raya hacia +5 V, GND común, módulo de fuente con el + en el riel rojo, jumper en 5 V.
- **Retos:** medir desde qué valor de PWM arranca el motor y ajustar `UMBRAL_ARRANQUE`; encendido con un toque (como la sesión 3); girar 3 s y detenerse.
- **Rompe y arregla:** el GND del Arduino sin unir al del módulo: el motor no gira (**fallo seguro**; no se plantan fallos con el diodo o la resistencia de base).
- **Evidencia:** motor con velocidad variable y el dato de arranque anotado.
- **Cuidado:** no trabar el aspa; el regulador del módulo se calienta si el motor se traba; el adaptador se revisa antes de enchufarse.
- **Ampliación:** el L293D de la lección 20 del kit (invertir el giro).

### Sesión 10 · Temperatura
- **Objetivo:** medir una magnitud con dos sensores distintos y compararlos.
- **Prácticas:** `P19_termistor_celsius` · `P20_dht11` (temperatura y humedad).
- **Teoría:** NTC: la resistencia baja al subir la temperatura y no es lineal (la ecuación se usa como caja negra); sensor analógico vs sensor digital; precisión y resolución; calibrar contra un termómetro. *Word, cap. 10 (se cambia el TMP36 por el termistor).*
- **Retos:** LED que enciende a 30 °C; tabla de temperatura cada minuto durante la clase; diferencia entre los dos sensores.
- **Rompe y arregla:** termistor sin resistencia fija: el programa avisa «revisa la conexión».
- **Evidencia:** temperaturas anotadas y `AJUSTE_C` calculado.

### Sesión 11 · Pantalla LCD
- **Objetivo:** mostrar datos al usuario sin computadora.
- **Prácticas:** `P21_lcd_hola` · `P22_estacion_clima` (DHT11 + LCD).
- **Teoría:** librerías; modo de 4 bits; contraste; la pantalla no muestra acentos. *Word, cap. 10.*
- **Retos:** nombre del equipo en pantalla; alternar mensajes; LED si la humedad pasa de 70 %.
- **Rompe y arregla:** contraste en cero (pantalla «vacía»), el fallo más común.
- **Evidencia:** estación de clima funcionando.
- **Cuidado:** son unos 12 cables; usar colores y que el instructor revise antes de energizar.

### Sesión 12 · Ventilador automático *(integración)*
- **Objetivo:** construir un sistema completo: medir, comparar, actuar. **Reemplaza al «Proyecto 7: Ventilador» del PowerPoint.**
- **Práctica:** `P23_ventilador_automatico` (termistor + perilla de límite + LCD + motor con transistor). **Depende de la sesión 9:** hasta resolver el motor, el «ventilador» puede ser un LED; la lógica (histéresis) es la misma.
- **Teoría:** lazo de control; histéresis (por qué no se apaga exactamente donde se enciende); variable de estado. *Word, cap. 6 y 10.*
- **Prueba:** límite 1–2 °C sobre la temperatura ambiente, calentar el termistor con los dedos, soltar y esperar.
- **Retos:** probar la lógica con un LED en lugar del motor; velocidad proporcional a la temperatura; aviso con zumbador sobre 35 °C.
- **Rompe y arregla:** límite igual a la temperatura ambiente: sin histéresis el ventilador «tiembla».
- **Evidencia:** video corto del ciclo encendido/apagado con la pantalla visible.

### Sesión 13 · Campo y agua
- **Objetivo:** calibrar un sensor con datos reales y convertirlo en un aviso útil.
- **Prácticas:** `P24_humedad_suelo` (semáforo de humedad) · `P25_nivel_agua` (modelo de tinaco).
- **Actividad:** «medimos nuestra tierra»: cada equipo trae tierra de macetas o del patio y anota lecturas en seco, húmeda y en agua.
- **Teoría:** una medición solo significa algo después de calibrarla; porcentaje con `map` y `constrain`; las sondas se corroen.
- **Retos:** bomba simulada con motor (P17 + P25 con histéresis); registro de lecturas a lo largo de un día.
- **Rompe y arregla:** sensor sin calibrar: los colores no corresponden a la realidad.
- **Evidencia:** tabla de calibración y umbrales elegidos.
- **Cuidado:** solo se moja la parte con pistas; la placa del sensor, los cables y el Arduino se mantienen secos; solo 5 V.

### Sesiones 14 a 16 · Proyecto final
- **Sesión 14, diseño y armado:** el equipo elige un reto, llena la hoja de diseño (¿qué problema resuelve?, ¿qué entradas, qué proceso, qué salidas?, lista de componentes, dibujo de conexiones) y arma la primera versión.
- **Sesión 15, pruebas y mejora:** el equipo define 3 pruebas con criterio (por ejemplo, «el ventilador enciende a 28 ±1 °C»), corrige y documenta.
- **Sesión 16, exhibición:** 5 minutos por equipo: problema, solución, demostración y qué aprendieron.
- **Retos propuestos** (todos usan lo visto; son **ideas por validar con los docentes de la prepa** sobre qué problemas locales conviene tomar):
  1. **Aviso de riego** para una maceta: humedad de suelo + semáforo de LED + zumbador + LCD.
  2. **Tinaco con alarma y bomba simulada:** nivel de agua + motor con transistor + histéresis.
  3. **Alarma de casa:** PIR + botón + sirena + LCD con el estado.
  4. **Termostato de invernadero o gallinero en maqueta:** DHT11 + motor + LCD.
  5. **Barrera de estacionamiento con contador:** HC-SR04 + servo + LCD.
  6. **Semáforo peatonal:** `X02` mejorado con sensor de luz que regule el brillo.
  7. **Reto libre**, con aprobación del instructor.
- **Componentes de ampliación** para equipos adelantados (código en `kit-arduino/Code/`): alarma de gas MQ-2 (lección 30; **solo con el instructor**, el sensor se calienta), sensor de sonido (27), lector RFID (29), reloj RTC (26), matriz LED (22), joystick (12), control remoto IR (15, con el IRremote del zip del kit), motor a pasos (16 y 28).

## 6. Cómo se organiza una sesión de 2 horas

En un día de 4 horas con dos sesiones, la apertura y el cierre se comparten (sección 3b).

| Minutos | Actividad | Detalle |
|---|---|---|
| 0–10 | Apertura | Revisar el kit con la hoja de inventario; una pregunta que retome la sesión anterior; abrir la bitácora |
| 10–25 | Idea del día | Demostración con el kit del instructor y dibujo en el pizarrón; sin leer láminas |
| 25–75 | Práctica 1 | Armar, subir, observar. El instructor circula |
| 75–105 | Práctica 2 y retos | Modificar el código (básico, medio, desafío) y resolver el fallo planeado |
| 105–120 | Cierre | Bitácora («qué cambié, qué pasó, por qué»), visto bueno del instructor, desarmar y guardar el kit completo |

## 7. Organización con 6 kits

- **Una computadora por kit.** Los sketches de `curso-arduino/sketches/` se copian de antemano a cada computadora; los alumnos los abren, no los teclean (así el tiempo se va en entender, no en errores de escritura).
- **Roles que rotan cada sesión** (con 3 alumnos): armador, programador y verificador/bitácora. Con 2, armador y programador se alternan en cada práctica.
- **Pedir ayuda sin interrumpir:** un vaso o tarjeta por equipo (verde = «vamos bien», rojo = «necesitamos ayuda»).
- **Kit ordenado:** cada kit lleva su número y una hoja de inventario. Se cuenta al empezar y al terminar la sesión; las piezas pequeñas (LED, resistencias) se guardan por tipo.
- **Revisión previa a energizar** en las sesiones 9, 11 y 12 (motor, fuente de 9 V y cableado de la pantalla): el instructor mira cada circuito antes de que se conecte el adaptador.

## 8. Evaluación

- **Durante el curso:** bitácora por sesión con visto bueno del instructor en tres puntos: **funciona**, **lo puede explicar con sus palabras** y **hizo al menos una modificación propia**.
- **Final:** el proyecto, con 4 criterios: funciona, está bien armado y ordenado, lo explican con claridad (incluyendo qué cambiaron y por qué) y trabajaron en equipo.
- **Quién decide si hay constancia o calificación, y con qué requisitos,** no está definido aquí; depende de la escuela y del IPPI.

## 9. Convención de pines

Todo el curso usa los mismos pines para lo mismo, para que el equipo no tenga que reaprender el cableado. Las lecciones del kit usan otros pines; los diagramas del PDF del fabricante **no coinciden** con estos.

| Elemento | Pin |
|---|---|
| LED rojo / amarillo / verde | 8 / 9 / 10 (LED azul de peatón: 11) |
| Botones | 2 (y 3 si hay un segundo) con `INPUT_PULLUP`, el otro extremo a GND |
| Zumbador | 12 |
| Sensor PIR | 7 |
| Perilla o sensor analógico | A0 (segundo analógico: A1) |
| Servo | 9 |
| HC-SR04 | TRIG 6 · ECHO 7 |
| Motor (base del PN2222 con 330 Ω) | 5 |
| DHT11 | A0 |
| LCD1602 | RS 7 · E 8 · D4 9 · D5 10 · D6 11 · D7 12 |

## 10. Material por sesión y compras sugeridas

Todo sale del kit. Los componentes se cuentan al iniciar cada sesión.

| Sesión | Del kit |
|---|---|
| 1 | Placa y cable USB, protoboard, 1 LED, 1 resistencia 220 Ω, jumpers |
| 2 | 3 LED (rojo, amarillo, verde), 3 resistencias 220 Ω |
| 3 | LED, 220 Ω, botón |
| 4 | Zumbador activo y pasivo, PIR (3 cables M-F), botón, LED, 2 resistencias de 220 Ω (LED y zumbador pasivo) |
| 5 | Potenciómetro, LED, 220 Ω |
| 6 | LDR, resistencia 10 kΩ, potenciómetro, LED, 220 Ω |
| 7 | Servo SG90, potenciómetro |
| 8 | HC-SR04 (4 cables M-F), servo, zumbador pasivo, LED, 2 resistencias de 220 Ω (LED y zumbador) |
| 9 | Motor con aspa, PN2222, 1N4007, resistencia 330 Ω, módulo de fuente y adaptador de 9 V, botón, potenciómetro |
| 10 | Termistor NTC, resistencia 10 kΩ, DHT11 (3 cables M-F) |
| 11 | LCD1602, potenciómetro (contraste), DHT11 |
| 12 | LCD1602, termistor, 10 kΩ, **2 potenciómetros (contraste y límite)**, motor, PN2222, 1N4007, 330 Ω, módulo de fuente |
| 13 | Sensor de humedad de suelo, sensor de nivel de agua (cables M-F), 3 LED, 4 resistencias 220 Ω (3 LED y el zumbador pasivo), zumbador pasivo; **vasos con agua, tierra y una maceta** (no vienen en el kit) |

**Compras que valen la pena (opcionales):**
1. **Potenciómetros de 10 kΩ con perilla** (unos 12; dos por kit). Los del kit son trimmer (F8) y, además, la sesión 12 usa los dos del kit a la vez.
2. **Un multímetro** para el instructor: medir la corriente real del motor (F10) y comprobar transistores antes del curso.
3. **Respaldo:** una placa Arduino UNO y un cable USB de repuesto, porque el equipo reconecta mucho.
4. **Solo si se confirma que el motor consume cerca de 1 A (V1):** motores pequeños para los 6 kits (por ejemplo de 130 con hélice, de menos consumo) o un transistor de potencia o MOSFET de nivel lógico con una fuente de más capacidad. No se compra nada hasta medir.

## 11. Tus prácticas previas (en el orden del curso)

La mejor preparación es vivir el curso como alumno: hacer P01 a P25 **en este orden**, con el kit, anotando tiempo y dudas. Calcula unas 8 a 10 horas en total. Para cada práctica, abre el sketch desde `curso-arduino/sketches/`, conecta según el encabezado del archivo y sube con el IDE (placa «Arduino Uno»).

**Lo que solo se puede confirmar con el kit en la mano** (anótalo; ajusta los sketches si no coincide):

| # | Prueba | Práctica | Qué anotar |
|---|---|---|---|
| V1 | **Corriente real del motor.** Tres datos no coinciden: lección 20 (0.35–0.4 A), datasheet del kit (hasta 0.25 A con carga y 0.5 A bloqueado) y la medición de Miguel (**funciona a partir de 0.95 A**) | P17 | Con la fuente a **5 V** (el voltaje del curso): corriente al arrancar y con el aspa girando libre; y si los 0.95 A fueron el consumo o el límite de corriente que configuraste |
| V2 | Orden de patas del PN2222 del kit (emisor-base-colector, según el datasheet) | P17 | Confirmar con el multímetro en prueba de diodo, si hay |
| V3 | Valor de PWM desde el que arranca el motor | P18 | Número para `UMBRAL_ARRANQUE` (puse 60 como punto de partida, sin medir) |
| V4 | Lecturas del DHT11 (adaptado del código del kit; compila, no se ha probado) | P20, P22 | Si lee y si coincide con el termistor |
| V5 | Precisión del termistor frente a un termómetro | P19 | Diferencia, para `AJUSTE_C` |
| V6 | Rango del LDR con 10 kΩ en el salón | P11 | Valores con luz, sombra y oscuridad |
| V7 | Valores de los sensores de suelo y de agua | P24, P25 | Lecturas para `VALOR_SECO`, `VALOR_MOJADO`, `NIVEL_BAJO`, `NIVEL_ALTO` (los de los sketches son supuestos) |
| V8 | Tiempo de calentamiento, retardo, bloqueo y sensibilidad del PIR; orden de sus patas y sentido de sus perillas | P08a, P08 | Segundos reales hasta que se estabiliza; retardo en los dos topes y sentido de giro; segundos de bloqueo; metros de alcance; letras de las patas; posición del puente |
| V9 | Servo desde el 5 V del Arduino por USB | P13, P16 | Si se reinicia o tiembla |
| V10 | Luz de fondo y contraste del LCD | P21 | Si hay que cambiar algo respecto al diagrama de la lección 19 |
| V11 | Tiempo real de cada práctica | todas | Para ajustar qué cabe en 2 horas |
| V12 | Zumbador pasivo con 220 Ω en serie: volumen y corriente real con `tone()` (con multímetro en serie, si hay) | P07b, P08 | Si se oye bien en un salón; mA medidos. Si se oye muy bajito, valorar otra resistencia **solo con la corriente medida** (100 Ω daría hasta unos 43 mA como peor caso sin contar el pin: demasiado cerca de los 40 mA) |
| V13 | Zumbadores del kit: cuál es el activo y cuál el pasivo, separación de sus patas, si entran en el protoboard y si la etiqueta del activo cambia el volumen | P07a, P07b | Agujeros entre patas; qué se oye con y sin etiqueta |

**Si el motor consume cerca de 1 A de forma sostenida** (a 5 V), el circuito con PN2222 y módulo de fuente no sirve: el PN2222 aguanta 600 mA, el módulo 700 mA y el regulador del módulo (de 9 V a 5 V) se sobrecalentaría. Opciones, de más simple a menos:

1. **Cambiar el motor** por uno de menor consumo para los 6 kits y conservar el circuito (cuesta poco y mantiene el kit sin cambios).
2. **Bajar el voltaje del motor** (es de 3–6 V): si a ~3 V consume bastante menos, se alimenta desde el riel de 3.3 V del módulo. Hay que medirlo.
3. **Relé** del kit (soporta 10 A) solo para encender y apagar. No sirve para variar la velocidad; la perilla controlaría un servo.
4. **Transistor de potencia o MOSFET de nivel lógico** con una fuente de más capacidad (compra, y cambia el diagrama).

Mientras no se resuelva: el actuador controlado con perilla es el **servo**, y el «ventilador automático» usa un LED para probar la lógica.

## 12. Qué cambia respecto al material actual

**Del PowerPoint (8 proyectos en Tinkercad):**

| Proyecto actual | Dónde queda |
|---|---|
| P1 Conectando LED | Sesiones 1 y 2 |
| P2 LED con pulsador | Sesión 3 |
| P3 Sensor de distancia + buzzer | Sesión 8 |
| P4 Servomotor | Sesión 7 |
| P5 Semáforo | Sesión 2 (con ampliación peatonal `X02`) |
| P6 Dado digital | Ampliación `X01` (dado con 6 LED; se resuelve la inconsistencia entre el display de la portada y los 7 LED del material, H7) |
| P7 Ventilador | **Se rehace** en las sesiones 9 y 12 (motor + transistor; termistor en lugar de TMP36) |
| P8 Potenciómetro | Sesión 5 |

**Se retira:** TMP36, ventilador de PC, Tinkercad como plataforma obligatoria (puede quedar como práctica extra en casa), las capturas de código en español (H2) y las 16 láminas repetidas de «Paso 1 y 2» (H5).
**Se agrega:** sensor de luz con decisiones, PIR, transistor y motor, termistor, DHT11, LCD, humedad de suelo, nivel de agua, integración y proyecto final.

**Del Word:** los capítulos 1 a 6 sirven como lectura de apoyo de las sesiones 1 a 6; el capítulo 7 (prácticas) corresponde a las sesiones 3, 5 y 6; el capítulo 8 (proyectos): alumbrado nocturno → sesión 6, indicador tricolor → sesión 13, botón de paro + LDR → reto de la sesión 6; el capítulo 9 → sesiones 7 y 8; el capítulo 10 → sesiones 10 a 12, cambiando TMP36 por el termistor. **Capítulos nuevos a escribir:** transistor y motor (sesión 9), sensores de campo y calibración (sesión 13), guía del proyecto final.

## 13. Decisiones pendientes (de ti)

1. ~~Sesiones y duración~~ → se conserva el curso completo de **16 sesiones (32 h)**; la primera visita son **dos días de 4 horas** y el resto se imparte en otras fechas (16 nov). **Falta:** cuántas visitas, qué fechas y cuánto dura cada una, y **dónde se guardan kits y computadoras entre visitas**.
2. ~~Computadoras~~ → **sí, 6** (16 nov).
3. **El motor** (V1): ¿a qué voltaje lo probaste, y los 0.95 A fueron el consumo o el límite de corriente de tu fuente? ¿Cuánto consume con el aspa girando libre a 5 V?
4. **¿Quién imparte?** ¿Habrá un apoyo para circular entre 6 equipos?
5. **Perfil de los alumnos:** grado, edad y si alguien ya programó. Si hay quien ya sabe, se les asignan retos «desafío» y el rol de apoyo.
6. ~~Retos del proyecto final~~ → **aprobados** (16 nov). Se recomienda confirmar con los docentes de la prepa cuáles se usan.
7. **Compras:** perillas, multímetro y respaldo (sección 10); lo del motor según V1.
8. **Constancia o calificación:** si habrá y con qué requisitos (sección 8).

## 14. Siguientes pasos

1. **Sesión por sesión (acordado el 16 nov):** para cada sesión se entrega una guía de práctica con **diagramas de cada ejercicio** (`curso-arduino/guias/`). Tú la haces con el kit y me dices qué ajustar antes de pasar a la siguiente. La Sesión 1 ya está (`S01-hola-arduino.md`). Toma **una foto del circuito armado con tu kit** en cada práctica (vista desde arriba): servirán para las láminas y evitan depender de los diagramas del fabricante (H12).
2. **Yo, con la secuencia aprobada:** construir la presentación en la plantilla `ippi-cursos` (barra lateral «CURSOS / IPPI»): portada, un divisor por etapa y, por práctica, objetivo y materiales, tabla de conexiones, código en texto, resultado esperado y retos. Calculo unas 130 a 160 láminas.
3. **Después:** adaptar el Word (sección 12), preparar la bitácora y la hoja de diseño del proyecto para imprimir, y la hoja de inventario del kit.
4. **Antes de ir a Atzingo:** prueba piloto con 1 o 2 estudiantes para medir los tiempos reales (V11).
