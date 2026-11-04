# Fuentes y datos CONEVAL para la presentación de la Mesa Técnica IPPI–SECIHTI (sustituye a CENEVAL)

**Área:** Subdirección de Desarrollo de Tecnologías de la Información, IPPI
**Fecha de elaboración:** 3 de noviembre de 2026 (consultas web y descargas hechas ese día)
**Presentación asociada:** `2026-11-04 - presentacion-mesa-tecnica-ippi-secihti.pptx`. **Actualizada el 3 de noviembre de 2026** con CONEVAL en lugar de CENEVAL y con el alcance de la mesa limitado a las líneas 1.1.1.13.2 y 1.1.1.13.3 (cambios reales en la sección 7; la tabla de ahí era la propuesta inicial y se ajustó al ejecutarla).
**Reemplaza a:** [fuentes-y-datos-ceneval-mesa-tecnica-ippi-secihti.md](fuentes-y-datos-ceneval-mesa-tecnica-ippi-secihti.md) en lo que toca a las diapositivas 7 a 10. Lo demás de ese archivo (secciones 7.1 a 7.5: Programa Especial, Ley de Egresos, MIR, base del IPPI, oficio) sigue vigente.
**Abreviaturas:** IRS = Índice de Rezago Social · PI = población indígena (definición de CONEVAL) · HLI = hablante de lengua indígena · HLI/PI no son lo mismo (ver 3.1).

---

## 1. Hallazgo principal (lo que hay que saber antes de cambiar diapositivas)

1. **CONEVAL no mide internet ni acceso a tecnología.** Ninguno de sus productos (pobreza multidimensional, IRS) incluye una variable de internet, computadora o conectividad. Buscar un «indicador CONEVAL de rezago tecnológico» no llevará a ningún lado. El acceso a TIC sale del Censo 2020 de INEGI, que **ya está en la base del IPPI** (hoja TECNOLOGÍA).
2. **Lo que CONEVAL sí aporta, y es lo que le sirve a la mesa:**
   - El **IRS es el indicador del propio Programa Especial** (diapositiva 3: «1 a 0.8, 2020-2030»). Tiene sentido que la presentación use la fuente del indicador.
   - CONEVAL publica pobreza y carencias **por municipio y para población indígena** (2010, 2015, 2020). Esto permite hacer, por primera vez en la presentación, una **medición de la población indígena** (la de CENEVAL era nacional y de egresados).
3. **El cruce propio (sección 4) es el dato nuevo:** en los 76 municipios, a mayor rezago social CONEVAL, menos internet y computadoras (correlación de −0.75 y −0.82). El «rezago tecnológico» se puede mostrar como **parte del rezago social que el Programa se propone reducir**, con CONEVAL como fuente del rezago e INEGI como fuente de la conectividad.
4. **CONEVAL dejó de existir como institución medidora en 2025** (sección 6). Los datos municipales de 2020 siguen siendo los más recientes con desagregación municipal; hay que decir «CONEVAL 2020» y no «actual».

---

## 2. Qué dato usa cada diapositiva (versión CONEVAL)

| Diap. | Dato | Fuente | Sección |
|---|---|---|---|
| 3 | Meta del Programa: IRS promedio 1 (2020) → 0.8 (2030) | Programa Especial 2024-2026 | (sin cambio; ver 4.6) |
| 6 | 14 % internet, 1.7 % a 72 %, 29 de 76, 8 sin WiFi, 8 % computadora | Base IPPI (INEGI Censo 2020, CFE) | (sin cambio; ver 4.1) |
| 7 (nueva) | Pobreza de la población indígena en los 76 municipios: mediana 85 %, 61 de 76 con 80 % o más | CONEVAL, pobreza municipal 2020, población indígena | 4.3 |
| 8 (nueva) | Internet y computadora según grado de rezago social | CONEVAL IRS 2020 + base IPPI | 4.2 |
| 9 (nueva) | Municipios tipo 1 frente a tipo 2: internet, computadora, IRS, pobreza | Base IPPI (clasificación) + CONEVAL | 4.4 |
| 10 (nueva) | Rezago educativo de la PI (mediana 36 %) y límites de la información | CONEVAL + MIR 2026 | 4.5 y 5 |

---

## 3. Fuentes CONEVAL y su descarga

Todo se descargó con `curl` desde el portal de CONEVAL y se guardó en [coneval-descargas/](coneval-descargas/). Los enlaces responden a 3 de noviembre de 2026.

### 3.1 Archivos usados

