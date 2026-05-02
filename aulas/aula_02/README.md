# Aula 2 — O Ciclo da Ciência de Dados Aplicado ao Direito (Parte 1)

**MÉTODO — Parte 1.** Do problema à base: perguntar, mapear e coletar
(etapas 1 a 3 do ciclo) no modo raiz.

## Objetivos

- Compreender o ciclo da ciência de dados em suas 6 etapas.
- Reconhecer os critérios de uma pergunta jurimétrica investigável.
- Reescrever uma pergunta jurídica vaga em pergunta de dados.
- Mapear, a partir de uma pergunta, as variáveis e fontes necessárias.
- Identificar fontes de coleta (públicas, internas, scraping, APIs) e
  cuidados de LGPD e vieses (Bloco 2).

## Blocos

| Bloco | Tema | Slides |
|-------|------|--------|
| 1 | Correção das 3 questões da Atividade 1 + ciclo + Etapas 1 (pergunta) e 2 (mapear) | [aula2_bloco1_jurimetria.pptx](slides/aula2_bloco1_jurimetria.pptx) ⚠ |
| 2 | Etapa 3 (coletar): fontes, scraping, APIs, LGPD, vieses + Atividade Prática 2 (3 questões) | _a produzir_ |

> ⚠ **Pendência de retrabalho de fundos.** O `aula2_bloco1_jurimetria.pptx`
> foi gerado antes da consolidação do padrão visual. Os fundos `image1.png`
> e `image2.png` estão **invertidos** em relação à norma fixada pela Aula 1
> (ver `.cursor/skills/build-aula-pptx/layout-canonical.md` seção 1).
> Trocar o `Target` do `rId3` em cada `slideN.xml.rels` antes da próxima
> entrega: `image1.png` em capa/transição/encerramento; `image2.png` em
> agenda, objetivos, conexão, conteúdo, síntese, ponte, referências e
> slides de correção.

> **Política de atividades.** A Atividade Prática só aparece no Bloco 2,
> sempre com **3 questões numeradas (Q1, Q2, Q3)**. Por isso, o Bloco 1
> da Aula 2 abre com a **correção comentada das 3 questões** da Atividade 1
> (1 slide por questão) e o Bloco 2 da Aula 2 termina com a Atividade
> Prática 2 (entrega até a Aula 3).

## Materiais

- `slides/` — apresentações da aula (.pptx).
- `scripts/` — scripts auxiliares de geração dos decks.
- `notebooks/` — notebooks Jupyter usados em sala.
- `dados/` — datasets específicos desta aula (não versionados).

## Como (re)gerar o pptx do Bloco 1

```bash
uv run python .cursor/skills/build-aula-pptx/scripts/unpack_pptx.py \
    docs/templates/layout.pptx /tmp/deck_aula2_bloco1/

python3 aulas/aula_02/scripts/build_aula2_bloco1.py

uv run python .cursor/skills/build-aula-pptx/scripts/pack_pptx.py \
    /tmp/deck_aula2_bloco1/ aulas/aula_02/slides/aula2_bloco1_jurimetria.pptx
```

QA visual e textual:

```bash
uv run python .cursor/skills/pptx-qa/scripts/render_to_pdf.py \
    aulas/aula_02/slides/aula2_bloco1_jurimetria.pptx /tmp/qa/
uv run python .cursor/skills/pptx-qa/scripts/render_to_jpegs.py \
    /tmp/qa/aula2_bloco1_jurimetria.pdf /tmp/qa/
uv run python .cursor/skills/pptx-qa/scripts/check_no_emdash.py \
    aulas/aula_02/slides/aula2_bloco1_jurimetria.pptx
```

## Atividade Prática 2 (apresentada no Bloco 2; entrega até a Aula 3)

A Atividade Prática 2 é introduzida ao final do Bloco 2 da Aula 2 e
corrigida em sala no início do Bloco 1 da Aula 3, em 3 slides
distintos (1 por questão). A atividade tem **exatamente 3 questões
numeradas (Q1, Q2, Q3)**. Esboço de enunciado:

- **Q1.** Escolher 1 pergunta jurimétrica para o trabalho final do
  grupo, no formato investigável (tema, recorte, variável, comparação).
- **Q2.** Aplicar o checklist da Etapa 1 a essa pergunta e justificar
  cada um dos 4 critérios em 1 a 2 linhas.
- **Q3.** Esboçar a tabela analítica mínima (Etapa 2): listar pelo
  menos 5 variáveis com tipo (categórica, numérica, temporal) e fonte
  esperada (interna XY&A, DataJud, scraping, etc.).

Compõe o Instrumento Avaliativo 1 (média aritmética das 4 atividades,
peso 3,0 sobre 10,0).
