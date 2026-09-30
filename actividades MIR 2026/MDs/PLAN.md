# Plan de conversión PDF → Markdown (actividades MIR 2026)

## Diagnóstico
- Los 11 PDFs son **escaneos** (cada página = imagen, 0 caracteres de texto) y no hay Tesseract/OCR instalado.
- Método: renderizar cada página a PNG (PyMuPDF, 110 dpi) en una carpeta temporal, leerla visualmente y transcribirla a Markdown.
- Total: 479 páginas → 96 lotes de 5 páginas.

## Reglas de trabajo
1. Un PDF a la vez, en el orden de la tabla.
2. Por PDF: lotes de 5 páginas (p. 1-5, 6-10, …). Tras cada lote se **anexa** al `.md` con un encabezado `<!-- Páginas X-Y -->`.
3. Salida: `MDs/<nombre del pdf>.md`, con encabezado (título, archivo origen, nº de páginas).
4. Transcripción fiel: títulos (`#`), listas, tablas en Markdown; imágenes/logos/firmas como `[Imagen: descripción]`; texto ilegible como `[ilegible]`.
5. Al terminar cada PDF se marca la casilla y se revisa antes de pasar al siguiente.

## Orden y avance

| # | PDF | Págs | Lotes | Estado |
|---|-----|------|-------|--------|
| 1 | 1.1 Tekitl Digital | 9 | 2 | [x] completo (2/2) |
| 2 | 1.2 Intercambio Digital | 12 | 3 | [x] completo (3/3) |
| 3 | 1.3 Base de datos Intercambio Digital | 47 | 10 | [!] págs 1-2 hechas; págs 3-47 son tablas ilegibles (pendiente decisión) |
| 4 | 1.4 Intercambio Digital Dir. Policia Turistica | 38 | 8 | [x] completo (8/8) |
| 5 | 1.5 Intercambio Digital Colaboracion Proyectos Estrategicos | 15 | 3 | [x] completo (3/3) |
| 6 | 1er Trim E088 DESARROLLO INTEGRAL DE LOS PUEBLOS INDIGENAS | 131 | 27 | [x] completo (págs 1-10 leídas; págs 11-131 = copia de 1.1-1.5, ensambladas; págs 34-78 ilegibles como en 1.3) |
| 7 | 1er Trimestre 2026 | 10 | 2 | [x] completo (2/2) |
| 8 | 2.1 PADI | 66 | 14 | [x] completo (14/14; el último lote cubrió págs 61-66) |
| 9 | 2.2 Altepetl | 27 | 6 | [x] completo (6/6) |
| 10 | 2do Trim SDTI_260710_134815 | 116 | 24 | [x] completo (compilado de 2do Trimestre + 2.1 PADI + 2.2 Altepetl, verificado por imagen; 15 págs. en blanco) |
| 11 | 2do Trimestre 2026 | 8 | 2 | [x] completo (2/2) |

Se sugiere empezar por los más cortos (1.1, 1er Trimestre 2026, 2do Trimestre 2026) y dejar para el final los de 100+ páginas (#6 y #10).




