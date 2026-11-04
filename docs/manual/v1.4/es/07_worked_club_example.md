# 07 — Ejemplo guiado: una aplicación de gestión para un club

ArquitecturaRepo · Manual completo de uso · Edición v1.4 · Español

> Este capítulo es un **ejemplo didáctico ficticio**, no una aplicación ya implementada ni un backend generado. Los datos, decisiones, nombres de campañas y resultados esperados son ilustrativos. En un proyecto real, requisitos, repositorio, DB, runtime, permisos y evidencia de aceptación tienen que provenir de sus fuentes vigentes.

## Contenido del capítulo

1. El producto que quiere construir el club
2. Descubrir preguntas que cambian el resultado
3. Instalar el control sin confundirlo con la app
4. Primera capacidad: gestión de socios
5. Del Planner a I3: una solicitud operable
6. Qué probar antes de aceptar
7. Segunda capacidad: cuotas y pagos
8. Evaluar el ejemplo completo
9. Primer ciclo con datos ficticios
10. Registrar y enrutar un defecto
11. Dependencias del segundo ciclo
12. Ejercicio final de recuperación

## 1. El producto que quiere construir el club

Imaginá un club de barrio con una persona administrativa que registra socios, cobra cuotas, administra actividades y anota participantes. Hoy usa planillas dispersas y anotaciones. Quiere una aplicación sencilla que conserve el historial, permita encontrar a cada socio, evite superar la capacidad de una actividad e informe quién tiene pagos al día.

La primera versión funcionará para operadores internos. Para controlar alcance, el CLIENT decide no incorporar todavía pagos en línea, una aplicación móvil separada, facturación fiscal, notificaciones masivas ni integraciones externas. No es que esas funciones sean malas; simplemente no resuelven el primer problema que se quiere validar y aumentarían tiempo, seguridad y coste.

Esa descripción propone una dirección, pero no decide el lenguaje, la base de datos, el hosting ni los permisos exactos. Tampoco significa que el framework cree una interfaz de socios al instalarse. Esas decisiones dependerán del repositorio real, del presupuesto, del ambiente y del criterio de ingeniería una vez que el CLIENT confirme los objetivos de producto.

El flujo probable de capacidades es identidad de socios, luego cuotas e historial, después actividades/cupos y finalmente inscripciones basadas en elegibilidad. No son cuatro aplicaciones ni obligatoriamente cuatro equipos. Son dependencias: no conviene asignar pagos a socios sin identidad consistente, ni habilitar inscripciones por deuda cuando todavía no existe un estado de cuotas confiable.

La arquitectura tiene valor si permite conservar esas decisiones y sus consecuencias durante varias semanas de trabajo, con agentes diferentes y sesiones interrumpidas. Su objetivo no es dibujar una organización compleja, sino mantener claras las interfaces y la autoridad para construir algo realmente útil.

## 2. Descubrir preguntas que cambian el resultado

El Planner entrevista al CLIENT: ¿quién usará la aplicación?, ¿funciona en una sola computadora o en la red?, ¿cuántos socios hay?, ¿qué información personal se almacena?, ¿qué respaldo necesitan?, ¿hay personal con distintos roles?, ¿cuánto tiempo y dinero hay disponibles? Cada respuesta cambia decisiones de riesgo, interfaces o tecnología.

Una regla inicial propuesta podría ser: «Un administrador puede desactivar un socio, pero sus pagos e inscripciones históricas siguen disponibles para el personal autorizado». Antes de implementarla se confirma qué significa «desactivar», quién está autorizado, qué aparece en una búsqueda de socios activos y cómo se conserva el historial.

Otras dudas deben hacerse visibles: ¿una cuota vencida impide inscribirse?, ¿qué pasa con un acuerdo de pago?, ¿se libera el cupo apenas una persona cancela?, ¿hay lista de espera?, ¿se puede reactivar una membresía?, ¿puede corregirse un pago ya emitido?, ¿cuándo se considera cerrado un período? Adivinar esas reglas desde la implementación produciría comportamientos difíciles de corregir después.

