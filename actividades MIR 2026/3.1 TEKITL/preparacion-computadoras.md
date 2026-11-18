# Preparación de las computadoras del aula

**Destino:** curso de Electrónica y programación con Arduino, San Juan Atzingo, San Gabriel Chilac, Puebla
**Fecha:** 2026-11-17 · **Escrito para:** Miguel, como instructor. Sirve de lista de verificación y de práctica: se puede seguir tal cual en cada computadora.
**Relacionado:** `plan-curso-arduino.md` (sección 7, «Organización con 6 kits») · `hallazgos-ajuste-curso.md` (H9) · `curso-arduino/librerias-kit.md` · `curso-arduino/compilar-sketches.ps1`

## 1. Resumen

- Cada computadora necesita **cuatro cosas**: Arduino IDE 2.x, el núcleo **Arduino AVR Boards 1.8.8**, las bibliotecas integradas **Servo** y **LiquidCrystal**, y la carpeta con los **sketches del curso**. Nada más: la secuencia principal no usa bibliotecas externas ni internet (sesiones 1 a 13 y proyecto final).
- **Esta PC ya cumple todo** (sección 3). Falta solo, y solo para las ampliaciones, instalar las **7 bibliotecas del kit**: sirve como tu práctica (sección 7).
- Si en el aula **no hay internet**, no se puede instalar el núcleo desde el Gestor de placas. Se resuelve copiando **336 MB** desde esta PC (sección 5). Esa copia se **probó** con `arduino-cli` en una carpeta aislada: compila sin descargar nada.
- **Lo que falta saber de las 6 computadoras de la escuela:** versión de Windows (el IDE 2.x pide Windows 10 o 11 de 64 bits), si hay permisos para instalar programas y si hay internet. Conviene preguntarlo antes de ir.

## 2. Qué necesita cada computadora

| Requisito | Detalle |
|---|---|
| Sistema | Windows 10 u 11, **64 bits**. No sirve Windows 7 ni 8, ni un sistema de 32 bits |
| Espacio libre | **2 GB** recomendados (el IDE ocupa 548 MB; el núcleo AVR y sus herramientas, 252 MB; las herramientas de apoyo, 22 MB; los sketches, menos de 1 MB) |
| Un puerto USB libre | Para el cable USB del kit (A–B) |
| Arduino IDE | **2.x** (en tu PC, la 2.3.11). Instalación «solo para mí»; es la misma carpeta `%LOCALAPPDATA%\Programs\Arduino IDE` de tu PC |
| Núcleo de placa | **Arduino AVR Boards 1.8.8** (para la Arduino UNO R3) |
| Bibliotecas | **Servo** y **LiquidCrystal**, que traen el IDE y el núcleo. **No** se instalan los zip `Servo`, `Stepper` ni `LiquidCrystal` de `kit-arduino/Libraries/` (duplican la biblioteca; ver `librerias-kit.md`) |
| Sketches | La carpeta `curso-arduino/sketches/` (66 sketches), copiada a cada computadora |
| Internet | **No** hace falta durante el curso. Solo para instalar, y se evita con la sección 5 |

## 3. Revisión de este equipo (17 nov 2026)

| Qué se revisó | Resultado |
|---|---|
| Windows | ✔ Windows 10 Pro (10.0.19045), 64 bits |
| Arduino IDE | ✔ 2.3.11, instalado por usuario en `%LOCALAPPDATA%\Programs\Arduino IDE` |
| `arduino-cli` incluido | ✔ 1.6.0 (el que usa `compilar-sketches.ps1`) |
| Núcleo `arduino:avr` | ✔ 1.8.8. También está `esp32:esp32` 3.3.12 (el curso no lo usa) |
| Bibliotecas **Servo** y **LiquidCrystal** | ✔ en `%LOCALAPPDATA%\Arduino15\libraries` (junto con Stepper, SD, Ethernet, Firmata, TFT, Keyboard y Mouse) |
| Bibliotecas externas que pide la secuencia principal | ✔ ninguna |
| Los 66 sketches del curso | ✔ compilan para Arduino UNO sin errores ni avisos (script `compilar-sketches.ps1`) |
| Las **7 bibliotecas del kit** (HC-SR04, Keypad, IRremote, LedControl, MPU6050, DS3231, rfid) | ✘ **no están instaladas.** En `Documentos\Arduino\libraries` solo hay bibliotecas de Adafruit y `DHT sensor library`. Solo hacen falta para las **ampliaciones** (sección 7) |
| `DHT sensor library` (Adafruit) 1.4.7 | ℹ está instalada, pero el curso **no la usa** (el DHT11 se lee con código propio). No estorba |
| Placa del kit | ℹ **no había una placa Arduino conectada** al hacer la revisión (Windows solo mostraba puertos Bluetooth, del chip Intel y dispositivos desconectados). Por eso **no se probó subir un programa** |

