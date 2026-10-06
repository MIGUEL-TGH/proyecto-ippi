# Plan de trabajo — Word del 3er Trimestre 2026 (E088, Act. 3.9)

Archivo destino: `3er Trim E088 DESARROLLO INTEGRAL DE LOS PUEBLOS INDIGENAS.docx`
Fuente de texto: `3er Trimestre SDTI 2026 - Borrador.md` (v2) · Contexto: `NOTAS-Q3-TEKITL.md`
Creado: 2026-10-05. Este archivo es la bitácora de control de cambios: se actualiza al cerrar cada paso.

---

## 1. Diagnóstico del Word (estado al 2026-10-05)

| Elemento | Estado |
|---|---|
| Página 1: portada | Hecha |
| Página 2: cuadro resumen | No va en el Word (es el Excel `Formato Cuadro resumen_Variable 1.xlsx`, hoja "3er Trim E088", que se imprime y se anexa) |
| Página 3: justificación | Hecha (4 párrafos, Gilroy, justificado, interlineado 1.15, 10 pt posterior) |
| Portada del informe anual | Hecha, una sola vez. Responsable: Miguel Trinidad Gómez Hernández, Encargado de Despacho; "Heroica Puebla de Zaragoza, Octubre de 2026."; ejercicio fiscal 2026 |
| I. Presentación | **Falta** (objeto de este plan) |
| II, III, IV y Relación de evidencia | Faltan (pasos posteriores) |

**Hallazgos técnicos del archivo** (importan para insertar sin romper el diseño):
- Una sola sección, carta (21.59 × 27.94 cm), márgenes 3.0 / 2.5 cm. Encabezado con imagen (`image1.jpeg`) y pie "Tel. 222 279 9605".
- **El salto entre páginas se hace con ~28 párrafos vacíos** (entre la justificación y la portada anual) y ~8 más dentro de la portada. Solo un párrafo tiene `pageBreakBefore`. Es frágil: cualquier cambio de texto antes de la portada la desplaza. Hay que **no tocar esos vacíos** y empezar la Presentación con un salto de página real (`pageBreakBefore`) después del último párrafo de la portada anual.
- Hay un párrafo vacío final (índice 60) antes del `sectPr`; la Presentación entra después de él o lo reemplaza.
- Fuente del cuerpo: **Gilroy**. Las corridas de la portada anual no declaran fuente (heredan el default). Al final hay que confirmar que Gilroy esté instalada en el equipo donde se imprime/convierte a PDF; si no, la paginación cambia.
- Q1 y Q2 imprimieron "2025" por error. Aquí ya se corrigió a 2026; no repetir.

## 2. Referencia: cómo fue la Presentación en Q1 y Q2

Estructura constante, **4 párrafos** en una hoja:
1. Qué es el informe + los dos proyectos del trimestre (como "pilares/eslabones").
2. Problema (brecha digital como exclusión histórica) + giro de enfoque (de asistencialismo a autodeterminación y soberanía tecnológica; Humanismo Mexicano, *Yeknemilis*).
3. Fundamento jurídico (Art. 13 constitucional, Sujetos de Derecho Público) + qué instrumenta cada proyecto.
4. "Resultado que se entrega" (ingeniería de proyecto de ejecución inmediata) + custodia pública.

El borrador v2 de Q3 ya sigue esa forma pero con **3 párrafos**.

## 3. Texto propuesto para I. Presentación (ajustes sobre el borrador v2)

Se conserva la estructura y la voz de Q1/Q2, pero se corrigen puntos que no se sostienen con la evidencia actual:

