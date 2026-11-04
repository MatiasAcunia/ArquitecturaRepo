# 02 — O Planner e a adoção do projeto

ArquitecturaRepo · Manual completo de utilização · Edição v1.4 · Português

> A presença de `.agentic-sdlc/` não prova que a aplicação tenha sido compreendida. O Planner tem de relacionar o framework com requisitos confirmados, código real, dados atuais, ambiente, decisões técnicas e autoridade. O objetivo da adoção é passar de `UNTRUSTED_CONTEXT` para um estado reconstruível **sem inventar factos nem criar um segundo sistema canónico**.

## Neste capítulo

1. Uma conversa sobre o projeto, não sobre a ferramenta
2. Preparar um espaço de trabalho
3. Discovery: fazer as perguntas corretas
4. Baseline de produto e plano de entrega
5. Adoção: relacionar starter e aplicação
6. O exame decisivo de um contexto fresco
7. Primeira campanha autorizada
8. Exemplo de sessão inicial com o Planner
9. Um baseline confirmado pelo CLIENT
10. Exemplo de primeira campanha

## 1. Uma conversa sobre o projeto, não sobre a ferramenta

O Planner começa pelo produto final. Uma pessoa pode dizer «quero um sistema de reservas para o clube» ou «preciso de uma API para organizar dados». Antes de falar em agentes, workflows ou ficheiros de estado, é necessário compreender quem utilizará o sistema, que problema existe hoje e como se poderá observar uma melhoria real.

Uma descrição útil distingue o trabalho do utilizador do trabalho técnico. O CLIENT pode decidir que uma reserva cancelada deve libertar um lugar imediatamente, mas não precisa escolher a implementação de uma transação. A engenharia pode propor uma base relacional, mas não deve decidir sem consulta que os dados antigos podem ser eliminados. O Planner mantém essas responsabilidades separadas.

Perguntas centrais são: quem usará o produto, em que ambiente, que dados são necessários, quais as funcionalidades realmente prioritárias, que integrações já existem, qual o limite de custo e prazo, e que situações negativas são perigosas. As respostas têm de ser confirmadas antes de se tornarem requisitos vigentes; hipóteses provisórias podem ser registadas como perguntas abertas.

Não é preciso transformar o primeiro contacto numa entrevista interminável. Para um protótipo simples, poucas perguntas podem bastar para começar uma capacidade pequena. Para um sistema com dinheiro, dados pessoais ou dependência de produção, o nível de investigação deve aumentar. A proporcionalidade é uma decisão de risco, não de formalismo.

## 2. Preparar um espaço de trabalho

O Planner deve saber qual é a fonte do código e qual é o projeto de destino. Antes de editar, inspecciona a estrutura de pastas, o estado de Git, a branch, alterações locais, configurações relevantes, testes existentes, DBs, scripts de arranque e a camada de controlo, se existir. Um checkout parecido pode conter fontes diferentes; a identidade não é estabelecida pelo nome da pasta.

A análise inicial deve ser principalmente de leitura. O objetivo é descobrir o que já existe e o que funciona. Para um projeto antigo com governação própria, o [preflight de attachment existente](../../../32_EXISTING_GOVERNED_ATTACHMENT.md) impede que uma instalação genérica crie uma segunda autoridade. Para um projeto novo sem governação, o scaffold inicial pode ser apropriado, mas continua em HOLD até concluir a adoção.

Uma ferramenta de descoberta pode enumerar ficheiros e hashes. Essa informação ajuda, mas não permite inferir automaticamente regras de negócio. Ler uma tabela chamada `payments` não comprova quais os tipos de pagamento, quem pode rever um registo ou se um lançamento pode ser anulado. O Planner tem de verificar com o CLIENT o significado funcional e com a engenharia o comportamento efetivo.

É importante separar material público do framework de artefactos privados do projeto. Relatórios com dados reais não devem ser colocados num repositório público para facilitar a continuidade. Pode-se preservar a identidade de um artefacto por referência e hash sem copiar o seu conteúdo para toda a equipa.

## 3. Discovery: fazer as perguntas corretas

Boas perguntas produzem decisões que alteram o produto. Para um clube fictício, por exemplo: pode existir um associado com mensalidades em atraso? Uma inscrição depende de estar em dia? Como se corrige um pagamento registado por engano? O que acontece a um histórico quando se desativa uma conta? É possível operar sem ligação à internet?

