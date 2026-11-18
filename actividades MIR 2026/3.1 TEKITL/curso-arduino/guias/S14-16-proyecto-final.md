# Sesiones 14 a 16 · Proyecto final

> **Dos advertencias de partida.** (1) **El motor sigue bloqueado** hasta resolver la validación V1 (ver la Sesión 9): los retos que hablan de un «ventilador» o una «bomba» usan **un LED con resistencia de 220 Ω** como carga; el programa es el mismo. (2) **Los siete retos son ideas por validar con los docentes de la prepa** sobre qué problemas locales conviene tomar.

**Guía de práctica para el instructor** (de aquí saldrán después las láminas, las hojas imprimibles y las fichas de los alumnos)
**Tiempos estimados (3 sesiones de 120 min):** Sesión 14 · apertura 5 · presentación del proyecto y de los retos 10 · hoja de diseño 30 · revisión previa del instructor 5 · armado y primera versión 60 · cierre 10. Sesión 15 · apertura y rearmado 20 · definir las 3 pruebas 15 · probar y corregir 55 · documentar 20 · ensayo del guion 10. Sesión 16 · últimas pruebas 15 · exhibición 50 (seis equipos, 5 min + 2 de preguntas) · rúbrica y comentarios 15 · cierre del curso 15 · desarmar y contar el inventario 25. Anota los tiempos reales en la tabla del final.
**Sketches:** `curso-arduino/sketches/Proyecto_plantilla/` (la estructura del proyecto) y, para cada reto, los sketches de las sesiones anteriores que se juntan (tabla del **mapa de reutilización**).
**Ideas nuevas de las sesiones:** pasar de **seguir instrucciones** a **diseñar** (problema → entradas, proceso, salidas → componentes y pines); **juntar** partes de varios programas sin que choquen sus pines ni sus nombres; **probar con criterio** (decir de antemano qué debe pasar y con qué número) y **mejorar en ciclos**; y **explicar** lo que se hizo a otras personas. Es la **segunda mitad de la visita 4**: el día 1 son las Sesiones 13 y 14; el día 2, las 15 y 16. **Cierra el curso.**

## Cómo leer esta guía

| Parte | Para qué sirve |
|---|---|
| **Reglas del proyecto** y **plan de las tres sesiones** | Qué se espera, cómo se reparte el tiempo y qué hace el instructor |
| **Banco de retos** y **mapa de reutilización** | Los siete retos, sus versiones (mínima y completa) y de qué sketches parte cada uno |
| **Mapa de pines**, **Pines por reto** y **cómo juntar dos sketches** | Evitar los choques de pines y de nombres al combinar programas; qué pin cambia en cada reto cuando hay pantalla |
| **Hoja A · Diseño** · **Hoja B · Pruebas** · **Hoja C · Exhibición y rúbrica** · **Hoja D · Entrega y cierre** | Hojas **para imprimir** (una por equipo); todas se llenan a mano |
| **La plantilla** (`Proyecto_plantilla`) | Un esqueleto que ya funciona y que cada equipo cambia pieza por pieza |

## Reglas del proyecto

- **Equipos de 2 o 3** (un kit por equipo, seis equipos). **Roles que rotan** entre las Sesiones 14, 15 y 16: **armador**, **programador** y **verificador/bitácora**. Con 2 personas, armador y programador se alternan.
- **Se elige un reto** de la lista (o uno libre con aprobación del instructor) y se **llena la Hoja A antes de armar**. **El instructor la revisa** (pines sin choques, componentes disponibles, nada peligroso) y la firma: **sin su visto bueno no se conecta la corriente.**
- **Primero la versión mínima, luego la completa.** En cada reto hay una versión **mínima** (casi siempre, un sketch del curso funcionando con **los números del equipo**) y una **completa** (lo que se le agrega). Se arma la mínima primero. **Un proyecto mínimo que funciona vale más que uno completo que no enciende.**
- **Se puede (y se debe) reutilizar** el código y los circuitos del curso. Lo que se evalúa es **entender lo que se junta** y **la parte propia**: ¿qué cambió el equipo y por qué? Dos equipos pueden tomar el mismo reto, pero con una **diferencia propia** (otra planta, otros umbrales, otro mensaje).
- **Solo 5 V.** Todo el proyecto funciona con la corriente del USB. Nada se conecta a la corriente de la casa. **Agua lejos de la placa y de los cables** (Sesión 13).
- **El kit se cuida.** Pantalla sin doblar sus patas; sensores y cables macho-hembra en su bolsa al terminar.
- **Se evalúa con cuatro criterios:** **funciona**, **está bien armado y ordenado**, **lo explican con claridad** (incluyendo qué cambiaron y por qué) y **trabajaron en equipo** (Hoja C). No es un examen: la rúbrica dice de antemano qué se espera.
- *(Pendiente de decisión de quien coordina: si el curso da constancia o calificación y con qué requisitos; la rúbrica solo describe niveles.)*

## Plan de las tres sesiones

### Sesión 14 · Diseño y armado (120 min)

