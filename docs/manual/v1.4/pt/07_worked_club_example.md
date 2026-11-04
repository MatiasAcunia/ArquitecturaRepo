# 07 — Exemplo guiado: aplicação de gestão de um clube

ArquitecturaRepo · Manual completo de utilização · Edição v1.4 · Português

> Este é um **exemplo fictício de aprendizagem**, não uma aplicação implementada, um backend automaticamente gerado ou prova de que um modelo de IA entregou um CRUD aceite. Os nomes, dados e resultados abaixo são ilustrativos. Num produto real, requisitos, código, DB, runtime, permissões e evidência precisam vir do projeto adotado.

## Neste capítulo

1. O produto que o clube pretende construir
2. Descobrir as questões que mudam o resultado
3. Instalar o controlo sem confundi-lo com a aplicação
4. Primeira capacidade: gestão de associados
5. Do Planner a I3: um pedido operacional
6. O que testar antes de aceitar
7. Segunda capacidade: mensalidades e pagamentos
8. Avaliar todo o exemplo
9. Primeiro ciclo com dados fictícios
10. Registar e encaminhar um defeito
11. As dependências do segundo ciclo
12. Exercício final de recuperação

## 1. O produto que o clube pretende construir

Imagine um clube local que utiliza folhas de cálculo para controlar associados, mensalidades, atividades e inscrições. Uma pessoa administrativa precisa saber quem está inscrito, quais quotas estão pagas e quantas vagas existem numa atividade. O objetivo é construir uma aplicação pequena, compreensível e confiável, que mantenha o histórico e evite erros de capacidade.

Para a primeira versão, o CLIENT decide que o programa será usado internamente. Não incluirá pagamentos online, uma aplicação móvel separada, faturação fiscal, notificações em massa ou integrações externas. Essas exclusões não são juízos definitivos contra as funcionalidades: são limites para a primeira entrega demonstrável, respeitando prazo, custo e complexidade.

Isso define a direção, mas não estabelece a linguagem, a base de dados, o hosting ou as permissões técnicas. O Planner precisa de confirmar o ambiente e a utilização; engenharia escolhe um stack proporcional aos riscos e ao código existente. O framework de coordenação não cria automaticamente formulários de associados nem grava dados por si só.

Uma sequência provável de capacidades é identidade dos associados, depois mensalidades e histórico, em seguida atividades/capacidade e finalmente inscrições com regras de elegibilidade. Essas capacidades dependem umas das outras. Não convém registar pagamentos sem identidade estável, nem validar inscrição por quotas quando o estado de pagamento ainda não é confiável.

O objetivo da arquitetura é manter a continuidade dessas decisões durante o desenvolvimento, não criar quatro hierarquias de agentes. Para um clube pequeno, um Controller competente e um Planner claro podem ser suficientes. Especialistas ou revisores independentes entram quando existe risco e trabalho adequadamente delimitado.

## 2. Descobrir as questões que mudam o resultado

O Planner começa com discovery. Quantas pessoas utilizarão a aplicação? Há dois operadores simultâneos? O programa precisa funcionar sem internet? Como são feitos os backups? Que informações pessoais são armazenadas? Existe histórico que nunca pode ser apagado? Qual o prazo de uma primeira demonstração útil?

Uma regra proposta poderia ser: «Um administrador pode desativar um associado, mas os pagamentos históricos continuam acessíveis a pessoas autorizadas». O CLIENT precisa confirmar o significado da regra. Desativar não é necessariamente apagar; podem existir obrigações de retenção ou critérios específicos de consulta.

Outras perguntas: um associado em atraso pode inscrever-se numa atividade? E se tiver um acordo de pagamento? Uma inscrição cancelada liberta a vaga imediatamente? Existe lista de espera? Quem pode corrigir um pagamento? A data de vencimento depende do mês civil ou da data de adesão? Sem essas decisões, o programa pode apresentar respostas contraditórias em ecrãs diferentes.

