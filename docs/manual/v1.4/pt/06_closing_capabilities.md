# 06 — Encerramento de capacidades e aceitação

ArquitecturaRepo · Manual completo de utilização · Edição v1.4 · Português

> Uma capacidade fecha contra **um candidato exato e a evidência aplicável**. O terminal de I3 convida à auditoria estratégica; não aprova automaticamente o produto, não substitui o gate humano e não autoriza publicação ou deploy. Este capítulo distingue as decisões e explica como devolver erros à mesma campanha sem recomeçar a arquitetura.

## Neste capítulo

1. A capacidade é um resultado de produto
2. Cinco componentes do encerramento
3. Candidato exato como unidade de revisão
4. Evidência insuficiente sem campanhas artificiais
5. Aceitar, retomar ou mudar o objetivo
6. Revisões periódicas e regra de paragem
7. Registo de encerramento auditável
8. Exemplo de rejeição e correção
9. Produto utilizável e framework verde
10. O que fazer depois do encerramento

## 1. A capacidade é um resultado de produto

«Gestão de associados» não está concluída quando alguém desenha um formulário nem quando um agente cria commits. Está concluída quando a pessoa prevista consegue realizar as ações acordadas no ambiente relevante, os dados se mantêm como devem, os testes aplicáveis passam, o estado atual é coerente e as autoridades competentes aceitam o resultado.

O Planner define fronteiras e charter; I3 implementa, integra um candidato, produz evidência e obtém revisão independente quando necessária. O Planner audita o terminal segundo os requisitos atuais. O CLIENT aceita preferências, comportamento do produto e qualidade perceptual dentro da sua autoridade. Estes papéis não se substituem só porque um deles declara `PASS`.

Uma campanha não precisa durar um número fixo de prompts. Pode sobreviver a limites de um serviço, falhas do ambiente, reintentos e checkpoints. Isso não gera nova autorização nem apaga a evidência anterior. Por outro lado, muitas horas de trabalho e um relatório confiante não demonstram que alguém consegue utilizar a funcionalidade.

Um protótipo com screenshots pode mostrar boa direção visual; ainda não prova persistência, permissões ou recuperação após reinício. Uma API que responde a um endpoint pode precisar de testes de integração e dados. A aceitação deve corresponder ao resultado de produto que o CLIENT realmente solicitou.

## 2. Cinco componentes do encerramento

| Componente | Pergunta essencial |
| --- | --- |
| Resultado visível | A pessoa prevista consegue concluir a tarefa no ambiente relevante? |
| Verificações aplicáveis | Foram realizados os controles de lógica, integração, dados, segurança e experiência pertinentes? |
| Estado atual coerente | Código, configuração, requisitos e dados/artefactos apontam para o mesmo candidato? |
| Sem bloqueio material oculto | Algum defeito aberto invalida o resultado anunciado? |
| Aceitação competente | Planner e CLIENT examinaram a evidência que lhes compete? |

Nem toda capacidade exige todos os testes imagináveis. Um script interno simples pode dispensar avaliação estética. Uma operação com mensalidades exige persistência e um percurso de utilização confiável. A regra é que um gate não substitua silenciosamente outro relevante.

O vocabulário de gates ajuda a evitar confusão:

- **Unit:** funções ou regras isoladas comportam-se corretamente em entradas controladas.
- **Integration:** componentes e interfaces funcionam juntos, incluindo casos negativos.
- **DB/currentness:** dados, migrações, snapshots e referências atuais são coerentes e duráveis no âmbito exigido.
- **Semantic/generalization:** o comportamento corresponde à regra de negócio, não apenas a uma fixture conveniente.
- **Physical:** o programa, artefacto ou percurso executa realmente no ambiente adequado.
- **Perceptual/human:** uma pessoa competente avalia qualidade subjetiva e experiência quando importa.
- **Release:** a distribuição exata, direitos, permissões, hashes e condições de publicação estão satisfeitos.

