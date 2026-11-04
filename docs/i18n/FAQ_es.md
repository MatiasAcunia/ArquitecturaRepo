# Agentic SDLC FAQ (es)

[ES guide](README_es.md) · [Miniguía v1.4](MINI_GUIDE_es.md) · [Main README](../../README.md)

### 1. ¿Qué es Agentic SDLC?

Es una arquitectura reutilizable para organizar desarrollo de software con agentes. No construye aplicaciones de manera completamente autónoma.

### 2. ¿Cómo empiezo?

Hacé un fork o inspeccioná el repositorio, empezá con reconocimiento de solo lectura, elegí el perfil mínimo y seguí el prompt de instalación. El scaffold inicial queda en HOLD.

### 3. ¿Puedo instalarlo sobre un proyecto existente?

Sí, pero primero hay que reconstruir código, datos y autoridad reales. Nunca se deben sobrescribir archivos de la aplicación ni copiar ejemplos como si fueran estado canónico.

### 4. ¿Los cuatro roles necesitan cuatro modelos?

No. CLIENT, Planner I2, Campaign Lead I3 y especialistas I4 describen responsabilidades, no una cantidad fija de procesos.

### 5. ¿Quién autoriza cambios sensibles?

El CLIENT conserva decisiones de producto, aceptación subjetiva, publicación, gasto y uso de datos sensibles. I3 no puede inventar esas autorizaciones.

### 6. ¿Ya funcionan automáticamente los Goals y Codex Desktop?

No automáticamente. v1.4 incluye controles portátiles de Goal, Plan y autoridad, pero la integración nativa de Codex Desktop/Goals en cada invocación necesita pruebas físicas separadas.

### 7. ¿Gemini es obligatorio o genera gastos por defecto?

No. I4 está desactivado hasta verificar consentimiento, credenciales, cuota y privacidad. No se envía código privado por defecto.

### 8. ¿Puede reiniciar o borrar mis chats de Codex?

No. El starter no reinicia, administra ni borra chats nativos de Codex. Cualquier adaptador del host exige autorización y evidencia independientes; v1.4 no certifica ese ciclo de vida.

### 9. ¿Qué feedback viene activado?

Un informe mínimo mensual de metadatos, guardado en los artifacts de GitHub Actions del propio proyecto. Sirve para mejorar el starter y ordenar información. No hay envío externo automático.

### 10. ¿Qué datos no incluye?

Código, conversaciones, nombres de proyectos o repositorios, rutas, credenciales, identificadores personales, requisitos, SHAs ni texto libre sin controlar.

### 11. ¿Cómo cambio de idioma o desactivo el feedback?

Usá --language auto|en|es|pt|fr|de|it|ja|zh; la documentación local sigue el idioma elegido. Para desactivar todo reporte, poné enabled=false en la configuración; --no-feedback-workflow solo desactiva la programación. El README de GitHub es estático.

### 12. ¿Qué está probado y cómo reporto errores?

**v1.4.0 está publicada** con [tag versionado, ZIP portátil y checksum SHA-256](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0); verificá los archivos descargados. `main` puede incluir documentación más reciente, mientras v1.3.0 sigue disponible como release anterior. Las pruebas portátiles en Linux/Windows no certifican hosts de agentes nativos ni usabilidad de terceros. Abrí un Issue con pasos reproducibles y logs sin secretos. El código original usa MIT; los derechos de terceros se evalúan aparte.

### 13. ¿Puedo combinar modos asíncrono, mixto, equipos y tareas de IA sin programación?

Sí, se combinan como dimensiones, sin crear agentes de más. Para ejecutar hacen falta scheduler/host real, ownership, recuperación y permisos comprobados; SMALL sigue simple. I2 guarda tu teoría y stack en el repositorio canónico. No se permiten commit ni branch mania. El feedback externo mínimo se prepara como opt-out cuando haya receptor verificado; hoy no existe receptor.

---

[ES guide](README_es.md) · [Miniguía v1.4](MINI_GUIDE_es.md)
