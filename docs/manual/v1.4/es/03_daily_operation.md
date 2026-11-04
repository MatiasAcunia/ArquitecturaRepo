# 03 — Operación diaria

ArquitecturaRepo · Manual completo de uso · Edición v1.4 · Español

> Este capítulo parte de un proyecto ya adoptado y con un charter vigente. El controlador opcional del starter ofrece mecanismos portables de referencia; no es una garantía de ejecución autónoma en Codex Desktop ni en otro host propietario. La compatibilidad de cada entorno debe comprobarse físicamente.

## Contenido del capítulo

1. Preparar una sesión sin empezar de nuevo
2. Convertir un deseo en una capacidad comprobable
3. Qué hace I3 cuando el trabajo se complica
4. Autorizaciones y efectos externos
5. Cómo leer críticamente un reporte del ejecutor
6. Git y la continuidad
7. Cierre diario en cinco preguntas
8. Una jornada sin depender de la memoria del chat
9. Ejemplo de despacho delimitado
10. Interpretar estados de un controlador
11. Procesar el reporte final
12. Dejar una sesión recuperable

## 1. Preparar una sesión sin empezar de nuevo

Antes de pedir otra función, identificá el proyecto, el worktree, la rama y el ref actuales, los cambios locales pendientes, el Product State canónico, el charter activo y el último candidato físicamente comprobado. Si una sesión se cerró por un límite del servicio, el trabajador nuevo tiene que recuperar el checkpoint durable, no recrear «un proyecto parecido» desde un prompt viejo.

Cuando el checkout es confiable y el baseline está identificado, la sincronización comienza por examinar el delta exacto de Git y sus dependencias. No reclones ni ejecutes `git pull` automáticamente en cada reanudación si hay cambios de usuario sin integrar. Tampoco confíes ciegamente en un delta incremental cuando las ramas divergen o la autoridad de source/currentness está en disputa: primero se investiga el conflicto de solo lectura.

El CLIENT puede recibir un resumen compacto, sin tener que decidir qué SHA o snapshot de DB prevalece. Inspeccionar el repositorio verdadero, las instrucciones aplicables, los cambios locales y las referencias de ownership es responsabilidad técnica. El Planner reconstruye el objetivo y la campaña antes de autorizar una nueva capacidad. Si falta una evidencia indispensable, se declara el hecho desconocido y se detienen solamente las escrituras que dependen de él.

Podés colocar la planificación en una ventana y el editor en otra, pero esa comodidad visual no constituye un protocolo de seguridad. La continuidad surge del código, el estado y los checkpoints reconstruibles, no de mantener abiertas dos conversaciones. Si alguien modificó código remotamente, el I3 debe reconciliarlo con el trabajo local antes de mutar.

## 2. Convertir un deseo en una capacidad comprobable

«Registrar pagos de cuotas, conservar el historial y mostrar quién está al día» es una capacidad observable. «Escribir la función de pagos» es una posible microtarea. El Planner comienza por el resultado que necesita el usuario, identifica interfaces, dependencias y riesgos, y autoriza el charter de esa capacidad. La implementación interna pertenece a I3.

Un encargo breve del CLIENT podría decir:

> Necesito que el personal registre pagos de cuotas sin perder movimientos anteriores y pueda ver quién debe. Por ahora no quiero pagos online. Priorizá una pantalla simple. Antes de aceptarlo quiero comprobar todo el recorrido.

La petición define intención, pero no necesariamente basta para iniciar ejecución: todavía hay que revisar requisitos actuales, reglas de datos, código, autoridad y entorno. El despacho del Planner contiene objetivo, fuentes verificadas, límites, interfaces, owners, gates y evidencia necesaria. No debería convertir al CLIENT en el coordinador de cada especialista.

En trabajo prolongado, costoso o por lotes, el [work order orientado al resultado](../../../44_OUTCOME_FIRST_AGENT_EXECUTION.md) añade un inventario concreto, ruta operativa viable, presupuestos, condiciones de parada, salida y lectura física de los resultados. Complementa al charter sin reemplazarlo ni inventar autorizaciones de proveedores. Si la tarea consiste en comprobar archivos y hashes, una herramienta determinista puede resolverla sin solicitar una evaluación de un modelo pago por cada elemento.