| Frase del borrador | Problema | Ajuste |
|---|---|---|
| "infraestructura física comunitaria" | El NODO está en el edificio del IPPI y aún no recibe visitas; no es comunitario hoy | "infraestructura física institucional de vocación comunitaria" |
| "cursos documentados y **listos para impartirse**" | El manual tiene respuestas en blanco y restos de LaTeX; lista de materiales incompleta; falta paquete EC0217.01 del curso de secundaria | "materiales formativos **preparados**, con primera impartición programada el 25 y 26 de nov." |
| "infraestructura instalada y probada" | Las capturas de pruebas son del 02/10 (fuera del trimestre) | Mantener solo si Miguel confirma fecha de instalación; si no, "instalada en el trimestre y probada a inicios de octubre" |
| "primera infraestructura física instalada" | Correcto como primera etapa, pero puede leerse como NODO completo | "primera etapa física del NODO (zonas de producción y sala de capacitación)" |
| Falta mencionar que Q1/Q2 fueron ingeniería de escritorio | Es el hilo narrativo ya usado en la justificación | Agregar una oración de continuidad en el párrafo 1 |

Esquema de los 4 párrafos:
1. Informe, periodo (3er trimestre) y los dos proyectos: TEKITL y NODO. Continuidad: de la ingeniería de proyecto (Q1–Q2) a formación técnica y primera etapa física.
2. Brecha digital: no es solo acceso; incluye no saber cómo funciona, se repara y se reutiliza la tecnología, y no poder producir contenido propio. Principios: Soberanía Tecnológica y *Yeknemilis*.
3. Fundamento: Art. 13 (Sujetos de Derecho Público), y qué instrumenta cada proyecto (TEKITL: comprensión del hardware y reaprovechamiento de residuos; NODO: producción de contenidos en lenguas originarias y formación de promotores).
4. Resultado que se entrega, con alcance honesto: materiales preparados, primera etapa instalada, sin cursos impartidos ni visitas; custodia pública del IPPI.

> El texto final se redacta y se muestra a Miguel **antes** de escribirlo en el Word (paso B).

## 4. Plan de ejecución

Orden pensado para no perder trabajo y poder revertir.

| # | Paso | Detalle | Estado |
|---|---|---|---|
| A | Respaldo | Copiar el docx a `_respaldos/` con fecha-hora antes de cada ronda de edición (el docx pesa ~6.5 MB; los respaldos no se suben a git: agregarlos a `.gitignore` si hace falta) | Hecho 2026-10-06 |
| B | Redactar I. Presentación | 4 párrafos según §3; revisión de Miguel en chat antes de tocar el Word | Hecho 2026-10-06 (aprobado por Miguel) |
| C | Insertar en el Word | python-docx: nuevo párrafo "I. PRESENTACIÓN" con el formato del encabezado "1. DESCRIPCIÓN DE LA JUSTIFICACIÓN" (Gilroy 12 pt, negrita) con `pageBreakBefore`; 4 párrafos de cuerpo clonando el formato de los de la justificación (justificado, 1.15, Gilroy). No modificar nada anterior | Hecho 2026-10-06 |
| D | Verificar | Convertir a PDF y revisar: Presentación en una sola hoja, sin desplazar portada anual ni justificación, encabezado y pie correctos, número total de páginas | Hecho 2026-10-06 (ver nota) |
| E | Marcar pendientes en el documento | Cualquier dato sin confirmar (fecha de instalación NODO) se deja en texto neutro, no inventado; el listado vive en §5 | Hecho: nada que marcar en la Presentación |
| F | Commit | Lo hace Miguel (convención del repo: `AAAA-MM-DD-HHMM[am/pm]`) | Pendiente |

Pasos siguientes (cada uno repite A→F): II. Resultados alcanzados · III. Acciones realizadas · IV. Conclusiones y relación de evidencia (A–K).

## 5. Decisiones y datos que necesito de Miguel

Bloquean o afectan la Presentación:
1. **Fecha de instalación del NODO.** El borrador pone 14/09/2026 pero las capturas son del 02/10 y las fotos de Zona 4 del 04/10. ¿Hubo evidencia previa al 30/09?
2. **Formulación aceptada para "preparado" vs. "listo"** (ver §3).
3. **Si se menciona la sala de capacitación (Zona 4) como instalada en el trimestre**, dado que sus fotos son posteriores al corte.

