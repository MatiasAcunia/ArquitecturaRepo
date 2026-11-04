# 05 — Errores, incidentes y recuperación

ArquitecturaRepo · Manual completo de uso · Edición v1.4 · Español

> El objetivo de recuperar un proyecto es volver a un estado **verdadero y verificable**, no simplemente hacer desaparecer un mensaje de error. Se conservan fuente, ownership, journal de transacciones, testigos de DB y evidencia vigente. Un bug ordinario dentro de un charter pertenece a I3; la falta de autorización o un conflicto de currentness canónica exige otra ruta.

## Contenido del capítulo

1. Primero conservar evidencia
2. Cuando falla el entorno o una cuenta
3. Si no valida el control layer
4. Git no es un botón para «deshacer problemas»
5. Un fallo repetido exige cambiar la causa
6. Seguridad, privacidad y derechos de terceros
7. Salir de un incidente con pruebas
8. Tres incidentes completos y su recuperación
9. Matriz para operaciones sensibles
10. Qué no demuestra una validación verde
11. Privacidad y feedback del starter

## 1. Primero conservar evidencia

Guardá el mensaje exacto, el comando o acción que lo produjo, el momento, el repositorio y worktree afectados, y el ref de código o artefacto cuando exista. No borres la carpeta, reinstales todo, descartes cambios locales ni crees otro clon por reflejo. Esas medidas pueden destruir la información que el responsable técnico necesita para recuperar el proyecto.

Antes de reparar, hay que clasificar el problema: herramienta faltante, permiso, defecto de aplicación, contrato de gobierno inválido, fuente desactualizada, transacción interrumpida, proveedor externo o autorización reservada. Son incidentes distintos y sus soluciones no son intercambiables.

| Señal | Respuesta inicial segura |
| --- | --- |
| Falla una prueba de integración de la feature activa. | I3 conserva reproducción y corrige en el charter vigente. |
| El validador rechaza un registro canónico. | HOLD de acciones dependientes e identificación de la relación y owner causales. |
| Hay cambios Git locales y remotos incompatibles. | Preservar ambas versiones, inspeccionar delta y conciliar sin adivinar. |
| Los datos reales de usuarios podrían estar dañados. | Detener escrituras sensibles, conservar backups, WAL y journal, evaluar restauración. |
| Falta permiso para publicar o gastar. | No ejecutar el efecto externo hasta contar con autorización específica. |
| El host pudo despachar una operación antes de caer. | Registrar el efecto como desconocido y realizar readback antes de reintentar. |

No se trata de que haya menos indicadores rojos, sino de corregir la causa y demostrar que el gate correspondiente pasa en el candidato actual. A menudo se puede continuar con análisis de solo lectura mientras las mutaciones materiales permanecen bloqueadas.

## 2. Cuando falla el entorno o una cuenta

**Python o un comando no se reconoce.** Verificá ruta, ejecutable, versión y entorno activo. Instalá las dependencias declaradas desde fuentes confiables. No modifiques Product State para compensar una herramienta ausente. Si el agente de programación puede inspeccionar la máquina, que examine el entorno; si no, conservá la salida completa para quien tenga acceso.

**GitHub no aparece en ChatGPT.** Distinguí autenticación, instalación del conector, permisos, alcance de repositorios y visibilidad de la rama. Un error de lectura no justifica dar acceso a toda la cuenta, entregar credenciales o cambiar archivos. Probá una lectura del repositorio concreto dentro del permiso autorizado.

**El ejecutor abre otro proyecto.** Confirmá que la carpeta existe y corresponde a la aplicación, no al starter genérico `ArquitecturaRepo/`. Antes de escribir, comprobá worktree, rama, archivos y permisos. Dos directorios parecidos no son intercambiables.

**Se interrumpe la sesión o se alcanza el límite de uso.** La sesión comercial no define la identidad de la campaña. Recuperá el Goal, owner, checkpoint, candidato integrado y efectos pendientes desde evidencia durable. El límite de una conversación no autoriza abrir otra campaña ni un controlador competidor. Si el servicio no puede recuperar el thread anterior, el repositorio sigue siendo la fuente de continuidad.

## 3. Si no valida el control layer

