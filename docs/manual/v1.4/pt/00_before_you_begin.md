# 00 — Antes de começar

ArquitecturaRepo · Manual completo de utilização · Edição v1.4 · Português

> O ArquitecturaRepo é uma arquitetura de coordenação de desenvolvimento, não um programador automático nem uma aplicação pronta. Ajuda a manter decisões de produto, responsabilidades, evidências e estado atual reconstruíveis mesmo quando uma conversa, ferramenta ou agente deixa de estar disponível. A edição pública v1.4 tem limites de suporte precisos: consulte o [guia público atual](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md) e as [notas de lançamento](../../../47_V1_4_RELEASE_NOTES_AND_UPGRADE.md) antes de executar comandos sensíveis à versão.

## Neste capítulo

1. O que está a instalar e para quê
2. Quem decide cada questão
3. Informação que deve permanecer acessível
4. Como utilizar este manual
5. Preparação das decisões que só o CLIENT pode tomar
6. Alcance, limites e versões
7. Um percurso de ponta a ponta
8. Decisões frequentes e responsabilidades
9. Ficha de arranque de uma página
10. Como avaliar se o sistema está a ajudar

## 1. O que está a instalar e para quê

Imagine uma pessoa a desenvolver um produto com ajuda de um chat de programação. Num dia, o assistente cria código, sugere uma arquitetura e resolve um problema. No dia seguinte, a conversa termina, entra outro agente e parte das decisões essenciais perdeu-se entre mensagens. Pode existir muito código, mas ninguém consegue explicar com segurança qual é o resultado pretendido, que ficheiros são os atuais ou porque se escolheu determinada abordagem.

O ArquitecturaRepo procura resolver essa fragilidade. A fonte de verdade fica no repositório e nas superfícies canónicas autorizadas, com referências para requisitos, Product State, responsabilidades, campanhas de engenharia, alterações, testes e evidências. O chat continua útil como interface de colaboração, mas deixa de ser o único local onde existe a história necessária para continuar o trabalho.

Uma instalação inicial acrescenta uma camada `.agentic-sdlc/` ao projeto de destino quando esse projeto não possui já governação canónica incompatível. Essa camada contém contratos, modelos de estado, documentação e ferramentas de validação. Não acrescenta automaticamente uma interface, uma API, um esquema de produção ou uma conta de inteligência artificial. Também não dá autorização para consumir serviços pagos, publicar conteúdo ou manipular dados reais de terceiros.

O valor esperado não é aumentar o número de papéis ou relatórios, mas reduzir três custos concretos: voltar a explicar decisões, perder a identidade do trabalho atual e aceitar resultados sem evidência suficiente. Se a estrutura consumir mais esforço do que o risco que evita, deve ser simplificada dentro dos limites aplicáveis.

## 2. Quem decide cada questão

O sistema distingue autoridades. O CLIENT é a pessoa que quer o produto: decide necessidades, prioridades, preferências, restrições e efeitos externos reservados. Pode não compreender Git, bases de dados, transações ou as particularidades de cada ferramenta. Isso não deve obrigá-lo a coordenar manualmente todos os detalhes técnicos.

O I2 Planner reconstrói a situação real, clarifica requisitos, define capacidades e dependências, propõe a estratégia e audita o terminal de uma campanha. Antes de autorizar uma alteração material deve fazer uma reconstrução completa e uma passagem adversarial independente. Esse esforço estratégico não tem de ser repetido como uma cerimónia a cada bug normal de implementação.

O I3 Controller recebe um charter autorizado e assume a execução contínua: programação, testes, integração, refatorações dentro dos limites, recuperação de falhas, correções, revisão independente e novos candidatos. Um erro de regressão não cria uma nova campanha por si só. Quando um defeito de uma mesma classe regressa repetidamente, o Controller deve investigar e endurecer o subsistema por inteiro.

O I4 é um papel opcional de execução ou revisão especializada. Não significa que sejam obrigatórios quatro modelos diferentes nem quatro conversas abertas. O I1 MASTER OWNER pode ser útil quando existe um portefólio de produtos, vários workstreams que precisam de integração ou conflitos de ownership relevantes. Para uma aplicação pessoal simples, uma organização mais pequena pode cumprir o mesmo contrato com menor custo.