| Minutos | Actividad | Detalle |
|---|---|---|
| 0–5 | Apertura | Contar el kit con la hoja de inventario (el kit sigue armado de la Sesión 13; se desmonta lo que no sirva para el proyecto) |
| 5–15 | **Presentación** | El instructor muestra **el reto 1 funcionando** (ya armado, 2 minutos) y lee las reglas. Se reparten las hojas A, B, C y D. Se presenta el banco de retos |
| 15–45 | **Hoja de diseño (Hoja A)** | Cada equipo elige, llena la hoja y **dibuja las conexiones**. Preguntas guía del instructor: *«¿qué problema resuelven y para quién?», «¿qué mide?, ¿qué decide?, ¿qué hace?»* |
| 45–50 | **Revisión previa del instructor** | Pasa por los seis equipos y **firma la hoja** (lista en la Hoja A). Los que no tengan firma ajustan antes de armar |
| 50–110 | **Armado y primera versión** | Se arma la **versión mínima**, se sube el sketch y se prueba. El instructor circula (**sin armar por ellos**, ver «Cómo ayudar sin resolver») |
| 110–120 | Cierre | En la bitácora: qué quedó armado, qué falta y qué sigue mañana. **El kit se desarma al final del día** (la pantalla sin doblar sus patas) y cada equipo **guarda su sketch y su hoja** |

### Sesión 15 · Pruebas y mejora (120 min)

| Minutos | Actividad | Detalle |
|---|---|---|
| 0–20 | Apertura y rearmado | Se vuelve a armar lo que quedó del día anterior con la **hoja de diseño y el dibujo de conexiones** (primera prueba de que esos documentos sirven). Con pantalla son unos 17 cables: el instructor revisa antes de energizar |
| 20–35 | **Definir 3 pruebas con criterio (Hoja B)** | Cada prueba dice **qué se hace**, **qué debe pasar** y **con qué número**. Ejemplo: *«con el vaso a la mitad, el semáforo se pone amarillo»* o *«el ventilador enciende a 28 ± 1 °C»*. Una prueba sin criterio («que funcione bien») no vale |
| 35–90 | **Probar, corregir y mejorar** | Se hacen las 3 pruebas, **se anota lo que pasó de verdad**, se corrige y se repite. Después, la **versión completa** (lo que alcance) |
| 90–110 | **Documentar** | Dibujo final de las conexiones (corregido si se cambió algo), sketch final comentado, **foto** del armado y **video corto de respaldo** (por si el día de la exhibición algo falla) |
| 110–120 | **Ensayo del guion** | Cada equipo ensaya sus 5 minutos (Hoja C): quién dice qué |

### Sesión 16 · Exhibición y cierre (120 min)

| Minutos | Actividad | Detalle |
|---|---|---|
| 0–15 | Apertura | Últimas pruebas. Cada equipo ordena su lugar (kit armado, hoja de diseño y bitácora a la vista) |
| 15–65 | **Exhibición** | **5 minutos por equipo + 2 de preguntas** (Hoja C): el problema, la solución, la demostración y qué aprendieron. El resto del grupo **escucha y pregunta** (una pregunta por equipo, por lo menos) |
| 65–80 | **Rúbrica y comentarios** | El instructor llena la rúbrica (Hoja C) con cada equipo y le da **dos cosas que salieron bien** y **una por mejorar** |
| 80–95 | **Cierre del curso** | Cada persona dice una cosa que aprendió y una cosa que le gustaría seguir haciendo. Se anota qué sigue (ver «Qué sigue»). Se recogen las ideas del grupo para mejorar el curso |
| 95–120 | **Desarmar, guardar y contar** | Hoja D: se desarma, se guarda cada pieza en su lugar, se cuenta el inventario y cada equipo **copia su sketch final a la carpeta del equipo** |

**Si un equipo no termina:** presenta lo que sí funciona (**la versión mínima**), enseña **qué falla y qué intentaron**. Eso también se evalúa: saber decir «aquí me quedé» es parte de entender el proyecto.

## Banco de retos

Siete ideas. **Todas usan lo visto en el curso.** «Mínima» es la que se arma primero; «completa» es lo que se le agrega después.

| # | Reto | Problema local | Entradas | Salidas |
|---|---|---|---|---|
| 1 | **Aviso de riego** para una maceta | Saber cuándo regar sin adivinar | Humedad de suelo | Semáforo de LED, zumbador, pantalla |
| 2 | **Tinaco con alarma y bomba simulada** | Que el tinaco o el tambo no se quede vacío ni se derrame | Nivel de agua | Semáforo, zumbador, «bomba» (LED; motor cuando se destrabe), pantalla |
| 3 | **Alarma de casa** | Avisar si alguien entra a un cuarto | PIR y botón | Sirena, LED, pantalla con el estado |
| 4 | **Termostato de invernadero o gallinero (en maqueta)** | Mantener fresco un espacio pequeño | Temperatura y humedad (DHT11), perilla del límite | «Ventilador» (LED; motor cuando se destrabe), pantalla |
| 5 | **Barrera de estacionamiento con contador** | Contar y dejar pasar vehículos | Distancia (HC-SR04) | Servo (la barrera), pantalla con el contador, LED |
| 6 | **Semáforo peatonal** | Cruzar la calle de forma segura, con luz que se adapta | Botón del peatón y sensor de luz | Semáforo de LED con brillo ajustable, zumbador |
| 7 | **Reto libre** | El que el equipo proponga | — | — |

### Mapa de reutilización (de qué sketches parte cada reto)

