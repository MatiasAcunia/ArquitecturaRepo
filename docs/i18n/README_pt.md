# Agentic SDLC — Guia inicial

Arquitetura reutilizável, baseada no repositório, para desenvolvimento de software com agentes. Oferece papéis, estado durável, planejamento, recuperação e verificação. Não constrói qualquer aplicativo automaticamente nem substitui decisões do responsável pelo produto.

## Instalar em um projeto

Escolha o menor perfil suficiente. Comece com descoberta somente leitura; não copie o Product State dos exemplos para um projeto real. Uma instalação nova começa em HOLD / UNTRUSTED_CONTEXT.

```bash
python tools/scaffold_project.py --target "../my-project" --profile SMALL --product-id EXAMPLE --language auto
```

## Papéis e autoridade

O CLIENT decide o produto e autoriza ações sensíveis; I2 define estratégia e aceitação; I3 executa engenharia e recuperação dentro da campanha; I4 é opcional para assistência limitada e revisão independente. Quatro papéis não exigem quatro processos.

## Privacidade e feedback mensal

Por padrão, novas instalações geram um relatório mensal mínimo de metadados nos artifacts do GitHub Actions do próprio projeto. Ele ajuda a melhorar a estrutura e organizar problemas. Não é enviado automaticamente ao mantenedor. Não inclui código, conversas, nomes de projetos, caminhos, identificadores ou credenciais.

Para desativar, altere enabled=false em .agentic-sdlc/feedback/ARCHITECTURE_FEEDBACK_CONFIG.json, remova .github/workflows/agentic-sdlc-feedback.yml ou instale com --no-feedback-workflow.

## Segurança e versões

A versão estável é 1.1.0. A 1.2 está em desenvolvimento: integrações reais com Codex Desktop Goal, Gemini, efeitos externos e tarefas multiprojeto exigem testes físicos. CI aprovada não equivale à aceitação do produto.

## Idiomas

O instalador detecta o idioma do sistema ou aceita --language pt. Os guias funcionam offline. O README principal do GitHub é estático: use os links para selecionar o idioma.

[FAQ](FAQ_pt.md) · [GitHub README](../../README.md)