## 4. Preparar una computadora **con** internet

Tiempo estimado: 15 a 20 minutos. Anota el real en la sección 12.

1. **Conseguir el instalador.** Ya está descargado en esta PC: `C:\Users\MTGH\Downloads\arduino\arduino-ide_2.3.11_Windows_64bit.exe` (153 MB, versión **2.3.11**, la misma que tienes instalada). Cópialo a una memoria USB: es el mismo para las 6 computadoras, así todas quedan con la misma versión y no hay que descargarlo seis veces. Si algún día lo necesitas de nuevo, la página es `https://www.arduino.cc/en/software` (elige «Windows, 64 bits»). **No hace falta instalar `arduino-cli` aparte:** el IDE ya lo trae dentro.
2. **Instalar** «solo para mí» (la opción que trae por omisión). Si Windows pregunta si confías en el software de «Arduino», acepta. **No instales «drivethelife»** ni otro programa de drivers que sugiera el PDF del fabricante (`revision-kit-arduino.md`, F7).
3. **Abrir el IDE.** Si pide actualizar, **no lo aceptes** (se queda la misma versión en las 6 computadoras).
4. **Núcleo AVR:** `Herramientas → Placa → Gestor de placas…`, busca «Arduino AVR Boards» y comprueba que diga **instalado, 1.8.8**. Si no lo está, instálalo. *(No pude observar en una computadora limpia si el IDE lo instala solo en el primer arranque: anótalo en la sección 12.)*
5. **Bibliotecas integradas:** abre `Sketch → Incluir biblioteca` y comprueba que aparezcan **Servo** y **LiquidCrystal**. Si faltan, `Sketch → Incluir biblioteca → Administrar bibliotecas…`, busca «Servo» (de Arduino) y «LiquidCrystal» (de Arduino, Adafruit) e instálalas.
6. **Conectar la placa** con el cable USB. Elige `Herramientas → Placa → Arduino AVR Boards → Arduino Uno` y `Herramientas → Puerto → COMx (Arduino Uno)`.
7. Sigue con la sección 6 (copiar los sketches) y la 8 (prueba).

**Driver USB.** En Windows 10 y 11 la placa suele aparecer sola, sin instalar nada (como «Dispositivo serie USB» o «Arduino Uno» en `Puertos (COM y LPT)` del Administrador de dispositivos). Si en vez de eso aparece como dispositivo desconocido o con un signo de exclamación amarillo, instala el driver a mano: Administrador de dispositivos → clic derecho en el dispositivo → *Actualizar controlador* → *Buscar controladores en este equipo* → elige la carpeta `%LOCALAPPDATA%\Arduino15\packages\arduino\hardware\avr\1.8.8\drivers` (con «incluir subcarpetas»). Esa carpeta viaja con la copia de la sección 5.

## 5. Preparar una computadora **sin** internet

La idea: instalar el IDE desde el instalador guardado en la USB y, aparte, **copiar a la nueva computadora el núcleo AVR y las bibliotecas integradas** desde esta PC. **No copies toda `%LOCALAPPDATA%\Arduino15`**: pesa 8.8 GB (incluye 2 GB de descargas viejas y el soporte de ESP32) y contiene `inventory.yaml`, con un identificador de tu instalación.

**Qué se copia (336 MB):**

| Carpeta o archivo de `%LOCALAPPDATA%\Arduino15` | Tamaño | Para qué |
|---|---|---|
| `packages\arduino` | 252 MB | núcleo AVR 1.8.8 y sus herramientas (compilador `avr-gcc`, `avrdude` para subir, drivers) |
| `packages\builtin` | 22 MB | herramientas de apoyo del IDE (monitor serie, detección de puertos) |
| `libraries` | 3.3 MB | Servo, LiquidCrystal y las demás bibliotecas integradas |
| `package_index.json`, `package_index.json.sig`, `library_index.json`, `library_index.json.sig` | unos 60 MB | los índices; sin ellos el IDE intenta descargarlos |

