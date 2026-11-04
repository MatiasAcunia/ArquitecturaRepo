# 03 — Operação diária

ArquitecturaRepo · Manual completo de utilização · Edição v1.4 · Português

> O trabalho quotidiano começa pelo estado **CURRENT**, pela fonte e pela evidência, não apenas pela última mensagem de um chat. A engenharia tem autonomia dentro de um charter aprovado; os limites de autoridade, privacidade, custo e revisão continuam a aplicar-se a cada operação material.

## Neste capítulo

1. Preparar uma sessão sem recomeçar do zero
2. Converter uma intenção numa capacidade verificável
3. O trabalho contínuo do Controller
4. Autorizações e efeitos externos
5. Como ler criticamente um relatório de execução
6. Git e continuidade entre contextos
7. Gestão de recursos, artefactos e espaço
8. Coordenação, concorrência e intervenções do CLIENT
9. Revisão independente e candidatos exatos
10. Uma rotina curta e reutilizável

## 1. Preparar uma sessão sem recomeçar do zero

Num projeto de várias semanas, uma nova conversa não significa um projeto novo. O primeiro passo é reconstruir a intenção aprovada e o estado atual a partir do repositório, Product State, DB, filas e artefactos canónicos. A memória do agente e um resumo anterior podem ajudar a localizar informação, mas não podem prevalecer sobre evidência física viva que os contradiga.

O Planner ou o Controller identifica a branch correta, commit ou versão da fonte, alterações locais ainda não integradas, Goal e charter atuais, owners, checkpoints, testigos de DB e gates pendentes. Se os nomes coincidirem mas os hashes não, a diferença deve ser investigada. Se o estado for desconhecido, descreve-se a incerteza concreta e mantém-se HOLD sobre as alterações materiais que dependem dela.

Uma sessão de engenharia pode começar com uma ação simples: verificar se o último terminal pertence realmente ao candidato atual. Quando o reviewer avaliou A e o código mudou para B, a aprovação antiga não serve automaticamente para fechar a campanha. O trabalho seguinte é determinar quais os controles que precisam ser repetidos, preservando a evidência estável que continua aplicável.

O [procedimento de bootstrap](../../../01_FORK_AND_BOOTSTRAP.md) e o [protocolo de reconstrução](../../../../protocols/CURRENTNESS_RECONSTRUCTION.md) ajudam a orientar a recuperação. O operador não deve declarar `READY` com base numa frase confiante; tem de apresentar fontes que outra pessoa possa localizar e verificar.

## 2. Converter uma intenção numa capacidade verificável

O CLIENT pode pedir «quero ver as mensalidades em atraso numa lista clara». O Planner confirma o significado de atraso, o período considerado, quem pode consultar a informação e como se observa o resultado. Também verifica se já existe uma capacidade anterior de pagamentos da qual a nova lista dependerá.

Um charter de capacidade descreve objetivo, limites, interfaces, dependências, owners, critérios de aceitação e falsificadores. Não precisa decidir antecipadamente todos os nomes de ficheiros e passos de execução. A divisão em tarefas, programação e tratamento de falhas competem a I3 depois da autorização.

É útil explicitar exclusões. Se a funcionalidade é uma consulta interna, ela não implica criar automaticamente um sistema de pagamentos online, notificações ou exportações fiscais. São mudanças de produto diferentes que exigem decisão própria. A engenharia não deve acrescentá-las porque a biblioteca técnica permitiria fazê-lo.

Quando um pedido é ambíguo, o Planner separa a parte segura da parte que exige nova decisão. Pode investigar estrutura de dados ou elaborar protótipos não materiais, mas não deve alterar dados reais com uma regra suposta. Uma boa pergunta ao CLIENT é curta, ligada a uma consequência e feita apenas quando a resposta não pode ser obtida nas fontes já autorizadas.

## 3. O trabalho contínuo do Controller

