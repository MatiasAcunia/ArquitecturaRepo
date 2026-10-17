# 04 — Solicitar cambios | ArquitecturaRepo v1.3.0

> Manual de uso revisado para el release público v1.3.0 (17 de octubre de 2026). Conserva el texto del manual original 00–07 de septiembre de 2026 y solo añade aclaraciones relacionadas con cambios reales en v1.3. Los pies de las figuras se conservan, pero esta transcripción Markdown no incluye las imágenes del PDF original.

## Actualización comprobada para v1.3.0

- El CLIENT especifica comportamiento observable, restricciones y prioridades. I2 transforma la necesidad en requisitos, plan de entrega, arquitectura y gates verificables.
- El Goal representa el resultado autorizado: `goal_id`, `campaign_id`, `charter_ref`, `authority_refs`, `definition_of_done`, `hard_gates`, `forbidden_effects` y `write_envelope`. No corresponde que I3 reescriba unilateralmente esas condiciones estratégicas.
- I3 sí puede revisar su plan, pasos, hipótesis y bloqueos dentro del charter. Una revisión táctica del plan no equivale a modificar el producto.
- Todo cambio del CLIENT que afecte a owners, fuentes, DB o garantías externas exige nueva confirmación y reconciliación con el estado actual; defectos ordinarios continúan en la misma campaña.

## Contenido del manual conservado

### Página 27 de la edición original

A R Q U I T E C T U RA R E P O / C O L E C C I Ó N D E U S O




04
Solicitar cambios

Precisar necesidades y preservar decisiones




Matías Acuña · ArquitecturaRepo                                Revisión de compatibilidad: 17 de octubre de 2026

### Página 28 de la edición original

Contenido

     • 1. Empezar por el resultado, no por el código                     • 7. Cuando el Planner necesita una decisión real
     • 2. Ficha breve para formular una necesidad                        • 8. Cinco ejemplos de requisitos bien formulados
     • 3. Cuáles son tus preguntas y cuáles no                           • 9. Cambios de producto frente a defectos de
     • 4. Cambiar de opinión sin destruir el estado                        implementación

     • 5. Pedir calidad sin pedir una tecnología específica              • 10. Qué decir cuando el resultado “funciona” pero
                                                                           no sirve
     • 6. Priorizar sin abrir diez objetivos simultáneos
                                                                         • 11. Guion corto para comunicar una prioridad




1. Empezar por el resultado, no por el código

El CLIENT describe quién usa la función, qué quiere hacer, qué resultado observa, cuándo puede fallar y
qué no debe perderse. El Planner traduce ese comportamiento en requisitos, dependencias, límites de
implementación y gates. Es legítimo tener preferencias técnicas; lo que no debería ocurrir es que el
sistema descargue sobre el CLIENT decisiones rutinarias que puede resolver desde evidencia técnica.




  Figura 7. Definición de cambios. Esquema explicativo; no acredita un proyecto de destino.



El pedido “agregá un botón de cancelar” es incompleto si cancelar modifica cupos, pagos o historia. La
pregunta adecuada es: “Al cancelar una inscripción, ¿el cupo vuelve a estar disponible? ¿Qué debe
conservarse en el historial?”. La diferencia no es retórica: determina qué se tiene que comprobar para
aceptar la función.


2. Ficha breve para formular una necesidad

Un pedido breve con información que sí altera la solución
En lugar de “haceme el módulo de socios”, indicá actor, acción, condición inicial, resultado visible y
límite. Por ejemplo: “Como administrativa del club, quiero desactivar una ficha sin borrar pagos
anteriores; al buscar socios activos no debe aparecer, pero debe seguir disponible en el historial”. El
Planner todavía tiene que aclarar si una ficha desactivada puede ser reactivada y qué datos se
consideran únicos.

No necesitás escoger una DB ni escribir tests. Una buena especificación de producto permite que
ingeniería proponga implementaciones distintas y que el CLIENT reconozca cuándo el resultado se parece
a lo que pidió. Un botón visible no prueba que la regla de negocio esté implementada.

### Página 29 de la edición original

Campo                                                  Ejemplo para la app del club

Persona usuaria                                        Personal administrativo del club.

Situación                                              Llega un socio que quiere inscribirse en una actividad.

Resultado visible                                      La inscripción se guarda si tiene cupo y cumple las reglas
                                                       vigentes.

Restricciones                                          Sin pagos online ni notificaciones automáticas en esta etapa.

Información que debe conservarse                       Identidad del socio, actividad, fecha y cambios posteriores.

Criterio de aceptación                                 Puedo inscribir, ver el cupo restante y cancelar sin perder
                                                       historial.



No hace falta completar un formulario de diez campos por cada cambio menor. Para una decisión
material, sí conviene que el Planner registre de manera durable el comportamiento vigente y cómo fue
confirmado.


