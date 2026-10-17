# 03 — Operación diaria | ArquitecturaRepo v1.3.0

> Manual de uso revisado para el release público v1.3.0 (17 de octubre de 2026). Conserva el contenido textual del manual original 00–07 de septiembre de 2026 con correcciones específicas. La fuente era un PDF ilustrado: los pies de figura se conservan pero esta transcripción Markdown no reproduce las imágenes. No utilizar las cifras de página como referencia del archivo renderizado.

## Actualización comprobada para v1.3.0

- Distinguir Goal estratégico protegido, `runtime/TACTICAL_PLAN_CURRENT.json` editable por I3, campaña/runtime y artefactos realmente ejecutados.
- `tools/goal_plan.py` conserva revisiones del plan con control de concurrencia y evidencia de revisión, pero declara el reloj activo **no verificado** y no emite permisos de ejecución nativos.
- `tools/host_dispatch.py` está diseñado para detener el despacho si el host no demuestra seguridad de write-set y costo por comando. No equivale a automatizar Codex Desktop.
- Un ciclo útil acaba en incremento físico observable, bloqueo causal preciso o checkpoint recuperable, no en sumar ejecuciones/commits.
- Cuando `/plan` no existe como herramienta nativa en el host real, guardar el plan local no debe declararse equivalente a que el host lo haya integrado. Hacen falta adaptación y comprobación separadas.

## Contenido del manual conservado

### Página 21 de la edición original

A R Q U I T E C T U RA R E P O / C O L E C C I Ó N D E U S O




03
Operación diaria

Continuidad, ejecución y control




Matías Acuña · ArquitecturaRepo                                Revisión de compatibilidad: 17 de octubre de 2026

### Página 22 de la edición original

Contenido

     • 1. Preparar una sesión sin volver a empezar                       • 7. Cierre diario en cinco preguntas
     • 2. Convertir un deseo en una capacidad                            • 8. Una jornada completa sin depender del chat
       comprobable                                                       • 9. Ejemplo de despacho bien delimitado
     • 3. Qué hace I3 cuando el trabajo se complica                      • 10. Cómo interpretar los estados de un controlador
     • 4. Autorizaciones y acciones externas                             • 11. Qué hacer con el reporte final
     • 5. Cómo leer el reporte del ejecutor                              • 12. Cierre de sesión recuperable
     • 6. Git y la continuidad




1. Preparar una sesión sin volver a empezar

Apertura operativa de dos minutos
Antes de dar una orden nueva, verificá repo y rama de destino, cambios sin integrar, Product State,
charter/ejecución activos y último candidato comprobado. Si un agente retoma el trabajo tras un límite de
uso, debe leer el checkpoint vigente, no arrancar “un proyecto parecido” desde un prompt anterior. El
CLIENT puede ver un resumen corto; no necesita depurar qué hash prevalece.

En un clon con baseline conocido, el trabajo de sincronización comienza por el delta exacto del branch
pertinente. No uses git pull , reclonado o relectura exhaustiva por rutina si el controlador puede
identificar el conjunto de cambios y sus dependencias; tampoco uses sincronización incremental cuando
hay divergencia o pérdida de autoridad aún sin resolver.

Antes de pedir otra función, el Planner recupera el objetivo actual, el Product State y el estado exacto de
la campaña o del candidato en revisión. Codex abre el repositorio local correcto y consulta las
instrucciones de agentes aplicables. Si la información actual está incompleta, se identifica el UNKNOWN y
no se fabrican hechos desde el chat anterior.

No hace falta dividir físicamente la pantalla en dos mitades; es una comodidad, no una regla de la
arquitectura. Sí hace falta que el ejecutor tenga el repositorio y el Planner pueda acceder a evidencia
fiable. Si el código fue modificado remotamente, el ejecutor reconcilia el delta con su trabajo local antes
de mutar; no se reclona por rutina.




  Figura 6. Ciclo de una capacidad. Esquema explicativo; no acredita un proyecto de destino.

### Página 23 de la edición original

