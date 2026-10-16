# Puente de continuidad de agentes — Agent Continuity Bridge 0.2.1

## Para qué existe

ArquitecturaRepo gestiona la autoridad, los planes y la aceptación del desarrollo. Este complemento opcional separa la integración con un controlador de continuidad externo y versionado. No es un modelo de IA, otro responsable de campañas ni un planificador obligatorio. El núcleo portable funciona sin él.

## Qué funciona actualmente

Inspecciona sin ejecutar un ZIP de Codex Daily Control 3.1: valida rutas, inventario, todos los SHA-256, versión y coherencia de la configuración; registra el hash del paquete en un proyecto existente, comprueba vigencia y retira el registro sin alterar el controlador. No incluye configuración privada, credenciales, Goals ni datos de proyectos.

## Requisitos y conexión

Python 3.10 o posterior; para instalar, un proyecto ArquitecturaRepo existente con directorio .agentic-sdlc; conseguir por separado el ZIP 3.1 propio. Ejecutar el controlador real en Windows requiere además PowerShell 5.1, Codex Desktop/app-server compatible y Git, SQLite y Drive/rclone cuando se configuren. Este complemento no instala ni conecta esos servicios.

## Seguridad y límites

El 3.1 sigue siendo candidato, sin aceptación física certificada. El cierre nativo, la cesión de Desktop, la reactivación por cuota y la entrega remota permanecen deshabilitados/no verificados. Comprobar el ZIP no autoriza ejecutar Goals.

## CLI

```bash
python "bridge.py" inspect --package "CONTROLLER_3_1.zip"
python "bridge.py" install --project "MY_PROJECT" --package "CONTROLLER_3_1.zip"
python "bridge.py" status --project "MY_PROJECT" --package "CONTROLLER_3_1.zip"
python "bridge.py" uninstall --project "MY_PROJECT"
```


Instalación dentro de un proyecto existente: `python install_into_project.py --project "PROYECTO_EXISTENTE"`. El comando queda en `.agentic-sdlc/extensions/agent-continuity-bridge/pluginctl.py`. Primero desregistrá el controlador y después ejecutá `--remove` para desinstalar el módulo. No se instala ni ejecuta Codex.