| # | Versión mínima | Versión completa (se le agrega) | Sketches del curso que se juntan |
|---|---|---|---|
| 1 | Sensor de suelo y semáforo, calibrados con **la maceta del equipo** | + zumbador que avise cuando esté seca; + pantalla con el porcentaje y el estado; + botón para silenciar | `P24_humedad_suelo` · `P24_zumbador_seco` · `P21_lcd_hola` (la pantalla) |
| 2 | Sensor de nivel, semáforo y pitido de nivel bajo | + «bomba» con histéresis (se enciende abajo y se apaga arriba); + pantalla con el nivel | `P25_nivel_agua` · `P25_bomba_simulada` · `P21_lcd_hola` |
| 3 | PIR, botón, LED y sirena | + tiempo de salida y código de desarme; + pantalla con **ARMADA / DESARMADA / ALARMA** | `P08_alarma_pir` · `P08_alarma_completa` · `P21_lcd_hola` |
| 4 | DHT11 y un LED que se enciende sobre un límite fijo | + perilla del límite; + **histéresis de 2 °C**; + pantalla con T, humedad, límite y estado | `P22_estacion_clima` · `P23_ventilador_automatico` (la estructura de control) |
| 5 | Barrera automática (HC-SR04 y servo) | + contador de vehículos en la pantalla; + «cupo»: al llegar a N vehículos, luz roja y la barrera **no abre** | `P16_barrera_automatica` · `P16_contador_vehiculos` · `P21_lcd_hola` |
| 6 | Semáforo con botón del peatón | + el sensor de luz regula el **brillo** de los LED (más luz, más brillo); + pitido durante el verde peatonal | `P06_semaforo_con_boton` · `P12_lampara_automatica` (la lectura de luz y `analogWrite`) |
| 7 | Lo que acuerden con el instructor | | `Proyecto_plantilla` |

**Antes de armar con pantalla:** la pantalla ocupa los pines 7 a 12 y casi todos los programas del curso usan alguno de ellos. Los pines nuevos de cada reto están en la sección **Pines por reto** (más abajo); hay que mirarla **antes de llenar la Hoja A**.

**Qué más tiene cada reto**

1. **Aviso de riego.** *Cuidado:* con la pantalla **cambian de pin los tres LED y el zumbador** (los cuatro chocan con la pantalla); además, la pantalla y el semáforo juntos ocupan mucho protoboard y el instructor revisa. *La parte propia:* la planta (¿qué humedad le conviene?) y los umbrales.
2. **Tinaco.** *Cuidado:* el **agua queda lejos** de la placa. Con la pantalla **cambian de pin los LED, el zumbador y la «bomba»** (el 5 lo ocupa ahora el LED amarillo, así que la «bomba» pasa al 13). Si se resuelve V1, la «bomba» puede pasar del LED al motor con el circuito de la Sesión 9 **sin cambiar el programa**. *La parte propia:* los dos niveles y qué hace la «bomba».
3. **Alarma de casa.** *Cuidado:* el programa del curso espera **60 segundos** de calentamiento del PIR (Sesión 4; el tiempo real se comprueba en V8) y sus perillas se ponen al mínimo para las pruebas. Con la pantalla **cambian de pin el PIR, el LED y el zumbador**; solo el botón se queda en el 2. En la versión completa, la pantalla se escribe **solo cuando cambia el estado** (regla 9 del mapa de pines). *La parte propia:* el tiempo de salida, el código de desarme y los mensajes.
4. **Termostato.** *Cuidado:* el DHT11 solo da **números enteros** (resolución de 1 °C y precisión de ± 2 °C, Sesión 10), así que una histéresis de 1 °C es **un solo escalón**: se usan **2 °C**. Es el **único reto que no cambia ningún pin** al agregar la pantalla, pero usa **los dos potenciómetros del kit** (uno para el contraste y otro para el límite): no sobra ninguno. *La parte propia:* el límite (¿qué temperatura necesita un pollito o una lechuga?) y la histéresis.
5. **Barrera con contador.** *Cuidado:* el HC-SR04 usa **dos pines** y el servo, el zumbador y el LED uno cada uno: con la pantalla **cambian cuatro de los cinco pines** del programa del curso (ECHO, servo, zumbador y LED; solo el TRIG, en el 6, se queda). La versión completa agrega un LED de «cupo lleno» y un botón de reinicio del contador. *La parte propia:* el cupo y la distancia a la que se abre.
6. **Semáforo peatonal.** *Cuidado:* para cambiar el brillo hay que usar **pines con ~**. Los pines con ~ son 3, 5, 6, 9, 10 y 11, pero `tone()` (el zumbador) le quita el ~ al 3 y al 11: quedan **5, 6, 9 y 10**. El semáforo del curso usa el 8 para el rojo y **el 8 no tiene ~**: el rojo se mueve al 5. Este reto **no lleva pantalla**. Pon el LDR **lejos de los LED** (si los LED lo iluminan, se repite la retroalimentación de la Sesión 6). *La parte propia:* los tiempos y el brillo.
7. **Reto libre.** Debe tener **al menos una entrada, una decisión que recuerde un estado y una salida**, y pasar la revisión de seguridad. Ejemplos: un semáforo con sonido para personas ciegas; un medidor de distancia con escala en LED; un reloj de aula con la pantalla (con `millis()`).

## Mapa de pines

Lo que **usó cada sesión** y lo que **queda libre cuando se usa la pantalla LCD** (que ocupa los pines **7 a 12**).

