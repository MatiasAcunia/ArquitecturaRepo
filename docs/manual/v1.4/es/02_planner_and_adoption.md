# 02 — El Planner y la adopción del proyecto

ArquitecturaRepo · Manual completo de uso · Edición v1.4 · Español

> Crear `.agentic-sdlc/` es instalar una capa inicial, no confirmar el baseline de una aplicación. Este capítulo explica cómo el Planner reconstruye el proyecto real, obtiene decisiones del CLIENT, adopta estado verificado y autoriza la primera campaña. Para comandos concretos, consultá la [guía pública v1.4](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md) y el [contrato de adopción](../../../16_TRANSFER_ADOPTION.md).

## Contenido del capítulo

1. Una conversación no es el proyecto
2. Preparar el espacio de trabajo
3. Discovery: hacer las preguntas correctas
4. Baseline técnico y plan de entrega
5. Adoption: conectar el starter con el proyecto real
6. El examen decisivo: contexto fresco
7. Primera campaña autorizada
8. Ejemplo de sesión inicial con el Planner
9. Un baseline que el CLIENT pueda confirmar
10. Ejemplo de primera campaña

## 1. Una conversación no es el proyecto

El I2 Planner es responsable de la estrategia de un producto o workstream delimitado. Puede trabajar mediante una conversación, pero el historial del chat no es una base de datos canónica ni prueba que la última implementación coincida con una afirmación anterior. Su autoridad proviene de los requisitos actuales confirmados por el CLIENT, los protocolos aplicables, la evidencia física del repositorio y de la DB, el ownership vigente y los registros válidos de campaña.

Si el último mensaje del ejecutor dice «terminado», el Planner todavía tiene que identificar el candidato exacto, comprobar la evidencia y distinguir qué gates realmente pasaron. No puede declarar aceptación estratégica porque el informe tenga una etiqueta `PASS` o porque un agente asegura que está todo resuelto.

En un proyecto pequeño, un Planner y un dueño de ejecución pueden ser suficientes. La figura I1 Master Owner tiene sentido cuando hay varios productos, líneas de trabajo independientes, recursos o presupuestos compartidos, o una necesidad sistémica de coordinar políticas. No reemplaza al Planner del producto y no mejora el sistema por existir como un chat adicional.

El Planner piensa desde el resultado final: quién utilizará la capacidad, qué interfaces y datos actuales afecta, cómo se observará el éxito, cuáles son las dependencias comprobadas y qué hallazgos impedirían aceptar el resultado. Con esa información prepara un charter de capacidad. Dentro del alcance autorizado, I3 se encarga de programación, depuración, reintentos, integración, revisión y recuperación. Un defecto ordinario no exige un nuevo charter ni una nueva campaña.

## 2. Preparar el espacio de trabajo

Empezá por el repositorio real de la aplicación, no por un resumen recordado. Leé el `AGENTS.md` vigente, los protocolos aplicables, los requisitos, el Product State canónico, las referencias actuales de código y las campañas o registros de runtime relevantes. Si el Planner no puede leer una superficie necesaria, debe identificar la falta concreta. No corresponde completar el hueco con memoria de una conversación distinta.

Podés organizar el trabajo en un Proyecto de ChatGPT u otro espacio de colaboración y guardar ahí el manual como referencia. Si conectás GitHub, limitá permisos y repositorios al alcance necesario. Verificá la lectura de un archivo conocido en el ref correcto. Que la cuenta aparezca conectada no significa que el asistente tenga acceso a todas las ramas, issues, bases de datos o procesos de ejecución. Ningún modelo, configuración de esfuerzo o suscripción específica es requisito universal del framework.

Una instrucción inicial útil para un Planner es:

> Actuá como I2 Planner de este proyecto. Yo soy CLIENT: defino reglas de negocio, prioridades, requisitos y autorizaciones externas reservadas. Antes de planificar, reconstruí el repositorio real y los protocolos aplicables; no inventes estado. Definí límites de capacidades y charters. Dejá implementación, depuración y recuperación táctica en I3, dentro del alcance autorizado. No me transfieras decisiones rutinarias de Git, pruebas, currentness o debugging. Distinguí lo que está comprobado, lo que sigue desconocido y las decisiones de producto que realmente necesito tomar.

El texto es una entrada de rol, no sustituye al `AGENTS.md` real, al registro de requisitos ni a una campaña que ya tiene autoridad. En cada nuevo contexto hay que reconstruir las superficies vigentes. Un título de rol tampoco concede permisos adicionales de filesystem o proveedores externos.

## 3. Discovery: hacer las preguntas correctas