No bloquean la Presentación, pero se necesitarán después:
4. Acciones de julio y agosto con fechas.
5. Realizado de septiembre (el Excel dice 2) y BR12 (meta al corte) vacía; debe ser 6.
6. Versión vigente del documento NODO (3 vs. 3 (2)) y del curso (original vs. V2).
7. Permiso para usar fotos donde aparece personal.
8. Quién elabora y quién valida: el Word pone a Miguel como responsable; el Excel pone como elaboró a Luis Antonio Molina Saldaña y como validó a Miguel; el borrador md decía Directora General.
9. Eliminar o excluir fotos duplicadas Zona 4.4, 4.5, 4.6.

### Respuestas de Miguel (2026-10-06)
1. NODO: espacio abierto al público, de uso bajo supervisión y participación del personal del IPPI. Redacción: "infraestructura física institucional de vocación comunitaria".
2. Instalación del NODO: **14/09/2026**, sin fotos de esa fecha. Pruebas y registro fotográfico: inicios de octubre (02 y 04/10). Se redacta así.
3. "Preparados" en lugar de "listos": aprobado.
4. Zona 4 (sala de capacitación) se menciona como instalada en el trimestre: aprobado.
5. Aclarado: EC0217.01 es el estándar CONOCER de impartición de cursos; los 6 kits Tekitl-Lab tienen expediente, el curso de secundaria no. No se afirma que cumpla el estándar.

## 6. Control de cambios

| Fecha | Cambio | Archivo | Resultado |
|---|---|---|---|
| 2026-10-05 | Análisis del docx y de Q1/Q2; creación de este plan | `PLAN-Q3-WORD.md` | Plan creado, sin cambios al Word |
| 2026-10-06 | Respuestas de Miguel registradas (§5); texto de I. Presentación propuesto en chat, pendiente de visto bueno | `PLAN-Q3-WORD.md` | Pasos A y B en curso; Word sin cambios |
| 2026-10-06 | Respaldo creado en `_respaldos/3er Trim E088 - antes de Presentacion - 20261006.docx` | `_respaldos/` | OK (no está en .gitignore: no subirlo a git) |
| 2026-10-06 | Insertada **I. PRESENTACIÓN** (4 párrafos, texto aprobado) tras la portada del informe anual, con salto de página y formato Gilroy 303030 justificado como la justificación. Eliminado el párrafo vacío final, que dejaba una hoja en blanco | `3er Trim E088 ... .docx` | Word: 4 páginas; Presentación en p. 4 en una sola hoja |
| 2026-10-06 | (ver también «Ronda 2026-10-06 (noche)» en §8.3) Insertada **II. RESULTADOS ALCANZADOS** (hoja nueva, págs. 5–6): Proyecto 1 TEKITL (Tekitl-Lab con fechas reales, tabla de 6 kits, Centinela, curso de secundaria), Proyecto 2 NODO (documento maestro, instalación 14/09 en 4 zonas, pruebas inicios de octubre) y Estatus Global (2 de 2; acumulado 6 de 8). Recortada la cifra de 180 t (ya está en la Justificación) | `3er Trim E088 ... .docx` | Word: 6 páginas |
| 2026-10-06 | Insertada **III. ACCIONES REALIZADAS** (7 acciones con fechas, pág. 7) con datos de Miguel: curso y sede en jul–ago; solicitudes de suficiencia presupuestal del 11/05/2026, folios IPPI/SDTI/003 y 004/2026 | `3er Trim E088 ... .docx` | Word + Gilroy: 7 páginas |
| 2026-10-06 | Corregida III acción 2 (solicitudes de **suficiencia presupuestal**). Insertada **IV. CONCLUSIONES Y RELACIÓN DE EVIDENCIA** (4 conclusiones, evidencias A–L, tabla de firmas) | `3er Trim E088 ... .docx` | Word + Gilroy: 9 páginas (IV en págs. 8–9) |
| 2026-10-06 | Revisión del Excel: corregidos I7 (guion), D27 (texto cortado al imprimir) y Z22 (alineado con el Word: fechas de kits y de instalación) | `Formato Cuadro resumen_Variable 1.xlsx` | 1 página; respaldo en `_respaldos/` |

