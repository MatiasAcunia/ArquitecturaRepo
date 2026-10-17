# 07 — Ejemplo guiado: club | ArquitecturaRepo v1.3.0

> Manual de uso revisado para el release público v1.3.0 (17 de octubre de 2026). Conserva el texto del manual original 00–07 de septiembre de 2026 y solo añade aclaraciones relacionadas con cambios reales en v1.3. Los pies de las figuras se conservan, pero esta transcripción Markdown no incluye las imágenes del PDF original.

## Actualización comprobada para v1.3.0

- El ejemplo del club sigue siendo un proyecto ficticio de aprendizaje; no se distribuye un backend terminado ni una promesa de que un modelo genere el CRUD automáticamente.
- Secuencia de primer uso: scaffold `STATEFUL` en proyecto sin gobierno previo → discovery y baseline → Goal/charter y work order → plan de I3 → implementación de alta/consulta/edición → pruebas del mismo candidato → revisión y acceptance gates.
- Para un proyecto ya gobernado, el instalador no añade una segunda autoridad: primero usar el attachment read-only y diseñar migración conservadora.
- En cualquier uso real deben verificarse DB/WAL, recuperación, entradas no válidas, permisos, privacidad y funcionamiento de UI si corresponde, además de pruebas unitarias.

## Contenido del manual conservado

### Página 46 de la edición original

A R Q U I T E C T U RA R E P O / C O L E C C I Ó N D E U S O




07
Ejemplo guiado: club

Caso didáctico, no aplicación desplegada




Matías Acuña · ArquitecturaRepo                                Revisión de compatibilidad: 17 de octubre de 2026

### Página 47 de la edición original

Contenido

     • 1. Producto de ejemplo: un club con necesidades                   • 7. Segunda capacidad: cuotas, sin inflar el alcance
       concretas                                                         • 8. Evaluación final del caso
     • 2. Antes de programar: preguntas que alteran el                   • 9. El primer ciclo con datos ficticios
       producto
                                                                         • 10. Cómo se registra un hallazgo y qué pasa
     • 3. Instalar sin confundir una plantilla con un                      después
       producto
                                                                         • 11. El segundo ciclo depende del primero
     • 4. Primera capacidad: gestionar socios
                                                                         • 12. Ejercicio final: reproducir el proyecto en otro
     • 5. De Planner a ejecución: un encargo completo                      contexto
     • 6. Qué se comprueba antes de aceptar




1. Producto de ejemplo: un club con necesidades concretas

Una persona administrativa debe registrar socios, cuotas, actividades e inscripciones. El sistema
conservará historial, evitará inconsistencias de cupos y permitirá saber quién está al día. La primera
versión será sencilla y de uso interno. No se incluyen pagos online, aplicación móvil, facturación fiscal ni
integraciones externas hasta que exista una necesidad de producto confirmada.




  Figura 10. Dependencias del caso didáctico. Esquema explicativo; no acredita un proyecto de destino.



El ejemplo no describe una app ya desarrollada. Es un recorrido didáctico. El codebase real, el stack,
las reglas finales y los gates deben derivarse del proyecto que efectivamente exista, no copiarse como
hechos desde estas páginas.


2. Antes de programar: preguntas que alteran el producto

El Planner consulta quién opera el club, si la app se usa en una PC o en red, qué datos personales guarda,
cómo se administran respaldos, el presupuesto, la fecha objetivo y qué acciones pueden modificar
historial. Un requisito inicial posible es “se puede desactivar un socio, pero no perder sus pagos
anteriores”.

El CLIENT responde las reglas de negocio; por ejemplo: “Un socio con cualquier cuota vencida no puede
inscribirse en una actividad nueva y debe ver el motivo”. El Planner también pregunta qué ocurre si una
actividad ya está llena y si una cancelación libera cupo. Hasta confirmar esas reglas, no puede tratar sus
suposiciones como comportamiento vigente.

Baseline de ejemplo, sujeto a confirmación:

### Página 48 de la edición original

Alcance                                                Primera versión

Socios                                                 Alta, edición, búsqueda y desactivación conservando historial.

Cuotas                                                 Registro de pagos, período adeudado y consulta de estado.

Actividades                                            Nombre, fecha, capacidad y disponibilidad.

Inscripciones                                          Alta/cancelación y control de cupo y reglas de cuota.

Excluido                                               Pagos online, app móvil, notificaciones masivas y dashboard
                                                       complejo.



Un sistema con cuotas e inscripciones tiene estado persistente; por eso el Planner evalúa el perfil
STATEFUL y sus exigencias de DB, idempotencia, recovery y seguridad proporcional a los datos reales.



3. Instalar sin confundir una plantilla con un producto

El lector prepara un repo club-app y, desde el starter, crea .agentic-sdlc con el perfil seleccionado. El
scaffold comienza HOLD / UNTRUSTED_CONTEXT ; no declara una campaña activa ni afirma que la aplicación
funciona. Después I2/I3 efectúan discovery, especificación de adopción, preflight, validación y
reconstrucción desde evidencia real.

