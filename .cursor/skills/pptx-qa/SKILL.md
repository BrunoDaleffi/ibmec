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

## Fluxo

```
- [ ] 1. Renderizar .pptx -> .pdf
- [ ] 2. Renderizar .pdf -> JPEGs (1 por slide)
- [ ] 3. Inspecionar capa, 1 transição, 3 conteúdos variados, referências, encerramento
- [ ] 4. Extrair texto e conferir cobertura do plano
- [ ] 5. Rodar checagem de travessões e corrigir todos
- [ ] 6. Aplicar correções em UM ciclo e re-renderizar
```

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

Abra os JPEGs (no Cursor, basta dar `Read` no arquivo de imagem dentro da
chat). Inspecione **no mínimo**:

- Capa (slide 1).
- 1 slide de transição (qualquer transição de tópico).
- 3 slides de conteúdo variados (idealmente 1 conceito, 1 stat callout,
  1 comparação ou diagrama).
- Slide de referências consolidadas.
- Slide de encerramento.

Procure por:

- **Texto cortado** ou invadindo a faixa amarela (à direita) ou a
  moldura cinza (bordas).
- **Sobreposição** com o logo ibmec ou o selo "ibmec.br".
- **Contraste ruim** (texto navy sobre amarelo, texto cinza pequeno
  sobre cinza, texto branco sobre branco).
- **Linha amarela decorativa** sob título de slide de conteúdo.
- **Bullets com `•` literal** em vez de `<a:buChar>`.
- **Slides só de texto** (precisam de pelo menos 1 elemento visual).

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

### 6. Correção em um ciclo

Aplique todas as correções, re-empacote (`pack_pptx.py`), re-renderize
e confirme. **Não entre em loop perfeccionista** — um ciclo é suficiente.

## Checklist final

```
- [ ] Slide 1: capa com fundo image2.png, título da aula e bloco
- [ ] Slides de transição: fundo image2.png, título grande, linha amarela
- [ ] Slides de conteúdo: fundo image1.png intacto
- [ ] 35 a 45 slides
- [ ] Nenhum texto invade a faixa amarela ou cobre o logo
- [ ] Paleta respeitada (navy, amarelo, cinza, branco)
- [ ] Todos os tópicos do plano cobertos e na ordem
- [ ] Nenhum slide só de texto
- [ ] Zero travessões/hífens parentéticos no texto
- [ ] Citação Autor (ano) presente nos slides que introduzem conceito
- [ ] Slide consolidado de referências antes do "Obrigado"
- [ ] extract_slide_text.py sem placeholders
```

## Referência cruzada

- `.cursor/skills/build-aula-pptx/SKILL.md` — construção do bloco.
- `.cursor/skills/pptx-design-system/SKILL.md` — regras de design.
- `.cursor/skills/build-aula-pptx/content-rules.md` — regras de conteúdo.
