# 06 — Cierre de capacidades | ArquitecturaRepo v1.3.0

> Manual de uso revisado para el release público v1.3.0 (17 de octubre de 2026). Conserva el texto del manual original 00–07 de septiembre de 2026 y solo añade aclaraciones relacionadas con cambios reales en v1.3. Los pies de las figuras se conservan, pero esta transcripción Markdown no incluye las imágenes del PDF original.

## Actualización comprobada para v1.3.0

- La aceptación del framework distingue dos familias de evidencia: A, corrección interna de código/contratos/transacciones; B, ciclo completo del framework realmente instalado. Ninguna equivale a aceptación de UX/negocio del producto construido con agentes.
- `verify_v1_release.py`, tests de control y `selftest_v13_installed_lifecycle.py` evalúan la distribución. Los adaptadores externos requieren además un ejercicio nativo comprobado.
- Una evidencia de revisión debe corresponder al mismo candidato y SHA actuales; cambios posteriores pueden invalidar la revisión favorable.
- Un terminal de I3 solicita decisión de la autoridad correspondiente. No publica, acepta, habilita derechos ni despliega por sí solo.

## Contenido del manual conservado

### Página 40 de la edición original

A R Q U I T E C T U RA R E P O / C O L E C C I Ó N D E U S O




06
Cierre de capacidades

Candidato exacto, evidencia y aceptación




Matías Acuña · ArquitecturaRepo                                Revisión de compatibilidad: 17 de octubre de 2026

### Página 41 de la edición original

Contenido

    • 1. Una capacidad es un resultado de producto         • 7. Una ficha de cierre que se pueda auditar
    • 2. Los cinco componentes del cierre                  • 8. Caso de rechazo: corregir sin reiniciar la
    • 3. El candidato exacto es la unidad de revisión        arquitectura

    • 4. Si algo falta, no abras un ciclo artificial       • 9. Producto usable, no solo arquitectura verde

    • 5. Aceptar, retomar o cambiar de objetivo            • 10. Cuándo cerrar la sesión y cuándo detener el
                                                             trabajo
    • 6. Revisión periódica y regla de parada




1. Una capacidad es un resultado de producto

“Gestión de socios” no termina cuando se escribió el formulario. Termina cuando el comportamiento
acordado funciona, conserva los datos pertinentes, satisface las verificaciones aplicables, tiene un estado
actual coherente y cuenta con la aceptación estratégica/humana que corresponda. Un ciclo no es el
número de prompts enviados ni una sesión de Codex: la identidad de campaña debe sobrevivir a
interrupciones normales.

El Planner define la capacidad y su charter; I3 produce un candidato integrado, coordina revisión
independiente y devuelve evidencia. El Planner audita el terminal contra el charter y los requisitos de
producto. El CLIENT interviene cuando se trata de una decisión de producto, una aceptación subjetiva o
una autorización externa reservada.


2. Los cinco componentes del cierre

Componente                                              Pregunta de cierre

Resultado visible                                       ¿La persona usuaria puede hacer lo que pidió, en el entorno
                                                        pertinente?

Pruebas aplicables                                      ¿Pasan tests de unidad, integración, DB/recovery, seguridad,
                                                        UI o runtime que corresponden a la capacidad?

Estado coherente                                        ¿Se conoce el ref/candidato exacto y la versión actual de
                                                        requisitos, Product State y datos relevantes?

Sin bloqueos ocultos                                    ¿Hay defectos materiales que invalidan el resultado aunque
                                                        otros checks estén verdes?

Aceptación competente                                   ¿Planner y, cuando toca, CLIENT verificaron la evidencia en
                                                        vez de aceptar un “DONE”?



No todas las capacidades necesitan todos los tipos de pruebas, pero no se puede reemplazar un gate que
sí aplica con otro más fácil. Un JSON válido no prueba que el CRUD persista. Un test unitario no
demuestra que una persona encuentre la función en la interfaz.

### Página 42 de la edición original

Figura 9. Capas de comprobación. Esquema explicativo; no acredita un proyecto de destino.




3. El candidato exacto es la unidad de revisión

Qué invalida una revisión favorable
Una revisión independiente debe estar vinculada a un ref exacto de código, configuración, datos y
artefactos cuando esas superficies determinan el resultado. Si el productor modifica materialmente el
candidato después del freeze, no se conserva la aprobación anterior por cortesía. El procedimiento es:
nueva mutación, nuevo freeze y nueva revisión. Una conclusión sobre un binario o un dataset no se
transfiere a otro solo porque el nombre sea igual.