## 3. Qué hace I3 cuando el trabajo se complica

Supongamos que el registro de un pago está implementado, pero falla una prueba de integración. I3 conserva la reproducción, identifica el componente causal, corrige el defecto, vuelve a ejecutar los tests pertinentes, integra el candidato y obtiene revisión independiente cuando corresponde. No necesita un nuevo charter por cada falla.

La depuración, los reintentos, los refactors internos, las migraciones previstas, la reparación de evaluadores, la integración y la recuperación tras una interrupción pertenecen continuamente al controlador I3 dentro del alcance autorizado. Si se repite la misma clase de problema, tiene que revisar el subsistema y sus tests de forma integral, no acumular remiendos locales o devolver el problema al Planner como una microcampaña.

Un bloqueo verdadero de currentness, la ausencia de autorización para una acción externa o un cambio material del objetivo se tratan de manera distinta. El I3 registra el límite exacto y al owner que puede resolverlo; no rebautiza el problema como «otro retry». A menudo puede seguir investigando de solo lectura mientras las escrituras dependientes permanecen en HOLD.

La revisión independiente debe cubrir el candidato exacto que se devuelve a auditoría. Si el código, la configuración o los artefactos relevantes cambian materialmente después de una revisión favorable, hay que renovar las comprobaciones afectadas. No se traslada automáticamente un PASS de la versión A a la versión B.

El `tools/campaignctl.py` portable ofrece mecanismos de referencia de control, pero no es un sistema universal de agentes distribuidos. Los helpers de Goal y plan táctico pueden administrar registros sin demostrar que un host externo activó comandos nativos como `/plan`. El [runtime de referencia](../../../11_REFERENCE_RUNTIME.md) documenta lo que puede afirmarse de su implementación.

## 4. Autorizaciones y efectos externos

| Acción | Tratamiento razonable |
| --- | --- |
| Leer código o ejecutar pruebas locales dentro del permiso otorgado. | Trabajo técnico rutinario autorizado. |
| Modificar e integrar código dentro de un charter aprobado. | Responsabilidad de I3 con ownership y worktree verificados. |
| Instalar dependencias o acceder a herramientas nuevas. | Comprobar procedencia, alcance, permisos y necesidad. |
| Desplegar, publicar, enviar correos, gastar crédito o borrar datos relevantes. | Autorización reservada específica y preflight proporcional. |
| Copiar un token o una base privada en el chat. | No hacerlo; usar el mecanismo aprobado de secretos y datos. |
| Encontrar contradicciones de código, DB, fuente o ownership canónicos. | HOLD para acciones dependientes y reconciliación basada en evidencia. |

El CLIENT decide reglas, experiencia y riesgos de producto, además de publicación y gasto cuando corresponden. No necesita elegir el nombre de índices SQL, resolver conflictos de Git, diseñar transacciones o coordinar la recuperación. La arquitectura debe mantener esa frontera sin apropiarse de las decisiones que realmente le pertenecen.

## 5. Cómo leer críticamente un reporte del ejecutor

Un reporte útil identifica el candidato exacto y su entorno, el comportamiento que se intentó obtener, los cambios físicamente comprobados, las pruebas ejecutadas, los fallos y correcciones, el alcance de la revisión independiente y los gates todavía abiertos. No mide progreso por número de commits, tokens, agentes o horas de runtime.

Cuando aparece `PASS`, preguntá qué gate significa. Una prueba unitaria puede comprobar lógica con mocks; una de integración, la comunicación entre componentes; una de DB/currentness, persistencia y referencias; una física, que la aplicación realmente abra y permita completar una tarea; una perceptual, que la experiencia sea adecuada para una persona. Pasar una no demuestra necesariamente las otras.

El informe debe terminar indicando la próxima acción y su owner. Si falta una regla nueva del negocio, vuelve al CLIENT y al Planner. Si es un bug previsto por el charter, permanece en I3. Si hay un candidato listo, vuelve para auditoría estratégica consolidada. El CLIENT no debe convertirse en director técnico de incidentes.