Uma pergunta trivial, cuja resposta já está documentada na fonte, desperdiça a atenção do CLIENT. O Planner deve primeiro ler o que existe e perguntar apenas pelos pontos de produto ainda indefinidos ou contraditórios. Uma pessoa que pede uma aplicação não deve ter de responder a dezenas de perguntas sobre nomes de classes ou frameworks que a engenharia consegue resolver.

| Tipo de pergunta | Exemplo | Consequência |
| --- | --- | --- |
| Necessidade | «Que tarefa demora mais hoje?» | Define a primeira capacidade de valor. |
| Regra de negócio | «Uma pessoa pode reservar com uma quota em atraso?» | Afeta elegibilidade e mensagens. |
| Dados | «É obrigatório conservar o histórico de pagamentos?» | Afeta persistência e recuperação. |
| Utilização | «Há dois operadores em simultâneo?» | Afeta concorrência e experiência. |
| Segurança | «Quem pode ver contactos pessoais?» | Afeta autorização e exposição. |
| Limites | «Qual é a data útil da primeira versão?» | Afeta escopo e critical path. |

O Planner confirma as respostas e regista-as como requisitos com fonte e data. Se o CLIENT responder «ainda não sei», mantém a questão aberta e evita iniciar trabalhos que dependam de uma hipótese não autorizada. Pode, entretanto, avançar naquilo que é independente da decisão pendente.

O [prompt de discovery de produto](../../../../prompts/PRODUCT_DISCOVERY_SESSION.md) e a [documentação sobre requisitos e entrega](../../../21_PRODUCT_DISCOVERY_REQUIREMENTS_STACK_AND_DELIVERY.md) fornecem referências. São meios de investigação, não substitutos da responsabilidade do CLIENT por escolhas relevantes.

## 4. Baseline de produto e plano de entrega

Uma vez confirmada a necessidade, o Planner regista uma linha de base: objetivo, público, comportamentos, critérios de aceitação, exclusões, restrições e decisões abertas. Separadamente, engenharia reconstrói uma linha de base técnica: linguagem, bibliotecas, banco, interfaces, ambiente de execução, proteção de dados, testes e eventuais serviços externos.

Estas duas linhas de base não são intercambiáveis. Uma escolha técnica não prova que o CLIENT desejou o comportamento; uma especificação de produto não prova que o código atual a realiza. O vínculo entre ambas deve apontar para fonte concreta e estado atual verificável.

O plano de entrega divide o resultado em capacidades demonstráveis e dependências. Para um clube: identidade de associados, mensalidades, atividades, inscrições. Se uma capacidade depende da anterior, o Planner deve evitar autorizar várias campanhas incompatíveis sobre a mesma interface. O critical path deve ser revisto quando mudam datas, custos ou requisitos.

Marcos como «cadastro utilizável» são melhores que «100 commits de backend». O primeiro permite observar uma tarefa; o segundo mede atividade. Uma previsão tem de explicitar pressupostos e riscos, não transformar uma data pretendida em promessa de entrega sem evidência de capacidade.

O resultado pode ser compacto. A qualidade vem de decisões verificáveis, owners e interfaces claras. Não há benefício em manter vários ficheiros que duplicam os mesmos requisitos atuais e se contradizem após cada mudança. Use a superfície canónica prevista pelo projeto.

## 5. Adoção: relacionar starter e aplicação

A adoção transforma um controlo genérico num sistema relacionado com a aplicação real. Não consiste em copiar os ficheiros do exemplo nem em atribuir valores arbitrários a schemas. O Planner e a engenharia identificam Product State, donos das fontes, referências Git, dados e testigos atuais, mapeiam interfaces e estabelecem uma rota de recuperação.

O [contrato de transferência e adoção](../../../16_TRANSFER_ADOPTION.md) descreve formatos e verificações. A especificação concreta tem de ser validada antes de promover o estado. O processo não deve fazer mutações materiais enquanto existirem contradições de autoridade, snapshots de DB insuficientes ou dependências que não foram reconfirmadas.

