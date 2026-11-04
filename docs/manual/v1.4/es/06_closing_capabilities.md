# 06 — Cierre de capacidades y aceptación

ArquitecturaRepo · Manual completo de uso · Edición v1.4 · Español

> Una capacidad se cierra contra un **candidato exacto y evidencia aplicable**, no contra el entusiasmo de un reporte. Un terminal de I3 habilita la revisión estratégica; no aprueba automáticamente el producto, no sustituye una revisión humana y no concede permiso para desplegar o publicar. Este capítulo separa esas decisiones y explica cómo devolver defectos a la misma campaña sin reiniciar la arquitectura.

## Contenido del capítulo

1. Una capacidad es un resultado de producto
2. Los cinco componentes del cierre
3. El candidato exacto como unidad de revisión
4. Evidencia insuficiente sin campañas artificiales
5. Aceptar, recuperar o cambiar el objetivo
6. Revisiones periódicas y regla de detención
7. Registro de cierre reconstruible
8. Ejemplo de rechazo y corrección
9. Producto utilizable frente a framework verde
10. Qué hacer después del cierre

## 1. Una capacidad es un resultado de producto

«Gestión de socios» no está terminada cuando aparece un formulario bonito ni cuando un agente hace un commit. Está terminada cuando la persona prevista puede realizar la tarea acordada en el entorno pertinente, los datos relevantes permanecen como corresponde, los controles aplicables pasan, el estado vigente y su lineage son coherentes y las autoridades competentes aceptaron el resultado.

El Planner delimita la capacidad y autoriza un charter de ingeniería. I3 integra un candidato concreto, realiza las pruebas, organiza la revisión independiente cuando corresponda y presenta un terminal respaldado por evidencia. El Planner audita ese terminal contra los requisitos vigentes y la aceptación pactada. El CLIENT conserva las decisiones de producto, preferencias perceptuales y autorización de efectos externos que le correspondan.

Una campaña no dura obligatoriamente una conversación, un sprint, un número fijo de prompts ni una sesión de Codex. Puede sobrevivir desconexiones, límites de servicio, reintentos y checkpoints. Esos hechos no crean una autorización nueva ni permiten olvidar pruebas anteriores; tampoco convierten la campaña en un éxito por el solo hecho de haber trabajado muchas horas.

La distinción es especialmente importante para productos con interfaz. Un screenshot muestra un estado visual; no demuestra por sí mismo que el botón guarde datos, que un usuario tenga los permisos correctos o que pueda recuperar lo guardado después de reiniciar. La aceptación del producto necesita observaciones relacionadas con el comportamiento real.

## 2. Los cinco componentes del cierre

| Componente | Pregunta que debe responderse |
| --- | --- |
| Resultado visible | ¿La persona prevista puede completar la tarea en el entorno relevante? |
| Verificaciones aplicables | ¿Se ejecutaron los controles de lógica, integración, DB, seguridad, runtime y experiencia que efectivamente corresponden? |
| Estado actual coherente | ¿Se conoce la identidad exacta de código, configuración, requisitos y datos o artefactos afectados? |
| Sin bloqueos materiales ocultos | ¿Existe algún defecto abierto que invalide lo que se afirma haber entregado? |
| Aceptación competente | ¿Revisaron las autoridades pertinentes evidencia real, en vez de aceptar un `DONE` genérico? |

No todas las capacidades requieren todos los ensayos posibles. Un pequeño script interno puede no necesitar una evaluación perceptual compleja. Un sistema que registra cuotas sí tiene que demostrar persistencia y permitir seguir correctamente el recorrido de la persona que lo opera. Lo que no puede pasar es que un gate reemplace silenciosamente a otro: validar la forma de un JSON no equivale a probar el CRUD; una prueba unitaria no demuestra que una pantalla cargue en el navegador.

En ArquitecturaRepo conviene distinguir los siguientes gates:

- **Unit:** la lógica aislada se comporta correctamente con entradas controladas y casos negativos.
- **Integration:** los componentes que se comunican cumplen interfaces y contratos reales.
- **DB/currentness:** registros, migraciones, relaciones, snapshots y testigos del estado actual son coherentes y suficientemente durables.
- **Semantic/generalization:** el comportamiento responde a la regla de negocio, incluso más allá de una fixture estrecha.
- **Physical:** el ejecutable, aplicación, artefacto o recorrido funciona realmente donde se pretende utilizar.
- **Perceptual/human:** una persona calificada evalúa experiencia, legibilidad o criterios subjetivos aplicables.
- **Release:** el paquete exacto, permisos, derechos, firmas o checksums y condiciones de distribución están verificados.

