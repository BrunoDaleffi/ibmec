# Jurimetria e Análise de Dados para Decisões Estratégicas

Material de apoio, slides, notebooks e código-fonte do curso **Jurimetria e
Análise de Dados para Decisões Estratégicas** (IBMEC).

> **Jurimetria** é a aplicação de métodos quantitativos (estatística, ciência
> de dados, machine learning) ao Direito, com o objetivo de apoiar decisões
> estratégicas em escritórios, departamentos jurídicos e tribunais.

## Sumário

- [Estrutura do repositório](#estrutura-do-repositório)
- [Pré-requisitos](#pré-requisitos)
- [Setup](#setup)
- [Como usar](#como-usar)
- [Convenções de código](#convenções-de-código)
- [Aulas](#aulas)

## Estrutura do repositório

```
.
├── aulas/                  # Conteúdo por aula (slides + notebooks + dados)
│   ├── aula_01/
│   │   ├── slides/         # Apresentações (.pptx)
│   │   ├── notebooks/      # Notebooks Jupyter da aula
│   │   ├── dados/          # Dados específicos da aula (não versionados)
│   │   └── README.md
│   ├── aula_02/
│   ├── aula_03/
│   ├── aula_04/
│   └── aula_05/
├── src/
│   └── jurimetria/         # Pacote Python com utilidades compartilhadas
│       ├── __init__.py
│       ├── paths.py        # Caminhos canônicos do projeto
│       └── io.py           # Helpers de leitura/escrita de dados
├── data/                   # Dados compartilhados entre aulas (não versionados)
│   ├── raw/                # Dados originais (read-only)
│   ├── processed/          # Dados tratados, prontos para análise
│   └── external/           # Dados de terceiros (CNJ, tribunais, etc.)
├── docs/                   # Documentação do curso
│   ├── plano_curso.docx    # Plano de ensino
│   └── templates/          # Templates de slides etc.
├── scripts/                # Scripts auxiliares (ETL, downloads, etc.)
├── tests/                  # Testes do pacote src/jurimetria
├── pyproject.toml          # Metadados e dependências
├── uv.lock                 # Lock de dependências (uv)
├── .python-version         # Versão do Python (pyenv/uv)
└── .gitignore
```

## Pré-requisitos

- **Python 3.12+**
- [**uv**](https://docs.astral.sh/uv/) (gerenciador de pacotes/ambientes)

Instalando o `uv` (Linux/macOS):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Setup

Clone o repositório e sincronize o ambiente virtual com todas as
dependências (incluindo as de desenvolvimento):

```bash
git clone <url-do-repo>
cd jurimetria_e_analise_de_dados_para_decisoes_estrategicas
uv sync --all-extras
```

Isso cria automaticamente o `.venv/` e instala tudo o que está no
`pyproject.toml` + `uv.lock`.

## Como usar

### Abrir os notebooks de uma aula

```bash
uv run jupyter lab aulas/aula_01/notebooks
```

### Rodar um script Python

```bash
uv run python scripts/meu_script.py
```

### Rodar os testes

```bash
uv run pytest
```

### Lint / formatação

```bash
uv run ruff check .
uv run ruff format .
```

### Importar os utilitários nos notebooks

O pacote `jurimetria` é instalado em modo editável pelo `uv sync`,
então pode ser importado de qualquer notebook:

```python
from jurimetria import RAW_DATA_DIR
from jurimetria.io import load_raw_csv

df = load_raw_csv("processos.csv")
```

## Convenções de código

- **Estilo**: [PEP 8](https://peps.python.org/pep-0008/), enforced via `ruff`.
- **Linha**: até 100 caracteres.
- **Imports**: ordenados pelo `ruff` (regra `I`, equivalente ao `isort`).
- **Type hints**: encorajados em código de `src/`.
- **Notebooks**: limpos antes de commitar (sem outputs gigantes ou
  metadados de kernels específicos da máquina).
- **Dados**: NÃO commitar arquivos brutos em `data/` ou `aulas/**/dados/`.
  Use `.gitkeep` para preservar a estrutura de pastas.

## Aulas

| Aula | Tema | Pasta |
| ---- | ---- | ----- |
| 1 | Introdução à Jurimetria | [`aulas/aula_01`](aulas/aula_01) |
| 2 | _A definir_ | [`aulas/aula_02`](aulas/aula_02) |
| 3 | _A definir_ | [`aulas/aula_03`](aulas/aula_03) |
| 4 | _A definir_ | [`aulas/aula_04`](aulas/aula_04) |
| 5 | _A definir_ | [`aulas/aula_05`](aulas/aula_05) |

Detalhes completos no plano de ensino: [`docs/plano_curso.docx`](docs/plano_curso.docx).
