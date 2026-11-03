# Fuentes y datos de la presentación de la Mesa Técnica IPPI–SECIHTI (con énfasis en CENEVAL)

**Área:** Subdirección de Desarrollo de Tecnologías de la Información, Instituto Poblano de los Pueblos Indígenas (IPPI)
**Fecha de elaboración:** 3 de noviembre de 2026 (todas las consultas web se hicieron ese día)
**Presentación asociada:** `2026-11-04 - presentacion-mesa-tecnica-ippi-secihti.pptx` (misma carpeta)
**Propósito:** Dejar registrado de dónde sale cada dato de la presentación, con los enlaces para volver a consultarlo o descargarlo, y los datos ya extraídos, para no repetir la investigación. Complementa a [fuentes-y-bases-transversalidad-pueblos-indigenas.md](fuentes-y-bases-transversalidad-pueblos-indigenas.md) y [analisis-mir-2026-secihti.md](analisis-mir-2026-secihti.md).

**Abreviaturas usadas:** ANS = Aún no satisfactorio · S = Satisfactorio · SS = Sobresaliente · IES = institución de educación superior · NSE = nivel socioeconómico · n = número de sustentantes.

---

## 1. Qué dato usa cada diapositiva

| Diap. | Dato que aparece | De dónde sale | Sección de este archivo |
|---|---|---|---|
| 1-2 | Fecha, hora, sede y orden del día de la mesa | Oficio circular IPPI/DG/008/2026 (30 oct 2026) | 7.5 |
| 3 | Estrategia 1.1.1.13, tres líneas, responsable SECIHTI, indicador del Programa | Programa Especial 2024-2026 | 7.1 |
| 4 | Roles de Instancia Rectora, Art. 84, 85 y 95; $4,030,549 | Ley de Egresos 2026 | 7.2 |
| 6 | 14 %, 1.7 % a 72 %, 29 de 76, 8 sin WiFi, 8 % con computadora | Base del IPPI (INEGI Censo 2020 y CFE) | 7.4 |
| 6 | Citas «no existen programas sistemáticos» y «prácticamente inexistentes» | Programa Especial, diagnóstico | 7.1 |
| 7 | 12,786 sustentantes; 26 % a 46 % sin nivel satisfactorio | CENEVAL, tableros EGEL Plus 2025 | 4.1 y 6 |
| 8 | Área más débil de cada examen (36.0 % a 55.4 %) | CENEVAL, tableros EGEL Plus 2025 | 4.3 y 6 |
| 9 | ANS por nivel socioeconómico (27 % a 49 %); internet fijo por nivel (98 % a 4 %) | CENEVAL, ICOMPU 2025, tablero «Ámbito social» | 4.4 y 6 |
| 10 | 8.9 %, 7.5 % y 3.4 % con un padre hablante de lengua indígena | CENEVAL, informes EGEL 2021 (PDF) | 5.1 |
| 10 | Variable ausente en 2025 | CENEVAL, ICOMPU 2025, tablero «Ámbito personal» | 4.4 |
| 10, 14 | Desagregación «Estatal» de Q002 1.2 | MIR 2026 de SECIHTI | 7.3 |
| 12 | Q001 y Q002 en las tablas 3 y 4; 14.5 %, 25.7 %, 21.3 % | Ley de Egresos 2026 | 7.2 y 6 |
| 13-14 | Cobertura del MIR por línea; ficha de Q002 1.2 | MIR 2026 de SECIHTI | 7.3 |
| 15-16 | Solicitudes y acuerdos | Propuesta del IPPI (derivada de 7.2 y 7.3) | 7.2 y 7.3 |

---

## 2. Cómo está organizada la información de CENEVAL

CENEVAL **no tiene una sección de datos abiertos ni de estadísticas tecnológicas generales**. Lo que publica y sirve para este tema son los **informes anuales de resultados de los EGEL** (examen de egreso de licenciatura) de las carreras de tecnología, con un cuestionario de contexto.

| Formato | Años | Dónde |
|---|---|---|
| Tableros interactivos Superset (públicos, sin cuenta) | 2025 | Sección 3.1 |
| Tableros Looker Studio | 2022, 2023, 2024 | Sección 3.2 |
| PDF (informe completo; los tres que se leyeron tienen de 267 a 333 páginas) | 2016 a 2021 | Sección 3.3 |
| Anuarios estadísticos | 2019 a 2023 | Sección 3.4 |

Página índice de todo lo anterior: <https://ceneval.edu.mx/examenes-egreso-informes-anuales/>

**Exámenes de tecnología que se revisaron (7):**

| Clave | Examen |
|---|---|
| COMPU | Ciencias Computacionales |
| ICOMPU | Ingeniería Computacional |
| ISOFT | Ingeniería de Software |
| INFO | Informática |
| IELEC | Ingeniería Eléctrica |
| IELECTRO | Ingeniería Electrónica |
| IMECATRO | Ingeniería Mecatrónica |

En esa página no aparecen informes de Telecomunicaciones, Ciencias de datos, Redes ni Tecnologías de la información como exámenes propios.

### Cómo consultar y descargar los tableros 2025 (Superset)

1. Abrir la URL del tablero (sección 3.1). **No requiere inicio de sesión.** La clave `?native_filters_key=...` que publica CENEVAL no es indispensable: se comprobó con ICOMPU (la URL sin clave carga los 2,039 sustentantes).
2. Dar clic en la pestaña **«Resultados en el EGEL Plus»**. Ahí están las tablas de distribución global, por sección y por área. Los filtros «Clave del campus o plantel» y «Número de aplicación» permiten acotar.
3. En la parte final de esa pestaña hay enlaces al **cuestionario de contexto** («Ámbito personal», «Ámbito escolar», «Ámbito social») y a la **distribución por institución**.
4. Cada gráfica tiene un menú `⋯` con las opciones **Download**, **View as table**, **Share** y **View query** (se verificó que existen; **no se probó descargar**, así que no se sabe si el rol público permite exportar a CSV o Excel). Si no deja descargar, «View as table» muestra los datos para copiarlos.
5. Los números de los tableros se extrajeron copiando el texto de la página; por eso algunas cifras grandes aparecen abreviadas (por ejemplo «1.03k»). Donde pasa, abajo se calculó la cifra exacta a partir de las otras dos categorías y del total.

---

## 3. Enlaces

### 3.1 Tableros EGEL Plus 2025 (Superset)

