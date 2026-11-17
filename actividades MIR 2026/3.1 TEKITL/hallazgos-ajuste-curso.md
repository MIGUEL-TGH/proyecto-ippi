# Hallazgos y soluciones: Curso de Electrónica y Programación Básica

**Destino:** alumnos de preparatoria, San Juan Atzingo, San Gabriel Chilac, Puebla
**Fecha del análisis:** 2026-11-15 · **Actualizado:** 2026-11-16 (decisiones de Miguel y plan de curso) · **Estado:** borrador de trabajo (para resolver punto por punto)

## 1. Qué se analizó

| Archivo | Qué es |
|---|---|
| `Proyectos Electronica Basica.pptm` | 65 láminas, 8 proyectos con Tinkercad. Sin macros, se puede guardar como .pptx. En este documento, «lámina N» se refiere a este archivo. |
| `Curso de Electronica y Programacion Basica.docx` | Manual teórico de 10 capítulos (19.9 MB, 52 imágenes): fundamentos, 3 prácticas, 3 proyectos, sensores avanzados, LCD. |
| `2026-11-18 - ippi-cursos.pptx` | **Plantilla a usar.** Su contenido (Mesa Técnica SECIHTI) se descarta; se conserva solo el diseño. |
| `kit-arduino/` | Material del fabricante del kit comprado (ver `revision-kit-arduino.md`). |

**Decisión tomada:** la plantilla correcta es `2026-11-18 - ippi-cursos.pptx`, aunque su contenido no sirva para el curso.

### Decisiones del 16 de noviembre de 2026

| Tema | Decisión |
|---|---|
| Materiales que se omiten | **Sensor TMP36 y ventilador de PC.** El ventilador es el motor 3–6 V con aspa del kit; la temperatura se mide con el termistor NTC y el DHT11. |
| Sensores del kit sin uso | **Sí se incorporan** (humedad de suelo, nivel de agua, DHT11, PIR, etc.) para mejorar la experiencia de los alumnos. |
| Secuencia del curso | Se rehace de lo simple a lo complejo: ver **`plan-curso-arduino.md`**. |
| Barra lateral de la plantilla | **«CURSOS / IPPI»** confirmado. |
| Migración del contenido | Sí. Se hace **sobre la secuencia nueva** del plan, no lámina por lámina del .pptm viejo (el orden y buena parte del contenido cambian). |
| Equipo | **6 kits; cada kit lo usan 2–3 alumnos** (12 a 18 alumnos por curso). **6 computadoras confirmadas** (una por kit). Internet sin confirmar, pero el plan no lo necesita. |
| Duración | **Se conserva el curso completo de 16 sesiones (32 h).** La primera visita son dos días de 4 horas (sesiones 1 a 4); el resto se imparte en otras fechas. Ver `plan-curso-arduino.md`, sección 3b. |
| Retos del proyecto final | Aprobados por Miguel (16 nov). |
| Software | Arduino IDE 2.x **ya instalado** en la PC de Miguel. Trae su propio `arduino-cli`, que se usa para compilar; no se instaló nada más. |

## 2. Resumen