| Pergunta | Autoridade habitual |
| --- | --- |
| «Que problema vamos resolver e para quem?» | CLIENT, com discovery conduzido pelo Planner. |
| «Que capacidade deve ser entregue primeiro?» | Planner, respeitando prioridades confirmadas pelo CLIENT. |
| «Qual o índice ou transação de DB apropriados?» | Engenharia no charter, sob responsabilidade de I3. |
| «A funcionalidade corresponde às regras já acordadas?» | Testes e revisão técnica; auditoria estratégica do Planner. |
| «A aparência é boa para os utilizadores previstos?» | Gate humano/perceptual competente, incluindo o CLIENT se apropriado. |
| «Podemos pagar, publicar ou enviar dados para fora?» | Autoridade explícita do CLIENT ou do responsável legal aplicável. |

## 3. Informação que deve permanecer acessível

Uma pessoa nova deve conseguir reconstruir o produto sem exigir que o CLIENT releia centenas de mensagens. Para isso é importante manter em superfícies canónicas distintas a intenção aprovada, o estado mutável atual, a autorização de uma campanha e a evidência produzida pelo runtime. Misturar tudo num único relatório longo cria contradições e dificulta saber qual dos documentos tem autoridade.

O repositório guarda código e decisões versionadas; a DB ou outro armazenamento canónico pode conter dados vivos; o Product State indica o que está atual e porquê; os artefactos e manifests documentam resultados; logs e journals ajudam a compreender transações interrompidas. Uma mensagem recente de um agente não é suficiente para substituir uma destas fontes, mesmo quando parece convincente.

Uma situação frequente ilustra o problema. Um revisor aprovou o candidato A. Mais tarde alguém alterou o código e gerou B sem repetir a revisão. O nome da branch continua igual, mas a aprovação de A não valida B. A identidade exata da fonte, configuração, DB e artefactos evita aceitar por engano evidência de uma versão anterior.

Outro caso envolve SQLite em modo WAL. O ficheiro principal da base de dados pode não representar todo o estado atual enquanto existirem transações no write-ahead log. Uma referência ao hash do ficheiro isolado pode ser insuficiente. O sistema deve preservar um testemunho consistente da DB ou declarar incerteza concreta, sem inventar uma prova de currentness.

## 4. Como utilizar este manual

Estes oito capítulos formam a edição extensa. Podem ser lidos em sequência na primeira utilização, mas também funcionam como referência. O capítulo 01 trata da instalação; o 02 explica discovery e adoção; o 03 aborda sessões de trabalho; o 04 ensina a solicitar mudanças; o 05 apresenta erros e recuperação; o 06 cobre aceitação; o 07 percorre um clube fictício desde a ideia até às provas necessárias.

Se pretende experimentar o framework em poucos minutos, a [miniguia em português](../../../i18n/MINI_GUIDE_pt.md) é mais direta. É intencionalmente curta e não substitui este livro. A [FAQ em português](../../../i18n/FAQ_pt.md) responde a questões frequentes; a documentação técnica do repositório serve de fonte precisa sobre versões e contratos.

Não é necessário memorizar cada nome de ficheiro interno. É mais importante saber que perguntas fazer, quem pode decidir, onde procurar a referência atual e quando bloquear uma alteração que depende de evidência desconhecida. O capítulo de instalação fornece comandos de exemplo, mas as opções efetivamente disponíveis devem ser verificadas na versão do script utilizado.

Para estudar, escolha um produto real ou fictício e escreva primeiro o objetivo em termos observáveis. Evite começar por desenhar uma frota de agentes ou por distribuir tarefas de código sem uma compreensão do problema. Depois compare os resultados físicos com as decisões preservadas. A experiência torna-se mais clara quando se associa cada conceito a uma ação concreta.

## 5. Preparação das decisões que só o CLIENT pode tomar

Antes de instalar, o CLIENT pode preparar uma descrição simples: quem utiliza o produto, que tarefa pretende executar, qual o primeiro resultado demonstrável, quais são os limites de custo e prazo, que dados são sensíveis e que ações exigem autorização. Nem tudo precisa estar decidido. A documentação deve separar requisitos confirmados de perguntas abertas, sem transformar hipóteses técnicas em vontade do utilizador.

Por exemplo, «quero gerir associados» ainda não determina se os associados pagam quotas, se há dois tipos de acesso, se uma baixa elimina o histórico ou se o sistema funciona sem internet. O Planner pergunta porque essas respostas mudam o comportamento do produto. Já a escolha entre duas estruturas de classes equivalentes costuma pertencer à engenharia e não requer uma votação do CLIENT.

