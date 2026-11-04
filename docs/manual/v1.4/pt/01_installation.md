# 01 — Instalação e configuração

ArquitecturaRepo · Manual completo de utilização · Edição v1.4 · Português

> Instalar o starter é criar uma camada de controlo inicial, **não adotar automaticamente a aplicação** nem demonstrar que um produto funciona. Os comandos deste capítulo seguem o [início público v1.4](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md). Um projeto novo começa corretamente em `HOLD / UNTRUSTED_CONTEXT` enquanto requisitos, fontes e autoridades não forem reconciliados.

## Neste capítulo

1. Ambiente e contas
2. Starter, fork e aplicação: três lugares diferentes
3. Verificar caminhos antes de escrever
4. Escolher um perfil proporcional
5. Criar a camada de controlo
6. Validar sem inventar aceitação
7. A próxima ação é discovery
8. Antes de repetir uma instalação
9. Passar do scaffold à adoção real
10. Conexões, permissões e privacidade
11. Diagnóstico seguro

## 1. Ambiente e contas

Para experimentar a instalação portátil, são necessários Python 3.12, uma forma de trabalhar com ficheiros e Git, e acesso à fonte do ArquitecturaRepo. Python 3.12 é o interpretador exercitado pela CI da v1.4. Um editor como VS Code pode ajudar a inspecionar os ficheiros, mas não é obrigatório ter uma integração de IA ou conta num fornecedor externo.

Num terminal Windows, pode verificar o Python em PowerShell com os comandos abaixo. Utilize os caminhos adequados ao ambiente; executar um comando dentro de um editor não garante que utiliza a mesma instalação Python da consola.

```powershell
& "python" --version
& "python" -m pip --version
& "git" --version
```

Se uma ferramenta não for reconhecida, investigue primeiro o executável, o PATH e a instalação. Não precisa alterar Product State para compensar uma dependência local em falta. Uma instalação de Python obtida de fonte confiável deve ser verificada antes de retomar o tutorial.

No Linux ou macOS, confirme que `python3` corresponde à versão pretendida e que o comando `python` existe se os exemplos o utilizarem. Nos comandos portáteis, as aspas delimitam caminhos com espaços. Para sistemas diferentes, a barra invertida dos exemplos PowerShell não deve ser confundida com o separador de diretórios do shell Unix.

É possível começar sem GitHub, utilizando uma cópia de fonte verificada localmente, mas Git e um repositório remoto facilitam a durabilidade de decisões e evidência. Antes de dar acesso a um agente, compreenda o âmbito das permissões: ler um repositório privado, editar ficheiros, aprovar um PR e publicar uma release são operações diferentes.

## 2. Starter, fork e aplicação: três lugares diferentes

Um erro frequente é misturar o repositório do framework com o repositório do produto. O starter contém documentação, protocolos, ferramentas e modelos. O fork é a sua cópia versionada do starter, caso pretenda acompanhar ou modificar essa arquitetura. O destino é a aplicação que quer desenvolver: por exemplo, uma API de reservas ou um sistema de associados.

A operação de scaffold parte da fonte do framework e escreve uma pasta `.agentic-sdlc/` dentro do **projeto de destino**, desde que não exista aí governação canónica incompatível. Não deve apagar o código de produto que já estava nesse diretório. A pasta do produto continua a ter os seus próprios requisitos, stack, dados, testes e permissões.

| Local | Conteúdo e função |
| --- | --- |
| `ArquitecturaRepo/` | Fonte do framework, scripts de scaffold, testes e documentação. |
| Fork do starter | Cópia sob o seu controlo, com histórico e eventuais personalizações. |
| `meu-projeto/` | Código verdadeiro da aplicação, com `.agentic-sdlc/` quando instalado. |
| `.agentic-sdlc/` | Contratos e estado de coordenação do produto, não o produto em si. |

Os exemplos de projeto incluídos no framework são sintéticos. Não representam a sua base de dados, não substituem os requisitos do CLIENT e não podem ser copiados como se fossem um estado de produção autorizado. Instalar uma camada de governo sem compreender o produto cria um ponto de partida, não um resultado validado.

## 3. Verificar caminhos antes de escrever

Antes de executar o instalador, confirme a pasta onde está o terminal, a origem e o destino. Em PowerShell, uma verificação simples permite distinguir a fonte do projeto que será alterado:

```powershell
& "python" "tools\scaffold_project.py" --help
```

Este comando de ajuda deve ser executado na raiz do starter e é de leitura. Reveja as opções realmente suportadas pela cópia instalada. Se não existir `tools\scaffold_project.py`, provavelmente está na pasta errada ou não tem a distribuição esperada. Não tente reparar copiando ficheiros aleatórios de outra versão.