| # | Qué es | Enlace | Archivo local | Contenido útil |
|---|---|---|---|---|
| 1 | **IRS 2020, entidades y municipios (2000–2020)** | <https://www.coneval.org.mx/Medicion/Documents/IRS_2020/IRS_ent_mun_2000_2020.zip> | `coneval-descargas/irs2020/IRS_entidades_mpios_2020.xlsx` (hoja *Municipios*) | Por municipio: población, 11 indicadores, IRS, grado y lugar nacional. Página de origen: <https://www.coneval.org.mx/Medicion/IRS/Paginas/Indice_de_Rezago_Social_2020_anexos.aspx> |
| 2 | **Pobreza municipal 2020 por grupos poblacionales** (incluye *pobindigena*) | <https://www.coneval.org.mx/Medicion/Documents/Pobreza_municipal/2020/gpos_pob/Indicadores_pobreza_grupos_municipal.zip> | `coneval-descargas/pobreza-municipal-2020/grupos/Indicadores_pobreza_grupos_municipal.xlsx` (hoja *pobindigena*) | Por municipio, para la población indígena: pobreza, ingreso, las seis carencias, 2010/2015/2020, con indicador de precisión estadística (✔ ⚠ ❌). Página de origen: <https://www.coneval.org.mx/Medicion/Paginas/Pobreza_grupos_poblacionales_municipal_2010_2020.aspx> |
| 3 | **Pobreza municipal 2020, población total** | <https://www.coneval.org.mx/Medicion/Documents/Pobreza_municipal/2020/Concentrado_indicadores_de_pobreza_2020.zip> | `coneval-descargas/pobreza-municipal-2020/concentrado/Concentrado_indicadores_de_pobreza_2020.xlsx` | Pobreza, pobreza extrema, carencias, 2010-2020. Página de origen: <https://www.coneval.org.mx/Medicion/Paginas/Pobreza-municipio-2010-2020.aspx> |
| 4 | Metodología y síntesis de población indígena | <https://www.coneval.org.mx/Medicion/Documents/Pobreza_municipal/2020/gpos_pob/Metodologia_pobreza_grupos_municipal.pdf> y <https://www.coneval.org.mx/Medicion/Documents/Pobreza_municipal/2020/gpos_pob/Sintesis_pobreza_PI_municipal.pdf> | `coneval-descargas/metodologia/` | Definición de PI y contexto nacional |

**Definición de población indígena de CONEVAL** (síntesis, p. 3): todas las personas de un hogar donde el jefe(a), su cónyuge o algún ascendiente declaró hablar lengua indígena, más las personas que declararon hablar lengua indígena y no están en esos hogares. **Es más amplia que «hablantes de lengua indígena»**; por eso no se debe comparar directamente con el 9.9 % de HLI del Censo.

**Variables del IRS 2020** (columnas del archivo 1): analfabetismo 15+; 6 a 14 años sin escuela; 15+ con educación básica incompleta; sin derechohabiencia a salud; vivienda con piso de tierra, sin excusado, sin agua entubada, sin drenaje, sin electricidad, sin lavadora, sin refrigerador. **No incluye internet ni computadora.** Está construido con el Censo 2020.

### 3.2 Otras fuentes consultadas

| Fuente | Enlace | Para qué |
|---|---|---|
| INEGI, boletín Censo 2020 Puebla (comunicado 50/21) | <https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2021/EstSociodemo/ResultCenso2020_Pue.pdf> | Comparativo estatal (sección 4.1). **Sí se abrió y leyó**. |
| CONEVAL, interactivo y descargas municipales | <https://municipal-coneval.hub.arcgis.com/pages/descargas> | Aparece en la búsqueda; no se abrió. Ruta alterna si cambian los enlaces. |
| CONEVAL, bases y programas de cálculo municipal | <https://www.coneval.org.mx/Medicion/Paginas/Programas_BD_municipal_2010_2020.aspx> | No se abrió. Permitiría bases a nivel persona. |
| CONEVAL, IRS 2020 (resultados) | <https://www.coneval.org.mx/Medicion/Documents/IRS_2020/Nota_principales_resultados_IRS_2020.pdf> | No se abrió. |

---

## 4. Datos y cálculos propios (los 76 municipios de la base del IPPI)

**Archivo del cruce:** [cruce-coneval-tecnologia-76-municipios.xlsx](cruce-coneval-tecnologia-76-municipios.xlsx) (una fila por municipio; hoja FUENTES con el origen de cada columna).

