# ArquitecturaRepo — Miniguía v1.4.0 (español)

Esta miniguía es para empezar a usar la versión **1.4.0** en un proyecto propio. Cubre los ocho temas 00–07 con un recorrido breve y ejecutable. **No es una traducción íntegra del manual histórico v1.3**: sus ocho capítulos completos se conservan en `docs/manual/ES/README.md` del repositorio fuente. Las afirmaciones de compatibilidad corresponden únicamente al alcance probado de la [release v1.4.0](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0). La v1.3.0 sigue disponible como versión anterior.

Esta miniguía se añadió a `main` **después** de publicar la release 1.4.0: el ZIP y el contenedor 1.4.0 originales no la incluyen. Está disponible en el repositorio actualizado; para distribuirla offline hará falta una publicación posterior con otra versión.

## 00 · Antes de empezar: qué hace y qué no hace

ArquitecturaRepo es una capa de control **local al repositorio**, no una aplicación que genere productos ni un sustituto de Codex. Conecta requisitos, decisiones, responsabilidades, estado actual, campañas, evidencias y recuperación para que otro agente o una sesión nueva pueda reconstruir qué está autorizado.

- CLIENT: decide el producto, confirma requisitos, aprueba acciones sensibles y acepta lo perceptual.
- I1: coordina el conjunto de proyectos cuando realmente hace falta.
- I2 Planner: reconstruye el producto, sus dependencias y riesgos; define capacidades y gates.
- I3 Controller: ejecuta y absorbe depuración, integración, pruebas y recuperación dentro de una campaña autorizada.
- I4: especialistas opcionales; **cuatro responsabilidades no requieren cuatro agentes ni cuatro chats**.

Podés conservar tu aplicación en un repositorio privado. El starter público no necesita recibir su código, su base de datos ni sus credenciales. El acceso real de los agentes a esos datos depende de las herramientas/proveedores que vos autorices; instalar este framework **no les concede permisos**.

## 01 · Instalación segura

Usá Python 3.12, versión probada en CI. Descargá el [ZIP portátil v1.4.0](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/download/v1.4.0/ArquitecturaRepo-v1.4.0-portable.zip), verificá el archivo `.sha256` publicado junto a él, extraelo y abrí una terminal en la carpeta extraída. También podés utilizar el código del tag `v1.4.0`. Si tu proyecto es nuevo o tiene código pero **no tiene un controlador canónico**, empezá con el perfil `SMALL`.

Bash, desde la carpeta del framework:

```bash
python "tools/scaffold_project.py" --target "../mi-proyecto" --profile SMALL --product-id MI_PROYECTO --objective "Objetivo inicial por confirmar" --language es --no-feedback-workflow
```

PowerShell, desde la misma carpeta:

```powershell
python "tools\scaffold_project.py" --target "..\mi-proyecto" --profile "SMALL" --product-id "MI_PROYECTO" --objective "Objetivo inicial por confirmar" --language "es" --no-feedback-workflow
```

El instalador coloca `.agentic-sdlc/` en el destino, conserva el código y los workflows existentes y rechaza sobrescribir un controlador previo. `--no-feedback-workflow` desactiva la programación del reporte mensual, **no** su generador local. Si no querés ningún reporte, poné `enabled=false` en `.agentic-sdlc/feedback/ARCHITECTURE_FEEDBACK_CONFIG.json`. No se incluye receptor externo.

Desde la **carpeta del proyecto destino**, ejecutá:

```bash
python -m pip install -r ".agentic-sdlc/requirements-validation.txt"
python ".agentic-sdlc/tools/project_status.py" --control-root ".agentic-sdlc"
python ".agentic-sdlc/tools/discover_project.py" --project-root "."
python ".agentic-sdlc/tools/reconstruct_context.py" --root ".agentic-sdlc"
```