| Área | Comportamento proposto para a primeira versão |
| --- | --- |
| Associados | Criar, editar, pesquisar e desativar, preservando relações históricas. |
| Mensalidades | Registar pagamentos, identificar períodos em atraso e consultar histórico. |
| Atividades | Definir nome, horário, capacidade e vagas disponíveis. |
| Inscrições | Inscrever e cancelar com regras explícitas de capacidade e quotas. |
| Exclusões | Sem pagamentos online, app móvel, notificações em massa ou dashboards elaborados. |

Cada linha continua provisória até confirmação do CLIENT. A necessidade de dados persistentes sugere o perfil `STATEFUL`, com controles de backup, currentness, migração e recuperação. Mas o perfil não cria uma política de pagamento nem confere permissão para guardar dados pessoais sem uma decisão adequada.

## 3. Instalar o controlo sem confundi-lo com a aplicação

Se o projeto do clube for novo e não tiver governação canónica anterior, é possível adicionar `.agentic-sdlc/` com um scaffold v1.4. Num checkout verificado do starter, o comando PowerShell ilustrativo é:

```powershell
& "python" "tools\scaffold_project.py" --target "..\clube-app" --profile "STATEFUL" --product-id "CLUBE_GESTAO" --objective "Gestão fictícia de associados e mensalidades" --language "pt" --no-feedback-workflow
```

Esse comando cria a camada de controlo inicial no projeto de destino, com `HOLD / UNTRUSTED_CONTEXT`. Não demonstra que existe uma aplicação, não inicializa uma DB, não instala um LLM e não concede autoridade para executar uma campanha. Os passos de [instalação do capítulo 01](01_installation.md) mostram como inspecionar os resultados.

Se `clube-app/` já estiver governado, não se deve copiar um segundo Product State. Utilize o [preflight somente leitura para governação existente](../../../32_EXISTING_GOVERNED_ATTACHMENT.md) e prepare a rota de adoção ou migração que preserva owners, fonte, DB e campanhas. O framework não é um atualizador in-place universal de controles de versões anteriores.

Depois do scaffold, Planner e engenharia investigam código, inventário, requisitos e estado existentes. Prepararam uma especificação de adoção revisada, fazem preflight, promovem apenas registos coerentes e demonstram reconstrução de contexto fresco. O CLIENT confirma escopo, prazo, restrições e prioridades antes de um charter de capacidade ser autorizado.

A decisão de stack deve considerar quem terá de manter a aplicação, ambiente real, conexão à rede, segurança e backups. Pode ser uma aplicação local simples ou um serviço mais elaborado se a necessidade justificar. Não se escolhe cloud, microserviços ou uma estrutura de agentes complexa apenas porque o framework admite esses conceitos.

## 4. Primeira capacidade: gestão de associados

Começar por associados resolve uma dependência fundamental. Quotas e inscrições precisam apontar para uma identidade estável. Uma capacidade inicial poderia definir:

> Um operador autorizado consegue criar um associado, consultar os seus dados, corrigi-los, pesquisá-lo e desativá-lo; pagamentos ou inscrições históricas permanecem preservados e disponíveis dentro das permissões previstas.

O charter identifica interfaces afetadas, ownership de dados, comportamento de erro e gates. Não precisa prescrever o nome de cada método. I3 organiza implementação, testes, correções, integração e revisão do candidato resultante. O Planner avalia a entrega contra os requisitos confirmados, não pela quantidade de código produzido.

Os testes relevantes abrangem identificador duplicado, campos inválidos, escrita e readback, persistência após reinício, filtros de ativos/inativos, histórico de relações, acesso não autorizado e interface real quando existe UI. A prova física deve executar o percurso do utilizador; uma unit test de validação não confirma que a ficha pode ser encontrada.

O CLIENT não precisa escolher um ORM, tipo de índice ou estrutura de diretórios. Engenharia pode decidir essas questões e explicar os trade-offs que alterem orçamento, acesso ou risco. Se o programa usar dados existentes, a migração deve respeitar o estado atual, backups e permissões; não se deve tratar o clube fictício deste manual como uma base real.

## 5. Do Planner a I3: um pedido operacional

Um dispatch completo pode continuar curto. Num projeto real teria de ser adaptado aos refs e requisitos canónicos, mas a estrutura é esta:

> **Goal:** Entregar a capacidade de gestão de associados dentro do charter atual.
>
> **Context:** Reconstruir requisitos confirmados, Product State, fonte exata, ambiente e estado atual da DB.
>
> **Constraints:** Preservar histórico, respeitar permissões e orçamento; não introduzir processamento de quotas nem funcionalidades não aprovadas.
>
> **Execution gates:** Exercitar fisicamente criação, pesquisa, edição, desativação e readback após reinício. Testar inputs inválidos, duplicados e caminhos pertinentes de segurança e concorrência. Rever independentemente o candidato integrado.
>
> **Done when:** Apresentar ref exato, evidência física, resultados dos gates, achados do reviewer, limitações e terminal estratégico honesto.

I3 pode dividir o trabalho em execuções táticas, ajustar interfaces internas, depurar, retestar e recuperar interrupções. Se um duplo clique cria dois associados com identificador supostamente único, a falha pertence à mesma campanha. Não se abre uma segunda campanha apenas para resolver duplicados.

Quando há operações múltiplas ou custo material, o Controller pode definir uma work order com inventário, limites de execução, orçamento e condições de paragem. Uma unidade de execução não pode ampliar a intenção do CLIENT nem chamar um serviço pago sem autoridade. O charter continua a ser o limite do trabalho.

## 6. O que testar antes de aceitar

Considere um registo totalmente fictício `ASSOCIADO-001`. A tabela seguinte é um plano de teste, **não prova de que a aplicação existe ou que o teste foi realizado**:

| Etapa | Ação | Resultado esperado |
| --- | --- | --- |
| 1 | Abrir a aplicação como administrador. | O controlo de acesso real permite o papel correto. |
| 2 | Criar `ASSOCIADO-001` com dados sintéticos válidos. | Exatamente um registo aparece com identidade estável. |
| 3 | Pesquisar pelo identificador permitido. | Aparece a ficha correta sem expor informação não autorizada. |
| 4 | Alterar um contacto fictício. | A mudança é visível após guardar e reler. |
| 5 | Fechar e reabrir a aplicação. | O dado persiste pelo caminho real de DB/recovery. |
| 6 | Desativar o associado. | Não aparece como ativo, mas a identidade histórica mantém-se. |
| 7 | Consultar histórico com permissão adequada. | Pagamentos e inscrições anteriores continuam disponíveis. |
| 8 | Tentar um dado inválido ou duplicado. | A aplicação rejeita sem corromper estado. |

Registe entrada, esperado, observado, candidato, data e ambiente em cada etapa. Um retorno HTTP 200 não prova que a escrita persistiu; deve ser conferido por leitura adequada. Se o estado precisa sobreviver a reinício, teste o reinício. Se dois operadores existem no escopo, exercite ações simultâneas ou intercaladas, conforme a arquitetura.

Não utilize dados reais de associados em screenshots, vídeos ou issues públicos. A avaliação de experiência deve usar dados fictícios e um ambiente representativo. Um gate perceptual feito por pessoa competente complementa, mas não substitui, as provas de DB, segurança e integração.

Quando a aplicação ainda não existe, o estado honesto desses passos é `NOT RUN`. Não os marque como PASS porque o manual descreve como deveriam funcionar. A finalidade do exercício é aprender que evidência será necessária, não produzir uma narrativa de sucesso sem implementação.

## 7. Segunda capacidade: mensalidades e pagamentos

Depois de aceitar estrategicamente a identidade de associados, o CLIENT pode pedir registo de mensalidades e consulta de atrasos. O Planner confirma períodos, vencimentos, pagamentos parciais, correções, permissões e tratamento de duplicados. O estado «em dia» deve derivar de uma regra consistente e dados atuais.

Uma decisão possível é: «Um pagamento registado por engano é revertido com uma entrada de auditoria, sem eliminar a transação original». O CLIENT confirma a política; o Planner documenta a regra e o risco; I3 implementa persistência, validações e recuperação. Uma segunda submissão da mesma operação não deve produzir efeito duplicado quando a regra exige idempotência.