| Pin | Lo que usó el curso | Si el proyecto lleva pantalla | Notas |
|---|---|---|---|
| 0 y 1 | Comunicación con la computadora (USB) | **No se usan** | Conectar algo aquí estorba para subir el programa y para el Monitor Serie |
| 2 | Botón | **Libre** | |
| 3 (~) | — | **Libre** | PWM; `tone()` le quita el PWM |
| 4 | — | **Libre** | |
| 5 (~) | Carga: motor o «ventilador» o «bomba» (Sesiones 9, 12 y 13) | **Libre** | PWM |
| 6 (~) | TRIG del HC-SR04 | **Libre** | PWM |
| 7 | PIR; ECHO del HC-SR04 | **Pantalla (D7)** | El PIR y el ECHO se mueven a otro pin libre |
| 8 | LED rojo | **Pantalla (D6)** | Los LED se mueven (por ejemplo, a 4, 5 y 6; ver **Pines por reto**) |
| 9 (~) | LED amarillo / LED con PWM; servo | **Pantalla (D5)** | El servo se mueve a otro pin libre |
| 10 (~) | LED verde | **Pantalla (D4)** | |
| 11 (~) | — | **Pantalla (E)** | |
| 12 | Zumbador | **Pantalla (RS)** | El zumbador se mueve (por ejemplo, al 3; `tone()` funciona en cualquier pin) |
| 13 | LED integrado «L» (Sesión 1) | **Libre** | El LED «L» parpadea al subir un programa |
| A0 | Sensor principal (perilla, LDR, termistor, DHT11, suelo, agua) | **Libre** | |
| A1 | Segunda perilla (Sesiones 6 y 12) | **Libre** | |
| A2 a A5 | — | **Libres** | Sirven como entradas analógicas o como pines digitales |

**Reglas para combinar** (las hojas de datos y las pruebas de las sesiones anteriores)

1. **Un pin, una función.** Antes de armar, llena la tabla de pines de la Hoja A y **busca los repetidos**.
2. **La pantalla ocupa 7 a 12.** Se declara `LiquidCrystal lcd(12, 11, 10, 9, 8, 7);` (la de la Sesión 11). Todo lo demás se acomoda en 2 a 6, 13 y A0 a A5. **Solo se mueve lo que choca:** un pin del curso que queda libre con la pantalla se deja donde estaba. Los pines nuevos de cada reto están en **Pines por reto**.
3. **El servo y los pines 9 y 10.** La biblioteca `Servo` le quita el PWM a los pines **9 y 10**. Si se usa servo, el PWM va en 3, 5 o 6. El servo puede ir en **cualquier pin**.
4. **`tone()` y los pines 3 y 11.** `tone()` interfiere con el PWM de esos dos pines, y **solo suena un tono a la vez**. Si hay zumbador y LED con brillo, el brillo va en un pin con ~ que `tone()` no toque: **5, 6, 9 o 10** sin pantalla, y solo **5 o 6** con pantalla (el 9, el 10 y el 11 son de la pantalla).
5. **El DHT11 de este curso solo funciona en A0 a A5.** Su código usa el puerto C: se cambia `#define DHT11_PIN 0` (A0) por 1 (A1), 2 (A2)… No funciona en los pines digitales 2 a 13.
6. **`delay()` largo bloquea todo.** Mientras dura, el programa no lee ni el botón ni el sensor. Se usan esperas cortas (medio segundo como máximo) o `millis()` (Sesión 11 y `P08_alarma_completa`).
7. **El 5 V y el GND son comunes.** Todo el proyecto comparte los rieles. Si la **pantalla parpadea** o **la placa se reinicia** cuando se mueve el servo, falta corriente del USB (V9): se prueba sin el servo o con otro cable USB.
8. **El motor sigue bloqueado** (V1): la carga es un **LED con 220 Ω**.
9. **Escribe en la pantalla solo cuando algo cambió.** `lcd.clear()` en cada vuelta hace que la pantalla **parpadee**. Se escribe en una posición fija (`lcd.setCursor`) y se sobrescribe con espacios, como en `P22_estacion_clima`, o solo cuando cambia el estado (por ejemplo, de ARMADA a ALARMA). Cada `lcd.print` tarda un poco: en un programa con vuelta de 10 ms, como `P08_alarma_completa`, escribir en cada vuelta la alarga.

## Pines por reto

Cuando un proyecto lleva **pantalla** (que ocupa los pines 7 a 12), los programas del curso que se juntan con ella tienen pines que chocan. **Solo se mueve lo que choca.** En cada tabla, «Pin en el curso» es el del sketch original y «Pin en el proyecto» es el que se usa al juntarlo con `P21_lcd_hola`. En el código se cambia **un solo número**, el de la constante de arriba (por ejemplo, `const int LED_ROJO = 4;`): el resto del programa usa el nombre y no hay que tocarlo.

**Cómo se comprobaron.** Se armó en código la **versión completa** de cada reto con estos pines. Los seis compilan para Arduino UNO sin errores ni avisos, y un verificador revisó que no haya pines repetidos, que no se use el 0 ni el 1, que todo `analogWrite` esté en un pin con ~ y que `tone()` y `Servo` no le quiten el PWM. **No se probaron con cables ni en la placa** (V8, V9 y V13 siguen pendientes). Son combinaciones del instructor: no están en `sketches/`, para que cada equipo arme la suya.

**Reto 1 · Aviso de riego** (`P24_zumbador_seco` + `P21_lcd_hola`)

| Pieza | Pin en el curso | Pin en el proyecto |
|---|---|---|
| Sensor de suelo (S) | A0 | A0 (igual) |
| LED rojo | 8 | **4** |
| LED amarillo | 9 | **5** |
| LED verde | 10 | **6** |
| Zumbador pasivo (con 220 Ω) | 12 | **3** |
| Botón «silenciar» (versión completa) | 2 | 2 (igual) |
| Pantalla LCD1602 | no lleva | 12, 11, 10, 9, 8, 7 |

*Quedan libres:* 13 y A1 a A5.

**Reto 2 · Tinaco con alarma y bomba simulada** (`P25_nivel_agua` + `P25_bomba_simulada` + `P21_lcd_hola`)