El Planner presenta al CLIENT una revisión del alcance actual, confirma requisitos, decide stack y red/
seguridad/backup y registra un plan de entrega con fechas y condiciones observables. Recién cuando el
baseline aplicable y el contexto son coherentes, crea el primer charter.


4. Primera capacidad: gestionar socios

El Planner puede empezar por socios porque cuotas e inscripciones necesitan una identidad estable. Esta
es una dependencia de producto, no una obligación de implementar un framework o estructura de
carpetas determinada.

Objetivo del charter: una persona administrativa crea un socio, consulta su ficha, corrige datos y lo
desactiva sin perder registros históricos. El charter define quién controla la persistencia, qué interfaces
afecta y cuáles son los gates aplicables: validación de entradas, duplicados, escritura/lectura real en DB,
flujo de UI, tratamiento de errores y revisión independiente del candidato exacto.

El CLIENT no elige el ORM ni decide la estructura del schema. El equipo técnico debe justificar e
implementar una solución adecuada al entorno y a las restricciones confirmadas. Si el proyecto ya
contiene datos, debe preservar y migrar lo que corresponda.


5. De Planner a ejecución: un encargo completo

Un mensaje bien formado del Planner puede organizarse sin microadministrar el trabajo interno:


  Goal: entregar la capacidad de gestión de socios descrita en el charter actual. Context: requisitos
  confirmados, Product State, repositorio y ref exactos. Constraints: preservar historial; no introducir
  pagos, notificaciones ni features no solicitadas. Execution gates: probar los flujos de alta, búsqueda,
  edición y desactivación con persistencia real; comprobar entradas inválidas y duplicados; revisar el
  candidato integrado de forma independiente. Done when: existe evidencia física del flujo, pruebas
  aplicables, candidato/ref exacto y terminal honesto para auditoría estratégica.

### Página 49 de la edición original

I3 puede descomponer tácticamente, delegar implementación o review, depurar y reintentar. Si al
guardar un socio se duplica el registro tras un doble clic, es un defecto dentro del alcance: no hace falta
abrir una segunda campaña para arreglarlo.


6. Qué se comprueba antes de aceptar

Plan de prueba del caso — no evidencia de una app existente
Prepará datos ficticios: SOCIO-001 , una ficha activa y una cuota de ejemplo. Ejecutá el alta, consultá por
un identificador admitido, corregí un dato, cerrá la aplicación y volvé a abrirla. Si el producto utiliza
persistencia, verificá que la lectura posterior devuelva la modificación. Desactivá la ficha y comprobá que
el filtro de activos la excluye pero el historial accesible la conserva. Registrá cada acción con entrada,
salida esperada, salida observada y ref del candidato.

No copies este resultado como “PASS” sin haber ejecutado la app concreta. El caso de club del manual es
una especificación didáctica, no un producto desplegado ni un benchmark de eficacia de
ArquitecturaRepo. Reglas de deuda, pagos y cupos requieren confirmación propia si se implementan en
otro proyecto.

Prueba visible de ejemplo: crear el socio “Caso de prueba 001”, consultar sus datos, cerrar/reabrir la
app y comprobar persistencia, modificar un campo, desactivar la ficha y verificar que desaparece de la
lista de activos sin borrar el historial. Si corresponde, ejecutar el flujo con dos intentos concurrentes y
demostrar que el resultado no duplica una operación sin autorización.

El informe de Codex puede contener comandos, resultados de tests, capturas y datos sintéticos. Eso no
autoriza al Planner a afirmar que el flujo funciona si nunca se comprobó físicamente. Al haber datos
personales, no uses socios reales en videos ni en logs compartidos.

Aceptación estratégica: el Planner contrasta candidato, requisitos y gates; cuando la experiencia de
uso es material, pide la valoración del CLIENT. La aceptación se persiste junto con el ref actual; no queda
únicamente en “me gustó” dentro de un chat.


7. Segunda capacidad: cuotas, sin inflar el alcance

Tras aceptar socios, el CLIENT pide registrar pagos, consultar si un socio está al día y conservar el
historial. El Planner aclara períodos, vencimientos, correcciones y permisos; decide las dependencias
técnicas; crea un nuevo charter completo. Una prueba importante es que corregir un pago no destruya el
historial de operación. Inscripciones y control de cupos llegan después, con reglas confirmadas.

No agregues por inercia microservicios, pagos online, múltiples roles complejos ni una aplicación móvil.
Esos mecanismos aumentan coste y riesgo sin aportar nada si el producto aún no los requiere.


8. Evaluación final del caso

Al finalizar el ejercicio, deberías poder explicar: qué decisión tomaste vos como CLIENT, cómo el Planner
registró los requisitos vigentes, qué evidencia física aportó I3, por qué una prueba verde no equivale a
aceptación, qué ocurre con un bug de la misma feature y cómo reconstruirías el proyecto desde una
conversación nueva.

