# Ruta de Aprendizaje TIC — Puntos Críticos 1.1, 1.2 y 1.3

**Objetivo de este documento:** no convertirte en experto, sino que tengas **panorama real** de seguridad informática, recuperación ante desastres e infraestructura de TI — lo suficiente para entender qué estás firmando/implementando en cada documento, tomar mejores decisiones técnicas, y llenar con criterio propio (no solo con plantilla) las secciones `[COMPLETAR]` de los tres borradores.

Todos los cursos listados están **en español**.

---

## Cómo usar esta ruta

- No es necesario terminar un curso completo antes de avanzar el documento correspondiente — puedes ir en paralelo: avanzas el borrador con lo que ya sabes, y conforme el curso te dé más contexto, regresas a mejorar esa sección.
- Sugerencia de ritmo: **2–3 horas por semana**, en el orden de prioridad de abajo (1.1 → 1.2 → 1.3), durante los próximos 3–4 meses. No hace falta ir rápido; lo que importa es que el conocimiento se quede.
- Cada bloque trae primero un **panorama conceptual** (para que entiendas la idea ya, sin esperar al curso) y después el curso para profundizar y practicar.

---

## 1️⃣ Prioridad 1 — Seguridad Informática (Documento 1.1)

### Panorama conceptual (lo esencial en 5 ideas)
1. **No existe la seguridad perfecta**, existe la *reducción de riesgo*: identificas qué es más valioso/vulnerable y proteges eso primero.
2. **La mayoría de los incidentes no son "hackers sofisticados"**, son contraseñas débiles, software sin actualizar, y personas que dan clic en un enlace (phishing). Por eso el protocolo dedica tanto espacio a contraseñas, parches y capacitación.
3. **Defensa en capas (defense in depth):** ninguna medida sola basta — antivirus + firewall + backups + capacitación se complementan, si una falla las otras contienen el daño.
4. **El firewall es la puerta de tu red**, no un antivirus: decide qué tráfico entra/sale. pfSense es de los más usados porque es gratuito y muy documentado.
5. **Seguridad ≠ solo tecnología:** un procedimiento claro de "qué hacer si algo raro pasa" (sección 6 del borrador 1.1) frecuentemente importa más que la herramienta.

