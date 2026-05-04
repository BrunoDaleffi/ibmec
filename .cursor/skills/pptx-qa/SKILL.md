---
name: pptx-qa
description: >-
  Faz QA (visual e textual) de um arquivo .pptx da disciplina "Jurimetria
  e Análise de Dados para Decisões Estratégicas". Renderiza para PDF e
  JPEGs para inspeção visual, extrai texto para checagem de cobertura
  do plano, e roda detecção de travessões em função parentética. Use
  quando o usuário pedir para "validar o pptx", "rodar QA da aula",
  "checar travessões", "revisar visualmente o deck", "conferir se está
  bom" ou variações no contexto desta disciplina.
---

# QA de um .pptx da disciplina

Esta skill é o estágio de validação após a `build-aula-pptx`. Roda QA
**visual** (PDF + JPEGs) e **textual** (extração de texto + checagem de
travessões + cobertura do plano).

## Pré-requisitos do sistema

- `libreoffice` (binário `soffice`) instalado para conversão pptx → pdf.
- `pdftoppm` (do pacote `poppler-utils`) para conversão pdf → jpg.

Em Debian/Ubuntu:

```bash
sudo apt install -y libreoffice poppler-utils
```

Se faltar `soffice` ou `pdftoppm`, os scripts emitem mensagem clara e
encerram com exit code 1.

## Fluxo (loop iterativo de correção visual — regra 12)

```
- [ ] 1. Renderizar .pptx -> .pdf
- [ ] 2. Renderizar .pdf -> JPEGs (1 por slide)
- [ ] 3. Inspecionar todos os slides (não só amostra) por sobreposição
- [ ] 4. Extrair texto e conferir cobertura do plano
- [ ] 5. Rodar checagem de travessões e corrigir todos
- [ ] 6. Aplicar correções e RE-RENDERIZAR
- [ ] 7. Re-inspecionar; se ainda houver erro, voltar ao passo 6
- [ ] 8. Parar somente quando: zero hard violations + zero travessões +
        zero sobreposições visuais nos JPEGs
```

> **Iterativo, não em um único ciclo.** A regra 12 da disciplina é
> explícita: "faz, analisa, corrige, refaz, analisa, corrige, refaz..."
> até que nenhuma sobreposição ou erro de layout subsista. Substituiu
> a antiga política de "1 ciclo só".

### 1–2. Renderização

```bash
uv run python .cursor/skills/pptx-qa/scripts/render_to_pdf.py \
  aulas/aula_X/slides/aulaX_blocoY_jurimetria.pptx /tmp/qa/

uv run python .cursor/skills/pptx-qa/scripts/render_to_jpegs.py \
  /tmp/qa/aulaX_blocoY_jurimetria.pdf /tmp/qa/
```

Saída: `/tmp/qa/aulaX_blocoY_jurimetria.pdf` e
`/tmp/qa/slide-001.jpg`, `/tmp/qa/slide-002.jpg`, ...

### 3. Inspeção visual

Abra os JPEGs (no Cursor, basta dar `Read` no arquivo de imagem dentro
da chat). **Inspecione todos os 40 slides** (não só amostra) e procure
por:

- **Sobreposição entre formas** (caixas de texto, cards, ícones,
  números, diagramas) — **proibido pela regra 12**. Tem que existir um
  pequeno espaço (≥ 60000 EMU) entre formas vizinhas.
- **Texto cortado**: caixa de texto pequena demais para o conteúdo, ou
  fonte grande demais para a caixa, fazendo o texto vazar para fora ou
  ficar truncado.
- **Texto invadindo a faixa amarela** (à direita do slide) ou a
  moldura cinza (bordas).
- **Sobreposição com o logo ibmec** ou o selo "ibmec.br".
- **Combinações de cor proibidas (regra 10)**: texto amarelo sobre
  navy (deveria ser branco); texto navy sobre amarelo (deveria ser
  branco); texto branco sobre branco; texto cinza sobre cinza.
- **Cards brancos sem borda navy** (regra 10).
- **Faixa amarela canônica ausente** sob algum H1 (regra 11).
- **Linha amarela decorativa** sob título de slide de conteúdo.
- **Bullets com `•` literal** em vez de `<a:buChar>` (slides com
  bullets devem usar círculos amarelos/navy estilizados, regra 10).
