# 04 — Solicitar cambios

ArquitecturaRepo · Manual completo de uso · Edición v1.4 · Español

> Las decisiones de producto pertenecen al CLIENT. El Planner las traduce a requisitos confirmados, límites técnicos, hitos y gates verificables. I3 puede modificar su plan táctico dentro de un charter autorizado, pero no reescribir por su cuenta el Goal estratégico, los efectos prohibidos ni la definición del producto.

## Contenido del capítulo

1. Empezar por el resultado, no por el código
2. Una ficha breve para formular la necesidad
3. Cuáles son tus preguntas y cuáles no
4. Cambiar de opinión sin destruir el historial
5. Pedir calidad sin imponer una tecnología
6. Priorizar en vez de abrir diez Goals
7. Cuando el Planner necesita una decisión real
8. Cinco requisitos bien formulados
9. Cambio de producto frente a defecto de implementación
10. Qué decir cuando «funciona» pero no sirve
11. Guion corto para comunicar una prioridad

## 1. Empezar por el resultado, no por el código

El CLIENT describe quién usa una función, qué quiere hacer, cuál es el resultado observable, qué condiciones deberían impedirla y qué información debe conservarse. El Planner convierte esa intención en requisitos confirmados, dependencias, límites de implementación y condiciones de aceptación. Podés tener preferencias técnicas, pero las decisiones rutinarias de APIs, tablas, tests y estructura de código deben resolverlas los responsables de ingeniería.

«Agregá un botón para cancelar» puede ser insuficiente. Si la cancelación modifica cupos, pagos, permisos o historial, dibujar el botón no alcanza. La pregunta útil es: «Cuando se cancela una inscripción, ¿el lugar vuelve a quedar disponible? ¿Qué queda guardado en el historial?». La respuesta determina qué comportamiento hay que implementar y demostrar.

Separar problema y solución permite explorar alternativas. Un Planner puede proponer un botón, una acción contextual o una pantalla distinta; lo fundamental es que respeten la regla de cancelación confirmada. Una maqueta visual ayuda a conversar sobre interfaz, pero no demuestra que el estado de la aplicación ni los errores estén resueltos.

## 2. Una ficha breve para formular la necesidad

No hace falta escribir una especificación extensa para cada cambio. Cuando importa la conducta del producto, describí actor, situación inicial, acción, resultado visible, exclusiones y datos que sobreviven. Por ejemplo:

> Como administrativa del club, quiero desactivar un socio sin borrar sus pagos anteriores. No debe aparecer en la búsqueda de activos, pero una persona autorizada debe poder consultar sus registros históricos.

El Planner todavía tiene que aclarar si una ficha puede reactivarse, qué identificadores son únicos y qué datos están sujetos a retención. El CLIENT no necesita diseñar el esquema SQL ni escribir tests para pedir ese comportamiento.

Una ficha concreta de inscripción podría ser:

| Campo | Ejemplo |
| --- | --- |
| Persona usuaria | Personal administrativo del club. |
| Situación | Llega un socio que quiere participar en una actividad. |
| Resultado | La inscripción se guarda solo si hay cupo y se cumplen las reglas actuales. |
| Exclusiones | Sin pagos online ni avisos automáticos en esta etapa. |
| Información que permanece | Identidad, actividad, fecha, estado y modificaciones posteriores. |
| Aceptación | Puedo inscribir, ver cupos restantes y cancelar sin perder historial. |

No conviertas la ficha en una burocracia de diez campos para arreglar un detalle menor. Su función es eliminar ambigüedad material. Las decisiones de producto que cambian requisitos vigentes deben persistirse; un mensaje en un chat no basta como estado recuperable.

## 3. Cuáles son tus preguntas y cuáles no

Una pregunta es del CLIENT si modifica el comportamiento o el riesgo de negocio: si una deuda bloquea inscripciones, si una ficha puede recuperarse, si el programa debe funcionar sin Internet, si se autoriza gastar, publicar o enviar mensajes. Son decisiones sobre personas y uso previsto.

La estructura de tablas, el framework de pruebas, las ramas, los logs, los algoritmos de reintento y las migraciones pertenecen a ingeniería. El Planner puede explicar consecuencias cuando una elección técnica afecta costo, privacidad, compatibilidad o la experiencia, pero no debería pedirle al CLIENT que resuelva un error de SQL porque el ejecutor no pudo depurarlo.

Cuando hay opciones legítimas de producto, presentalas con efectos comprensibles: «Con lista de espera, el personal tiene que confirmar el ingreso cuando se libera un lugar; sin lista de espera, el sistema rechaza la inscripción inmediatamente». Indicá el impacto y recomendá si hay evidencia suficiente. No es necesario dar una clase de arquitectura para obtener una respuesta.

## 4. Cambiar de opinión sin destruir el historial

Los requisitos pueden cambiar. Hay que registrar **cuál** decisión cambia, **por cuál** se sustituye y **desde cuándo**. Por ejemplo:

> Antes no se permitía inscribir socios con cuotas vencidas. Ahora se permite, pero la deuda debe aparecer claramente en la vista administrativa. Registrá la regla anterior como sustituida y evaluá el impacto en código, datos, pantallas y pruebas.

