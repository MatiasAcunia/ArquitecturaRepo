# Manual de ArquitecturaRepo v1.3.0 — Colección 00–07 (español)

Guía pública para personas que quieren aplicar ArquitecturaRepo a un proyecto propio. Esta edición revisa el texto de la colección original del 22/09/2026 y solo modifica o añade las instrucciones necesarias para reflejar el release **v1.3.0** publicado el 17/10/2026.

**Fuente canónica del software**: [release v1.3.0](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.3.0), commit `9c00e19b74d19c741983987b9359cb5c2ac83c55`. La rama `main` puede contener documentación y procesos posteriores, pero el paquete versionado se construye desde el tag.

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
- [Scope v1.3 y soporte portable](../../42_V1_3_PORTABLE_SUPPORT_AND_RELEASE_GATES.md)
- [Notas oficiales v1.3](../../43_V1_3_RELEASE_NOTES_AND_UPGRADE.md)
- [Guía de instalación principal](../../../prompts/INSTALL_THIS_SDLC.md)
