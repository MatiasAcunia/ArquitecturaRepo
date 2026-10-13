# Agentic SDLC FAQ (pt)

[PT guide](README_pt.md) · [Main README](../../README.md)

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

Ainda não. v1.2 oferece controles opcionais de integridade de Goal e Plan, mas a integração física por invocação ainda precisa ser provada.

### 7. Gemini é obrigatório ou pago por padrão?

Não. O caminho I4 fica desativado até autorização, credenciais, cota e privacidade serem verificadas. Não há envio padrão de código privado.

### 8. O starter pode reiniciar ou apagar chats Codex?

Não por si só. Codex Daily Control 2.0.2 é uma referência independente, ainda sem adaptador de host aceito em v1.2.

### 9. Que feedback está ativado por padrão?

Um relatório mensal mínimo de metadados, guardado nos artifacts GitHub Actions do próprio projeto. Ajuda a melhorar o starter, mas não é enviado automaticamente para fora.

### 10. Quais dados ficam excluídos?

Código, conversas, nomes de projetos/repositórios, caminhos, credenciais, identificadores pessoais, requisitos, SHAs e texto livre irrestrito.

### 11. Como alterar idioma ou desligar o feedback?

Use --language auto|en|es|pt|fr|de|it|ja|zh. Para desligar relatórios, defina enabled=false ou instale com --no-feedback-workflow. O README no GitHub é estático.

### 12. O que foi testado e como relatar problemas?

1.1.0 é estável; v1.2 permanece candidata até passar testes físicos independentes. Abra um Issue com reprodução e logs sem segredos. O material original usa MIT.

### 13. Posso combinar modos assíncronos, híbridos, equipes e IA sem programação?

Sim, são dimensões de configuração. A execução exige host, autoridade, recuperação e direitos comprovados; SMALL continua simples. I2 mantém requisitos e stack no repositório canônico; commit/branch mania são proibidos. O feedback externo mínimo terá opção de desligar quando existir coletor verificado, ainda ausente.

---

[PT guide](README_pt.md)