Um teste unitário verde não demonstra que a UI abre; um JSON válido não prova CRUD; um screenshot agradável não prova que o banco persiste. O gate precisa de candidato, ambiente, resultado e owner claros. Acrescentar controles que não reduzem risco é desperdício; omitir os que importam produz aceitação prematura.

## 3. Candidato exato como unidade de revisão

Um reviewer independente tem de examinar a mesma fonte e estado que serão submetidos à aceitação. Isso pode exigir commit, configuração, schema da DB, testigos de dados, hashes dos assets e ambiente. Uma revisão do candidato A não se transfere automaticamente ao candidato B só porque ambos usam a branch `main` ou um ficheiro chamado `final`.

A sequência normal é: integrar candidato, congelar identidade relevante, realizar testes físicos e revisão independente, apresentar terminal estratégico. Se alguém modifica materialmente a implementação após a revisão, renova os controles afetados. Evidência verdadeiramente independente da alteração pode ser reaproveitada quando a relação com as fontes é demonstrável.

O [protocolo de review freeze e integridade de terminal](../../../../protocols/REVIEW_FREEZE_AND_TERMINAL_INTEGRITY.md) especifica esta relação. O controlador portátil pode modelar estados e contratos, mas não pode fingir ter observado uma aplicação externa ou recebido autorização humana real.

Mesmo depois de um PASS técnico, podem continuar pendentes revisão de privacidade, disponibilidade em produção, aceitação perceptual, licença de terceiros ou autorização de release. Registe estes gates separadamente. Um terminal técnico significa «há evidência para o próximo julgamento», não «todos os efeitos posteriores estão autorizados».

Essa disciplina protege a própria equipa. Um revisor que encontra uma falha num candidato desatualizado não deve bloquear indevidamente uma versão diferente sem verificar o delta. E uma aprovação antiga não deve ser utilizada para encobrir uma mudança de comportamento posterior. A identidade exata permite determinar o que precisa realmente ser revisto.

## 4. Evidência insuficiente sem campanhas artificiais

Se um terminal falha por razões que já pertencem ao charter, o Planner devolve a I3 um conjunto **consolidado de falsificadores**: requisito esperado, comportamento observado, candidato, gate e evidência. I3 corrige, testa, integra e obtém revisão na mesma campanha. Não pede um charter novo porque uma transação falhou.

Uma falha de teste, defeito identificado por reviewer, migração em envelope, refactor interno ou crash recuperável são problemas de execução. Não se criam PASS4 ou PASS5 para transformar o Planner num depurador. O Controller tem autoridade e responsabilidade por essas reparações até existir um terminal estratégico.

Se o mesmo tipo de defeito regressa repetidamente, I3 investiga o subsistema completo. Pode ser necessário rever contratos, persistência, concorrência, testes e a integração. Uma correção que esconde apenas um sintoma não satisfaz a capacidade; o objetivo é reduzir a classe de risco de forma demonstrável.

Uma decisão nova de negócio, alteração de permissões ou incompatibilidade estratégica pode invalidar o charter. Nesse caso o Planner volta à estratégia. A distinção não depende de quão complicado ficou o código, mas de saber se o resultado continua dentro da autorização vigente.

Um terminal bem escrito contém candidato e ambiente, percurso observado, gates aprovados, gates abertos com impacto, riscos e próxima ação com owner. É um índice para fontes canónicas, não uma nova cópia do Product State. Se uma referência aponta para um log antigo, não serve para aceitar o estado presente.

## 5. Aceitar, retomar ou mudar o objetivo

**Aceitar.** O Planner audita a evidência pertinente e regista a capacidade aceite nas superfícies canónicas. O CLIENT realiza a sua aceitação perceptual ou de produto quando aplicável. Downstreams só devem depender de uma capacidade se os requisitos necessários foram efetivamente demonstrados.