| Examen | URL base (probada con ICOMPU) | URL publicada por CENEVAL (con clave de filtros) |
|---|---|---|
| ICOMPU | <https://superset.ceneval.edu.mx/superset/dashboard/661/> | <https://superset.ceneval.edu.mx/superset/dashboard/661/?native_filters_key=L6JllXnBuDM> |
| ISOFT | <https://superset.ceneval.edu.mx/superset/dashboard/54/> | <https://superset.ceneval.edu.mx/superset/dashboard/54/?native_filters_key=JmjBkQOizLg> |
| INFO | <https://superset.ceneval.edu.mx/superset/dashboard/596/> | <https://superset.ceneval.edu.mx/superset/dashboard/596/?native_filters_key=9nfoSkCcqwM> |
| COMPU | <https://superset.ceneval.edu.mx/superset/dashboard/48/> | <https://superset.ceneval.edu.mx/superset/dashboard/48/?native_filters_key=12PDunhL3j4> |
| IELEC | <https://superset.ceneval.edu.mx/superset/dashboard/622/> | <https://superset.ceneval.edu.mx/superset/dashboard/622/?native_filters_key=Tch62e1Q5p0> |
| IELECTRO | <https://superset.ceneval.edu.mx/superset/dashboard/56/> | <https://superset.ceneval.edu.mx/superset/dashboard/56/?native_filters_key=qvsGdFlh-s4> |
| IMECATRO | <https://superset.ceneval.edu.mx/superset/dashboard/62/> | <https://superset.ceneval.edu.mx/superset/dashboard/62/?native_filters_key=ngYju2aHEkA> |

**Tableros de contexto de ICOMPU 2025** (solo estos se revisaron; los de los otros seis exámenes están enlazados desde la pestaña «Resultados» de cada tablero):

| Tablero | URL |
|---|---|
| Ámbito personal (sexo, beca, edad, promedio) | <https://superset.ceneval.edu.mx/superset/dashboard/662/?native_filters_key=pPsYiQr3ClE> |
| Ámbito escolar (prácticas profesionales, servicio social) | <https://superset.ceneval.edu.mx/superset/dashboard/663/?native_filters_key=IWzGETZyZJE> |
| Ámbito social (nivel socioeconómico, capital cultural, situación laboral) | <https://superset.ceneval.edu.mx/superset/dashboard/664/?native_filters_key=_sGR8-Btuaw> |
| Distribución por institución (campus o plantel) | <https://superset.ceneval.edu.mx/superset/dashboard/694/?native_filters_key=KpvVSF-Sdt4> |

### 3.2 Tableros 2022, 2023 y 2024 (Looker Studio) — no se abrieron

Se anotan para la serie histórica. Los enlaces provienen de la página índice; **no se revisó su contenido** (Looker Studio es más difícil de leer en automático).