El discovery comienza por la persona y el problema, no por elegir framework. Preguntá qué usuario necesita completar qué recorrido, cuáles son los datos persistentes, los errores importantes, la conectividad, la exposición a Internet, la sensibilidad de los datos, los costos, las fechas, los requisitos de accesibilidad y las exclusiones. El Planner puede agrupar tres a siete preguntas relacionadas y luego devolver una síntesis coherente para que el CLIENT la corrija.

La pregunta adecuada modifica una decisión de producto:

| Pregunta útil para el CLIENT | Decisión técnica que normalmente pertenece a ingeniería |
| --- | --- |
| ¿Quién utiliza el sistema, en qué equipos y desde dónde? | Puertos, topología, framework de interfaz y despliegue. |
| ¿Qué sucede con los pagos cuando se desactiva un socio? | Tablas, claves foráneas, migraciones y transacciones. |
| ¿Se permitirán pagos por Internet en la primera versión? | Diseño del proveedor, respetando autorización de gasto y operaciones reales. |
| ¿Qué resultado debe poder demostrarse antes de la fecha objetivo? | Orden interno de tareas, mecanismos de pruebas y checkpoints. |
| ¿Varias personas editarán la misma ficha simultáneamente? | Concurrencia, transacciones y resolución de conflictos. |

Al cerrar discovery, presentá una sola revisión del baseline: funciones, recorrido, reglas de datos, calidad no funcional, seguridad y red, comportamiento de interfaz, backups, recuperación, presupuesto, fechas, exclusiones y preguntas pendientes. El CLIENT confirma si esa síntesis representa el producto actual. La confirmación no es un contrato legal ni impide cambios futuros; fija una versión rastreable de la decisión que vale para planificar ahora.

No descargues sobre el CLIENT incertidumbres exclusivamente técnicas. «¿Qué base de datos elegimos?» suele ser una pregunta de ingeniería. «¿Cuántas horas de pagos es aceptable perder después de un corte de luz?» es una pregunta de producto porque condiciona la estrategia de respaldo. El Planner debe explicar la consecuencia para la persona usuaria antes de pedir una decisión reservada.

## 4. Baseline técnico y plan de entrega

Cuando la intención del producto está confirmada, el Planner elige o confirma la estrategia técnica contra el código y las restricciones reales. Registra lenguaje, frameworks, persistencia, migraciones, despliegue, secretos, permisos, pruebas, integración de UI, backups y recuperación. En el control layer instalado, las decisiones vigentes se conservan en `state/TECHNICAL_BASELINE_CURRENT.json`, no únicamente en un comentario de chat.

El plan de entrega describe hitos observables, fechas objetivo, dependencias, confianza, riesgos y próxima revisión. Si una fecha cambia, debe quedar registrado el cambio. Sobrescribir silenciosamente la fecha anterior destruye información importante para razonar sobre el progreso y los compromisos. Una lista de tareas de programación sin plazos ni resultados visibles no sustituye el plan de entrega.

`tools/baseline_guard.py` verifica si las precondiciones de una campaña material están coherentes. No debería eludirse mediante campos inventados. Si los requisitos no están confirmados, hay una decisión material de seguridad/red pendiente o las referencias actuales se contradicen, se mantiene HOLD para la campaña dependiente.

El Planner también debe comprobar que el encargo sea ejecutable. Un charter que solo dice «implementar gestión de socios» puede definir una idea estratégica, pero resultar demasiado abstracto para un controlador que hará muchas operaciones o consumirá recursos. El contrato de [ejecución orientada al resultado](../../../44_OUTCOME_FIRST_AGENT_EXECUTION.md) propone un *work order* acotado cuando hay múltiples operaciones materiales, lotes, proveedores pagos o runtime significativo.

El charter define qué y por qué; el work order vincula inventario real, operaciones viables, presupuesto, resultado físico, límites y condiciones de parada. No es una segunda campaña. `tools/work_order_guard.py` permite ejecutar `validate` sobre la estructura y `assess` sobre recibos de avance, pero su evaluación no constituye aceptación física, perceptual ni autorización externa. Si una operación se resuelve con herramientas deterministas del sistema operativo, no hay motivo para imponer una consulta paga a un modelo por cada archivo.

## 5. Adoption: conectar el starter con el proyecto real

La adopción debe describir la aplicación que existe físicamente. El recorrido reproducible comienza con scaffold, inventario, especificación de adopción revisada, preflight sobre una copia temporal del control y promoción de registros con journal. `discover_project.py` enumera metadatos y hashes; no deduce por sí solo los requisitos de negocio. `apply_adoption.py` materializa hechos verificados y decisiones expresadas en una especificación válida, pero no puede inventar la intención del CLIENT.

