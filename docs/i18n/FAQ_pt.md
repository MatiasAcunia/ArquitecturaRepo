# Agentic SDLC FAQ (pt)

[PT guide](README_pt.md) · [Miniguia v1.4](MINI_GUIDE_pt.md) · [Main README](../../README.md)

### 1. O que é Agentic SDLC?

É uma arquitetura reutilizável para organizar desenvolvimento de software com agentes. Não é um construtor autônomo de qualquer aplicação.

### 2. Como começar?

Faça um fork ou inspecione o repositório, comece com descoberta somente leitura, escolha o menor perfil e siga o prompt de instalação. O scaffold inicial fica em HOLD.

### 3. Posso adotar em um repositório existente?

Sim. Primeiro reconstrua o código, os dados e a autoridade reais. Não sobrescreva arquivos da aplicação nem trate exemplos como verdade canônica.

### 4. Quatro papéis exigem quatro modelos?

Não. CLIENT, Planner I2, Campaign Lead I3 e especialistas I4 representam responsabilidades, não quantidade fixa de processos.

### 5. Quem autoriza alterações sensíveis?

O CLIENT mantém decisões de produto, aceitação subjetiva, publicação, custos e dados sensíveis. I3 não pode inventar permissões.

### 6. Goals e Codex Desktop já funcionam automaticamente?

Não automaticamente. v1.4 inclui controles portáteis de Goal, Plan e autorização; a integração nativa por invocação com Codex Desktop/Goals ainda requer provas físicas separadas.

### 7. Gemini é obrigatório ou pago por padrão?

Não. O caminho I4 fica desativado até autorização, credenciais, cota e privacidade serem verificadas. Não há envio padrão de código privado.

### 8. O starter pode reiniciar ou apagar chats Codex?

Não. O starter não reinicia, gerencia nem apaga chats nativos do Codex. Qualquer adaptador de host requer autorização e evidência adicionais; v1.4 não certifica esse ciclo de vida.

### 9. Que feedback está ativado por padrão?

Um relatório mensal mínimo de metadados, guardado nos artifacts GitHub Actions do próprio projeto. Ajuda a melhorar o starter, mas não é enviado automaticamente para fora.

### 10. Quais dados ficam excluídos?

Código, conversas, nomes de projetos/repositórios, caminhos, credenciais, identificadores pessoais, requisitos, SHAs e texto livre irrestrito.

### 11. Como alterar idioma ou desligar o feedback?

Use --language auto|en|es|pt|fr|de|it|ja|zh. Para desligar todos os relatórios, defina enabled=false; --no-feedback-workflow só desativa o agendamento. O README no GitHub é estático.

### 12. O que foi testado e como relatar problemas?

O código-fonte está na versão 1.4.0, mas ela só é uma release quando o [tag imutável v1.4.0, ZIP e checksum](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0) forem publicados e verificados; v1.3.0 continua disponível. Os testes portáteis de Linux/Windows não certificam hosts de agentes nativos nem usabilidade de terceiros. Abra um Issue com reprodução e logs sem segredos. O material original usa MIT.

### 13. Posso combinar modos assíncronos, híbridos, equipes e IA sem programação?

Sim, são dimensões de configuração. A execução exige host, autoridade, recuperação e direitos comprovados; SMALL continua simples. I2 mantém requisitos e stack no repositório canônico; commit/branch mania são proibidos. O feedback externo mínimo terá opção de desligar quando existir coletor verificado, ainda ausente.

---

[PT guide](README_pt.md) · [Miniguia v1.4](MINI_GUIDE_pt.md)
