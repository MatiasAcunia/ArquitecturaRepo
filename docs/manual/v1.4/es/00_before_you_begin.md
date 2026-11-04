# 00 — Antes de empezar

ArquitecturaRepo · Manual completo de uso · Edición v1.4 · Español

> Este capítulo presenta la finalidad, los límites y las responsabilidades del sistema. Corresponde a la [versión pública v1.4.0](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0). Su contenido es una guía de uso, no una prueba de que una aplicación particular haya sido construida, asegurada o aceptada. Los comandos vigentes se encuentran en la [guía de primera instalación](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md) y las [notas de release](../../../47_V1_4_RELEASE_NOTES_AND_UPGRADE.md).

## Contenido del capítulo

1. Qué vas a instalar y qué no
2. Quién toma cada decisión
3. La información que debe permanecer accesible
4. Cómo leer el manual completo
5. Preparación: las decisiones que sí son tuyas
6. Alcance, límites y versiones
7. Un recorrido de extremo a extremo
8. Decisiones habituales y sus responsables
9. Ficha de arranque de una página
10. Cómo evaluar si el sistema te está ayudando

## 1. Qué vas a instalar y qué no

ArquitecturaRepo es un starter público y portable de control de ingeniería. Reúne protocolos de operación, plantillas, perfiles de instalación, contratos comprobables, herramientas Python de validación y recuperación, y un controlador local de campañas opcional. Su función es mantener organizado un proyecto de software incluso cuando el trabajo pasa entre personas, agentes de programación, revisores y conversaciones nuevas.

No es una aplicación ya terminada ni un servicio al que le entregás una idea y recibís automáticamente un producto validado. Instalarlo no programa la aplicación, no crea un equipo de agentes competente por sí solo y no reemplaza las decisiones del dueño del producto. La aplicación que quieras construir necesita sus propios requisitos, elecciones técnicas, implementación real, pruebas, análisis de riesgos y aceptación.

La versión pública se identifica mediante un tag y artefactos de release concretos, no únicamente por el texto de un README. La v1.4.0 se publicó con un ZIP portable, checksum SHA-256 y manifest. Antes de instalar un archivo descargado, verificá su identidad. La rama `main` puede contener correcciones posteriores que no forman parte del ZIP ya publicado. Que el framework haya pasado sus pruebas significa que fueron comprobados ciertos mecanismos del framework: no demuestra que funcione una aplicación distinta construida con ellos.

El repositorio contiene ejemplos sintéticos y una aplicación de referencia para ejercitar partes del sistema. Esos ejemplos no son un Product State real, ni requisitos confirmados de una empresa, ni resultados que deban copiarse como si fueran tuyos. Cuando una capacidad de tu aplicación todavía no se verificó físicamente, corresponde dejarla como desconocida, pendiente o bloqueada según el caso; no marcarla como terminada porque un agente lo anunció.

El beneficio buscado es continuidad. Una sesión nueva tendría que poder inspeccionar evidencia durable y reconstruir qué producto se desarrolla, qué decisiones siguen vigentes, qué versión del código y del estado técnico es actual, qué trabajo está autorizado, qué se comprobó realmente y cuál es la próxima acción válida. Los chats pueden terminar, los servicios pueden cambiar y un agente puede perder contexto. El proyecto no debería exigir que alguien recuerde toda la conversación anterior.

En los ejemplos se usan Windows, GitHub, Python y agentes conversacionales porque son un punto de partida conocido. No son dependencias universales: se puede trabajar en otro sistema operativo, con otra pila tecnológica o exclusivamente con personas. Los modelos externos, APIs pagas, credenciales y servicios de nube son opciones separadas, que requieren configuración y autorización específica.

Hay tres afirmaciones que nunca conviene confundir:

- El starter puede instalarse y sus mecanismos portables pasan sus propias comprobaciones.
- Tu aplicación adoptó el starter mediante requisitos, autoridades y estado actuales coherentes.
- Tu aplicación cumple sus funciones, seguridad, confiabilidad y expectativas de uso.

La primera afirmación no demuestra las otras dos. Una instalación puede estar correctamente en `HOLD / UNTRUSTED_CONTEXT` sin que eso signifique que haya fallado; significa que todavía falta reconstruir y confirmar el proyecto real.

## 2. Quién toma cada decisión

La arquitectura distribuye responsabilidades, no impone una cantidad fija de personas, modelos o ventanas de chat. Un proyecto pequeño puede funcionar con una persona dueña del producto, un rol de planificación y un ejecutor. Separar un Master Owner cobra sentido cuando existen productos diferentes, recursos compartidos, políticas transversales o fronteras de coordinación reales. Abrir otra conversación con el título «Master Owner» no crea por sí mismo esa necesidad.

