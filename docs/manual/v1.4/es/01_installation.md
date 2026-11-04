# 01 — Instalación y configuración

ArquitecturaRepo · Manual completo de uso · Edición v1.4 · Español

> Este capítulo explica la primera instalación y su separación de la adopción del proyecto real. Los comandos siguen la [guía pública v1.4.0](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md). Un scaffold creado correctamente **no** significa que la aplicación ya fue comprendida, adoptada, implementada o aceptada.

## Contenido del capítulo

1. Entorno y cuentas
2. Starter, fork y aplicación: tres ubicaciones distintas
3. Verificar rutas antes de escribir
4. Elegir un perfil proporcional
5. Crear el control layer
6. Validar sin inventar aceptación
7. La próxima acción es discovery, no programar
8. Antes de repetir una instalación
9. Del scaffold a una adopción real
10. Conexiones, permisos y privacidad
11. Diagnóstico seguro

## 1. Entorno y cuentas

Este recorrido utiliza Windows, PowerShell, Python y una copia local de ArquitecturaRepo. GitHub permite alojar el código, un asistente conversacional puede ayudar con planificación y un agente de programación puede trabajar en una carpeta autorizada. Ninguno de esos servicios comerciales es una dependencia universal del sistema. Si manejás Git por consola, no necesitás GitHub Desktop. Para usar agentes remotos tampoco necesitás una GPU dedicada en tu computadora.

Lo que sí necesitás es una ubicación de trabajo identificable, suficiente espacio en disco, acceso confiable a los archivos y permisos para instalar las herramientas elegidas. Antes de autorizar escrituras, comprobá qué repositorio contiene la aplicación que querés desarrollar y qué carpeta puede modificar el ejecutor. Un error común es abrir el starter genérico y empezar a programar ahí una función de una aplicación distinta. El starter y la aplicación tienen finalidades separadas y normalmente viven en repositorios diferentes.

Desde PowerShell, comprobá la disponibilidad de Python:

```powershell
& "python" --version
& "py" --version
```

Python 3.12 es la versión comprobada por la CI portable de v1.4. Si ninguno de los comandos funciona, instalá una versión compatible desde su distribuidor oficial, reiniciá la terminal y repetí la verificación. No uses instaladores de procedencia incierta. Si un comando termina con error, no supongas que tuvo éxito porque no mostró una ventana nueva. Las interfaces de GitHub, ChatGPT y los editores pueden cambiar; buscá la función necesaria y no dependas de la ubicación exacta de un botón.

Protegé tus cuentas con autenticación adecuada y permisos mínimos. No pegues contraseñas, claves privadas, tokens ni cadenas de conexión en prompts, commits o archivos públicos. Conectar un proveedor a ChatGPT no demuestra que el Planner haya visto el repo correcto, ni que el servicio tenga permiso para escribir sobre tu aplicación. La existencia de una herramienta y la autorización para usarla son asuntos distintos.

## 2. Starter, fork y aplicación: tres ubicaciones distintas

| Ubicación | Finalidad | Confusión que hay que evitar |
| --- | --- | --- |
| `ArquitecturaRepo/` | Código público de referencia, protocolos, plantillas, scripts y tests para crear un control layer. | No contiene por defecto tu aplicación ni su estado vigente. |
| Tu fork opcional | Copia propia del starter para mantener modificaciones o adaptaciones. | No equivale a crear un producto nuevo. |
| `club-app/` o el proyecto real | Código, datos, historial y control `.agentic-sdlc/` de la aplicación concreta. | No es un ejemplo descartable del framework. |

Los ejemplos del starter utilizan hechos sintéticos. Copiar su Product State a una aplicación real afirmaría requisitos, ref de código, ownership y decisiones que quizás nunca existieron. Por eso la instalación empieza de forma prudente, sin marcar automáticamente un estado adoptado.

Una organización sencilla de carpetas locales es:

```text
C:\Proyectos\
    ArquitecturaRepo\
    club-app\
```

Revisá el [README](../../../../README.md) y la [licencia MIT](../../../../LICENSE). Si querés adaptar el framework de forma independiente, podés mantener un fork; si no, alcanza con un checkout normal. La aplicación puede ser privada. Si ya tiene código, datos o historial, utilizá ese repositorio real en lugar de inventar otro «desde cero» para imitar el manual.

Para obtener una versión reproducible, elegí el [release v1.4.0](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0), que incluye ZIP portable, checksum y manifest. Verificá los bytes descargados. El branch `main` puede evolucionar con documentación nueva después de publicarse el paquete; lo que aparece en GitHub hoy no debe atribuirse retroactivamente al ZIP de la release.