### Notas de verificación (2026-10-06)
- Verificado con Word (exportación y conteo de páginas). **Gilroy no está instalada en este equipo**, así que Word sustituyó la fuente; revisar la paginación en el equipo donde se imprima.
- La portada anual llena exactamente su página: cualquier línea adicional en ella genera una hoja en blanco antes de la Presentación.
- Redacción acordada: NO se afirma que el curso de secundaria cumpla el estándar EC0217.01.

## 7. Después de entregar el reporte (no es parte del Q3)
- Generar el expediente EC0217.01 del curso "Electrónica y Programación Básica": carta descriptiva, lista de verificación de requerimientos, lista de asistencia, contrato de aprendizaje, cuestionarios con claves, lista de cotejo, guía de observación, encuesta de satisfacción, informe final y presentación. Antes de la impartición del 25 y 26 de noviembre de 2026 (Eloxochitlán).
- Completar el paquete de Impulso Lumínico (solo tiene carta descriptiva y presentación).
- Corregir el manual: respuestas en blanco, restos de LaTeX y lista de materiales incompleta.

## 8. II. RESULTADOS ALCANZADOS — análisis y plan (2026-10-06)

### 8.1 Hallazgos de la verificación contra evidencia
| Tema | Hallazgo | Consecuencia en el texto |
|---|---|---|
| Fechas de los kits Tekitl-Lab | Los expedientes se crearon del 29/03 al 07/05/2026 (metadatos). El "29/06" del borrador es solo la fecha de descarga de los zips. El Documento Ejecutivo es del 02/06/2026 | Son trabajo de **Q2 no reportado**. Se incluyen como base formativa de TEKITL **con su fecha real**, no como logro de jul–sep |
| Paquete de los 6 kits | H2O, Dinámica Rotatoria, Espectro Audible, Ponte las Pilas y Forja Térmica tienen los 10 documentos + presentación. **Impulso Lumínico solo tiene carta descriptiva y presentación** | Se dice "cinco completos; Impulso Lumínico parcial" |
| "Despertando al OJO" | Es el 7.º módulo del Documento Ejecutivo; su única impartición se suspendió | **No se menciona** en II |
| Centinela | Manual de uso: "fase de pruebas", solo el Sensor 5 habilitado para video. Fecha del código no determinable (mtime de git) | "Prototipo en fase de pruebas", sin fecha |
| Curso de secundaria | Manual con 10 capítulos (creado 11/09/2026); guía de 8 proyectos, 66 láminas (11–22/09). El borrador describe bien los capítulos 8–10 | Se conserva. Sin afirmar cumplimiento de EC0217.01 |
| NODO | Documentos de 24/07 (primera versión), 12–19/08 (NODO 3, dossier). Instalación 14/09 (dicho por Miguel); fotos 02 y 04/10 | Documentos "julio–agosto"; instalación 14/09; pruebas "a inicios de octubre" |
| Fotos de las zonas | Revisadas Zonas 1, 2, 3 y 4: coinciden con las descripciones. En Zona 2 el equipo "consola de video" es un conmutador pequeño con faders | Se redacta "consola de conmutación de video" y "pantalla de pared" (no "de proyección") en Zona 3 |
| 180 toneladas | Doc. Ejecutivo: 91.25 + 91.25 = 182.5 t/año (Cuetzalan y Zacapoaxtla) | "Más de 180" es correcto |

### 8.2 Decisiones tomadas al redactar (revertibles)
1. Los kits de Tekitl-Lab se reportan **con su fecha real (marzo–mayo / junio)**. Si Miguel prefiere no reportar trabajo anterior al trimestre, basta quitar ese bloque (la Presentación y la Justificación no dependen de él).
2. Estatus global: **2 de 2 proyectos del trimestre; acumulado 6 de 8** (coincide con "Realizado Sep = 2" del Excel y meta al corte 6). Se declara 100 % del trimestre solo con el matiz de "materiales preparados" y "primera etapa instalada".
3. Estructura como Q1/Q2: introducción, Proyecto 1, Proyecto 2, Estatus Global. II empieza en hoja nueva.
4. Formato: subtítulos en negritas, viñetas "•" con sangría francesa (el Word no tiene listas numeradas), tabla "Table Grid" para los 6 kits, Gilroy 303030 justificado.

