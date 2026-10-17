# 02 — El Planner y la adopción | ArquitecturaRepo v1.3.0

> Manual de uso revisado para el release público v1.3.0 (17 de octubre de 2026). Conserva el contenido textual del manual original 00–07 de septiembre de 2026 con correcciones específicas. La fuente era un PDF ilustrado: los pies de figura se conservan pero esta transcripción Markdown no reproduce las imágenes. No utilizar las cifras de página como referencia del archivo renderizado.

## Actualización comprobada para v1.3.0

- I2 debe reconstruir código, Product State, DB/WAL, Goal, interfaces, herramientas y restricciones del host. Un charter abstracto no constituye por sí mismo un encargo ejecutable.
- Antes de un Goal prolongado o de alto costo, entregar un **work order** con resultados observables, método viable, operación inicial, herramientas, verificación y rutas de fallo. Revisar `docs/44_OUTCOME_FIRST_AGENT_EXECUTION.md` y `tools/work_order_guard.py`.
- El work order se valida con `validate` y se evalúa con `assess`; en la versión portable v1.3 esas dos operaciones **no** dan por sí mismas aceptación física o perceptual.
- Mantener I2 en estrategia: bugs, reintentos y hardening dentro del charter se resuelven en I3; ningún documento del Planner crea un permiso nativo del host.
- La adaptación de un repositorio gobernado exige mantener sus owners y DB canónicos; no instalar un segundo control layer.

## Contenido del manual conservado

### Página 15 de la edición original

A R Q U I T E C T U RA R E P O / C O L E C C I Ó N D E U S O




02
El Planner y la adopción

Requisitos confirmados antes de ejecutar




Matías Acuña · ArquitecturaRepo                                Revisión de compatibilidad: 17 de octubre de 2026

### Página 16 de la edición original

Contenido

    • 1. Una conversación no es el proyecto                • 6. El examen real: contexto fresco
    • 2. Preparar el espacio de trabajo                    • 7. Primera campaña autorizada
    • 3. Discovery: hacer las preguntas correctas          • 8. Sesión inicial: qué decirle al Planner
    • 4. Baseline técnico y plan de entrega                • 9. Un baseline que se pueda confirmar
    • 5. Adoption: pasar del starter al proyecto real      • 10. Un ejemplo de primera campaña




1. Una conversación no es el proyecto

El Planner es el responsable estratégico de un límite de producto o workstream. Puede funcionar en un
chat de ChatGPT, pero sus decisiones duraderas no deben depender de ese chat. Su autoridad proviene
del objetivo y requisitos actuales, las instrucciones vigentes, los contratos de la arquitectura y la
evidencia física del repositorio. No debe inventar estado porque el último mensaje de un ejecutor dijo
“hecho”.

En un único proyecto pequeño, mantener un Planner y un Campaign Lead/ejecutor puede ser suficiente.
Un Master Owner aparte se justifica cuando existe una capa sistémica o varios productos/workstreams
que necesitan coherencia compartida, no como “versión superior” del Planner.


2. Preparar el espacio de trabajo

Instrucción de apertura que evita un falso handoff
El proyecto de ChatGPT es una interfaz cómoda, no una base de datos canónica. La primera sesión debe
identificar el repositorio correcto, leer AGENTS.md , el conjunto de protocolos aplicables y el estado vigente
del proyecto. Si no puede acceder al repo o a la ejecución actual, debe decir exactamente qué evidencia
le falta en vez de completar el contexto con la memoria de otra conversación.

No es obligatorio usar un modelo, esfuerzo de razonamiento ni conector específicos. Lo indispensable es
el acceso autorizado a la evidencia y que cada decisión material vuelva a su owner persistente. Un
Planner sin visibilidad del repo no debe declarar cerrada una campaña basándose solo en un
resumen de Codex.

Creá un espacio identificable para el proyecto en ChatGPT, si la interfaz de tu plan ofrece Proyectos.
Podés guardar ahí los manuales como referencia y agregar instrucciones breves. Conectá GitHub
únicamente con el alcance necesario. Verificá el acceso empezando por una consulta de lectura al
repositorio exacto; tener la app conectada no garantiza permisos sobre todos los repositorios.