| Área | Comportamiento propuesto para la primera versión |
| --- | --- |
| Socios | Crear, editar, buscar y desactivar, conservando relaciones históricas. |
| Cuotas | Registrar pagos, identificar períodos pendientes y consultar historial. |
| Actividades | Definir nombre, horario, cupos y plazas disponibles. |
| Inscripciones | Inscribir y cancelar con reglas explícitas de deuda y capacidad. |
| Fuera de alcance | Pago online, app móvil, avisos masivos y dashboards elaborados. |

Esta tabla no es un requisito vigente hasta que el CLIENT la confirme. La necesidad de guardar transacciones sugiere evaluar el perfil `STATEFUL`, pero incluso ese perfil requiere una adopción adecuada: definir owners de datos, migraciones, idempotencia, seguridad, recuperación y evidencia física proporcional.

## 3. Instalar el control sin confundirlo con la app

En un repositorio de club nuevo y sin control canónico previo, se puede preparar una capa de gobierno. Desde un checkout de ArquitecturaRepo v1.4, por ejemplo, en PowerShell:

```powershell
& "python" "tools\scaffold_project.py" --target "..\club-app" --profile "STATEFUL" --product-id "CLUB_MANAGER" --objective "Gestión ficticia de socios y cuotas del club" --language "es" --no-feedback-workflow
```

El comando crea `.agentic-sdlc/` dentro de `club-app/`, en estado inicial `HOLD / UNTRUSTED_CONTEXT`. No crea el backend, no inventa una DB, no demuestra que existe una pantalla, no configura automáticamente un LLM y no autoriza ejecutar una campaña de desarrollo. La capa de control es infraestructura para organizar el trabajo de producto; la aplicación sigue siendo el resultado a construir.

Si `club-app/` ya tiene un sistema de gobierno canónico, el procedimiento es distinto: se usa el [preflight read-only de proyectos gobernados](../../../32_EXISTING_GOVERNED_ATTACHMENT.md). No hay que instalar otro Product State encima, reemplazar un controlador existente ni duplicar la autoridad para que el ejemplo funcione.

Después del scaffold, se ejecutan los comandos de inspección, validación e inventario indicados por el instalador y el [capítulo 01](01_installation.md). Planner e I3 leen la aplicación que realmente existe, reconstruyen requisitos y baseline, preparan una especificación revisada de adopción, hacen preflight, promueven los registros autorizados y verifican que una sesión nueva pueda reconstruir todo sin depender del chat.

El CLIENT revisa alcance, experiencia esperada, presupuesto y fecha. Ingeniería propone stack, modelo de datos, red, backups, permisos y plan de entregas. La primera campaña material se autoriza solo cuando la base y el estado vigente son coherentes. Si faltan datos, se mantiene un HOLD concreto para las operaciones que dependan de ellos.

## 4. Primera capacidad: gestión de socios

¿Por qué comenzar por socios? Porque cuotas e inscripciones necesitan una identidad estable a la cual referirse. Una capacidad inicial bien delimitada podría decir:

> Una persona administrativa autorizada puede registrar un socio, encontrar su ficha, corregir datos, consultar el estado y desactivarlo, sin destruir pagos e inscripciones históricas que deban conservarse.

El charter de esta capacidad especifica sus interfaces, dependencias, inputs/outputs, ownership de datos, comportamiento de errores y gates aplicables. No necesita imponerle al ejecutor los nombres de todas las funciones ni una lista microscópica de commits. I3 organiza la implementación, las pruebas, refactors internos y la revisión del candidato integrado.

La lista de casos relevantes incluye identificadores duplicados, datos inválidos, escritura seguida de lectura real, recuperación tras reinicio, búsquedas con filtros activos/inactivos, preservación de relaciones, autorización de operaciones y recorrido completo de interfaz si existe una UI. Los ensayos deben registrar ambiente, candidato y resultado observable. Una prueba aislada de validación del esquema no basta para afirmar que el usuario pudo realizar el flujo completo.

El CLIENT no tiene por qué decidir el ORM, el tipo de índice o los nombres de las tablas. Ingeniería sí debe pedir confirmación cuando una decisión técnica tenga consecuencias de producto o coste: uso sin internet, exposición de datos, restauraciones, derechos de acceso, dependencia de un proveedor externo o presupuesto de operación.

Los registros existentes —si el club ya usa una base— son evidencia y datos que hay que proteger. No se toman las fichas de este manual como si fueran datos reales; tampoco se copian muestras con información personal hacia un issue público. Una migración necesaria se diseña y prueba con rollback y respaldo autorizado, no se presupone segura porque el scaffold pasó.