**Método.** Los 76 municipios de la hoja TECNOLOGÍA se unieron con los archivos CONEVAL por nombre de municipio normalizado dentro de Puebla (clave estatal 21). **Coincidieron los 76, sin duplicados.** Las dos columnas de internet y computadora son las ya calculadas en la base del IPPI (viviendas con internet o con computadora entre total de viviendas). La clasificación (columna F de la hoja MUNICIPIOS) separa **58 municipios tipo 1 (indígenas, 40 % o más)** y **18 tipo 2 (con presencia indígena)**; juntos son exactamente los 76 de la hoja TECNOLOGÍA. Los 141 municipios tipo 3 (población indígena dispersa) **no tienen datos de tecnología en la base**.

### 4.1 Contexto estatal (INEGI, Censo 2020, Puebla)

| Indicador | Estado de Puebla | 76 municipios IPPI |
|---|---:|---:|
| Viviendas con internet | 40.4 % | mediana 14.0 %; ponderado 46.3 %, y 25.4 % sin Puebla, Atlixco, Amozoc y San Andrés Cholula |
| Viviendas con computadora o laptop | 29.6 % | mediana 8.3 % |
| Viviendas con celular | 84.4 % | mediana 71.8 % |
| HLI de 3 años o más | 615,622 (9.9 %) | no calculado |

**Cuidado:** el estatal es un porcentaje global; los de los 76 son medianas municipales (cada municipio pesa igual). La comparación válida y honesta es «el municipio mediano tiene 14 % frente a 40 % del estado», y debe decirse así. En 2010, el estado tenía 14.6 % de internet: el municipio indígena mediano de 2020 está donde el estado estaba hace diez años (observación a partir de ese dato del boletín).

### 4.2 Rezago social (IRS CONEVAL 2020) y conectividad

Grado de rezago social de los 76 municipios y su conectividad (mediana):

| Grado de rezago | Municipios | Mediana % internet | Mediana % computadora |
|---|---:|---:|---:|
| Muy alto | 8 | 7.0 | 3.1 |
| Alto | 23 | 7.9 | 4.7 |
| Medio | 25 | 14.0 | 9.4 |
| Bajo | 17 | 26.5 | 18.2 |
| Muy bajo | 3 | 63.9 | 49.4 |

- Correlación entre el IRS y el % de viviendas con internet: **−0.75** (Pearson; −0.72 Spearman). Con computadora: **−0.82**.
- **31 de los 76** tienen rezago alto o muy alto. **20 de esos 31** tienen menos de 10 % de viviendas con internet.
- El estado de Puebla tiene IRS 2020 de 0.744, grado de rezago **Alto**, lugar 5 nacional (hoja *Estados* del mismo archivo).
- Municipios de rezago muy alto: Olintla (internet 4.6 %), Coyomeapan (5.4 %), Eloxochitlán (5.9 %), Vicente Guerrero (6.3 %), Zoquitlán (7.8 %), San Sebastián Tlacotepec (10.9 %), Tepetzintla (11.5 %), Hueytlalpan (25.9 %).
- Los 8 municipios **sin WiFi gratuito de CFE** son de rezago alto (Acteopan, Tepango, Zongozotla, Teopantlán) o medio (Pahuatlán, Zapotitlán de Méndez, Chigmecatitlán, Santa Catarina Tlaltempan).

*Límite:* es una correlación entre municipios (ecológica), no una causa. Además el IRS incluye variables de vivienda que pueden compartir causas con la falta de internet (aislamiento, ingreso). Se puede decir «coinciden», no «el rezago causa la falta de internet».

### 4.3 Pobreza de la población indígena (CONEVAL 2020)

- **Mediana municipal: 84.8 %** de la PI en situación de pobreza; mínimo 59.6 %, máximo 95.9 %. **61 de 76** municipios tienen 80 % o más.
- Ponderando por población indígena (979,717 personas en los 76 según CONEVAL): **81.8 %**.
- Las estimaciones de los 76 tienen la marca de precisión **✔ (con precisión)** tanto en pobreza como en rezago educativo.
- Comparación estatal: una búsqueda web reportó que, en 2020, 81.99 % de los HLI de Puebla estaban en pobreza, con 62.43 % de pobreza estatal general (fuente en 6; **no verificada en el original**). Es coherente con el 81.8 % calculado.
- Los municipios con menos internet son también de pobreza indígena alta: Chiconcuautla (1.7 % internet, 93.4 % pobreza PI), Acteopan (2.5 %, 89.7 %), Tepango de Rodríguez (3.4 %, 95.9 %, el máximo).
- Correlación entre pobreza de la PI e internet: −0.56. Con rezago educativo de la PI: −0.43 (más débil).

### 4.4 Municipios tipo 1 frente a tipo 2