| Participante | Responsabilidad principal | Qué no debería resolver rutinariamente |
| --- | --- | --- |
| CLIENT / dueño del producto | Problema, usuarios, prioridades, reglas de negocio, experiencia esperada, presupuesto, publicación y demás autorizaciones reservadas. | Conflictos de Git, esquemas internos, estrategia de tests o reparación de currentness. |
| I1 · Master Owner, cuando corresponde | Coherencia entre productos, recursos compartidos, problemas sistémicos, capacidad y fronteras de ownership. | Sustituir al Planner o coordinar cada pequeña tarea. |
| I2 · Planner | Interpretación del producto, estrategia, arquitectura, límites de capacidades, charters y auditoría estratégica. | Convertirse en el bucle de depuración o escribir un nuevo charter por cada bug. |
| I3 · Execution Controller / Campaign Lead | Implementación, integración, reintentos, depuración, revisión independiente, checkpoints y recuperación dentro de la campaña autorizada. | Inventar reglas de negocio o aprobar unilateralmente su resultado final. |
| I4 · Especialistas de ejecución | Código, investigación acotada, pruebas, revisión técnica y evidencia vinculada a la fuente. | Reemplazar decisiones del CLIENT o declarar aceptación estratégica. |

El dueño del producto puede rechazar una interfaz que resulta confusa aunque las pruebas automáticas sean verdes. Un revisor técnico puede rechazar un candidato que no conserva los datos. El Planner evalúa si la capacidad cumple las condiciones estratégicas del charter. Son decisiones relacionadas, pero una no reemplaza silenciosamente a otra.

En un flujo posible, ChatGPT ayuda a planificar y Codex modifica el repositorio. Es un ejemplo, no una obligación de utilizar una plataforma ni una suscripción. El rol depende de su autoridad y de las evidencias que debe producir. Una misma persona puede cubrir varias responsabilidades acotadas, siempre que se respeten los conflictos de interés y las necesidades reales de revisión independiente.

## 3. La información que debe permanecer accesible

Para averiguar el estado técnico, empezá por el código, los artefactos y el entorno que realmente existen. Contrastalos con el Product State canónico, los requisitos actuales, la autoridad de campaña y, cuando importa, las evidencias de DB y runtime. Un resumen viejo del chat, aun si dice «PASS», no tiene más autoridad que la evidencia física vigente.

Una nueva decisión explícita del CLIENT puede cambiar el producto. El Planner debe registrarla como requisito actual y, cuando corresponde, marcar la decisión anterior como sustituida. No alcanza con elegir el archivo que parece más reciente por el nombre. Si falta un hecho, se marca `UNKNOWN`. Si dos autoridades actuales se contradicen materialmente, corresponde `HOLD` para las acciones dependientes hasta reconciliar el conflicto. Las investigaciones de solo lectura pueden continuar.

El sistema distingue tres planos de continuidad:

1. L0: evidencia de lo que el CLIENT solicitó, corrigió y aprobó, incluidas las decisiones posteriores.
2. L1: requisitos interpretados, teoría de producto y Product State canónicos vigentes.
3. L2: implementación, código, bases de datos, campañas, checkpoints, revisiones y pruebas de runtime.

La separación evita que una promesa formulada en una conversación se confunda con software desplegado. También impide que una propuesta antigua reemplace una implementación posteriormente comprobada sin registrar esa decisión.

Como mínimo, un trabajador que llega a un contexto nuevo debe reconstruir el objetivo, los requisitos, el ref de código que puede comprobar, los testigos relevantes del entorno o de la DB, la campaña activa si existe, el gate abierto, la mejor evidencia disponible, las incertidumbres y la próxima acción permitida o prohibida. Si no puede hacerlo, todavía no se demostró continuidad.

Los términos que aparecen a lo largo de los ocho capítulos son:

- **Scaffold:** la carpeta de control `.agentic-sdlc/` instalada en la aplicación. Comienza deliberadamente en `HOLD / UNTRUSTED_CONTEXT`.
- **Discovery:** investigación inicial, preferentemente de solo lectura, para conocer código, uso, entorno, datos y necesidades reales.
- **Adoption:** promoción controlada de hechos verificados y decisiones confirmadas a un estado coherente. No es copiar una plantilla sin revisar.
- **Product State:** referencia canónica del estado actual de las capacidades del producto.
- **Charter:** contrato estratégico de una capacidad, sus límites, dependencias, gates y falsificadores.
- **Gate:** condición de verificación antes de una aceptación; distintos riesgos exigen distintas pruebas.
- **Currentness:** comprobación de que código, requisitos, estado, autoridad y artefactos siguen vinculados a sus versiones reales.