## 5. Del Planner a I3: una solicitud operable

El mensaje al Controller debe ser íntegro y suficientemente compacto para ejecutar. Un ejemplo de estructura, no una campaña real, es:

> **Goal:** Entregar la capacidad aprobada de gestión de socios.
>
> **Context:** Reconstruir requisitos confirmados, Product State canónico, repositorio actual y ref exacto. Identificar registros afectados y estado vigente de DB.
>
> **Constraints:** Conservar historial, respetar permisos y presupuesto; no agregar cuotas, notificaciones ni funciones no autorizadas.
>
> **Execution gates:** Probar físicamente alta, búsqueda, edición, baja lógica y persistencia tras reinicio; cubrir datos inválidos, duplicados, permisos y concurrencia relevante. Revisar independientemente el candidato integrado.
>
> **Done when:** Entregar identidad exacta, evidencia física, tests aplicables, hallazgos del reviewer, gates abiertos y terminal estratégico honesto.

La campaña contiene el resultado y sus límites. I3 puede organizar tareas, investigar fallos y volver a probar sin pedir una nueva autorización por cada error. Si el doble clic crea dos socios idénticos pese a una regla de unicidad confirmada, se corrige dentro de la campaña. No existe razón para abrir una segunda campaña estratégica llamada «evitar doble clic».

Cuando una operación implica varios cambios delicados o mucho coste, el Controller puede preparar una unidad acotada de trabajo con inventario, presupuestos y condiciones de parada. Eso no cambia las decisiones de producto ni concede permiso para ejecutar un proveedor de pago. La autoridad de una unidad técnica deriva del charter y no puede superar sus límites.

## 6. Qué probar antes de aceptar

Tomá una ficha completamente ficticia con el identificador `SOCIO-001`. La siguiente tabla enumera acciones esperadas para una futura aplicación: **no es evidencia de que exista ni de que ya se haya ejecutado**.

| Paso | Acción del usuario | Resultado que se debería observar |
| --- | --- | --- |
| 1 | Abrir la app como administrador autorizado. | El mecanismo de acceso real permite el rol correcto. |
| 2 | Crear `SOCIO-001` con datos sintéticos válidos. | Se guarda exactamente una ficha identificable. |
| 3 | Buscar por identificador permitido. | Aparece la ficha correcta sin filtrar datos de otros roles. |
| 4 | Editar un teléfono ficticio. | La nueva información figura al guardar y releer. |
| 5 | Cerrar y abrir la aplicación. | El cambio persiste mediante la DB y el camino de recuperación reales. |
| 6 | Desactivar al socio. | Ya no figura como activo; su identidad histórica permanece. |
| 7 | Consultar pagos anteriores con permisos. | Se conserva historial y se expone solamente al rol previsto. |
| 8 | Intentar una operación inválida o duplicada. | Se rechaza de forma clara sin corromper datos. |

Para cada paso anota entrada, acción, esperado, observado, candidato, fecha y entorno. La ausencia de excepciones en una consola no demuestra persistencia. Es necesario releer el estado de forma independiente y, si importa la durabilidad, reiniciar el proceso que guarda los registros.

Si varios empleados pueden operar a la vez, se ensayan acciones solapadas o concurrencia adecuada a la arquitectura. Un test secuencial no prueba seguridad ante dos operaciones simultáneas. Si hay datos personales, se utilizan registros ficticios en capturas y demos; los secretos de acceso nunca se incorporan al repositorio.

La evaluación perceptual debe hacerla una persona competente cuando la experiencia de usuario tenga importancia. Esa prueba no reemplaza los tests de backend ni la inspección de DB. Del mismo modo, una prueba de DB no prueba que alguien encuentre un botón o comprenda el mensaje de error. Cada gate tiene su propósito y su resultado.

## 7. Segunda capacidad: cuotas y pagos

Una vez aceptada la identidad de socios, el club solicita cuotas. Ahora el Planner confirma períodos de pago, vencimientos, deudas parciales, correcciones, permisos, idempotencia y quién puede revisar o revertir una operación. El estado «al día» debe surgir de reglas explícitas y datos actuales, no de un cálculo improvisado en cada pantalla.

