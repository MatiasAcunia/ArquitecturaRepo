# 01 — Instalación | ArquitecturaRepo v1.3.0

> Manual de uso revisado para el release público v1.3.0 (17 de octubre de 2026). Conserva el contenido textual del manual original 00–07 de septiembre de 2026 con correcciones específicas. La fuente era un PDF ilustrado: los pies de figura se conservan pero esta transcripción Markdown no reproduce las imágenes. No utilizar las cifras de página como referencia del archivo renderizado.

## Actualización comprobada para v1.3.0

La fuente canónica pública es el tag `v1.3.0`. El instalador sigue siendo `tools/scaffold_project.py` y requiere destino, perfil e identificador. En un directorio nuevo y sin gobierno previo, el comando base es:

```powershell
& "python" "tools\scaffold_project.py" --target "..\mi-proyecto" --profile "SMALL" --product-id "mi-proyecto" --language "es" --no-feedback-workflow
```

Como alternativa mediante GitHub Packages, después de instalar Docker y montar una carpeta vacía:

```powershell
docker run --rm -v "${PWD}:/workspace" ghcr.io/matiasacunia/arquitecturarepo:1.3.0 --target "/workspace/mi-proyecto" --profile "SMALL" --product-id "mi-proyecto" --language "es" --no-feedback-workflow
```

- `--with-runtime` es opcional; no presupongas que inicia Codex ni proporciona el API nativo de Goals.
- Una instalación nueva comienza en HOLD/UNTRUSTED_CONTEXT. Requiere discovery, requisitos y autoridad antes de producir cambios.
- En repositorios existentes ya gobernados (incluido v1.2), **no** ejecutes el scaffold encima de su Product State. Usá el preflight read-only y una migración evaluada aparte.
- `--no-feedback-workflow` impide instalar la automatización periódica; la configuración local de feedback y su consentimiento son cuestiones distintas.

## Contenido del manual conservado

### Página 8 de la edición original

A R Q U I T E C T U RA R E P O / C O L E C C I Ó N D E U S O




01
Instalación y
configuración

Del starter genérico a un control layer verificable




Matías Acuña · ArquitecturaRepo                                Revisión de compatibilidad: 17 de octubre de 2026

### Página 9 de la edición original

Contenido

    • 1. Entorno y cuentas                                • 7. Próxima acción: discovery, no programación
    • 2. Starter y aplicación: dos cosas diferentes       • 8. Antes de repetir una instalación
    • 3. Confirmar la carpeta antes de tocar archivos     • 9. Después del scaffold: descubrimiento y adopción
    • 4. Elegir un perfil proporcional                    • 10. Conexiones y permisos: mínimo necesario
    • 5. Crear el scaffold                                • 11. Diagnóstico rápido sin borrar nada
    • 6. Validación inicial sin inventar aceptación




1. Entorno y cuentas

Este ejemplo utiliza Windows, Python y una copia local del starter. GitHub, ChatGPT y Codex pueden
facilitar el trabajo, pero no son requisitos técnicos universales de la arquitectura. GitHub Desktop facilita
el primer clonado; una persona con experiencia puede hacerlo desde Git. No necesitás GPU dedicada
para usar agentes remotos. Sí necesitás espacio de disco, conexión estable y permisos para instalar las
herramientas elegidas.

Antes de instalar nada en el proyecto, comprobá que conocés qué carpeta abrirá Codex y qué repositorio
alojará tu aplicación. No copies tokens en prompts ni los guardes en archivos del repositorio. Activá las
protecciones de acceso que correspondan a tus cuentas.

Verificación mínima de Python. Abrí PowerShell y ejecutá uno de estos comandos. Si ambos fallan,
instalá una versión compatible de Python desde su sitio oficial y reiniciá la terminal.


  & "python" --version
  & "py" --version


Los ejemplos suponen que Python está disponible en la terminal. Si no lo está, corregí el entorno antes de
ejecutar herramientas del starter. No ejecutes instaladores de procedencia incierta. Las interfaces de
ChatGPT, Codex y GitHub pueden cambiar de ubicación; identificá la función, no un botón por su color.


2. Starter y aplicación: dos cosas diferentes

Tres ubicaciones que no deben confundirse
ArquitecturaRepo es el repositorio de referencia. Tu fork es una copia donde podés mantener o adaptar
ese starter. La aplicación que querés desarrollar vive en su propio repositorio o carpeta de proyecto
y recibe allí su control layer .agentic-sdlc/ . Un script ejecutado desde una carpeta distinta puede
terminar instalando el control en el lugar equivocado sin que el nombre del comando lo advierta.