La cantidad y profundidad de pruebas debe ser proporcional al impacto. Pedir docenas de controles sin capacidad de descubrir defectos materiales puede demorar el producto; omitir los que importan genera aceptación falsa. Un gate útil tiene owner, criterio, candidato y evidencia. Si no se puede explicar qué riesgo reduce, vale la pena revisar si corresponde.

## 3. El candidato exacto como unidad de revisión

El revisor independiente tiene que inspeccionar el mismo candidato que luego se propone aceptar. Según el producto, su identidad abarca hash o ref de fuente, configuración, versión del esquema, estado de la DB, manifiesto de archivos, assets y entorno de ejecución. Una revisión favorable de un archivo con nombre `final` no puede transferirse automáticamente a otro archivo con el mismo nombre y contenido cambiado.

El flujo razonable es integrar el candidato, congelar su identidad relevante, ejecutar las pruebas físicas y la revisión independiente, y recién después presentarlo al Planner. Si se modifica materialmente después de la revisión, hay que renovar los controles afectados. No es necesario repetir toda evidencia estable cuyos inputs no cambiaron, pero sí impedir que una revisión antigua parezca avalar bytes nuevos.

El [protocolo de freeze y terminal](../../../../protocols/REVIEW_FREEZE_AND_TERMINAL_INTEGRITY.md) describe esa relación. El controlador de referencia puede representar transiciones de freeze, review y terminal, pero no puede fingir que un tercero aceptó un diseño ni certificar una aplicación externa que no ejecutó físicamente.

El gate técnico puede quedar aprobado y continuar pendientes una prueba con usuarios, una revisión de datos personales, un permiso de publicación, una licencia de un recurso ajeno o una aceptación final del CLIENT. Registrá cada una por separado. Un terminal estratégico significa «hay evidencia para decidir lo próximo», no «todos los efectos posteriores están autorizados».

Es útil que cada informe cite el commit, manifest y environment que realmente observó. Si la rama avanzó después, el nombre de la rama no prueba por sí solo currentness. El salto entre código, base de datos, artefactos y revisión debe ser rastreable de manera mecánica o con referencias precisas.

## 4. Evidencia insuficiente sin campañas artificiales

Si falta evidencia de algo ya incluido en el charter, el Planner devuelve a I3 una lista **consolidada de falsifiers**: qué se esperaba, qué ocurrió, qué candidato y evidencia lo demuestra y qué gate está afectado. I3 investiga, arregla, integra, vuelve a probar y obtiene la revisión necesaria en la **misma campaña**.

No corresponde abrir una nueva campaña porque falló un test unitario, porque el backend devuelve un error previsto, porque el reviewer detectó una regresión o porque una herramienta se desconectó. Tampoco corresponde crear PASS4, PASS5 y PASS6 para que el Planner vaya minando bugs que el Controller tiene autoridad y responsabilidad de resolver.

Cuando la misma clase de defecto reaparece en dos o más terminales, I3 debe dejar de aplicar arreglos estrechos y endurecer el subsistema de forma exhaustiva, con revisión independiente. El retorno siguiente debe demostrar que se corrigió la causa sistémica, no que se ocultó otra manifestación. Esto es disciplina de ingeniería dentro del charter autorizado.

La situación cambia cuando aparece una regla de negocio material no decidida, cambian los permisos del CLIENT o se descubre una incompatibilidad estratégica que invalida el charter. Ahí el Planner vuelve a evaluar el objetivo, los límites y las dependencias. El criterio no es cuán difícil se volvió el bug, sino si el trabajo sigue autorizado y responde al mismo objetivo.

Un terminal legible se puede expresar así: candidato y entorno exactos; recorrido real realizado; gates aprobados con enlaces; gates abiertos con impacto concreto; riesgos nuevos; decisión pendiente; ruta siguiente y owner. Ese resumen sirve para encontrar evidencia canónica, no para instalar un segundo Product State paralelo.

## 5. Aceptar, recuperar o cambiar el objetivo

**Aceptar.** Cuando el Planner tiene los datos apropiados, registra la capacidad aceptada y actualiza las superficies canónicas y punteros `CURRENT` que correspondan. El CLIENT ejerce su aceptación reservada cuando hay calidad perceptual, comportamiento de producto o efectos externos. Solo entonces pueden depender de esa capacidad los trabajos posteriores que la necesiten.

