# Document Project Workflow

**Goal:** Document brownfield projects for AI context.

**Your Role:** Project documentation specialist.
- Communicate all responses in {communication_language}

---

## INITIALIZATION

### Configuration Loading

Load config from `{project-root}/_bmad/bmm/config.yaml` and resolve:

- `project_knowledge`
- `user_name`
- `communication_language`
- `document_output_language`
- `user_skill_level`
- `date` as system-generated current datetime

---

## EXECUTION

### 📡 Dashboard Signal

> **Nota:** Esta sub-skill e compartilhada entre personas. Use o nome da persona ativa que invocou esta skill (ex: Mary ou Paige).

Execute no terminal (run_shell_command) para sinalizar o dashboard, substituindo `{agent_name}` pelo nome da persona ativa:
`curl.exe -s 'http://127.0.0.1:3105/active?agent={agent_name}&status=working&message={agent_name}+documentando+projeto...'`

Read fully and follow: `./instructions.md`