| # | Hallazgo | Gravedad | Solución propuesta | Estado |
|---|---|---|---|---|
| H1 | Word, PowerPoint y kit no coinciden en materiales | Alta | Rehacer ambos a partir del inventario real del kit. **Se omiten TMP36 y ventilador de PC** (decisión 16 nov). | ◐ decidido; falta rehacer Word y PPT |
| H2 | El código de las láminas son capturas de Tinkercad en español: no compila en Arduino IDE | Alta | Reemplazar por texto en C++ verificado, tomado de los `.ino` del kit | ◐ 38 sketches nuevos compilados (28 de la secuencia y 10 soluciones de retos) en `curso-arduino/sketches/` (falta probarlos en placa) |
| H3 | Proyecto 7 (ventilador) es inconsistente: dice transistor, el circuito lleva un TMP36 y el código tiene errores | Alta | Rediseñar con PN2222 + 1N4007 + motor 3–6 V (todo en el kit) | ◐ rediseñado en sesiones 9 y 12 del plan (sketches P17, P18, P23) pero **bloqueado**: el motor funciona a partir de 0.95 A (medición de Miguel, 16 nov), más de lo que aguanta el PN2222. Ver `plan-curso-arduino.md`, sección 11, V1 |
| H4 | Capturas recortadas conservan la pantalla completa (correo, WhatsApp, marcadores) | Media | Regenerar capturas limpias antes de compartir | ☐ |
| H5 | 16 láminas son los Pasos 1 y 2 idénticos en los 8 proyectos | Media | Consolidar en una sola sección «Preparación» | ☐ |
| H6 | Hay pasos con solo imagen y sin instrucción, y láminas sin título | Media | Añadir instrucción, tabla de conexiones y resultado esperado | ☐ |
| H7 | Las 8 portadas son imágenes aplanadas; la del Dado no coincide con el material | Media | Recrear con la plantilla; decidir el diseño del dado | ☐ |
| H8 | Formato inconsistente (listas de materiales en letra diminuta, tamaños distintos) | Baja | Se corrige al pasar a la plantilla | ☐ |
| H9 | El curso depende de Tinkercad (en línea) y de computadoras | Alta | Confirmar acceso a computadora e internet en Atzingo; plan sin conexión | ✔ hay 6 computadoras (una por kit) y el plan nuevo no usa Tinkercad, internet ni librerías externas |
| H10 | Falta pasar el curso a la plantilla `ippi-cursos` | Tarea 1 | Ver sección 4 | ◐ etiqueta «CURSOS / IPPI» confirmada; se construye cuando se apruebe la secuencia del plan |
| H11 | El Word usa TMP36 y una tabla de materiales que no es la del kit | Media | Adaptar capítulos 8–10 al termistor NTC y a la lista real | ☐ |
| H12 | Derechos de las imágenes y diagramas del fabricante | Baja | Citar fuente o redibujar | ☐ |

## 3. Detalle de cada hallazgo

### H1. Los tres materiales no coinciden

Cruce de componentes entre lo que pide cada material y lo que trae el kit (REXQualis UNO R3 Complete Starter Kit):

| Componente | PowerPoint | Word | ¿Está en el kit? |
|---|---|---|---|
| LED, resistencias, pulsador, jumpers, protoboard | Sí | Sí | **Sí** (25 LED, 120 resistencias, 5 botones, 65 + 20 cables) |
| Fotorresistor (LDR) | No | Sí | **Sí** (2) |
| Potenciómetro | Sí (P8) | Sí | **Sí** (2, tipo trimmer de 10 kΩ) |
| Buzzer | Sí (P3) | Sí | **Sí** (activo y pasivo) |
| HC-SR04 | Sí (P3) | Sí | **Sí** |
| Servo SG90 | Sí (P4) | Sí | **Sí** |
| LCD 16x2 | No | Sí | **Sí** (sin módulo I2C: más cables) |
| **TMP36** | Sí (P7, sin decirlo) | Sí | **No.** El kit trae termistor NTC y DHT11 |
| Transistor | Lo menciona (P7) | No | **Sí** (PN2222 ×5, con diodo 1N4007 ×5) |
| Ventilador DC (tipo PC) | Portada de P7 | No | **No.** Trae motor 3–6 V con aspa |
| 7 LED sueltos (P6) | Sí | No | **Sí** (hay 25) |

**Solución:** usar el inventario del kit como lista maestra. Cada proyecto del curso debe corresponder a una lección del kit o a una adaptación documentada. La correspondencia propuesta está en `revision-kit-arduino.md`, sección 5.

### H2. Código en capturas de Tinkercad en español

Lo que se ve en las láminas 22, 29, 38, 47, 48, 56 y 64 es la vista en español de Tinkercad: `SALIDA`, `ENTRADA`, `ALTO`, `BAJO`, `retardoMicrosegundos`, `retraso`, `si / demás`, `largo`, `flotante`, `lecturaAnáloga`. **Nada de eso compila en Arduino IDE**, que espera `OUTPUT`, `INPUT`, `HIGH`, `LOW`, `delay`, `if / else`, `long`, `float`, `analogRead`. Solo la lámina 14 está en código válido.

Además, el código está en imagen: los alumnos no pueden copiarlo, y el del Dado (115 líneas) ocupa dos láminas ilegibles.

**Solución:**
- Poner el código como **texto monoespaciado** en la lámina, no como captura.
- Tomarlo de los `.ino` del kit (están en inglés y probados por el fabricante) o de sketches propios.
- **Compilar cada sketch antes de publicarlo.** Esta PC no tiene Arduino IDE ni arduino-cli (ver `revision-kit-arduino.md`).
- Regla para el material: nunca capturar código desde Tinkercad en español.