O destino deve ser explícito e específico. Por exemplo, `"..\meu-projeto"` refere-se a uma pasta adjacente, não ao diretório do sistema e não a um caminho universal. Se a pasta já contiver uma aplicação, faça inventário dos ficheiros e da governação antes de iniciar. Se nela existir um Product State, um controlador ativo ou um esquema de dados que o framework não conhece, utilize a rota de leitura para projetos já governados.

Para uma instalação reproduzível, descarregue a [release v1.4.0](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0), que contém ZIP portátil, ficheiro de checksum e manifest. Confira o SHA-256. Pode também trabalhar com um checkout do tag. A branch `main` é móvel; não atribua ao ZIP publicado ficheiros que só foram adicionados depois.

## 4. Escolher um perfil proporcional

O framework dispõe de seis perfis com famílias de controlo diferentes. Não são níveis de prestígio e nenhum deles faz a aplicação funcionar automaticamente:

| Perfil | Quando o considerar |
| --- | --- |
| `SMALL` | Aplicação pequena, com riscos modestos e sem persistência material complexa. |
| `STATEFUL` | Dados duráveis, esquemas, utilizadores, recuperações, backups ou runtime com estado. |
| `ARTIFACT_HEAVY` | Muitos ficheiros, recursos caros, lineage, licenças e políticas de utilização. |
| `MULTI_WORKSTREAM` | Linhas de trabalho diferentes que integram um único produto final. |
| `MULTI_PRODUCT` | Produtos realmente distintos com recursos ou políticas partilhadas. |
| `HIGH_CONSEQUENCE` | Risco material de segurança, privacidade, integridade ou efeitos difíceis de reverter. |

Para uma primeira experiência sem requisitos especiais, `SMALL` costuma ser adequado. Um clube com registo de associados e quotas persistentes pode justificar `STATEFUL`. Um sistema de edição de vídeos que rastreia centenas de recursos pode necessitar de controlos de artefactos e direitos. A escolha deriva do comportamento e do risco, não de uma vontade de criar mais agentes.

O perfil não concede automaticamente permissões de rede, escrita em bases de produção ou despesas. Ainda é necessário descobrir a fonte real, definir ownership e confirmar com o CLIENT as decisões que alteram o produto. A documentação técnica dos [perfis](../../../06_SCALING_PROFILES.md) e [modos de projeto](../../../27_PROJECT_MODES_AND_STACK_SELECTION.md) explica as diferenças.

## 5. Criar a camada de controlo

Na raiz do starter v1.4, pode criar uma camada de controlo para um projeto novo. Em PowerShell, com caminhos e valores explicitamente delimitados:

```powershell
& "python" "tools\scaffold_project.py" --target "..\meu-projeto" --profile "SMALL" --product-id "MEU_PROJETO" --objective "Objetivo inicial pendente de confirmação" --language "pt" --no-feedback-workflow
```

Para o exemplo fictício de um clube com estado persistente:

```powershell
& "python" "tools\scaffold_project.py" --target "..\clube-app" --profile "STATEFUL" --product-id "CLUBE_GESTAO" --objective "Gestão fictícia de associados e mensalidades" --language "pt" --no-feedback-workflow
```

No shell Unix, utilize o script com `/`, por exemplo `"tools/scaffold_project.py"`, e o destino `"../meu-projeto"`. Adapte `product-id`, objetivo e pasta aos dados legítimos da aplicação. O instalador deverá recusar sobrescritas de controlo canónico e preservar ficheiros preexistentes que não lhe pertencem.

O estado inicial `HOLD / UNTRUSTED_CONTEXT` é o resultado esperado. Ele indica que o sistema não fabricou decisões do CLIENT, um baseline de código, um Goal em execução ou uma capacidade aceite. Escrever manualmente `READY` em um JSON para obter uma validação verde não altera os factos, apenas esconde a lacuna.

A opção `--with-runtime`, quando aplicável, acrescenta mecanismos portáteis de referência para campanhas; não autentica uma conta de Codex Desktop, não inicia um LLM e não concede acesso a provedores externos. `--no-feedback-workflow` evita o agendamento periódico, mas não desativa o gerador local de relatórios por si só. Consulte a configuração instalada antes de ativar fluxos de rede.

## 6. Validar sem inventar aceitação

Depois de criar o scaffold, abra o **diretório do projeto de destino**, não permaneça na raiz do framework. Em PowerShell, execute:

