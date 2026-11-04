# 04 — Solicitar mudanças e novas capacidades

ArquitecturaRepo · Manual completo de utilização · Edição v1.4 · Português

> Um pedido de alteração deve comunicar **o comportamento de produto pretendido**, o contexto e a forma de comprovar o resultado. O CLIENT não tem de desenhar a implementação. O Planner avalia decisões novas e impacto estratégico; I3 resolve defeitos e alterações técnicas dentro da campanha já autorizada.

## Neste capítulo

1. Descrever o resultado que se quer obter
2. Distinguir novo requisito, bug e refactor
3. Um formato simples para pedir alterações
4. Prioridades, orçamento e critical path
5. Alterações que afetam dados e segurança
6. Feedback sobre UX e aceitação humana
7. Devolução de defeitos ao mesmo Controller
8. Como evitar campanhas e políticas duplicadas
9. Exemplos de pedidos bem delimitados
10. Confirmar que a alteração ficou atual

## 1. Descrever o resultado que se quer obter

Um utilizador não deveria precisar de escrever um mini-charter técnico para pedir algo útil. Pode dizer: «Quero encontrar as mensalidades vencidas por associado e ver a data do último pagamento». A frase descreve uma tarefa observável. O Planner aprofunda as regras que faltam, identifica dependências e decide onde essa capacidade se encaixa no produto.

Uma instrução como «melhora o backend» é muito ampla. Não explica qual problema existe nem que comportamento provar. «A pesquisa de associados demora demasiado quando temos cinco mil registos; quero obter resultados corretos sem esperar muito» é mais útil porque permite investigar desempenho real, ambiente e compromisso aceitável. Não é necessário impor previamente índices, caching ou framework.

As decisões funcionais pertencem ao CLIENT. Um agente pode propor opções, exemplos e trade-offs, mas não pode apresentar a sua preferência como requisito aprovado. Engenharia decide detalhes de implementação dentro dos limites confirmados. Essa separação permite que alguém sem experiência técnica participe plenamente na direção do produto.

O pedido deve indicar o que acontece hoje, o que deveria acontecer, quem é afetado e como saberíamos que foi corrigido. Se existir um vídeo ou captura demonstrando o problema, pode ser útil desde que não exponha dados confidenciais e esteja vinculado ao candidato real. Uma descrição clara vale mais do que uma grande quantidade de screenshots sem contexto.

## 2. Distinguir novo requisito, bug e refactor

Três situações podem parecer parecidas na conversa, mas têm owners e rotas diferentes. Um **novo requisito** altera o comportamento desejado. Um **bug** viola um comportamento já confirmado. Um **refactor** modifica estrutura técnica sem alterar a regra de produto prometida.

Suponha que o clube acordou que desativar um associado mantém o histórico de pagamentos. O sistema apaga esse histórico: é um bug dentro do charter. I3 corrige a persistência, testa e submete o novo candidato. Não precisa de uma campanha estratégica nova para «corrigir histórico».

Agora o CLIENT pede reativação de associados anteriormente desativados. Se a regra nunca foi definida, existe decisão nova: quem pode reativar, que identidade regressa e como ficam quotas em atraso. O Planner confirma os detalhes e avalia o impacto. Não é correto declarar que qualquer comportamento anterior era defeito sem um requisito que o estabeleça.

Um refactor, como dividir uma classe muito grande em componentes, pode estar ao alcance de I3 se serve o charter e preserva contratos. Se afetar interfaces públicas, migrações de dados ou compatibilidade de um downstream, a mudança pode tornar-se material. A classificação depende de efeitos e autoridade, não da etiqueta escolhida pelo programador.

| Situação | Rota habitual |
| --- | --- |
| A funcionalidade já aprovada falha num caso. | I3 investiga e corrige na mesma campanha. |
| O CLIENT pede comportamento novo. | Planner confirma requisito e impacto antes de autorizar. |
| O código é reorganizado sem mudar a capacidade. | I3 executa com testes e revisão dentro do charter. |
| Um problema revela inconsistência entre produtos ou owners. | Coordenação estratégica apropriada, possivelmente I1. |
| Um serviço externo exige nova despesa ou permissão. | Aprovação reservada antes de realizar o efeito. |