### Cursos recomendados
| Curso | Por qué | Enlace | Estado |
|---|---|---|---|
| Seguridad Informática en Servidores Linux: Hardening | Práctico, defensa en profundidad aplicada a servidores reales | [Ver curso](https://www.udemy.com/course/seguridad-informatica-servidores-linux-hardening-defensa-blueteam/) | ✅ Comprado — en progreso |
| pfSense: Instalación y configuración con Práctica | Para entender y montar tú mismo un firewall perimetral (punto 5.4 del protocolo) | [Ver curso](https://www.udemy.com/course/firewall-pfsense-redes-ciberseguridad-walter-coto-alvaro-chirou/) | ⬜ Pendiente |
| ISO/IEC 27001 Sistema de Gestión Seguridad de la Información | Para que el protocolo tenga respaldo de estándar internacional reconocido | [Ver curso](https://www.udemy.com/course/sistema-de-gestion-de-seguridad-de-la-informacion-iso-27001/) | ⬜ Pendiente |

---

## 2️⃣ Prioridad 2 — Plan de Recuperación ante Desastres (Documento 1.2)

### Panorama conceptual
1. **RTO (Recovery Time Objective):** ¿cuánto tiempo puede estar caído un sistema antes de que sea un problema serio? (ej. el SIG IN-TI a 4 horas).
2. **RPO (Recovery Point Objective):** ¿cuánta información puedes permitirte "perder" desde el último respaldo? (ej. 24 horas = si haces respaldo diario, en el peor caso pierdes lo capturado ese día).
3. **Regla 3-2-1:** 3 copias de tu información, en 2 medios distintos, con 1 copia fuera de la sede — así un incendio u ocurra ahí ya no destruye también el respaldo.
4. **Un respaldo que nunca se ha restaurado es una suposición, no un respaldo.** Por eso el borrador exige pruebas trimestrales: es el paso que casi todas las organizaciones se saltan y el que evita la peor sorpresa.
5. **BIA (Business/Análisis de Impacto):** antes de definir cómo recuperar, hay que saber qué sistema es más crítico — no todo puede ser "prioridad máxima".

### Cursos recomendados
| Curso | Por qué | Enlace | Estado |
|---|---|---|---|
| Plan de Recuperación ante Desastres: Todo lo que necesitas | Coincide casi directo con la estructura del documento 1.2 | [Ver curso](https://www.udemy.com/course/plan-de-recuperacion-ante-desastres-todo-lo-que-necesitas/) | ⬜ Pendiente |
| Gestión de respaldos para la continuidad de negocio | Enfoque práctico de estrategia de backup (sección 5 del DRP) | [Ver curso](https://www.udemy.com/course/gestion-de-respaldos-para-la-continuidad-de-negocio/) | ⬜ Pendiente |
| ISO 22301 - Gestión de la Continuidad del Negocio | Más metódico: BIA, análisis de riesgo, formatos de plan formales | [Ver curso](https://www.udemy.com/course/iso-22301-gestion-de-la-continuidad-del-negocio/) | ⬜ Pendiente |
| Gestión de Incidentes y Crisis edición 2024 | Complementa la sección 9 (comunicación en crisis) del borrador | [Ver curso](https://www.udemy.com/course/gestion-de-incidentes-y-crisis/) | ⬜ Pendiente |

---

## 3️⃣ Prioridad 3 — Infraestructura de TIC (Documento 1.3)

### Panorama conceptual
1. **Todo diagnóstico de infraestructura empieza por un inventario y un diagrama de red** — si no sabes qué tienes y cómo está conectado, no puedes priorizar mejoras con criterio (por eso la tabla `[COMPLETAR]` del borrador 1.3 es la base de todo lo demás).
2. **La disponibilidad depende tanto de energía como de red:** un servidor perfecto sirve de poco si un corte de luz en la sierra lo tumba — por eso UPS/reguladores aparecen como "prioridad inmediata" en la matriz.
3. **Segmentar la red reduce el daño de un incidente:** separar la red administrativa de la red de invitados/Módulos evita que un problema en un extremo se propague a todo.
4. **No toda mejora cuesta lo mismo ni da el mismo beneficio** — de ahí la matriz impacto/esfuerzo: hay mejoras baratas y de alto impacto (documentar, UPS) antes que otras costosas (segundo enlace de internet).

### Cursos recomendados
| Curso | Por qué | Enlace | Estado |
|---|---|---|---|
| Redes con Linux para Entornos Corporativos y Servidores | Base técnica: TCP/IP, DNS, permisos, automatización con Bash | [Ver curso](https://www.udemy.com/course/redes-con-linux/) | ⬜ Pendiente |
| CCNA - Fundamentos y administración de redes Cisco | Diseño de red desde cero: cómo pensar arquitectura, no solo configurarla | [Ver curso](https://www.udemy.com/course/ccna-fundamentos-y-administracion-de-redes-cisco/) | ⬜ Pendiente |

---

## 🎯 Siguiente nivel (opcional, cuando tengas los 3 documentos avanzados)

**[Curso completo de Hacking Ético y Ciberseguridad](https://www.udemy.com/course/curso-completo-de-hacking-etico-y-ciberseguridad/)** (Santiago Hernández)

Muy práctico (Kali Linux, casos reales) y te permite **auditar tú mismo** lo que implementaste en el punto 1.1 — ver tu red con ojos de atacante para confirmar que los controles realmente funcionan. Es largo y orientado a pentesting, por lo que rinde más *después* de tener las bases de hardening/redes, no antes. Úsalo solo contra tu propia infraestructura o con autorización explícita.

---

## Resumen de ritmo sugerido

| Mes | Enfoque |
|---|---|
| Mes 1 | Panorama de seguridad (leer conceptos arriba) + iniciar curso de Hardening o pfSense, en paralelo con avanzar el documento 1.1 |
| Mes 2 | Terminar seguridad + iniciar curso de DRP/backups, en paralelo con el documento 1.2 |
| Mes 3 | Terminar DRP + iniciar Redes/CCNA, en paralelo con el documento 1.3 (empezar por el inventario) |
| Mes 4 | Consolidar, y si el tiempo lo permite, Hacking Ético como profundización |

---
*Documento de apoyo generado con Claude Code — complementa los borradores [1.1](1.1%20Protocolo%20de%20Seguridad%20Informatica%20-%20Borrador.md), [1.2](1.2%20Plan%20de%20Recuperacion%20ante%20Desastres%20-%20Borrador.md) y [1.3](1.3%20Plan%20de%20Mejora%20de%20Infraestructura%20TIC%20-%20Borrador.md).*