El resultado adoptado vincula requisitos, fuentes de código, baseline técnico, Product State, contexto de entrada, registro de owners y overlays del proyecto. Cuando una base de datos o un testigo SQLite WAL es relevante, tiene que concordar con las referencias actuales. Si ya hay una campaña activa, no se debe usar la adopción como un reinicio disimulado. En una aplicación con control canónico previo, el [preflight read-only](../../../32_EXISTING_GOVERNED_ATTACHMENT.md) es el camino inicial, no una reinstalación genérica.

Si el Planner solo puede leer el repo remotamente y el I3 tiene un checkout local autorizado, el Planner prepara un despacho completo. No le pide al CLIENT que edite manualmente registros de ownership, concilie SHAs o ensamble fragmentos de JSON. El ejecutor utiliza la evidencia real y reporta resultados físicos. El código, los datos y el historial previos se conservan salvo una modificación específica, justificada y autorizada.

El informe de adopción debería responder cinco preguntas:

1. ¿Qué repositorio y versión del código se inspeccionaron realmente?
2. ¿Qué requisitos y decisiones confirmó el CLIENT?
3. ¿Qué estado técnico, owners y registros de control se materializaron?
4. ¿Qué verificaciones se ejecutaron físicamente y con qué resultado?
5. ¿Qué incertidumbre, HOLD o primera frontera de trabajo permitida queda?

Si el informe solo dice «se instalaron archivos» o «todo verde», la transición no quedó demostrada. Las herramientas sirven para registrar un estado verdadero; no permiten sustituir evidencia del producto por una etiqueta tranquilizadora.

## 6. El examen decisivo: contexto fresco

Abrí una sesión realmente nueva, sin entregarle la narrativa completa de la conversación anterior. Proporcioná únicamente la identidad del repositorio, el acceso de lectura autorizado y las instrucciones normales de entrada. Pedile que reconstruya su rol y límites, requisitos, ref de código, Product State, campaña y checkpoint si existen, gate abierto, mejor evidencia, hechos desconocidos, siguiente acción permitida y acciones prohibidas.

La respuesta debe fundarse en superficies durables. Repetir de memoria la arquitectura no demuestra continuidad. Tampoco pasa si confunde un documento sustituido con el actual, inventa estado de la DB, considera un PASS de I4 como aceptación o delega al CLIENT una contradicción técnica que debe resolver el owner del sistema.

Si el problema es falta de acceso, identificá y corregí ese permiso dentro del alcance autorizado. Si el propio estado canónico se contradice, reconciliá la causa y el mecanismo de currentness. No apruebes el examen simplemente por escribir un handoff de cien páginas para el próximo chat. Consultá el [test de contexto fresco](../../../07_FRESH_CONTEXT_TEST.md) y su [prompt de prueba](../../../../prompts/FRESH_CONTEXT_PROBE.md).

## 7. Primera campaña autorizada

Elegí una capacidad que pueda construirse y verificarse de extremo a extremo. El charter expresa resultado, dependencias, ownership, interfaces afectadas, recursos que pueden interferir, gates pertinentes, evidencia exigible y condiciones de invalidación. No debería imponer veinte microcommits ni cuántos reintentos necesita I3 para corregir un bug.

No confundas «el control layer valida» con «la persona puede registrar un socio y conservar sus pagos». La primera frase habla de contratos del framework; la segunda necesita integración, persistencia, seguridad, funcionamiento físico y posiblemente una valoración humana de uso.

Según el riesgo, diferenciá gates de unidad, integración, DB/currentness, semántica/generalización, funcionamiento físico, experiencia humana y publicación. Ninguno reemplaza silenciosamente al otro. Una vez autorizado el charter, I3 asume implementación y rework dentro del alcance. Bugs, refactors, reintentos, migraciones previstas y hallazgos de review no justifican volver a estrategia. Una modificación real de objetivo, autoridad o interfaz crítica sí puede invalidar el encargo.

## 8. Ejemplo de sesión inicial con el Planner

Un pedido de entrada breve puede ser suficiente:

> Quiero desarrollar una aplicación para registrar socios y cuotas. Antes de planificar implementación, inspeccioná mi repositorio real y el starter ArquitecturaRepo de solo lectura. Guiame por las decisiones de producto pendientes. Separá lo confirmado de lo inferido; no inventes datos ni infraestructura. Prepará un baseline para que yo lo revise. Después de mi confirmación, elegí el perfil justificado, la estrategia técnica y un plan con hitos y fechas. No inicies una campaña material hasta satisfacer los gates de baseline y continuidad.