**Recuperar después de una interrupción.** Si cambia el ejecutor o termina la sesión, el nuevo actor reconstruye campaña, checkpoint, candidato, owner y evidencia desde el repositorio y estado autorizado. No marca la capacidad terminada porque venció el tiempo de servicio. Tampoco crea una versión competidora del charter para continuar más rápido. La continuidad no requiere memoria perfecta del chat, pero sí un estado durable coherente.

**Cambiar prioridades.** Posponer un módulo puede ser un ajuste de cronograma; cambiar la condición de elegibilidad de un socio es una nueva regla de negocio. En el segundo caso se registran la decisión, el impacto y las supersesiones. Dos charters contradictorios no deben permanecer activos sobre el mismo concern. El trabajo anterior válido se conserva cuando todavía tiene valor y puede ser referenciado.

**Detener por incertidumbre.** Si no hay forma de relacionar un candidato con el estado actual de la DB o las fuentes, se deja HOLD para la aceptación dependiente. La investigación segura puede continuar. HOLD no equivale a «todo el proyecto está roto» ni autoriza a inventar una respuesta para destrabar la conversación.

## 6. Revisiones periódicas y regla de detención

Una revisión semanal debería permitirle al CLIENT preguntar: ¿qué capacidades están aceptadas?, ¿qué puedo demostrar hoy?, ¿qué falta para llegar a la próxima entrega?, ¿cuál es el riesgo de plazo?, ¿qué decisión real necesita mi intervención?, ¿el gasto y el alcance siguen justificados? El informe debe apoyarse en evidencia observable.

La actividad técnica es un medio: commits, agentes, documentos, tests, minutos de runtime y tokens no son el valor entregado. A veces un buen resultado requiere pocos cambios y pruebas bien elegidas; otras veces necesita mucha recuperación interna. Contar operaciones no permite comparar esas situaciones ni aceptar por cantidad.

El framework tiene también una regla de detención. Una vez logrados los gates de release, no agregues maquinaria genérica, políticas duplicadas o más jerarquía solo porque se puede. Un mecanismo nuevo necesita abordar una clase de falla identificada o desbloquear una capacidad. La misma regla opera dentro de la aplicación: perseguir indefinidamente microdefectos sin relevancia estratégica consume tiempo y puede deteriorar el resultado.

El equilibrio es concreto: no aceptar prematuramente una app rota, pero tampoco mantener una capacidad en limbo porque no existe un test imposible que nadie había requerido. El Planner y el CLIENT deben ver qué riesgos son materiales y qué evidencias les permiten decidir con honestidad.

## 7. Registro de cierre reconstruible

Una persona que no participó en la implementación tiene que encontrar lo necesario sin leer todo el historial de conversación. La ficha de cierre apunta a las superficies existentes y debería contener:

| Campo | Evidencia rastreable |
| --- | --- |
| Candidato | Código, configuración, artifact y state exactos revisados. |
| Resultado | Entrada, acción y salida observada en recorrido end-to-end. |
| Pruebas | Resultados, comandos relevantes y entorno donde corrieron. |
| Datos persistentes | Readback, reinicio y recuperación cuando son aplicables. |
| Seguridad y derechos | Controles proporcionados a datos sensibles, licencias y exposición. |
| Revisión independiente | Identidad del reviewer, alcance y candidato efectivamente inspeccionado. |
| Cambios posteriores | Qué cambió después del freeze y qué gates se renovaron. |
| Aceptación humana | Decisión auténtica, no inferida a partir de un screenshot. |
| Ruta siguiente | Accept, retorno a I3, pregunta al CLIENT o HOLD con causa. |

No copies cada campo a otro archivo `CURRENT` creado para una presentación. El registro funciona como índice de evidencia, con owners únicos y referencias que realmente resuelven. Si el enlace apunta a un artifact inexistente, a una versión anterior o a una fixture que nunca ejercitó el producto, el cierre no está debidamente sustentado.

Las familias de pruebas del propio starter también deben mantenerse separadas: corrección interna de código, contratos y transacciones por un lado; ciclo completo de instalación y recuperación en un destino portátil real por otro. Ninguna de ellas certifica por defecto la experiencia de usuario ni la lógica comercial de otra aplicación construida con el framework.

## 8. Ejemplo de rechazo y corrección