## 3. Verificar rutas antes de escribir

Abrí PowerShell en la copia local del starter y ejecutá comandos de inspección:

```powershell
Get-Location
& "python" --version
& "git" status --short
```

Si Git informa que no estás dentro de un repositorio, revisá la ubicación. Si aparecen archivos modificados, no los descartes para obtener un árbol «limpio» sin investigar a quién pertenecen. Comprobá el destino que vas a pasar al instalador y no confundas la ruta actual de la terminal con la ruta donde querés crear `.agentic-sdlc/`.

Si utilizás GitHub Desktop, verificá qué repositorio está activo. Si utilizás Codex u otro agente, abrí la carpeta exacta de la aplicación y proporcioná la ubicación del starter como referencia de lectura hasta aclarar los permisos de instalación. Un agente autorizado puede realizar la adaptación, pero primero debe inspeccionar el destino y detectar si ya existe gobierno del proyecto.

Si encontrás un `.agentic-sdlc/` anterior, una campaña activa, Product State, historial real o una base de datos, detené la instalación genérica. No borres el proyecto para seguir el tutorial. Para una aplicación ya gobernada corresponde el [preflight de attachment de solo lectura](../../../32_EXISTING_GOVERNED_ATTACHMENT.md). Ese proceso preserva referencias y puede comprobar currentness, pero **no** es un actualizador automático de v1.2/v1.3 ni autoriza ejecución nueva.

## 4. Elegir un perfil proporcional

Los perfiles responden a riesgos y características del producto, no a cuántos agentes querés utilizar. Las seis familias están definidas en [profiles/profiles.json](../../../../profiles/profiles.json):

| Perfil | Cuándo considerarlo |
| --- | --- |
| `SMALL` | Un producto pequeño sin persistencia material ni riesgos que justifiquen controles adicionales. |
| `STATEFUL` | Datos persistentes, usuarios, cambios de esquema, recuperación, backups o runtime con estado. |
| `ARTIFACT_HEAVY` | Archivos numerosos o costosos, lineage, almacenamiento, ciclo de vida o derechos de uso. |
| `MULTI_WORKSTREAM` | Varias líneas de trabajo planificadas de forma independiente para un único producto final. |
| `MULTI_PRODUCT` | Productos distintos con recursos, políticas o infraestructura compartidos; puede justificar I1. |
| `HIGH_CONSEQUENCE` | Consecuencias materiales sobre privacidad, seguridad, integridad, finanzas o acciones irreversibles. |

`HIGH_CONSEQUENCE` no es una medalla de profesionalismo y `MULTI_PRODUCT` no obliga a contratar más servicios o multiplicar conversaciones. El perfil selecciona familias de controles; no crea hechos del proyecto ni permisos para publicar, gastar o procesar datos. Documentá qué características justifican la elección y revisala cuando cambien los riesgos verificados.

La aplicación ficticia del club se clasificaría razonablemente como `STATEFUL` porque conserva socios, cuotas y actividades. No necesita necesariamente un Master Owner separado ni una flota de agentes. Para un primer experimento realmente nuevo y sin gobierno previo, `SMALL` suele ser una base más proporcional. Elegí los mecanismos necesarios para el problema, no la arquitectura más grande disponible.

## 5. Crear el control layer

Desde la carpeta del starter v1.4, en PowerShell, podés crear un control para un proyecto nuevo. Revisá primero el destino:

```powershell
& "python" "tools\scaffold_project.py" --target "..\mi-proyecto" --profile "SMALL" --product-id "MI_PROYECTO" --objective "Objetivo inicial, pendiente de confirmación" --language "es" --no-feedback-workflow
```

Si se trata del club ficticio y el perfil `STATEFUL` está justificado:

```powershell
& "python" "tools\scaffold_project.py" --target "..\club-app" --profile "STATEFUL" --product-id "CLUB_MANAGER" --objective "Gestión de socios y cuotas de un club" --language "es" --no-feedback-workflow
```

Estos comandos son ejemplos de una sola línea; cambiá la ruta, el identificador y el objetivo según el proyecto concreto. El script crea `.agentic-sdlc/` dentro de la aplicación sin reescribir por defecto su código o sus workflows. Debe rechazar sobreescrituras de gobierno canónico existente. No uses opciones de fuerza como método rutinario de reparación.