Antes de ejecutar el scaffold, comprobá el directorio de trabajo y el destino; si existe una app previa,
conservá sus archivos y registrá el ref actual. Un starter público puede incluir ejemplos sintéticos: jamás
copies ese Product State como si describiera tu base de datos, tu rama o un cliente real.

El starter es una plantilla genérica reutilizable. La aplicación es tu producto concreto. En este ejemplo
llamaremos club-app al segundo repositorio. Se pueden guardar en carpetas hermanas para que un
agente autorizado pueda leer el starter e instalar su control layer sin mezclar el código de una app con
las reglas genéricas.

### Página 10 de la edición original

Figura 3. De scaffold a adopción. Esquema explicativo; no acredita un proyecto de destino.



 1. Abrí ArquitecturaRepo en GitHub y revisá el README y la licencia MIT.
 2. Hacé un fork a tu cuenta si querés mantener una copia propia del starter. El fork no es tu aplicación.
 3. Creá el repositorio de la aplicación; puede ser privado. Si ya existe un proyecto real, usá ese
    repositorio y no fabriques uno nuevo para “empezar limpio”.
 4. Cloná el starter; identificá o creá por separado el repositorio de tu aplicación antes de instalar su
    control layer.


  C:\Proyectos\
    ArquitecturaRepo\
    club-app\


El código público del starter puede evolucionar. Registrá qué ref/versión utilizaste cuando instales; no
supongas que el README histórico siempre describe tu copia local.


3. Confirmar la carpeta antes de tocar archivos

Preflight antes de escribir
En Windows, abrí una terminal en tu copia local del starter y comprobá las rutas. Estos comandos son de
inspección; ninguno crea un proyecto ni borra datos:


  Get-Location
  python --version
  git status --short


Si git status responde que no hay repositorio, probablemente abriste la carpeta incorrecta. Si el árbol
tiene cambios locales, registralos antes de actualizar o clonar otra cosa. Elegí una ubicación de destino
que reconozcas y verificá que contenga la app correcta. Para un proyecto con historia, usa la guía de
reanclaje; no empieces por forzar una plantilla encima de estado existente.

En GitHub Desktop comprobá que el repositorio activo es club-app . En Codex abrí precisamente la
carpeta de tu proyecto, no la del starter. La instalación puede hacerla Codex mediante un mensaje
completo, pero primero debe leer el starter y examinar el proyecto objetivo en modo de lectura.

No borres un proyecto real para imitar el tutorial. Si club-app ya tiene archivos, base de datos o historial,
esos datos son evidencia que el proceso de adopción deberá respetar.

### Página 11 de la edición original

4. Elegir un perfil proporcional

No elijas el perfil por la cantidad de agentes
Elegí SMALL si la app tiene una frontera de producto simple y sus riesgos son acotados. Si posee datos
persistentes, migraciones o recuperación, el criterio que importa es STATEFUL , aunque solo la
programe un agente. Si produce archivos grandes, caros o sujetos a revisión de derechos, evaluá
ARTIFACT_HEAVY ; si separa workstreams planificados o productos independientes, analizá esas fronteras
antes de activar I1.

HIGH_CONSEQUENCE requiere controles adicionales porque una acción incorrecta puede producir
consecuencias materiales: no es una insignia de profesionalismo. Documentá qué riesgo justifica cada
módulo añadido. profiles/profiles.json define las familias públicas; un perfil no autoriza por sí solo
publicar, gastar ni leer secretos.




  Figura 4. Selección de perfil. Esquema explicativo; no acredita un proyecto de destino.



El starter ofrece SMALL , STATEFUL , ARTIFACT_HEAVY , MULTI_WORKSTREAM , MULTI_PRODUCT y HIGH_CONSEQUENCE . El
perfil instala familias de controles; no fabrica hechos del producto ni obliga a crear todos los roles por
separado.

Elegí                                                                  Cuando el proyecto presenta…

 SMALL                                                                 Un producto pequeño sin persistencia o riesgo material que
                                                                       justifique mecanismos adicionales.

 STATEFUL                                                              Datos persistentes, migraciones, usuarios, recuperación o
                                                                       runtime con estado.

 ARTIFACT_HEAVY                                                        Salidas numerosas o costosas, lineage, almacenamiento y
                                                                       ciclo de vida de artifacts.

 MULTI_WORKSTREAM                                                      Varias líneas de trabajo planificadas de manera independiente
                                                                       para un mismo producto.

 MULTI_PRODUCT                                                         Productos distintos con procesos y recursos compartidos;
                                                                       puede justificar I1.

 HIGH_CONSEQUENCE                                                      Impacto material en privacidad, seguridad, finanzas,
                                                                       integridad o acciones irreversibles.