### H3. Proyecto 7, «Ventilador», es incoherente

| Lámina | Qué dice o muestra |
|---|---|
| 51 | Objetivo: «utilizamos un transistor como interruptor electrónico». Materiales: «Transistor». |
| 54–55 | El circuito lleva un componente de 3 patas marcado **TMP** (el sensor TMP36) y el ventilador conectado **directo al pin 12 y a GND**. No hay transistor. |
| 56 | Código de termostato con errores: `temperatura = voltaje * 100 - 50` (la fórmula del TMP36 es `(voltaje − 0.5) * 100`); compara `lectura >= 50` en cuentas del ADC, no en °C; imprime `temp`, variable que no existe (no compila). |

Problemas de fondo: un motor no debe alimentarse desde un pin del Arduino (el límite es de unos 20 mA recomendados, 40 mA máximos) y el kit no trae TMP36.

**Solución:** reconstruir el proyecto con piezas del kit.
- **Opción A (recomendada, pero ver el bloqueo por el consumo de 0.95 A del motor):** PN2222 como interruptor + diodo 1N4007 de protección + motor 3–6 V con aspa, controlado por botón o potenciómetro. Pinout del PN2222 según su datasheet: 1 = Emisor, 2 = Base, 3 = Colector (verificar con multímetro, ver `revision-kit-arduino.md`).
- **Opción B:** el motor con el L293D, como en la lección 20 del kit.
- **Termostato:** si se quiere un ventilador por temperatura, usar el termistor NTC con el código de la lección 19, o el DHT11 (lección 14).

### H4. Las capturas conservan la pantalla completa

Las 8 capturas de código (láminas 14, 22, 29, 38, 47, 48, 56, 64) están recortadas en la lámina, pero el archivo guarda la imagen de 1920×1080. Con «Restablecer imagen» se ve todo: pestañas de correo (con el número de mensajes sin leer), WhatsApp, X, marcadores de trabajo y la barra de tareas.

**Solución:** al reemplazar el código por texto (H2) desaparece el problema. Para cualquier captura que se conserve (circuitos), recortarla en un editor de imágenes, no con la herramienta de recorte de PowerPoint, y comprobar con «Comprimir imágenes → eliminar áreas recortadas».

### H5. Pasos repetidos

Las láminas 3, 4, 10, 11, 18, 19, 26, 27, 33, 34, 42, 43, 52, 53, 60 y 61 (16 de 65) repiten «Busca tu Arduino y no olvides conectarlo» y «Busca tu protoboard».

**Solución:** una sola sección inicial «Conoce tu kit y prepara tu mesa» (placa, protoboard, filas y columnas, riel de alimentación, cómo conectar el USB). Cada proyecto arranca directo en el circuito. Ahorra unas 14 láminas.

### H6. Láminas sin instrucción

- Con solo imagen y el título «PASO N» (sin texto): 13, 14, 21, 22, 29, 36–38, 45, 46, 63, 64.
- Sin título: 47 y 48 (código del dado).
- Sin pie ni resultado esperado: las de «RESULTADO FINAL».

**Solución:** cada paso lleva (1) la instrucción en una frase, (2) una **tabla de conexiones** (pin del Arduino → componente), (3) qué debe verse. Las tablas de pines salen de los sketches del kit.

### H7. Portadas

Las láminas 1, 8, 16, 24, 31, 40, 50 y 58 son imágenes con el texto incluido (no editable) y con otro diseño distinto al institucional.

- La portada del **Dado Digital** (lámina 40) muestra un display de 7 segmentos con un «5», pero el material de la lámina 41 pide «siete focos LED». Hay que decidir cuál se construye.
- La portada del **Ventilador** (lámina 50) muestra un ventilador de PC, que el kit no trae (ver H3).

**Solución:** portadas nuevas con el diseño de la plantilla (divisor de sección). Se puede conservar la foto de la placa si se recorta limpia.

### H8. Formato inconsistente

Las listas de materiales usan tamaños de letra distintos y muy pequeños (por ejemplo, láminas 2, 9, 17, 25). El Proyecto 1 no tiene código y el resto sí, sin avisarlo. **Solución:** se resuelve al usar las tarjetas de la plantilla (objetivo, materiales, conceptos).