### 8.3 Pasos
| # | Paso | Estado |
|---|---|---|
| II-A | Respaldo previo | Hecho: `_respaldos/3er Trim E088 - antes de Resultados - 20261006.docx` |
| II-B | Insertar II después de la Presentación (hoja nueva) | Hecho 2026-10-06 |
| II-C | Verificar con Word: páginas, ubicación, tabla y viñetas | Hecho 2026-10-06 (ver nota) |
| II-D | Commit (Miguel) | Pendiente |
| II-E | Instalar tipografías Gilroy y Corra Montserra y re-verificar con la fuente real | Hecho 2026-10-06 |
| II-F | Ajustar el layout a la fuente real (portada anual y extensión de II) | Hecho 2026-10-06 |

### Ronda 2026-10-06 (noche): tipografías y ajuste con Gilroy real
**Decisiones de Miguel:** se mantienen los kits de Tekitl-Lab con su fecha (§8.2-1); se confirma "100 %" del trimestre y acumulado 6 de 8 (§8.2-2); se conserva su salto de línea sobre los encabezados "I." y "II.". Julio–agosto: "se estuvieron preparando los cursos" (falta detalle y fechas para III).

**Tipografías:** instaladas para el usuario actual (sin administrador) desde `Downloads\TIPOGRAFÍAS`: Gilroy (20 OTF) y Corra Montserra (9 TTF estáticos) en `%LOCALAPPDATA%\Microsoft\Windows\Fonts` y registro `HKCU\...\Fonts`. Para quitarlas: borrar esos archivos y las entradas del registro. En otros equipos hay que instalarlas también.

**Efecto de Gilroy real (más ancha que la fuente sustituta):**
- La portada del informe anual dependía de ~28 párrafos vacíos y se desbordaba una línea. **Cambio:** se eliminaron los 28 vacíos y se puso un párrafo espaciador de altura exacta (185 pt) con salto de página antes del título. Ahora la portada se coloca igual en cualquier equipo con Gilroy.
- II excedía 2 páginas. **Cambios:** se recortaron frases (lista de capítulos del manual, componentes del NITC, descripción de Zona 2 y 4, texto de pruebas/estatus) y **la tabla de los 6 kits pasó a una lista en línea dentro de la viñeta** (la tabla ocupaba ~8 líneas). Resultado: II en págs. 5–6 con ~170 pt libres.

**Cambios de Miguel en Word detectados (se respetan):** salto de línea sobre "I. PRESENTACIÓN" y "II."; los cuatro sub-puntos de zonas quedaron sin el guion "–".

**Incidente y reparación:** al aplicar recortes, mis scripts indexaron mal los runs (Word separó viñeta y tabulador) y se sobrescribieron los encabezados en negrita de 3 viñetas (Seis cursos, Centinela y Estatus Global). Se detectó en la verificación y se reparó leyendo el texto de cada párrafo; se revisó el texto completo de II después. Lección: localizar por contenido, no por posición.

**Verificación final (Word + Gilroy):** 6 páginas: 1 portada · 2 justificación · 3 portada informe anual · 4 Presentación · 5–6 Resultados.

## 9. III. ACCIONES REALIZADAS (2026-10-06)

**Datos aportados por Miguel:** en julio y agosto se empezó a trabajar el curso "Electrónica y Programación Básica" y se definió la sede; la adquisición de los equipos fue en mayo, con solicitud de suficiencia presupuestal el 11/05/2026, folios IPPI/SDTI/003/2026 e IPPI/SDTI/004/2026.

