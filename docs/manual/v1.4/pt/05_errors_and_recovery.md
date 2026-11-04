# 05 — Erros, incidentes e recuperação

ArquitecturaRepo · Manual completo de utilização · Edição v1.4 · Português

> Recuperar um projeto significa voltar a um estado **verdadeiro e verificável**, não apenas eliminar um erro do terminal. Preserve fonte, ownership, journal de transações, DB e evidência atual. Um bug comum dentro de um charter pertence a I3; uma contradição de autoridade ou currentness exige reconciliação apropriada.

## Neste capítulo

1. Preservar a evidência antes de reparar
2. Falhas do ambiente, contas e permissões
3. Quando a camada de controlo não valida
4. Git não é uma forma de apagar problemas
5. Repetição de defeitos e causas sistémicas
6. Segurança, privacidade e direitos externos
7. Provar a saída de um incidente
8. Três cenários de recuperação
9. Operações sensíveis e limites de autoridade
10. O que uma validação verde não demonstra
11. Feedback e dados locais do starter

## 1. Preservar a evidência antes de reparar

Quando ocorre um problema, guarde a mensagem exata, o comando ou ação que o provocou, data, diretório, fonte/branch, candidato e eventuais operações pendentes. Não apague por reflexo a pasta `.agentic-sdlc/`, a base de dados ou os logs. Uma reinstalação pode destruir precisamente a informação necessária para perceber o que aconteceu.

Primeiro classifique a falha. Pode ser uma ferramenta ausente, um problema de permissões, um bug da aplicação, um contrato de governação inválido, fonte antiga, uma transação incompleta, um fornecedor externo indisponível ou uma autorização do CLIENT ainda pendente. Essas causas têm owners e soluções diferentes.

| Sinal | Resposta inicial segura |
| --- | --- |
| Uma prova de integração de uma feature falha. | I3 conserva a reprodução e corrige na campanha vigente. |
| O validador rejeita uma referência canónica. | HOLD dependente, identificar relação, fonte e owner causais. |
| Git mostra mudanças locais e remotas incompatíveis. | Preservar ambas, estudar o diff e reconciliar. |
| Dados reais podem estar danificados. | Suspender escritas sensíveis, proteger backups, WAL e journals. |
| Falta permissão para publicar ou gastar. | Não executar o efeito até obter autorização específica. |
| Um host caiu durante uma operação. | Efeito desconhecido; fazer readback antes de reexecutar. |

Uma correção tem de resolver a causa e demonstrar o gate afetado. Uma melhoria cosmética que muda o estado de vermelho para verde pode deixar o produto defeituoso. Enquanto escritas materiais permanecem suspensas, muitas vezes é possível continuar a investigação read-only e preparar testes em ambiente isolado.

O CLIENT precisa de compreender a consequência do incidente e as decisões que lhe cabem, não a implementação de cada script de recuperação. O Controller é responsável por reproduzir e corrigir falhas dentro da sua autoridade. Uma escalada estratégica é necessária quando os limites do charter foram realmente invalidados.

## 2. Falhas do ambiente, contas e permissões

**Python ou comando não encontrado.** Confirme a versão, localização do executável, PATH e diretório de trabalho. Instale dependências declaradas, como `jsonschema`, usando fontes confiáveis. Não modifique um schema canónico para contornar uma dependência local ausente.

**Não consegue ler GitHub.** Diferencie autenticação, âmbito do token, visibilidade do repositório, instalação do conector e acesso à branch. Uma falha de leitura não autoriza a entregar credenciais em texto simples nem a ampliar permissões para toda a conta. Teste somente o acesso necessário e preserve a mensagem de erro.

**O agente abriu o projeto errado.** Compare caminho, branch, origem e ficheiros antes de escrever. Duas pastas com nomes semelhantes podem ter histórias diferentes. Se o runtime apontar para outro worktree, registe o desvio e volte a reconstruir a fonte atual de forma segura.

**Ocorreu timeout ou limite de utilização.** A sessão de um serviço não define a identidade da campanha. Goal, charter, candidatos, owner, checkpoints e ações pendentes pertencem ao estado durable. Um novo agente deve reconstruí-los sem inventar autorização. A falha do host não transforma automaticamente uma operação em «não executada».

**Permissão negada no sistema de ficheiros.** Descubra o alvo exato e porquê a operação requer escrita. Não tente contornar proteções para remover um diretório amplo. Se o contrato de segurança exige aprovação, pare a operação e obtenha-a, em vez de procurar outro meio de fazer o mesmo efeito sem permissão.