La nueva regla puede afectar validaciones, persistencia, UI, pruebas y campañas activas. El Planner rastrea esas relaciones y actualiza el requisito canónico vigente. Que una decisión anterior haya sido válida no significa que deba seguir activa para siempre. Lo incorrecto sería conservar dos archivos `CURRENT` que exijan comportamientos opuestos sin una supersesión explícita.

Otro cambio posible:

> Ya no quiero eliminar definitivamente fichas de socios desde la interfaz. Quiero desactivarlas y conservar pagos e inscripciones. Tratá la política anterior como reemplazada, comprobá qué sucede con datos existentes y explicame el nuevo recorrido de usuario.

El equipo técnico diseña migración, recuperación, tests e interfaces. El CLIENT confirma el nuevo comportamiento y los permisos reservados. La siguiente sesión tiene que encontrar la decisión actual en las superficies del repositorio, sin depender de que alguien recuerde el último mensaje.

Si el pedido transforma completamente el producto —por ejemplo, de una aplicación interna de un club a un servicio público para cientos de clubes— puede requerirse invalidación o rediseño del charter estratégico. Si simplemente se detectó que un campo no valida como exige el requisito vigente, I3 corrige en la misma campaña.

## 5. Pedir calidad sin imponer una tecnología

«Que quede profesional» orienta, pero no basta como criterio de aceptación. Contá qué sería incorrecto o molesto para una persona: no encontrar una ficha, perder datos al corregir un error, no saber si el pago quedó guardado, recibir mensajes incomprensibles o activar una acción irreversible sin confirmación.

Un pedido útil es:

> La pantalla de cuotas debe mostrar estado, importe y fecha del último pago sin abrir varias ventanas. Si el guardado falla, no debe parecer exitoso. Prefiero claridad y consistencia antes que una decoración sofisticada.

Esto permite plantear pruebas de integración y condiciones de uso sin elegir un framework visual. Una captura real con una crítica específica suele ser más útil que diez adjetivos. Cuando la calidad depende de la experiencia, la evaluación del CLIENT puede ser un gate perceptual genuino; una prueba unitaria o una puntuación automática no deberían suplantar esa decisión.

También importa el comportamiento negativo. Una pantalla puede guardar un pago en el caso ideal y duplicarlo después de dos clics; puede aceptar datos válidos pero perder el resto del formulario al mostrar un error. El Planner vincula los riesgos con gates pertinentes; I3 define cómo implementar y comprobar las correcciones.

## 6. Priorizar en vez de abrir diez Goals

La prioridad señala cuál es la próxima capacidad que debe volverse utilizable respetando dependencias y recursos. En el club, una secuencia razonable sería: socios confiables, luego cuotas y después actividades e inscripciones. Si el tercer paso necesita datos del primero y del segundo, el Planner registra la relación. No hay beneficio en autorizar diez capacidades a la vez solo porque un asistente pueda generar diez planes.

| Frase vaga | Pedido útil |
| --- | --- |
| «Hacé todo el sistema del club». | «Primero dejá verificable la gestión de socios; después integrá cuotas». |
| «Arreglá lo que haya». | «Al cancelar una inscripción no se libera el cupo; corregilo sin borrar historial y demostrámelo». |
| «Hacelo más moderno». | «Reducí los pasos para encontrar un socio y revisar su deuda; priorizá legibilidad». |
| «Agregá todo lo que alguien podría necesitar». | «Validemos primero el recorrido administrativo principal antes de ampliar alcance». |

Si la prioridad cambia durante la ejecución, el sistema debería cerrar correctamente la frontera abierta o dejar un checkpoint recuperable. Un cambio repentino no autoriza a borrar trabajo sin integrar, reemplazar silenciosamente un Goal ni perder el estado de campaña. El Planner considera dependencias, interferencia y camino crítico.

## 7. Cuando el Planner necesita una decisión real

La pregunta debería describir el problema en lenguaje de uso, alternativas viables, efectos sobre costo o riesgo y cuál es exactamente la elección reservada al CLIENT. «¿El personal puede reactivar una inscripción cancelada?» es útil. «¿Qué índice SQL agrego para la migración?» normalmente no lo es.

Ante una consulta de estado, pedí tres datos: qué comportamiento existe y se comprobó; qué falta para el objetivo activo; y si hay alguna decisión de producto que solo vos podés resolver. Una respuesta que enumera commits, horas, tokens y nombres de agentes sin explicar qué puede hacer el usuario no es una evaluación honesta del avance.

Si aún no tenés una respuesta para una decisión material, señalala como abierta. El equipo puede continuar el trabajo seguro que no dependa de ella. La ingeniería no debe convertir una preferencia no confirmada en un requisito autorizado.

## 8. Cinco requisitos bien formulados

### Búsqueda

> Quiero encontrar socios por nombre o número y distinguir activos de desactivados. Si no hay coincidencias, mostrámelo con claridad. No quiero exponer datos personales a usuarios no autorizados.

