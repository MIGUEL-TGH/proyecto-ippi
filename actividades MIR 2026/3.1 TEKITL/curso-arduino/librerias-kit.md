# Librerías del kit: cuáles son, dónde están y cómo instalarlas

**Fecha:** 2026-11-16 · **Kit:** REXQualis UNO R3 Complete Starter Kit

## Lo esencial

- Son **7 librerías**. Están como archivos `.zip` en
  `actividades MIR 2026/3.1 TEKITL/kit-arduino/Libraries/`
- **La secuencia principal del curso (sesiones 1 a 13, `curso-arduino/sketches/`) no necesita ninguna.** Estas librerías solo hacen falta para las lecciones del kit que se usan como ampliación o en el proyecto final (código en `kit-arduino/Code/`).
- Las 7 en total pesan **1.1 MB**: caben en una USB para llevarlas a otras computadoras.
- **Estado en la PC de Miguel (17 nov):** ninguna de las 7 está instalada (en `Documentos\Arduino\libraries` solo hay bibliotecas de Adafruit y `DHT sensor library`). La instalación paso a paso, como práctica, está en `preparacion-computadoras.md` (sección 7).

## Las 7 librerías

| # | Archivo (en `kit-arduino/Libraries/`) | Qué maneja | Lección del kit que la usa | Carpeta que crea en el IDE |
|---|---|---|---|---|
| 1 | `HC-SR04.zip` | Sensor de distancia ultrasónico (`SR04.h`) | 11 | `HC-SR04` |
| 2 | `Keypad.zip` | Teclado de membrana 4×4 | 13 | `Keypad` |
| 3 | `IRremote.zip` | Receptor y control remoto infrarrojo | 15 y 16 | `IRremote` |
| 4 | `LedControl.zip` (también existe suelta la carpeta `LedControl/`) | Matriz LED MAX7219 | 22 | `LedControl` |
| 5 | `MPU6050.zip` | Acelerómetro y giroscopio MPU-6050 | 23 | `MPU6050` |
| 6 | `DS3231.zip` | Reloj de tiempo real DS3231 | 26 | `DS3231` |
| 7 | `rfid.zip` | Lector RFID RC522 (`MFRC522.h`, versión 1.1.8) | 29 | `MFRC522` (con otro nombre que el zip) |

Las lecciones 23, 26 y 29 además usan `Wire.h` y `SPI.h`, que **ya vienen con el IDE**.

## Las 3 que NO se instalan

`Servo.zip`, `Stepper.zip` y `LiquidCrystal.zip` están en la misma carpeta, pero **Arduino IDE ya las trae**. Instalarlas duplica la librería y puede dar conflictos. No las copies.

## Cómo instalarlas en otra computadora

### Opción A: desde el IDE (la más sencilla)

1. Copia a la otra computadora los 7 `.zip` de la tabla.
2. Abre Arduino IDE 2.x.
3. `Sketch → Incluir biblioteca → Añadir biblioteca .ZIP…` y elige el primer archivo.
4. Repite con cada uno de los 7.
5. Las librerías quedan en `Documentos\Arduino\libraries\`.

Nota: seis de los siete zip **no traen el archivo `library.properties`** (formato antiguo; solo `rfid.zip` lo trae). Probé la instalación de los siete con el mismo motor que usa el IDE (`arduino-cli` 1.6.0, que viene dentro del IDE), en una carpeta aislada: **los siete se instalan**. No probé el clic en el menú del IDE en sí. Si el IDE rechazara alguno, usa la opción B.

### Opción B: manual (si el IDE rechaza un zip)

1. Descomprime el `.zip`. Dentro hay una carpeta con el nombre de la librería (por ejemplo `Keypad`).
2. Copia **esa carpeta** a `Documentos\Arduino\libraries\` (debe quedar `…\libraries\Keypad\Keypad.h`).
3. Cierra y vuelve a abrir el IDE.

### Cómo comprobar que funcionó

Abre el sketch de la lección que usa la librería y presiona **Verificar** (✓). Si compila, la librería está bien instalada.

| Librería | Sketch para comprobar |
|---|---|
| HC-SR04 | `Code/Lesson 11 Ultrasonic Sensor Module/…` |
| Keypad | `Code/Lesson 13 Membrane Switch Module/…` |
| IRremote | `Code/Lesson 15 IR Receiver Module/…` |
| LedControl | `Code/Lesson 22 MAX7219 LED Dot Matrix Module/…` |
| MPU6050 | `Code/Lesson 23 MPU-6050 Module/…` |
| DS3231 | `Code/Lesson 26 Real Time Clock Module/…` |
| rfid (MFRC522) | `Code/Lesson 29 RC522 RFID Module/…` |

Verificado el 16 nov 2026: instaladas así, las 8 lecciones (11, 13, 15, 16, 22, 23, 26, 29) **compilan** para Arduino UNO.

## Avisos

- **IRremote:** instálala **solo desde el zip del kit**. Es la versión clásica (clases `IRrecv` y `decode_results`). Las versiones nuevas del Gestor de bibliotecas (3.x y 4.x) cambiaron esa API, y los sketches de las lecciones 15 y 16 probablemente no compilarán con ellas (no lo probé). Si ya hay otro IRremote instalado, quítalo antes.
- **Versiones:** salvo `rfid` (1.1.8), los zip no indican versión. Los sketches del kit están hechos para estas copias, por eso conviene usarlas y no las del Gestor de bibliotecas.
- **Compilar no es probar:** que compile confirma que la librería está bien puesta, no que el módulo funcione con la placa.
- **Derechos:** son librerías de terceros y del fabricante. Para uso interno de capacitación no hay problema; antes de difundir el repositorio, revisa que se pueda redistribuir la carpeta `kit-arduino/` (hallazgo H12).