El `tools/validate_project.py` instalado examina contratos y referencias de `.agentic-sdlc/`. Puede rechazar una autoridad inexistente, un owner duplicado, una relación candidato/review incompatible o una referencia `CURRENT` mal formada. No demuestra por sí solo que la aplicación se conecte a su DB, que alguien pueda iniciar sesión o que los pagos sobrevivan a un reinicio.

Antes de tocar estado, conservá el error, el root del control, ref actual de Git, cambios locales y testigos relevantes de DB. El owner técnico determina si falta una dependencia, cambió el contrato, hay una referencia stale, una transacción parcial o una modificación externa conflictiva.

No escribas `READY` en un JSON ni borres el journal para obtener una pantalla verde. Si dos actores reclaman el mismo efecto o un candidato cambió después de una revisión favorable, la solución es reconstruir autoridad y lineage. Un ajuste cosmético puede hacer que el informe parezca correcto mientras empeora el estado real.

Las transiciones pueden actualizar varios archivos canónicos. El framework describe [recuperación transaccional](../../../12_TRANSACTION_RECOVERY.md) basada en hashes antes y después. Un journal pendiente puede bloquear legítimamente otras escrituras. Si un tercero modificó uno de los destinos, la recuperación debe registrar `CONFLICT`, no sobrescribirlo por comodidad. Solo se reanuda cuando las relaciones pertinentes concuerdan y el resultado de recuperación fue comprobado físicamente.

En SQLite, el archivo principal `.db` no siempre representa todo el estado vivo si se utiliza Write-Ahead Logging. El WAL y un snapshot consistente pueden ser indispensables. Un hash del archivo principal aislado no autentica automáticamente el contenido actual. La ruta de [attachment de gobierno existente](../../../32_EXISTING_GOVERNED_ATTACHMENT.md) contempla esta distinción, pero no repara automáticamente una base de producción.

## 4. Git no es un botón para «deshacer problemas»

Cuando GitHub Desktop o la consola muestran un conflicto, no elijas ciegamente «mi versión» o «la remota». Las dos pueden contener trabajo valioso. Primero inspeccioná la base común, los cambios locales, el delta remoto y el ownership vigente. No borres un checkout confiable simplemente porque el diff resulte incómodo.

El starter incluye `tools/repo_delta.py` para inspección incremental acotada y `tools/workspace_gc.py` para limpieza controlada. Ninguna herramienta habilita a borrar código fuente, datos, artefactos aceptados, archivos humanos desconocidos o evidencia canónica. Empezá con inventario read-only y dry-run. El borrado requiere demostrar que el recurso pertenece al proceso correspondiente y es efectivamente descartable.

Mantené un checkout persistente por repositorio cuando sea posible. Los worktrees temporales se justifican por concurrencia real; los clones adicionales, caches grandes y copias duplicadas de evidencia no deben acumularse «por si acaso». A la vez, la higiene del disco no es excusa para destruir lineage, backups, registros de transacciones activas o artefactos que pueden ser necesarios para falsificar una capacidad.

Comandos destructivos como `git reset --hard`, reemplazos forzados de rama o borrados recursivos no son recetas generales de recuperación. Si realmente se necesita rollback, identificá objetivo, punto de restauración, datos afectados y autorización antes de actuar. Retroceder un commit Git no revierte automáticamente transacciones de la DB.

## 5. Un fallo repetido exige cambiar la causa

Repetir una orden con los mismos inputs, entorno e hipótesis casi nunca reduce el riesgo. Cuando reaparece la misma clase de fallo, I3 consolida observaciones, examina el subsistema y sus interfaces, fortalece las pruebas relevantes y solicita revisión independiente. Sigue siendo la misma campaña salvo una invalidación estratégica real.

El work order acotado define presupuestos, límites de reintento y condiciones de salida cuando hay costo relevante. Si varios intentos no entregan resultados, I3 cambia materialmente el método o registra el bloqueo causal preciso. El Planner no debería emitir una secuencia interminable de nuevas campañas para renombrar el mismo defecto. Tampoco se acepta el resultado solo porque una prueba unitaria pasó tras el último parche cuando el flujo físico continúa roto.

Un terminal útil puede consistir en una capacidad físicamente entregada con verificaciones pertinentes, un bloqueo preciso con evidencia y owner, o un checkpoint recuperable y una acción siguiente válida. Contar commits, horas o llamadas a modelos no reemplaza esos resultados.