O I3 Controller é o responsável operacional por uma campanha autorizada. Pode organizar execuções técnicas, implementar, depurar, testar, recuperar crashes, refatorar dentro do scope, corrigir avaliadores, coordenar revisão independente e integrar candidatos sucessivos. Não regressa ao Planner por cada erro normal encontrado no percurso.

Uma falha de teste de integração pode exigir mudar duas classes, atualizar uma migração e melhorar o teste. Se tudo continua a satisfazer o mesmo charter, essa é execução interna. Uma revisão que deteta uma regressão deve devolver evidência precisa a I3; não criar uma nova campanha apenas para corrigir a regressão.

Quando a mesma classe de defeito regressa várias vezes, o Controller deve investigar a causa no subsistema, em vez de explorar um falso terminal após outro. Uma correção sólida pode envolver testes de regressão, revisão dos limites de transação, inspeção de contratos e uma avaliação independente contra o novo candidato. O número de rondas não é o objetivo; o desbloqueio da capacidade é.

O Controller pode recorrer a especialistas quando o problema é separável e a autoridade está definida. Quatro papéis não precisam virar quatro agentes sempre ativos. Concurrency só se justifica quando worktrees, DBs, ficheiros e recursos afetados permitem trabalho sem interferência material.

## 4. Autorizações e efeitos externos

Nem toda operação técnica necessita de aprovação humana individual. Ler código, executar testes locais, fazer commits dentro de um charter e recuperar uma falha conhecida podem estar no mandato de I3. Já publicar, enviar mensagens, gastar dinheiro, apagar dados importantes, enviar código privado a um serviço externo ou modificar uma base de produção pode exigir autorização específica.

| Ação | Tratamento razoável |
| --- | --- |
| Ler código e realizar verificações autorizadas. | Operação de engenharia normal. |
| Corrigir implementação dentro do charter. | Responsabilidade de I3, com ownership e revisão adequados. |
| Instalar dependências novas. | Confirmar procedência, necessidade, segurança e permissões. |
| Publicar, realizar pagamento ou apagar dados relevantes. | Validar autoridade e preflight específico antes do efeito. |
| Copiar credenciais ou dados privados para uma conversa. | Não o fazer; utilizar mecanismos de segredo aprovados. |
| Encontrar contradições de owner ou DB. | HOLD dependente e reconciliação baseada em evidência. |

Um CLIENT não deveria decidir entre dois índices SQL semelhantes, gerir conflitos de merge técnicos ou escolher a semântica de idempotência de uma operação já especificada. Deve, porém, decidir se o produto aceita uma determinada política de retenção, a experiência esperada ou um efeito de custo que ultrapassa o limite autorizado.

O starter inclui ferramentas de referência como `campaignctl.py`, mas a existência desses scripts não demonstra que um host externo tenha iniciado uma operação nativa de Codex ou outro fornecedor. Antes de declarar uma execução real, é preciso verificar o efeito no sistema alvo e não somente a intenção do controlador.

## 5. Como ler criticamente um relatório de execução

Um relatório útil indica o que foi tentado, o candidato exato, ambiente, comandos e dados de teste, resultado físico, mudanças feitas, resultados de gates, revisão independente e limitações. Também aponta para a próxima ação e para o owner responsável. Sem essas referências, termos como `PASS`, `READY` e `DONE` podem ocultar diferenças importantes.

Uma prova unitária confirma lógica isolada; um teste de integração verifica componentes juntos; uma prova de DB/currentness aborda dados e referências atuais; uma avaliação semântica verifica a regra de negócio; uma prova física executa o percurso real; um gate perceptual requer julgamento humano quando aplicável; um gate de release verifica a distribuição exata.

Uma prova de que um botão é renderizado não mostra que funciona. Um backend verde não demonstra que o utilizador consegue encontrar a função. Uma fixture sintética não é uma aplicação em produção. A pergunta útil é: «Qual gate foi exercitado, sobre que candidato e com que evidência?». Essa pergunta evita aceitar capacidades apenas pela confiança do agente.