| | Tipo 1 (indígenas, n = 58) | Tipo 2 (presencia, n = 18) |
|---|---:|---:|
| Mediana % internet | 10.1 | 25.0 |
| Mediana % computadora | 6.2 | 17.9 |
| Municipios con menos de 10 % de internet | 28 | 1 |
| Municipios sin WiFi gratuito CFE | 8 | 0 |
| IRS promedio 2020 | **1.00** | −0.20 |
| Mediana pobreza población total | 84.2 % | 71.5 % |
| Mediana pobreza PI | 86.4 % | 80.8 % |
| Mediana % PI con carencia de servicios básicos | 69.4 % | 45.8 % |

**Lectura:** el rezago tecnológico es **un problema casi exclusivo de los municipios tipo 1**: 28 de los 29 municipios con menos de 10 % de internet y los 8 sin WiFi son del tipo 1. Esto da una razón objetiva para priorizar la clasificación del IPPI en las líneas 13.1 y 13.2.

### 4.5 Rezago educativo de la población indígena (CONEVAL 2020)

Mediana municipal de PI con carencia por rezago educativo: **35.8 %** (tipo 1: 37.2 %; tipo 2: 32.4 %). Es el insumo CONEVAL más cercano a la línea 13.2 (formación). Rezago educativo en CONEVAL = carencia educativa por edad (sin asistencia, sin educación básica según cohorte), **no mide habilidades digitales**.

### 4.6 Coincidencia con la línea base del Programa

El Programa Especial fija como línea base **IRS promedio = 1 (2020)** para los municipios indígenas. El promedio simple del IRS 2020 de los 58 municipios tipo 1 es **1.002**. Es consistente con esa línea base, lo que sugiere que el Programa usa los municipios tipo 1; **es una inferencia, no una confirmación**: el Programa no detalla el universo ni la forma de promediar. Conviene preguntarlo antes de afirmarlo en la mesa.

---

## 5. Limitaciones y cuidados

1. **CONEVAL no tiene datos de internet ni de habilidades digitales.** La presentación debe decir que el acceso a TIC viene del Censo 2020 (INEGI) y que CONEVAL aporta el rezago social y la pobreza. No titular «rezago tecnológico según CONEVAL».
2. **Los datos municipales son de 2020** (Censo y modelo estadístico de ENIGH). Después de 2020 hubo medición estatal de CONEVAL 2022 y de INEGI 2024, pero **sin desagregación municipal**; no se usan para los 76 municipios.
3. **El IRS es relativo:** mide la posición entre municipios del país, no un nivel absoluto. Su meta (de 1 a 0.8) es una mejora de posición relativa.
4. **El cruce es asociación entre municipios**, no causalidad ni comportamiento individual.
5. **Estimaciones de CONEVAL por grupo poblacional tienen precisión estadística variable**; en los 76 municipios todas las usadas están marcadas ✔. En otros municipios hay ⚠ y ❌ (Excel trae el símbolo junto a cada cifra).
6. **Nombres:** la unión es por nombre normalizado. Se verificó que los 76 coinciden y que no hay claves repetidas, pero no se contrastó contra una tabla oficial de claves INEGI de la base del IPPI (la base no trae clave).
7. **Los tipo 3 (141 municipios) no están en el análisis tecnológico** por falta de datos en la base.

---

## 6. Estado institucional de CONEVAL y datos de búsqueda sin verificar

