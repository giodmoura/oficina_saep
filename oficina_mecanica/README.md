# Sistema para Oficina Mecânica — SAEP / SENAI

Projeto desenvolvido conforme o guia passo a passo anexado. Tecnologias: Python, Flask, MySQL, Bcrypt, HTML5, CSS3 e JavaScript puro.

## Estrutura

```text
oficina_mecanica/
├── saep_db.sql
└── sistema/
    ├── app.py
    ├── autenticacao.py
    ├── banco.py
    ├── clientes.py
    ├── veiculos.py
    ├── agendamento.py
    ├── rotas.py
    ├── requirements.txt
    ├── templates/
    └── static/
```

## 1. Preparar ambiente Python

Na raiz do projeto:

```bash
python -m venv venv
```

Ativar o ambiente:

```bash
# Windows CMD
venv\Scripts\activate

# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Linux/macOS
source venv/bin/activate
```

Instalar dependências:

```bash
pip install -r sistema/requirements.txt
```

## 2. Criar o banco MySQL

Execute o arquivo SQL:

```bash
mysql -u root -p < saep_db.sql
```

**Atenção:** conforme o guia da aula, o script remove e recria as tabelas com `DROP TABLE IF EXISTS`. Execute apenas em uma base de demonstração sem dados que queira preservar.

## 3. Configurar conexão

As configurações aceitam variáveis de ambiente `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` e `DB_PORT`. Os padrões são `localhost`, `root`, senha vazia, `saep_db` e `3306`. Também defina `SECRET_KEY` para substituir a chave de demonstração.

Exemplo em Linux/macOS:

```bash
export DB_HOST=localhost
export DB_USER=root
export DB_PASSWORD='sua_senha_mysql'
export DB_NAME=saep_db
export DB_PORT=3306
export SECRET_KEY='defina_uma_chave_local'
```

No Windows PowerShell, use `$env:DB_PASSWORD="sua_senha_mysql"` e equivalentes para as demais variáveis.

## 4. Testar a conexão e iniciar

```bash
python sistema/banco.py
python sistema/app.py
```

Abra <http://127.0.0.1:5000>.

## Usuários de demonstração

| Usuário | Senha |
|---|---|
| `admin` | `admin123` |
| `mecanico` | `senha123` |
| `recepcao` | `rec123` |

As contas e três registros demonstrativos de clientes, veículos e agendamentos são criados pelo script SQL.