Al aceptar una capacidad, el Planner registra qué candidato se aceptó, con qué charter, requisitos y evidencia. Al rechazar defectos dentro del alcance, devuelve un conjunto consolidado de falsificadores a la misma campaña. Un cambio genuino de producto se persiste como decisión nueva y no se disimula bajo el nombre de «bug fix».

## 6. Git y la continuidad

Git conserva código e historial, pero no sustituye Product State, registros de autorización ni estado de la base de datos. Un commit identifica contenido y padres; no prueba quién autorizó cada cambio, quién es el dueño de una campaña o si el usuario aceptó el producto. El movimiento de una rama tampoco demuestra currentness de datos reales.

No hagas un commit canónico por cada mensaje de I4. Los especialistas entregan cambios y evidencias acotados; la integración la realiza el owner correspondiente. Un worktree puede conservar trabajo del usuario sin commitear. No lo borres para obtener un status «limpio». Cuando trabajan varios actores, analizá la interferencia según los archivos, bases, runtime y recursos que comparten, no solamente según el nombre del proyecto.

Reutilizá un checkout confiable cuando sea seguro. Los worktrees temporales se justifican cuando existe concurrencia real, no como hábito. Las capturas, renders, exports y caches derivados deberían ser efímeros o ignorados salvo cuando constituyan evidencia canónica. El espacio en disco es un recurso que hay que proteger, sin destruir por ello registros actuales ni artefactos necesarios.

El mismo charter puede continuar tras el límite de uso de una sesión si el ref, checkpoint, owners y evidencia siguen reconstruibles. El límite de tokens de un servicio no invalida por sí mismo una campaña. Si un host ya no permite abrir el thread anterior, recurrí al estado canónico en vez de fingir que el historial sigue disponible.

## 7. Cierre diario en cinco preguntas

Antes de terminar una jornada, el sistema debería poder responder:

1. ¿Qué capacidad sigue activa y quién controla la ejecución?
2. ¿Qué ref de código, Product State y testigos de DB/currentness están realmente comprobados?
3. ¿Cuál fue el último gate que pasó, con qué evidencia?
4. ¿Qué defecto, riesgo, permiso o decisión de producto continúa abierto?
5. ¿Cuál es la próxima acción válida y quién la debe realizar, sin pedirle al CLIENT que arbitre cuestiones técnicas?

Persistí las decisiones materiales y próximas rutas en las superficies canónicas del repositorio. El chat puede conservar contexto conversacional, pero no debe ser la única fuente de verdad. El próximo trabajador tendría que recuperar las respuestas por su cuenta.

## 8. Una jornada sin depender de la memoria del chat

Al comenzar el día, recuperá el Goal vigente antes de pedir otra función. El Planner comprueba si hay campaña abierta, último ref integrado, evidencia pendiente y decisiones reservadas al CLIENT. Las rutas razonables son continuar I3, auditar un terminal consolidado, pedir una decisión de producto o autorizar una capacidad nueva después de satisfacer sus dependencias.

Si el trabajo se interrumpió por capacidad o por una caída, retomá desde un checkpoint real. Cuando no existe checkpoint, intentá reconstruir el estado durable. Si tampoco hay evidencia suficiente, declarás qué se perdió y detenés las acciones dependientes. Una nueva sesión que solo afirma «íbamos por la mitad» no demostró que el proyecto esté a mitad de camino.

## 9. Ejemplo de despacho delimitado

Un mensaje de ejecución para una campaña ya autorizada puede ser compacto:

> **Goal:** implementar la gestión de socios prevista en el charter vigente.
>
> **Contexto:** leer el `AGENTS.md` real, requisitos confirmados, Product State, charter y código/ref actuales. Reconstruir ownership y currentness antes de mutar.
>
> **Restricciones:** conservar historial; respetar exposición local confirmada; no introducir pagos online ni funciones ajenas; no publicar ni gastar servicios externos.
>
> **Gates:** comprobar físicamente alta, búsqueda, edición, desactivación y persistencia al reiniciar; probar entradas inválidas y duplicados; revisar independientemente el candidato integrado.
>
> **Cierre:** entregar ref exacto, evidencia rastreable, resultado de revisión, riesgos y un terminal honesto. Resolver bugs, reintentos y refactors dentro de la misma campaña.