Las opciones de modelos, esfuerzos de razonamiento, precios y límites se actualizan. Para trabajo
estratégico elegí la capacidad disponible suficiente y verificá el estado real: ningún modelo sustituye
permisos, evidencia actual ni una regla de autorización.

Instrucción inicial breve para el Planner:


  Actuá como I2 Planner de este proyecto. Yo soy CLIENT: decido requisitos y preferencias de producto
  y autorizo acciones externas reservadas. Empezá por reconstruir el repositorio real y los protocolos
  aplicables; no inventes estado. Definí las capacidades y charters; delegá ejecución táctica y
  depuración al I3/Campaign Lead. No me transfieras decisiones rutinarias de Git, código, pruebas,
  currentness ni recovery. Distinguí siempre lo comprobado, lo pendiente y lo que necesitás decidir
  conmigo.

### Página 17 de la edición original

Este texto es una entrada de rol, no reemplaza AGENTS.md , el conjunto vigente de requisitos ni el control
layer ya instalado. Al entrar en una sesión nueva, el Planner vuelve a leer las superficies actuales.


3. Discovery: hacer las preguntas correctas

Una sesión de discovery que produce una decisión
Primero identificá quién utilizará el producto y qué problema concreto resuelve. Después pedí ejemplos
de tareas completas, datos conservados, casos de error, condiciones de uso, nivel de exposición de red,
privacidad, costos, fecha objetivo y exclusiones. El Planner puede agrupar de tres a siete preguntas
relacionadas y devolver una síntesis para corregirla antes de profundizar.

Cerrá la conversación con una sola revisión explícita del baseline: funciones, restricciones, calidad,
seguridad/red, interfaz, datos/respaldos, costo, fechas, exclusiones y preguntas abiertas. La confirmación
del CLIENT no es una firma legal y no impide cambios posteriores; fija el estado contra el que el equipo
puede planificar ahora.

Pregunta útil para el CLIENT                            Decisión técnica que NO le corresponde resolver

¿Quién usa el sistema y desde dónde?                    Elegir puertos, topología de servicios o framework.

¿Qué datos deben conservarse al desactivar un socio?    Diseñar tablas, foreign keys o migrations.

¿Se permitirán pagos online en la primera versión?      Elegir proveedor de pagos sin autorización presupuestal.

¿Qué resultado debe verse antes de la fecha objetivo?   Orden interno de tareas, tipo de test o diseño de checkpoints.



El Planner presenta una síntesis única de requisitos funcionales, no funcionales, seguridad/red, UI, datos/
recovery, coste, fechas, exclusiones y preguntas abiertas. El CLIENT confirma si esa síntesis representa el
producto actual. La confirmación no es un contrato legal y puede cambiar más adelante; debe persistirse
junto con su versión y fecha.


4. Baseline técnico y plan de entrega

Qué registra el Planner después de la confirmación
Una vez confirmado el baseline de producto, el Planner decide lenguaje, frameworks, persistencia,
migraciones, pruebas, despliegue, red, secretos, interfaz y respaldo a partir de la evidencia del proyecto
y sus restricciones. Esas elecciones se persisten en state/TECHNICAL_BASELINE_CURRENT.json ; no deberían
volver a sortearse cada vez que empieza otra sesión.

El plan de entrega registra hitos observables con fechas objetivo, dependencias, condición de
terminado, confianza, riesgos y próxima revisión. Cambiar una fecha exige actualizar su historia, no
sustituir silenciosamente el valor anterior. La comprobación pre-campaña del starter nuevo es
baseline_guard.py , que puede bloquear una campaña material hasta que ese conjunto esté coherente.

El plan de entrega contiene hitos con fechas, dependencias, condición observable de terminado,
confianza, riesgos y fecha de revisión. Una fecha que cambia se registra; no desaparece silenciosamente
porque el agente escribió un plan nuevo.

No iniciar campaña si los requisitos no están confirmados, la estrategia de red/seguridad material está
sin resolver o el baseline_guard.py bloquea el inicio. El gate previene construir una solución técnica sobre
un producto que todavía no está definido.

### Página 18 de la edición original

