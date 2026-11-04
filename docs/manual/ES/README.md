# Manual de ArquitecturaRepo v1.3.0 — Colección 00–07 (español)

> Edición **completa histórica de v1.3.0**, con ocho capítulos extensos. Para instalaciones actuales de v1.4.0, usá la [miniguía v1.4 en español](../../i18n/MINI_GUIDE_es.md) o [su índice de ocho idiomas](../../../README.md). Los comandos e imágenes de contenedor de abajo describen exclusivamente la versión antigua; **no** los tomes como la versión publicada más reciente. Las otras siete traducciones del manual extenso aún no están disponibles.

Guía pública para personas que quieren aplicar ArquitecturaRepo a un proyecto propio. Esta edición revisa el texto de la colección original del 22/09/2026 y solo modifica o añade las instrucciones necesarias para reflejar el release **v1.3.0** publicado el 17/10/2026.

**Fuente canónica del software**: [release v1.3.0](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.3.0), commit `9c00e19b74d1`. La rama `main` puede contener documentación y procesos posteriores, pero el paquete versionado se construye desde el tag.

## Si estás usando v1.4.0

No hay una edición extensa de v1.4 terminada ni una traducción completa de este manual a otros siete idiomas. Esta colección es útil para **entender el proceso**, pero tiene prioridad histórica: no garantiza que sus comandos, capturas ni rutas sigan siendo idénticos. Para instalar, ejecutar o determinar qué está soportado, consultá primero el [release v1.4.0](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0), la [guía de primer uso](../../46_V1_4_PUBLIC_START_AND_SUPPORT.md) y las [notas de compatibilidad](../../47_V1_4_RELEASE_NOTES_AND_UPGRADE.md).

| Capítulo extenso histórico | Referencia práctica para v1.4.0 |
| --- | --- |
| 00 · Antes de empezar | [Arquitectura y responsabilidades](../../00_ARCHITECTURE_OVERVIEW.md); [límites de soporte v1.4](../../46_V1_4_PUBLIC_START_AND_SUPPORT.md) |
| 01 · Instalación | [Instalación v1.4, perfiles y preflight](../../46_V1_4_PUBLIC_START_AND_SUPPORT.md); [release y actualizaciones](../../47_V1_4_RELEASE_NOTES_AND_UPGRADE.md) |
| 02 · Planner y adopción | [Descubrimiento y baseline](../../21_PRODUCT_DISCOVERY_REQUIREMENTS_STACK_AND_DELIVERY.md); [adopción](../../16_TRANSFER_ADOPTION.md) |
| 03 · Operación diaria | [Runtime de referencia](../../11_REFERENCE_RUNTIME.md); [ejecución orientada a resultados](../../44_OUTCOME_FIRST_AGENT_EXECUTION.md) |
| 04 · Solicitar cambios | [Modelo de roles y límites](../../00_ARCHITECTURE_OVERVIEW.md); [gobierno de cambios y fallos](../../04_FAILURE_MODES.md) |
| 05 · Errores y recuperación | [Transacciones y recuperación](../../12_TRANSACTION_RECOVERY.md); [adjuntar un proyecto ya gobernado](../../32_EXISTING_GOVERNED_ATTACHMENT.md) |
| 06 · Cierre de capacidades | [Gates y criterios de release](../../17_V1_RELEASE_GATES.md); [límites reales de v1.4](../../47_V1_4_RELEASE_NOTES_AND_UPGRADE.md) |
| 07 · Ejemplo guiado del club | [Ejemplo físico y transferencia](../../15_STATEFUL_REFERENCE_AND_TRANSFER.md); [miniguía actual en español](../../i18n/MINI_GUIDE_es.md) |

El código, los esquemas y el estado canónico de **tu proyecto** tienen prioridad sobre un ejemplo narrativo. Un instalador no autoriza un agente a programar ni a publicar. Si hay controladores, Product State o campañas preexistentes, conservá ese estado y usá la ruta de lectura antes de modificar nada.

## Guías