El club del manual 07 usa STATEFUL porque debe conservar socios, pagos e inscripciones. No le agregues
Master Owner, Sentinel ni infraestructuras complejas solo por aparecer en un diagrama. El perfil puede
revisarse cuando aparezca una clase de fallo real.

### Página 12 de la edición original

5. Crear el scaffold

Ejecución guiada y resultado esperable
Ejecutá el comando desde el starter, con una ruta de destino revisada. En PowerShell podés escribirlo en
una sola línea, sin barras de continuación de Bash:


  & "python" "tools\scaffold_project.py" --target "..\mi-proyecto" --profile "SMALL" --product-id
  "PROYECTO_DEMO" --objective "Objetivo visible de mi aplicación"


El resultado es una estructura de control local; comienza deliberadamente en HOLD / UNTRUSTED_CONTEXT ,
sin campaña activa ni aceptación de producto. No edites esos estados a READY para que desaparezca la
advertencia. El siguiente trabajo es descubrir el proyecto y adoptar un baseline explícito. El script rechaza
sobrescribir un control existente salvo autorización expresa mediante --force ; no lo uses como primer
intento de recuperación.


  cd "C:\Proyectos\ArquitecturaRepo"
  & "python" "tools\scaffold_project.py" --target "..\club-app" --profile "STATEFUL" --product-id
  "CLUB_MANAGER" --objective "Sistema de gestión para un club."


El script crea el control layer dentro de la app. El estado esperado inmediatamente después es HOLD /
UNTRUSTED_CONTEXT : significa que la instalación se negó a inventar el código actual, las decisiones del
cliente o un trabajo ya autorizado. No marques “instalación de arquitectura terminada” en esta etapa.

El starter permite agregar --with-runtime , pero el Campaign Lead de referencia es opcional y requiere
una campaña autorizada, no un clic para automatizar todo. La instalación también puede incluir un
workflow de feedback semanal de metadatos; el envío externo está deshabilitado por defecto. Si no
querés ese workflow, el scaffolder ofrece --no-feedback-workflow (leer previamente sus efectos en el
README actual).


6. Validación inicial sin inventar aceptación

Dos resultados distintos que deben quedar anotados

  python "tools/validate_project.py" --root "../mi-proyecto/.agentic-sdlc"


Desde el proyecto, instalá las dependencias de validación indicadas por el scaffold. Después ejecutá el
validador local. Estas acciones comprueban contratos y relaciones; no comprueban el producto ni
sustituyen la adopción.


  cd "C:\Proyectos\club-app"
  & "python" -m pip install -r ".agentic-sdlc\requirements-validation.txt"
  & "python" ".agentic-sdlc\tools\validate_project.py" --root ".agentic-sdlc"


Si valida, comprobá que existe .agentic-sdlc , que tu aplicación no fue reemplazada y que el starter sigue
separado. Si falla, conservá el error completo. No edites JSON a ciegas ni reinicies el trabajo creando otra
carpeta. El responsable técnico debe diagnosticar si la ruta, la versión, un contrato o el estado de control
son la causa.

Punto de control: el resultado correcto aquí es scaffold creado y validado; proyecto todavía no
adoptado. La adopción exige lectura del producto, requisitos, baseline técnico, plan de entrega y
reconstrucción en contexto fresco.

### Página 13 de la edición original

7. Próxima acción: discovery, no programación

El siguiente paso está documentado en prompts/INSTALL_THIS_SDLC.md y prompts/
PRODUCT_DISCOVERY_SESSION.md : el Planner inspecciona el proyecto, consulta decisiones de producto y
presenta un baseline para confirmación del CLIENT. La adopción técnica se realiza después mediante una
especificación explícita y comprobaciones sobre el control layer. Para proyectos existentes puede ser
relevante prompts/REANCHOR_EXISTING_PROJECT.md .


8. Antes de repetir una instalación

Si ya existe .agentic-sdlc , no ejecutes --force para resolver un error. Primero determiná si contiene
estado actual, campañas, owners o evidencias que deban preservarse. Reinstalar sin esa comprobación
puede destruir continuidad. Un problema de validación se investiga en el control layer existente, no se
oculta recreándolo.


9. Después del scaffold: descubrimiento y adopción