I3 entrega evidencia al Planner para auditoría estratégica. Incluso después de un review favorable
pueden quedar abiertos un gate humano, una prueba en entorno real, un permiso de publicación o una
revisión de derechos. El terminal del controlador no equivale a que el producto esté aceptado o
desplegado.

La revisión independiente debe observar el mismo código/ref y estado que se propone aceptar. Si el
productor modifica materialmente el candidato después de la revisión, el veredicto favorable anterior se
invalida para el nuevo candidato. Un enlace histórico al review no prueba que las últimas modificaciones
también se revisaron.

El terminal de I3 es “listo para volver al Planner”, no “producto aceptado”. El ejemplo opcional
campaignctl.py modela el freeze, la revisión independiente y el terminal estratégico, pero no es la
autoridad final de producto ni reemplaza el runtime real.


4. Si algo falta, no abras un ciclo artificial

Si el defectuoso está dentro del charter, el Planner devuelve a I3 una lista consolidada de falsificadores y
evidencia de fallo, sin pedir un nuevo plan por cada bug. I3 se hace cargo de investigación, refactor,
pruebas, integración y nueva revisión. Si la misma clase de defecto se repite, endurece sistemáticamente
el subsistema en vez de acumular correcciones puntuales.

Si aparece una decisión nueva del CLIENT que cambia el producto o un límite esencial del charter, el
Planner registra la nueva autoridad y reconsidera la frontera. Eso es distinto de un test fallido.

Informe breve útil para decidir:


  Candidato: ref exacto y entorno. Resultado observable: qué flujo se ejecutó. Gates comprobados:
  evidencia enlazada. Gates abiertos: qué impiden aceptar. Riesgos y cambios de decisión: separados.
  Próxima acción y responsable: una sola ruta vigente.

### Página 43 de la edición original

5. Aceptar, retomar o cambiar de objetivo

Aceptar: el Planner registra la capacidad y actualiza el Product State y los pointers actuales; el CLIENT
valida el gate que le corresponde. Solo después se activa el trabajo aguas abajo que dependa de esa
capacidad.

Retomar tras interrupción: la sesión nueva reconstruye la campaña y checkpoint actuales; no da por
completado lo que solo estaba iniciado ni inventa aprobación porque haya terminado un límite de uso.

Cambiar prioridades: distinguir un cambio temporal de orden de un cambio real de requisitos. La
autoridad de producto debe persistirse y los trabajos no concluidos necesitan un estado recuperable. No
mantener simultáneamente dos charters actuales contradictorios para el mismo concern.


6. Revisión periódica y regla de parada

Cada semana, el CLIENT debería poder responder en lenguaje simple: qué capacidades están aceptadas,
cuál es la prioridad vigente, qué se puede demostrar hoy, qué fecha objetivo sigue válida, qué riesgos
materiales quedan y qué decisión de producto se le solicita. La cantidad de commits, agentes o horas de
ejecución no constituye por sí misma progreso.

El starter v1 tiene una regla explícita de parada: tras alcanzar los gates de la release, no sumar
mecanismos genéricos por el mero hecho de continuar iterando. Nuevas políticas deben responder a una
clase de fallo real que los controles existentes no cubren. La misma idea se aplica al proyecto: no
confundir más organización con más valor.


7. Una ficha de cierre que se pueda auditar

Un informe de cierre debe poder responder a una persona que no estuvo presente durante la ejecución.
Por eso se registra el candidato exacto, entorno usado, resultado visible, evidencia de los gates
aplicables, qué revisó un agente independiente, qué cambios ocurrieron después de esa revisión y qué
queda fuera de alcance.

Campo                                                 Evidencia exigible en el proyecto

Candidato                                             Ref o identificador exacto del código y estado que se revisó.

Resultado                                             Recorrido visible completado, con entrada y salida
                                                      observables.

Pruebas                                               Salidas de tests e integración apropiadas al tipo de
                                                      capacidad.

Estado persistente                                    Lectura posterior, reinicio y recovery si aplican.

Seguridad / derechos                                  Comprobación proporcional cuando hay datos, red o material
                                                      ajeno.

Revisión                                              Identidad de revisor independiente y vínculo al candidato
                                                      revisado.

Gate humano                                           Aprobación o rechazo del recorrido cuando depende de uso
                                                      real.

Siguiente acción                                      Una ruta vigente: aceptar, volver a I3, esperar decisión o
                                                      bloquear.

### Página 44 de la edición original