5. Adoption: pasar del starter al proyecto real

Lo que la herramienta adopta y lo que no decide
El flujo reproducible del starter parte del scaffold, inventario de archivos sin mutar la aplicación,
especificación de adopción explícita, preflight en una copia temporal del control y promoción con journal.
discover_project.py inventaría metadatos; no interpreta por sí solo el objetivo del producto.
apply_adoption.py materializa decisiones ya reconstruidas y expresadas en una especificación válida; no
debe utilizarse para inventar requisitos, owners o evidencia de runtime.

Si existe una campaña activa, no ejecutes la adopción como atajo de reseteo. El informe de instalación
debe indicar qué quedó materializado, qué fue físicamente ejercitado, qué sigue en HOLD y cuál es la
primera frontera legal de trabajo. Una instalación sin ese detalle es una colección de archivos, no una
adopción demostrada.

El Planner debe coordinar que Codex, si tiene acceso local, ejecute las herramientas reales del starter
para inventariar y aplicar la adopción. Si el Planner dispone solo de lectura remota, prepara un dispatch
completo; no te pide que reconcilies a mano registros de ownership o JSON de Product State. La
aplicación original debe conservar sus archivos y su historial.

La adopción materializa requisitos actuales, estado, bootstrap, registro de owners y overlay de proyecto.
En un proyecto ya activo, no se debe ejecutar una adopción que intente inventar una nueva campaña
encima de una existente. El informe de instalación debe distinguir mecanismos simplemente declarados
de mecanismos materializados y físicamente comprobados.


6. El examen real: contexto fresco

La sesión nueva no recibe el relato anterior
Abrí un contexto realmente nuevo y compartí únicamente la identidad del repositorio, acceso a sus
pruebas y las instrucciones de entrada. Pedile que reconstruya rol y no-rol, requisitos actuales, ref de
código, Product State, campaña y checkpoint, gate abierto, mejor evidencia, hechos desconocidos,
siguiente acción autorizada y acciones prohibidas. El criterio no es que repita la arquitectura de memoria;
es que llegue al estado actual por superficies duraderas.

Si faltan datos que el agente debía poder leer, clasificá el problema de acceso antes de culpar al
repositorio. Si el propio estado es contradictorio, corregí el owner o el mecanismo de currentness; no
apruebes el examen dándole al siguiente chat un handoff más largo.




  Figura 5. Prueba de continuidad. Esquema explicativo; no acredita un proyecto de destino.

### Página 19 de la edición original

No pasa si usa documentos sustituidos como actuales, inventa el estado de la DB, confunde un PASS de
worker con aceptación o pide al CLIENT que arregle una contradicción técnica que el sistema debería
resolver. Una falla del test exige reparar la continuidad durable, no escribir un handoff cada vez más
largo.


7. Primera campaña autorizada

Primer charter: objetivo y límites, no lista de clics
La primera campaña debe nombrar una capacidad de producto cerrable, dependencias, owners,
interfaces afectadas, recursos que pueden interferir, evidencia necesaria, gates y falsifiers. No debe
imponer una lista de veinte microtareas o el número de intentos que I3 necesita para depurar. Los bugs
y revisiones fallidas dentro del alcance siguen en la misma campaña. Un cambio real de
requisitos, autoridad, interfaz crítica o alcance estratégico puede exigir volver al Planner.

Antes de autorizar, distinguí la prueba de infraestructura (“scaffold valida”) de la prueba de la capacidad
(“la persona usuaria completa el recorrido”). Si la segunda todavía no está definida, el charter no está
listo para ejecución material.


8. Sesión inicial: qué decirle al Planner

Abrí el repositorio de la aplicación con permisos de lectura y comenzá la sesión sin afirmar que el sistema
está instalado. Un encargo inicial completo puede ser breve; la complejidad técnica debe resolverla el
Planner:


  Quiero desarrollar una aplicación para registrar socios y cuotas de un club. Antes de planificar
  implementación, inspeccioná el proyecto real y el starter ArquitecturaRepo en modo de lectura.
  Guiame por las decisiones de producto que faltan. Separá lo que confirmé de lo que inferís; no
  inventes datos de aplicación o infraestructura. Prepará un baseline de producto para que yo lo
  confirme. Después elegí el perfil, la estrategia técnica y un plan con fechas. No inicies una campaña
  material mientras los gates de baseline y continuidad no estén satisfechos.