**En esta PC (con la USB como unidad `E:`; cambia la letra por la tuya):**

```powershell
$origen  = "$env:LOCALAPPDATA\Arduino15"
$destino = "E:\ArduinoOffline\Arduino15"
New-Item -ItemType Directory -Force $destino | Out-Null
robocopy "$origen\packages\arduino"  "$destino\packages\arduino"  /E
robocopy "$origen\packages\builtin"  "$destino\packages\builtin"  /E
robocopy "$origen\libraries"         "$destino\libraries"         /E
Copy-Item "$origen\package_index.json", "$origen\package_index.json.sig", "$origen\library_index.json", "$origen\library_index.json.sig" $destino
```

(`robocopy` devuelve un código de salida de 0 a 7 cuando todo salió bien; no es un error.)

**En cada computadora nueva:**

1. Instala el IDE con el instalador de la USB (`arduino-ide_2.3.11_Windows_64bit.exe`; sección 4, pasos 1 y 2). **Ábrelo una vez y ciérralo:** así se crea `%LOCALAPPDATA%\Arduino15`.
2. Copia **el contenido** de `E:\ArduinoOffline\Arduino15` dentro de `%LOCALAPPDATA%\Arduino15`:

   ```powershell
   robocopy "E:\ArduinoOffline\Arduino15" "$env:LOCALAPPDATA\Arduino15" /E
   ```
3. Abre el IDE y haz los pasos 4, 5 y 6 de la sección 4. El Gestor de placas debe decir «Arduino AVR Boards **1.8.8** instalado». Si no hay internet, el IDE puede mostrar avisos rojos al buscar actualizaciones: se ignoran.

**Cómo se probó.** Se armó esta misma copia en una carpeta aislada y se dejó que `arduino-cli` viera **solo esa carpeta** (con caché vacío). Resultado: `core list` mostró `arduino:avr 1.8.8` instalado **sin descargar nada**, y compilaron `P02_led_parpadeo`, `P13_servo_barrido` (Servo), `P21_lcd_hola` (LiquidCrystal) y `P20_dht11`. **Sin `packages\builtin`** (primer intento), el CLI volvió a descargar cinco herramientas de apoyo: por eso se incluye. **No se probó** con el IDE gráfico en otra computadora ni subiendo a la placa: es parte de tu práctica.

## 6. Copiar los sketches del curso

Los alumnos **abren** los sketches, no los teclean (plan, sección 7). Se copian a cada computadora de antemano.

```powershell
# Desde la carpeta del repositorio (o desde la USB, si ahí guardaste una copia de curso-arduino\sketches)
$origen  = ".\actividades MIR 2026\3.1 TEKITL\curso-arduino\sketches"
$destino = "$env:USERPROFILE\Documents\Arduino\curso"
robocopy $origen $destino /E
```

- Quedan 66 carpetas `P02_…`, `X01_…`, `Proyecto_plantilla`, etc., cada una con **un solo `.ino` del mismo nombre** (es lo que pide el IDE). Si alguien guarda otro `.ino` dentro de una de esas carpetas, el IDE da el error `redefinition of …`; la regla de las guías es **«Guardar como…» y un nombre nuevo** para las copias propias.
- Las carpetas de **«solución del instructor»** (P02_SOS, P06_semaforo_con_boton, P08_alarma_completa…) quedan mezcladas con las demás. Varias se reutilizan en el proyecto final, así que conviene copiarlas todas. Si prefieres no mostrarlas antes de tiempo, copia por visita (visita 1: `P02`–`P08`; visita 2: `P09`–`P16`; visita 3: `P17`–`P23`; visita 4: `P24`, `P25`, `X01`, `X02` y `Proyecto_plantilla`). `robocopy` no borra nada: se puede volver a correr en cada visita.
- **En cada regreso** se confirma que la carpeta sigue ahí (plan, sección 3b).

## 7. Bibliotecas del kit (opcionales): tu práctica

**Cuándo hacen falta.** Solo para las **ampliaciones** de equipos adelantados y del proyecto final (alarma de gas, RFID, reloj RTC, matriz LED, joystick, control remoto IR, motor a pasos; lista en `S14-16-proyecto-final.md`). La secuencia principal **no** las necesita. **En esta PC ninguna de las 7 está instalada**, así que puedes practicar la instalación aquí.