2. Convertir un deseo en una capacidad comprobable

Un pedido útil describe un resultado observable. “Registrar pagos de cuotas y mostrar deuda de un socio”
es una capacidad; “escribir una función de pagos” es una microtarea. El Planner identifica dependencias
reales, riesgos, interfaces y gate de producto, define el charter y deja que I3 organice la implementación
interna.

Ejemplo de encargo breve del CLIENT:


  Necesito registrar pagos de cuotas sin perder el historial. El personal debe poder ver quién está al
  día. No agregues pagos online en esta etapa; mantené simple la pantalla. Quiero comprobar el flujo
  completo antes de aceptarlo.


Un dispatch del Planner al I3/Codex contiene al menos: objetivo de la capacidad, fuentes actuales,
límites/exclusiones, owners/interfaces, gates de ejecución y evidencia exigida para considerar que el
candidato está listo. No debe transformar al CLIENT en jefe de cada subagente.


3. Qué hace I3 cuando el trabajo se complica

Una falla normal no es una campaña nueva
Supongamos que la funcionalidad está implementada pero falla una prueba de integración. I3 conserva el
log, ubica la causa, corrige el componente implicado, vuelve a probar, integra y solicita revisión
independiente sobre el nuevo candidato. No pide al Planner que reprograme la estrategia en cada fallo. Si
reaparece la misma clase de defecto, corresponde endurecer el subsistema y revisar la causa sistémica
antes de seguir acumulando parches locales.

Un bloqueo de currentness, una autorización externa ausente o un cambio material del objetivo no son
simplemente “otro retry”: se declaran con la autoridad y evidencia apropiadas. La distinción permite
continuar sin fingir que todo error tiene la misma solución.

I3 puede investigar, implementar, modificar pruebas, revisar, corregir, integrar y reintentar dentro del
charter. Un bug de una feature autorizada no es motivo para crear un nuevo plan estratégico. Si vuelve a
fallar la misma clase de defecto, se revisa la causa sistémica dentro de la campaña en vez de acumular
parches equivalentes.

La revisión independiente debe examinar el candidato exacto que se devolverá al Planner. Si cambió el
código materialmente después del review, la evaluación favorable anterior no habilita el nuevo estado. El
runtime campaignctl.py es una implementación opcional de parte de este control; no ejecuta agentes en
la nube automáticamente ni concede autoridad por sí mismo.


4. Autorizaciones y acciones externas

Acción observada                                               Tratamiento

Leer repositorio, correr pruebas locales o modificar código    Trabajo técnico normal con permisos adecuados.
dentro del alcance aprobado

Instalar dependencias o acceder a una herramienta nueva        Comprobar procedencia, permisos y alcance; no aceptar
                                                               ciegamente prompts de ejecución.

Desplegar, publicar, enviar correos, gastar crédito o borrar   Requiere la autorización externa correspondiente y preflight
datos                                                          proporcional al riesgo.

### Página 24 de la edición original

Acción observada                                           Tratamiento

Solicitud de contraseña, token o dato privado en el chat   No copiarlo al chat ni al repositorio; usar el mecanismo de
                                                           secretos autorizado.

Contradicción en estado actual, datos o ownership          HOLD para lo dependiente; I3/Planner reconstruyen evidencia
                                                           antes de actuar.



El CLIENT autoriza efectos externos reservados y decide preferencias de producto. No tiene que escoger
el nombre de la base de datos, coordinar tres ramas ni interpretar un error de migración.


5. Cómo leer el reporte del ejecutor

Un reporte que permite auditar, no impresionar
Pedí una referencia exacta del candidato, qué comportamiento se intentó obtener, qué cambió de forma
verificable, qué pruebas se corrieron y en qué entorno, qué falló, qué revisión independiente se hizo y
qué gate sigue abierto. Un conteo de commits, horas de ejecución o mensajes no mide avance de
producto. No aceptes “todo verde” sin distinguir unidad, integración, datos, experiencia de uso y
publicación cuando correspondan.