## 4. Cómo leer el manual completo

El capítulo 01 conviene leerlo antes de la primera instalación. El 02 corresponde antes de autorizar la primera función material. Los demás se consultan cuando aparece su problema operativo. No hace falta memorizar unas sesenta páginas para probar el perfil `SMALL` en un proyecto nuevo y sin gobierno previo.

| Capítulo | Cuándo consultarlo | Resultado que deberías poder comprobar |
| --- | --- | --- |
| 00 · Antes de empezar | Antes de instalar. | Entendés las responsabilidades, límites y recorrido. |
| 01 · Instalación | Al preparar un proyecto. | Existe un control layer validado, sin inventar adopción ni permiso de ejecución. |
| 02 · Planner y adopción | Antes de la primera capacidad. | Requisitos, baseline, autoridad y próximo paso se reconstruyen sin el chat anterior. |
| 03 · Operación diaria | Durante el desarrollo. | El trabajo se autoriza, ejecuta, verifica y registra con continuidad en la misma campaña. |
| 04 · Solicitar cambios | Al definir funciones o revisar decisiones. | Cada pedido describe comportamiento, prioridades y límites observables. |
| 05 · Errores y recuperación | Ante incidentes y dudas de estado. | Se conserva evidencia y se evita daño adicional hasta verificar la recuperación. |
| 06 · Cierre de capacidades | Cuando alguien dice «terminado». | El candidato exacto posee evidencia suficiente para los gates que le corresponden. |
| 07 · Ejemplo guiado del club | Para practicar el flujo integral. | Podés seguir una capacidad desde requisitos hasta aceptación. |

Después del 01 puede ser correcto seguir en HOLD. Después del 02, una sesión genuinamente nueva debería poder reconstruir el proyecto. Después del 06, el candidato aceptado debería tener identidad y evidencias separadas por gate. Si falta alguno de esos resultados, hay que volver a producir la evidencia correspondiente, no repetir una explicación más larga.

## 5. Preparación: las decisiones que sí son tuyas

Antes de instalar, prepará una ficha breve. Describí el problema, las personas usuarias, el recorrido principal, los datos, el contexto de uso, el plazo, el presupuesto, las expectativas de interfaz y las exclusiones. Si una decisión todavía no se tomó, señalala como pregunta abierta.

Por ejemplo:

> Quiero una aplicación local para registrar socios y cuotas de un club. La usa una persona administrativa. La primera versión no acepta pagos online. Debe conservar el historial de pagos. Prefiero una pantalla simple y legible. El presupuesto de servicios pagos es cero.

No necesitás elegir SQLite o PostgreSQL, determinar la cantidad de ramas de Git, seleccionar un ORM ni programar un rollback. Esas decisiones corresponden a ingeniería, que debe explicarte las consecuencias cuando afectan el producto o un permiso reservado. Cuando hay datos personales, pagos, publicación o conexiones externas, los agentes no eliminan tus responsabilidades de autorización ni las obligaciones legales pertinentes.

## 6. Alcance, límites y versiones

ArquitecturaRepo distribuye mecanismos reutilizables y ejemplos sintéticos. Sus pruebas de transferencia y recuperación no certifican automáticamente que cada aplicación se pueda instalar, operar o publicar con seguridad. `tools/campaignctl.py` ofrece un runtime de referencia opcional; por sí solo no llama a cualquier agente de programación ni certifica la integración nativa con Codex Desktop.

La versión v1.4 distingue controles portables comprobados, mecanismos experimentales y capacidades de hosts externos no verificadas. Para un uso real hay que contrastar las instrucciones sensibles a versión con el código y la release que efectivamente se instalaron. Precios, opciones de modelos, pantallas de servicios y restricciones de terceros pueden cambiar; no son invariantes del método.

El código y la documentación originales del proyecto tienen licencia MIT; las dependencias y los recursos ajenos pueden tener sus propias condiciones. El tag identifica una versión, pero la integridad del archivo distribuido requiere comprobar su checksum. Que exista una release verificada no autoriza una campaña nueva, una compra de API ni un despliegue público de tu aplicación.

## 7. Un recorrido de extremo a extremo

Imaginá una asociación que necesita registrar socios. El CLIENT decide quién puede dar de alta una ficha, qué datos son obligatorios y qué significa desactivarla. El Planner convierte esas decisiones en requisitos verificables; no supone que desactivar sea borrar para siempre. Antes de ordenar implementación, inspecciona lo que ya existe, identifica dependencias y consulta únicamente las decisiones que cambian el comportamiento esperado.

