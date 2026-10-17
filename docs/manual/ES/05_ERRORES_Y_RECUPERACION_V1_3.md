# 05 — Errores y recuperación | ArquitecturaRepo v1.3.0

> Manual de uso revisado para el release público v1.3.0 (17 de octubre de 2026). Conserva el texto del manual original 00–07 de septiembre de 2026 y solo añade aclaraciones relacionadas con cambios reales en v1.3. Los pies de las figuras se conservan, pero esta transcripción Markdown no incluye las imágenes del PDF original.

## Actualización comprobada para v1.3.0

- Los diagnósticos de currentness de SQLite reconocen WAL: un SHA del archivo SQLite principal por sí solo no autentica necesariamente el estado completo en caliente.
- Un host interrumpido después de despachar una operación puede quedar en `EFFECT_UNKNOWN`; no hay que reejecutarla a ciegas. Usá la vía de reconciliación/readback y preservá idempotency key y linaje.
- La limpieza de disco se apoya en el ledger de artefactos; solamente descartables con ownership y comprobación positiva pueden eliminarse. Fuente, estado canónico, DB, evidencia vigente y archivos desconocidos no son basura.
- Si la misma ruta no produce resultados, I3 cambia materialmente el método o registra el bloqueo exacto dentro de la campaña. Una sucesión de reintentos idénticos no es una mejora.
- El host externo debe demostrar permisos, límites de escritura/costo y recepción de efectos; pasar tests del núcleo portable no significa tener operaciones nativas Codex habilitadas.

## Contenido del manual conservado

### Página 33 de la edición original

A R Q U I T E C T U RA R E P O / C O L E C C I Ó N D E U S O




05
Errores y recuperación

Diagnóstico, autoridad y respuesta proporcional




Matías Acuña · ArquitecturaRepo                                Revisión de compatibilidad: 17 de octubre de 2026

### Página 34 de la edición original

Contenido

     • 1. El primer movimiento ante un error es conservar                • 6. Seguridad, privacidad y derechos
       evidencia                                                         • 7. Salir del incidente de forma comprobable
     • 2. Cuando falla el entorno                                        • 8. Tres incidentes y su ruta de recuperación
     • 3. Si el control layer no valida                                  • 9. Matriz de decisiones para operaciones sensibles
     • 4. Git no es un botón de “deshacer problemas”                     • 10. Qué no demuestra una verificación exitosa
     • 5. Un fallo que se repite requiere revisar la causa               • 11. Privacidad y feedback del starter




1. El primer movimiento ante un error es conservar evidencia

Copiá el mensaje exacto, el comando o acción que lo produjo y el momento en que apareció. No borres
una carpeta, reinstales todo ni reclones el repositorio como reflejo. El responsable técnico tiene que
distinguir si se trata de un problema de herramienta, permiso, código, contrato del control layer, DB,
despliegue o autorización externa.




  Figura 8. Ruta de recuperación. Esquema explicativo; no acredita un proyecto de destino.




Señal                                                                 Respuesta inicial

Error local de una prueba en una feature activa                       El Campaign Lead conserva logs y corrige dentro del mismo
                                                                      charter.

 validate_project.py rechaza el estado de control                     HOLD sobre decisiones dependientes; localizar relación y
                                                                      owner causales.

Repo con cambios locales y remotos incompatibles                      Conservar ambas versiones; reconciliar desde evidencia, sin
                                                                      sobrescribir al azar.

Datos de usuario posiblemente dañados                                 Detener nuevas escrituras sensibles, preservar backups y
                                                                      evaluar recuperación antes de ejecutar scripts.

Falta autorización para publicar o gastar                             No actuar externamente hasta obtener autorización explícita
                                                                      del CLIENT.



El objetivo no es “que el error desaparezca de la pantalla”. Es que el sistema recupere un estado
verdadero y pueda demostrar que el mismo defecto no sigue oculto.

### Página 35 de la edición original

2. Cuando falla el entorno

Python o comando no encontrado: comprobar la carpeta, el ejecutable y la versión instalada. No
descargar herramientas desde enlaces aleatorios. Codex puede diagnosticar la ruta y el entorno si tiene
acceso; si solo tenés el error, copiá el texto completo sin editarlo.