3. Cuáles son tus preguntas y cuáles no

Una pregunta corresponde al CLIENT cuando cambia el producto: si una cuota vencida bloquea
inscripciones; si una persona puede recuperar un registro eliminado; si el sistema se usa solo en una PC;
si se permiten gastos o publicaciones. Una pregunta corresponde a ingeniería cuando trata de tablas SQL,
framework, ramas, tests, logs, retries o compatibilidad entre interfaces internas.

El Planner puede mostrar alternativas de producto con consecuencias legibles: “Con lista de espera, el
personal deberá confirmar un lugar cuando se libere; sin lista de espera, la inscripción se rechaza”. No
necesita convertir eso en una clase de arquitectura para obtener tu opinión.


4. Cambiar de opinión sin destruir el estado

Cuando un nuevo pedido contradice uno anterior
Escribí qué decisión cambia y desde cuándo se aplica. “Antes no permitíamos inscripción a socios con
cuota vencida; ahora permitimos la inscripción, pero marcamos deuda visible a la administrativa”. Esa
variación afecta reglas, UI, datos y tests. El Planner identifica impactos, persiste el nuevo requisito como
actual, marca el anterior como reemplazado y revisa trabajo en curso.

Un cambio legítimo de producto no convierte el historial previo en falso. Lo que sí sería incorrecto es
tener dos archivos CURRENT que exijan conductas incompatibles. La ruta técnica de migración y los
reintentos pertenecen al equipo; el CLIENT confirma el comportamiento nuevo.

Un requisito vigente puede ser reemplazado. La nueva decisión del CLIENT debe quedar registrada como
actual y la anterior como sustituida cuando corresponda. Luego el Planner identifica qué código, datos,
pruebas, interfaces o campañas quedan afectados. No basta con “acordarse” del último mensaje: un
ejecutor nuevo tiene que recuperar la decisión vigente desde las superficies del proyecto.


  Nueva decisión de producto: ya no quiero borrar definitivamente socios desde la interfaz. Quiero
  desactivarlos y conservar pagos e inscripciones. Tratá la regla anterior como sustituida, evaluá el
  impacto sobre datos existentes y explicame qué cambia para la persona usuaria.

### Página 30 de la edición original

Si el cambio modifica radicalmente el objetivo, el Planner puede invalidar el charter anterior y definir un
nuevo límite estratégico. Si se trata de un defecto dentro de lo ya acordado, el Campaign Lead repara el
mismo alcance y no abre una campaña nueva.


5. Pedir calidad sin pedir una tecnología específica

“Profesional” es una dirección, no una aceptación verificable. Señalá qué sería incómodo o incorrecto
para quien usa el sistema: no encontrar un socio, perder datos al actualizar, no saber si un pago se
guardó, campos con mensajes confusos, acciones destructivas sin confirmación. El Planner convierte esas
observaciones en un gate de uso real y en prioridades de diseño.

Ejemplo útil: “La pantalla de cuotas debe permitir ver estado, importe y fecha del último pago sin abrir
cinco ventanas. Si falla el guardado, no debe aparentar éxito. No quiero una interfaz visualmente
sofisticada; necesito que sea clara y consistente”.

Una captura real con una observación concreta puede valer más que un adjetivo. La opinión subjetiva del
CLIENT puede ser gate de aceptación cuando la funcionalidad depende de la experiencia de uso; un test
automático no debe sustituirla.


6. Priorizar sin abrir diez objetivos simultáneos

Una prioridad es una restricción sobre el trabajo actual. Para el club: primero identificar socios y
conservar sus cambios; luego cuotas; después actividades e inscripciones. Si una capacidad depende de
otra, el Planner lo registra. Si el proyecto cambia de prioridad, el Campaign Lead guarda checkpoint o
termina adecuadamente la frontera abierta antes de abandonar trabajo irreconstruible.

Frase vaga                                             Encargo útil

“Hacé todo el club”.                                   “Primero gestión de socios; cuotas después de que el flujo de
                                                       socios sea verificable”.

“Arreglá lo que haya”.                                 “Al cancelar una inscripción el cupo no se libera; corregilo sin
                                                       perder historial y comprobá el flujo”.

“Hacelo más moderno”.                                  “Puedo encontrar un socio y su deuda con menos pasos;
                                                       priorizá legibilidad sobre decoración”.




7. Cuando el Planner necesita una decisión real

Debería explicarte el problema en términos de uso, las consecuencias de las opciones, una
recomendación técnica cuando corresponda y cuál es la decisión reservada al CLIENT. No debería pedirte
que depures una migración ni que decidas un patrón de persistencia porque falló un test.

