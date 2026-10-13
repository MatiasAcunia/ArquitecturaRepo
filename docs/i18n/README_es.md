# Agentic SDLC — Guía de inicio

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

Para desactivarlo, poné enabled=false en .agentic-sdlc/feedback/ARCHITECTURE_FEEDBACK_CONFIG.json, borrá .github/workflows/agentic-sdlc-feedback.yml o instalá con --no-feedback-workflow.

## Seguridad y versión

La versión estable es 1.1.0. La 1.2 es candidata: la integración real con Codex Desktop Goal, Gemini, efectos externos y cinco tareas todavía necesita pruebas físicas. La CI verde no sustituye la aceptación del producto.

## Idiomas

El instalador detecta el idioma del sistema o acepta --language es, por ejemplo. La documentación funciona sin conexión. El README principal de GitHub es estático: elegí el idioma mediante los enlaces visibles.

[FAQ](FAQ_es.md) · [GitHub README](../../README.md)