Supongamos que una aplicación de club ya permite registrar y desactivar socios. El reviewer encuentra que al desactivar un socio se borran sus pagos históricos, pese a que el charter exigía preservarlos. Eso es un defecto de implementación dentro del alcance ya autorizado. El Planner devuelve un falsifier concreto: «Desactivar un socio con pagos previos debe conservar transacciones después de un reinicio; en el candidato X desaparecen».

I3 inspecciona relaciones y operaciones de persistencia, corrige la causa, agrega una regresión significativa, prueba el registro después de reiniciar, integra un nuevo candidato y solicita revisión independiente. No abre una campaña «arreglar botón de desactivar». Tampoco le exige al CLIENT decidir cómo implementar una foreign key; esa es una responsabilidad técnica.

Si el reviewer revisó A y el cambio de persistencia generó B, el PASS de A no acepta B. Podrán aprovecharse pruebas que dependían de componentes intactos, pero debe renovarse la evidencia afectada por el cambio y la revisión sobre el nuevo candidato. El objetivo es evitar tanto repetición inútil como reutilización engañosa.

Ahora imaginá que el CLIENT pregunta por una función de reactivación con permisos especiales. No es la reparación del borrado de pagos: introduce comportamiento nuevo. El Planner confirma quién puede reactivar, qué pasa con el identificador anterior, cuáles son las reglas sobre pagos y si el charter actual permite esa ampliación. Una regla nueva y un fallo de una regla existente son hechos distintos.

## 9. Producto utilizable frente a framework verde

Una campaña puede superar validaciones de gobierno y poner el controlador de referencia en estado terminal sin que exista una pantalla usable. Para aceptar la aplicación del club, hay que abrirla, registrar un socio ficticio, encontrarlo, modificarlo, desactivarlo y verificar que su historial permitido permanece. Si la persistencia importa, reiniciá el programa y comprobá el readback real. Si hay permisos, también intentá la ruta que debe ser denegada.

El release gate de ArquitecturaRepo es diferente: `tools/verify_v1_release.py` comprueba una versión concreta del framework reutilizable mediante ejecución y fixtures sintéticas. Verificación de fuentes, instalación portátil Linux/Windows y lectura de artefactos de release son controles distintos. El hecho de que el framework haya pasado no demuestra que cada proyecto que lo adopte opere correctamente ni que una integración nativa de un host tercero esté probada.

La [matriz pública de soporte v1.4](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md) distingue exactamente lo ejercitado de lo que queda fuera de la prueba portátil. Evitá frases como «todo pasó» sin especificar candidato, escenario, entorno y gate. Un PASS limitado puede ser un progreso real; exagerarlo lo convierte en una fuente de error de producto.

## 10. Qué hacer después del cierre

Tras la aceptación estratégica, persistí los cambios en Product State y referencias actuales, y desbloqueá únicamente los downstream que dependen de lo demostrado. Ante un rechazo in-charter, devolvé a I3 la reparación consolidada. Ante una invalidación material, revisá el límite con el owner estratégico. Ante currentness no verificable, declarás HOLD concreto y seguís con las verificaciones seguras posibles.

El CLIENT debería poder terminar el día sabiendo qué existe realmente, qué no está listo, quién lo está resolviendo y cuándo se revisará el siguiente objetivo. Si esa información solo se puede reconstruir abriendo el chat de ayer, la arquitectura aún no cumplió su promesa de continuidad.

En cada cierre conviene preguntarse si la evidencia sería convincente para una persona escéptica que no participó del desarrollo. No hace falta escribir un tratado por feature: hacen falta IDs correctos, pruebas apropiadas, resultados observados y una ruta siguiente clara. Esa austeridad documental protege la velocidad y la confianza al mismo tiempo.

**Siguiente:** capítulo 07, ejemplo completo de una aplicación para un club.

## Fuentes y vigencia

- [Integridad de revisión, freeze y terminal](../../../../protocols/REVIEW_FREEZE_AND_TERMINAL_INTEGRITY.md)
- [Ciclo de capacidades y evidencia](../../../../protocols/CAPABILITY_LIFECYCLE_AND_EVIDENCE.md)
- [Validación ejecutable](../../../10_EXECUTABLE_VALIDATION.md)
- [Gates de release del framework](../../../17_V1_RELEASE_GATES.md)
- [Soporte y distribución v1.4](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md)
- [Verificador de release](../../../../tools/verify_v1_release.py)

La aceptación siempre depende del candidato y producto reales. Los ejemplos no reemplazan pruebas ni conceden autoridad a quien no la tiene.