Para una consulta de estado pedí tres cosas: qué comportamiento existe y está comprobado; qué falta
para el objetivo activo; y si existe una decisión de producto indispensable que únicamente vos podés
tomar. La respuesta no debe convertir la cantidad de commits o la longitud del trabajo de Codex en una
medida de progreso.


8. Cinco ejemplos de requisitos bien formulados

Búsqueda. “Quiero encontrar un socio por nombre o número y distinguir los activos de los desactivados.
Si no hay coincidencias, la pantalla debe decirlo con claridad. No quiero que el buscador muestre datos

### Página 31 de la edición original

personales a usuarios no autorizados”. Esto define comportamiento y un riesgo real, sin elegir un motor
de búsqueda.

Edición. “Necesito corregir el teléfono de un socio. Antes de guardar debe quedar claro qué registro
estoy editando. Si el dato es inválido, quiero conservar el resto del formulario y recibir una explicación
concreta”. Esto permite diseñar pruebas de navegación y validación, no solo probar un endpoint.

Desactivación. “Al desactivar un socio deja de aparecer en la lista de activos, pero su historial de pagos
se conserva y una persona autorizada puede consultarlo”. La palabra desactivar deja de ser ambigua; si
el proyecto requiere eliminación legal posterior, es una regla distinta.

Rendimiento. “La búsqueda debe seguir siendo utilizable con el volumen de socios que esperamos
durante el primer año; si el Planner necesita una cifra para dimensionarla, me la pregunta”. No hace falta
imponer una tecnología antes de conocer los datos.

Nueva funcionalidad. “Quiero agregar inscripciones cuando socios y cuotas ya sean utilizables. Primero
acordemos reglas de cupo, cancelación, vencimientos y permisos; después planifiquemos su integración”.
Evita iniciar trabajo que dependa de capacidades todavía no comprobadas.


9. Cambios de producto frente a defectos de implementación

Si la app permite inscribirse pese a una cuota vencida y el requisito vigente lo prohíbe, la implementación
incumple una regla actual: se corrige en la campaña correspondiente. Si el requisito nunca definió cómo
tratar pagos parciales, el Planner necesita una decisión de producto antes de inventar el resultado. Si
ahora querés permitir que un familiar pague una cuota por otro socio, hay una regla nueva: se registra,
se evalúan interfaces y se modifica el alcance de forma explícita.

La diferencia importa porque el equipo no debería pedirte autorización para cada bug, pero tampoco
debería transformar una preferencia tuya en una inferencia técnica. Las decisiones materiales actualizan
los requisitos actuales y dejan constancia de lo anterior; no basta con una conversación que otro agente
quizá no pueda leer.


10. Qué decir cuando el resultado “funciona” pero no sirve

Podés pedir cambios de calidad del producto sin prescribir cómo lograrlos. Por ejemplo: “El formulario
guarda bien, pero desde el celular no puedo ver el botón de confirmar; no acepto esta capacidad hasta
que el recorrido completo se pueda usar en esa pantalla”. Es un hallazgo perceptual: adjuntá captura o
describí el dispositivo/estado y el resultado esperado.

Si el interfaz fue acordado solo para escritorio, cambiar el objetivo a uso móvil no es necesariamente un
bug ordinario. El Planner debe explicitar la diferencia, decidir si invalida el charter y ajustar fechas si
corresponde. Cuando el defecto sí está dentro del alcance, I3 repara el candidato y renueva la evidencia
pertinente.


11. Guion corto para comunicar una prioridad

  Mi prioridad actual es [resultado visible]. La persona usuaria es [quién]. Debe poder [recorrido
  observable] y no debe [límite importante]. Tengo una fecha objetivo de [fecha] y un costo máximo
  de [presupuesto si existe]. Antes de programar, confirmame qué decisiones de producto faltan y qué
  capacidades actuales dependen de este cambio. Lo técnico, las pruebas y la integración quedan a
  cargo del sistema.

### Página 32 de la edición original

No necesitás usar este texto literalmente. Lo importante es que se pueda reconstruir tu intención y que el
sistema la traduzca a requisitos verificables, sin convertir una sugerencia casual en una obligación
irreversible.

Continuar con: Manual 05 ante errores o autorizaciones sensibles; Manual 06 para cerrar el ciclo.

Referencias de esta edición
Fuente: repositorio público MatiasAcunia/ArquitecturaRepo en el commit 56f04267b6a9 . Rutas verificadas:

  • protocols/CLIENT_BOUNDARY.md
  • protocols/INTERACTION_LEDGER.md
  • prompts/PRODUCT_DISCOVERY_SESSION.md
  • protocols/PRODUCT_DISCOVERY_REQUIREMENTS_AND_TECHNICAL_BASELINE.md

Las instrucciones de este volumen describen el starter y un procedimiento de uso. Ninguna prueba de los
ejemplos sustituye la verificación del proyecto de destino.
