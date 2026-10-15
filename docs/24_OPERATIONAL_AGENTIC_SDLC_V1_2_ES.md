# Agentic SDLC v1.2.0 — Estado, instalación y límites

**Estado:** v1.2.0 es la última release pública publicada. Este documento sustituye el resumen previo de candidatura, que afirmaba incorrectamente que v1.1 era la última versión estable. No constituye un nuevo gate de aceptación ni prueba de ejecución nativa de agentes.

La versión portátil incluye mecanismos de Goal/Plan y campañas, validación y currentness, recuperación de estado, registro de artefactos y controles de privacidad. Las operaciones realmente disponibles se verifican mediante el código y la matriz de soporte de la versión instalada.

## Privacidad y feedback opcional

En proyectos nuevos, el scaffold puede generar un informe mensual de **metadatos limitados**, almacenado en artifacts de GitHub Actions del propio proyecto. El informe no debe incluir código, contenido de requisitos, conversaciones, identificadores privados ni credenciales. La generación local está habilitada de forma predeterminada, salvo que el usuario desactive el workflow.

El envío a un receptor externo sólo puede ocurrir cuando se configura expresamente un endpoint compatible; la preferencia implementada es opt-out, que debe mostrarse al usuario. No hay un colector mantenedor predeterminado empaquetado. Verificar la configuración real antes de afirmar que no salió información.

Para desactivar el workflow al instalar: `--no-feedback-workflow`. Después, desactivar la configuración local o retirar el workflow generado. Consultar [privacidad y feedback](22_PRIVACY_PRESERVING_ARCHITECTURE_FEEDBACK.md).

## Proveedores y agentes

ArquitecturaRepo no requiere OpenAI, Codex, Gemini, Claude ni otra plataforma. Las integraciones de host son módulos opcionales. Un preflight de Codex Daily Control es una verificación de paquete/configuración, no un ejecutor nativo. No corresponde afirmar soporte físico del host sin pruebas reales en la versión concreta.

El framework garantiza únicamente los contratos y las capacidades que puede demostrar; no garantiza que un modelo programe correctamente una aplicación.

## Nuevos y existentes

Usar el [README](../README.md) y la [guía de instalación](../prompts/INSTALL_THIS_SDLC.md). Para repositorios con gobierno existente, primero realizar un preflight no destructivo; no crear un segundo Product State ni asumir autorización de escritura.

Referencias: [capacidades v1.2](23_OPERATIONAL_AGENTIC_SDLC_V1_2.md) y [índice documental](README.md).
