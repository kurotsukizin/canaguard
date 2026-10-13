# CanaGuard

> Sistema em Python para registro, análise e persistência de perdas na colheita de cana-de-açúcar.

## Problema no agronegócio

A cana-de-açúcar possui grande relevância para o agronegócio brasileiro. Entretanto, perdas na colheita — especialmente em operações mecanizadas — podem reduzir a produtividade e causar impacto financeiro ao produtor.

Quando informações como área plantada, produtividade esperada, produção efetivamente colhida e valor da tonelada não são registradas e analisadas de forma organizada, torna-se mais difícil identificar talhões com perdas elevadas e priorizar ações corretivas.

O CanaGuard atua no setor de **produção agrícola**, apoiando o acompanhamento de perdas por talhão durante a colheita de cana-de-açúcar.

## Solução proposta

O **CanaGuard** é um programa Python executado pelo terminal. Ele permite cadastrar registros de colheita, calcular perdas físicas e financeiras, classificar o nível de risco e armazenar os dados em memória, JSON, TXT e Oracle.

A solução foi projetada para oferecer uma visão clara sobre:

- Produção esperada por talhão.
- Produção efetivamente colhida.
- Perda estimada em toneladas.
- Percentual de perda.
- Prejuízo financeiro estimado.
- Talhões classificados como críticos.

## Funcionalidades

- Cadastro de registros de colheita por talhão.
- Validação de textos obrigatórios.
- Validação de valores numéricos positivos.
- Conversão de vírgula para ponto em números decimais.
- Cálculo automático de produção esperada.
- Cálculo de perda em toneladas.
- Cálculo de percentual de perda.
- Cálculo de prejuízo estimado.
- Classificação de perdas em baixo, atenção e crítico.
- Listagem de registros cadastrados.
- Consulta por talhão.
- Listagem de registros críticos.
- Persistência de dados em JSON.
- Carregamento de dados a partir de JSON.
- Geração de relatório em TXT.
- Persistência e consulta de registros no Oracle.

## Requisitos da disciplina

| Requisito | Implementação no CanaGuard |
|---|---|
| Funções e procedimentos | Funções como `calcular_dados_colheita()`, `classificar_perda()`, `salvar_json()` e `gerar_relatorio_txt()` |
| Passagem de parâmetros | `calcular_dados_colheita(area_hectares, produtividade_estimada, producao_colhida, valor_tonelada)` |
| Lista | `registros_colheita` armazena todos os registros criados |
| Tupla | `STATUS_PERDA` mantém os status fixos da aplicação |
| Dicionário | Cada colheita é representada por um dicionário chamado `registro` |
| Tabela de memória | Documentada em [`docs/tabela_memoria.md`](docs/tabela_memoria.md) |
| Arquivo JSON | Dados salvos em `data/colheitas.json` |
| Arquivo TXT | Relatório gerado em `reports/relatorio_colheitas.txt` |
| Banco Oracle | Script SQL em `docs/modelo_oracle.sql` e conexão em `database.py` |
| Validação de dados | Funções `ler_texto_obrigatorio()`, `ler_numero_positivo()` e `ler_opcao_menu()` |
| Usabilidade | Menu interativo, mensagens claras e tabelas alinhadas no terminal |

## Regras de cálculo

### Produção esperada

```text
produção esperada = área do talhão × produtividade estimada
```

### Perda em toneladas

```text
perda em toneladas = produção esperada - produção colhida
```

Se a produção colhida for maior que a esperada, o sistema considera perda igual a zero.

### Percentual de perda

```text
percentual de perda = (perda em toneladas / produção esperada) × 100
```

### Prejuízo estimado

```text
prejuízo estimado = perda em toneladas × valor da tonelada
```

### Critérios didáticos de classificação

| Percentual de perda | Status |
|---:|---|
| Até 5% | `BAIXO` |
| Acima de 5% até 10% | `ATENCAO` |
| Acima de 10% | `CRITICO` |

> Os critérios de classificação foram definidos para fins didáticos e não substituem análise agronômica profissional.

## Estrutura do projeto

```text
canaguard/
├── README.md
├── .gitignore
├── main.py
├── database.py
├── config.example.py
├── requirements.txt
│
├── data/
│   └── colheitas.json
│
├── docs/
│   ├── modelo_oracle.sql
│   └── tabela_memoria.md
│
└── reports/
    └── .gitkeep
```

## Como executar

### 1. Clone o repositório

```bash
git clone [URL_DO_REPOSITORIO]
cd canaguard
```

### 2. Crie e ative um ambiente virtual

No Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Instale as dependências

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure a conexão Oracle

Copie o arquivo de exemplo:

```powershell
Copy-Item config.example.py config.py
```

Preencha `config.py` com as credenciais Oracle fornecidas pela instituição:

```python
ORACLE_USER = "SEU_USUARIO"
ORACLE_PASSWORD = "SUA_SENHA"
ORACLE_DSN = "HOST:PORT/SERVICE_NAME"
```

> O arquivo `config.py` está no `.gitignore` e não deve ser enviado ao repositório.

### 5. Crie a tabela Oracle

Execute o arquivo:

```text
docs/modelo_oracle.sql
```

no Oracle SQL Developer ou ferramenta disponibilizada pela disciplina.

### 6. Execute o sistema

```powershell
python main.py
```

## Menu da aplicação

```text
1 - Cadastrar colheita
2 - Listar colheitas
3 - Consultar por talhao
4 - Exibir registros criticos
5 - Salvar dados em JSON
6 - Carregar dados do JSON
7 - Gerar relatorio em TXT
8 - Gravar ultimo registro no Oracle
9 - Consultar registros do Oracle
0 - Sair
```

## Exemplo de uso

Dados de entrada:

```text
Talhão: T-01
Área: 10 hectares
Produtividade estimada: 100 toneladas/hectare
Produção colhida: 850 toneladas
Valor da tonelada: R$ 145,00
```

Resultado esperado:

```text
Produção esperada: 1000.00 t
Perda estimada: 150.00 t
Percentual de perda: 15.00%
Prejuízo estimado: R$ 21750.00
Classificação: CRITICO
```

## Persistência de arquivos

### JSON

Os registros são salvos em:

```text
data/colheitas.json
```

O arquivo permite recuperar os dados entre diferentes execuções do programa.

### Relatório TXT

O sistema gera um relatório consolidado em:

```text
reports/relatorio_colheitas.txt
```

O relatório contém resumo geral, perda total estimada, prejuízo total estimado, quantidade de registros críticos e detalhamento por talhão.

## Integração Oracle

A integração com Oracle está organizada nos seguintes arquivos:

| Arquivo | Responsabilidade |
|---|---|
| `docs/modelo_oracle.sql` | Criação da tabela `COLHEITA_CANA` |
| `config.example.py` | Modelo de configuração de acesso |
| `config.py` | Credenciais locais, ignoradas pelo Git |
| `database.py` | Conexão, inserção e consulta no Oracle |
| `main.py` | Menu para gravar e consultar registros |

A aplicação utiliza o pacote `python-oracledb` e comandos SQL parametrizados.

> A execução da integração depende da disponibilidade, desbloqueio e credenciais do ambiente Oracle fornecido pela instituição.

## Integrantes

| Nome | RM |
|---|---|

Guilherme Cabral Mendes Mariano | 574221

## Observações

Este projeto tem finalidade acadêmica. As estimativas financeiras e os critérios de classificação representam uma simulação para demonstrar aplicação de lógica de programação, estruturas de dados, manipulação de arquivos e banco de dados em um contexto do agronegócio.