Una decisión posible del CLIENT es: «Un pago cargado por error se revierte con un asiento de auditoría; el registro original nunca se borra». Tiene consecuencias de producto, privacidad y arquitectura. El Planner persiste la decisión; I3 implementa las operaciones, esquema, restricciones, pruebas, recuperación y evidencia necesaria.

La repetición de una solicitud —por red inestable, doble clic o reintento automático— no debe generar un cobro duplicado si la política acordada exige una operación idempotente. Eso se prueba en los límites adecuados, no solamente llamando una función en aislamiento. Si la aplicación procesa dinero real, los gates de autorización, auditoría, seguridad y publicación necesitan un tratamiento proporcional y explícito.

Las actividades e inscripciones se construyen después de tener identidad y estado de cuotas confiables. No se agrega por moda un conjunto de microservicios, un procesador de pagos cloud, una aplicación móvil o un sistema complejo de roles. Cada elemento adicional debe justificar el riesgo, coste y beneficio. La meta de la primera versión es que alguien del club resuelva tareas concretas.

## 8. Evaluar el ejemplo completo

Al terminar, deberías poder distinguir qué decidió el CLIENT, qué requisitos confirmó el Planner, cómo I3 desarrolló dentro del charter, qué evidencia física y de DB se produjo, qué revisó una persona independiente y quién puede aceptar cada gate. También deberías entender por qué los tests verdes del framework no hacen automáticamente aceptable la aplicación construida con él.

El objetivo no es memorizar nombres internos de JSON o enumerar todas las políticas. Es conocer dónde vive la verdad vigente, quién puede cambiarla, cómo se demuestra un comportamiento y qué hacer cuando el contexto se pierde. Una arquitectura con roles elaborados pero sin recorrido de socio demostrable no entregó la capacidad solicitada.

La misma idea se aplica a otros productos: una API CRUD, un servicio de reservas, un dashboard de un negocio, una aplicación educativa o un juego. Lo que se debe demostrar cambia según el producto, pero la separación entre intención, autorización, implementación, evidencia y aceptación sigue siendo útil.

## 9. Primer ciclo con datos ficticios

Para practicar, inventá a «Persona de prueba A» y un número de contacto obviamente ficticio. Preguntá qué datos son obligatorios, qué identificador debe ser único y quién puede modificarlos. El Planner transforma decisiones confirmadas en requisitos verificables. Ingeniería selecciona persistencia, controles de unicidad, manejo de concurrencia y transacciones.

Recorré todo el circuito propuesto: alta, listado, búsqueda, edición, reinicio, readback, desactivación y consulta autorizada del historial. Anotá qué ocurrió realmente en cada etapa. Una captura al crear el socio es el comienzo del ensayo, no una prueba de que la DB guardó el cambio. Si todavía no programaste la app, marca esos pasos como `NOT RUN`, nunca como PASS.

Agregá pruebas negativas: un identificador repetido, campo inválido, desconexión controlada de base durante el guardado y dos envíos del mismo formulario. Las respuestas esperadas dependen de las reglas confirmadas, pero no debería generarse un estado silenciosamente contradictorio. En un producto con varios operadores, verificá condiciones de carrera que afecten registros o cupos.

El feedback de la primera prueba puede modificar detalles de experiencia: orden de campos, claridad de una advertencia, lugar de un botón. Si una observación implica una regla de negocio nueva, corresponde al CLIENT y Planner; si revela un defecto bajo reglas existentes, I3 lo repara en el charter. La frontera se decide por el significado de la observación, no por el cargo de quien la encontró.

## 10. Registrar y enrutar un defecto

Supongamos que el CLIENT desactiva a «Persona de prueba A» y descubre que el historial de pagos desaparece. Si conservarlo era requisito aprobado, esto es un defecto in-charter. La evidencia debe indicar candidato exacto, pasos de reproducción, datos ficticios usados, resultado observado y gate afectado.

El Planner consolida el falsifier y lo entrega a I3. El Controller investiga las relaciones de persistencia, implementa la corrección causal, agrega regresión, prueba readback después de reinicio, integra la versión nueva y solicita la revisión apropiada. No crea campaña paralela, no pide al CLIENT determinar cómo funciona una clave foránea y no acepta un PASS emitido para los bytes anteriores.