O terminal deve distinguir o que passou, o que está aberto e o que precisa de decisão de produto. Não deve obrigar o CLIENT a ler logs enormes, mas também não pode esconder um risco material. Um resumo curto e preciso com links canónicos é mais útil que uma narrativa heroica de horas de execução.

## 6. Git e continuidade entre contextos

Git preserva mudanças versionadas, mas um commit não identifica automaticamente o ator, a campanha ou o owner da decisão. Também não prova que a DB esteja coerente, que a revisão inspecionou o mesmo candidato ou que um artefacto publicado corresponda ao código mais recente. Cada relação necessária deve ser documentada nas superfícies adequadas.

Quando existem alterações locais, preserve-as antes de sincronizar. Um `git pull` cego sobre um worktree com ficheiros importantes pode gerar conflitos; uma limpeza destrutiva pode apagar evidência. Compare base, ref remoto, alterações do utilizador e ownership antes de integrar. Os nomes das branches ajudam a navegar, mas os hashes e os registos de autoridade fazem a diferença.

Um commit de checkpoint pode ser valioso para recuperação, sem representar aceitação. Do mesmo modo, cinco commits pequenos não equivalem a cinco capacidades entregues. Um relatório de progresso deveria falar de resultados observados e riscos reduzidos, não de quantidade de movimento no Git.

As [ferramentas de delta do repositório](../../../../tools/repo_delta.py) permitem inspeção incremental. Se um agente novo não conseguir identificar a fonte atual com segurança, deve investigar antes de modificar. Uma conversa passada não autoriza adivinhar o estado só porque a última mensagem dizia que «estava tudo pronto».

## 7. Gestão de recursos, artefactos e espaço

O espaço em disco é um recurso do projeto. Não crie clones completos repetidos para cada agente se existe um checkout canónico seguro. Quando a concorrência exigir isolamento, prefira worktrees temporárias que partilham o banco de objetos Git e remova-as quando deixam de ser necessárias, preservando os registos relevantes.

Renders, builds, áudio temporário, screenshots e caches podem consumir muito espaço. Antes de gerar um artefacto pesado, verifique se já existe uma versão canónica com identidade e lineage adequados. Evite várias cópias do mesmo vídeo ou PDF com nomes diferentes apenas para cada reviewer. A evidência pode apontar para o mesmo artefacto por hash e caminho autorizado.

O `tools/workspace_gc.py` e os protocolos de [inventário e limpeza de artefactos](../../../34_FILE_ARTIFACT_INVENTORY_AND_GC.md) tratam descarte baseado em ownership. Uma execução de limpeza deve começar com inventário e dry-run. Não se removem dados humanos desconhecidos, source code, artefactos aceites ou conteúdo canónico só porque parecem antigos.

O custo também inclui tempo de compute, APIs e limites de fornecedores. Uma operação pode ser pequena em código e cara em geração de mídia; outra pode exigir testes demorados mas sem cobrança externa. O Controller deve conhecer orçamentos e condições de parada da campanha. Nunca transforma uma permissão para testar localmente em autorização para consumir serviços pagos.

## 8. Coordenação, concorrência e intervenções do CLIENT

Num projeto com mais de um workstream, os owners devem distinguir quem decide, quem executa e que superfície de estado é canónica. Dois agentes podem alterar componentes independentes em paralelo; dois escritores sobre a mesma DB, schema ou contrato exigem coordenação explícita. O nome do projeto não é suficiente para decidir se a concorrência é segura.

O I1 MASTER OWNER ajuda a resolver riscos de integração entre workstreams, duplicação de políticas, campanhas que não avançam e conflitos que o Planner local não consegue solucionar. Não deve transformar-se num segundo Planner que reabre todas as decisões, nem numa desculpa para que I3 devolva bugs de engenharia a um nível superior.