```powershell
& "python" -m pip install -r ".agentic-sdlc\requirements-validation.txt"
& "python" ".agentic-sdlc\tools\project_status.py" --control-root ".agentic-sdlc"
& "python" ".agentic-sdlc\tools\discover_project.py" --project-root "."
& "python" ".agentic-sdlc\tools\reconstruct_context.py" --root ".agentic-sdlc"
```

O primeiro instala dependências locais declaradas. O `project_status.py` apresenta estado inicial; `discover_project.py` recolhe inventário, metadados e hashes de ficheiros sem enviar o conteúdo do código ao mantenedor; `reconstruct_context.py` tenta recuperar a situação a partir dos registos disponíveis. A discovery deve respeitar limites de caminhos, links simbólicos e destinos fora do projeto.

Algumas verificações podem devolver HOLD enquanto não existir adoção confirmada. Isso é correto. A validação de contratos verifica relações e estruturas da camada de controlo; não demonstra que o backend da aplicação se ligue à DB, que a UI abra ou que um utilizador consiga recuperar uma reserva depois de reiniciar.

Registe o estado, os erros e a versão de código utilizada. Confirme que a aplicação anterior continua intacta. Se faltar `jsonschema`, instale as dependências declaradas, não edite um estado canónico para evitar a verificação. Se um comando falhar por permissões, não contorne a proteção com uma eliminação ou instalação forçada.

O resultado desta fase é **camada inicial instalada e inspecionada**. A adoção da aplicação real exige ainda discovery, requisitos aprovados, baseline, owner, currentness e autorização do charter. O sucesso de instalação deve ser relatado com esse limite explícito.

## 7. A próxima ação é discovery

O Planner deve começar pela aplicação que existe, pelos utilizadores previstos e pelas decisões confirmadas. Os [prompts de instalação e adaptação](../../../../prompts/INSTALL_THIS_SDLC.md), [discovery de produto](../../../../prompts/PRODUCT_DISCOVERY_SESSION.md) e [transferência/adoção](../../../16_TRANSFER_ADOPTION.md) servem como referências. Não entregue imediatamente à engenharia uma lista genérica de funcionalidades baseada apenas no exemplo do manual.

Discovery identifica: problema, critérios observáveis de aceitação, código e DB atuais, interfaces e dependências, restrições de prazo e custos, riscos de privacidade, tecnologia existente e responsabilidades. O CLIENT confirma decisões de produto; a engenharia comprova afirmações técnicas. O Planner separa hipóteses de requisitos efetivamente aceites.

Depois, prepara-se uma especificação explícita de adoção. Faz-se preflight contra as fontes atuais, promove-se o estado de modo coerente e verifica-se se uma sessão fresca consegue recuperar o mesmo contexto. Só após esse baseline pode ser autorizada uma campanha material com limites reais.

Uma boa instalação não acelera o projeto se os agentes começarem a modificar ficheiros sem saber qual o requisito. A etapa de discovery é a ponte entre um framework genérico e um produto específico. O custo inicial desta ponte deve ser proporcional à dimensão e ao risco da primeira entrega.

## 8. Antes de repetir uma instalação

Se `.agentic-sdlc/` já existir, pare e investigue. Pode conter Product State, campanhas, owners, journals, fontes adotadas e referências a dados que não devem ser perdidos. Não apague a pasta para repetir o exemplo. Não use uma opção de força como método de resolução de erros e não inicialize um segundo controlador sobre o primeiro.

Quando a aplicação já possui governação, use o [preflight de attachment somente leitura](../../../32_EXISTING_GOVERNED_ATTACHMENT.md). Essa rota pode testar referências ao código e consistência de snapshots de SQLite/WAL, mas não é um atualizador automático de qualquer v1.2 ou v1.3. Uma migração material exige uma decisão com owners e evidência apropriados.

Se um comando falha após uma interrupção, antes de repetir confirme se houve efeito parcial. Ficheiros podem ter sido criados, journals podem estar pendentes e uma operação externa pode ter ocorrido mesmo que o terminal tenha perdido a ligação. Primeiro faça readback e preserve evidência; depois o Controller escolhe uma recuperação idempotente.

Nem todo problema de instalação pertence ao Planner. Dependências, caminhos, permissões e ajustes dentro de um charter são assuntos de execução. Uma incompatibilidade de autoridade ou alteração material do contrato pode exigir reconstrução estratégica. Separar essas classes evita ciclos de planeamento desnecessários.

## 9. Passar do scaffold à adoção real

