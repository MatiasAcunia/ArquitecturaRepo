# Agentic SDLC — Guia inicial

[Miniguia v1.4](MINI_GUIDE_pt.md) · [FAQ](FAQ_pt.md)

O [manual completo v1.4 em português, com oito capítulos](https://github.com/MatiasAcunia/ArquitecturaRepo/blob/main/docs/manual/v1.4/pt/README.md) está disponível no repositório de origem, com um [PDF de 57 páginas](https://github.com/MatiasAcunia/ArquitecturaRepo/blob/main/output/pdf/ArquitecturaRepo_Manual_Completo_v1.4_PT.pdf). O [livro espanhol histórico v1.3](https://github.com/MatiasAcunia/ArquitecturaRepo/blob/main/docs/manual/ES/README.md) continua disponível separadamente. A edição extensa não é copiada para a instalação local v1.4.0, cujo ZIP foi publicado anteriormente. Este guia é uma introdução breve e não substitui o livro; consulte o [guia de instalação v1.4](../46_V1_4_PUBLIC_START_AND_SUPPORT.md) para comandos atuais.

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

Para desativar todos os relatórios, defina enabled=false em .agentic-sdlc/feedback/ARCHITECTURE_FEEDBACK_CONFIG.json. Remover .github/workflows/agentic-sdlc-feedback.yml ou usar --no-feedback-workflow desativa somente o agendamento, não o gerador local.

## Segurança e versões

**A v1.4.0 já foi publicada** como [release versionada com ZIP portátil e checksum SHA-256](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0). Confira os arquivos baixados antes da instalação; a branch `main` pode incluir alterações posteriores de documentação e não é o artefato publicado. A release anterior v1.3.0 continua disponível. Projetos novos ou sem governança podem seguir o [guia de primeira instalação v1.4](../46_V1_4_PUBLIC_START_AND_SUPPORT.md); projetos já governados exigem uma [verificação somente leitura](../32_EXISTING_GOVERNED_ATTACHMENT.md), sem sobrescrever o estado existente. A CI portátil não certifica execução nativa do Codex Desktop, provedores externos de IA ou efeitos reais.

## Idiomas

O instalador detecta o idioma do sistema ou aceita --language pt. Os guias funcionam offline. O README principal do GitHub é estático: use os links para selecionar o idioma.

[Miniguia v1.4](MINI_GUIDE_pt.md) · [FAQ](FAQ_pt.md) · [GitHub README](../../README.md)