O tratamento de ambiente deve ser proporcional. Muitos problemas resolvem-se com um diagnóstico simples; outros revelam estado parcial que precisa de recovery. O que importa é não confundir a primeira mensagem de erro com a causa final.

## 3. Quando a camada de controlo não valida

O `tools/validate_project.py` instalado verifica contratos e relações de `.agentic-sdlc/`. Pode detetar ownership duplicado, referências CURRENT inconsistentes, candidato e revisão incompatíveis ou mudanças de schema incompletas. Não prova por si só que a aplicação abra, que um login funcione ou que a base de produção contenha os dados esperados.

Antes de alterar estado, guarde o erro, root de controlo, ref Git, alterações locais e testigos de DB. Investigue se falta uma dependência, se um owner foi supersedido, se há journal pendente ou se um terceiro modificou um destino. Não coloque `READY` manualmente num JSON nem apague o journal para obter um relatório verde.

As transições podem afetar vários ficheiros canónicos. O [protocolo de recuperação transacional](../../../12_TRANSACTION_RECOVERY.md) trabalha com hashes anteriores e posteriores e rejeita conflitos. Se a recuperação descobre que um ficheiro foi alterado por outro processo, deve preservar `CONFLICT`, não sobrescrever por comodidade. Depois é preciso validar os efeitos físicos e atualizar referências coerentes.

Em SQLite com Write-Ahead Logging, os bytes do ficheiro principal `.db` podem não conter todos os writes confirmados. É necessário um snapshot transacionalmente consistente quando o estado atual depende dele. A [rota de attachment de governação existente](../../../32_EXISTING_GOVERNED_ATTACHMENT.md) aborda esse testemunho; não é uma ferramenta automática de reparação da base de produção.

Se o teste de estrutura passa mas o Product State aponta para um candidate antigo, ainda existe problema de currentness. Se o estado é coerente mas a aplicação não arranca, existe problema físico. Os gates são distintos e não se substituem mutuamente. Um bom diagnóstico explica qual passou e qual continua pendente.

## 4. Git não é uma forma de apagar problemas

Quando Git mostra um conflito, não escolha cegamente «minha versão» ou «versão remota». Ambas podem conter trabalho útil. Investigue a base comum, diff local, alterações remotas e ownership do recurso. Uma estratégia de merge tem de preservar significado, não apenas produzir um repositório com status limpo.

Não use resets destrutivos ou elimine um checkout para escapar ao trabalho de conciliação. Se existirem ficheiros do utilizador, estado de uma campanha ou dados derivados que continuam a ter valor, devem ser preservados até ser possível provar que a limpeza não afeta autoridade nem evidência.

O starter fornece [inspeção incremental de delta](../../../../tools/repo_delta.py) e [inventário/limpeza de artefactos](../../../34_FILE_ARTIFACT_INVENTORY_AND_GC.md). Essas ferramentas não autorizam apagar código, dados humanos desconhecidos ou artefactos aceites. Uma operação de garbage collection começa por listar alvos e validar ownership; apenas recursos descartáveis e explicitamente identificados podem ser removidos.

Um nome de branch não prova quem produziu um commit, nem qual campanha o autorizou. A identidade do ator e a autoridade de execução devem vir de registos próprios. Se dois agentes afirmarem ter escrito a mesma mudança, o histórico Git pode ajudar a investigar, mas não substitui a cadeia de autorização.

Quando um ficheiro de configuração mudou depois da revisão, o reviewer deve avaliar o novo candidato na parte afetada. Um checkout limpo com código novo não transforma uma revisão anterior em evidência atual. A disciplina de fonte exata é tão importante na recuperação como na aceitação.

## 5. Repetição de defeitos e causas sistémicas

Um bug previsto pelo charter pertence a I3. Isso inclui testes falhados, correções de integração, pequenos refactors, recuperação de crashes e auditorias técnicas dentro do scope. Não há motivo para criar uma campanha nova ou pedir ao Planner um PASS estratégico adicional depois de cada defeito.

Se o mesmo tipo de problema regressa várias vezes, a resposta muda. Em vez de corrigir cada sintoma isoladamente e declarar novo terminal prematuro, o Controller investiga a classe inteira: contratos, dados, concorrência, testes, boundaries e revisões anteriores. Realiza hardening abrangente, novas provas relevantes e revisão independente.

Considere um módulo que perde pagamentos ao desativar associados. Se um patch resolve um caso mas continua a falhar com pagamentos parciais, não é suficiente trocar mais uma condição. É necessário compreender o modelo de persistência, relações, transações e regras de retenção, com casos negativos representativos e readback real.