| Pieza | Pin en el curso | Pin en el proyecto |
|---|---|---|
| Sensor de nivel (S) | A0 | A0 (igual) |
| LED rojo / amarillo / verde | 8 / 9 / 10 | **4 / 5 / 6** (el mismo semáforo del reto 1) |
| Zumbador pasivo (con 220 Ω) | 12 | **3** |
| «Bomba» (LED con 220 Ω; con el motor, la base del PN2222 con 330 Ω) | 5 | **13** |
| Pantalla LCD1602 | no lleva | 12, 11, 10, 9, 8, 7 |

*Nota:* el 5 lo ocupa ahora el LED amarillo, por eso la «bomba» pasa al 13. El LED integrado «L» de la placa se enciende junto con la «bomba» (es el mismo pin). *Quedan libres:* 2 y A1 a A5.

**Reto 3 · Alarma de casa** (`P08_alarma_pir` o `P08_alarma_completa` + `P21_lcd_hola`)

| Pieza | Pin en el curso | Pin en el proyecto |
|---|---|---|
| Sensor PIR (OUT) | 7 | **5** |
| Botón (arma y desarma) | 2 | 2 (igual) |
| LED «armada» | 8 | **4** |
| Zumbador pasivo (con 220 Ω) | 12 | **3** |
| Pantalla LCD1602 | no lleva | 12, 11, 10, 9, 8, 7 |

*Quedan libres:* 6, 13 y A0 a A5.

**Reto 4 · Termostato de invernadero o gallinero** (`P22_estacion_clima` + `P23_ventilador_automatico` + `P21_lcd_hola`)

| Pieza | Pin en el curso | Pin en el proyecto |
|---|---|---|
| DHT11 (S) | A0 | A0 (igual; el DHT11 solo funciona en A0 a A5) |
| Perilla del límite | A1 | A1 (igual) |
| «Ventilador» (LED con 220 Ω; con el motor, la base del PN2222 con 330 Ω) | 5 | 5 (igual) |
| Pantalla LCD1602 | 12, 11, 10, 9, 8, 7 | 12, 11, 10, 9, 8, 7 (igual) |

**Ningún pin cambia.** Aquí el DHT11 reemplaza al termistor de `P23`: la temperatura llega como número entero (`byte`) y se compara igual con el límite. *Usa los dos potenciómetros del kit* (contraste y límite). *Quedan libres:* 2, 3, 4, 6, 13 y A2 a A5.

**Reto 5 · Barrera de estacionamiento con contador** (`P16_barrera_automatica` + `P16_contador_vehiculos` + `P21_lcd_hola`)

| Pieza | Pin en el curso | Pin en el proyecto |
|---|---|---|
| HC-SR04 · TRIG | 6 | 6 (igual) |
| HC-SR04 · ECHO | 7 | **5** |
| Servo (señal) | 9 | **4** |
| Zumbador pasivo (con 220 Ω) | 12 | **3** |
| LED verde «barrera abierta» | 8 | **2** |
| LED rojo «cupo lleno» (versión completa) | no lleva | **13** |
| Botón de reinicio del contador (versión completa) | no lleva | **A1** (`pinMode(A1, INPUT_PULLUP);`) |
| Pantalla LCD1602 | no lleva | 12, 11, 10, 9, 8, 7 |

*Cambian cuatro de los cinco pines del programa del curso.* Los pines A1 a A5 también sirven como pines digitales. *Quedan libres:* A0, A2 a A5.

**Reto 6 · Semáforo peatonal** (`P06_semaforo_con_boton` + `P12_lampara_automatica`; **sin pantalla**)

| Pieza | Pin en el curso | Pin en el proyecto |
|---|---|---|
| LED rojo | 8 (no tiene ~) | **5** (con ~) |
| LED amarillo | 9 | 9 (igual, con ~) |
| LED verde | 10 | 10 (igual, con ~) |
| Botón del peatón | 2 | 2 (igual) |
| Sensor de luz (LDR + 10 kΩ) | A0 | A0 (igual) |
| Zumbador (pitido peatonal) | 12 | 12 (igual) |
| Perilla (brillo mínimo o máximo, opcional) | A1 | A1 (igual) |

*Solo cambia el rojo*, porque necesita ~ para regular el brillo y el 8 no lo tiene. Los tres LED quedan en 5, 9 y 10, que conservan el PWM aunque suene el zumbador. Con el reto 6 **sin** pantalla sobran 3, 4, 6, 7, 8, 11 y 13.

**Reto 7 · Reto libre.** Se parte de `Proyecto_plantilla` (entrada en A0, salida en el 5). Si lleva pantalla, esos dos pines ya están libres; los demás se acomodan con las reglas del mapa de pines.

## Cómo juntar dos sketches

1. **Abre los dos** y **uno nuevo** (guárdalo con el nombre del proyecto, en una carpeta propia: un solo `.ino` por carpeta).
2. **Copia** primero lo que es de **uno** y **pruébalo**. Después agrega el otro **poco a poco**, y prueba cada vez.
3. **Los pines van arriba.** Copia las líneas `const int PIN_…` y **cambia los que choquen** (tabla de **Pines por reto**). El número se cambia **solo en esa línea**: el resto del programa usa el nombre.
4. **Los `#include` y los objetos** (`Servo`, `LiquidCrystal`) se copian una sola vez, arriba.
5. **El `setup()` se junta**: todas las líneas de los dos `setup()`, en **un** solo `setup()`.
6. **El `loop()` es el que se piensa**: es la receta **medir → decidir → actuar → mostrar** (ver la plantilla). No se pegan dos `loop()` uno tras otro: se **mezclan los pasos** de los dos.
7. **Los nombres no se repiten.** Si los dos sketches tienen una variable o una función con el mismo nombre (por ejemplo `medirDistancia`), el compilador lo dice: se cambia **uno**.
8. **Si compila pero no funciona**, se divide el problema (ver «Cómo ayudar sin resolver»): ¿llega la lectura?, ¿llega la decisión?, ¿llega la salida?

