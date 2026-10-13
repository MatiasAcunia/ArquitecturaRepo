# Agentic SDLC 1.2 — Estado e instalación

Estado: candidato en desarrollo, NO release v1.2.0.

La versión estable sigue siendo 1.1.0. La rama de desarrollo incorpora controles para Goals, planificación táctica I3, efectos externos ambiguos, consultas I4 opcionales y recuperación mutua de cinco tareas multiproyecto. Estas funciones necesitan integrarse y verificarse físicamente antes de presentarlas como automatización operativa completa.

## Feedback automático mínimo, activado por defecto

En proyectos nuevos se genera **una vez al mes** un informe de metadatos y se conserva como artifact en GitHub Actions del mismo proyecto. Sirve para mejorar la estructura del starter, ordenar categorías de fallos y simplificar instalación y recuperación.

Incluye versión y perfil, estados de validación, datos agregados de uso del mecanismo, cantidades de errores, reintentos, recuperaciones y bloqueos. No recopila código, contenido del proyecto, conversaciones, nombres de repositorios, rutas, identificadores persistentes, SHA ni credenciales.

**No se envía automáticamente al creador del starter** por el mero hecho de generarlo: ese envío necesita un receptor real y configuración/autorización informada. Nunca se inventa que llegó.

Para desactivarlo: cambiar enabled a false en .agentic-sdlc/feedback/ARCHITECTURE_FEEDBACK_CONFIG.json, borrar .github/workflows/agentic-sdlc-feedback.yml o generar el proyecto con --no-feedback-workflow. No afecta al funcionamiento del proyecto.

## Qué falta probar en Windows

El paquete de referencia correcto es **Codex Daily Control 2.0.2-hardening-candidate**. Antes de declarar soporte real se comprobarán en tu PC las operaciones Goal/Plan, reinicio, cuota, cierre diario, readback Drive, limpieza, entrega Gemini y rollback sin afectar proyectos ni conversaciones productivas.

Toda aceptación requiere código, tests y evidencia física. La prueba en esta rama es independiente de cualquier aceptación que hubiera tenido tu controlador Windows anterior.

Guía técnica completa: docs/23_OPERATIONAL_AGENTIC_SDLC_V1_2.md.