El Planner debería inspeccionar archivos y ramas antes de preguntarte qué archivo existe o qué SHA tiene una referencia que puede consultar. Sí puede preguntar cuántas personas operan el club, desde dónde, qué datos deben conservarse y cómo se distingue un pago vencido de uno cancelado. Cada pregunta debe afectar la solución, no extender innecesariamente la conversación.

## 9. Un baseline que el CLIENT pueda confirmar

«Hagamos un CRUD profesional» no es una especificación revisable. Un ejemplo más útil es:

| Dimensión | Requisito propuesto para la primera versión | Estado |
| --- | --- | --- |
| Usuario | Una persona administrativa usa la aplicación desde una computadora del club. | Pendiente de confirmación. |
| Datos | Socios, cuotas, pagos históricos e inscripciones. | Pendiente de confirmación. |
| Regla de retención | Desactivar una ficha nunca borra sus pagos anteriores. | Pendiente de confirmación. |
| Funciones iniciales | Alta, búsqueda, edición y desactivación de socios. | Pendiente de confirmación. |
| Seguridad y red | Uso local; sin publicar el servicio en Internet inicialmente. | Pendiente de confirmación. |
| Interfaz | Formularios legibles, búsqueda útil y errores claros. | Pendiente de confirmación. |
| Recuperación | Definir intervalo de respaldo y pérdida máxima de registros aceptable. | Decisión abierta. |
| Exclusiones | Sin pagos online ni aplicación móvil en la primera versión. | Pendiente de confirmación. |

Solo marcá un requisito como confirmado si el CLIENT realmente lo aprobó. Cuando el baseline refleje su decisión, persistí la versión y el momento de confirmación. Si más adelante se modifica, registrá qué sustituye y cuál es el impacto. No borres el historial de decisiones legítimas.

Luego el Planner registra tecnología, almacenamiento, red, backups y milestones con fechas, dependencias, evidencia de aceptación, confianza y riesgos. Las elecciones deben responder a la aplicación real; no a un stack de moda ni a la preferencia arbitraria del asistente.

## 10. Ejemplo de primera campaña

Una capacidad inicial razonable para el club sería: «Crear, consultar, modificar y desactivar socios sin perder historial de pagos, con errores comprensibles cuando los datos son inválidos». Puede demostrarse en una aplicación abierta y verificarse mediante persistencia real. El charter identifica límites del producto, reglas de datos, dependencias y gates. No necesita determinar cada archivo ni cada comando que ejecutará el I3.

I3 recibe ese objetivo autorizado y el código actual. Implementa, prueba, revisa, integra y corrige defectos en la misma campaña. Si el formulario rechaza un teléfono válido, lo arregla sin pedir otra estrategia. Si el CLIENT modifica el proyecto para atender cientos de clubes mediante un servicio público, cambia la necesidad y deben reconsiderarse requisitos, red, seguridad y alcance antes del reroute estratégico.

El resultado final debe tener un candidato y evidencia identificables. El Planner revisa gates técnicos y estratégicos; el CLIENT prueba el recorrido que le corresponde y puede aceptar o rechazar la experiencia. Una fixture verde no reemplaza una aplicación real ni la valoración de su usuario.

**Siguiente:** capítulo 03, Operación diaria.

## Fuentes y vigencia

- [Discovery, requisitos y plan de entrega](../../../21_PRODUCT_DISCOVERY_REQUIREMENTS_STACK_AND_DELIVERY.md)
- [Prompt de instalación y adaptación](../../../../prompts/INSTALL_THIS_SDLC.md)
- [Prompt de discovery](../../../../prompts/PRODUCT_DISCOVERY_SESSION.md)
- [Prueba de contexto fresco](../../../../prompts/FRESH_CONTEXT_PROBE.md)
- [Test de contexto fresco](../../../07_FRESH_CONTEXT_TEST.md)
- [Contrato de transferencia y adopción](../../../16_TRANSFER_ADOPTION.md)
- [Preflight de gobierno existente](../../../32_EXISTING_GOVERNED_ATTACHMENT.md)
- [Work orders orientados al resultado](../../../44_OUTCOME_FIRST_AGENT_EXECUTION.md)
- [Protocolo del Planner](../../../../protocols/PLANNER_KERNEL.md)
- [Código de baseline guard](../../../../tools/baseline_guard.py)
- [Código de work-order guard](../../../../tools/work_order_guard.py)

Los ejemplos utilizan datos de club ficticios. No constituyen prueba de que un repositorio de destino haya sido inspeccionado, adoptado o aceptado.
