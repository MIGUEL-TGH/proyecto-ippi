# Presentación del curso de Arduino

**Archivo:** `Curso-Arduino-presentacion.pptx` (16:9 de 20 × 11.25 pulgadas, con la plantilla institucional `../../cursos-arduino.pptx`).
Sale de las guías de `../guias/` por medio de un programa; **no se edita a mano la sesión completa**: se corrige la guía y se vuelve a generar.

## Cómo está organizada
- **573 láminas en 19 secciones de PowerPoint** (panel de secciones o vista Clasificador de diapositivas): presentación, Sesión 1 a 13, proyecto final (reglas, retos y pines), Sesión 14, 15 y 16, cierre.
- Cada sesión: portada, plan de tiempos, materiales, ideas de la sesión y, por práctica: de qué se trata, diagrama de conexiones, pasos de armado junto al diagrama del protoboard, lista de revisión, código, qué debes ver, explora, retos, rompe y arregla, si no funciona y evidencia para la bitácora.
- **Notas del orador:** cada lámina trae el texto completo de su sección de la guía. Lo que es solo para quien imparte (soluciones de los retos, claves de validación V1 a V16, pendientes) **no sale en la lámina**: está en las notas, bajo «(Solo instructor)».
- Letra: 20 pt o más en tablas y 22 pt o más en textos corridos; si no cabe, se reparte en otra lámina (nunca se encoge más).
- Fuentes que debe tener la computadora donde se proyecte: **Gilroy, Montserrat y Consolas** (las mismas de la plantilla).

## Cómo regenerarla
```
python construye.py            (todo el curso; unos 20 segundos)
python construye.py S06 S07    (solo esas sesiones, para probar; escribe ...-prueba.pptx)
.\verifica.ps1                 (revisa con PowerPoint que ningún texto se salga de su cuadro)
.\verifica.ps1 -Imagenes .\imagenes   (además exporta cada lámina a PNG)
```
Hace falta Python con `python-pptx`, `Pillow` y `lxml`.

## Archivos
| Archivo | Para qué sirve |
|---|---|
| `construye.py` | Convierte cada guía en láminas (reglas por tipo de bloque y de sección) |
| `proyecto_final.py` | Composición propia de la guía de las Sesiones 14 a 16 (hojas A a D, banco de retos, mapas de pines) |
| `pptx_base.py` | Medición de texto con las fuentes reales, formas, tablas, paneles de código, marcos de la plantilla, notas y secciones |
| `md_guias.py` | Lee el Markdown de las guías |
| `verifica.ps1`, `qa_texto.py` | Comprobación con PowerPoint |

## Límites que conviene saber
- Los diagramas son los PNG de las guías, hechos para hoja impresa: se muestran lo más grandes posible, pero sus rótulos finos se leen pequeños al proyectar. Los pasos de armado van en tarjetas junto al diagrama justamente para no depender de esos rótulos.
- La portada y el pie (nombre de la subdirección, localidad, «16 sesiones de 2 horas · kit Arduino UNO R3») son texto propio; no hay fecha ni nombre de quien imparte.
- No se ha proyectado en el salón ni se ha probado en otra computadora.
