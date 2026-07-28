# Relatório da refatoração

## Backend

- Autenticação JWT passou a usar o ID imutável do usuário no `sub`.
- Gestão de usuários restrita ao administrador.
- Funcionários podem criar solicitações e visualizam apenas as próprias.
- Somente gerentes e administradores encerram solicitações.
- Transições de status encerradas não podem ser refeitas.
- `PATCH` usado para atualizações parciais.
- Paginação básica adicionada às listagens.
- Transações centralizadas com rollback em falha.
- Constraints de quantidade adicionadas aos models.
- Datas de criação, atualização e resolução adicionadas.
- Health check passa a verificar o banco.
- Rota duplicada `/request-resources` removida.

## Frontend

- CSS deixou de ser minificado e foi dividido por responsabilidade.
- JavaScript deixou de ser monolítico e foi separado em config, services, components, utils e pages.
- Elementos são obtidos explicitamente por seletores; IDs não viram variáveis globais.
- Dados vindos da API são inseridos com `textContent`, reduzindo risco de XSS.
- Event delegation usada nas listas.
- Comunicação HTTP centralizada em `services/api.js`.
- Autenticação e armazenamento isolados em módulos próprios.
- Cada página possui um único arquivo de inicialização.
- HTML atualizado para ES Modules e classes CSS reutilizáveis.

## Validações executadas

- `python -m compileall` em todo o backend.
- `node --check` em todos os arquivos JavaScript.
- Busca por referências antigas a `script.js`, `style.css` e `/request-resources`.

## Próximos passos para produção

- Substituir `create_all()` por Alembic.
- Adicionar testes com pytest e cobertura.
- Adicionar rate limiting ao login.
- Preferir cookie HttpOnly ao `localStorage` em produção.
- Adicionar logging estruturado e auditoria.
