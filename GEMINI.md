# BMAD Project - Guia de Desenvolvimento e Guardrails

Este arquivo contém mandatos fundamentais para o Gemini CLI operando no projeto BMAD. Estas instruções têm precedência sobre os comportamentos padrão.

## 🚀 Visão Geral do Projeto
O BMAD (Business Management AI Developer) é um ecossistema de agentes de IA orquestrados em uma interface visual de escritório virtual (GBA Style). Ele utiliza Node.js/Socket.io para o dashboard e Python para o pipeline de assets.

## 🛡️ Guardrails e Regras de Integridade
1. **Alterações Cirúrgicas:** Ao modificar um componente específico (ex: um avatar, uma skill ou um script), NUNCA altere ou quebre os demais componentes. Mantenha a compatibilidade com o sistema de grid e animações existentes.
2. **Preservação de Estilo:** O dashboard deve manter a estética Pixel Art / GBA. Não introduza frameworks CSS pesados ou componentes que fujam dessa identidade visual.
3. **Pipeline de Assets:** Ao adicionar novos agentes, siga rigorosamente o processo de fatiamento de sprites e remoção de fundo verde via scripts Python (`sprite_slicer.py`, `process_all.py`).
4. **Comunicação Bidirecional:** O fluxo `Terminal -> Skill -> Curl -> Dashboard (Socket.io)` é sagrado. Mantenha a porta 3105 como o padrão para comunicação de eventos dos agentes.
5. **Estrutura HTML do `#scene`:** O `index.html` do dashboard DEVE manter a hierarquia `#game-container > #scene > (#office-floor + #workspaces-layer)`. O `<div id="scene">` é o wrapper que recebe o zoom (`transform: scale(1.8)`) via `updateZoom()`. Se ele for removido ou ficar fora da árvore, toda a lógica de `updateAgentUI()` quebra com `TypeError: Cannot read properties of null`. O `#dialog-box` deve ficar FORA do `#scene` para não ser afetado pelo zoom.

## 🛠️ Instruções Específicas
1. **Chamadas Curl ao Dashboard:** As chamadas para atualizar o dashboard devem SEMPRE usar a ferramenta de terminal (`run_shell_command`) com o binário real do Windows: `curl.exe -s 'http://127.0.0.1:3105/active?agent=...'`. **REGRAS:**
   - Use `curl.exe` (NÃO `curl`) pois o alias nativo do PowerShell causa erro com a flag `-s`.
   - Use **aspas simples** (`'`) para a URL (NÃO aspas duplas `"`), pois o `&` dentro de aspas duplas é interpretado como operador de pipeline no PowerShell, quebrando silenciosamente o comando.
   - **NÃO use acentos** (á, é, í, ó, ú, ã, õ, ç, etc.) nas mensagens do curl. Caracteres UTF-8 na URL quebram silenciosamente o `curl.exe` no Windows. Use equivalentes ASCII: `sessao`, `configuracoes`, `proximo`, `codigo`, etc.
2. **Consistência de Dados:** Sempre que adicionar uma nova persona em `.agent/skills`, certifique-se de que o ID correspondente existe no array `agentsData` dentro do `index.html` do dashboard para garantir que o avatar apareça corretamente.
3. **Efeitos Visuais da Ativação:** Ao chamar o endpoint `/active`, os seguintes efeitos devem ocorrer simultaneamente: (a) glow verde/amarelo na baia e no sprite, (b) zoom `scale(1.8)` centralizado na posição do agente, (c) ícone da bolha atualizado (💻 working / ⏳ waiting / 💤 idle), (d) mensagem no painel INFINITY COMMS e typewriter na dialog box.

## 🏗️ Arquitetura de Referência
- **Frontend:** HTML/Vanilla JS + Socket.io Client.
- **Backend de Sinalização:** Node.js (Express) + Socket.io Server.
- **Lógica de Agentes:** Markdown-based skills em `.agent/skills/`.
- **Processamento de Imagem:** Python + OpenCV/PIL.

## 📡 Sinais de Dashboard nas Sub-Skills

Cada workflow de sub-skill DEVE sinalizar o dashboard ao iniciar a execução. O sinal é inserido **após o carregamento de configuração** (INITIALIZATION) e **antes do primeiro step**.

### Formato do Sinal
```
curl.exe -s 'http://127.0.0.1:3105/active?agent={NOME}&status=working&message={NOME}+{mensagem_contextual}'
```

### Ciclo de Vida Completo de Status
1. **Persona ativada** → `status=working` (persona SKILL.md)
2. **Persona aguardando comando** → `status=waiting` (persona SKILL.md)
3. **Sub-skill invocada** → `status=working` (workflow.md da sub-skill)
4. **Sub-skill aguardando input** → `status=waiting` (workflow.md da sub-skill)
5. **Persona dispensada** → `status=done` (persona SKILL.md)

### Mapeamento Agente → Sub-Skills Exclusivas
| Agente | Sub-Skills |
|--------|------------|
| John (PM) | create-prd, validate-prd, edit-prd, create-epics-and-stories |
| Bob (SM) | sprint-planning, create-story, retrospective |
| Amelia (Dev) | dev-story |
| Quinn (QA) | qa-generate-e2e-tests |
| Winston (Architect) | create-architecture |
| Mary (Analyst) | brainstorming, market-research, domain-research, technical-research, product-brief |
| Sally (UX) | create-ux-design |
| Barry (Solo Dev) | quick-dev |

### Sub-Skills Compartilhadas (usam `{agent_name}` dinâmico)
| Sub-Skill | Personas que usam |
|-----------|-------------------|
| correct-course | John, Bob |
| check-implementation-readiness | John, Winston |
| code-review | Amelia, Barry |
| document-project | Mary, Paige |

Para sub-skills compartilhadas, o workflow usa `{agent_name}` que deve ser resolvido pelo nome da persona ativa no momento da invocação.