En otro momento el CLIENT pregunta si un socio inactivo puede recuperar el mismo número al ser reactivado. Si no había una regla confirmada, no se puede llamar bug a una de las respuestas posibles. El Planner hace la pregunta de producto, registra la nueva decisión, examina impactos y determina si puede resolverse dentro de los límites actuales o necesita revisar la estrategia.

El manual no sustituye hechos. Ninguna de estas historias prueba que en algún repositorio real haya sido implementada una operación. Lo correcto es usar el ejemplo para aprender qué testigos, contratos y autorizaciones pedir antes de aceptar un resultado equivalente.

## 11. Dependencias del segundo ciclo

Las cuotas necesitan identificador estable de socio y reglas claras de pagos parciales, duplicados, vencimientos y correcciones. El Planner registra su definición usando la capacidad de socios aceptada; I3 trabaja con el candidato e interfaces actuales, no con una implementación vieja recordada de una conversación.

Antes de implementar la inscripción a actividades, hay que comprobar que el sistema realmente produce un estado de cuotas consistente y consumible. Si la elegibilidad depende de una deuda mal definida, una inscripción puede aceptarse en una pantalla y rechazarse en otra. El objetivo del diseño por dependencias es evitar dos lógicas de negocio contradictorias.

El orden de capacidades también ayuda a conversar con el CLIENT. Un hito visible de socios puede probarse antes de invertir en pagos; un hito de cuotas puede validarse antes de un calendario de actividades. Así se obtiene feedback temprano, se detecta un problema en el modelo cuando todavía es barato corregirlo y se protege la fecha de entrega.

No confundas una dependencia de producto con la necesidad de multiplicar agentes. Un único Controller competente puede orquestar implementación y QA; el Planner conserva estrategia y aceptación. Los especialistas o revisores independientes se usan cuando reducen un riesgo material, con scope, evidencia y autoridad claramente limitados.

## 12. Ejercicio final de recuperación

Imaginá que el trabajo se interrumpe hoy y mañana entra un Planner nuevo que no leyó este chat. El repositorio y el runtime autorizado deben permitir reconstruir qué capacidad de socios se aceptó, qué candidato y evidencias respaldan esa aceptación, qué preguntas sobre cuotas siguen abiertas, quién posee la ejecución y cuál es la próxima acción permitida.

Si dos campañas reclaman el mismo recurso, hay que conciliar autoridad antes de escribir. Si el último informe dice `CURRENT` pero apunta a una versión anterior, la discrepancia se investiga; no se decide por el mensaje más reciente. Si falta un testigo de DB o una fuente comprometida, se establece HOLD específico para el trabajo dependiente y se siguen realizando comprobaciones read-only permitidas.

Para cerrar el ejercicio, clasificá cada evento como decisión nueva de producto, defecto ordinario dentro del charter, fallo de entorno, permiso externo pendiente o invalidación estratégica. Esa clasificación define owner y ruta. Si podés reconstruir el siguiente paso sin depender de la memoria de una conversación, el framework comenzó a cumplir su propósito.

Lo más importante del ejemplo no es haber instalado `.agentic-sdlc/`. Es transformar una intención humana en capacidades demostrables, sin perder coherencia después de cambios, interrupciones y revisiones. La prueba definitiva está en el producto que alguien usa y en la evidencia que otra persona puede comprobar.

## Fuentes y vigencia

- [Ejemplo sintético mínimo del repositorio](../../../../examples/minimal/README.md)
- [Fork y bootstrap](../../../01_FORK_AND_BOOTSTRAP.md)
- [Discovery, requisitos, stack y delivery](../../../21_PRODUCT_DISCOVERY_REQUIREMENTS_STACK_AND_DELIVERY.md)
- [Límite de decisiones del CLIENT](../../../../protocols/CLIENT_BOUNDARY.md)
- [Estándar de Engineering Campaign Charter](../../../../protocols/CAMPAIGN_CHARTER_STANDARD.md)
- [Inicio público y soporte v1.4](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md)
- [Preflight de repositorio ya gobernado](../../../32_EXISTING_GOVERNED_ATTACHMENT.md)

Los pasos y resultados de la aplicación del club son didácticos. No representan un sistema desplegado, una capacidad aceptada ni una integración de IA o servicio externo.