**Retomar após interrupção.** Uma sessão nova reconstrói charter, owner, checkpoint, candidato e efeitos pendentes. Não declara a campanha terminada porque foi atingido um limite de tokens ou porque o host já não consegue ler uma conversa antiga. A fonte física continua mais forte que a memória do agente.

**Mudar prioridades.** Um atraso de cronograma não muda necessariamente a regra de negócio. Alterar a política de pagamento ou elegibilidade muda. Registe supersessões e dependências, preservando trabalho que continua válido. Não mantenha dois charters contraditórios como atuais para o mesmo concern.

**Manter HOLD.** Se não existe forma de relacionar um candidato com DB ou fonte atual, bloqueie apenas as ações dependentes da incerteza. Provas de leitura e investigação segura podem continuar. Um HOLD específico é melhor que inventar currentness ou paralisar indiscriminadamente o produto inteiro.

## 6. Revisões periódicas e regra de paragem

Uma reunião semanal deveria responder às seguintes perguntas: o que está aceite, o que pode ser demonstrado hoje, qual a prioridade seguinte, que prazo ainda é plausível, que risco importante existe e qual decisão é realmente do CLIENT. As respostas devem apontar para resultados físicos, não apenas para o volume de atividade.

Commits, documentação, número de agentes, tokens e horas de runtime são meios e custos. Podem ser necessários para entregar uma capacidade, mas não são a capacidade em si. Um projeto que passa semanas a produzir relatórios sem completar um percurso de utilizador precisa de rever o método, não celebrar a produção de documentação.

O framework tem uma regra de paragem: depois de satisfazer os gates de release, não deve continuar a ganhar políticas genéricas sem uma falha identificada ou benefício real. Cada novo mecanismo aumenta manutenção e possíveis contradições. A mesma disciplina vale para os produtos feitos com ele.

O equilíbrio deve ser concreto. Aceitar uma feature quebrada porque uma fixture passou é perigoso; bloquear indefinidamente uma feature válida por um microdefeito sem impacto é improdutivo. A revisão estratégica distingue riscos materiais de detalhes que podem ser melhorados depois, com as autoridades apropriadas.

## 7. Registo de encerramento auditável

Um trabalhador que entra amanhã deve conseguir localizar a evidência sem ler todo o chat. Um registo curto pode apontar para:

| Campo | O que deve ser rastreável |
| --- | --- |
| Candidato | Fonte, configuração, estado e artefactos exatos revistos. |
| Resultado | Entrada, ação e saída observada no percurso end-to-end. |
| Testes | Comandos relevantes, ambiente e outputs. |
| Persistência | Readback, reinício e recuperação quando necessários. |
| Segurança e direitos | Verificações proporcionais à privacidade e ao material externo. |
| Revisão | Reviewer, âmbito e identidade do candidato. |
| Mudanças posteriores | Delta após freeze e gates renovados. |
| Gate humano | Aprovação ou rejeição autêntica, nunca inferida. |
| Próxima rota | Aceitar, devolver a I3, perguntar ao CLIENT ou HOLD específico. |

Não crie outro ficheiro `CURRENT` só para organizar essa tabela. Use links para as superfícies com owner canónico. Se um link falta, se a DB não corresponde à fonte ou se a prova é apenas uma fixture não relacionada com o produto, o registo ainda não sustenta a aceitação.

Também é necessário diferenciar provas do framework e provas da aplicação. A instalação e recuperação portátil do starter podem ser verificadas na CI, mas a experiência de um utilizador num projeto concreto necessita dos seus próprios testes. Um gate de release do framework não confere garantia universal a todas as aplicações que o adotarem.

## 8. Exemplo de rejeição e correção

Suponha que uma aplicação do clube permite criar e desativar associados. A revisão independente descobre que uma desativação elimina o histórico de pagamentos, embora o charter determinasse retenção. O Planner devolve a I3 um falsificador claro: «Desativar um associado com pagamentos anteriores deve preservá-los após reiniciar; o candidato X elimina-os».