Tras confirmar el alcance, el Planner persiste requisitos actuales, Product State, baseline técnico y plan de entrega con fechas. Elige una capacidad que pueda demostrarse de principio a fin. Su charter expresa el resultado, el motivo, las fronteras permitidas, las interfaces afectadas, los gates y las condiciones que invalidarían el encargo.

I3 organiza la implementación. Puede encargar código, pruebas o review a especialistas o resolverlos directamente en un proyecto pequeño. Repara bugs ordinarios y vuelve a correr las verificaciones aplicables dentro de la misma campaña. No devuelve cada fallo al Planner como un nuevo problema estratégico. Cuando hay un candidato significativo, el Planner inspecciona la evidencia y el CLIENT evalúa los aspectos de producto y experiencia que le corresponden.

El ciclo no termina porque el ejecutor escribió un informe convincente ni porque hubo muchos commits. Termina cuando la capacidad funciona con el nivel aceptado y el repositorio preserva suficientes hechos actuales para que otro trabajador continúe. El capítulo 07 recorre este ejemplo con datos ficticios.

## 8. Decisiones habituales y sus responsables

| Situación | Responsable y evidencia esperada |
| --- | --- |
| «Los socios con cuotas vencidas no pueden inscribirse». | CLIENT confirma la regla; Planner la registra en los requisitos vigentes. |
| «¿Usamos SQLite o PostgreSQL?» | Ingeniería elige según carga real, concurrencia, backups, despliegue y riesgos. |
| «¿Podemos mostrar datos de socios reales en una demo?» | Hace falta autorización lícita, concreta y controles de acceso; lo normal es usar datos ficticios. |
| «Una prueba falló después de una corrección». | I3 investiga, corrige y renueva evidencia dentro del mismo charter. |
| «Ahora quiero transformar la app local en un servicio público». | CLIENT confirma el cambio; Planner reconsidera red, seguridad, costo y alcance. |
| «El agente dijo que todo está listo». | El mensaje no constituye aceptación; hay que identificar el candidato y sus pruebas técnicas y humanas. |

## 9. Ficha de arranque de una página

Podés empezar sin una especificación técnica extensa. Una ficha útil contiene:

- **Propósito:** qué problema resuelve la primera versión y para quién.
- **Recorrido principal:** qué intenta lograr la persona y cómo se ve el éxito.
- **Datos:** qué se almacena, si hay información personal y cuánto debe conservarse.
- **Entorno:** equipos, ubicación, conectividad y funcionamiento sin Internet.
- **Límites:** fecha objetivo, presupuesto, integraciones aprobadas y funciones excluidas.
- **Calidad visible:** legibilidad, accesibilidad, errores comprensibles y rendimiento que importan al usuario.

No hace falta que resuelvas todas las incógnitas de arquitectura. El sistema de ingeniería debe investigar lo que pueda y exponerte solamente las decisiones de producto que no debe inventar. La ficha sirve de entrada al discovery y a la adopción del capítulo 02.

## 10. Cómo evaluar si el sistema te está ayudando

Tras dos o tres ciclos de entrega, pedí una demostración breve: ¿qué capacidad nueva puedo usar?, ¿dónde está la evidencia?, ¿qué cambió desde el ciclo anterior?, ¿qué riesgo material sigue abierto?, ¿cuál es la próxima acción autorizada? Si la respuesta se limita a «hicimos muchos commits», «abrimos varios agentes» o «redactamos más documentación», todavía no quedó demostrado el avance del producto.

Una buena arquitectura puede reducir la dependencia de conversaciones anteriores, pero no reemplaza el juicio humano, la revisión de seguridad o la prueba de funcionamiento real. Medí su valor por continuidad, claridad de responsabilidades, capacidades utilizables, calidad de evidencia y recuperación confiable; no por la cantidad de protocolos, sesiones o pantallas.

**Siguiente:** capítulo 01, Instalación y configuración.

## Fuentes y vigencia

- [Release pública v1.4.0](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0)
- [Primera instalación y límites de soporte](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md)
- [Notas de release y actualización](../../../47_V1_4_RELEASE_NOTES_AND_UPGRADE.md)
- [Visión general de arquitectura](../../../00_ARCHITECTURE_OVERVIEW.md)
- [Modelo de autoridad](../../../../protocols/AUTHORITY_MODEL.md)
- [Licencia MIT](../../../../LICENSE)

Este capítulo describe el starter y un ejemplo ficticio. Ninguna prueba genérica sustituye la comprobación del proyecto real que lo adopte.