Um percurso adequado contém etapas distintas: inventariar o código; confirmar os requisitos com o CLIENT; estabelecer baseline de produto e baseline técnico; escolher estratégia e marcos datados; preparar a especificação de adoção; executar preflight; promover estado e ownership coerentes; validar fresh-context; e somente então autorizar uma capacidade material.

Cada etapa produz evidência que será utilizada pela seguinte. O baseline técnico não pode apontar para um commit antigo enquanto a campanha foi construída sobre outro. O estado da DB não deve ser descrito por um hash insuficiente. O charter não pode afirmar que existe uma credencial, licença ou integração que ninguém verificou.

O CLIENT não é obrigado a reunir hashes, gerir leases ou decidir entre dois scripts de recuperação. O sistema deve permitir que se concentre no comportamento desejado, no orçamento e na aceitação humana. A engenharia deve tornar os limites e as falhas compreensíveis, sem transferir a responsabilidade técnica para quem pediu o produto.

Se o destino for uma aplicação já em desenvolvimento, preserva-se código e evidência úteis. Adotar a arquitetura não é uma autorização para reescrever tudo. O trabalho começa por compreender o que já funciona, o que falta e onde existe risco material que as ferramentas conseguem realmente reduzir.

## 10. Conexões, permissões e privacidade

Os conectores para GitHub, ferramentas de programação, bases de dados ou serviços de IA dependem de permissões configuradas no ambiente. O instalador não traz tokens nem autenticadores e não consegue garantir a sessão nativa de um fornecedor. Se a integração falhar, diagnostique o âmbito do acesso e o erro sem pedir ao CLIENT que exponha credenciais numa conversa.

O gerador local de feedback de arquitetura utiliza metadados restritos. Na instalação padrão, pode existir um workflow mensal que guarda relatórios nos artefactos do próprio GitHub Actions do projeto. O pacote público v1.4 não inclui um endereço de coleta externo. `--no-feedback-workflow` desativa o agendamento; para desligar inteiramente a geração, configure `enabled=false` no ficheiro instalado de feedback. A [política de privacidade](../../../22_PRIVACY_PRESERVING_ARCHITECTURE_FEEDBACK.md) detalha os limites.

Nunca copie código privado, identificadores de pessoas, bases completas, logs com tokens ou conversas para um issue público. Um bug pode ser relatado com ambiente, comando, resultado esperado, erro sanitizado e exemplo fictício. Antes de ativar efeitos de rede, despesas, publicação ou envio de dados, obtenha a autorização específica adequada.

Licenças também importam: o framework ter licença MIT não transforma automaticamente imagens, fontes, bases, serviços ou documentos de terceiros em recursos livres. O responsável pela aplicação deve avaliar direitos de acordo com o uso efetivo e com a evidência disponível, sem impor controles irrelevantes nem ignorar restrições legais reais.

## 11. Diagnóstico seguro

Se o Python não iniciar, confirme executável e versão. Se faltar uma dependência, instale a lista declarada. Se um caminho não existir, compare diretório atual, origem e destino. Se aparecer `EXISTING_CONTROL_PRESERVED`, não tente sobrescrever: siga a rota de attachment. Se o Project State estiver inconsistente, investigue as referências atuais antes de qualquer escrita.

Para problemas de Git, preserve worktree e branches; para SQLite, preserve snapshots consistentes e WAL; para operações interrompidas, preserve journal e identidade da tentativa. O [capítulo 05](05_errors_and_recovery.md) aprofunda a recuperação. A regra comum é diagnosticar a causa e demonstrar o gate afetado, não apenas fazer desaparecer a mensagem.

Um bom relatório de instalação contém versão exata do starter, pasta de destino, perfil, preservação dos ficheiros existentes, comandos executados, resultados de validação e limites abertos. Nunca deve concluir que a aplicação foi desenvolvida ou aceite apenas porque o scaffold iniciou corretamente.

**A seguir:** capítulo 02, o Planner, o discovery e a adoção de um projeto real.

## Fontes e âmbito

- [Primeiro uso e suporte público v1.4](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md)
- [Scaffold e perfis](../../../06_SCALING_PROFILES.md)
- [Transferência e adoção](../../../16_TRANSFER_ADOPTION.md)
- [Attachment de projeto com governação existente](../../../32_EXISTING_GOVERNED_ATTACHMENT.md)
- [Privacidade e feedback](../../../22_PRIVACY_PRESERVING_ARCHITECTURE_FEEDBACK.md)
- [Instalador de referência](../../../../tools/scaffold_project.py)

Os exemplos são ilustrativos e não alteram as condições do ZIP v1.4.0 já publicado. Instalar o starter não concede autoridade para executar campanhas, utilizar fornecedores nem modificar uma aplicação já governada.
