# Colores institucionales — Marca Gobierno de Puebla 2024-2030

Paleta aprobada para su uso. Transcrita de `COLOR-GOB.jpeg`.

Material de referencia oficial: https://bit.ly/PueblaGamaCromática2024-2030

## Gama cálida (guindas, dorados y neutros claros)

| # | Muestra | CMYK | HEX | RGB |
|---|---------|------|-----|-----|
| 1 | Guinda oscuro | C=35 M=99 Y=54 K=54 | `#5F1B2D` | 95, 27, 45 |
| 2 | Guinda | C=27 M=100 Y=64 K=29 | `#861E34` | 134, 30, 52 |
| 3 | Rojo | C=21 M=100 Y=74 K=15 | `#AF1732` | 175, 23, 50 |
| 4 | Dorado | C=17 M=42 Y=68 K=6 | `#C79B66` | 199, 155, 102 |
| 5 | Arena | C=9 M=30 Y=47 K=1 | `#E2BE96` | 226, 190, 150 |
| 6 | Marfil | C=0 M=0 Y=10 K=0 | `#FFFDED` | 255, 253, 237 |

## Gama fría y neutros (verdes y grises)

| # | Muestra | CMYK | HEX | RGB |
|---|---------|------|-----|-----|
| 7 | Verde oscuro | C=89 M=51 Y=65 K=68 | `#0E312D` | 14, 49, 45 |
| 8 | Verde bosque | C=82 M=34 Y=60 K=35 | `#216358` | 33, 99, 88 |
| 9 | Verde jade | C=74 M=17 Y=55 K=2 | `#3D9B84` | 60, 155, 133 |
| 10 | Gris oscuro | C=63 M=54 Y=51 K=52 | `#484747` | 72, 71, 71 |
| 11 | Gris medio | C=0 M=0 Y=0 K=40 1 | `#B2B2B1` | 179, 178, 178 |
| 12 | Gris claro | C=0 M=0 Y=0 K=10 1 | `#ECECEC` | 236, 236, 236 |

## Variables CSS

```css
:root {
  --puebla-guinda-oscuro: #5F1B2D;
  --puebla-guinda: #861E34;
  --puebla-rojo: #AF1732;
  --puebla-dorado: #C79B66;
  --puebla-arena: #E2BE96;
  --puebla-marfil: #FFFDED;
  --puebla-verde-oscuro: #0E312D;
  --puebla-verde-bosque: #216358;
  --puebla-verde-jade: #3D9B84;
  --puebla-gris-oscuro: #484747;
  --puebla-gris-medio: #B2B2B1;
  --puebla-gris-claro: #ECECEC;
}
```

## Notas de transcripción

Los nombres de las muestras (Guinda, Dorado, etc.) son descriptivos y no vienen en la imagen. Algunos valores de la imagen no coinciden entre sí. Se resolvieron así:

- **#3 Rojo:** la imagen dice HEX `cf 17 31`, pero RGB 175, 23, 50 equivale a `#AF1732`. Se usó el valor RGB.
- **#6 Marfil:** el RGB aparece cortado ("255 253 23"). Se usó 237 según el HEX `ff fd ed`.
- **#7 Verde oscuro:** el HEX aparece como `c 31 2d`, que se leyó como `#0E312D` según RGB 14, 49, 45.
- **#8 Verde bosque:** la imagen dice HEX `24 62 57` y RGB 33, 99, 88 (`#216358`). Se usó el RGB. Conviene confirmarlo con el material oficial.
- **#9 y #11:** hay diferencias de ±1 entre HEX y RGB. Se conservó el HEX impreso en #9 y el RGB en #11 solo en la columna RGB.
- **#11 y #12:** el CMYK incluye un "1" suelto tras K, tal como aparece en la imagen.

Ante cualquier duda, el enlace oficial prevalece sobre esta transcripción.