El reporte debe nombrar la próxima acción y su owner. Si hay un nuevo requisito de negocio, vuelve al
CLIENT/Planner; si es un bug previsto en el charter, se queda en ejecución; si hay candidato listo, vuelve
a la auditoría estratégica. De ese modo el CLIENT no actúa como coordinador técnico de incidentes.

Un buen reporte devuelve qué candidato/ref modificó, qué comportamiento comprobó, qué pruebas
corrió, qué falló y se corrigió, qué evidencia física existe y qué gates siguen abiertos. Decir “hecho” o
mostrar un diff no sustituye una demostración del flujo de usuario. El Planner contrasta el reporte con la
evidencia del repositorio y, cuando importa, el runtime o la DB.

Cuando la evidencia es suficiente: el Planner registra aceptación de la capacidad y la próxima
frontera legal. Cuando el defecto es del mismo alcance: devuelve los falsificadores consolidados a la
misma campaña. Cuando cambió el objetivo de producto: registra la nueva decisión del CLIENT y
reconsidera el charter; no la oculta como un bug.


6. Git y la continuidad

GitHub conserva código e historial; no es por sí solo un Product State. Un commit señala una unidad de
integración, no la autoría completa de todos los actos ni la aceptación del producto. Los workers I4 no
deben producir commits canónicos por defecto; la integración corresponde a la autoridad del sistema que
coordina la campaña.

No hagas un commit por mensaje ni borres un árbol local para “sincronizar”. Cuando existe un clon
confiable, se observa el delta exacto de la rama antes de decidir merge, pull o nuevo checkout.
Conflictos, cambios locales sin integrar y evidencia no publicada requieren tratamiento explícito del
ejecutor.

Una sesión nueva puede continuar el mismo objetivo si el charter, checkpoint, code/ref y evidencia son
reconstruibles. Un límite temporal de uso no transforma el trabajo en una nueva campaña.


7. Cierre diario en cinco preguntas

 1. ¿Qué capacidad sigue activa y quién la controla?

### Página 25 de la edición original

2. ¿Qué ref/estado actual está comprobado?
 3. ¿Cuál fue el último gate realmente superado?
 4. ¿Qué defecto, riesgo o decisión de producto sigue abierta?
 5. ¿Cuál es la próxima acción legal para mañana, sin requerir que el CLIENT interprete la arquitectura?

Registrá en el repositorio las decisiones materiales; el chat puede contener conversación útil, pero no
debe ser el único sitio donde exista la verdad actual. Para reglas de producto nuevas, continuá con el
Manual 04; para bloqueos, el Manual 05.


8. Una jornada completa sin depender del chat

Al comenzar, identificá el objetivo actual antes de pedir otra función. El Planner verifica si hay campaña
abierta, cuál es el último ref integrado, qué evidencia falta y si hay alguna decisión reservada al CLIENT.
Si el trabajo quedó suspendido por capacidad o una sesión terminó, la continuidad debe venir de un
checkpoint o del estado durable, no de “recuerdo que íbamos por la mitad”.

El primer pedido del día debe producir una ruta clara: continuar el encargo vigente, auditar un terminal,
resolver una decisión de producto o iniciar una capacidad nueva que ya esté autorizada. No es necesario
abrir múltiples conversaciones para cada una de estas acciones. Podés dejar la ventana de planificación a
un lado y la ejecución a otro; esa disposición es comodidad, no un mecanismo de seguridad ni una
condición del starter.


9. Ejemplo de despacho bien delimitado

Un mensaje de ejecución puede contener todas las condiciones necesarias sin convertir al CLIENT en
director técnico. El siguiente modelo no es un prompt universal; representa una campaña cuya autoridad
y requisitos ya existen en el repositorio:


  Goal: implementar la capacidad de socios del charter vigente. Context: leer AGENTS.md , requisitos
  actuales, Product State, charter autorizado y código/ref real; reconstruir antes de mutar. Constraints:
  conservar historial, respetar la exposición local confirmada, no añadir pagos online ni funciones
  nuevas, no publicar ni gastar servicios externos. Execution gates: probar físicamente alta, búsqueda,
  edición, desactivación y persistencia al reiniciar; comprobar entradas inválidas y duplicados; revisar
  independientemente el candidato integrado. Done when: entregar ref exacto, evidencia rastreable,
  resultado de revisión y un terminal honesto para auditoría de Planner. Resolver bugs ordinarios,
  refactors y reintentos dentro del mismo charter sin pedirme microdecisiones técnicas.


