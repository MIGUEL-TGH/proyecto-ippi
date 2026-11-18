# Progreso de Miguel con el curso de Arduino

**Para qué sirve:** llevar el registro de qué guías ya están generadas y hasta dónde ha llegado Miguel con su práctica. Miguel avisa cómo avanza («ya hice la Sesión 5», «en P10 pasó tal cosa») y se actualiza este archivo; los hallazgos se aplican después a las guías, los sketches y los diagramas.
**Última actualización:** 2026-11-17 (archivo creado; **guías de las sesiones 5 a 16 listas**, plan y conteos al día; falta que Miguel practique las sesiones 5 a 16 y avise lo que encuentre). **Revisión del 17 nov:** tablas de pines por reto con pantalla en `S14-16-proyecto-final.md`, `compilar-sketches.ps1` arreglado y guía `preparacion-computadoras.md`

## Cómo avisar

- **«Ya hice la Sesión N»** sin más: se anota como hecha, sin hallazgos.
- **«En la Sesión N pasó esto…»**: se anota en la tabla de hallazgos y se corrige la guía, el sketch o el diagrama que corresponda.
- Cada guía termina con una tabla **«Tu práctica: anota lo que encuentres»**: se puede pegar llena aquí.

## Estado por sesión

| Sesión | Prácticas | Guía generada | Práctica de Miguel | Hallazgos por aplicar |
|---|---|---|---|---|
| 1 · Hola, Arduino | P01, P02 | 16 nov | Hecha (16 nov) | Ninguno pendiente (el error `redefinition of 'int pinLed'` ya se corrigió) |
| 2 · Luces con tiempos | P03, P04 | 16 nov | Hecha (16 nov) | Ninguno |
| 3 · Botones | P05, P06 | 16 nov | Hecha (reportada el 17 nov, sin comentarios) | Sin comprobar: qué patas del botón van unidas por dentro (medir continuidad); `INPUT` sin pull-up |
| 4 · Sonido y alarma | P07a, P07b, P08a, P08 | 16 nov | Hecha (reportada el 17 nov, sin comentarios) | **Sin datos:** V8 (PIR), V12 (corriente del zumbador pasivo con 220 Ω), V13 (separación de patas de los zumbadores) |
| 5 · Perilla y brillo | Paso 0, P09, P09a, P10a, P10 | 17 nov | **Pendiente** | V14 (potenciómetro, PWM a mano, `analogWrite` en un pin sin `~`) |
| 6 · Luz y decisiones | P11, P12 | 17 nov | Pendiente | V6 (rango del LDR en el salón) |
| 7 · Servo | P13, P14 | 17 nov | Pendiente | V9 (el servo con el 5 V del USB) |
| 8 · Distancia y barrera | P15, P16 | 17 nov | Pendiente | Orden real de las letras del HC-SR04; error frente a la regla |
| 9 · Transistor (y motor) | P17, P18 | 17 nov (versión con LED) | Pendiente | V2 (patas del PN2222); el motor sigue **bloqueado** (V1, V3) |
| 10 · Temperatura | P19, P20 | 17 nov | Pendiente | V4 (DHT11) y V5 (termistor frente a un termómetro) |
| 11 · Pantalla LCD | P21, P22 | 17 nov | Pendiente | V10 (contraste y luz de fondo con 100 Ω) |
| 12 · Ventilador automático | P23 | 17 nov (versión con LED) | Pendiente | Rieles divididos del protoboard; histéresis frente al ruido real; el motor depende de V1 |
| 13 · Campo y agua | P24, P25 | 17 nov | Pendiente | V7 (lecturas reales de suelo y agua; si la sonda es de pistas al descubierto; lectura máxima del sensor de nivel: 860 o 1023); orden real de las patas de los módulos (AO·DO·GND·VCC y S·+·−, tomado de las fotos del kit); resistencia de 220 Ω en 2 agujeros |
| 14 a 16 · Proyecto final | reto elegido (plantilla `Proyecto_plantilla`) | 17 nov | Pendiente | Tiempos de armado con pantalla; que el PIR, el HC-SR04, el servo y el DHT11 funcionen en los pines nuevos de «Pines por reto» (las combinaciones de los retos 1 a 6 ya compilan sin choques de pines ni de nombres); si los 7 retos interesan a los docentes de la prepa |

## Plan de generación (una sesión a la vez)

Para cada sesión se hace, en este orden: (1) revisar sus sketches y las hojas de datos del kit; (2) ajustar o crear sketches y compilarlos; (3) dibujar los diagramas (protoboard y cableado de cada circuito más las ayudas de ideas) y revisarlos uno por uno; (4) escribir la guía en `curso-arduino/guias/`; (5) marcar aquí.