**Redacción (7 acciones, formato Q2: lista numerada con título en negrita + fecha):**
1. Consolidación del programa Tekitl-Lab (marzo a junio de 2026) — antecedente rotulado con su fecha real.
2. Gestión de la adquisición de los equipos del NODO (mayo de 2026) — solicitudes de **suficiencia presupuestal** (folios 003 y 004, 11/05/2026), previas a la requisición a Recursos Materiales (la compra llega ~2 semanas después).
3. Elaboración del curso "Electrónica y Programación Básica" (julio a septiembre de 2026).
4. Definición de la sede de la primera impartición (julio y agosto de 2026) — Eloxochitlán.
5. Integración del Documento Maestro y Dossier del NITC (julio y agosto de 2026) — 24/07 y 12–19/08.
6. Instalación del NODO (14 de septiembre de 2026).
7. Configuración y pruebas de los equipos (inicios de octubre de 2026).

**Supuestos que Miguel debe confirmar:**
- Que los folios 003 y 004 son solicitudes de presupuesto **de los equipos que hoy integran el NODO** (así se redactó). Se redactó "solicitudes de presupuesto", no compra ni entrega.
- (Resuelto) Miguel: acciones 1 y 2 se quedan con sus fechas (marzo–junio y mayo) y la acción 7 se queda como inicios de octubre.

**Formato:** III sigue a II sin salto de página (como en Q1/Q2); el bloque de encabezado + introducción + acción 1 se mantiene unido y las acciones no se parten entre páginas. Resultado en Word con Gilroy: II en págs. 5–6 y III en la pág. 7 (7 páginas en total).

| # | Paso | Estado |
|---|---|---|
| III-A | Respaldo previo `_respaldos/3er Trim E088 - antes de Acciones - 20261006.docx` | Hecho |
| III-B | Insertar III con formato | Hecho 2026-10-06 |
| III-C | Verificar con Word + Gilroy | Hecho |
| III-D | Commit (Miguel) | Pendiente |

## 10. IV. CONCLUSIONES Y RELACIÓN DE EVIDENCIA DOCUMENTAL (2026-10-06)

### 10.1 Análisis de la evidencia
| Tema | Hallazgo | Consecuencia |
|---|---|---|
| Fotos del NODO | Solo Zona 3 (3.1–3.4) y Zona 1 (1.9, 1.10) conservan fecha EXIF: **02/10/2026**. El resto perdió metadatos. Ninguna es de 14/09 (Miguel lo confirmó) | En el Word se fecha solo lo comprobable (Z3: 02/10; Z4: 04/10 según Miguel; capturas OBS: 02/10); Zonas 1 y 2 van sin fecha |
| Duplicados | Zona 4.4, 4.5 y 4.6 son idénticas (hash) a 4.1, 4.2 y 4.3 | Evidencia K = 6 fotos: 4.1, 4.2, 4.3, 4.7, 4.8, 4.9 |
| Personas en fotos | Solo las **capturas de OBS** muestran a una persona (la misma): Z1.6, Z1.7, Z1.8, Z2.7, Z2.8. Las fotos de ambiente no muestran personas (en Z2.1 alcanza a verse una mano/pierna al borde) | Confirmar con la persona que aparece (probablemente del equipo) o excluir esas 5 capturas |
| Versiones del curso | Carpeta `TEKITL/`: original y V2 con **texto idéntico** (11/09 creado, 02/10 modificado). Raíz de `actividades MIR 2026/`: "Curso…" y "…- Formato" (05/10, Miguel está reformateando; encabezados en minúsculas; 1 imagen vs 30) | En el Word la evidencia se describe por título y fecha, **sin rutas** (como Q1/Q2), así no depende de la versión. Decidir cuál se imprime/anexa |
| Versiones del NODO | `NODO. DOC (1) (1)` 24/07 (primera) · `NODO 3` 12–14/08 · `NODO 3 (2)` 12–19/08 (la más reciente; quita "Leaflet" y "celismo") · Dossier/Tríptico 19/08 | Anexar **`NODO 3 (2).docx`** (vigente) + Dossier. Pendiente OK de Miguel |
| Kits | H2O, Dinámica Rotatoria, Espectro Audible, Ponte las Pilas y Forja Térmica completos; Impulso Lumínico solo carta y pptx | Evidencia B lo dice |
| Folios 003/004 | No están en el repo | Evidencia G; **escanear al llegar a la oficina (07/10)** y guardar en `Solicitudes/` |
| Firmas | Excel (más reciente): Elaboró Luis Antonio Molina Saldaña (Analista de la SDTI) / Validó Miguel (Encargado de despacho). Portada del Word: responsable Miguel. Notas del 02/10: validaba la DG | Se usó la combinación del Excel + portada; **por confirmar** |