## La plantilla `Proyecto_plantilla`

`curso-arduino/sketches/Proyecto_plantilla/Proyecto_plantilla.ino` es un esqueleto que **ya funciona** (con una perilla en A0 y un LED con 220 Ω en el pin 5) y que tiene las cuatro tareas del proyecto, cada una en su función:

```cpp
void loop() {
  int valor = medir();                 // 1. MEDIR
  decidir(valor);                      // 2. DECIDIR
  actuar();                            // 3. ACTUAR
  mostrar(valor);                      // 4. MOSTRAR
  delay(ESPERA_MS);
}
```

- **Sección 1 · Pines**, todos juntos arriba y con nombre. **Sección 2 · Valores que se ajustan** (`UMBRAL`, `HISTERESIS`…). **Sección 3 · Variables que recuerdan** (`encendido`). **Sección 4 · Tareas**: `medir()`, `decidir()`, `actuar()`, `mostrar()`.
- El encabezado tiene espacio para **escribir el nombre del equipo, el problema, las entradas, el proceso, las salidas y las conexiones**: **es parte del proyecto** y se llena.
- `decidir()` ya trae la **histéresis** de la Sesión 12; `mostrar()` imprime en el formato `Valor:…,Estado:…` que el **Serial Plotter** dibuja como gráfica (Sesión 5).
- Es **un punto de partida, no la respuesta**: ningún reto sale solo con cambiar un número.

## Cómo ayudar sin resolver

Un equipo atorado **no necesita la solución, necesita una pregunta**. Las que más sirven:

- *«¿Qué esperabas que pasara y qué pasó?»* (anotar las dos cosas)
- *«¿Qué dice el Monitor Serie?»* — si **no imprime nada**, el problema está antes; si imprime algo raro, está en `medir()`.
- **Dividir el problema:** ¿llega la **lectura** (se ve en el Monitor Serie)? ¿llega la **decisión** (el estado cambia)? ¿llega la **salida** (el LED o el servo responde)? El primer «no» marca dónde buscar.
- *«¿Qué cambió desde la última vez que funcionó?»* — casi siempre es **una** cosa.
- *«Deja solo esta parte y quita el resto»*: probar **un** sensor o **una** salida **sola** es la mejor herramienta.
- *«Lee el diagrama de la sesión donde lo hicimos»*: las guías de las Sesiones 1 a 13 tienen el armado y las fallas comunes de cada pieza.

**Reglas del instructor:** no se arma ni se teclea por el equipo; se **señala el lugar** y se pregunta. Si falta una pieza, **se deja sin resolver y se anota** (puede ser una limitación del kit). **Las ideas que se inventen no se descartan solo porque no estén en el banco de retos**: se evalúan con la revisión de seguridad.

## Hoja A · Diseño *(imprimir; una por equipo)*

**Equipo:** ______________________   **Fecha:** __________   **Reto elegido (número y nombre):** ______________________

| Rol | Sesión 14 | Sesión 15 | Sesión 16 |
|---|---|---|---|
| **Armador** | | | |
| **Programador** | | | |
| **Verificador / bitácora** | | | |

**1. ¿Qué problema resuelve y para quién?** (una o dos frases, con sus palabras)

&nbsp;

**2. Entrada, proceso, salida**

| ENTRADA: ¿qué mide? | PROCESO: ¿qué decide? (con qué números) | SALIDA: ¿qué hace o muestra? |
|---|---|---|
| | | |

**3. Componentes** *(marca los que usarán y cuántos)*

| Componente | Cantidad | Componente | Cantidad |
|---|---|---|---|
| LED (colores: ______) | | Zumbador pasivo | |
| Resistencias de 220 Ω | | Pantalla LCD1602 (+ potenciómetro y 100 Ω) | |
| Botón | | Servo | |
| Perilla (potenciómetro) | | Sensor de suelo / de agua | |
| Fotorresistencia + 10 kΩ | | Termistor + 10 kΩ / DHT11 | |
| HC-SR04 | | PIR | |
| Cables macho-macho | | Cables macho-hembra | |

**4. Tabla de pines** *(un pin, una función; revisa el mapa de pines y **Pines por reto** de la guía)*

**¿El proyecto lleva pantalla?** ☐ Sí → escribe «pantalla» en los pines 7 a 12 (7 = D7, 8 = D6, 9 = D5, 10 = D4, 11 = E, 12 = RS) ☐ No

| Pin | Qué se conecta | Pin | Qué se conecta |
|---|---|---|---|
| 2 | | 8 | |
| 3 | | 9 | |
| 4 | | 10 | |
| 5 | | 11 | |
| 6 | | 12 | |
| 7 | | 13 | |
| A0 | | A3 | |
| A1 | | A4 | |
| A2 | | A5 | |

Pines con **~** (para brillo con `analogWrite`): 3, 5, 6, 9, 10 y 11. El servo le quita el ~ al 9 y al 10; `tone()` (el zumbador), al 3 y al 11.

¿Se repite algún pin? ☐ No ☐ Sí → ¿cómo se resolvió? ________________________________

**5. Dibujo de las conexiones** *(en esta hoja o al reverso: cada cable con su color y a dónde va)*