Se a aplicação envolver dinheiro real, os gates de autorização, segurança, auditoria e dados precisam ser proporcionais às consequências. O framework não traz um processador de pagamentos e não autoriza ligar um serviço externo por iniciativa de um agente. O exemplo de quotas serve para estudar dados e regras, não para assumir operações financeiras publicadas.

Atividades e inscrições vêm depois, quando identidade e estado de mensalidades são confiáveis. Uma pessoa só pode inscrever-se respeitando lotação e elegibilidade. Se os dados upstream ainda forem provisórios, iniciar a inscrição completa arrisca implementar regras contraditórias; o Planner deve reconhecer a dependência antes de autorizar a campanha.

## 8. Avaliar todo o exemplo

Ao concluir este capítulo, deverá conseguir explicar o que o CLIENT decide, o que o Planner confirma, que trabalho I3 executa, como é identificada a fonte atual, porque a revisão independente tem de ver o candidato exato e como se obtém uma aceitação real. Também deve reconhecer que instalar o framework não é entregar a aplicação.

O objetivo não é decorar cada nome de ficheiro JSON. É saber qual superfície contém a verdade atual, quem é responsável por alterá-la e que resultado observável demonstra uma capacidade. Se o processo produz dezenas de documentos mas não consegue mostrar um percurso de associado, ainda não resolveu o problema do clube.

O exemplo aplica-se também a uma API CRUD, gestão de reservas, biblioteca, aplicação educativa ou sistema interno de uma empresa. Os riscos concretos mudam, mas a separação entre intenção, autorização, implementação, evidência e aceitação continua útil.

A mesma análise ajuda a comparar uma abordagem estruturada com programação direta num chat. Um protótipo isolado pode avançar mais depressa com prompts diretos; um produto longo pode ganhar em continuidade, revisão e recuperação. A superioridade de um método tem de ser medida no trabalho real, não proclamada pelo manual.

## 9. Primeiro ciclo com dados fictícios

Para praticar, invente «Pessoa de Teste A» com contacto obviamente fictício. Decida com o CLIENT quais campos são obrigatórios e qual identificador deve ser único. O Planner registra os requisitos; engenharia escolhe o modelo de dados, validações e limites de transação.

Execute o percurso: criar, listar, pesquisar, editar, reiniciar, reler, desativar e consultar o histórico autorizado. Registe em cada etapa o resultado realmente observado. A captura do primeiro ecrã é apenas o começo da prova; não demonstra que uma alteração sobreviveu a reinício ou que uma pessoa sem permissão foi bloqueada.

Acrescente casos negativos: identificadores repetidos, campos inválidos, falha controlada da DB durante uma escrita e submissões duplicadas. O comportamento de erro deve ser claro e consistente com os requisitos confirmados. Não se aceita um estado contraditório silencioso como resultado normal.

Se vários operadores podem aceder simultaneamente, verifique situações de concorrência: duas inscrições para a última vaga, dois pagamentos da mesma obrigação, edição simultânea de um contacto. Testes sequenciais não provam automaticamente que o sistema é seguro nessas situações. Escolha os ensaios de acordo com o risco e o ambiente real.

O feedback do primeiro ciclo pode gerar pequenos ajustes de UX: posição dos campos, mensagem de erro, facilidade de encontrar uma ação. Se a alteração está dentro do envelope, I3 corrige; se acrescenta uma regra de negócio, o Planner confirma a decisão com o CLIENT. A observação humana e o resultado técnico pertencem a gates diferentes.

## 10. Registar e encaminhar um defeito

Suponha que «Pessoa de Teste A» é desativada e o histórico de pagamentos desaparece. Se a retenção estava confirmada, é um bug in-charter. Registe candidato, passos, dados sintéticos, resultado observado e gate afetado. O Planner devolve um falsificador consolidado a I3.

O Controller investiga relações de persistência, corrige a causa, executa testes de regressão e readback após reinício, integra novo candidato e obtém revisão independente aplicável. Não cria uma campanha paralela e não pede ao CLIENT para decidir como configurar uma foreign key. Essas decisões de engenharia pertencem ao seu mandato.