| Examen | 2022 | 2023 | 2024 |
|---|---|---|---|
| COMPU | [2022](https://lookerstudio.google.com/reporting/3c92e33c-9586-43d8-aa03-d0faf404cca7/page/p_d3dapnho0c) | [2023](https://lookerstudio.google.com/reporting/ba2f15ae-2d0a-435b-ac88-472f23774153/page/p_d3dapnho0c) | [2024](https://lookerstudio.google.com/u/0/reporting/d36f2273-9620-4d10-81c9-49a36697e1d4/page/p_d3dapnho0c) |
| ICOMPU | [2022](https://lookerstudio.google.com/reporting/b9d0cf23-7630-45c9-9bb7-485ee5c6e23e/page/p_d3dapnho0c) | [2023](https://lookerstudio.google.com/reporting/eaad2737-1b2f-470a-8dd0-2b0eeb3ef6b6/page/p_d3dapnho0c) | [2024](https://lookerstudio.google.com/u/0/reporting/07bdddc2-fe0f-4a19-bc5f-1c1550641828/page/p_d3dapnho0c) |
| ISOFT | [2022](https://lookerstudio.google.com/reporting/749d95e1-1051-4b3d-9dec-f4fe98882a81/page/p_d3dapnho0c) | [2023](https://lookerstudio.google.com/reporting/ccb442e4-4c07-4332-873f-90320f35511b/page/p_d3dapnho0c) | [2024](https://lookerstudio.google.com/u/0/reporting/aa633344-60ed-464c-b5a4-b301f1e95fe1/page/p_d3dapnho0c) |
| INFO | [2022](https://lookerstudio.google.com/reporting/e904281f-c827-42a2-9f6c-ab0e2224184f/page/p_d3dapnho0c) | [2023](https://lookerstudio.google.com/reporting/2980eef2-bea8-4f4a-ab08-f68ed2fe9ae0/page/p_d3dapnho0c) | [2024](https://lookerstudio.google.com/u/0/reporting/561cb4f7-439b-4abd-90da-e0f8b09e826a/page/p_d3dapnho0c) |
| IELEC | [2022](https://lookerstudio.google.com/reporting/acbae6e5-624a-4c05-9da0-44a4fe46b22a/page/p_d3dapnho0c) | [2023](https://lookerstudio.google.com/reporting/7dbc3717-cc65-4364-8556-61dacf19d1c5/page/p_d3dapnho0c) | [2024](https://lookerstudio.google.com/u/0/reporting/b5cb6eb2-e6ff-4018-a572-0d29393ada11/page/p_d3dapnho0c) |
| IELECTRO | [2022](https://lookerstudio.google.com/reporting/4af4784b-89b5-427f-a933-4d0c6bbf9bea/page/p_d3dapnho0c) | [2023](https://lookerstudio.google.com/reporting/3a69403b-c44b-4a4b-bbac-3d0e7adfca45/page/p_d3dapnho0c) | [2024](https://lookerstudio.google.com/u/0/reporting/8e2b432c-43d7-4bb2-aa6c-64104d9fe06e/page/p_d3dapnho0c) |
| IMECATRO | [2022](https://lookerstudio.google.com/reporting/f4f5ef17-0f15-4123-acab-38731b5838c8/page/p_d3dapnho0c) | [2023](https://lookerstudio.google.com/reporting/05cad185-f2d9-4554-9035-60625897bb98/page/p_d3dapnho0c) | [2024](https://lookerstudio.google.com/u/0/reporting/3c279567-42ac-40e7-b11a-d1e8c175f53c/page/p_d3dapnho0c) |

### 3.3 Informes en PDF 2016 a 2021

Los **42 enlaces responden (HTTP 200)**, comprobado el 3 de noviembre de 2026 con solicitudes de encabezado (no se descargaron). Pesan en conjunto unos **229 MB** (unos 5.5 MB en promedio; los tres de 2021 que se revisaron pesan entre 6.7 y 8.8 MB). De los de 2021, solo ICOMPU, ISOFT e INFO se revisaron, en sus secciones 2 y 3.

| Examen | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 |
|---|---|---|---|---|---|---|
| COMPU | [PDF](https://ceneval.edu.mx/wp-content/uploads/2021/07/COMPU_2016.pdf) | [PDF](https://ceneval.edu.mx/wp-content/uploads/2021/07/COMPU_2017.pdf) | [PDF](https://ceneval.edu.mx/wp-content/uploads/2021/07/COMPU_2018.pdf) | [PDF](https://ceneval.edu.mx/wp-content/uploads/2021/07/COMPU_2019.pdf) | [PDF](https://ceneval.edu.mx/wp-content/uploads/2021/07/COMPU_2020.pdf) | [PDF](https://ceneval.edu.mx/wp-content/uploads/2022/04/COMPU_2021.pdf) |
| ICOMPU | [PDF](https://ceneval.edu.mx/wp-content/uploads/2021/07/ICOMPU_2016.pdf) | [PDF](https://ceneval.edu.mx/wp-content/uploads/2021/07/ICOMPU_2017.pdf) | [PDF](https://ceneval.edu.mx/wp-content/uploads/2021/07/ICOMPU_2018.pdf) | [PDF](https://ceneval.edu.mx/wp-content/uploads/2021/07/ICOMPU_2019.pdf) | [PDF](https://ceneval.edu.mx/wp-content/uploads/2021/07/ICOMPU_2020.pdf) | [PDF](https://ceneval.edu.mx/wp-content/uploads/2022/03/ICOMPU2021.pdf) |
| ISOFT | [PDF](https://ceneval.edu.mx/wp-content/uploads/2021/07/ISOFT_2016.pdf) | [PDF](https://ceneval.edu.mx/wp-content/uploads/2021/07/ISOFT_2017.pdf) | [PDF](https://ceneval.edu.mx/wp-content/uploads/2021/07/ISOFT_2018.pdf) | [PDF](https://ceneval.edu.mx/wp-content/uploads/2021/07/ISOFT_2019.pdf) | [PDF](https://ceneval.edu.mx/wp-content/uploads/2021/07/ISOFT_2020.pdf) | [PDF](https://ceneval.edu.mx/wp-content/uploads/2022/03/ISOFT2021-1.pdf) |
| INFO | [PDF](https://ceneval.edu.mx/wp-content/uploads/2021/07/INFO_2016.pdf) | [PDF](https://ceneval.edu.mx/wp-content/uploads/2021/07/INFO_2017.pdf) | [PDF](https://ceneval.edu.mx/wp-content/uploads/2021/07/INFO_2018.pdf) | [PDF](https://ceneval.edu.mx/wp-content/uploads/2021/07/INFO_2019.pdf) | [PDF](https://ceneval.edu.mx/wp-content/uploads/2021/07/INFO_2020.pdf) | [PDF](https://ceneval.edu.mx/wp-content/uploads/2022/03/INFO2021.pdf) |
| IELEC | [PDF](https://ceneval.edu.mx/wp-content/uploads/2021/07/IELEC_2016.pdf) | [PDF](https://ceneval.edu.mx/wp-content/uploads/2021/07/IELEC_2017.pdf) | [PDF](https://ceneval.edu.mx/wp-content/uploads/2021/07/IELEC_2018.pdf) | [PDF](https://ceneval.edu.mx/wp-content/uploads/2021/07/IELEC_2019.docx.pdf) | [PDF](https://ceneval.edu.mx/wp-content/uploads/2021/07/IELEC_2020.pdf) | [PDF](https://ceneval.edu.mx/wp-content/uploads/2022/04/IELEC_2021.pdf) |
| IELECTRO | [PDF](https://ceneval.edu.mx/wp-content/uploads/2021/07/IELECTRO_2016.pdf) | [PDF](https://ceneval.edu.mx/wp-content/uploads/2021/07/IELECTRO_2017.pdf) | [PDF](https://ceneval.edu.mx/wp-content/uploads/2021/07/IELECTRO_2018.pdf) | [PDF](https://ceneval.edu.mx/wp-content/uploads/2021/07/IELECTRO_2019.pdf) | [PDF](https://ceneval.edu.mx/wp-content/uploads/2021/07/IELECTRO_2020.pdf) | [PDF](https://ceneval.edu.mx/wp-content/uploads/2022/03/IELECTRO2021.pdf) |
| IMECATRO | [PDF](https://ceneval.edu.mx/wp-content/uploads/2021/07/IMECATRO_2016.pdf) | [PDF](https://ceneval.edu.mx/wp-content/uploads/2021/07/IMECATRO_2017.pdf) | [PDF](https://ceneval.edu.mx/wp-content/uploads/2021/07/IMECATRO_2018.pdf) | [PDF](https://ceneval.edu.mx/wp-content/uploads/2021/07/IMECATRO_2019.pdf) | [PDF](https://ceneval.edu.mx/wp-content/uploads/2021/07/IMECATRO_2020.pdf) | [PDF](https://ceneval.edu.mx/wp-content/uploads/2022/04/IMECATRO_2021.pdf) |

**Estructura de cada informe 2021** (sirve para ubicar datos): 1 Introducción · 2 Datos descriptivos (demográficos, escolaridad de los padres, condición socioeconómica, trayectoria académica) · 3 Resultados en testimonios y niveles de desempeño (3.2 testimonios, 3.3 áreas) · 4 Relación entre variables de contexto y resultados · 5 Padrón EGEL · Anexos I a III (resultados por institución). Para los informes de 2016 a 2020 la estructura es parecida pero **no se revisó**.

### 3.4 Anuarios estadísticos (no se revisaron)

| Año | URL |
|---|---|
| 2019 | <https://ceneval.edu.mx/wp-content/uploads/2022/06/Ceneval-Anuario-estadistico-2019.pdf> |
| 2020 | <https://ceneval.edu.mx/wp-content/uploads/2022/06/Ceneval-Anuario-estadistico-2020_WEB.pdf> |
| 2021 | <https://ceneval.edu.mx/wp-content/uploads/2022/10/Anuarioestadistico20213small.pdf> |
| 2022 | <https://online.flippingbook.com/view/784563051/> |
| 2023 | <https://online.flippingbook.com/view/22783921/> |

Índice: <https://ceneval.edu.mx/anuarios-estadisticos/>. Se desconoce si cubren programas de tecnología.

### 3.5 Otras páginas de CENEVAL

| Para qué | URL |
|---|---|
| Informes de resultados de ingreso (EXANI) | <https://ceneval.edu.mx/examenes-ingreso-resultados_anuales/> |
| Informes de resultados DOMINA-BACH | <https://ceneval.edu.mx/estadisticas-anuales-domina-bach/> |
| Padrón EGEL (programas de alto rendimiento) | <https://reconocimiento.ceneval.edu.mx/padron-egel/> |
| Portal de reconocimiento y premiaciones | <https://reconocimiento.ceneval.edu.mx> |
| Informes institucionales | <https://ceneval.edu.mx/sobre_el_ceneval-informes/> |
| Ceneval Investiga (revista) | <https://ceneval.edu.mx/sobre_el_ceneval-publicaciones-ceneval_investiga/> |

---

## 4. Datos extraídos de los tableros EGEL Plus 2025 (enero a diciembre de 2025)

### 4.1 Nivel de desempeño global

| Examen | Sustentantes | ANS n | ANS % | S n | S % | SS n | SS % |
|---|---:|---:|---:|---:|---:|---:|---:|
| COMPU | 940 | 259 | 27.55 | 565 | 60.11 | 116 | 12.34 |
| ICOMPU | 2,039 | 735 | 36.05 | 1,061 | 52.04 | 243 | 11.92 |
| ISOFT | 3,275 | 871 | 26.60 | 1,945 | 59.39 | 459 | 14.02 |
| INFO | 1,457 | 468 | 32.12 | 807 | 55.39 | 182 | 12.49 |
| IELEC | 312 | 82 | 26.28 | 186 | 59.62 | 44 | 14.10 |
| IELECTRO | 841 | 383 | 45.54 | 387 | 46.02 | 71 | 8.44 |
| IMECATRO | 3,922 | 1,579 | 40.26 | 1,929 | 49.18 | 414 | 10.56 |
| **Total** | **12,786** | | | | | | |

En cada fila, ANS + S + SS suma exactamente el número de sustentantes. El examen es el **EGEL Plus** (200 reactivos en ICOMPU: sección disciplinar de 140 y sección transversal de Lenguaje y Comunicación de 60).

### 4.2 Por sección (disciplinar y transversal de Lenguaje y Comunicación)

| Examen | Disciplinar ANS / S / SS (n) | Disciplinar ANS / S / SS (%) | Transversal ANS / S / SS (n) | Transversal ANS / S / SS (%) |
|---|---|---|---|---|
| COMPU | 259 / 565 / 116 | 27.55 / 60.11 / 12.34 | 138 / 601 / 201 | 14.68 / 63.94 / 21.38 |
| ICOMPU | 735 / 1,056 / 248 | 36.05 / 51.79 / 12.16 | 416 / 1,235 / 388 | 20.40 / 60.57 / 19.03 |
| ISOFT | 871 / 1,933 / 471 | 26.60 / 59.02 / 14.38 | 501 / 1,789 / 985 | 15.30 / 54.63 / 30.08 |
| INFO | 468 / 800 / 189 | 32.12 / 54.91 / 12.97 | 367 / 884 / 206 | 25.19 / 60.67 / 14.14 |
| IELEC | 82 / 182 / 48 | 26.28 / 58.33 / 15.38 | 90 / 204 / 18 | 28.85 / 65.38 / 5.77 |
| IELECTRO | 383 / 386 / 72 | 45.54 / 45.90 / 8.56 | 155 / 549 / 137 | 18.43 / 65.28 / 16.29 |
| IMECATRO | 1,579 / 1,921 / 422 | 40.26 / 48.98 / 10.76 | 639 / 2,256 / 1,027 | 16.29 / 57.52 / 26.19 |

### 4.3 Por área (ANS / S / SS, con n y %)

Los nombres de las áreas vienen del párrafo del tablero que las lista en orden; las tablas del tablero se llaman «Area 1_D, 2_D…» y **se asignaron por ese orden**. Como control, en todas las áreas ANS + S + SS suma el total de sustentantes del examen. Para confirmarlo a ojo, abrir el tablero y comparar los títulos de las gráficas.

**ICOMPU (n = 2,039)**

| Área | ANS | S | SS |
|---|---|---|---|
| 1. Implementación de hardware | 919 (45.07 %) | 604 (29.62 %) | 516 (25.31 %) |
| 2. Implementación de redes de computadoras | 1,129 (55.37 %) | 492 (24.13 %) | 418 (20.50 %) |
| 3. Desarrollo de software | 621 (30.46 %) | 1,022 (50.12 %) | 396 (19.42 %) |
| T1. Comprensión lectora | 268 (13.14 %) | 879 (43.11 %) | 892 (43.75 %) |
| T2. Redacción indirecta | 772 (37.86 %) | ≈1,034 (50.71 %) * | 233 (11.43 %) |

**ISOFT (n = 3,275)**

| Área | ANS | S | SS |
|---|---|---|---|
| 1. Análisis de sistemas de software | 1,180 (36.03 %) | 1,465 (44.73 %) | 630 (19.24 %) |
| 2. Diseño de sistemas de software | 995 (30.38 %) | 1,521 (46.44 %) | 759 (23.18 %) |
| 3. Desarrollo de sistemas de software | 903 (27.57 %) | 1,721 (52.55 %) | 651 (19.88 %) |
| 4. Gestión de proyectos de software | 1,026 (31.33 %) | 1,215 (37.10 %) | 1,034 (31.57 %) |
| T1. Comprensión lectora | 325 (9.92 %) | 1,195 (36.49 %) | 1,755 (53.59 %) |
| T2. Redacción indirecta | 958 (29.25 %) | ≈1,637 (49.98 %) * | 680 (20.76 %) |

**INFO (n = 1,457)**

| Área | ANS | S | SS |
|---|---|---|---|
| 1. Necesidades informáticas de una organización | 728 (49.97 %) | 462 (31.71 %) | 267 (18.33 %) |
| 2. Gestión de proyectos informáticos | 372 (25.53 %) | 705 (48.39 %) | 380 (26.08 %) |
| 3. Implementación de sistemas de información | 472 (32.40 %) | 562 (38.57 %) | 423 (29.03 %) |
| 4. Función informática | 716 (49.14 %) | 407 (27.93 %) | 334 (22.92 %) |
| T1. Comprensión lectora | 259 (17.78 %) | 644 (44.20 %) | 554 (38.02 %) |
| T2. Redacción indirecta | 640 (43.93 %) | 691 (47.43 %) | 126 (8.65 %) |

**COMPU (n = 940)**

| Área | ANS | S | SS |
|---|---|---|---|
| 1. Algoritmia | 488 (51.91 %) | 347 (36.91 %) | 105 (11.17 %) |
| 2. Desarrollo de software de base | 306 (32.55 %) | 403 (42.87 %) | 231 (24.57 %) |
| 3. Desarrollo de software de aplicación | 283 (30.11 %) | 430 (45.74 %) | 227 (24.15 %) |
| 4. Soluciones de cómputo inteligente | 121 (12.87 %) | 351 (37.34 %) | 468 (49.79 %) |
| T1. Comprensión lectora | 108 (11.49 %) | 395 (42.02 %) | 437 (46.49 %) |
| T2. Redacción indirecta | 265 (28.19 %) | 522 (55.53 %) | 153 (16.28 %) |

**IELEC (n = 312)**

| Área | ANS | S | SS |
|---|---|---|---|
| 1. Diseño de equipos y sistemas eléctricos | 96 (30.77 %) | 112 (35.90 %) | 104 (33.33 %) |
| 2. Construcción de equipos y sistemas eléctricos | 83 (26.60 %) | 160 (51.28 %) | 69 (22.12 %) |
| 3. Operación de equipos y sistemas eléctricos | 141 (45.19 %) | 110 (35.26 %) | 61 (19.55 %) |
| 4. Pruebas y mantenimiento de equipos y sistemas eléctricos | 70 (22.44 %) | 168 (53.85 %) | 74 (23.72 %) |
| T1. Comprensión lectora | 73 (23.40 %) | 166 (53.21 %) | 73 (23.40 %) |
| T2. Redacción indirecta | 143 (45.83 %) | 153 (49.04 %) | 16 (5.13 %) |

**IELECTRO (n = 841)**

| Área | ANS | S | SS |
|---|---|---|---|
| 1. Diseño de equipos y sistemas electrónicos | 414 (49.23 %) | 290 (34.48 %) | 137 (16.29 %) |
| 2. Construcción de equipos y sistemas electrónicos | 429 (51.01 %) | 280 (33.29 %) | 132 (15.70 %) |
| 3. Operación de equipos y sistemas electrónicos | 400 (47.56 %) | 307 (36.50 %) | 134 (15.93 %) |
| T1. Comprensión lectora | 106 (12.60 %) | 376 (44.71 %) | 359 (42.69 %) |
| T2. Redacción indirecta | 322 (38.29 %) | 437 (51.96 %) | 82 (9.75 %) |

**IMECATRO (n = 3,922)**

| Área | ANS | S | SS |
|---|---|---|---|
| 1. Diseño de sistemas mecatrónicos | 2,076 (52.93 %) | 1,350 (34.42 %) | 496 (12.65 %) |
| 2. Implementación de sistemas mecatrónicos | 1,813 (46.23 %) | 1,468 (37.43 %) | 641 (16.34 %) |
| 3. Integración de tecnologías para sistemas mecatrónicos | 1,236 (31.51 %) | 1,720 (43.86 %) | 966 (24.63 %) |
| T1. Comprensión lectora | 513 (13.08 %) | 1,331 (33.94 %) | 2,078 (52.98 %) |
| T2. Redacción indirecta | ≈1,160 (29.58 %) * | ≈2,060 (52.52 %) * | 702 (17.90 %) |

\* El tablero mostró la cifra abreviada («1.03k», «1.64k», «1.16k», «2.06k»). El valor exacto se obtuvo restando las otras dos categorías al total de sustentantes y coincide con el porcentaje publicado.

**Descriptores de los niveles** (qué sabe hacer un sustentante en cada área): están en la pestaña «Característica del EGEL Plus» de cada tablero. Se leyeron los de ICOMPU; incluyen, por ejemplo, para Redes: modelo OSI y TCP/IP, cableado estructurado, vulnerabilidades y criptografía.

### 4.4 Cuestionario de contexto, ICOMPU 2025 (n = 2,039)

**Nivel socioeconómico** (tablero «Ámbito social», <https://superset.ceneval.edu.mx/superset/dashboard/664/?native_filters_key=_sGR8-Btuaw>)

| NSE | Sustentantes | % | ANS | S | SS | ANS / sustentantes |
|---|---:|---:|---:|---:|---:|---:|
| A/B | 508 | 24.91 | 137 | 297 | 74 | 27.0 % |
| C+ | 389 | 19.08 | 112 | 227 | 50 | 28.8 % |
| C | 335 | 16.43 | 131 | 164 | 40 | 39.1 % |
| C- | 394 | 19.32 | 164 | 185 | 45 | 41.6 % |
| D+ | 214 | 10.50 | 94 | 96 | 24 | 43.9 % |
| D | 186 | 9.12 | 91 | 86 | 9 | 48.9 % |
| E | 11 | 0.54 | 6 | 4 | 1 | 54.5 % (n muy pequeño) |
| No contestó | 2 | 0.10 | 0 | 2 | 0 | |

La última columna es un **cálculo propio**. Las columnas ANS, S y SS son las del tablero.

**Descripción de cada nivel que da CENEVAL** (la usa la diapositiva 9; es la referencia nacional por nivel de hogar, **no** el acceso de los sustentantes):

| NSE | Hogares con internet fijo en la vivienda | Otro dato que da CENEVAL |
|---|---:|---|
| A/B | 98 % | Jefe de hogar con estudios profesionales o posgrado: 82 %. Gasto en alimentos 28 % |
| C+ | 93 % | 87 % con al menos un vehículo. Alimentos 32 % |
| C | 77 % | 83 % con jefe de hogar con estudios mayores a primaria. Alimentos 35 % |
| C- | 52 % | 74 % con jefe de hogar con estudios mayores a primaria. Alimentos 38 % |
| D+ | 22 % | 62 % con jefe de hogar con estudios mayores a primaria. Alimentos 42 % |
| D | 4 % | En 56 % el jefe de hogar tiene hasta primaria. Alimentos 46 % |
| E | 0.2 % | 95 % con jefe de hogar con hasta primaria. Alimentos 52 % |

El modelo de CENEVAL construye el NSE (siete niveles) con estas variables: internet en casa, automóvil, baños completos, cuartos, personas de 14 años o más que trabajaron el mes pasado y escolaridad de la jefa o el jefe del hogar.

**Datos generales** (tablero «Ámbito personal», <https://superset.ceneval.edu.mx/superset/dashboard/662/?native_filters_key=pPsYiQr3ClE>). En la sección «Datos generales» aparecen únicamente **sexo, beca, edad y promedio**; no aparece ninguna variable de lengua indígena o autoadscripción (se revisó solo ICOMPU).

| Variable | Categoría | n | % | ANS | S | SS |
|---|---|---:|---:|---:|---:|---:|
| Sexo | Hombre | 1,544 | 75.72 | 494 | 856 | 194 |
| | Mujer | 495 | 24.28 | 241 | 205 | 49 |
| Beca | Sí | 818 | 40.12 | 310 | 414 | 94 |
| | No | 1,221 | 59.88 | 425 | 647 | 149 |
| Edad | 21 o menos | 54 | 2.65 | 22 | 28 | 4 |
| | 22 a 25 | 1,350 | 66.21 | 471 | 703 | 176 |
| | 26 a 29 | 410 | 20.11 | 156 | 218 | 36 |
| | 30 a 33 | 96 | 4.71 | 37 | 44 | 15 |
| | 34 o más | 129 | 6.33 | 49 | 68 | 12 |
| Promedio autorreportado | 6.0 a 6.9 | 7 | 0.34 | 4 | 3 | 0 |
| | 7.0 a 7.9 | 191 | 9.37 | 81 | 98 | 12 |
| | 8.0 a 8.9 | 1,146 | 56.20 | 449 | 574 | 123 |
| | 9.0 a 10 | 693 | 33.99 | 201 | 384 | 108 |
| | No contestó | 2 | 0.10 | 0 | 2 | 0 |

Cálculo propio: ANS entre mujeres 241 / 495 = 48.7 %; entre hombres 494 / 1,544 = 32.0 %.

**Prácticas profesionales** (tablero «Ámbito escolar», <https://superset.ceneval.edu.mx/superset/dashboard/663/?native_filters_key=IWzGETZyZJE>): utilidad declarada.

| Pregunta | Aún no realizó | Nada | Poco | Regular | Mucho | No contestó |
|---|---:|---:|---:|---:|---:|---:|
| Me ayudaron a aplicar los conocimientos | 457 (22.41 %) | 35 (1.72 %) | 94 (4.61 %) | 494 (24.23 %) | 957 (46.93 %) | 2 |
| Me proporcionaron nuevos conocimientos | 458 (22.46 %) | 32 (1.57 %) | 64 (3.14 %) | 406 (19.91 %) | 1,077 (52.82 %) | 2 |
| Me ayudaron a encontrar trabajo | 466 (22.85 %) | 250 (12.26 %) | 223 (10.94 %) | 512 (25.11 %) | 586 (28.74 %) | 2 |

---

## 5. Datos extraídos de los informes EGEL 2021 (enero a noviembre de 2021)

Informes de marzo de 2022. Solo se leyeron ICOMPU, ISOFT e INFO. Se extrajo el texto de los PDF y se contrastó con el contenido de las gráficas.

### 5.1 Perfil de los sustentantes (sección 2 de cada informe)

| Dato | ICOMPU | ISOFT | INFO |
|---|---:|---:|---:|
| Sustentantes | 1,520 | 1,612 | 1,384 |
| Planteles de IES | 151 | 106 | 146 |
| Hombres / mujeres | 74.6 / 25.4 % | 80.8 / 19.2 % | 68.1 / 31.9 % |
| Edad de 22 a 25 años | 60.9 % | 70.9 % | 56.4 % |
| **Uno de sus padres habla lengua indígena** | **8.9 %** | **3.4 %** | **7.5 %** |
| Trabajan al presentar | 63.3 % | 61.3 % | 67.3 % |
| Obtuvo beca | 51.9 % | 59.2 % | 53.2 % |
| Promedio 9.0 a 10 | 20.6 % | 28.8 % | 21.3 % |
| Promedio 8.0 a 8.9 | 59.5 % | 61.3 % | 61.0 % |
| Promedio 7.0 a 7.9 | 17.7 % | 9.8 % | 17.3 % |
| Promedio 6.0 a 6.9 | 2.2 % | 0.2 % | 0.4 % |
| Computadoras en casa: ninguna | 1.3 % | 0.8 % | 2.0 % |
| una | 46.3 % | 30.4 % | 48.5 % |
| dos | 31.0 % | 27.9 % | 26.4 % |
| tres | 13.5 % | 16.7 % | 13.1 % |
| cuatro o más | 8.0 % | 24.2 % | 10.0 % |

El porcentaje de lengua indígena es sobre el total de sustentantes. Otros porcentajes (trabajo, computadoras) se calculan sobre quienes respondieron esa pregunta (en ICOMPU, n = 1,427).

### 5.2 Testimonios de desempeño

| | ICOMPU | ISOFT | INFO |
|---|---:|---:|---:|
| Sin testimonio | 856 (56.3 %) | 604 (37.5 %) | ≈646 (46.7 %) |
| Testimonio satisfactorio | 495 (32.6 %) | 714 (44.3 %) | 534 (38.6 %) |
| Testimonio sobresaliente | 169 (11.1 %) | 294 (18.2 %) | 204 (14.7 %) |

En INFO el conteo de «sin testimonio» se calculó como 1,384 − 534 − 204.

### 5.3 Niveles de desempeño por área (2021)

**ICOMPU (n = 1,520)**

| Área | ANS | S | SS |
|---|---|---|---|
| Selección de sistemas computacionales para aplicaciones específicas | 794 (52.3 %) | 531 (34.9 %) | 195 (12.8 %) |
| Nuevas tecnologías para la implementación de sistemas de cómputo | 618 (40.7 %) | 807 (53.0 %) | 95 (6.3 %) |
| Desarrollo de hardware y su software asociado para aplicaciones específicas | 630 (41.4 %) | 794 (52.3 %) | 96 (6.3 %) |
| Adaptación de hardware y/o software para aplicaciones específicas | 791 (52.0 %) | 655 (43.1 %) | 74 (4.9 %) |
| Redes de cómputo para necesidades específicas | 585 (38.5 %) | 701 (46.1 %) | 234 (15.4 %) |

**ISOFT (n = 1,612)**

| Área | ANS | S | SS |
|---|---|---|---|
| Análisis de sistemas de información | 487 (30.2 %) | 861 (53.4 %) | 264 (16.4 %) |
| Desarrollo e implantación de aplicaciones computacionales | 583 (36.2 %) | 758 (47.0 %) | 271 (16.8 %) |
| Gestión de proyectos de tecnologías de información | 378 (23.4 %) | 913 (56.7 %) | 321 (19.9 %) |
| Implementación de redes, bases de datos, sistemas operativos y lenguaje de desarrollo | 602 (37.3 %) | 842 (52.3 %) | 168 (10.4 %) |

**INFO (n = 1,384)**

| Área | ANS | S | SS |
|---|---|---|---|
| Detección de las necesidades informáticas de las organizaciones | 546 (39.5 %) | 727 (52.5 %) | 111 (8.0 %) |
| Gestión de proyectos tecnológicos | 482 (34.8 %) | 750 (54.2 %) | 152 (11.0 %) |
| Gestión de la función informática | 623 (45.0 %) | 481 (34.8 %) | 280 (20.2 %) |
| Diseño de soluciones de tecnologías de la información y comunicación | 715 (51.7 %) | 413 (29.8 %) | 256 (18.5 %) |
| Implementación de tecnologías de la información y comunicación | 839 (60.6 %) | 530 (38.3 %) | 15 (1.1 %) |

Nota: en algunas áreas el texto del informe y su gráfica 10 difieren en una décima por redondeo (por ejemplo, en ICOMPU, Selección: 52.3 % en el texto y 52.2 % en la gráfica; 794 / 1,520 = 52.24 %). Aquí se usó el texto del informe.

### 5.4 Ubicación en los PDF (para citar)

| Dato | ICOMPU 2021 | ISOFT 2021 | INFO 2021 |
|---|---|---|---|
| Resumen de sustentantes e IES | Introducción, primer párrafo | Introducción, primer párrafo | Introducción, primer párrafo |
| Datos demográficos y lengua indígena de los padres | Sección 2.1 | Sección 2.1 | Sección 2.1 |
| Computadoras en casa | Sección 2.3, gráfica 5 | Sección 2.3, gráfica 5 | Sección 2.3, gráfica 5 |
| Testimonios | Sección 3.2, gráfica 8 | Sección 3.2, gráfica 8 | Sección 3.2, gráfica 8 |
| Áreas | Sección 3.3, gráficas 10 a 19 | Sección 3.3, gráficas 10 a 17 | Sección 3.3, gráficas 10 a 19 |

---

## 6. Cálculos propios que aparecen en la presentación

| Cifra en la presentación | Cálculo | Resultado |
|---|---|---|
| 12,786 sustentantes (diap. 7) | 940 + 2,039 + 3,275 + 1,457 + 312 + 841 + 3,922 | 12,786 |
| 26 % a 46 % sin nivel satisfactorio (diap. 7) | Mínimo IELEC 26.28 % · máximo IELECTRO 45.54 %, redondeados | 26 % a 46 % |
| Área más débil de cada examen (diap. 8) | Mayor porcentaje de ANS entre las áreas disciplinares de cada examen (tabla 4.3) | ICOMPU redes 55.37 · IMECATRO diseño 52.93 · COMPU algoritmia 51.91 · IELECTRO construcción 51.01 · INFO necesidades informáticas 49.97 · IELEC operación 45.19 · ISOFT análisis 36.03 |
| «Hasta 55 %» y «45 % a 55 %» | Seis de los siete exámenes tienen su área más débil entre 45.19 % y 55.37 %; ISOFT queda en 36.03 % | |
| 27 % → 49 % (diap. 9) | ANS / sustentantes por NSE: A/B 137 / 508 = 26.97 % · D 91 / 186 = 48.92 % | 27 % y 49 % |
| 98 % → 4 % (diap. 9) | Internet fijo que CENEVAL describe para los niveles A/B y D | 98 % y 4 % |
| 14.5 %, 25.7 % y 21.3 % (diap. 12) | 1,084,497 / 7,483,027 · 2,946,052 / 11,456,869 · 4,030,549 / 18,939,896 | 14.49 %, 25.71 %, 21.28 % |
| $18,939,896 (diap. 12) | 7,483,027 + 11,456,869 (Q001 + Q002 en la tabla 3) | 18,939,896 |
| Crecimiento de sustentantes 2021 a 2025 (no está en las diapositivas; se mencionó en el resumen de la investigación) | 2,039 / 1,520 · 3,275 / 1,612 · 1,457 / 1,384 | ICOMPU +34 % · ISOFT +103 % · INFO +5 % |

---

## 7. Datos de las otras fuentes de la presentación

### 7.1 Programa Especial para el Bienestar de Pueblos Indígenas y Afromexicano 2024-2026

Archivos: `programa-especial-del-bienestar-de-pueblos-indigenas-y-afromexicano-2024-2026.pdf` y su transcripción `.md` (raíz del repositorio). Emisor: Gobierno del Estado de Puebla, SPFyA.

| Dato | Ubicación en la transcripción `.md` |
|---|---|
| Estrategia 1.1.1.13 y sus tres líneas, responsable SECIHTI | Líneas 670 a 676 |
| Indicador del Programa: Índice de Rezago Social promedio, CONEVAL, línea base 1 (2020), meta 0.8 (2030) | Después de la estrategia, sección «Indicador» (línea 682) |
| «profunda exclusión» de la infraestructura de conectividad; «2.84 %» | Línea 487 |
| «no existen programas sistemáticos para desarrollar habilidades digitales con pertinencia cultural» | Línea 489 |
| TIC en lenguas indígenas «prácticamente inexistentes» | Línea 491 |
| «falta una apropiación tecnológica con identidad» | Línea 384 |
| 34 municipios con más de 10,000 personas indígenas y su rezago social | Líneas 449 a 462 |

**Advertencia sobre el 2.84 %.** El diagnóstico dice que «el acceso a internet en viviendas [de los municipios indígenas] es de apenas un 2.84 %, menos de la mitad del ya de por sí bajo promedio estatal», sin citar fuente específica (el Programa cita en general el Censo 2020 del INEGI y CONEVAL). **No coincide con la base de indicadores del IPPI** (sección 7.4: mediana municipal de 14.0 % y ningún municipio por debajo de 1.7 %). Por eso la presentación **no usa el 2.84 %**. Una pista no verificada: una búsqueda web ubicó que el boletín de INEGI del Censo 2020 de Puebla reporta 40.4 % de viviendas con internet en el estado (<https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2021/EstSociodemo/ResultCenso2020_Pue.pdf>); ese documento **no se abrió**.

### 7.2 Ley de Egresos del Estado de Puebla para el Ejercicio Fiscal 2026

Archivo: `presupuesto-transversal/PF_LEY DE EGRESOS DEL ESTADO DE PUEBLA, para el Ejercicio Fiscal 2026.pdf` (195 páginas; Periódico Oficial del 4 de diciembre de 2025).

Las cifras se **verificaron visualmente** en las hojas **136 y 137 del PDF** (páginas 137 y 138 impresas del Periódico Oficial). La extracción de texto desordena estas tablas, pero el contraste visual coincide.

| Tabla (Anexo de Transparencia, Apartado E) | Ramo 36 Ciencia, Humanidades y Tecnología | Importe |
|---|---|---:|
| **Tabla 3.** Programas presupuestarios que inciden en la tecnología e innovación (hoja 136) | Total del ramo | 131,074,297 |
| | P011 Impulso a la Simplificación Administrativa | 575,699 |
| | P012 Transformación Digital | 111,558,702 |
| | **Q001 Investigación Científica y Humanística** | **7,483,027** |
| | **Q002 Desarrollo Tecnológico, Innovación y Vinculación Sectorial** | **11,456,869** |
| **Tabla 4.** Programas para el bienestar de pueblos indígenas y afromexicanos (hoja 137) | Total del ramo | 4,030,549 |
| | **Q001** | **1,084,497** |
| | **Q002** | **2,946,052** |

Otros totales: tabla 3 completa 1,982,213,089; tabla 4 completa 3,000,278,997. La suma de P011 + P012 + Q001 + Q002 da exactamente el total del ramo en la tabla 3, y Q001 + Q002 da el total del ramo en la tabla 4.

La Ley **no dice** que los importes de la tabla 4 sean un subconjunto de los de la tabla 3; por eso la diapositiva 12 los presenta como dos cifras comparables y no como un desglose.

Artículos usados: Cap. IX, Art. 84 y 85 (transversalidad, Instancia Rectora, evidencia de cumplimiento) y Sección IV, Art. 95 y 96 (obligaciones de los Ejecutores de Gasto con el IPPI). Detalle y ubicación en [fuentes-y-bases-transversalidad-pueblos-indigenas.md](fuentes-y-bases-transversalidad-pueblos-indigenas.md).

### 7.3 MIR 2026 de SECIHTI

Archivos: `MIR-2026-SECIHTI.pdf` y `MIR-2026-SECIHTI-editar.pdf` (texto idéntico). Páginas 1975 a 2022 de 2317 del Presupuesto de Egresos 2026. Análisis completo en [analisis-mir-2026-secihti.md](analisis-mir-2026-secihti.md).

| Dato de la presentación | Dónde |
|---|---|
| Q002 1.2 (cursos para pueblos indígenas y «afroamericanos»; meta 4; indicador «participantes capacitados»; variable «cursos promovidos»; desagregación «Estatal») | Pág. 2015 |
| Q002 1.3 (4 mesas con IES, «regiones marginadas») | Pág. 2016 |
| Q001 1.1 (22 mesas) | Pág. 2006 |
| Q001 1.4 y 1.5 (cursos y divulgación, sin enfoque indígena) | Págs. 2009 y 2010 |
| P012 trata infraestructura del Ejecutivo estatal, no figura en la tabla 4 | Págs. 1987 a 2005 |
| 58 actividades, solo una menciona pueblos indígenas | Todo el documento |

### 7.4 Base de indicadores de municipios indígenas del IPPI

Archivo: `presupuesto-transversal/INDICADORES MPIOS INDÍGENAS.xlsx` (hojas: MUNICIPIOS, ECONOMÍA, MIGRACIÓN, INFRAESTRUCTURA, GOBERNABILIDAD Y GOBERNANZA, MEDIO AMBIENTE, SALUD, CULTURA, JUSTICIA Y SEGURIDAD, TECNOLOGÍA, LENGUA, EDUCACIÓN, AFROMEXICANA, AFRO). Complemento: `municipios indígenas censo 2020.xlsx`.

Fuentes que cita el propio archivo para la hoja TECNOLOGÍA:
1. INEGI (2021). *Bienes y TIC*. Censo de Población y Vivienda 2020, Tabulados del Cuestionario Básico. <https://www.inegi.org.mx/programas/ccpv/2020/#Tabulados>
2. CFE. *Puntos de WiFi gratuito*. Telecomunicaciones e Internet para Todos. <https://mapa.internetparatodos.cfe.mx/> (responde 403 a consultas automáticas; abrirlo desde el navegador)

**Cómo se calculó** (para reproducirlo en Excel; son 76 municipios, filas 5 a 80 de cada hoja, unidos por la columna «NO.»):
- % de viviendas con internet = hoja TECNOLOGÍA, columna D («Viviendas particulares habitadas que disponen de internet (2020)») ÷ hoja INFRAESTRUCTURA, columna D («Total de viviendas»).
- % con computadora, laptop o tablet = TECNOLOGÍA columna H ÷ INFRAESTRUCTURA columna D.
- Puntos de WiFi gratuito = TECNOLOGÍA columna E.
- En INFRAESTRUCTURA, agua + «sin agua» = total de viviendas, así que el total corresponde a viviendas particulares habitadas.

| Resultado | Valor |
|---|---|
| Mediana municipal de viviendas con internet | **14.0 %** (13.98) |
| Mínimo / máximo | 1.7 % (Chiconcuautla) / 72.5 % (San Andrés Cholula) |
| Municipios con menos de 10 % / menos de 5 % / menos de 20 % | 29 / 8 / 54 (de 76) |
| Mediana municipal de viviendas con computadora, laptop o tablet | **8.3 %** |
| Municipios sin punto de WiFi gratuito de CFE | **8**: Pahuatlán, Tepango de Rodríguez, Zongozotla, Zapotitlán de Méndez, Teopantlán, Chigmecatitlán, Santa Catarina Tlaltempan y Acteopan |
| Total de puntos de WiFi gratuito en los 76 | 1,511 |
| Los ocho municipios con menos internet | Chiconcuautla 1.7 % · Acteopan 2.5 % · Atlequizayan 3.3 % · Camocuautla 3.3 % · Tepango de Rodríguez 3.4 % · Tlaola 4.0 % · Zihuateutla 4.2 % · Olintla 4.6 % |
| Viviendas con internet, ponderado por viviendas (76 municipios) | 46.3 % (483,926 de 1,044,977), arrastrado por Puebla, Atlixco, Amozoc y San Andrés Cholula |
| Igual, sin esos cuatro municipios (72) | 25.4 % |
| Mediana municipal de viviendas con celular / televisor | 71.8 % / 74.6 % |

Control de calidad: ningún valor no numérico, y ningún municipio tiene más viviendas con internet o con computadora que viviendas totales. Un solo nombre cambia de ortografía entre hojas (Santiago Miahuatlán).

La hoja EDUCACIÓN trae «% de aulas con internet» (mediana municipal 16.4 %), pero su fuente es de 2013 (INEGI, Censo de Escuelas, Maestros y Alumnos de Educación Básica y Especial); **no se usó**.

### 7.5 Oficio de invitación

Archivo: `presupuesto-transversal/2026-20-29 - OFICIO CIRCULAR Mesa Técnica de trabajo ippi-secihti.docx` (el nombre del archivo dice «2026-20-29»; el oficio está fechado el 30 de octubre de 2026).

Oficio circular IPPI/DG/008/2026. Invitado: Héctor Guillermo Silva Galindo, Encargado de Despacho de SECIHTI. Firma: Lic. Apolinaria Martínez Arroyo, Directora General. Fecha de la mesa: **miércoles 4 de noviembre de 2026, 12:00 h**, oficinas centrales del IPPI (Boulevard Atlixco 2103, colonia Belisario Domínguez, Puebla), modalidad presencial. El oficio enlista solo las líneas 1.1.1.13.2 y 1.1.1.13.3 en el punto 4 del orden del día.

---

## 8. Limitaciones y cuidados al usar estos datos

1. **Los datos de CENEVAL son nacionales y de quienes presentaron el examen.** No representan a todos los egresados del país y **no están desagregados por pueblo indígena** (solo en 2021 hay una pregunta sobre lengua indígena de los padres).
2. **2021 y 2025 no son comparables en desempeño.** Cambiaron el diseño (EGEL a EGEL Plus), las áreas y el criterio de resultado (testimonios frente a niveles). Además, 2021 cubre hasta noviembre. Solo el número de sustentantes se puede comparar.
3. **El internet por NSE (diapositiva 9) es la referencia de CENEVAL para cada nivel de hogar**, no una medición de los sustentantes. La relación con el desempeño es una asociación, no una causa.
4. **Las áreas de 2025 se asignaron por orden** (sección 4.3). Los conteos cuadran con los totales, pero conviene confirmarlo con los títulos de las gráficas del tablero.
5. **Los tableros pueden actualizarse o cambiar de URL.** Las cifras de este archivo son las que se vieron el 3 de noviembre de 2026. Si CENEVAL publica el informe 2026, la URL probablemente cambie.
6. **En las notas del orador de la presentación** (diapositivas 6 a 14) se repiten la fuente y el método de cada cifra.

## 9. Qué no se revisó (y se podría ampliar)

- Informes de 2016 a 2020 en PDF (para una serie histórica de 10 años) y los tableros de 2022 a 2024.
- Los anuarios estadísticos 2019 a 2023.
- Los cuestionarios de contexto de 2025 de los otros seis exámenes, y la distribución por institución (tablero 694), para ver cuántos sustentantes salen de instituciones de Puebla.
- Si el menú «Download» de Superset permite exportar CSV o Excel sin cuenta.
- Los resultados de EXANI (ingreso) en carreras de tecnología.
- Los PDF de 2021 de COMPU, IELEC, IELECTRO e IMECATRO.