Um projeto com código mas sem governação pode receber a camada de controlo de forma não destrutiva. Um projeto que já possui outro Product State requer uma rota de attachment de leitura, migração cuidadosamente autorizada ou convivência explicitamente delimitada. A palavra «instalação» não é licença para substituir a fonte da verdade existente.

Os dados persistentes merecem especial cuidado. Um snapshot válido deve representar estado transacionalmente consistente quando a aplicação utiliza SQLite com WAL ou outro mecanismo equivalente. Um hash do ficheiro principal isolado não prova que as últimas escritas estejam representadas. Se faltar um testemunho relevante, o estado dependente deve ficar em HOLD.

O mesmo vale para os artefactos. Não basta apontar para `final.pdf` ou `demo.mp4` se o conteúdo mudou. Versão, hash, fonte, contexto de geração e rights devem ser rastreáveis quando afetam aceitação ou reutilização. O custo de guardar evidência deve ser proporcional: não duplique gigabytes de ficheiros só para criar uma cópia para cada agente.

## 6. O exame decisivo de um contexto fresco

Uma adoção ainda não é confiável se só o agente que a escreveu consegue interpretá-la. O teste de contexto fresco pede que outra sessão, sem memória da conversa anterior, descubra o projeto, identifique o Product State, distinga requisitos confirmados de perguntas abertas e indique a próxima ação permitida.

O comando `reconstruct_context.py` instalado oferece uma verificação portátil desse mecanismo. Pode detetar relações incoerentes ou fontes não reconciliadas, mas não substitui uma leitura competente da aplicação. A reconstrução deve ser conferida com evidência real: ref atual, owners, campanha, plano, estado da DB, artefactos e eventuais journals pendentes.

Se um novo agente identifica dois charters como atuais para a mesma capacidade ou encontra um relatório que aponta para código antigo, deve preservar a contradição e investigar. Não escolhe o estado mais recente por data de ficheiro nem assume que o último chat tinha razão. O sistema falha de forma segura quando não consegue demonstrar currentness.

Um resultado `HOLD` pode ser correto. Deve dizer qual dado falta, porque importa e quem pode obtê-lo. Uma mensagem vaga «não consigo continuar» é menos útil que «a DB usa WAL e não há snapshot consistente correspondente ao ref autorizado; leituras seguras continuam, mas escrita material está suspensa».

## 7. Primeira campanha autorizada

Depois de adoção coerente, o Planner prepara a primeira campanha por capacidade. O charter delimita o que será entregue, porque importa, que interfaces serão afetadas, responsabilidades, dependências, critérios de aceitação, riscos e falsificadores. Não prescreve cada ficheiro e microtarefa que I3 deve modificar.

Uma passagem estratégica completa examina o produto final, currentness, DB, recuperação, segurança, custos, concorrência, licenças, revisão humana e interações com outras capacidades. Uma segunda passagem adversarial procura contradições ou pressupostos frágeis. Uma terceira é excecional, justificada por risco sistémico ou evidência nova material, não por qualquer bug encontrado num teste.

Depois da autorização, I3 tem espaço operacional para implementar e corrigir. O Planner não deve interromper para reformular a arquitetura a cada falha de CI, refactor interno ou necessidade de retry. Se a revisão terminal identificar problemas dentro do charter, devolve falsificadores consolidados à mesma campanha.

É aqui que a autonomia técnica se torna concreta: o CLIENT aprova a direção e os limites do produto; o Planner governa a estratégia; o Controller trata das dificuldades de engenharia até existir uma entrega verificável. O trabalho pode usar um ou vários especialistas, mas a autoridade e a evidência não se perdem entre eles.

## 8. Exemplo de sessão inicial com o Planner

Uma pessoa diz: «Quero uma aplicação local para controlar inscrições num clube. Hoje tenho uma planilha e preciso de algo que funcione daqui a um mês». O Planner não deve responder com uma escolha aleatória de cloud, microserviços e agentes. Primeiro investiga se existem dados reais, quem utiliza a ferramenta e qual a menor tarefa que precisa de melhorar.

Uma resposta organizada começa por esclarecer o objetivo, confirmar se há mais de um operador e perguntar quais regras determinam inscrição e cancelamento. Depois identifica a pasta de código existente, se existe, e o ambiente onde a aplicação terá de executar. Se o prazo é curto, propõe uma primeira capacidade que possa ser testada e uma lista explícita de exclusões.