## 6. Seguridad, privacidad y derechos de terceros

Un charter técnico no concede permiso implícito para exponer datos privados, consumir una API paga, divulgar credenciales, borrar registros protegidos o publicar contenido ajeno. Esas operaciones tienen límites de autoridad propios. Aplicá permisos mínimos, datos sintéticos en demostraciones no autorizadas, secretos gestionados por el entorno, tratamiento lícito de datos y verificación de licencias según el uso real.

- No coloques contraseñas, tokens, claves privadas ni cadenas de conexión en prompts, issues, historial Git o logs públicos.
- Usá datos ficticios o debidamente desidentificados en reviews y demos que no requieran datos personales reales.
- Antes de una migración o limpieza destructiva, determiná registros afectados y comprobá backup y restauración apropiados.
- Antes de publicar imágenes, código, música o video de terceros, verificá procedencia, licencia, atribución y alcance del uso. La licencia MIT del starter no cubre recursos ajenos.
- Antes de usar proveedores pagos, obtené un presupuesto autorizado y límites de reintento y costo. Un error de conexión no justifica llamadas ilimitadas.
- Antes de exponer la app a Internet, comprobá autenticación, autorización, configuración de red, datos, secretos y autorización de despliegue.

Privacidad, propiedad intelectual, seguridad y funcionamiento son gates relacionados pero distintos. Que una persona acepte el aspecto visual de un recurso no crea derechos para publicarlo. Que un test técnico pase no autoriza publicar datos personales. Conservá cada decisión con su owner competente.

## 7. Salir de un incidente con pruebas

El informe de recuperación explica qué falló, por qué, qué cambió, qué código y datos se conservaron o restauraron, qué pruebas físicas se ejecutaron y qué riesgos siguen abiertos. Identifica el candidato actual y el dueño de la próxima acción. I3 comprueba la reparación técnica; el Planner evalúa si la capacidad recuperó sus condiciones estratégicas.

Si el estado actual no puede reconstruirse o no existe un camino confiable para recuperar datos críticos, hay que decirlo. Un HOLD específico con un testigo faltante es preferible a fingir que el incidente terminó. Se puede continuar la investigación segura sin autorizar mutaciones sobre un estado incierto.

## 8. Tres incidentes completos y su recuperación

### Incidente A — La sesión del agente termina durante una campaña

El host se desconecta mientras se implementa búsqueda de socios. No envíes la misma petición abstracta a otra sesión aislada esperando que el trabajo sea equivalente. Inspeccioná el checkout real y sus cambios sin integrar, journal de campaña, último checkpoint, ownership y lease, recibos de efectos pendientes y candidato integrado.

Si la fuente y la autoridad concuerdan, I3 reanuda la misma campaña desde el siguiente paso permitido. Si falta una referencia crítica, registra el testigo exacto que se debe recuperar y mantiene HOLD para lo dependiente. Un límite de uso no agrega requisitos ni invalida automáticamente el charter.

### Incidente B — Se interrumpe una actualización de estado de varios archivos

Una transición iba a actualizar bootstrap, Product State, ownership y checkpoint, pero se corta a la mitad. Varios archivos podrían presentar versiones actuales incompatibles. El journal transaccional permite distinguir cambios aplicados, pendientes y conflictivos. Hay que inspeccionarlo antes de continuar escribiendo.

Utilizá la recuperación documentada de la herramienta responsable de la transición, por ejemplo `campaignctl recover` cuando corresponda al runtime de referencia. El mecanismo avanza solo si los hashes before/after justifican cada operación. Si otra persona editó el mismo archivo, el resultado puede ser `CONFLICT`. No borres el journal ni edites estados a mano para quitar el HOLD.

### Incidente C — Los tests pasan, pero la aplicación real falla

El cálculo de cuotas pasa pruebas unitarias, pero la pantalla muestra un importe anterior después de guardar. Registrá candidato, pasos, entorno, salida esperada y observada, y estado de DB. El gate unitario pasó; el gate end-to-end o de persistencia no. Ejecutá el recorrido afectado y repará el enlace entre UI, backend o estado compartido.