&nbsp;

&nbsp;

&nbsp;

**6. ¿Qué sketches del curso vamos a juntar?** ________________________________________________

**7. ¿Qué va a ser **nuestro** y diferente de los ejemplos?** (los umbrales, la planta, los mensajes, una función nueva…) ________________________________________________

**8. ¿Qué podría salir mal y cuál es el plan B?** ________________________________________________

**Revisión previa del instructor** *(antes de conectar la corriente)*

- ☐ Sin pines repetidos y sin pines 0 y 1. Con pantalla, **nada más usa los pines 7 a 12**.
- ☐ Todo lo que lleva brillo (`analogWrite`) está en un pin con ~ que ni el servo ni `tone()` le quiten.
- ☐ Todo el equipo está en el kit (nada de piezas que no hay).
- ☐ Cada LED tiene su resistencia de 220 Ω; el zumbador pasivo, la suya.
- ☐ Solo 5 V; agua (si hay) lejos de la placa y de los cables.
- ☐ El motor **no** está en el diseño (la carga es un LED).

**Visto bueno:** ______________ **Hora:** ________

## Hoja B · Pruebas *(imprimir; una por equipo)*

**Equipo:** ______________________   **Proyecto:** ______________________

**Una prueba dice 1) qué se hace, 2) qué debe pasar y 3) con qué número.** Ejemplos: *«poner el vaso a la mitad → el semáforo se pone amarillo»* · *«con la mano a 15 cm → la barrera se abre en menos de 1 segundo»* · *«el ventilador enciende a 28 ± 1 °C»*. Una prueba sin criterio («que funcione bien») no vale.

| # | **Qué hago** | **Qué debe pasar** (con número) | **Qué pasó de verdad** | **¿Pasó?** | **Qué cambié** |
|---|---|---|---|---|---|
| 1 | | | | ☐ Sí ☐ No | |
| 2 | | | | ☐ Sí ☐ No | |
| 3 | | | | ☐ Sí ☐ No | |

**Segunda vuelta** *(después de corregir; repetir las pruebas que no pasaron)*

| # | **Qué pasó ahora** | **¿Pasó?** | **Qué más cambió** |
|---|---|---|---|
| 1 | | ☐ Sí ☐ No | |
| 2 | | ☐ Sí ☐ No | |
| 3 | | ☐ Sí ☐ No | |

**¿Qué falla puede tener nuestro proyecto?** (un sensor desconectado, un valor raro…) ¿Qué hace entonces? ________________________________________________

**Lo que descubrimos:** ________________________________________________

## Hoja C · Exhibición y rúbrica *(imprimir; una por equipo)*

### Guion de los 5 minutos *(el equipo lo escribe y lo ensaya)*

| Minuto | Qué se dice | Quién |
|---|---|---|
| 0:00 a 0:30 | **El problema.** ¿Qué problema resuelve y para quién? | |
| 0:30 a 1:30 | **La solución.** Cómo funciona: *entra… se decide… sale…* (con el dibujo) | |
| 1:30 a 3:30 | **Demostración en vivo.** Mostrar que funciona, y **una prueba de la Hoja B** | |
| 3:30 a 4:30 | **Qué cambiamos y qué aprendimos.** ¿Qué cambió con respecto al ejemplo del curso y por qué? ¿Qué falló y cómo se resolvió? | |
| 4:30 a 5:00 | **Cierre.** Una mejora que harían con más tiempo | |

**Si la demostración falla:** se enseña el **video de respaldo** (Sesión 15) y se explica qué pasó. Eso no baja la nota por sí solo: se evalúa **cómo se explica**.

### Rúbrica *(la llena el instructor con el equipo)*

| Criterio | **En desarrollo** | **Logrado** | **Destacado** |
|---|---|---|---|
| **1 · Funciona** | Funciona a ratos o solo con ayuda | **Cumple lo que dice la Hoja A** y pasa **al menos 2 de las 3 pruebas** de la Hoja B | Pasa las 3 pruebas y **maneja una falla** (sensor desconectado o valor raro) sin descomponerse |
| **2 · Bien armado y ordenado** | Cables enredados, sin colores, piezas flojas | **Colores consistentes** (negro GND, rojo 5 V), piezas ordenadas, el **sketch tiene nombres claros** y comentarios | Además, **el dibujo del equipo coincide con el armado real**, el código está **en funciones** y los valores ajustables están arriba |
| **3 · Lo explican con claridad** | Solo muestran; no saben decir cómo funciona | Explican el **problema**, **cómo funciona** (entra, se decide, sale) y **qué cambiaron y por qué** | Además explican **los números que eligieron** (umbrales, calibración), **qué falló** y cómo lo resolvieron |
| **4 · Trabajaron en equipo** | Una sola persona hizo casi todo | Los **roles rotaron** y **todas las personas** pueden explicar una parte | Además **ayudaron a otro equipo** o se repartieron las tareas con un plan |

| Criterio | Nivel | Comentario del instructor |
|---|---|---|
| 1 · Funciona | | |
| 2 · Bien armado y ordenado | | |
| 3 · Lo explican con claridad | | |
| 4 · Trabajaron en equipo | | |

**Dos cosas que salieron bien:** ______________________________________________

**Una cosa por mejorar:** ______________________________________________

**Preguntas del grupo** *(una por equipo, por lo menos)*: ______________________________________________

## Hoja D · Entrega y cierre *(imprimir; una por equipo)*

**Equipo:** ______________________   **Número de kit:** ______

**Al desarmar** *(la persona que verifica va marcando)*

