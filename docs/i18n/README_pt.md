# Agentic SDLC — Guia inicial

[Manual prático v1.4 (oito temas)](MANUAL_pt.md) · [FAQ](FAQ_pt.md)

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

Este código-fonte está na versão 1.4.0. **A versão só está publicada quando a [release imutável v1.4.0](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0), seu ZIP e checksum verificados existirem**. A release anterior v1.3.0 continua disponível. Projetos novos ou sem governança podem seguir o [guia de primeira instalação v1.4](../46_V1_4_PUBLIC_START_AND_SUPPORT.md); projetos já governados exigem uma [verificação somente leitura](../32_EXISTING_GOVERNED_ATTACHMENT.md), sem sobrescrever o estado existente. A CI portátil não certifica execução nativa do Codex Desktop, provedores externos de IA ou efeitos reais.

## Idiomas

O instalador detecta o idioma do sistema ou aceita --language pt. Os guias funcionam offline. O README principal do GitHub é estático: use os links para selecionar o idioma.

[Manual prático v1.4](MANUAL_pt.md) · [FAQ](FAQ_pt.md) · [GitHub README](../../README.md)