Si está en el charter vigente, I3 realiza la corrección, repite las pruebas físicas y de datos, integra un candidato nuevo y renueva la revisión pertinente. Repetir el mismo test unitario no prueba que se solucionó una sincronización de interfaz. La recuperación termina cuando el recorrido y las comprobaciones adyacentes afectadas realmente funcionan.

## 9. Matriz para operaciones sensibles

| Acción propuesta | Riesgo principal | Límite previo |
| --- | --- | --- |
| Mostrar una demo con fichas reales. | Exposición de datos personales. | Preferir datos ficticios; si es necesario, autorización, finalidad y protección adecuadas. |
| Crear un token de GitHub. | Acceso excesivo o filtración. | Permiso mínimo, secreto fuera del repo y revocación si se expone. |
| Borrar carpetas supuestamente temporales. | Pérdida de trabajo o evidencia. | Identidad del owner, descartabilidad y dry-run comprobados. |
| Publicar la aplicación en Internet. | Ataques, privacidad y gastos. | Autorización del CLIENT, preflight de seguridad/red y recuperación. |
| Activar una API paga. | Costos o reintentos sin límite. | Presupuesto, topes, medición y salida de error definida. |
| Publicar medios de terceros. | Uso sin derechos suficientes. | Fuente identificada, licencia y condiciones aplicables. |

Un «sí, podés trabajar en mi carpeta» no equivale a permiso para efectos irreversibles, externos o pagos. La ingeniería implementa controles; las decisiones reservadas de producto y exposición deben quedar explícitas.

## 10. Qué no demuestra una validación verde

`validate_project.py` puede comprobar coherencia estructural del control layer. No prueba que el backend responda, que la DB sobreviva a un reinicio, que los permisos de los endpoints sean correctos o que una persona pueda completar la tarea. Un test sintético de adopción no autoriza migrar una DB real sin comprobar ese caso. Una captura bonita tampoco reemplaza la interacción física.

Después de reparar un incidente, repetí el gate que falló y las comprobaciones cercanas que la corrección pudo afectar. Identificá el candidato y quién revisó su estado actual. No invalides toda la evidencia estable sin razón, pero tampoco promociones cambios materiales con reviews viejos. Cuando código, DB y Product State se contradicen, mantené HOLD para los efectos dependientes.

La distribución también tiene una frontera: un source build verde no prueba por sí solo el contenido, digest o disponibilidad de un ZIP ya publicado. El readback de la release comprueba el artefacto exacto y constituye un gate distinto.

## 11. Privacidad y feedback del starter

En v1.4, la configuración local del reportador de metadatos estrictos está habilitada por defecto. El instalador puede crear un workflow periódico en GitHub Actions. El paquete público no incluye un collector externo; el envío requiere los opt-ins explícitos documentados. Revisá la [política de feedback](../../../22_PRIVACY_PRESERVING_ARCHITECTURE_FEEDBACK.md) y cualquier workflow ejecutable antes de autorizar efectos de red.

`--no-feedback-workflow` evita instalar el programador, pero **no** apaga el generador local. Para desactivar toda generación, configurá `enabled=false` en el archivo de feedback instalado. No describas una opción como «sin telemetría» sin comprobar qué parte del mecanismo realmente desactiva.

Estas políticas del starter tampoco certifican que una aplicación desarrollada después trate correctamente sus propios datos personales. Cada producto debe revisar sus secretos, logs, flujos de datos, permisos, red y retención reales.

**Siguiente:** capítulo 06, Cierre y aceptación de capacidades.

## Fuentes y vigencia

- [Seguridad, privacidad, derechos y acciones externas](../../../../protocols/SECURITY_PRIVACY_RIGHTS_AND_EXTERNAL_ACTIONS.md)
- [Recuperación transaccional](../../../12_TRANSACTION_RECOVERY.md)
- [Feedback con privacidad](../../../22_PRIVACY_PRESERVING_ARCHITECTURE_FEEDBACK.md)
- [Preflight de gobierno existente](../../../32_EXISTING_GOVERNED_ATTACHMENT.md)
- [Implementación de transacciones](../../../../tools/state_tx.py)
- [Limpieza de workspaces](../../../../tools/workspace_gc.py)
- [Inspección incremental del repo](../../../../tools/repo_delta.py)

Estos incidentes son hipotéticos. Una recuperación real necesita evidencia directa del entorno afectado y autorización proporcional.
