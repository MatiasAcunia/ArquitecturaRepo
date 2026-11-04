# Agentic SDLC — Guía de inicio

[Miniguía v1.4](MINI_GUIDE_es.md) · [FAQ](FAQ_es.md)

Arquitectura reutilizable, basada en el repositorio, para desarrollar software con agentes. Incluye roles, estado durable, planificación, recuperación y verificación. No construye automáticamente cualquier aplicación ni elimina las decisiones del dueño del producto.

## Instalar en un proyecto existente

Elegí el perfil más simple que alcance. Empezá con reconocimiento de solo lectura y no copies el Product State de los ejemplos a tu proyecto. Un scaffold nuevo comienza en HOLD / UNTRUSTED_CONTEXT.

```bash
python tools/scaffold_project.py --target "../my-project" --profile SMALL --product-id EXAMPLE --language auto
```

## Roles y autoridad

El CLIENT define el producto y autoriza acciones sensibles; I2 decide estrategia y aceptación; I3 realiza ingeniería y recuperación dentro del charter; I4 es opcional para consultas acotadas y evidencia independiente. Cuatro roles no implican cuatro procesos.

## Privacidad y feedback mensual

Los proyectos nuevos generan un informe mínimo de metadatos una vez al mes en los artifacts de GitHub Actions del propio proyecto. Viene activado por defecto para mejorar la estructura y clasificar errores. No se envía automáticamente al mantenedor. No incluye código, conversaciones, nombres de proyectos, rutas, identificadores ni credenciales.

Para desactivar todos los reportes, poné enabled=false en .agentic-sdlc/feedback/ARCHITECTURE_FEEDBACK_CONFIG.json. Borrar .github/workflows/agentic-sdlc-feedback.yml o instalar con --no-feedback-workflow desactiva solo la programación, no el generador local.

## Seguridad y versión

Este árbol de código corresponde a la versión 1.4.0. **Solo está publicada cuando existen la [release inmutable v1.4.0](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0), su ZIP y su checksum verificados**. La release anterior v1.3.0 sigue disponible. Para proyectos nuevos o sin gobierno previo, seguí la [guía de primera instalación v1.4](../46_V1_4_PUBLIC_START_AND_SUPPORT.md); para proyectos ya gobernados, usá el [preflight de solo lectura](../32_EXISTING_GOVERNED_ATTACHMENT.md), sin sobrescribir su estado. La CI portátil no certifica ejecución nativa de Codex Desktop, proveedores externos de IA ni efectos reales.

## Idiomas

El instalador detecta el idioma del sistema o acepta --language es, por ejemplo. La documentación funciona sin conexión. El README principal de GitHub es estático: elegí el idioma mediante los enlaces visibles.

[Miniguía v1.4](MINI_GUIDE_es.md) · [FAQ](FAQ_es.md) · [GitHub README](../../README.md)