O Planner volta quando existe terminal estratégico adequado ou evidência nova que invalida o charter. Aumentar a dificuldade de implementação não significa por si só que o produto tenha mudado. A cadeia de ownership protege a execução de ficar presa num ciclo de replaneamento.

O MASTER OWNER também deve reconhecer problemas sistémicos de governação: policies duplicadas, Controllers que devolvem bugs repetidamente, integrações entre workstreams com owner indefinido ou deadlines irrealistas. Nesse caso a correção recai sobre a causa do sistema, não sobre criar novas microcampanhas.

## 6. Segurança, privacidade e direitos externos

Os logs e exemplos públicos devem ser sanitizados. Não inclua tokens, senhas, nomes completos de clientes, caminhos pessoais, bases privadas, documentos de terceiros nem transcrições de conversas em issues ou relatórios que saem do projeto. Um defeito costuma poder ser reproduzido com dados fictícios e uma descrição técnica precisa.

A instalação do framework não autoriza o envio de código a fornecedores externos. Modelos e serviços são opcionais, e credenciais dependem do ambiente e de decisões específicas. Se uma solução exige um serviço pago, uma ligação de rede nova ou publicar algo, obtenha aprovação apropriada antes de executar o efeito.

As licenças devem ser proporcionais ao uso. O facto de o starter ser MIT não autoriza qualquer imagem, fonte, música ou dataset utilizado pela aplicação. Da mesma forma, a ausência de uma ficha documental perfeita não significa automaticamente que um recurso seja proibido: avalie direitos concretos e evidência mínima razoável sem burocracia artificial.

Para recuperação de dados, distinga leitura, restauração, sobrescrita e apagamento. Um backup pode conter informação sensível; guardá-lo em local público não é uma forma aceitável de facilitar um teste. A engenharia tem de preservar confidencialidade e integridade durante toda a recuperação.

## 7. Provar a saída de um incidente

Uma recuperação só fica concluída quando os efeitos são verificados contra a fonte atual. O relatório deve indicar incidente, candidato, ambiente, causa demonstrada, alterações realizadas, testes repetidos, estado da DB e próximos riscos. O desaparecimento de um stack trace não basta se o utilizador ainda não consegue realizar a tarefa.

Quando se corrige uma migração, faça leitura posterior e, se necessário, reinício. Quando se corrige um problema de UI, abra a aplicação no ambiente relevante. Quando um host caiu a meio de uma chamada externa, consulte o efeito remoto antes de tentar novamente. Uma segunda execução cega pode duplicar pagamentos, publicações ou alterações de estado.

Se a recuperação exigiu modificar o candidato depois de uma revisão, renove a parte afetada da revisão. A decisão final pertence ao owner competente. I3 pode declarar um terminal técnico com evidência, mas não pode aprovar sozinho a experiência reservada ao CLIENT nem conceder autorizações externas.

Um resumo de incidente deve ser suficientemente curto para orientar a pessoa que retoma o trabalho e suficientemente preciso para localizar a evidência. A continuidade não necessita de transcrições enormes, mas precisa de referências corretas e owners claros.

## 8. Três cenários de recuperação

**Cenário A — Instalação interrompida.** O instalador escreve parte de `.agentic-sdlc/` e o terminal fecha. Antes de repetir, inspecione o destino e descubra se há estado parcial. Preserve ficheiros existentes, compare com o manifesto e utilize o caminho de reparação ou reinstalação segura autorizado. Não apague toda a pasta do projeto.

**Cenário B — Operação de DB incerta.** Um pedido de pagamento recebe timeout. O cliente não sabe se o valor foi registado. O Controller procura um identificador de operação e faz readback da fonte transacional antes de reexecutar. Se não conseguir determinar o efeito com segurança, suspende reenvios que possam duplicá-lo e estabelece HOLD específico enquanto investiga.

**Cenário C — Revisão desatualizada.** O reviewer aprovou versão A, mas um refactor produziu B. O Planner não aceita B com base no PASS de A. I3 identifica o delta, executa os gates afetados e apresenta uma revisão aplicável a B. A evidência não afetada pode continuar válida se a independência estiver justificada.

Cada caso ilustra um tipo diferente de risco: efeitos parciais, idempotência e identidade do candidato. A resposta correta não consiste em reiniciar o processo estratégico; consiste em preservar a verdade e reparar no owner adequado.

## 9. Operações sensíveis e limites de autoridade

Antes de realizar uma ação de risco, pergunte: qual é o alvo exato, de quem é o recurso, quais os efeitos reversíveis, que dados podem ser expostos, qual o rollback e que autorização existe? A resposta deve ser baseada no sistema atual, não em uma suposição de que «isto é só um teste».