## 3. Um formato simples para pedir alterações

Não é preciso um formulário complicado. Para muitas mudanças basta comunicar cinco elementos: resultado observado hoje, resultado esperado, contexto, restrições e um critério concreto de aceitação. O Planner transforma essa informação numa decisão e num charter de capacidade quando necessário.

Por exemplo: «Na lista de associados, uma pessoa inativa aparece como ativa. Quero que a pesquisa de ativos a exclua, mas que os pagamentos anteriores continuem disponíveis a administradores. A correção está feita quando a pesquisa e o readback após reinício confirmarem essa regra no ambiente real». Se a regra já constava do charter, isso é uma descrição de bug diretamente executável.

Outro exemplo: «Na próxima versão quero poder exportar um relatório mensal em CSV para a tesouraria; deve incluir totais, não números de telefone». É uma capacidade nova. O Planner confirma período, formato, permissões, dados sensíveis e impacto na DB. Engenharia decide como gerar CSV, testes e estrutura de exportação, respeitando as restrições.

O CLIENT pode também fornecer referências visuais e preferências de experiência: «A tela de reservas deve mostrar vagas disponíveis antes de pedir os dados pessoais». A equipa testa a viabilidade e, quando a UX importa, apresenta opções para avaliação humana. Não se devem inventar gostos, aprovações ou objetivos comerciais com base em padrões genéricos.

## 4. Prioridades, orçamento e critical path

Mudar prioridade não é necessariamente mudar requisitos. Uma funcionalidade aprovada pode ser adiada por tempo ou capacidade, mantendo-se válida. Já alterar uma regra funcional exige atualizar a fonte canónica e avaliar efeitos nos módulos dependentes. Uma boa gestão distingue calendário, escopo e comportamento.

O Planner deve perceber o critical path real. Se inscrever membros depende do estado das quotas, não faz sentido declarar a campanha de inscrições independente de dados de pagamento ainda provisórios. Também não se deve impedir todo o trabalho caso existam componentes demonstravelmente independentes que possam avançar sem risco de integração.

Quando há prazo curto, a primeira entrega deve ser a menor capacidade que fornece valor comprovável. Um CRUD simples e durável pode ser melhor prova de conceito do que uma arquitetura de microserviços com os endpoints principais ainda falsos. Essa escolha não significa aceitar qualidade baixa, mas proteger o resultado observável.

O custo precisa de contexto: horas de desenvolvimento, infraestrutura, dados, revisão humana, operação e serviços externos. O número de agentes ou tokens não mede valor. Um mecanismo novo tem de desbloquear capacidade ou reduzir risco material; caso contrário aumenta complexidade e custo sem melhorar o produto.

Uma mudança que exige cobrança, publicação ou manipulação irreversível de dados não pode ser executada apenas porque o agente achou uma solução. O CLIENT ou responsável autorizado deve aprovar o efeito específico. O Planner documenta a decisão; I3 prepara preflight e executa apenas dentro dos limites concedidos.

## 5. Alterações que afetam dados e segurança

Algumas mudanças parecem pequenas na interface, mas têm consequências profundas. «Eliminar associados duplicados» pode apagar histórico legítimo. «Mostrar relatórios para todos» pode expor dados pessoais. «Atualizar a versão da DB» pode quebrar migrações ou backups. A forma correta de avaliar depende de dados, lineage, owners e recuperação.

O Planner reconstrói entradas e saídas, fontes de verdade, consumidores downstream, semântica de invalidation e gates. Engenharia identifica migrações, relações, locks, idempotência e rollback técnico. Se existir um snapshot SQLite/WAL, deve ser transacionalmente consistente; caso contrário a leitura de currentness pode estar errada.

Um pedido de remoção de dados precisa distinguir eliminação lógica, desativação, retenção obrigatória e apagamento físico. O CLIENT confirma a regra e permissões. O Controller não deve usar scripts destrutivos amplos sem resolver o alvo exato e sem proteger dados não abrangidos pela autorização.

