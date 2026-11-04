# ArquitecturaRepo — Miniguia v1.4.0 (português)

Este miniguia cobre oito etapas (00–07) para utilizar a versão **v1.4.0** em um projeto real. É um **resumo prático**, não a tradução integral do manual histórico em espanhol da v1.3. A fonte de distribuição é o [Release versionado v1.4.0](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0); v1.3.0 continua disponível como versão anterior.

Este miniguia foi acrescentado à branch `main` **depois** da publicação v1.4.0. O ZIP e o contêiner originais **não** o incluem. Para disponibilizá-lo offline, será necessária uma futura distribuição com outra versão.

## 00 · Antes de começar

O ArquitecturaRepo é uma camada de coordenação **local ao repositório** para requisitos, decisões, estado atual, responsabilidades, campanhas, evidências e recuperação. Não gera automaticamente uma aplicação nem substitui Codex.

- CLIENT define o produto, aprova ações sensíveis e julga o resultado visível.
- I1 coordena vários projetos quando necessário; I2 Planner define estratégia, capacidades e critérios de aceitação.
- I3 Controller implementa, depura, integra, testa e recupera dentro da campanha autorizada.
- I4 é opcional; **quatro funções não exigem quatro agentes**.

Seu aplicativo pode permanecer privado. O starter não precisa enviar código, dados, credenciais ou conversas ao mantenedor. O uso de provedores externos depende de sua autorização e configuração; a instalação não concede acesso nem permissões.

## 01 · Instalação segura

Use Python 3.12, testado no CI. Baixe o [ZIP portátil v1.4.0](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/download/v1.4.0/ArquitecturaRepo-v1.4.0-portable.zip), confira o `.sha256` publicado, extraia e execute os comandos **na pasta do framework extraído**. O tag Git `v1.4.0` é uma alternativa equivalente de código-fonte.

Para projetos novos ou com código, mas **sem governança canônica**, comece com `SMALL`:

```bash
python "tools/scaffold_project.py" --target "../meu-projeto" --profile SMALL --product-id MEU_PROJETO --objective "Objetivo inicial pendente de confirmação" --language pt --no-feedback-workflow
```

No PowerShell:

```powershell
python "tools\scaffold_project.py" --target "..\meu-projeto" --profile "SMALL" --product-id "MEU_PROJETO" --objective "Objetivo inicial pendente de confirmação" --language "pt" --no-feedback-workflow
```

O instalador adiciona `.agentic-sdlc/` sem modificar o código existente e recusa sobrescrever controles canônicos. `--no-feedback-workflow` remove o agendamento mensal, **não** o gerador local. Para desligar todos os relatórios, defina `enabled=false` em `.agentic-sdlc/feedback/ARCHITECTURE_FEEDBACK_CONFIG.json`. Nenhum servidor de coleta externa está incluído.

Agora, **dentro da pasta do projeto de destino**:

```bash
python -m pip install -r ".agentic-sdlc/requirements-validation.txt"
python ".agentic-sdlc/tools/project_status.py" --control-root ".agentic-sdlc"
python ".agentic-sdlc/tools/discover_project.py" --project-root "."
python ".agentic-sdlc/tools/reconstruct_context.py" --root ".agentic-sdlc"
```

No PowerShell, use caminhos entre aspas com `\`. O primeiro estado `HOLD / UNTRUSTED_CONTEXT` é **esperado** até confirmar os requisitos, a fonte e a autoridade. Se já existir Product State/controlador, **não** reinstale por cima: consulte o [preflight de governança existente, somente leitura](https://github.com/MatiasAcunia/ArquitecturaRepo/blob/v1.4.0/docs/32_EXISTING_GOVERNED_ATTACHMENT.md). Não há atualização automática universal da v1.2/v1.3.

## 02 · Planner e adoção

Investigue o código real, usuários, dados, interfaces, riscos e requisitos; o CLIENT valida a linha de base. I2 escreve um charter de **capacidade**: objetivo, escopo, responsáveis, dependências, critérios de aceitação, gates e falsificadores. Não substitua o estado real por exemplos sintéticos nem trate a instalação como autorização para executar.

## 03 · Operação diária

Comece pelo estado CURRENT, Git e evidências, não apenas pelo histórico do chat. I3 administra implementação, testes, refatorações internas, falhas e recuperação da **mesma campanha**. Novos agentes só são úteis quando há trabalho separável. Sem provas consistentes de fonte, identidade, lease e banco de dados, mantenha `HOLD`. Integração nativa com Codex Desktop/Goals ou provedores externos **não** é garantida pelo CI portátil.

## 04 · Solicitação de mudanças

Informe o comportamento observável, contexto, restrições e como validar. Exemplo: “Mostrar mensalidades atrasadas sem perder pagamentos anteriores; aceitar após testes e conferência na interface”. I2 avalia impacto estratégico; I3 resolve o trabalho já autorizado.

## 05 · Erros e recuperação

- `UNTRUSTED_CONTEXT`: confirme fontes e requisitos; não altere artificialmente o estado.
- `jsonschema` ausente: instale `requirements-validation.txt` no projeto.
- `EXISTING_CONTROL_PRESERVED`: pare; utilize o caminho de leitura, nunca `--force` nem exclusão do controle.
- Git/SQLite WAL/lease incompatíveis: suspenda mudanças materiais até reconciliar as evidências.
- Interrupção: preserve journal, identidade da execução e artefatos; recupere na campanha original. Só limpe arquivos com propriedade e política de descarte verificadas.

Issues públicos devem conter exemplos genéricos e logs ocultando tokens, caminhos pessoais, nomes privados, dados e conversas.

## 06 · Aceitação da capacidade

Verifique separadamente gates unitários, integração, banco de dados/currentness, semântica, execução física, percepção humana e release. Testes verdes e “feito” de um agente não são aceitação do CLIENT. Registre versão exata, evidência, responsável e decisão nos arquivos canônicos. CI sintético não certifica produção.

## 07 · Exemplo: clube de associados

1. CLIENT solicita cadastro, mensalidades e consulta de atrasos, definindo exemplos de uso.
2. I2 estuda banco, permissões e objetivos e delimita a menor capacidade útil.
3. I3 entrega o fluxo cadastro → mensalidade → dívida, com testes e recuperação.
4. Se surgir erro no cálculo, I3 corrige na **mesma** campanha.
5. CLIENT experimenta o sistema e aceita ou devolve problemas; a decisão e a evidência permanecem registradas.

## Referências

[Guia rápido](README_pt.md) · [FAQ](FAQ_pt.md) · [README principal](../../README.md) · [Escopo real v1.4](https://github.com/MatiasAcunia/ArquitecturaRepo/blob/v1.4.0/docs/46_V1_4_PUBLIC_START_AND_SUPPORT.md).

Este guia não comprova segurança de produção, usabilidade independente, integração nativa nem superioridade medida frente ao Codex direto. A licença MIT não cobre automaticamente material de terceiros.
