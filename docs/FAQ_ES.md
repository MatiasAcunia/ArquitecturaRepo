# Preguntas frecuentes — ArquitecturaRepo

Una guía breve para quienes quieren **probar el starter en un proyecto real**. Esta página orienta la adopción; los contratos, herramientas y límites vigentes están documentados en el [README](../README.md) y en las guías técnicas enlazadas abajo.

## Empezar a usarlo

### 1. ¿Qué es ArquitecturaRepo?

Es un **starter experimental de Agentic SDLC**: protocolos, plantillas, contratos verificables y herramientas de referencia para organizar proyectos de software en los que trabajan agentes de IA. Busca mejorar la continuidad técnica, la distribución de responsabilidades y la verificación. **No es una aplicación que construya automáticamente cualquier producto.**

### 2. ¿Qué gano si lo adapto a mi proyecto?

La propuesta es dejar en el repositorio información recuperable: qué producto querés construir, qué requisitos y decisiones siguen vigentes, qué campaña está autorizada, qué evidencia respalda el estado declarado y qué corresponde hacer después. También separa quién decide el producto, quién planifica y quién ejecuta. El beneficio real debe comprobarse en cada adopción; no se garantiza por copiar archivos.

### 3. ¿Por dónde arranco?

La ruta recomendada está en [Quick Start](../README.md#quick-start):

1. Hacé un **fork** del repositorio.
2. Dale al agente que vaya a trabajar acceso al fork y a tu proyecto real.
3. Abrí y copiá las instrucciones de [`prompts/INSTALL_THIS_SDLC.md`](../prompts/INSTALL_THIS_SDLC.md).
4. Pedí que **primero inspeccione el proyecto sin modificarlo** y que elija la configuración mínima suficiente.
5. Confirmá los requisitos de producto que requieran tu decisión. Luego exigí validación y una prueba de reconstrucción desde un contexto nuevo antes de considerar instalada la arquitectura.

No interpretes un reporte de instalación como prueba de que la aplicación ya funciona.

### 4. ¿Y si mi proyecto ya tiene bastante código o historia?

Usá [`prompts/REANCHOR_EXISTING_PROJECT.md`](../prompts/REANCHOR_EXISTING_PROJECT.md) como punto de entrada. La adopción debe reconstruir primero el estado real, conservar los archivos existentes y registrar qué decisiones están vigentes. No hay que trasplantar un estado ficticio desde los ejemplos del starter.

### 5. ¿Tengo que crear cuatro agentes o cuatro chats?

**No.** I1–I4 son clases de responsabilidad, no una cantidad obligatoria de chats, sesiones o procesos. En un proyecto pequeño puede bastar un Planner y un ejecutor; el Master Owner separado es opcional cuando no existe una frontera compartida que gobernar. Empezá por [el perfil mínimo](05_MINIMUM_VIABLE_PROFILE.md) y [el árbol de adaptación](09_ADAPTATION_DECISION_TREE.md).

### 6. ¿Es obligatorio usar Windows, ChatGPT, Codex o alguna herramienta paga?

No como requisito universal de la arquitectura. Los recorridos ilustrativos pueden usar esas herramientas, pero el agente, el sistema operativo y los servicios se eligen según el proyecto. Las utilidades de referencia del starter incluyen scripts de Python. El código original del repositorio se distribuye bajo licencia MIT; **servicios externos, inferencia de modelos, infraestructura y almacenamiento pueden tener costes propios**.

### 7. ¿Puedo empezar sin que un agente modifique mi proyecto?

Sí. Podés inspeccionar el repositorio, hacer un fork y pedir descubrimiento de solo lectura antes de autorizar cambios. La opción de scaffold en el README crea una capa de control inicial en **`HOLD / UNTRUSTED_CONTEXT`**, sin atribuirle al proyecto un estado de aceptación que todavía no demostró.

## Cómo funciona

### 8. ¿Esto les da memoria permanente a los modelos?

No modifica la memoria interna de ningún modelo. La **continuidad** se apoya en requisitos, Product State, registros de estado, código y evidencia durables en el repositorio. Un contexto nuevo debe poder reconstruir la situación vigente a partir de esas fuentes. Hay una [prueba específica de contexto nuevo](07_FRESH_CONTEXT_TEST.md).

### 9. ¿Puedo limitarme a definir el producto y dejar que los agentes resuelvan lo técnico?

Es el objetivo de diseño, no una garantía de autonomía absoluta. La persona conserva decisiones de producto, prioridades, aceptación subjetiva y autorizaciones sensibles. La arquitectura asigna planificación, implementación, depuración, revisión y recuperación a responsables técnicos para evitar que tengas que coordinar cada bug o reconstruir el estado manualmente.

### 10. ¿Qué diferencia hay entre Planner y responsable de ejecución?

El **Planner (I2)** define estrategia, límites de capacidades y condiciones de aceptación. El **Campaign Lead / Execution Controller (I3)** gestiona implementación, pruebas, retries, integración y correcciones dentro de una campaña ya autorizada. Un fallo ordinario de test no debería provocar una campaña nueva. Ver [visión general](00_ARCHITECTURE_OVERVIEW.md) y [runtime de referencia](11_REFERENCE_RUNTIME.md).

### 11. ¿El controlador local ejecuta agentes automáticamente?

**No por sí solo.** `tools/campaignctl.py` es un controlador de campaña de referencia y opcional: mantiene estado, dependencias, checkpoints, autoridad de ejecución, reintentos y revisión. No lanza arbitrariamente agentes ni sustituye las integraciones propias del entorno. Ver [límites del runtime](11_REFERENCE_RUNTIME.md#limits).

### 12. ¿Qué pasa cuando falta información o hay estados contradictorios?

No se debería inventar continuidad. Un dato ausente es **UNKNOWN**; una contradicción material de autoridad o currentness requiere **HOLD** y reconciliación antes de la acción dependiente. Para los cambios críticos de estado hay mecanismos de transacción y recuperación. Ver [reconstrucción](07_FRESH_CONTEXT_TEST.md) y [recuperación](12_TRANSACTION_RECOVERY.md).

## Pruebas, seguridad y límites

### 13. ¿Qué está probado y qué no?

El starter tiene validaciones automatizadas, casos sintéticos de adopción de varios perfiles y una referencia física con SQLite. Es evidencia sobre **mecanismos del starter**, no una demostración de que cualquier aplicación real adoptada esté correcta. En tu proyecto siguen siendo necesarios sus propios tests, ejecución real, gates de seguridad y evaluación humana cuando corresponda. Ver [alcance de la evidencia](02_RESEARCH_BASIS_AND_LIMITS.md) y [gates de release](17_V1_RELEASE_GATES.md).

### 14. ¿Puedo usarlo en producción o con datos sensibles?

La licencia permite adaptar el código, pero **eso no certifica seguridad ni preparación para producción**. Evaluá autenticación, secretos, permisos, datos personales, backups, red, licencias de terceros y despliegue según tu caso. No entregues credenciales ni datos privados a agentes o issues públicos. Consultá también [la decisión de perfiles](09_ADAPTATION_DECISION_TREE.md).

### 15. ¿El starter envía información de mi proyecto a alguien?

La arquitectura no presupone que debas compartir el contenido del proyecto. En scaffolds nuevos, un workflow programado puede producir en **GitHub Actions** un reporte de metadatos estrictamente limitados y conservarlo como artifact; **el envío externo necesita un receptor HTTPS aprobado, todavía no configurado**; con receptor comprobado, v1.2 usará una preferencia opt-out, con aviso visible y desactivación antes del primer envío. La generación programada también se puede desactivar. No equivale a que el uso de modelos o servicios externos sea privado por definición: revisá los proveedores que elijas. Ver [configuración, contenido y opt-out](22_PRIVACY_PRESERVING_ARCHITECTURE_FEEDBACK.md).

## Documentación y colaboración

### 16. ¿Dónde encuentro una explicación más detallada?

El [README](../README.md) contiene el recorrido inicial, los perfiles y el mapa del repositorio. Las [guías técnicas](00_ARCHITECTURE_OVERVIEW.md) desarrollan arquitectura, adaptación, currentness, pruebas, ejecución y recuperación. Los ejemplos de `examples/` son **sintéticos**: sirven para estudiar los mecanismos, no para copiar un proyecto ajeno como si fuese tu estado actual.

### 17. ¿Cómo reporto un error o cuento qué me funcionó?

En la pestaña **Issues** del repositorio, abrí una incidencia y, si podés, incluí:

- Qué querías lograr y en qué tipo de proyecto.
- Qué perfil/ruta de instalación usaste.
- Pasos concretos para reproducir el problema.
- Resultado esperado y resultado observado.
- Versión del starter y mensajes de error **sin secretos ni información privada**.

También sirven experiencias de adopción: qué te aportó, qué te complicó y qué te parece innecesario. Eso ayuda a decidir mejoras a partir de uso real, no de promesas.

### 18. ¿Lo puedo modificar, compartir o incorporar a otro proyecto?

Sí: el código y la documentación originales se publican bajo [licencia MIT](../LICENSE), con las condiciones indicadas allí. El material de terceros no queda automáticamente cubierto por esa licencia.

### 19. ¿Qué modos y proyectos admite v1.2?

Podés describir proyectos CRUD, API, web, móviles, datos, automatización, videojuegos, infraestructura y tareas de IA no dedicadas a programación. La configuración es por dimensiones: síncrono/asíncrono/híbrido, solo/equipo y software/no-código/mixto. No habilita ejecución autónoma por sí sola; se exige host, autoridad, permisos, recovery y evidencia física. Consultá [modos y tecnología](27_PROJECT_MODES_AND_STACK_SELECTION.md).

### 20. ¿El feedback se envía automáticamente al mantenedor y cómo lo desactivo?

El informe mínimo mensual local está activado y queda en los artifacts de GitHub Actions del proyecto. La preferencia de envío al mantenedor es opt-out **cuando haya un receptor HTTPS aprobado**. Esta candidata todavía no tiene uno: no hay entrega central real que podamos afirmar. No incluye código, conversaciones, nombres, rutas, secretos ni texto libre. Para desactivar todo, poné `enabled=false`; para cortar sólo el envío, `external_submission_enabled=false`, o borrá el workflow. Más detalles en la [guía de privacidad](22_PRIVACY_PRESERVING_ARCHITECTURE_FEEDBACK.md).

---

**Ruta corta:** [README / Quick Start](../README.md#quick-start) → [prompt de instalación](../prompts/INSTALL_THIS_SDLC.md) → descubrimiento de solo lectura → adopción proporcional → validación + [fresh-context probe](07_FRESH_CONTEXT_TEST.md).

Este FAQ resume el punto de entrada; ante diferencias, prevalecen los archivos y contratos vigentes del repositorio.