| # | Archivo (en `kit-arduino/Libraries/`) | Lección del kit que la usa | Sketch para comprobar |
|---|---|---|---|
| 1 | `HC-SR04.zip` | 11 | `Code/Lesson 11 Ultrasonic Sensor Module/…` |
| 2 | `Keypad.zip` | 13 | `Code/Lesson 13 Membrane Switch Module/…` |
| 3 | `IRremote.zip` | 15 y 16 | `Code/Lesson 15 IR Receiver Module/…` |
| 4 | `LedControl.zip` | 22 | `Code/Lesson 22 MAX7219 LED Dot Matrix Module/…` |
| 5 | `MPU6050.zip` | 23 | `Code/Lesson 23 MPU-6050 Module/…` |
| 6 | `DS3231.zip` | 26 | `Code/Lesson 26 Real Time Clock Module/…` |
| 7 | `rfid.zip` | 29 | `Code/Lesson 29 RC522 RFID Module/…` |

**Opción A, desde el IDE** (la más sencilla): `Sketch → Incluir biblioteca → Añadir biblioteca .ZIP…` y eliges cada archivo (7 veces). Quedan en `Documentos\Arduino\libraries`.

**Opción B, a mano** (si el IDE rechaza algún zip; seis de los siete no traen `library.properties`):

```powershell
$zips = "HC-SR04","Keypad","IRremote","LedControl","MPU6050","DS3231","rfid"
$libs = "$env:USERPROFILE\Documents\Arduino\libraries"
foreach ($z in $zips) {
    Expand-Archive -Path ".\actividades MIR 2026\3.1 TEKITL\kit-arduino\Libraries\$z.zip" -DestinationPath $libs
}
```

Cada zip trae una sola carpeta de primer nivel con el nombre de la biblioteca (se comprobó: `HC-SR04`, `Keypad`, `IRremote`, `LedControl`, `MPU6050`, `DS3231` y `rfid`), así que quedan en su lugar. **Cierra y vuelve a abrir el IDE.** La de RFID queda en una carpeta llamada `rfid`; con la opción A el IDE la nombra `MFRC522`. Da igual para compilar.

**Cuidado:**
- **IRremote:** instálala **solo desde el zip del kit** (es la versión clásica; las versiones 3.x y 4.x del Gestor de bibliotecas cambiaron la API y los sketches de las lecciones 15 y 16 probablemente no compilarían). Si ya hay otro IRremote, quítalo antes.
- **No instales** `Servo.zip`, `Stepper.zip` ni `LiquidCrystal.zip` del kit.
- Que compile **no prueba** que el módulo funcione con la placa.

**Cómo comprobar:** abre el sketch de la lección y presiona **Verificar** (✓). El 16 nov se verificó que las 8 lecciones (11, 13, 15, 16, 22, 23, 26 y 29) compilan con estas bibliotecas instaladas.

## 8. Prueba de 10 minutos por computadora

Hazla en **cada** computadora antes del primer día. Marca la hoja de la sección 9.

1. `Archivo → Ejemplos → 01.Basics → Blink` → **Subir**. Debe parpadear el LED «L» de la placa (comprueba placa, cable, puerto, driver y núcleo).
2. Abre `Documentos\Arduino\curso\P02_led_parpadeo\P02_led_parpadeo.ino` → **Verificar**. Debe decir «Compilado» sin errores.
3. Abre `P13_servo_barrido` → **Verificar** (usa `Servo`).
4. Abre `P21_lcd_hola` → **Verificar** (usa `LiquidCrystal`).
5. Abre `P09_perilla_serie` → **Subir** → `Herramientas → Monitor Serie` a **9600 baudios**. Deben aparecer números (con el cable de la perilla conectado o suelto; basta con que escriba algo).
6. *(Opcional, si copiaste el repositorio a esa computadora)* en PowerShell, desde `curso-arduino`: `.\compilar-sketches.ps1 -Filtro "P02*"`. Debe terminar con `Con error: 0`. Sin filtro compila los 66 (varios minutos la primera vez).

## 9. Hoja de verificación (una columna por computadora)