| Operação | Limite relevante |
| --- | --- |
| Ler fontes e executar testes locais. | Escopo e permissões técnicas habituais. |
| Modificar código dentro de um charter. | Ownership, gates e revisão de I3. |
| Alterar schema e dados reais. | Preflight, migração e recuperação verificáveis. |
| Apagar diretórios ou bases. | Alvo específico e autorização expressa quando material. |
| Enviar ficheiros a terceiros. | Privacidade, licença, custo e permissão do CLIENT. |
| Publicar release ou comunicar externamente. | Gate de release e autoridade externa aplicável. |

Quando falta a autorização, pare o efeito e peça-a. Não procure uma rota alternativa para contornar um bloqueio. Quando o problema é apenas uma falha técnica dentro do contrato, I3 deve resolvê-lo sem transferir decisões internas ao CLIENT.

Os limites também se aplicam à recuperação automática. Um script que limpa caches pode ser razoável, mas não deve remover ficheiros desconhecidos numa pasta ampla. Um mecanismo que repete transações precisa de idempotência comprovada. A capacidade de automatizar uma operação não justifica executá-la sem conhecer o seu impacto.

## 10. O que uma validação verde não demonstra

O `validate_structure.py` do repositório verifica relações documentais e contratos estruturais. Um teste de scaffold confirma que a camada pode ser instalada em cenários controlados. Uma prova de recuperação sintética verifica o comportamento de um mecanismo sob determinadas condições. Nenhuma dessas provas certifica uma aplicação de terceiros em produção.

Um teste unitário pode passar enquanto a API está mal ligada; uma integração pode passar enquanto o estado de DB aponta para uma versão errada; uma aplicação pode funcionar fisicamente mas ter experiência confusa. O gate semântico e o gate humano têm responsabilidades próprias. O relatório deve distinguir o que foi observado do que ainda depende de prova.

As releases versionadas têm outra fronteira: para dizer que um ZIP foi publicado, é necessário verificar o artefacto exato no GitHub Release e os checksums correspondentes. Um build local e uma tag não provam a disponibilidade remota de todos os ficheiros. E uma release do framework não é uma release de cada produto que o utiliza.

Se um gate não é aplicável, explique porquê de forma proporcional. Se é aplicável e falta prova, não o substitua por outro que já passou. O objetivo é evitar tanto falsos positivos como um processo infinito de testes irrelevantes.

## 11. Feedback e dados locais do starter

Na v1.4, a geração local de relatórios mínimos de metadados pode estar ativa por padrão. O workflow periódico, quando instalado, guarda a saída nos artefactos GitHub Actions do próprio projeto. A distribuição pública não inclui um endpoint de coleta externo. A opção `--no-feedback-workflow` desativa o agendamento, não a geração local.

Para desligar inteiramente a geração, utilize `enabled=false` em `.agentic-sdlc/feedback/ARCHITECTURE_FEEDBACK_CONFIG.json`. Antes de ativar uma integração outbound, verifique a [política de feedback e privacidade](../../../22_PRIVACY_PRESERVING_ARCHITECTURE_FEEDBACK.md), o código do workflow e as permissões reais. Não presuma que uma opção de privacidade na UI altera automaticamente o comportamento de todos os scripts.

Se precisar reportar um incidente do próprio framework, inclua versão, plataforma, passos reproduzíveis, logs sanitizados e resultado observado. Não anexe os dados privados da aplicação. Uma descrição baseada em um projeto sintético pode permitir a correção sem expor informação sensível.

O objetivo final da recuperação é que qualquer trabalhador autorizado possa continuar de um estado coerente, sabendo o que passou, o que falhou e o que permanece por decidir. Um sistema que só parece recuperado enquanto a conversa original continua aberta precisa de mais evidência durable.

**A seguir:** capítulo 06, fechamento de capacidades e aceitação com candidatos exatos.

## Fontes e âmbito

- [Recuperação de transações](../../../12_TRANSACTION_RECOVERY.md)
- [Attachment de governação existente](../../../32_EXISTING_GOVERNED_ATTACHMENT.md)
- [Ferramenta de delta de fonte](../../../../tools/repo_delta.py)
- [Inventário e GC de ficheiros](../../../34_FILE_ARTIFACT_INVENTORY_AND_GC.md)
- [Privacidade e feedback](../../../22_PRIVACY_PRESERVING_ARCHITECTURE_FEEDBACK.md)
- [Verificação pública v1.4](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md)

As soluções exatas dependem do ambiente e do produto. Nunca trate um exemplo de recuperação como autorização para substituir ou apagar estado canónico real.