### 10.2 Redacción
- **Conclusiones (4):** del diseño a la implementación; autonomía técnica y cultural (en futuro: "permitirán", no hay cursos impartidos); capacidad instalada para operar (primera impartición 25–26/11; NODO en condiciones de iniciar visitas supervisadas, sin fecha de apertura); siguientes etapas. Se evitó "listos para impartirse" y cualquier afirmación sobre EC0217.01 del curso de secundaria.
- **Evidencia A–L:** TEKITL (A documento maestro · B paquetes de los 6 cursos · C Centinela · D manual · E guía de 8 proyectos) y NODO (F documento maestro + dossier · G solicitudes de suficiencia presupuestal · H–K fotos por zona · L capturas OBS).
- **Firmas:** tabla ELABORÓ / VALIDÓ con espacio de firma; filas sin cortarse entre páginas.
- **Formato:** IV inicia en hoja nueva. Resultado en Word con Gilroy: IV en págs. 8–9; documento de 9 páginas.

### 10.3 Pasos
| # | Paso | Estado |
|---|---|---|
| IV-A | Respaldo `_respaldos/3er Trim E088 - antes de Conclusiones - 20261006.docx` | Hecho |
| IV-B | Corregir III acción 2 (suficiencia presupuestal) | Hecho |
| IV-C | Insertar IV, evidencia A–L y tabla de firmas | Hecho |
| IV-D | Verificar con Word + Gilroy; revisión de integridad (sin marcadores pendientes) | Hecho |
| IV-E | Commit (Miguel) | Pendiente |

## 11. Revisión del Excel `Formato Cuadro resumen_Variable 1.xlsx` (2026-10-06)

Hoja que se imprime: **"3er Trim E088"** (Instructivo y Ejemplo no se tocan). Respaldo previo: `_respaldos/Formato Cuadro resumen - antes de revision - 20261006.xlsx`.

**Verificado y correcto (sin cambios):**
- Programado: Mar 2, Jun 2, Sep 2, Dic 2; Anual 8; **Meta al corte 6** (BR12 ya estaba en 6).
- Realizado: Mar 2, Jun 2, Sep 2, Dic 0; **Anual 6; Meta al corte 6**. Sigue la convención del cuadro de Q2 (ceros en meses futuros; "Anual" = acumulado: Q2 imprimió 4 y 4). Coincide con el Word (100 % del trimestre, 6 de 8).
- Componente, Actividad, Indicador y título idénticos a Q1/Q2. Beneficiarios "NO APLICA". Elaboró/Validó coinciden con la tabla de firmas del Word (Luis Antonio Molina Saldaña / Miguel Trinidad Gómez Hernández). Una hoja horizontal, 76 %, área A1:CE32.
- Observación sobre Q1: el cuadro oficial de Q1 muestra Realizado Mar = 1 y Anual = 8 (aparente error de captura); Q2 ya lo corrigió a 2 y 4. El Q3 continúa la serie de Q2.

**Corregido (3 cambios):**
| Celda | Antes | Después | Motivo |
|---|---|---|---|
| I7 Unidad Responsable | `DA3Q INSTITUTO POBLANO…` | `DA3Q - INSTITUTO POBLANO…` | Como en Q1 y Q2 |
| D27 (línea de anexos) | texto en una línea, **cortado** al imprimir ("…y la evidencia") | mismo texto, con ajuste de línea y fila a 32 pt | Se perdía "fotográfica de la instalación" |
| Z22 (comentarios) | "Se consolidó… serie de 6 cursos"; "instaló y probó… área de sonido y proyección"; sin fecha de instalación | "Se integró… elaborados de marzo a mayo de 2026 con documentación en formato EC0217.01"; "Se instaló el 14 de septiembre de 2026… Los equipos se probaron a inicios de octubre"; "área de sonido" | Alinear con el Word (II, III) y no atribuir al trimestre trabajo de marzo–mayo |