GitHub no aparece en ChatGPT: distinguir autenticación, permisos de la integración, alcance de
repositorios y falta de visibilidad del conector. Una lectura fallida no autoriza cambiar archivos o conceder
acceso a toda la cuenta. Verificá que el repo exacto esté autorizado.

Codex no abre el proyecto: verificar que la carpeta local exista y sea la del producto. No abrir
ArquitecturaRepo en lugar de club-app por parecido de nombres. Si faltan permisos, evaluá la solicitud
concreta y no habilites acceso indiscriminado.

Límite temporal de uso o interrupción: un límite de la sesión no elimina la campaña durable. El
ejecutor debe persistir un checkpoint coherente cuando sea posible y la nueva sesión reconstruirlo antes
de continuar. No se abre una campaña nueva solo porque cambió la ventana de chat.


3. Si el control layer no valida

Separá un error del validador de un error de la aplicación
validate_project.py examina contratos y relaciones dentro de .agentic-sdlc ; puede bloquear una
referencia inexistente, un owner duplicado o una cadena de candidato/revisión incompatible. No
diagnostica por sí solo la conexión de la app a la DB ni el resultado de una acción de usuario. Guardá el
error exacto, la ruta del control y el ref actual antes de tocar archivos; el responsable técnico determina si
corresponde actualizar una superficie propietaria, recuperar una transacción o corregir una referencia.

Nunca cambies estados a READY ni borres el journal para hacer pasar el validador. Si hay dos
owners plausibles o un candidato cambiado después de su revisión, necesitás reconstrucción, no una
modificación cosmética de JSON.

 tools/validate_project.py valida contratos y relaciones del control layer; puede rechazar estado
incoherente antes de una implementación peligrosa. No fuerces JSON para convertir la pantalla en verde.
El Planner/I3 deben recuperar la autoridad, el último ref comprobado, el archivo causal y los objetos
relacionados.

Una transacción parcialmente escrita puede dejar un journal pendiente. La ruta documentada en docs/
12_TRANSACTION_RECOVERY.md es recuperación explícita, con comparación de hashes before/after; una
modificación externa conflictiva no debe sobrescribirse por conveniencia. El control layer puede rechazar
acciones normales mientras la reconciliación esté pendiente.

Punto importante: la validación estructural verde tampoco significa que una DB real está sana. El
estado de producción requiere evidencia del entorno actual y de los datos que utiliza la aplicación.


4. Git no es un botón de “deshacer problemas”

Si GitHub Desktop muestra conflicto, no elijas automáticamente “mi versión” o “la remota”. Ambas
pueden contener cambios válidos. Si se necesita sincronizar, el ejecutor primero observa el delta del ref
exacto y el estado local. No elimina .git , no reclona sin motivo ni convierte cada intento fallido en un
commit canónico.

El starter incluye tools/repo_delta.py para una inspección incremental y tools/workspace_gc.py para
limpieza de workspaces marcados. El GC no es una licencia para borrar assets de producto, evidencia

### Página 36 de la edición original

aceptada, carpetas humanas ni directorios que “parecen viejos”. Empezá con un dry-run; la ausencia de
ownership positivo significa conservar.


5. Un fallo que se repite requiere revisar la causa

Un reintento idéntico con el mismo entorno y las mismas hipótesis rara vez reduce el riesgo. Después de
varios fallos del mismo tipo, I3 debe agrupar los falsificadores, revisar interfaces y dependencias
afectadas, fortalecer evaluadores y obtener revisión independiente. Sigue siendo la misma campaña
mientras el charter no haya sido invalidado materialmente.

No abras una feature nueva para escapar del bug. No aceptes el resultado porque “ahora pasan los tests”
si el flujo real permanece roto. El cierre exige evidencia del candidato actual y de los gates pendientes.


6. Seguridad, privacidad y derechos

Autorizaciones que no se deducen de un charter
Acceso a credenciales, gasto con APIs, borrado de datos protegidos, exposición de red y publicación de
material ajeno tienen límites de autorización propios. Un charter técnico no concede permiso implícito
para pagar un servicio o subir información privada. Usá permisos mínimos, datos ficticios en ejemplos y
evidencia de licencias cuando un artefacto pueda publicarse.

