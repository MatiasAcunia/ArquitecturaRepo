# Ponte de continuidade de agentes — Agent Continuity Bridge 0.2.1

## Por que existe

ArquitecturaRepo coordena autoridade, planos e aceitação de engenharia. Este complemento opcional separa a integração com um controlador externo de continuidade de agentes, com versão independente. Não é um modelo de IA nem um segundo responsável pela campanha. O núcleo portátil funciona sem ele.

## O que funciona agora

Inspeciona offline um ZIP Codex Daily Control 3.1: valida caminhos, inventário, SHA-256, versão e configuração; registra o digest no projeto existente, verifica a identidade do pacote e remove apenas o registro próprio. Não distribui credenciais, configurações privadas, Goals nem dados de projetos.

## Requisitos e conexão

Python 3.10+; para registrar, projeto ArquitecturaRepo com diretório .agentic-sdlc; ZIP 3.1 obtido separadamente. O controlador nativo, se utilizado, requer Windows, PowerShell 5.1, Codex Desktop compatível e Git, SQLite e opcionais Drive/rclone configurados separadamente. A ponte não instala esses serviços.

## Segurança e limites

O controlador 3.1 é candidato a lançamento, sem validação física nativa. Fechamento, transferência de controle do Desktop, recuperação de cota e entrega remota continuam desabilitados/não verificados nesta ponte.

## CLI

```bash
python "bridge.py" inspect --package "CONTROLLER_3_1.zip"
python "bridge.py" install --project "MY_PROJECT" --package "CONTROLLER_3_1.zip"
python "bridge.py" status --project "MY_PROJECT" --package "CONTROLLER_3_1.zip"
python "bridge.py" uninstall --project "MY_PROJECT"
```


Instalação em projeto existente: `python install_into_project.py --project "PROJETO"`. Use `.agentic-sdlc/extensions/agent-continuity-bridge/pluginctl.py`; remova primeiro o registro e depois use `--remove`. Nenhuma ação nativa é executada.