El estado inicial esperado es `HOLD / UNTRUSTED_CONTEXT`. Significa que el framework no inventó los requisitos, los owners, el ref del código, la campaña ni la aceptación del producto. Es un resultado correcto. Cambiar manualmente el JSON a `READY` sería falsear la continuidad; todavía falta discovery y adopción.

El instalador puede ofrecer `--with-runtime` para agregar maquinaria de referencia de campañas. Esa opción no autentica proveedores, no inicia Codex Desktop y no crea permiso para ejecutar cualquier instrucción. La opción `--no-feedback-workflow` evita instalar el programador periódico de feedback, pero **no** desactiva por sí sola el generador local de metadatos. Su configuración es una decisión separada.

## 6. Validar sin inventar aceptación

Una vez creado el scaffold, entrá en la carpeta de la aplicación y usá los comandos vigentes de v1.4:

```powershell
& "python" -m pip install -r ".agentic-sdlc\requirements-validation.txt"
& "python" ".agentic-sdlc\tools\project_status.py" --control-root ".agentic-sdlc"
& "python" ".agentic-sdlc\tools\discover_project.py" --project-root "."
& "python" ".agentic-sdlc\tools\reconstruct_context.py" --root ".agentic-sdlc"
```

El primer comando instala dependencias locales de validación. `project_status.py` permite inspeccionar el estado inicial; `discover_project.py` inventaría metadatos y hashes de archivos sin copiar su contenido a un servicio remoto; `reconstruct_context.py` comprueba qué estado puede recuperar un trabajador nuevo desde las superficies durables. La discovery rechaza enlaces a archivos externos a la carpeta objetivo y destinos vinculados que no cumplen su contrato.

Es posible que la reconstrucción termine en HOLD porque aún no se adoptó un baseline confirmado. Ese estado puede ser el resultado correcto: la herramienta debe explicar qué evidencia falta, no inventarla. Los validadores de contratos no comprueban por sí solos que la aplicación abra, que una cuota se guarde en una DB real o que el usuario entienda la interfaz.

Verificá tres hechos: existe el control layer en la ruta prevista; los archivos y workflows anteriores de la aplicación permanecen intactos; los resultados de estado, inventario y reconstrucción son accesibles sin depender del chat. Conservá los mensajes de error. Si falta `jsonschema`, instalá las dependencias declaradas en vez de editar Product State o recrear el repositorio.

El resultado de esta etapa es **control inicial instalado e inspeccionado**, no «aplicación adoptada». La adopción exige evidencias del proyecto real y la confirmación de los requisitos por su dueño.

## 7. La próxima acción es discovery, no programar

Seguí las instrucciones de [instalación y adaptación](../../../../prompts/INSTALL_THIS_SDLC.md), la [sesión de descubrimiento del producto](../../../../prompts/PRODUCT_DISCOVERY_SESSION.md) y el [contrato de transferencia y adopción](../../../16_TRANSFER_ADOPTION.md). Para una aplicación anterior sin el mismo baseline también puede importar el [prompt de reanclaje](../../../../prompts/REANCHOR_EXISTING_PROJECT.md).

El Planner identifica qué hace el código actual, qué quiere cambiar el CLIENT, cuáles son los datos y el entorno relevantes, quién tiene autoridad y qué preguntas siguen abiertas. Una campaña material debe esperar un baseline adoptado y un charter explícito. Programar apenas aparece `.agentic-sdlc/` saltearía el paso que conecta el sistema con la verdad del proyecto.

## 8. Antes de repetir una instalación

Si `.agentic-sdlc/` ya existe, investigá su contenido antes de reintentar. Puede conservar el Product State canónico, ownership, una campaña vigente, referencias a la DB, lease o evidencia imprescindible. Una segunda instalación que parece funcionar puede destruir continuidad si reemplaza esas superficies.

Ante un error, no empieces por borrar, forzar ni reclonar. Clasificá si el problema se debe a entorno, ruta, dependencia, contrato, versión, currentness o control canónico preexistente. Conservá la salida completa y dirigí la corrección a su owner técnico. Un repositorio ya gobernado requiere attachment read-only y una migración evaluada por separado, no el scaffold genérico.

## 9. Del scaffold a una adopción real

Una secuencia razonable de adopción tiene pasos distintos:

1. Investigar aplicación y entorno reales, inicialmente de solo lectura.
2. Confirmar con el CLIENT los requisitos y exclusiones actuales.
3. Registrar un baseline de producto y un baseline técnico vinculados al código comprobado.
4. Elaborar un plan con hitos, fechas y condiciones observables de terminado.
5. Preparar una especificación explícita de adopción y comprobar preflight.
6. Promover registros de estado y ownership de manera coherente y recuperable.
7. Validar el resultado y demostrar reconstrucción desde contexto fresco.
8. Autorizar recién entonces una capacidad material mediante su charter.