É razoável pedir uma primeira demonstração pequena, como cadastrar uma pessoa fictícia e encontrá-la depois de reiniciar a aplicação. O resultado pode ser medido. «Ter uma arquitetura profissional» isoladamente é difícil de aceitar e abre espaço para produzir muitos documentos sem entregar uma capacidade utilizável.

Os requisitos mudam com aprendizagem real. A arquitetura permite registar supersessões e manter evidência útil, não congelar o primeiro pensamento para sempre. Quando surge uma decisão material nova, o Planner atualiza o contrato apropriado. Quando surge um bug de uma regra já confirmada, I3 corrige no charter existente.

## 6. Alcance, limites e versões

A release pública [v1.4.0](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0) foi distribuída com um ZIP portátil, checksum e manifest. Para instalar de forma reproduzível, utilize o release exato e confira o hash do ficheiro descarregado. A branch `main` pode incluir documentação e melhorias posteriores; o que aparece em `main` não passa automaticamente a fazer parte dos bytes da release anterior.

A v1.4 verificou mecanismos portáteis do framework, incluindo o scaffold, perfis, reconstrução de contexto, recuperação e testes de contratos em ambientes Linux/Windows. Isso não prova que qualquer aplicação de terceiros, integração nativa com um host específico ou serviço de IA funcione. Uma funcionalidade externa necessita dos próprios testes, permissões e gates.

O projeto é neutro quanto a modelos: não obriga à utilização de um LLM, não instala credenciais de um fornecedor e não confere permissões de cobrança ou publicação. Pode ser utilizado para coordenar trabalhos executados por agentes ou por programadores humanos. O papel da ferramenta é preservar decisões e evidências, não assegurar que uma determinada tecnologia produza software correto sem verificação.

Os perfis `SMALL`, `STATEFUL`, `ARTIFACT_HEAVY`, `MULTI_WORKSTREAM`, `MULTI_PRODUCT` e `HIGH_CONSEQUENCE` ativam famílias proporcionais de controlos. Nenhum perfil, por si só, certifica segurança, qualidade de UX ou conformidade legal. A seleção depende dos riscos concretos; projetos pequenos não devem herdar toda a complexidade de sistemas maiores sem justificação.

Também importa distinguir instalações novas de projetos já governados. O scaffold genérico não é um sistema universal de migração do Product State de uma v1.2/v1.3 para v1.4. Se há um controlador canónico, dados e campanhas ativos, começa-se com o [preflight somente leitura](../../../32_EXISTING_GOVERNED_ATTACHMENT.md) e decide-se como reconciliar a autoridade, sem sobrescrever por conveniência.

## 7. Um percurso de ponta a ponta

Imagine o desenvolvimento de uma pequena biblioteca de reservas. O CLIENT define que uma pessoa autorizada deve criar reservas e verificar disponibilidade. O Planner pergunta por horários, conflitos, cancelamentos, permissões e prazo. As respostas confirmadas tornam-se requisitos de produto, com um baseline de fontes e ambiente.

Com o projeto adotado, o Planner autoriza um charter para a primeira capacidade. I3 implementa, testa, corrige falhas, integra um candidato exato e organiza a revisão apropriada. A prova física não é apenas um teste de função: alguém cria a reserva, consulta-a depois, verifica conflitos e reinicia o programa se persistência for necessária.

O Planner audita o terminal contra o comportamento confirmado. O CLIENT verifica as questões reservadas de produto e experiência. Se um teste revelar que reservas duplicadas são permitidas apesar do requisito contrário, I3 corrige dentro da mesma campanha. Se o CLIENT acrescentar uma política nova de prioridade para associados, trata-se de uma decisão de produto e avalia-se o impacto estratégico.

Depois da aceitação, o estado canónico aponta para o candidato e evidências corretos. Um novo agente pode continuar sem recomeçar o discovery nem depender da memória de quem implementou a primeira versão. Essa é a diferença entre um chat de programação com bons resultados pontuais e um processo de desenvolvimento durável.

## 8. Decisões frequentes e responsabilidades

**Posso usar só um chat e o repositório?** Sim, se conseguir respeitar os limites e manter estado atual verificável. O contrato não exige quantidade fixa de processos. Uma pessoa ou ferramenta pode desempenhar várias operações técnicas sem inventar autoridades conflituosas.