O mesmo princípio aplica-se a artefactos. Um PDF de relatório ou um render de vídeo pode depender de fonte, configuração, licença e versão. Se um input relevante mudou, a validade de artefactos derivados pode ter de ser revista. Não basta renomear um ficheiro como `final` para o tornar atual.

Segurança proporcional significa avaliar a exposição e o impacto reais. Um protótipo privado local não exige os mesmos mecanismos de uma plataforma pública com pagamentos, mas ambos precisam de respeitar segredos e não publicar dados confidenciais sem autorização.

## 6. Feedback sobre UX e aceitação humana

Uma pessoa pode achar uma interface difícil de usar apesar de todos os testes automatizados estarem verdes. A avaliação perceptual é um gate distinto. O feedback útil especifica a tarefa, o público e o problema observado: «Quando uma reserva falha por falta de vagas, o aviso não explica o que fazer» é mais concreto do que «a interface está feia».

Preferências visuais legítimas pertencem ao CLIENT ou a avaliadores humanos apropriados. Engenharia pode propor alternativas e explicar trade-offs, mas não deve assumir que a primeira composição aprovada num teste sintético é o design final. A demonstração deve utilizar o candidato exato, com dados fictícios e ambiente representativo.

Um comentário de UX pode ser um bug se contraria um comportamento já confirmado; pode ser uma mudança de produto se acrescenta uma regra nova; ou pode ser um ajuste em envelope de implementação. Classificar corretamente evita que cada pedido de alinhamento visual gere um novo planejamento estratégico.

Ao recolher feedback, proteja privacidade. Capturas com nomes, emails, tokens e informação de clientes não devem ser colocadas em PRs ou issues públicos. Um exemplo sintético pode reproduzir o problema sem divulgar dados reais. A revisão humana deve dizer o que viu, não atribuir aprovações a quem não participou.

## 7. Devolução de defeitos ao mesmo Controller

Quando o Planner rejeita um terminal por problemas dentro do charter, devolve a I3 um conjunto **consolidado de falsificadores**. Cada item explica esperado, observado, candidato, evidência e gate. O Controller pesquisa a causa, corrige, testa e integra um novo candidato com revisão independente adequada.

Não se cria nova campanha, novo charter nem PASS extra porque uma fixture falhou. Esse tipo de churn faz o Planner trabalhar como um depurador de primeira linha e obriga o CLIENT a acompanhar engenharia que já devia ter ownership operacional. O charter permanece vigente até existir aceitação estratégica real ou invalidation material.

Se o mesmo subsistema falhar repetidamente, I3 deve interromper a sequência de microcorreções e realizar hardening abrangente. Isso pode implicar estudar as transações, procurar falhas semelhantes, reforçar testes de regressão e usar revisão independente. O objetivo é eliminar a classe de defeitos, não colecionar terminais parcialmente verdes.

Uma mudança de comportamento pedida pelo CLIENT não deve ser escondida como bug fix. Do mesmo modo, um erro ordinário não deve ser inflacionado para invalidation estratégico. A diferença protege a velocidade e a autoridade de quem decide o produto.

## 8. Como evitar campanhas e políticas duplicadas

O sistema funciona melhor quando cada preocupação tem um owner canónico e uma superfície atual. Se duas campanhas editam o mesmo recurso sem coordenação, podem gerar referências incompatíveis. Se dois documentos dizem qual é o estado `CURRENT`, uma sessão nova pode escolher o errado.

Antes de criar um ficheiro ou política nova, procure o contrato existente. Uma atualização pequena ao lugar correto é preferível a outra cópia de verdade. As decisões de produto, estado mutável, autoridade de campanha e transporte/runtime devem permanecer conceitualmente separados, embora estejam ligados por referências verificáveis.

Reaproveitar artefactos também exige lineage e identidade. Se um relatório aprovado é reutilizado numa nova feature, registe a relação e invalide quando inputs relevantes mudarem. A contagem de documentos e commits não é prova de que essa rede de referências esteja coerente.