En scaffolds actuales puede instalarse un workflow de feedback arquitectónico: por defecto genera un
artefacto de metadatos limitados dentro de GitHub Actions, con envío externo deshabilitado. Debe
comunicarse al CLIENT y puede desactivarse; habilitar envío externo requiere una decisión explícita. La
licencia MIT del código y documentación originales del starter no concede derechos sobre assets de
terceros.

Las acciones con efectos externos deben distinguirse de pruebas locales: publicación, despliegue, gasto,
borrado masivo, migración irreversible, tratamiento de datos sensibles y transferencia de archivos a
servicios externos. El CLIENT autoriza lo reservado; el equipo técnico evalúa la implementación, los
límites, el rollback y la observabilidad.

  • Nunca pegues contraseñas, tokens o claves privadas en el repositorio ni en un prompt. Usá los
    mecanismos de secretos propios del entorno.
  • Para datos personales, trabajá con datos sintéticos o anonimizados en demostraciones y revisiones
    no autorizadas.
  • Antes de una migración o limpieza destructiva, verificá backup, recuperación y qué registros serán
    afectados.
  • Antes de publicar música, imágenes, código o clips de terceros, verificá licencias, atribución y alcance
    de uso. La licencia MIT del starter no concede derechos sobre recursos de terceros ajenos al
    repositorio.
  • Los servicios de pago requieren un presupuesto y autorización de alcance; un fallo de conexión no
    autoriza reintentos ilimitados.

El workflow opcional de feedback del starter genera metadatos estrictos y guarda un artefacto
almacenado en GitHub Actions por defecto. El envío externo está desactivado salvo opt-in explícito. Podés
deshabilitar el workflow si no corresponde al proyecto. Revisá cualquier workflow ejecutable como parte
de los límites de confianza del repo.

### Página 37 de la edición original

7. Salir del incidente de forma comprobable

La reparación debe explicar: qué falló, por qué, qué cambió, qué datos/ref fueron preservados o
restaurados, qué pruebas físicas pasaron, qué queda sin verificar y quién es dueño de la próxima acción.
El informe de un worker es evidencia para I3; el Planner decide si el resultado restaura la capacidad y su
estado estratégico.


  Si no se pudo reconstruir el estado actual o no existe una copia confiable de datos críticos, la salida
  correcta es declarar el bloqueo concreto. Continuar como si el incidente hubiese terminado crearía
  una segunda falla de control.



8. Tres incidentes y su ruta de recuperación

Incidente A · Se interrumpió la sesión de Codex
No inicies una copia nueva del mismo encargo por reflejo. El sistema debe verificar si hubo escritura
parcial, qué candidato está integrado y si existe una autoridad de ejecución todavía activa. A partir de
Product State, charter, checkpoint y runtime reconstruye la siguiente unidad legal. Cuando falta una
referencia crítica, registra HOLD y explica qué evidencia debe recuperar.

Un límite de uso del servicio no invalida la arquitectura. Lo que sí la invalida es depender exclusivamente
del historial de una sesión: sin estado durable no puede demostrarse qué trabajo está autorizado ni qué
se debe retomar.

Incidente B · Falló una actualización de varios archivos de estado
Una transición puede actualizar bootstrap, Product State, ownership y checkpoint. Si el proceso se
interrumpe a la mitad, dos archivos podrían aparentar estados actuales incompatibles. El starter utiliza
un journal de transacción para esas operaciones del control layer: mientras queda una transacción
pendiente, la inspección o mutación normal relevante debe detenerse hasta recuperación explícita.

El camino del proyecto de referencia es comprobar primero el estado del journal y después utilizar la
recuperación documentada por la herramienta que efectuó la transición, por ejemplo campaignctl recover
para su runtime. El mecanismo solo avanza si los hashes demuestran que cada destino pertenece todavía
a esa transacción; un cambio externo produce CONFLICT , no una sobrescritura forzada. No edites los JSON
manualmente para “quitar el HOLD”.