La guía de [adopción](../../../16_TRANSFER_ADOPTION.md) detalla esa transición. Un agente no debería inventar un JSON, un SHA, un Goal activo ni una aprobación para obtener un informe verde. Cuando falta una decisión de producto, responde el CLIENT. Cuando falta evidencia técnica, el dueño de ingeniería investiga y demuestra el resultado. El CLIENT puede actuar como interlocutor y aprobador sin tener que reconciliar a mano los registros internos.

## 10. Conexiones, permisos y privacidad

Podés conectar GitHub u otro servicio para facilitar lecturas. Concedé el alcance mínimo necesario y verificá la rama y el repositorio concretos. Una sesión autenticada no prueba que el agente vea toda la evidencia o que tenga el permiso correcto. Antes de escrituras, revisá carpeta, worktree, permisos y charter aplicable.

Las comprobaciones locales reversibles son distintas de publicar, desplegar, enviar mensajes, comprar llamadas de API, borrar datos o compartir información privada. Estos efectos requieren autorización específica, alcance definido y una evaluación proporcional. No guardes secretos en prompts o repositorios públicos. Una aplicación construida con este starter puede conservar su código y datos privados.

En v1.4 la configuración del generador local de feedback de metadatos estrictos está habilitada por defecto; no se incluye un collector externo en el paquete público. El parámetro `--no-feedback-workflow` desactiva el programador de GitHub Actions, no el generador local. Para desactivar completamente la generación, establecé `enabled=false` en la configuración instalada. Consultá la [política de privacidad y feedback](../../../22_PRIVACY_PRESERVING_ARCHITECTURE_FEEDBACK.md) antes de habilitar cualquier envío o aceptar cambios en workflows ejecutables.

## 11. Diagnóstico seguro

| Observación | Interpretación prudente | Próxima comprobación |
| --- | --- | --- |
| Python no se reconoce. | La terminal no localiza el intérprete. | Revisar instalación y ruta; no tocar la app. |
| Falta `.agentic-sdlc/`. | La creación falló o apuntó a otra carpeta. | Comparar ruta objetivo y salida del instalador. |
| `HOLD / UNTRUSTED_CONTEXT`. | Hay scaffold pero faltan hechos confirmados del producto. | Seguir con discovery y adopción. |
| Falta `jsonschema`. | No se instalaron las dependencias del intérprete actual. | Instalar requirements y volver a inspeccionar. |
| Se preservó un control existente. | El instalador protegió gobierno canónico. | Usar el preflight read-only correspondiente. |
| Falló validación o reconstrucción. | Puede existir conflicto estructural, de fuente o autoridad. | Conservar el informe y reparar la causa comprobada. |
| El agente ve otro repositorio. | Su alcance operativo apunta a otra carpeta. | Detener escrituras y confirmar worktree y permisos. |
| Tests verdes pero la app no abre. | Las pruebas del control no cubrieron comportamiento físico. | Ejecutar la aplicación real y probar el recorrido del usuario. |

El cierre de este capítulo es un control layer inicial cuyo estado y límites se pueden inspeccionar. Su adaptación a requisitos, código, DB y autoridad reales constituye un trabajo distinto. El capítulo 02 explica esa frontera.

**Siguiente:** capítulo 02, El Planner y la adopción.

## Fuentes y vigencia

- [GitHub Release v1.4.0](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0)
- [Inicio público y soporte comprobado](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md)
- [Notas de release y actualización](../../../47_V1_4_RELEASE_NOTES_AND_UPGRADE.md)
- [Fork y bootstrap](../../../01_FORK_AND_BOOTSTRAP.md)
- [Transferencia y adopción](../../../16_TRANSFER_ADOPTION.md)
- [Attachment de proyectos gobernados](../../../32_EXISTING_GOVERNED_ATTACHMENT.md)
- [Validación ejecutable](../../../10_EXECUTABLE_VALIDATION.md)
- [Privacidad del feedback](../../../22_PRIVACY_PRESERVING_ARCHITECTURE_FEEDBACK.md)
- [Código del instalador](../../../../tools/scaffold_project.py)

Las instrucciones corresponden al starter o a ejemplos ficticios. No prueban que un proyecto concreto esté instalado, adoptado o aceptado.