Este texto es un ejemplo, no una autorización universal para cualquier repositorio. Adaptalo al charter real. No inventes `AGENTS.md` ni Product State por aparecer en el ejemplo: hay que localizar las superficies actuales y declarar las ausencias concretas.

## 10. Interpretar estados de un controlador

| Estado | Qué indica | Qué no demuestra |
| --- | --- | --- |
| `READY` | Una unidad satisface las dependencias para poder ejecutarse. | Que ya se esté ejecutando o vaya a funcionar. |
| `ACTIVE` | Un contexto autorizado posee una ejecución activa. | Que el comportamiento final sea correcto. |
| `VERIFY` | Se preparan o realizan las comprobaciones pertinentes. | Que todos los gates del producto pasaron. |
| `HOLD` / `CAPACITY` | Hay una condición registrada que impide continuar. | Que haga falta abrir otra campaña. |
| `DONE` táctico | Una unidad de ejecución alcanzó sus condiciones locales. | Que Planner o CLIENT hayan aceptado la capacidad. |
| Terminal estratégico | I3 devuelve un candidato o bloqueo con evidencia. | Que exista autorización de publicación. |

El runtime portable es una referencia, no una integración nativa universal. Si el proyecto usa otro controlador, verificá que su implementación real preserve límites de autoridad, currentness, ownership, control de concurrencia y recuperación.

## 11. Procesar el reporte final

El Planner revisa candidato, requisitos actuales, entorno comprobado, resultados físicos, tests, review independiente y riesgos. No tiene que repetir el trabajo táctico de I3 ni aceptar un PASS por su etiqueta. Si la evidencia es incompleta, señala el gate específico sin declarar automáticamente que todo lo demás falló.

Para devolver un defecto dentro del charter, consolidá comportamiento observado, condiciones de reproducción, evidencia y gate bloqueado. I3 corrige e integra. Si vuelve reiteradamente la misma clase de falla, corresponde hardening del subsistema y revisión independiente, no una serie interminable de correcciones puntuales.

Una regla nueva de producto, permiso o interfaz incompatible puede justificar intervención estratégica. No se debe usar esa posibilidad para regresar a planificación cada vez que una prueba de regresión detecta un error conocido.

## 12. Dejar una sesión recuperable

Antes de cerrar, persistí el ref de código actual, objetivo vigente, checkpoint, evidencias de DB o artefactos cuando correspondan, mejores pruebas y review, bloqueos y ruta siguiente. Conservá datos privados fuera de documentación pública. Una release requiere su propio gate aunque una unidad táctica haya terminado.

El CLIENT debería poder preguntar «¿qué puedo usar hoy?» y recibir una respuesta sobre capacidades disponibles y riesgos importantes. La continuidad está demostrada cuando otra sesión recupera por sí misma esa respuesta desde el repositorio y el runtime autorizado, sin releer la conversación entera.

**Siguiente:** capítulo 04, Solicitar cambios.

## Fuentes y vigencia

- [Protocolo de ejecución](../../../../protocols/EXECUTION_TEAM_OS.md)
- [Ciclo de vida y evidencia](../../../../protocols/CAPABILITY_LIFECYCLE_AND_EVIDENCE.md)
- [Runtime de referencia](../../../11_REFERENCE_RUNTIME.md)
- [Eficiencia y cuidado del disco](../../../20_REPOSITORY_EFFICIENCY_AND_LOCAL_HYGIENE.md)
- [Work orders orientados al resultado](../../../44_OUTCOME_FIRST_AGENT_EXECUTION.md)
- [Código Goal/Plan](../../../../tools/goal_plan.py)
- [Código de host dispatch](../../../../tools/host_dispatch.py)
- [Controlador de campañas](../../../../tools/campaignctl.py)

Los mecanismos descritos son referencias y contratos. Su presencia en el repo no certifica el funcionamiento de ningún host externo ni aplicación específica.