En PowerShell, reemplazá `/` por `\` en las rutas entre comillas. Que el primer estado sea `HOLD / UNTRUSTED_CONTEXT` es **correcto**: todavía falta confirmar producto, línea base y autoridad.

¿Ya hay un Product State, actor, campaña o controlador del proyecto? **No ejecutes el scaffold encima**. Seguí el preflight de lectura de [gobierno existente](https://github.com/MatiasAcunia/ArquitecturaRepo/blob/v1.4.0/docs/32_EXISTING_GOVERNED_ATTACHMENT.md). No existe una migración automática universal desde v1.2/v1.3.

## 02 · Planner y adopción

Primero se reconstruye el código real, sus dependencias, datos, usuarios, límites de seguridad, objetivos y decisiones actuales; después el CLIENT valida requisitos y prioridades. I2 decide la arquitectura y escribe un charter de **capacidad** con límites, ownership, interfaces, condiciones de aceptación y falsificadores; no una lista interminable de microtareas.

Para un proyecto sin gobierno previo, utilizá el flujo de adopción existente. Para un proyecto ya gobernado, el preflight es solo lectura: nunca copies Product State sintético ni fabriques autorización a partir de un test exitoso.

## 03 · Operación diaria sin burocracia

Trabajá desde la intención del CLIENT, el estado CURRENT y la evidencia del repositorio. I3 organiza tareas dentro del charter, implementa, integra, prueba y recupera interrupciones. Los agentes pueden estar en un solo chat o en varios, según el riesgo y el trabajo. Una vez autorizado el charter, los bugs, reintentos y ajustes ordinarios vuelven **a la misma campaña**, no al Planner para inventar una nueva.

La recuperación de contexto debe comprobar Git, estado, autoridad y evidencias; si algo decisivo no concuerda, `HOLD` es una protección. No se supone integración nativa con Codex Desktop, Goals, proveedores de IA ni ejecución autónoma solo por instalar.

## 04 · Cómo pedir cambios

Describí **resultado observable**, contexto, restricciones y criterio de aceptación. Ejemplo: «En el CRUD de socios necesito consultar cuotas impagas por mes; no cambiar el esquema sin verificar migraciones; acepto cuando la consulta devuelve los casos correctos en pruebas y en pantalla». I2 decide si afecta el charter existente o exige una decisión material nueva. I3 resuelve el trabajo interno autorizado.

## 05 · Errores y recuperación

- `UNTRUSTED_CONTEXT`: falta reconstrucción y confirmación; no alteres manualmente un estado para que parezca aprobado.
- `ModuleNotFoundError: jsonschema`: instalá las dependencias del archivo `requirements-validation.txt` del destino.
- `EXISTING_CONTROL_PRESERVED` o conflicto de Product State: detente y usá la ruta de lectura; nunca fuerces ni borres el estado anterior.
- Git, base de datos SQLite/WAL, lease o identidad inconsistentes: frená acciones materiales hasta obtener evidencia coherente.
- Campaña interrumpida: conservá journals, identificadores y artefactos; recuperá dentro de la campaña autorizada. No borres muestras ni bases de datos sin ownership y un criterio verificable de limpieza.

El reporte de errores en Issues debe utilizar reproducciones genéricas y registros **anonimizados**: jamás publiques tokens, rutas personales, nombres privados, dumps, requisitos confidenciales ni conversaciones.

## 06 · Cierre de capacidades

No alcanza con que un agente diga «terminado». Revisá por separado: pruebas unitarias, integración, DB/currentness, semántica y generalización, ejecución física, evaluación humana/perceptual y, cuando corresponda, release. Guardá referencias exactas de código, entradas, resultados, responsables y estado aceptado. Los ejemplos sintéticos y el CI portátil no prueban que una app real funcione o esté lista para producción.

## 07 · Ejemplo guiado: club de socios

1. CLIENT pide registrar socios, cobrar cuotas y consultar deudas; acuerda los casos visibles de aceptación.
2. I2 inspecciona el repositorio y el esquema real; confirma si el club maneja cuotas mensuales, atrasos y permisos; identifica la capacidad mínima viable.
3. I3 implementa primero un recorrido vertical (alta de socio → cuota → consulta), agrega pruebas, verifica persistencia y mantiene el estado recuperable.
4. Ante un bug de cálculo, I3 corrige y vuelve a probar la **misma** capacidad; no crea campañas de corrección por defecto.
5. CLIENT prueba el flujo real y acepta o devuelve observaciones; las evidencias y la decisión quedan en las superficies canónicas del proyecto.

## Enlaces y límites de versión

- [Guía corta](README_es.md) · [FAQ en español](FAQ_es.md) · [README raíz](../../README.md).
- [Contrato de inicio, soporte y privacidad de v1.4](https://github.com/MatiasAcunia/ArquitecturaRepo/blob/v1.4.0/docs/46_V1_4_PUBLIC_START_AND_SUPPORT.md).
- [Release v1.4.0 y activos](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0).

Esta es una guía de uso público del código versionado, no un certificado de seguridad, host nativo, aceptación humana externa ni superioridad sobre Codex directo. La licencia MIT no concede derechos sobre material de terceros.