El mensaje debe adaptarse al charter actual; si ese charter ya resolvió restricciones distintas, se aplica el
contrato vigente. No inventes un AGENTS.md o un Product State por el mero hecho de que aparecen en
este ejemplo: el agente debe localizar las superficies efectivamente existentes y registrar las faltantes.


10. Cómo interpretar los estados de un controlador

Estado operativo                     Qué significa                        Qué no significa

READY                                Hay trabajo con dependencias         Que esté ejecutándose.
                                     satisfechas.

ACTIVE                               Una ejecución posee una unidad       Que el resultado funcione.
                                     autorizada.

### Página 26 de la edición original

Estado operativo                     Qué significa                           Qué no significa

VERIFY                               Se reúnen y ejecutan comprobaciones     Que todos los gates del producto están
                                     aplicables.                             satisfechos.

HOLD / CAPACITY                      Existe una razón registrada para        Que deba abrirse otra campaña.
                                     detener o pausar.

DONE táctico                         Una unidad cumplió sus condiciones      Que Planner aceptó la capacidad.
                                     locales.

Terminal estratégico                 I3 devuelve un candidato o un bloqueo   Que el CLIENT autorizó publicación.
                                     explicado.



El runtime de referencia del starter es un mecanismo opcional de control: no llama a Codex por sí solo ni
crea un entorno distribuido. Si un proyecto usa un controlador distinto, exige que los mismos límites de
autoridad, currentness y recuperación puedan verificarse en su implementación real.


11. Qué hacer con el reporte final

Una respuesta útil identifica el candidato exacto, el entorno comprobado, las pruebas realizadas, las
fallas o riesgos restantes, la revisión independiente y el estado siguiente propuesto. El Planner contrasta
esas afirmaciones con pruebas y artefactos; no reescribe el mismo trabajo ni aprueba solo porque el
reporte diga PASS.

Si el candidato requiere correcciones in-scope, la devolución a I3 debe consolidar defectos:
comportamiento observado, condiciones para reproducirlo, evidencia y qué gate bloquea. Es
responsabilidad de I3 corregir e integrar sin pedirle al CLIENT que decida cómo depurar. Si la misma clase
de problema regresa reiteradamente, I3 debe revisar el subsistema y sus tests en conjunto, no encadenar
remiendos locales.


12. Cierre de sesión recuperable

Antes de terminar una jornada larga, el sistema deja persistidos el ref de código, el objetivo activo, el
último checkpoint, la evidencia y el trabajo pendiente. El CLIENT debería poder preguntar “¿qué puedo
usar hoy?” y obtener una respuesta sobre capacidades y riesgos, no un transcript técnico. Una sesión
nueva demuestra continuidad cuando puede recuperar ese estado por su cuenta. En caso contrario, no se
debe confundir la sesión que sigue abierta con un proyecto realmente recuperable.

Referencias de esta edición
Fuente: repositorio público MatiasAcunia/ArquitecturaRepo en el commit 56f04267b6a9 . Rutas verificadas:

  • protocols/EXECUTION_TEAM_OS.md
  • protocols/CAPABILITY_LIFECYCLE_AND_EVIDENCE.md
  • docs/11_REFERENCE_RUNTIME.md
  • docs/20_REPOSITORY_EFFICIENCY_AND_LOCAL_HYGIENE.md
  • tools/campaignctl.py

Las instrucciones de este volumen describen el starter y un procedimiento de uso. Ninguna prueba de los
ejemplos sustituye la verificación del proyecto de destino.