| Dato | Fuente reportada por la búsqueda | Estado |
|---|---|---|
| Las atribuciones de medición de pobreza pasaron de CONEVAL a INEGI; reforma publicada el 17 de julio de 2025 | Resultado de búsqueda (CEIGEP Puebla / SNIEG: <https://www.snieg.mx/Documentos/CONSEJO/sesiones/doc_22025/2_ppt_ccn.pdf>) | No verificado en el texto de la reforma |
| INEGI publicó la medición de pobreza 2024 el 13 de agosto de 2025: 38.49 millones de personas en pobreza (nacional) | <https://www.nmas.com.mx/nacional/porcentaje-inegi-pobreza-mexico-2025-cuantas-personas-viven-esta-situacion-cifra/> | No verificado en INEGI |
| Puebla, serie de pobreza 2016–2024: 50.2, 49.9, 49.7, 42.6 y 36.1 % (36.1 sería 2024) | <https://www.inegi.org.mx/contenidos/desarrollosocial/pm/doc/pm_infog_21_2024.pdf> | Interpretación del año no confirmada; **no usar sin abrir la infografía** |
| Pobreza estatal 2020 Puebla 62.43 % y 81.99 % de HLI en pobreza | <https://ceigep.puebla.gob.mx/docs/boletines/coneval-2020.pdf> | No abierto |
| Puebla, 54.0 % de pobreza y 11.4 % de extrema en 2022 (un medio) frente a 62 % y 13 % (documento estatal) | resultados de búsqueda | **Contradictorio. No usar** |

---

## 7. Cómo cambiaría la presentación (propuesta; el pptx no se tocó)

Lo que **ya no debe aparecer** (CENEVAL): EGEL, 12,786 sustentantes, niveles de desempeño, áreas débiles, NSE, lengua indígena de padres 2021. Afecta las diapositivas **7, 8, 9 y 10**, el título de la sección 1 (diapositiva 5, notas «datos de referencia de CENEVAL»), la nota de la diapositiva 6 si menciona CENEVAL y las notas del orador.

| Diap. actual | Propuesta CONEVAL |
|---|---|
| 7. «Brechas de desempeño EGEL Plus 2025» | **«Dónde falta más conectividad es donde hay más rezago social»**: gráfica de barras de mediana de internet por grado de rezago (7.0 / 7.9 / 14.0 / 26.5 / 63.9 %) y dos cifras: «−0.75» y «20 de 31 municipios de rezago alto con menos de 10 % de internet». Fuente: CONEVAL IRS 2020 + base IPPI. |
| 8. «Área más débil de cada examen» | **«La pobreza de la población indígena en los 76 municipios»**: mediana 85 %; 61 de 76 con 80 % o más; ponderado 81.8 %. Fuente: CONEVAL 2020, población indígena. Sirve para justificar por qué la línea 13.2 debe atender a esta población. |
| 9. «Menor NSE: menos internet» | **«El rezago tecnológico se concentra en los municipios indígenas (tipo 1)»**: tabla de 4.4. 28 de 29 con menos de 10 % de internet y los 8 sin WiFi son tipo 1; mediana de 10 % frente a 25 %. |
| 10. «Sin desagregación por pueblo no hay seguimiento posible» | Conservar el mensaje con datos CONEVAL: **meta del Programa = IRS (CONEVAL)** y línea base 1.002 de los tipo 1, **pero el IRS no mide tecnología**: proponer a la mesa un **indicador complementario de conectividad (INEGI Censo)**. Mantener el recuadro de la MIR («Estatal», sin pueblo ni municipio). Quitar el recuadro «En 2025…» y los 8.9 %, 7.5 % y 3.4 %. |

**Mensaje para la mesa (una frase):** «La meta del Programa es bajar el Índice de Rezago Social; donde ese índice es más alto es también donde hay menos internet y computadoras; por eso la Estrategia 1.1.1.13 es una palanca para la meta y debe medirse».

**Cuidado de redacción:** el IRS no contiene internet, de modo que no puede afirmarse que instalar infraestructura baje el IRS. Se puede afirmar que coinciden geográficamente y que la meta del Programa es relativa.

---

## 8. Pendientes (lo que no se alcanzó o conviene hacer)

1. **Confirmar con el área de planeación del IPPI** qué universo y qué promedio usa el Programa para su línea base «1» (sección 4.6).
2. **Abrir y verificar** los datos de la sección 6 antes de usarlos (infografía INEGI 2024 y el boletín del CEIGEP).
3. **Tipo 3:** descargar del Censo 2020 los tabulados de internet y computadora de los 141 municipios con población dispersa (<https://www.inegi.org.mx/programas/ccpv/2020/#Tabulados>) para completar los 217.
4. **Serie 2010 → 2020 de internet** en los 76 (Censo 2010 y 2020) para mostrar crecimiento; no se hizo.
5. **Pobreza 2020 por carencia de la PI por pueblo**: CONEVAL solo desagrega por municipio. Para pueblo (náhuatl, totonaco, mazateco…) habría que cruzar la lengua dominante por municipio (hoja LENGUA de la base del IPPI). No se hizo.
6. **ENDUTIH (INEGI)** mide uso de internet por persona y por hablante de lengua indígena a nivel nacional/estatal. Es la fuente adecuada para uso (no solo acceso) y no se consultó.
7. Actualizar las diapositivas 5 a 10 y sus notas, y revisar que el pptx no conserve rastros de CENEVAL (el archivo estaba abierto en otro equipo, con candado `~$`).

*Archivos descargados* (en [coneval-descargas/](coneval-descargas/)): unos 48 MB entre ZIP, Excel descomprimidos y PDF. Si no se quieren en el repositorio, se pueden volver a bajar con los enlaces de la sección 3.