- ☐ Sensores desconectados y secos (suelo, agua); **pistas limpias**.
- ☐ Pantalla LCD guardada **sin doblar sus patas**.
- ☐ Cables macho-hembra en su paquete; macho-macho ordenados por color.
- ☐ Servo, LED, resistencias, botón, zumbadores, termistor, DHT11, HC-SR04 y PIR **en su lugar**.
- ☐ **Inventario contado** con la hoja del kit: falta ______________________________________

**Entregamos** *(copiados a la carpeta del equipo)*

- ☐ El **sketch final** (en una carpeta con su nombre: `Proyecto_______`).
- ☐ La **hoja de diseño (A)** y las **pruebas (B)** con lo que pasó.
- ☐ El **dibujo final** de las conexiones.
- ☐ Una **foto** del armado y el **video de respaldo**.
- ☐ La **bitácora** con el visto bueno del instructor.

**Una cosa que aprendimos:** ______________________________________________

**Una cosa que nos gustaría seguir haciendo:** ______________________________________________

**Una idea para mejorar este curso:** ______________________________________________

## Si un equipo va adelantado

Se le propone **mejorar** su proyecto antes de agregar piezas: una **segunda prueba**, un **mensaje claro** en la pantalla, la **protección contra fallas** (qué hace si el sensor se desconecta), el **registro de datos** en el Monitor Serie o una **maqueta de cartón**. Si lo terminó todo y quiere un componente nuevo, el kit trae piezas de **ampliación** con código de la lección correspondiente en `kit-arduino/Code/`: **alarma de gas MQ-2** (lección 30; **solo con el instructor**, el sensor se calienta), **sensor de sonido** (27), **lector RFID** (29), **reloj RTC** (26), **matriz de LED** (22), **joystick** (12), **control remoto IR** (15, con la biblioteca `IRremote` del zip del kit) y **motor a pasos** (16 y 28). **Son extras: no están probados ni adaptados al curso.**

## Qué sigue *(para comentar al cerrar)*

- Cada equipo **conserva su sketch, sus hojas y su foto** (copia en la carpeta del equipo y, si hay forma, en su memoria USB).
- Qué se puede hacer **con lo aprendido** en la escuela y en la comunidad (los problemas del banco de retos, en grande).
- *(Pendiente de decisión de quien coordina: constancia, continuidad del taller, dónde se guardan los kits entre ciclos.)*

## Tu práctica: anota lo que encuentres

Haz **un reto completo** como lo haría un equipo (por ejemplo, el 1 o el 3) y llena esto. Sirve para ajustar el tiempo, las hojas y la rúbrica.

| Dato | Anota aquí |
|---|---|
| Reto que hiciste y versión (mínima o completa) | |
| Tiempo real de la **hoja de diseño** y del **armado** | |
| ¿Hubo pines repetidos al juntar sketches? ¿Cuáles? | |
| ¿La tabla de **Pines por reto** del reto que hiciste coincide con lo que armaste? ¿Algún componente no funcionó en el pin nuevo? | |
| ¿La **pantalla** más los demás componentes **caben** en el protoboard sin estorbarse? ¿En cuántas columnas? | |
| ¿La pantalla parpadea o la placa se reinicia con el servo y la pantalla juntos (V9)? | |
| ¿Se pudo juntar los sketches sin errores de nombres repetidos? ¿Cuántas veces compiló mal antes de funcionar? | |
| ¿Funciona `Proyecto_plantilla` tal cual (perilla en A0 y LED en el pin 5)? | |
| Pruebas con criterio que escribiste y cuáles pasaron a la primera | |
| ¿Alcanzan 60 minutos para armar la versión mínima? ¿Y 55 para probar y corregir? ¿Y 20 para rearmar al empezar la Sesión 15? | |
| ¿Se entiende la **rúbrica**? ¿Algún criterio es ambiguo? | |
| ¿Alcanzan 50 minutos para seis exhibiciones de 5 + 2 minutos? | |
| Dudas o errores que tuviste | |
| Foto y video del proyecto terminado | |

## Para recompilar o regenerar

- El sketch `Proyecto_plantilla` se verifica con `curso-arduino/compilar-sketches.ps1`, igual que los demás. Los sketches que se juntan en cada reto son los de las sesiones anteriores, **con sus pines tal como están**: al combinarlos, **los equipos cambian los pines que choquen** (tabla de **Pines por reto**).
- Estas Sesiones **no tienen diagrama propio**: cada equipo hace el suyo en la Hoja A. Los diagramas de cada pieza están en las guías de las Sesiones 1 a 13.
- **Verificado el 17 nov:** las tablas de **Pines por reto** se comprobaron armando en código la versión completa de los retos 1 a 6 con esos pines: compilan sin errores ni avisos para Arduino UNO (incluidas las que juntan `Servo` y `LiquidCrystal` o el DHT11 y la pantalla), sin pines repetidos y sin choques de PWM con `tone()` ni `Servo`. Con los pines originales del curso, la barrera del reto 5 chocaba en **cuatro** pines con la pantalla (7, 8, 9 y 12). Esas combinaciones son del instructor y no están en `sketches/`.
- Cosas que **no** están verificadas: que seis proyectos con pantalla quepan en la visita (tiempo de armado), que el PIR, el HC-SR04, el servo y el DHT11 funcionen igual en los pines nuevos (solo cambia la constante, pero no se probó con cables), que la histéresis de 2 °C con el DHT11 baste frente al ruido real, y que los **siete retos** sean los que interesan a los docentes de la prepa. Ninguno de los sketches se ha probado en la placa.
