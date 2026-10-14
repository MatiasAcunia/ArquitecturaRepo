# Agentic SDLC FAQ (es)

[ES guide](README_es.md) · [Main README](../../README.md)

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

Todavía no. v1.2 incorpora controles optativos de Goal y Plan, pero la integración física en cada invocación sigue pendiente de pruebas.

### 7. ¿Gemini es obligatorio o genera gastos por defecto?

No. I4 está desactivado hasta verificar consentimiento, credenciales, cuota y privacidad. No se envía código privado por defecto.

### 8. ¿Puede reiniciar o borrar mis chats de Codex?

El starter no lo hace. Codex Daily Control 2.0.2 es una referencia separada; su adaptador seguro aún no está aceptado en v1.2.

### 9. ¿Qué feedback viene activado?

Un informe mínimo mensual de metadatos, guardado en los artifacts de GitHub Actions del propio proyecto. Sirve para mejorar el starter y ordenar información. No hay envío externo automático.

### 10. ¿Qué datos no incluye?

Código, conversaciones, nombres de proyectos o repositorios, rutas, credenciales, identificadores personales, requisitos, SHAs ni texto libre sin controlar.

### 11. ¿Cómo cambio de idioma o desactivo el feedback?

Usá --language auto|en|es|pt|fr|de|it|ja|zh; la documentación local sigue el idioma elegido. Para el feedback, poné enabled=false en la configuración o usá --no-feedback-workflow. El README de GitHub es estático.

### 12. ¿Qué está probado y cómo reporto errores?

1.1.0 es estable; v1.2 sigue siendo una candidata hasta pasar pruebas físicas independientes. Abrí un Issue con pasos reproducibles y logs sin secretos. El código original usa MIT; los derechos de terceros se evalúan aparte.

### 13. ¿Puedo combinar modos asíncrono, mixto, equipos y tareas de IA sin programación?

Sí, se combinan como dimensiones, sin crear agentes de más. Para ejecutar hacen falta scheduler/host real, ownership, recuperación y permisos comprobados; SMALL sigue simple. I2 guarda tu teoría y stack en el repositorio canónico. No se permiten commit ni branch mania. El feedback externo mínimo se prepara como opt-out cuando haya receptor verificado; hoy no existe receptor.

---

[ES guide](README_es.md)