| Comprobación | PC 1 | PC 2 | PC 3 | PC 4 | PC 5 | PC 6 |
|---|---|---|---|---|---|---|
| Windows 10 u 11, 64 bits | | | | | | |
| Arduino IDE 2.x instalado (misma versión en todas: ______) | | | | | | |
| Núcleo «Arduino AVR Boards 1.8.8» instalado | | | | | | |
| Aparecen `Servo` y `LiquidCrystal` en Incluir biblioteca | | | | | | |
| La placa aparece en un puerto COM | | | | | | |
| Blink sube y el LED «L» parpadea | | | | | | |
| `P13_servo_barrido` y `P21_lcd_hola` se verifican | | | | | | |
| Carpeta `Documentos\Arduino\curso` con los 66 sketches | | | | | | |
| Monitor Serie a 9600 muestra números (P09) | | | | | | |
| Actualizaciones del IDE ignoradas | | | | | | |

## 10. Si algo falla

| Síntoma | Qué revisar |
|---|---|
| `Servo.h: No such file or directory` o `LiquidCrystal.h: …` | Faltan las bibliotecas integradas: repite el paso 5 de la sección 4, o copia `libraries` como en la sección 5 |
| `Arduino AVR Boards` no aparece como instalado, o falla `avr-gcc` | Falta el núcleo: instálalo desde el Gestor de placas (con internet) o copia `packages\arduino` (sección 5) |
| No aparece ningún puerto COM | Prueba otro cable y otro puerto USB; revisa el Administrador de dispositivos; instala el driver a mano (sección 4, «Driver USB») |
| `avrdude: stk500_getsync(): not in sync` al subir | Placa o puerto equivocados: `Herramientas → Placa → Arduino Uno` y el puerto correcto |
| `redefinition of …` al verificar | Hay dos `.ino` en la misma carpeta; deja uno solo (regla de las guías) |
| El IDE insiste en actualizar | Ignora el aviso. No actualices a media serie de visitas |
| `compilar-sketches.ps1` no corre («la ejecución de scripts está deshabilitada») | Ábrelo con `powershell -NoProfile -ExecutionPolicy Bypass -File .\compilar-sketches.ps1` |

## 11. Qué se verificó y qué no

**Verificado el 17 nov, en esta PC:** versiones del IDE, de `arduino-cli` y del núcleo; presencia de Servo y LiquidCrystal; ausencia de las 7 bibliotecas del kit; compilación de los 66 sketches; la copia de 336 MB (compila sin descargar nada, con `arduino-cli` en una carpeta aislada); la estructura de los 7 zip de bibliotecas.

**No verificado (queda para tu práctica):**
- El IDE gráfico y la subida a la placa en otra computadora (no había placa conectada y solo hay una instalación).
- Si el instalador del IDE instala solo el núcleo AVR y las bibliotecas integradas en el primer arranque, y si pide permisos de administrador en las computadoras de la escuela.
- El driver USB de la placa del kit en esas computadoras (la hoja de datos del kit menciona el chip ATmega16U2; en Windows 10 y 11 normalmente no hace falta instalar nada).
- La versión de Windows, los permisos y el internet de las 6 computadoras del aula.

**Para practicar en esta misma PC sin tocar tu instalación:** crea otra cuenta de usuario de Windows (cada cuenta tiene su propia carpeta `%LOCALAPPDATA%`) y sigue la sección 4 o la 5 desde cero. O úsala en una computadora que no tenga el IDE.

## 12. Tu práctica: anota lo que encuentres

| Dato | Anota aquí |
|---|---|
| Computadora y versión de Windows | |
| Tiempo real de instalar el IDE (sección 4, pasos 1 a 3) | |
| ¿El IDE instaló solo el núcleo AVR y las bibliotecas en el primer arranque? ¿Pidió internet? | |
| ¿Pidió permisos de administrador? ¿En qué paso? | |
| ¿La placa apareció sola en un puerto COM? ¿Hubo que instalar el driver a mano? | |
| Tiempo real de la copia sin internet (sección 5) y si el Gestor de placas mostró «1.8.8 instalado» | |
| ¿Blink subió y parpadeó el LED «L»? | |
| ¿Se verificaron `P13_servo_barrido` y `P21_lcd_hola`? | |
| Instalación de las 7 bibliotecas del kit: ¿opción A o B? ¿Alguna falló? ¿Compilaron las 8 lecciones? | |
| Tiempo total para dejar **una** computadora lista (con la prueba de la sección 8) | |
| Dudas o errores que tuviste | |