El objetivo no es memorizar los archivos internos del starter. Es reconocer qué autoridad corresponde a
cada actor y exigir un resultado observable cuya continuidad pueda reconstruirse desde el repositorio.

### Página 50 de la edición original

9. El primer ciclo con datos ficticios

Empezá con un registro sintético, nunca con datos personales reales de socios. El CLIENT confirma los
campos indispensables para identificar una ficha; el Planner deriva la capacidad de producto y el equipo
decide modelo de datos, controles de duplicados y transacciones. La primera demostración no debería
limitarse a una captura de formulario: debe probar un recorrido completo.

Recorrido de aceptación del ejemplo: crear “Socio Prueba A”; confirmar que aparece en la lista;
buscar por un dato admitido; editar un teléfono ficticio; cerrar y reabrir la aplicación; confirmar que el
cambio persiste; desactivar la ficha; verificar que ya no aparece como activo y que puede consultarse el
historial mediante el flujo previsto. Cada paso tiene una salida observada; la ausencia de un error visible
no demuestra que la DB haya conservado la escritura.

Pruebas negativas de ejemplo: intentar crear dos fichas con identificador único duplicado, ingresar un
dato que el producto considere inválido, guardar con la conexión a la base de datos interrumpida en un
entorno controlado y repetir una operación que podría llegar dos veces. El resultado esperado depende
de las reglas confirmadas, pero no debe dejar datos silenciosamente inconsistentes. Si el objetivo incluye
varios operadores, se necesita verificar el comportamiento concurrente en ese entorno, no deducirlo de
un test secuencial.


10. Cómo se registra un hallazgo y qué pasa después

Durante la revisión, el CLIENT descubre que la ficha se desactiva pero desaparece también del historial
de pagos. Esto contradice un requisito vigente: se comunica el recorrido, el candidato exacto y la salida
observable. El Planner no debate si vale la pena conservar el historial porque el CLIENT ya lo confirmó.
Devuelve el defecto consolidado a I3; I3 lo investiga, corrige, integra, prueba otra vez y solicita revisión
independiente del candidato nuevo.

Otro hallazgo posible es una pregunta de producto nueva: ¿una persona desactivada puede reactivarse y
conservar el mismo número? Como no estaba especificado, el Planner consulta al CLIENT, actualiza la
autoridad vigente y evalúa si la campaña sigue cubriendo el cambio. Es distinta la ruta para un requisito
abierto que para una implementación defectuosa.


11. El segundo ciclo depende del primero

Cuando socios está aceptado, cuotas necesita una referencia estable a cada ficha y reglas explícitas para
pagos parciales, pagos duplicados, vencimientos y correcciones. El Planner no debe inventar esas reglas.
El CLIENT puede decidir, por ejemplo, que un pago registrado por error se anula con auditoría en vez de
borrarse. La ingeniería traduce esa decisión a modelo de persistencia, interfaz, pruebas y recuperación.

Antes de agregar actividades o inscripciones, se comprueba que los estados de cuota que esas reglas
consultarán estén disponibles y sean actuales. Si se intenta empezar por inscripciones, se corre el riesgo
de codificar una política provisoria que después no coincide con la gestión real del club. Esa relación
entre capacidades es un ejemplo de critical path de producto, no de la obligación de tener muchos
agentes.


12. Ejercicio final: reproducir el proyecto en otro contexto

Imaginá que terminaste la sesión y mañana entra un agente nuevo. Sin enviarle el chat anterior, debe
poder identificar que socios está aceptado, qué candidato y evidencia lo demuestra, qué requisitos de
cuotas siguen abiertos y cuál es la próxima acción legal. Si encuentra dos campañas “activas” diferentes
o un informe antiguo etiquetado como actual, tiene que declararlo y no continuar a ciegas.

### Página 51 de la edición original

La práctica está completa cuando se puede repetir ese ejercicio y el CLIENT sabe distinguir una decisión
de negocio, un bug in-scope, una incapacidad temporal del entorno y una verdadera invalidación
estratégica. La meta del ejercicio es una aplicación comprobada en el entorno del ejemplo y un estado de
trabajo que una sesión nueva pueda reconstruir. Que esa continuidad se logre debe probarse; no se
deduce de instalar el starter.

Referencias de esta edición
Fuente: repositorio público ArquitecturaRepo en el commit 9c00e19b74d1 . Rutas verificadas:

  • examples/minimal/README.md
  • docs/01_FORK_AND_BOOTSTRAP.md
  • docs/21_PRODUCT_DISCOVERY_REQUIREMENTS_STACK_AND_DELIVERY.md
  • protocols/CLIENT_BOUNDARY.md
  • protocols/CAMPAIGN_CHARTER_STANDARD.md

Las instrucciones de este volumen describen el starter y un procedimiento de uso. Ninguna prueba de los
ejemplos sustituye la verificación del proyecto de destino.