El Planner debería revisar el estado físico antes de preguntarte qué branch usar o si ya existe un archivo
que puede inspeccionar. Sí puede preguntarte cuántas personas usarán el sistema, desde qué lugar, qué
datos se conservan y qué diferencia hay entre un pago vencido y uno cancelado. Cada pregunta debe
alterar una decisión real de producto o una restricción relevante.


9. Un baseline que se pueda confirmar

No aceptes un resumen del tipo “vamos a hacer un CRUD profesional”. Pedí que la revisión previa a tu
confirmación exprese funciones, recorrido de usuario, datos y reglas, calidad esperada, exposición de red,
seguridad/privacidad, recuperación, presupuesto, plazo y exclusiones. Este es un ejemplo reducido:

Dimensión                           Requisito de ejemplo                      Estado

Usuario                             Una persona administrativa usa la app     A confirmar.
                                    desde una computadora del club.

Datos                               Socios, estado de cuotas e historial de   A confirmar.
                                    pagos.

Regla                               Desactivar una ficha no elimina           A confirmar.
                                    movimientos previos.

### Página 20 de la edición original

Dimensión                            Requisito de ejemplo                       Estado

Primera versión                      Alta, consulta, edición y desactivación    A confirmar.
                                     de socios.

Seguridad                            Acceso local; sin publicación pública en   A confirmar.
                                     la primera versión.

Interfaz                             Legible, simple, con errores claros y      A confirmar.
                                     búsqueda utilizable.

Exclusiones                          Sin pagos online ni app móvil inicial.     A confirmar.



Una vez que refleje tus decisiones reales, confirmá expresamente el baseline actual; no hace falta una
firma legal. Si cambiás de opinión después, ese cambio se incorpora mediante una revisión rastreable, no
mediante edición silenciosa de una frase vieja.

Después de esa confirmación, el Planner escoge y registra stack, base de datos, estrategia de
respaldo y recuperación, exposición de red, seguridad, entorno de ejecución y costos supuestos. También
define hitos con fechas, dependencias, condición de finalización, confianza y riesgos. Una lista de tareas
sin fechas no satisface el plan de entrega del starter actual.


10. Un ejemplo de primera campaña

El Planner parte del resultado final y selecciona la primera capacidad cerrable. El charter debe decir qué
capacidad agrega, por qué importa, qué interfaces y recursos afecta, qué límites no pueden romperse y
qué evidencia invalida o permite aceptar el resultado. No necesita enumerar cada archivo que Codex va a
editar ni decidir de antemano cuántos ciclos de prueba hacen falta.

Una primera campaña del club podría exigir crear, consultar, modificar y desactivar socios sin perder
historial, con una prueba física de persistencia y entradas inválidas. I3 recibe ese resultado esperado y el
repositorio actual; él resuelve implementación, pruebas, revisión, integración y recuperación. Si aparece
un cambio de objetivo —por ejemplo, pasar a varios clubes en Internet— debe volver a la autoridad de
producto y a planificación estratégica. Si solo falló una validación del formulario, permanece dentro del
mismo encargo.

Continuar con: Manual 03, operación diaria.

Referencias de esta edición
Fuente: repositorio público ArquitecturaRepo en el commit 9c00e19b74d1 . Rutas verificadas:

  • prompts/INSTALL_THIS_SDLC.md
  • prompts/PRODUCT_DISCOVERY_SESSION.md
  • prompts/FRESH_CONTEXT_PROBE.md
  • docs/07_FRESH_CONTEXT_TEST.md
  • docs/16_TRANSFER_ADOPTION.md
  • docs/21_PRODUCT_DISCOVERY_REQUIREMENTS_STACK_AND_DELIVERY.md
  • protocols/PLANNER_KERNEL.md
  • tools/baseline_guard.py

Las instrucciones de este volumen describen el starter y un procedimiento de uso. Ninguna prueba de los
ejemplos sustituye la verificación del proyecto de destino.