Define comportamiento, estado vacío y privacidad sin imponer un motor de búsqueda. Permite comprobar consultas autorizadas y denegadas.

### Edición

> Necesito corregir el teléfono de un socio. Antes de guardar debe quedar claro qué ficha estoy editando. Si ingreso un dato inválido, conservá los otros campos y explicá el error.

Describe navegación, retención del formulario y feedback; probar solo el endpoint no demuestra la interacción completa.

### Desactivación

> Desactivar una ficha la excluye de la lista de activos, conserva los pagos y permite que personal autorizado consulte el historial.

La palabra desactivar tiene un significado comprobable. Una exigencia posterior de eliminación legal se trataría como una regla distinta.

### Rendimiento

> La búsqueda debe seguir siendo utilizable con la cantidad de socios que esperamos durante el primer año. Si necesitás una estimación para dimensionarla, preguntámela.

Vincula rendimiento con uso real sin imponer prematuramente caching o una base de datos.

### Nueva capacidad

> Agregá inscripciones después de que socios y cuotas sean utilizables. Primero acordemos cupos, cancelaciones, vencimientos y permisos; después planificá la integración.

Evita construir un componente que depende de capacidades incompletas o reglas contradictorias.

## 9. Cambio de producto frente a defecto de implementación

Si el requisito vigente prohíbe inscripciones a socios morosos y el programa las permite, la implementación incumple una regla: I3 la corrige dentro del alcance autorizado. Si nunca se decidió cómo tratar pagos parciales, el Planner consulta antes de inventar la conducta. Si ahora se quiere que un familiar pueda pagar la cuota de otra persona, aparece una regla nueva que puede afectar identidad, permisos e historial.

La diferencia es importante: ingeniería no debería exigir autorización por cada bug, pero tampoco apropiarse de una preferencia nueva. Las decisiones materiales cambian requisitos actuales con trazabilidad, de forma que el próximo agente pueda recuperar la regla válida.

Una revisión del plan táctico no equivale automáticamente a un cambio de producto. El Goal estratégico puede tener `goal_id`, `campaign_id`, `charter_ref`, `authority_refs`, `definition_of_done`, `hard_gates`, `forbidden_effects` y `write_envelope`. I3 puede corregir pasos, hipótesis y tests dentro de ese contrato. No puede convertir unilateralmente un gasto o efecto prohibido en algo autorizado.

## 10. Qué decir cuando «funciona» pero no sirve

Podés rechazar una capacidad por un recorrido de usuario inutilizable aunque el guardado técnico funcione. Por ejemplo:

> El formulario guarda los datos, pero en el celular el botón de confirmar queda fuera de pantalla. No acepto el recorrido hasta que pueda completarse desde ese dispositivo.

Una captura o una descripción precisa del dispositivo, estado y resultado esperado sirve como evidencia perceptual. Si el uso móvil estaba expresamente excluido del alcance, incorporarlo puede ser un cambio de producto, no un bug ordinario. El Planner debe aclarar esa frontera y revisar fechas cuando corresponda. Si la compatibilidad móvil ya era un requisito, I3 repara y renueva la evidencia pertinente dentro de la misma campaña.

La valoración positiva del CLIENT tampoco reemplaza los tests técnicos. Una interfaz agradable puede conservar mal los datos o fallar en permisos. Una capacidad aceptable satisface los gates que su riesgo exige, cada uno con su evidencia y autoridad.

## 11. Guion corto para comunicar una prioridad

Podés decirle al Planner:

> Mi prioridad actual es [resultado visible]. La persona usuaria es [quién]. Debe poder [recorrido comprobable] y no debe [restricción principal]. La fecha objetivo es [fecha] y el costo máximo es [presupuesto, si existe]. Antes de programar, decime qué decisiones de producto siguen abiertas y qué capacidades vigentes dependen de este cambio. La tecnología, las pruebas, la integración y la recuperación dentro del alcance quedan a cargo de ingeniería.

No es necesario copiar el texto literalmente. Lo importante es que tu intención quede reconstruible y verificable sin transformar cada sugerencia casual en un compromiso irreversible. Un buen Planner sabe cuándo preguntar, cuándo leer evidencia física y cuándo dejar ejecutar a I3.

**Siguiente:** capítulo 05 para errores y permisos sensibles; capítulo 06 para aceptación de capacidades.

## Fuentes y vigencia

- [Fronteras de decisión del CLIENT](../../../../protocols/CLIENT_BOUNDARY.md)
- [Registro de interacciones y decisiones](../../../../protocols/INTERACTION_LEDGER.md)
- [Prompt de discovery](../../../../prompts/PRODUCT_DISCOVERY_SESSION.md)
- [Requisitos y baseline técnico](../../../../protocols/PRODUCT_DISCOVERY_REQUIREMENTS_AND_TECHNICAL_BASELINE.md)
- [Ciclo de vida y evidencia](../../../../protocols/CAPABILITY_LIFECYCLE_AND_EVIDENCE.md)

Los ejemplos son requisitos ilustrativos. No constituyen una decisión real del CLIENT sobre una aplicación concreta.