### H9. Dependencia de Tinkercad y de computadoras

Tinkercad Circuits solo funciona en línea. El Word además usa Arduino IDE, que necesita una computadora por equipo y, la primera vez, descargar el IDE y las librerías.

**Pendiente de confirmar:** ¿habrá computadoras e internet en el aula de Atzingo? ¿Cuántos alumnos y cuántos kits? (Referencia: en la base del IPPI de 76 municipios indígenas, la mediana es 14% de viviendas con internet y 8% con computadora; falta ver el dato específico de San Gabriel Chilac.)
**Solución (según respuesta):** con computadoras sin internet, instalar IDE y librerías con anticipación desde la carpeta `kit-arduino`. Sin computadoras, usar solo la placa con los sketches ya cargados, o planear cargarlos por equipo desde una laptop del instructor.

### H10. Pasar el curso a la plantilla (Tarea 1)

El archivo `ippi-cursos.pptx` tiene el diseño institucional (Gobierno de Puebla 2024-2030 / IPPI) en 5 variantes: portada, divisor de sección, contenido claro con barra lateral, contenido oscuro con tarjetas y cierre. Todas las láminas usan el layout «En blanco» y el diseño está pegado lámina por lámina, no en el patrón. Las fuentes (Gilroy, Montserrat, Raleway) están embebidas.

**Solución:**
1. Construir sobre una copia de la plantilla para conservar fuentes, logos y patrón.
2. Crear layouts reales (portada, divisor de proyecto, contenido claro, contenido oscuro, cierre) para que los ajustes posteriores no requieran copiar formas.
3. Sustituir el texto de la barra lateral «MESA TÉCNICA» (propuesta: **«CURSOS / IPPI»**).
4. Guardar como `.pptx` nuevo. Los originales no se tocan.

### H11. El Word y el kit

- El capítulo 10 usa TMP36 y su fórmula `(V − 0.5) × 100`; el kit trae termistor NTC (la lección 19 del kit usa la ecuación de Steinhart–Hart).
- La tabla de materiales (tabla 7) lista solo 10 elementos y omite servo, HC-SR04, LCD y los demás que usan los capítulos 9 y 10.
- Pesa casi 20 MB; conviene revisar imágenes antes de compartirlo.

**Solución:** reescribir la tabla de materiales con el inventario del kit y adaptar el capítulo 10 al termistor o al DHT11.

### H12. Derechos de las imágenes del fabricante

Los PDF de lecciones traen diagramas y fotos de REXQualis. **Solución:** para capacitación interna, citar la fuente; si el material se va a difundir, redibujar los circuitos.

## 4. Orden de trabajo sugerido

- [ ] **Fase 0. Prácticas propias** con el kit, en el orden del curso (`plan-curso-arduino.md`, sección 11). El IDE ya está instalado; los sketches están en `curso-arduino/sketches/`.
- [ ] **Fase 1. Plantilla:** layouts + portada + secciones (H10).
- [ ] **Fase 2. Contenido por kit:** elegir proyectos, tablas de pines, código en texto (H1, H2, H3, H5, H6).
- [ ] **Fase 3. Limpieza:** capturas, derechos, Word (H4, H11, H12).
- [ ] **Fase 4. Prueba piloto** con 1–2 estudiantes antes de implementar en Atzingo (tiempos reales por práctica).

## 5. Decisiones pendientes

1. ~~Texto de la barra lateral~~ → «CURSOS / IPPI» (16 nov).
2. ~~Alcance de la migración~~ → sí, completa, sobre la secuencia nueva (16 nov).
3. Nombre del archivo de salida (propuesta: `Curso Electronica y Programacion con Arduino - IPPI.pptx`; el nombre anterior ya no describe el contenido).
4. ~~Número de alumnos, kits, computadoras y duración~~ → 6 kits, 2–3 alumnos por kit, 6 computadoras, 32 h en visitas (la primera, dos días de 4 horas). **Siguen pendientes:** fechas y duración de las visitas 2 a 4, dónde se guardan kits y computadoras entre visitas, y el consumo real del motor.
5. Aprobar la secuencia y los retos del proyecto final (ver `plan-curso-arduino.md`, secciones 3 y 5).