O CLIENT intervém nos pontos de decisão relevantes: confirmar uma regra, aprovar uma mudança de custo, avaliar a experiência ou aceitar o resultado. Pode ser um intermediário que cola uma mensagem completa entre ChatGPT e Codex se o ambiente não permite integração direta. O sistema continua responsável por preparar o contexto técnico e as verificações.

Uma comunicação operacional ao Controller deve ser completa e executável: objetivo, fontes atuais, limites, gates e critério de terminal. Não peça ao CLIENT que junte cinco patches nem que sincronize manuais de estado contraditórios. A organização existe precisamente para reduzir esse trabalho de coordenação humana.

## 9. Revisão independente e candidatos exatos

Antes de apresentar uma capacidade para aceitação, I3 integra um candidato definido e obtém os controles previstos. Um reviewer independente deve examinar o mesmo código, dados e artefactos relevantes. Se o candidato muda depois da revisão, é necessário renovar os controles afetados, sem fingir que a aprovação antiga se aplica ao novo conteúdo.

O [protocolo de freeze e integridade de terminal](../../../../protocols/REVIEW_FREEZE_AND_TERMINAL_INTEGRITY.md) organiza essas relações. Ele não garante por si só o comportamento de uma aplicação externa: quando a prova física importa, é preciso abrir ou executar realmente o produto e observar os passos exigidos.

Se a revisão encontra um defeito dentro do charter, o Planner devolve a I3 o conjunto de falsificadores. Se encontra uma nova decisão de produto, pede confirmação ao CLIENT e avalia o impacto estratégico. Um terminal técnico não pode ultrapassar a autorização humana e um screenshot agradável não substitui prova de dados.

O êxito depende de coerência entre afirmação e evidência. Um `PASS` deve identificar o gate, candidato e âmbito, não ser usado como certificado universal. A revisão humana também deve distinguir gosto subjetivo de uma regra objetiva já confirmada.

## 10. Uma rotina curta e reutilizável

No início de cada sessão, recupere objetivo, autoridade, fonte, currentness e bloqueios. Durante o trabalho, preserve checkpoints, execute alterações dentro do charter e verifique os efeitos materiais. Antes de apresentar um terminal, integre o candidato, execute gates aplicáveis, obtenha revisão e escreva um relatório conciso com evidência rastreável.

Se a sessão for interrompida, conserve a tentativa, journal e estado. O próximo agente tem de conseguir retomar sem reproduzir erros ou inventar progresso. Se houver contradição, HOLD sobre o efeito dependente e investigação segura. Se o bug estiver dentro do scope, I3 corrige. Se a premissa de produto mudou, o Planner reentra no limite certo.

No fim de uma semana, o CLIENT deveria ouvir quais capacidades são realmente utilizáveis, que risco está aberto e qual decisão precisa tomar. Se a resposta consiste apenas em listas de commits e horas, a arquitetura ainda não transformou atividade em resultado.

**A seguir:** capítulo 04, como solicitar mudanças sem perder foco nem criar trabalho duplicado.

## Fontes e âmbito

- [Bootstrap e estado atual](../../../01_FORK_AND_BOOTSTRAP.md)
- [Reconstrução de currentness](../../../../protocols/CURRENTNESS_RECONSTRUCTION.md)
- [Integridade de freeze e revisão](../../../../protocols/REVIEW_FREEZE_AND_TERMINAL_INTEGRITY.md)
- [Ferramenta de delta](../../../../tools/repo_delta.py)
- [Inventário e garbage collection](../../../34_FILE_ARTIFACT_INVENTORY_AND_GC.md)
- [Validação executável](../../../10_EXECUTABLE_VALIDATION.md)

Estes procedimentos descrevem responsabilidades e limites; não significam que qualquer host proprietário ou serviço de IA tenha sido integrado e testado pelo starter.