Agora o CLIENT pergunta se o associado inativo pode ser reativado com o mesmo número. Se a política anterior não definia isso, não é automaticamente um bug. O Planner pergunta qual o comportamento desejado, confirma impacto na identidade, permissões e pagamentos e decide se cabe no charter ou exige revisão estratégica.

Não se inventa aceitação a partir da história fictícia. Se a aplicação não foi construída, o teste continua `NOT RUN`. Se o gate físico passou mas o CLIENT ainda não experimentou a experiência, o gate perceptual permanece aberto. Se a DB não foi verificada, não se afirma persistência apenas pelo sucesso visual.

## 11. As dependências do segundo ciclo

As mensalidades precisam de um identificador de associado estável e de regras claras sobre pagamentos parciais, vencimentos, correções e duplicados. O Planner utiliza a capacidade aceite como input atual; I3 implementa com interfaces e dados vigentes. Não se volta a uma versão antiga guardada apenas na memória do chat.

Antes da implementação de inscrições, confirme que o estado de mensalidades consumido pelas regras de elegibilidade realmente existe e é atual. Uma regra de atraso ainda indefinida pode levar a conflitos entre API e interface. O critical path não significa iniciar mais agentes, mas construir capacidades na ordem que permite testar as dependências.

Uma entrega incremental permite ao CLIENT provar primeiro a gestão de associados e só depois investir em quotas. A experiência pode revelar novos requisitos, como campos específicos do clube ou um processo de reativação. Registar a mudança cedo e atualizar downstream de forma consciente costuma ser mais barato que descobrir contradições depois de implementar tudo.

Evite acrescentar complexidade automática: microserviços, cloud, aplicações móveis, serviços de pagamento e políticas elaboradas de autorização precisam de justificação concreta. A qualidade não se mede pelo número de tecnologias usadas, mas pela utilidade, segurança proporcional e capacidade de manutenção do produto.

## 12. Exercício final de recuperação

Imagine que hoje o desenvolvimento para e amanhã entra um Planner que nunca leu a conversa anterior. O repositório e o runtime autorizado têm de revelar se a capacidade de associados foi aceite, qual candidato e evidência a sustentam, que decisões sobre quotas estão abertas, quem controla a campanha e qual próximo passo é permitido.

Se aparecerem duas campanhas ativas para o mesmo recurso, é necessário reconciliar autoridade. Se um relatório antigo diz `CURRENT`, mas o ref da fonte é diferente, a contradição deve ser investigada. Se falta testemunho de DB, o trabalho dependente fica em HOLD específico enquanto prosseguem verificações seguras.

Classifique os eventos observados: decisão nova do CLIENT, bug dentro do charter, falha de ambiente, autorização externa pendente ou invalidation estratégico. Cada tipo tem owner e rota. Um sistema confiável permite fazer esta distinção sem recriar o contexto por tentativa e erro.

O exercício está terminado quando consegue passar de intenção a comportamento demonstrável e recuperar a continuidade depois de uma interrupção. A prova de valor não é a existência de `.agentic-sdlc/` nem o número de agentes. É o produto que alguém usa e a evidência de currentness que outra pessoa consegue verificar.

**Fim do exemplo:** consulte o [índice desta edição](README.md) para regressar a um capítulo ou utilizar as referências técnicas.

## Fontes e âmbito

- [Exemplo sintético mínimo](../../../../examples/minimal/README.md)
- [Fork e bootstrap](../../../01_FORK_AND_BOOTSTRAP.md)
- [Discovery, requisitos e entrega](../../../21_PRODUCT_DISCOVERY_REQUIREMENTS_STACK_AND_DELIVERY.md)
- [Limites do CLIENT](../../../../protocols/CLIENT_BOUNDARY.md)
- [Padrão de charter](../../../../protocols/CAMPAIGN_CHARTER_STANDARD.md)
- [Início público v1.4](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md)
- [Attachment de governação existente](../../../32_EXISTING_GOVERNED_ATTACHMENT.md)

Os exemplos de clube são didáticos. Nenhum deles demonstra um sistema instalado, uma capacidade aceite, um pagamento real ou uma integração externa provada.