**É melhor que programar diretamente com Codex?** Depende do trabalho e da implementação real. Para um protótipo pequeno, a conversa direta pode ser mais rápida. Para um produto longo com várias capacidades, alterações de contexto, revisão e necessidade de continuidade, a arquitetura pode oferecer vantagens. Essas vantagens são uma hipótese verificável, não uma superioridade medida que o manual possa afirmar sem comparar resultados, qualidade e custo.

**O que acontece quando um agente erra?** Se o defeito cabe no charter, I3 resolve e retesta. A responsabilidade técnica não volta ao CLIENT a cada erro. O Planner regressa quando há terminal estratégico ou uma mudança material do contrato.

**O que significa `HOLD`?** É a decisão de não avançar com efeitos dependentes de dados ou autoridade ainda não reconciliados. Não significa que toda a análise esteja proibida. Podem continuar investigações seguras, relatórios read-only e propostas que não dependam da incerteza.

**E se o projeto for privado?** Pode continuar privado. A camada de controlo não precisa de enviar código, nomes de projeto, conversas, credenciais nem dados pessoais ao mantenedor. Qualquer integração externa deve respeitar privacidade, licença e autorização do responsável.

## 9. Ficha de arranque de uma página

Antes da primeira campanha, confirme que consegue responder aos pontos seguintes:

| Campo | Resposta necessária |
| --- | --- |
| Produto | Problema, pessoa utilizadora e primeiro resultado observável. |
| Repositório | Código verdadeiro, branch/ref atual, estado local e alterações pendentes. |
| Autoridade | CLIENT, Planner, Controller e eventuais owners de recursos partilhados. |
| Requisitos | Decisões confirmadas, dúvidas abertas e restrições de produto. |
| Ambiente | Linguagem, plataforma, dados, rede, custo e limites de permissões. |
| Estado | Product State e referências atuais sem contradições. |
| Campanha | Charter de capacidade, interfaces e falsificadores. |
| Evidência | Gates aplicáveis, candidato exato, revisões e testes físicos. |
| Continuidade | Próxima ação que um agente novo consegue recuperar sem ler o chat. |

Se faltar um item material, não o preencha com uma suposição só para deixar a tabela verde. Identifique o owner que pode obter a resposta. A ausência de uma preferência do CLIENT não é falha de código; a ausência de um hash não é decisão de produto; a ausência de um ambiente de testes não é motivo para aceitar um resultado simulado como físico.

Esta ficha não cria um segundo registo `CURRENT`: deve servir de índice para as fontes canónicas já existentes. A duplicação de superfícies vivas pode gerar mais confusão do que aquela que a arquitetura pretende resolver.

## 10. Como avaliar se o sistema está a ajudar

Depois de algumas sessões, pergunte se o projeto consegue continuar após trocar de agente, se as decisões permanecem claras, se houve menos trabalho perdido e se a pessoa utilizadora recebeu uma capacidade demonstrável. Não conte apenas commits, documentos, testes ou tokens; esses indicadores de atividade não são o produto.

Uma comparação honesta com uma abordagem de chat direto deve observar tempo total, quantidade de intervenções do CLIENT, qualidade de engenharia, taxa de regressões, facilidade de recuperar contexto e comportamento real da aplicação. O framework pode exigir custo inicial maior. Esse custo é justificável apenas quando traz redução mensurável de risco ou melhora de continuidade.

Não se deve adicionar uma nova regra ou camada só porque um problema foi difícil. O princípio de proporcionalidade permanece válido durante todo o desenvolvimento: o trabalho técnico deve servir o produto, e o sistema de governação deve servir o trabalho técnico. A melhor evidência é uma capacidade que funciona e que qualquer novo responsável autorizado consegue compreender e manter.

**A seguir:** capítulo 01, instalação e configuração segura da camada de controlo v1.4.

## Fontes e âmbito

- [Visão geral da arquitetura](../../../00_ARCHITECTURE_OVERVIEW.md)
- [Perfis de escala](../../../06_SCALING_PROFILES.md)
- [Limite de autoridade do CLIENT](../../../../protocols/CLIENT_BOUNDARY.md)
- [Ciclo de capacidades e evidências](../../../../protocols/CAPABILITY_LIFECYCLE_AND_EVIDENCE.md)
- [Primeiro uso público de v1.4](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md)
- [Notas de lançamento v1.4](../../../47_V1_4_RELEASE_NOTES_AND_UPGRADE.md)

Este capítulo explica um método e as suas limitações. Não certifica aplicações concretas, integrações externas nem comparações de desempenho não realizadas.