Um MASTER OWNER deve detetar churn sistémico, duplicação de políticas e falhas de integração entre workstreams. A solução apropriada é corrigir o owner e o processo que causam a repetição, não adicionar mais um nível de aprovação a cada bug.

## 9. Exemplos de pedidos bem delimitados

**Caso A — Filtro de mensalidades.** «Preciso identificar associados que não pagaram o mês atual. O cálculo deve considerar pagamentos parciais e permitir verificar o histórico». O Planner pergunta pela definição de período e pagamento parcial, confirma a regra e delimita consultas, permissões e testes. I3 implementa com fontes de dados atuais.

**Caso B — Corrigir perda de informação.** «Quando desativo um associado, os pagamentos desaparecem após reiniciar. O requisito era preservá-los». Trata-se de bug in-charter. I3 investiga persistência e restaura o comportamento, mantendo evidência do candidato anterior e do novo.

**Caso C — Novo relatório CSV.** «A tesouraria necessita exportar totais por mês sem dados pessoais». É nova capacidade. O Planner define formato, público, autorização e limites. Engenharia escolhe geração, casos negativos e cuidado com formula injection quando pertinente.

**Caso D — Melhorar uma tela.** «O botão de cancelar reserva fica oculto no telemóvel e o cliente não consegue concluir a tarefa». É necessário verificar o layout no dispositivo relevante e avaliar se a alteração se encontra no envelope já autorizado. Uma captura isolada em desktop não prova a correção.

**Caso E — Migrar base de dados.** «Queremos passar de armazenamento local para um servidor partilhado». A mudança tem implicações de rede, backup, custos, concorrência e segurança; requer avaliação estratégica, plano de migração, critérios de rollback e provas de conservação de dados.

O que estes exemplos partilham não é um template rígido de prompts. É a separação entre a intenção humana, as decisões ainda abertas, o trabalho técnico e a evidência exigida para afirmar que o resultado foi alcançado.

## 10. Confirmar que a alteração ficou atual

Depois de integrar um candidato, não basta mostrar um diff ou repetir «feito». É necessário verificar que o comportamento exigido funciona no ambiente relevante e que Product State, fonte, DB e artefactos afetados correspondem ao candidato submetido. A revisão deve ser realizada sobre essa identidade, não sobre outra versão com nome parecido.

O Planner audita o terminal e regista a decisão apropriada. O CLIENT faz a aceitação que lhe compete, por exemplo da experiência visual. Se um downstream depende da nova regra, é preciso verificar que a referência para a capacidade aceite está atual antes de iniciar trabalho dependente.

Uma sessão futura deve recuperar essa decisão sem consultar o chat original. Se encontrar dois requisitos contraditórios, um link quebrado ou evidência de um candidato antigo, não inventa continuidade: reconcilia ou declara HOLD concreto. A qualidade da mudança inclui a capacidade de ser compreendida e mantida posteriormente.

Um pedido de alteração bem realizado termina com menos incerteza sobre o produto, não apenas mais código. O sistema deve deixar claro o que mudou, porquê, quem aprovou a regra, o que foi testado e que próximo passo está autorizado.

**A seguir:** capítulo 05, erros, incidentes e recuperação sem perder a verdade do projeto.

## Fontes e âmbito

- [Limite das decisões do CLIENT](../../../../protocols/CLIENT_BOUNDARY.md)
- [Padrão de charter de engenharia](../../../../protocols/CAMPAIGN_CHARTER_STANDARD.md)
- [Ciclo de capacidades e evidência](../../../../protocols/CAPABILITY_LIFECYCLE_AND_EVIDENCE.md)
- [Requisitos, stack e plano de entrega](../../../21_PRODUCT_DISCOVERY_REQUIREMENTS_STACK_AND_DELIVERY.md)
- [Integridade de revisão e terminal](../../../../protocols/REVIEW_FREEZE_AND_TERMINAL_INTEGRITY.md)
- [Primeiro uso v1.4](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md)

Os pedidos fictícios não criam requisitos nem campanhas reais. O produto e as fontes atuais determinam a autoridade e a evidência necessária.