Incidente C · Un cambio funciona en tests pero falla al usarlo
Guardá una prueba reproducible del recorrido, versión exacta, entorno y salida observable. La
arquitectura debe distinguir el gate que pasó de aquel que falló. No repitas un test unitario esperando
demostrar un defecto de interacción o de persistencia: ejecutá la comprobación adecuada sobre el
candidato actual y repará el subsistema sin cambiar de campaña cuando el defecto sea in-scope.


9. Matriz de decisiones para operaciones sensibles

Acción                              Riesgo específico                     Límite antes de ejecutar

Mostrar una demo con datos reales   Exposición de información personal.   Usar datos ficticios o contar con
                                                                          autorización adecuada y control de
                                                                          acceso.

Crear un token para GitHub          Acceso excesivo o filtración.         Alcance mínimo, secreto fuera del repo
                                                                          y revocación si se expone.

### Página 38 de la edición original

Acción                                Riesgo específico                        Límite antes de ejecutar

Eliminar carpetas temporales          Borrar trabajo o evidencia todavía       Identidad de propietario,
                                      necesarios.                              reconstruibilidad, caducidad y dry-run
                                                                               verificables.

Desplegar públicamente                Exposición de red, datos y gastos.       Confirmar objetivo y autoridad externa;
                                                                               revisar configuración de seguridad.

Activar una API paga                  Gasto o reintentos incontrolados.        Presupuesto y tope autorizados; registro
                                                                               de ejecución y modo terminal de error.

Publicar medios de terceros           Reutilización sin licencia suficiente.   Verificar procedencia y derechos de
                                                                               publicación en ese contexto.



Un “sí” general para que un agente trabaje en tu carpeta no equivale a autorización para acciones
irreversibles, gasto externo o publicación. La implementación de controles técnicos pertenece al equipo;
la decisión reservada de negocio o exposición debe quedar explícita.


10. Qué no demuestra una verificación exitosa

Que validate_project.py termine correctamente puede demostrar relaciones entre contratos de estado;
no demuestra que el backend responda, que una base de datos conserve información después de un
reinicio o que los permisos de un endpoint sean seguros. Un test de adopción con datos sintéticos no
autoriza migrar una base real sin comprobar el caso específico. Un video que parece correcto tampoco
sustituye una evaluación del flujo por la persona que lo usará.

Al cerrar un incidente, repetí el gate que falló y las comprobaciones vecinas que podrían haber sido
afectadas por la reparación. Registrá el nuevo candidato y quién lo revisó. Si aparece una contradicción
relevante entre código, DB y estado actual, mantené HOLD para las acciones dependientes hasta
conciliarla físicamente.


11. Privacidad y feedback del starter

Los scaffolds actuales pueden incorporar un workflow periódico que genera un informe de metadatos
limitado y lo almacena como artefacto de GitHub Actions. Según la documentación actual, el envío a un
endpoint externo está apagado por defecto y necesita tanto habilitación en el config como variables del
repositorio. Si no querés esa observabilidad, se puede desactivar o evitar su instalación.

Revisá permisos y cambios de cualquier workflow porque es código ejecutable. No confundas la política
declarada del reportador con una garantía universal para aplicaciones que se instalen posteriormente:
cada proyecto debe comprobar de forma independiente sus secretos, permisos y tratamientos de datos.

Continuar con: Manual 06 para el cierre formal y el tratamiento de gates pendientes.

Referencias de esta edición
Fuente: repositorio público MatiasAcunia/ArquitecturaRepo en el commit 56f04267b6a9 . Rutas verificadas:

  • protocols/SECURITY_PRIVACY_RIGHTS_AND_EXTERNAL_ACTIONS.md
  • docs/12_TRANSACTION_RECOVERY.md
  • docs/22_PRIVACY_PRESERVING_ARCHITECTURE_FEEDBACK.md
  • tools/state_tx.py
  • tools/workspace_gc.py

### Página 39 de la edición original

Las instrucciones de este volumen describen el starter y un procedimiento de uso. Ninguna prueba de los
ejemplos sustituye la verificación del proyecto de destino.