O Planner regista decisões e prepara o baseline. Se a aplicação já tiver código com autenticação e uma base de dados, não reimplementa tudo só para encaixar o starter. Se o repositório estiver vazio, escolhe uma tecnologia proporcional e explica impactos significativos de manutenção ou instalação. O produto e os riscos determinam o stack, não o inverso.

No fim da sessão o CLIENT deve saber o que foi confirmado, o que ficou em aberto, qual é o primeiro resultado a ver e que decisão ainda precisa tomar. Não precisa compreender a sintaxe de todos os schemas de governança para conseguir aprovar um objetivo.

## 9. Um baseline confirmado pelo CLIENT

Um resumo de uma página pode dizer: «O sistema permite a um administrador registar associados, consultar o histórico e gerir mensalidades em computador local. Não processa pagamentos online. O histórico deve ser mantido após a desativação. A primeira demo deve realizar alta, pesquisa, edição e readback persistente». Se estas frases forem confirmadas pelo CLIENT, podem virar requisitos explícitos.

A engenharia acrescenta informação verificável: código e ref adotados, versão do interpretador, biblioteca de persistência, formato dos backups, eventuais riscos de dados pessoais e comandos de teste. As preferências ainda desconhecidas permanecem identificadas como pendentes; não se inventam aprovações ou prazos de terceiros.

Esse baseline permite rejeitar uma funcionalidade que não responde ao pedido. Se alguém criar um painel bonito mas não conseguir gravar um associado, o resultado visual é insuficiente. Se alguém adicionar pagamentos online apesar da exclusão, ultrapassou o contrato. Os critérios de aceitação devem observar a experiência de uso, os dados e o comportamento real.

Um requisito pode mudar após feedback. Nesse caso regista-se a supersessão e avaliam-se downstream e compatibilidade com o charter. Não se mantém simultaneamente uma regra antiga e uma regra nova como verdade canónica para o mesmo assunto.

## 10. Exemplo de primeira campanha

Uma primeira campanha pode ter como objetivo «Gestão de associados com persistência verificável». O resultado esperado inclui criar, encontrar, editar e desativar um associado fictício, mantendo histórico relevante. As interfaces afetam formulário, API ou camada de aplicação, operações de DB e pesquisa. O charter define limites de dados e segurança e deixa o desenho interno ao Controller.

Os gates poderiam envolver testes unitários de validação, integração de criação e pesquisa, readback após reinício, casos negativos de duplicados, segurança de permissões, prova física da interface e revisão independente. O CLIENT participa onde comportamento e experiência exigem julgamento humano. Nenhum gate substitui outro que tenha relevância para a funcionalidade.

Se uma desativação apagar pagamentos anteriores apesar do requisito, I3 corrige no mesmo charter. Se o CLIENT pedir uma função de exportação fiscal que não estava prevista, o Planner avalia a nova necessidade, os dados e as autorizações. Saber distinguir estas rotas evita burocracia excessiva e alterações não consentidas.

Ao concluir, o Controller apresenta identidade exata do candidato, testes realmente executados, evidência dos passos, reviewer, limitações e resultado. O Planner decide aceitar ou devolver falsificadores. O novo Product State deve refletir a decisão competente, e a próxima campanha deve depender da capacidade que foi de facto aceite.

**A seguir:** capítulo 03, operação diária, controle de execução e continuidade.

## Fontes e âmbito

- [Discovery de produto](../../../../prompts/PRODUCT_DISCOVERY_SESSION.md)
- [Requisitos e entrega](../../../21_PRODUCT_DISCOVERY_REQUIREMENTS_STACK_AND_DELIVERY.md)
- [Transferência e adoção](../../../16_TRANSFER_ADOPTION.md)
- [Attachment de governação existente](../../../32_EXISTING_GOVERNED_ATTACHMENT.md)
- [Padrão de charter](../../../../protocols/CAMPAIGN_CHARTER_STANDARD.md)
- [Limites do CLIENT](../../../../protocols/CLIENT_BOUNDARY.md)

Um baseline só é atual quando vinculado a decisões, fontes e estado verdadeiros. Os exemplos de clube deste manual não servem como aprovação de um produto real.