- **Slides só de texto** (precisam de pelo menos 1 elemento visual).
- **Mini-caso prático ausente** antes da introdução de método novo (regra 9).

### 4. Extração de texto

```bash
uv run python .cursor/skills/build-aula-pptx/scripts/extract_slide_text.py \
  aulas/aula_X/slides/aulaX_blocoY_jurimetria.pptx
```

Confira contra a saída de `extract_block_from_plan.py`:

- Todos os tópicos do plano aparecem em algum slide?
- A ordem do plano é respeitada?
- Sobrou placeholder ("Lorem ipsum", "Texto do exemplo", "Subtítulo")?
- Os títulos batem com a tabela de planejamento?

### 5. Checagem de travessões

```bash
uv run python .cursor/skills/pptx-qa/scripts/check_no_emdash.py \
  aulas/aula_X/slides/aulaX_blocoY_jurimetria.pptx
```

O script imprime cada ocorrência de `—`, `–` ou hífen em **função
parentética** com:

- Slide e número da linha do XML.
- Texto do contexto (antes e depois).
- Se é uso legítimo (intervalo numérico, palavra composta) ou proibido.

**Toda ocorrência marcada como proibida** deve ser corrigida (vírgulas,
parênteses ou nova frase). Veja exemplos em
`.cursor/skills/build-aula-pptx/content-rules.md`.

### 6. Loop iterativo de correção visual (regra 12)

Aplique as correções, re-empacote (`pack_pptx.py`), re-renderize e
re-inspecione. **Continue iterando** até que:

- `check_useful_area.py` retorne **zero hard violations**.
- `check_no_emdash.py` retorne **zero ocorrências proibidas**.
- A inspeção JPEG não mostre **nenhuma sobreposição**, texto cortado
  ou combinação de cor proibida.

**Iterativo, não perfeccionista.** O critério de parada é objetivo (as
três checagens zeradas), não estético. Se um slide entrar em loop com
a mesma classe de erro 3 vezes, **rebaixe a densidade do conteúdo**
(menos bullets, fonte um ponto menor, encurtar texto) em vez de
empurrar margens para fora do soft limit.

## Checklist final

```
- [ ] Slide 1: capa com fundo image1.png, título da disciplina e
      "Aula X – Bloco Y"
- [ ] Slides de transição (01, 02, …): fundo image1.png, número grande
      amarelo (sz=9600), título navy (sz=3600), linha amarela
- [ ] Slides de encerramento: fundo image1.png ("Fim do Bloco N" ou
      "Fim da Aula N")
- [ ] Slides de conteúdo, agenda, objetivos, conexão, síntese, ponte,
      referências, atividade prática, correção: fundo image2.png intacto
- [ ] **Exatamente 40 slides** (regra 2)
- [ ] Faixa amarela canônica (cy=54900) presente sob todo H1 (regra 11)
- [ ] Nenhum texto invade a faixa amarela ou cobre o logo
- [ ] Sem combinações proibidas: nenhum texto amarelo sobre navy;
      nenhum texto navy sobre amarelo (regra 10)
- [ ] Cards brancos com borda navy w=12700 (regra 10)
- [ ] Sem sobreposição entre formas (≥ 60000 EMU de respiro) — regra 12
- [ ] Paleta respeitada (navy, amarelo, cinza, branco)
- [ ] Todos os tópicos do plano cobertos e na ordem
- [ ] Mini-casos práticos antes da formalização de cada método (regra 9)
- [ ] Nenhum slide só de texto
- [ ] Zero travessões/hífens parentéticos no texto (regra 7)
- [ ] Citação Autor (ano) presente nos slides que introduzem conceito (regra 6)
- [ ] Slide consolidado de referências antes do encerramento
- [ ] Atividade Prática (B2 Aulas 1–4): 1 único slide com 3 questões
      Q1, Q2, Q3 (regra 3)
- [ ] Correção (B1 Aulas 2–5): 5 slides ao todo, sendo 3 dedicados às
      questões na ordem original (regra 3)
- [ ] extract_slide_text.py sem placeholders
```

## Referência cruzada

- `.cursor/skills/build-aula-pptx/SKILL.md` — construção do bloco.
- `.cursor/skills/pptx-design-system/SKILL.md` — regras de design.
- `.cursor/skills/build-aula-pptx/content-rules.md` — regras de conteúdo.