Un scaffold coloca infraestructura de control genérica; el sistema todavía desconoce qué código y datos
son actuales. La instalación no queda lista para una campaña hasta completar una secuencia distinta:
descubrimiento de solo lectura, definición del alcance por el CLIENT, baseline de requisitos, baseline
técnico y plan de entrega, especificación explícita de adopción, preflight, promoción coherente, validación
y prueba de contexto fresco.

El repositorio proporciona prompts/INSTALL_THIS_SDLC.md para encargar esa adaptación a un agente que
tenga acceso real al proyecto. También describe el recorrido en docs/16_TRANSFER_ADOPTION.md . No le
dictes al agente un JSON inventado ni le pidas que marque READY porque “ya instaló todo”: debe
reconstruir el proyecto y registrar solo hechos verificables.

Si un agente propone empezar a programar una feature inmediatamente después de crear la carpeta,
falta la parte decisiva. Pedile que informe la primera condición sin cumplir: requisitos, estado actual,
referencias de código, entorno, permisos, evidencia o charter. Cuando la falta sea una decisión de
producto, respondés vos; cuando sea técnica, el agente debe resolverla y mostrarte el efecto.


10. Conexiones y permisos: mínimo necesario

La conexión de GitHub a ChatGPT, cuando se usa, sirve para facilitar lectura de archivos y estado; su
presencia no demuestra que el Planner haya leído el repositorio correcto ni que pueda ejecutar código.
Empezá con acceso de lectura limitado al repo de trabajo. Codex, en cambio, necesita conocer la carpeta
de trabajo donde está autorizado a operar. Revisá que no esté abierto por error el directorio del starter
genérico ni un proyecto que contenga información privada ajena al encargo.

No concedas autorizaciones globales “por si acaso”. Operaciones que publican, gastan dinero, revelan
secretos, eliminan archivos fuera del entorno de trabajo o modifican servicios externos requieren una
autorización concreta y un alcance entendible. Un comando de prueba local y reversible no es
equivalente a desplegar la app en Internet.

La versión pública del starter puede instalar un workflow de feedback. Su modo predeterminado genera
metadatos como artefacto de GitHub Actions; el envío externo está desactivado hasta la doble
autorización definida en la documentación. Si no querés generación periódica, podés pedir el scaffold con
--no-feedback-workflow o desactivarla después. Revisá cualquier cambio a workflows ejecutables antes de
aceptarlo.

### Página 14 de la edición original

11. Diagnóstico rápido sin borrar nada

Observación                           Interpretación segura                     Próxima comprobación

No se reconoce Python.                El entorno local no encuentra el          Revisar instalación y ruta; no tocar la
                                      ejecutable.                               app.

No existe .agentic-sdlc .             No se creó el scaffold en esa carpeta.    Confirmar carpeta objetivo y salida del
                                                                                comando.

 HOLD / UNTRUSTED_CONTEXT .           Se creó la plantilla pero aún no se       Seguir con discovery y adoption.
                                      reconstruyó el producto.

El validador falla.                   Hay una inconsistencia estructural o de   Conservar el informe y reparar la causa
                                      referencias.                              en el control layer.

Codex ve otro repo.                   El contexto de ejecución apunta a otro    Detener escrituras y verificar proyecto y
                                      directorio.                               permisos.

El informe dice PASS pero la app no   La validación genérica no cubre           Ejecutar la app y comprobar el flujo de
abre.                                 funcionalidad física.                     producto.



El resultado de esta etapa es un control layer inicial cuya estructura puede validarse. Su adaptación al
proyecto real sigue pendiente. La adopción completa se explica en el manual 02: la diferencia entre
ambos estados es una de las protecciones centrales del sistema.

Continuar con: Manual 02, configurar el Planner y adoptar el proyecto.

Referencias de esta edición
Fuente: repositorio público ArquitecturaRepo en el commit 9c00e19b74d1 . Rutas verificadas:

  • README.md
  • prompts/INSTALL_THIS_SDLC.md
  • docs/01_FORK_AND_BOOTSTRAP.md
  • docs/10_EXECUTABLE_VALIDATION.md
  • docs/16_TRANSFER_ADOPTION.md
  • docs/22_PRIVACY_PRESERVING_ARCHITECTURE_FEEDBACK.md
  • tools/scaffold_project.py
  • tools/validate_project.py

Las instrucciones de este volumen describen el starter y un procedimiento de uso. Ninguna prueba de los
ejemplos sustituye la verificación del proyecto de destino.