1. [00 · Antes de empezar](00_ANTES_DE_EMPEZAR_V1_3.md) — roles, límites, producto y autoridad.
2. [01 · Instalación](01_INSTALACION_V1_3.md) — preparar el proyecto, escoger perfil, instalar y comprobar.
3. [02 · El Planner y la adopción](02_PLANNER_Y_ADOPCION_V1_3.md) — discovery, baseline, charter y work orders.
4. [03 · Operación diaria](03_OPERACION_DIARIA_V1_3.md) — Goal, plan de I3, Codex, recuperación y entregas.
5. [04 · Solicitar cambios](04_SOLICITAR_CAMBIOS_V1_3.md) — expresar requisitos y gestionar nuevas decisiones.
6. [05 · Errores y recuperación](05_ERRORES_Y_RECUPERACION_V1_3.md) — incidentes, currentness, estado y limpieza segura.
7. [06 · Cierre de capacidades](06_CIERRE_DE_CAPACIDADES_V1_3.md) — gates, aceptación, evidencias y entregables.
8. [07 · Ejemplo guiado del club](07_EJEMPLO_GUIADO_CLUB_V1_3.md) — recorrido aplicado a un CRUD de socios y cuotas.

## Instalación mediante GitHub Packages (contenedor GHCR)

La imagen `ghcr.io/matiasacunia/arquitecturarepo:1.3.0` expone directamente `tools/scaffold_project.py`. Es un instalador; no es un servidor ni un agente autónomo.

En PowerShell, desde la carpeta donde querés crear el proyecto (Docker Desktop iniciado):

```powershell
docker run --rm -v "${PWD}:/workspace" "ghcr.io/matiasacunia/arquitecturarepo:1.3.0" --target "/workspace/mi-proyecto" --profile "SMALL" --product-id "mi-proyecto" --language "es" --no-feedback-workflow
```

En Bash:

```bash
docker run --rm -v "$(pwd):/workspace" ghcr.io/matiasacunia/arquitecturarepo:1.3.0 --target /workspace/mi-proyecto --profile SMALL --product-id mi-proyecto --language es --no-feedback-workflow
```

La imagen se publica desde [el workflow verificable de GitHub Actions](https://github.com/MatiasAcunia/ArquitecturaRepo/actions/workflows/publish-ghcr-package.yml). **GHCR puede iniciar con visibilidad privada: el propietario debe seleccionar Public en Package settings para garantizar descargas anónimas.** No confundir un push exitoso con confirmación de visibilidad pública.

Otra opción es descargar el [ZIP portable del Release](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/download/v1.3.0/ArquitecturaRepo-v1.3.0-portable.zip), descomprimirlo y ejecutar `python tools/scaffold_project.py --help`.

## Advertencias y alcance real

- Instalación nueva: comienza en **HOLD / UNTRUSTED_CONTEXT**. Ninguna operación supone una autorización de cambios.
- Si el proyecto ya tiene un controlador canónico, **no** superpongas otra instalación: primero ejecutá el preflight read-only de repositorio gobernado.
- El starter portable no garantiza que un modelo programe correctamente ni que el host Codex Desktop ofrezca un control nativo de Goal, `/plan` o permisos de escritura comprobados.
- Un resultado de tests del framework no equivale a aceptación perceptual del software construido.
- Este manual Markdown conserva el texto de la colección original y sus referencias de figura, pero **no contiene las imágenes de diagramas del PDF fuente**. Las notas de compatibilidad v1.3 al principio de cada capítulo son posteriores y separadas.
- La presencia del paquete GHCR en el panel lateral del repositorio depende de la vinculación y los ajustes de visibilidad del propio GitHub.

## Referencias

- [README del framework](../../../README.md)
- [Manual breve actual de v1.4.0 (español)](../../i18n/MINI_GUIDE_es.md)
- [Guía de instalación v1.4.0](../../46_V1_4_PUBLIC_START_AND_SUPPORT.md)
- [Scope v1.3 y soporte portable](../../42_V1_3_PORTABLE_SUPPORT_AND_RELEASE_GATES.md)
- [Notas oficiales v1.3](../../43_V1_3_RELEASE_NOTES_AND_UPGRADE.md)
- [Guía de instalación principal](../../../prompts/INSTALL_THIS_SDLC.md)