Esta ficha es un formato de lectura, no otro Product State que compita con el estado canónico. Las
referencias reales deben vivir en las superficies de evidencia que el proyecto haya definido. Si un enlace
no lleva al artefacto o ref revisado, el informe no permite aceptar por sí solo.


8. Caso de rechazo: corregir sin reiniciar la arquitectura

Cuándo la corrección vuelve a I3 y cuándo al Planner
Si el registro de un socio falla por una validación mal implementada, el defecto ya estaba dentro de la
capacidad: I3 corrige, prueba, integra y vuelve a revisión en la misma campaña. No hace falta crear
otra estrategia ni un nuevo charter. Si el CLIENT cambia las reglas de identidad o aparece una
dependencia que invalida la arquitectura prevista, el Planner revisa la frontera estratégica antes de
continuar.

Un cierre útil tiene dos columnas conceptuales: “evidencia que permite aceptar” y “objeciones aún
abiertas”. Evitá el extremo de aceptar por un check verde y el contrario de mantener la campaña viva
indefinidamente por detalles que ya no amenazan el gate estratégico.

Supongamos que se implementó alta y desactivación de socios y que la revisión encontró una pérdida de
historial al desactivar. El charter ya exige conservación histórica. El Planner no necesita abrir una
campaña distinta para “arreglar la baja”: devuelve una condición concreta a I3. El equipo corrige
persistencia, demuestra que el historial sigue disponible después del reinicio, vuelve a integrar el
candidato y solicita nueva revisión independiente.

Si el revisor evalúa la versión A y el productor cambia la persistencia para crear la versión B, el veredicto
de A no sirve para aceptar B. Es precisamente el motivo de fijar el candidato. I3 no debe reciclar el PASS
anterior ni presentar un “nuevo resultado” sin indicar su referencia.

Si el CLIENT decide ahora que los socios desactivados deben poder reactivarse con permisos especiales,
aparece una regla de producto nueva; requiere confirmación y análisis de impacto antes de asumir que el
charter anterior cubre esa conducta. La separación evita tanto planificación por cada bug como
implementación de requisitos no autorizados.


9. Producto usable, no solo arquitectura verde

Una campaña puede tener contratos correctos, herramientas instaladas y el controlador en estado
terminal, pero seguir sin ofrecer una pantalla utilizable. El gate de aceptación debe demostrar el
resultado de producto. Para una app local de socios, esto incluye abrir el programa, registrar un socio
ficticio, encontrarlo, modificarlo, desactivarlo y verificar conservación del historial. Cuando existe
persistencia, el reinicio forma parte de la prueba.

Para el starter reutilizable hay un gate de release distinto: tools/verify_v1_release.py cubre mecanismos
genéricos y ejemplos sintéticos en el commit concreto. Su PASS no certifica automáticamente una
instalación adaptada ni la aplicación que alguien construya con ella. Cada proyecto mantiene sus propias
pruebas, riesgos y autorizaciones.


10. Cuándo cerrar la sesión y cuándo detener el trabajo

Después de una aceptación estratégica se persiste el cambio de Product State, se actualizan los pointers
actuales y se habilita el trabajo posterior que realmente depende de esa capacidad. Después de un
rechazo se mantiene la misma campaña cuando el defecto está en alcance; después de una invalidación
material se revisa la frontera estratégica. Si la evidencia no permite determinar el estado, la decisión
correcta es una incertidumbre explícita, no una aprobación por intuición.

### Página 45 de la edición original

El CLIENT puede terminar su jornada sin conocer cada detalle del runtime, pero debe poder ver qué
puede usar hoy, qué no puede usar todavía, qué decisión propia está pendiente y cuándo se revisará el
siguiente hito. Un proyecto que solo sabe responder esas preguntas mientras permanece abierto el chat
no superó la prueba de continuidad.

Continuar con: Manual 07, un ejemplo guiado de principio a fin.

Referencias de esta edición
Fuente: repositorio público ArquitecturaRepo en el commit 9c00e19b74d1 . Rutas verificadas:

  • protocols/REVIEW_FREEZE_AND_TERMINAL_INTEGRITY.md
  • protocols/CAPABILITY_LIFECYCLE_AND_EVIDENCE.md
  • docs/10_EXECUTABLE_VALIDATION.md
  • docs/17_V1_RELEASE_GATES.md

Las instrucciones de este volumen describen el starter y un procedimiento de uso. Ninguna prueba de los
ejemplos sustituye la verificación del proyecto de destino.