Verificación: solo cambiaron I7 y Z22 (valores) y el formato de D27; logos, hojas, 87 celdas combinadas y la impresión en una página se conservan. Texto de comentarios 1,625 caracteres (antes 1,641), cabe en su celda.

**Pendiente en el Excel (decisión de Miguel):** si D27 debe mencionar también la relación de evidencia (A–L) y las solicitudes de suficiencia presupuestal. Se dejó el texto original.

## 12. Pendientes para cerrar el reporte
*(Lista de impresión con casillas: `LISTA-IMPRESION-Q3.md`; PDFs de fotos listos para imprimir en `_impresion/`.)*

1. **Escanear folios IPPI/SDTI/003/2026 y 004/2026** (Evidencia G) al llegar a la oficina.
2. (Hecho 2026-10-06, ver §11) Excel revisado: BR12 = 6 ya estaba; coincide con el Word; se corrigieron I7, D27 y Z22.
3. Confirmar firmas (Elaboró/Validó) en el Word y el Excel.
4. Decidir qué versión se imprime/anexa del curso (raíz "Formato" vs `TEKITL/`) y del documento NODO (recomendada: `NODO 3 (2).docx`).
5. Persona que aparece en las capturas de OBS (Evidencias K y L): confirmar permiso o excluir esas capturas.
6. Eliminar o excluir las fotos duplicadas Zona 4.4–4.6.
7. Revisar el Word completo en el equipo de impresión (Gilroy instalada) y exportar a PDF.
8. Commit y, después de entregar: expediente EC0217.01 del curso de secundaria (§7).

| 2026-10-06 | Evidencia G escaneada: memorándums IPPI/SDTI/003 y 004 (impresos con "/2025" por error de origen; el informe se deja "/2026" por decisión de Miguel), fechados 16/04/2026 y recibidos por Administración y Finanzas el 06/05/2026. Corregida la fecha en III acción 2 (pág. 6) y en la relación de evidencia G (pág. 9); antes decía 11/05/2026. Escaneos movidos a `Solicitudes/` | `3er Trim E088 ... .docx` | Word + Gilroy: 9 páginas; solo cambian págs. 6 y 9 |
| 2026-10-06 | Folios cambiados a **IPPI/SDTI/003/2025 e IPPI/SDTI/004/2025**, como están impresos en los memorándums (decisión de Miguel, para que coincidan con la Evidencia G). 4 menciones, en págs. 6 y 9; el Excel no los menciona | `3er Trim E088 ... .docx` | Word + Gilroy: 9 páginas; solo cambian págs. 6 y 9 |
| 2026-10-06 | Instaladas en este equipo (por usuario) las 20 variantes de Gilroy y las 9 de Corra Montserra TTF, desde `TIPOGRAFÍAS/`. Antes solo estaba Gilroy Light, así que la paginación anterior era con fuente sustituta. Con Gilroy real: 9 páginas y firmas en la 9, pero III. ACCIONES empieza en la pág. 7 y cambian los cortes de las págs. 5-7. Nombre interno de la familia: "Cora Montserra" (una "r") | Sistema | Reimprimir el informe completo |
| 2026-10-06 | Evidencia F (pág. 9): quitado "y Tríptico informativo". El archivo `NODO. DOSSIER y TRIPTICO…docx` trae el Dossier y solo la estructura del tríptico (texto por panel), no un tríptico diseñado (observación de Miguel). Queda "Documento Maestro Ejecutivo y Dossier del NITC", igual que en II y III | `3er Trim E088 ... .docx` | 9 páginas; solo cambia la 9 |