- [x] S5 · `S05-perilla-y-brillo.md` (17 nov)
- [x] S6 · `S06-luz-y-decisiones.md` (17 nov)
- [x] S7 · `S07-servo.md` (17 nov)
- [x] S8 · `S08-distancia-y-barrera.md` (17 nov)
- [x] S9 · `S09-transistor-y-motor.md` (17 nov; con LED, el motor sigue bloqueado)
- [x] S10 · `S10-temperatura.md` (17 nov)
- [x] S11 · `S11-pantalla-lcd.md` (17 nov; pines del LCD reordenados: RS 12, E 11, D4 a D7 en 10, 9, 8, 7)
- [x] S12 · `S12-ventilador-automatico.md` (17 nov; con LED, el motor sigue bloqueado)
- [x] S13 · `S13-campo-y-agua.md` (17 nov; los sensores se conectan directo a la placa, como en las lecciones 25 y 31 del kit; semáforo de la Sesión 2 como Paso 0)
- [x] S14 a S16 · `S14-16-proyecto-final.md` (17 nov; hojas A a D imprimibles, banco de 7 retos con mapa de reutilización y mapa de pines; sketch `Proyecto_plantilla`)
- [x] Al final: plan, memoria y conteos de sketches al día (17 nov; **66 sketches**, 0 errores y 0 avisos con `compilar-sketches.ps1`; el plan, `hallazgos-ajuste-curso.md` y `revision-kit-arduino.md` ya tienen los conteos nuevos)

## Validaciones con el kit en la mano (V1 a V16)

El detalle de cada una está en `plan-curso-arduino.md`, sección 11. Aquí solo el estado.

| # | Qué se comprueba | Estado |
|---|---|---|
| V1 | Corriente real del motor (0,95 A según tu medición; a qué voltaje y si es arranque o giro libre) | Sin resolver: bloquea P17, P18 y P23 con motor |
| V2 | Orden de patas del PN2222 | Sin comprobar |
| V3 | PWM desde el que arranca el motor | Sin comprobar (motor bloqueado) |
| V4 | Lecturas del DHT11 | Sin comprobar |
| V5 | Precisión del termistor frente a un termómetro | Sin comprobar |
| V6 | Rango del LDR con 10 kΩ en el salón | Sin comprobar |
| V7 | Valores de los sensores de suelo y de agua | Sin comprobar |
| V8 | PIR: calentamiento, retardo, bloqueo, sensibilidad, orden de patas | Sin datos (S4 hecha sin hallazgos) |
| V9 | Servo alimentado desde el 5 V del Arduino por USB | Sin comprobar |
| V10 | Luz de fondo y contraste del LCD | Sin comprobar |
| V11 | Tiempo real de cada práctica | En curso: sin datos de tiempos todavía |
| V12 | Zumbador pasivo con 220 Ω: volumen y corriente | Sin datos |
| V13 | Zumbadores: cuál es cuál, separación de patas | Sin datos |
| V14 | Potenciómetro, PWM a mano y `analogWrite` en un pin sin `~` | Sin comprobar (S5 pendiente) |
| V15 | Resistencias que abarcan solo 2 agujeros del protoboard (¿caben «paradas»?): P11, P12, P16, P17, P19, P20, P25 | Sin comprobar |
| V16 | Rieles del protoboard divididos a la mitad (la Sesión 12 usa 46 columnas y trae puentes opcionales) | Sin comprobar |

## Decisiones pendientes de Miguel

- Compras opcionales: potenciómetros con perilla (unos 12), multímetro, placa Arduino y cable de repuesto, **desarmador plano pequeño** para los potenciómetros del kit, un termómetro de referencia para calibrar el termistor.
- Quién imparte, fechas y número de visitas, dónde se guardan kits y computadoras entre visitas.
- Si habrá constancia o calificación y con qué requisitos.
- Condiciones de la prueba del motor (voltaje y tipo de corriente) para decidir si se destraban P17, P18 y P23 con motor.
- Revisar si el repositorio de GitHub es público: `kit-arduino/` (PDF, hojas de datos y bibliotecas del fabricante; hallazgo H12) **ya está versionado y subido** (commit `ead1531`, 16 nov).
- Versión de Windows, permisos para instalar e internet de las 6 computadoras de la escuela; y practicar `preparacion-computadoras.md` (incluye instalar las 7 bibliotecas del kit, que no están en esta PC).

## Registro de hallazgos de la práctica

(Aquí se anotan, con fecha, los hallazgos que Miguel reporte: qué pasó, en qué sesión y práctica, y qué se cambió.)

| Fecha | Sesión y práctica | Qué pasó | Qué se cambió |
|---|---|---|---|
| 2026-11-16 | S1 · P02 | Error del IDE `redefinition of 'int pinLed'` por tener dos `.ino` en la misma carpeta | Regla de un solo `.ino` por carpeta y «Guardar como…» en las guías |
| 2026-11-17 | S14 a S16 · retos con pantalla | Revisión: la guía decía que en el reto 5 solo había que mover el ECHO, pero con la pantalla chocan **cuatro** pines (ECHO, servo, zumbador y LED); lo mismo, en menor grado, en los retos 1 a 3 | Sección «Pines por reto» con la tabla de cada reto, notas corregidas, Hoja A con pines 7 a 12 marcados y regla 9 (escribir en la pantalla solo al cambiar). Comprobado compilando la versión completa de los retos 1 a 6 |
| 2026-11-17 | Herramienta · `compilar-sketches.ps1` | El script se detenía en el primer sketch con un `NativeCommandError` cuando el caché de compilación del núcleo estaba vacío (Windows PowerShell 5.1 convierte en error lo que `arduino-cli` escribe por stderr) | Corregido, y se agregó `-Filtro` para compilar solo algunos sketches. Probado con caché vacío y con la corrida completa (66/66) |