I3 investiga relações e persistência, corrige a causa, acrescenta regressão significativa, testa o readback depois do reinício, integra novo candidato e pede revisão independente. Não abre uma campanha chamada «corrigir desativação» e não exige que o CLIENT escolha a foreign key apropriada.

Se a alteração produz B e o reviewer avaliou A, o PASS de A não aceita B. Pode reutilizar-se evidência de componentes não afetados, mas os testes de persistência e a revisão sobre B precisam ser renovados. Isso evita tanto repetição excessiva como aprovação desatualizada.

Agora imagine que o CLIENT pede uma funcionalidade de reativação com permissões especiais. É comportamento novo e precisa de uma decisão sobre quem pode reativar e como fica o histórico. O Planner avalia o impacto e a autorização. A nova regra não é a mesma coisa que corrigir um defeito de regra antiga.

## 9. Produto utilizável e framework verde

Uma campanha pode passar na validação de contratos do controller sem produzir uma aplicação utilizável. Para aceitar um CRUD de associados, abra a aplicação real, crie um registo fictício, pesquise, edite, desative e confirme a retenção de histórico. Se a persistência importa, reinicie e faça uma nova leitura. Se existem permissões, teste também o acesso que deve ser recusado.

O `tools/verify_v1_release.py` do ArquitecturaRepo verifica um snapshot concreto do framework e cenários sintéticos. Verificação de fonte, instalação portátil Linux/Windows, leitura de artefactos de release e aceitação de um produto de terceiros são gates diferentes. A documentação de [suporte público v1.4](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md) especifica o que foi exercitado.

É incorreto anunciar «todos os testes passaram» sem indicar de que testes se trata. Pode ser verdade que a camada de controlo valide e que a aplicação ainda esteja em `NOT RUN` no gate físico. Uma declaração honesta permite continuar o trabalho certo; uma frase global pode induzir o CLIENT a aceitar algo inexistente.

Uma integração nativa com outro host também exige prova própria. O funcionamento de scripts de referência não é prova de que Codex Desktop, um fornecedor pago ou um serviço externo tenham sido autenticados e executados com sucesso no ambiente adotado.

## 10. O que fazer depois do encerramento

Depois da aceitação, atualize Product State, lineage e referências atuais para o candidato correto. Desbloqueie apenas os dependentes justificados por essa aceitação. Se houver rejeição por bug dentro do charter, retorne a I3. Se uma mudança de produto invalidou a estratégia, volte ao Planner. Se falta prova de currentness, mantenha HOLD sobre o trabalho dependente.

O CLIENT deve conseguir terminar a sessão sabendo o que está realmente utilizável, o que continua aberto, quem resolve a questão e quando haverá nova demonstração. Se só o agente da conversa anterior consegue responder, a continuidade ainda é insuficiente.

Um bom encerramento dispensa um relatório gigantesco, mas exige identidade, evidência e decisão. A pergunta final é: alguém que não participou no desenvolvimento consegue confirmar a afirmação a partir dos artefactos e fontes apresentados? Se a resposta for não, ainda falta trabalho de engenharia ou de documentação da prova.

**A seguir:** capítulo 07, um exemplo completo de aplicação de gestão de um clube.

## Fontes e âmbito

- [Integridade de freeze e terminal](../../../../protocols/REVIEW_FREEZE_AND_TERMINAL_INTEGRITY.md)
- [Ciclo de vida de capacidades](../../../../protocols/CAPABILITY_LIFECYCLE_AND_EVIDENCE.md)
- [Validação executável](../../../10_EXECUTABLE_VALIDATION.md)
- [Gates de release](../../../17_V1_RELEASE_GATES.md)
- [Suporte e distribuição v1.4](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md)
- [Código do verificador de release](../../../../tools/verify_v1_release.py)

Os critérios de aceitação dependem do produto e do candidato atual. Estes exemplos não concedem autoridade nem substituem verificação real.
