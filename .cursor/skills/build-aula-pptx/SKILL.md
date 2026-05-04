---
name: build-aula-pptx
description: >-
  Constrói o arquivo .pptx de um bloco de aula da disciplina "Jurimetria e
  Análise de Dados para Decisões Estratégicas" a partir do plano de ensino
  (docs/plano_curso.docx) e do template oficial (docs/templates/layout.pptx).
  Use quando o usuário pedir para "montar a aula X", "gerar o bloco Y",
  "criar o pptx", "produzir o slide deck" ou variações no contexto desta
  disciplina. Cobre o fluxo completo: extrair conteúdo do plano, desempacotar
  o layout, planejar 40 slides, editar XML, empacotar e salvar em
  aulas/aula_X/slides/aulaX_blocoY_jurimetria.pptx.
---

# Construir o .pptx de um bloco de aula

Esta skill orquestra a produção de **um arquivo `.pptx` para um único bloco**.

## Regras invioláveis da disciplina (ler antes de qualquer coisa)

1. **Toda aula tem 2 blocos de 1h50.** Bloco 1 termina com slide de
   **encerramento do Bloco 1** ("Fim do Bloco 1 · Intervalo de 15
   minutos"); Bloco 2 termina com **encerramento da aula** ("Fim da
   Aula N").
2. **Todo bloco tem exatamente 40 slides.** Não 35, não 45. **40.**
3. **Todo bloco contém:** (i) capa, (ii) agenda, (iii) objetivos,
   (iv) transições de tópico, (v) slide final de encerramento (do bloco
   ou da aula). Além disso:
   - **Todo Bloco 1 (das Aulas 2 a 5)** contém **3 slides de correção
     dos exercícios da aula anterior**, um slide por questão (Q1, Q2,
     Q3), na mesma ordem do enunciado original. Aula 1 · Bloco 1 é a
     única exceção (não há atividade anterior).
   - **Todo Bloco 2 (das Aulas 1 a 4)** contém **um único slide de
     Atividade Prática**, com o enunciado das 3 questões e instruções
     de entrega. Aulas 5 e 6 não têm Atividade Prática.
4. **Capa, transição de tópico e encerramento usam o fundo `image2.png`
   do `docs/templates/layout.pptx`** (o "forte", com faixa amarela
   cheia + logo no amarelo).
5. **Slides de conteúdo (e demais estruturais)** usam o fundo
   `image1.png` do `docs/templates/layout.pptx` (o "suave", com logo no
   branco). **Atenção:** os PNGs físicos do template estão trocados em
   relação à convenção visual da disciplina; o build script faz o swap
   idempotente para que, no `.pptx` final, `image1.png` carregue o
   fundo "forte" e `image2.png` o fundo "suave" (igual à Aula 1
   publicada). Ver `layout-canonical.md` §1 e §1.1 para o protocolo
   completo e os md5 canônicos.
6. **Sempre que possível, traga referências reais** (Nunes, ABJ, CNJ,
   TJSP, Susskind, Wheelan, Huff, Silver, Katz, James et al., etc.) com
   ano e fonte explícitos. Ver `content-rules.md` §"Referência
   bibliográfica em cada conceito relevante".
7. **Proibido o uso de travessões (`—`, `–`) ou hífens em função
   parentética** no conteúdo dos slides (corpo, títulos, subtítulos,
   bullets, speaker notes). Ver `content-rules.md` §"Proibição de
   travessões".
8. **Margens canônicas obrigatórias** por tipo de slide (conteúdo,
   capa, transição, encerramento). Tamanhos de caixas de texto, cards,
   imagens, tabelas, fontes — todos extraídos diretamente do XML do
   Bloco 1 da Aula 1 (gold standard) e consolidados em
   [`layout-canonical.md`](layout-canonical.md) §0 e §§2 a 14a.
9. **Seguir rigorosamente `docs/plano_curso.docx`** (cronograma
   detalhado das aulas). Toda aula precisa entregar conteúdo relevante
   com **mini-casos práticos detalhados** sempre que possível antes de
   formalizar o método. Ver `content-rules.md` §"Mini-casos práticos
   antes da formalização" para exemplos canônicos (moeda × testes de
   hipóteses; provisionamento estratégico × modelos de desfecho/tempo/
   valor).
10. **Design "estiloso" permitido e encorajado** dentro da paleta e da
    tipografia canônicas (definições em caixas navy com texto branco;
    bullets estilizados com círculos amarelos ou navy; cards para
    informações importantes; diagramas; tabelas; imagens). Cores: navy
    `#1B2A4A` para títulos, amarelo `#E8A317` para subtítulos. **Fundo
    azul não combina com texto amarelo** (use branco). **Fundo amarelo
    não combina com texto azul** (use branco). Cards/caixas com fundo
    branco devem ter **borda navy** (slide 16 do Bloco 1 da Aula 1 é o
    exemplo canônico). Ver `design-system.md` §§"Combinações de cores"
    e "Cards brancos com borda navy".
11. **Todo título (H1) tem, logo abaixo, a faixa amarela horizontal
    canônica** em `#E8A317`, com altura fixa `54900` EMU e largura fixa
    `1500000` EMU (em transições) ou variável conforme a largura do H1
    nos slides estruturais (vai de `~1500000` a `~1808100` EMU). Ver
    `layout-canonical.md` §2. Inegociável em qualquer slide com H1
    textual.
12. **Após montar cada slide, valide visualmente em ciclo iterativo**
    até que não haja sobreposição de conteúdo nem texto cortado. Use
    `check_useful_area.py` (área útil) e a renderização JPEG da
    `pptx-qa` (sobreposição). Espaçamento mínimo entre elementos: ver
    `layout-canonical.md` §0.4. **Iterativo significa:** monta →
    renderiza → analisa → corrige → re-renderiza → analisa → corrige,
    até zero erros visuais. Ver passo 10 do fluxo abaixo.

## Antes de começar

Confirme com o usuário, em uma única pergunta objetiva, se faltar:

- **Aula** (1 a 6) e **Bloco** (1 ou 2).
- Eventuais ênfases ou recortes específicos.

Se o usuário já informou (ex.: "monta aula 2 bloco 1"), siga em frente.

## Fluxo (execute SEMPRE nesta ordem)

Copie este checklist e atualize conforme avança:

```
- [ ] 1. Ler o conteúdo do bloco no plano de ensino
- [ ] 2. Ler as regras de design e conteúdo (referências)
- [ ] 3. Desempacotar o layout.pptx
- [ ] 4. Planejar os 40 slides em texto (validar internamente)
- [ ] 5. Duplicar slides (slide1.xml para capa/transição, slide2.xml para conteúdo)
- [ ] 6. Editar o XML de cada slide (textos, formas, cards, ícones)
- [ ] 7. Atualizar presentation.xml com a ordem final dos sldId
- [ ] 8. Empacotar em aulas/aula_X/slides/aulaX_blocoY_jurimetria.pptx
- [ ] 9. QA visual + textual (delegar para pptx-qa)
- [ ] 10. Aplicar correções de um único ciclo (não entrar em loop)
```

### 1. Ler o conteúdo do bloco

Use o script para extrair somente o trecho do plano referente ao bloco
solicitado. Isso evita sobrecarregar o contexto:

```bash
uv run python .cursor/skills/build-aula-pptx/scripts/extract_block_from_plan.py \
  docs/plano_curso.docx --aula <X> --bloco <Y>
```

Saída: lista numerada dos tópicos do bloco, na ordem do plano. **Todos** os
tópicos retornados precisam aparecer no deck final, na ordem indicada.
Você pode expandir, exemplificar e intercalar slides adicionais, mas
**não pode omitir tópicos nem reordenar a sequência pedagógica**.

### 2. Ler as regras

Antes de planejar slides, leia (se ainda não estiverem no contexto):

- [`layout-canonical.md`](layout-canonical.md) — **obrigatório:** tipos de
  slide padronizados (capa, agenda, objetivos, transição, correção,
  atividade, etc.) com referência aos XML da **Aula 1**; faixa amarela sob H1
  em conteúdo; checklist de paridade visual. Inclui o **catálogo §14a de
  design "estiloso" replicável** (Venn 3 círculos, cards 2×2 numerados,
  comparação em cards coloridos, tabela com coluna semântica, etc.) com
  slide-fonte da Aula 1 para copiar.
- [`design-system.md`](design-system.md) — paleta, tipografia, áreas úteis,
  regras invioláveis do layout (image1.png/image2.png como fundos).
- [`content-rules.md`](content-rules.md) — proibição de travessões,
  citação por conceito, fio condutor XY&A, registro PT-BR formal-didático.
- [`pedagogical-structure.md`](pedagogical-structure.md) — macroestrutura
  de **exatamente 40 slides**, **diferente entre Bloco 1 e Bloco 2**.
  Atividade prática só no Bloco 2 (Aulas 1 a 4). Bloco 1 das Aulas 2 a
  5 abre com a correção comentada da atividade do Bloco 2 da aula
  anterior, em **3 slides de correção (1 por questão)**.
- [`slide-templates.md`](slide-templates.md) — snippets XML prontos para
  os layouts mais usados (cabeçalho Aula 1, capa, transição, conceito,
  stat callout, comparação 2 colunas, diagrama, citação, referências
  consolidadas).

### 3. Desempacotar o layout

```bash
uv run python .cursor/skills/build-aula-pptx/scripts/unpack_pptx.py \
  docs/templates/layout.pptx /tmp/deck_aulaX_blocoY/
```

Estrutura resultante:

```
/tmp/deck_aulaX_blocoY/
├── ppt/slides/slide1.xml          # molde com fundo image2.png (use para agenda, objetivos, conteúdo, etc.)
├── ppt/slides/slide2.xml          # molde com fundo image1.png (use para capa, transição, fim)
├── ppt/slides/_rels/slideN.xml.rels
├── ppt/media/image1.png           # NÃO TOCAR
├── ppt/media/image2.png           # NÃO TOCAR
├── ppt/presentation.xml           # editar p:sldIdLst no final
└── ...
```

### 4. Planejar os 40 slides em texto

Antes de tocar em XML, escreva uma tabela com:

| # | Tipo | Layout | Título | Esboço de conteúdo | Fundo |
|---|------|--------|--------|---------------------|-------|

- **Tipo:** capa / transição / conteúdo / correção_atividade / atividade_prática / síntese / referências / fim
- **Layout:** conceito, stat callout, comparação, diagrama, tabela, citação, mini-caso, armadilha, card-com-borda-navy, caixa-navy-com-texto-branco
- **Fundo (no `.pptx` final, após o swap):** `image1.png` para capa do
  bloco, transição de tópico (01, 02, …) e encerramento ("Fim do Bloco
  N", "Fim da Aula N"); `image2.png` para todo o resto (agenda,
  objetivos, conexão, conteúdo, síntese, ponte, referências, atividade
  prática, correção). **Equivalência no template:** `image1.png` final
  = `image2.png` do `layout.pptx` original (forte); `image2.png` final
  = `image1.png` do `layout.pptx` original (suave). O swap idempotente
  do build script faz essa correspondência automaticamente.

Atenção à **diferença entre Bloco 1 e Bloco 2** (ver
`pedagogical-structure.md`):

- **Bloco 1 das Aulas 2 a 5** abre com **correção comentada** da
  atividade entregue no Bloco 2 da aula anterior. Bloco 1 **não** tem
  Atividade Prática nova. A correção ocupa **5 slides**: 1 transição
  + 1 recap + **3 slides de correção (exatamente 1 por questão, na
  ordem original Q1, Q2, Q3)**.
- **Bloco 2 das Aulas 1 a 4** fecha com **Atividade Prática N** em **um
  único slide**, que tem **exatamente 3 questões numeradas (Q1, Q2,
  Q3)** e instruções de entrega. Bloco 2 das Aulas 5 e 6 não tem
  Atividade.
- **Aula 1 · Bloco 1** é o único bloco do curso que não tem nem
  correção no início nem atividade no fim.
- O número (Q1, Q2, Q3) e a ordem das 3 questões definidas no Bloco 2 são
  **preservados** nos 3 slides de correção do Bloco 1 da aula seguinte.

Confira contra `pedagogical-structure.md`. O alvo é **exatamente 40
slides por bloco**. Se um tópico do plano gerar 6–10 slides, use 1
slide de transição de tópico (fundo `image1.png`) antes do
desenvolvimento.

Valide internamente: todos os tópicos do plano estão cobertos? Há ao menos
1 stat callout, 1 comparação, 1 diagrama e 1 tabela ao longo do bloco?

### 5. Duplicar slides

**Atenção ao mapeamento real do `layout.pptx`:** o template foi criado
com a convenção antiga (slide1.xml = `image2.png`, slide2.xml =
`image1.png`). A convenção atual da disciplina (fixada pela Aula 1) é o
oposto: `image1.png` é o fundo "forte" usado em capa/transição/fim e
`image2.png` é o fundo "suave" usado nos demais slides.

> **PNGs físicos do template estão trocados em relação à convenção
> canônica.** Todo build script novo deve, em ordem, no `main()`:
> (1) `unpack_layout_fresh()` com `--force` para apagar
>     `/tmp/deck_aulaX_blocoY/` antes do unpack;
> (2) `swap_media_para_aula1()` **idempotente** (compara
>     `md5(image1.png)` com `b0987cbbb2c05a7cebbd3bac3576c0bb` e só
>     troca se estiver fora do estado canônico).
> Receita pronta em [`layout-canonical.md` §1.1](layout-canonical.md).
> Esquecer o `--force` ou usar swap não-idempotente causa double-swap
> e deck com fundos invertidos (incidente 2026-05-02).

Por isso, ao duplicar do template, o **molde** (`slide1.xml` ou
`slide2.xml`) é escolhido pelo **fundo** que ele já carrega, não pelo
papel pedagógico do nome. Use a tabela:

| Tipo do slide novo | Fundo desejado | Duplique do template |
|---|---|---|
| Capa, transição de tópico (01, 02, …), encerramento ("Fim do Bloco N", "Fim da Aula N") | `image1.png` | `slide2.xml` |
| Agenda, objetivos, conexão, conteúdo, síntese, ponte, referências, atividade prática, correção | `image2.png` | `slide1.xml` |

```bash
# Slide com fundo image1.png (capa, transição, fim) — duplica slide2.xml
uv run python .cursor/skills/build-aula-pptx/scripts/add_slide.py \
  /tmp/deck_aulaX_blocoY/ slide2.xml

# Slide com fundo image2.png (todos os demais) — duplica slide1.xml
uv run python .cursor/skills/build-aula-pptx/scripts/add_slide.py \
  /tmp/deck_aulaX_blocoY/ slide1.xml
```

> **Verificação obrigatória.** Após duplicar, confirme em
> `ppt/slides/_rels/slideN.xml.rels` que o `Target` do `rId3` aponta
> para `../media/image1.png` ou `../media/image2.png` conforme a regra
> da seção 1 de `layout-canonical.md`. Se estiver errado, edite o
> `Target` antes de continuar.

O script imprime o `<p:sldId>` correspondente, que deve ser inserido
em `ppt/presentation.xml` dentro de `<p:sldIdLst>` na ordem desejada.

### 6. Editar o XML

Use `StrReplace` em `ppt/slides/slideN.xml` para:

- Trocar o texto dos `<a:t>...</a:t>` (títulos, bullets, legendas).
- Adicionar `<p:sp>` (formas, cards, ícones, tabelas) dentro de
  `<p:spTree>`, respeitando os limites de área útil.
- Adicionar `<a:buChar>` ou `<a:buAutoNum>` para bullets (NÃO usar `•` literal).

**Não toque** nos seguintes blocos em nenhum slide:

- `<p:bg><p:bgPr><a:blipFill><a:blip r:embed="rId3">...</p:bg>` — define o fundo.
- `rId3` no `slideN.xml.rels` — aponta para `image1.png` ou `image2.png`.

Para snippets XML prontos (caixa de título, card, stat callout, comparação
em 2 colunas, fluxo, citação), consulte [`slide-templates.md`](slide-templates.md).

### 7. Atualizar `presentation.xml`

Em `ppt/presentation.xml`, dentro de `<p:sldIdLst>`:

1. Remova o `<p:sldId>` de `slide2.xml` original (modelo em branco).
2. Mantenha ou edite `<p:sldId>` de `slide1.xml` se vai servir de capa.
3. Insira os novos `<p:sldId>` na ordem dos slides finais.

Os IDs (`r:id="rIdN"`) também precisam estar em
`ppt/_rels/presentation.xml.rels`. O script `add_slide.py` já registra
o relacionamento, então só falta a ordem dentro de `<p:sldIdLst>`.

### 8. Empacotar

**Antes** de empacotar, valide a área útil de todos os slides:

```bash
uv run python .cursor/skills/build-aula-pptx/scripts/check_useful_area.py \
  /tmp/deck_aulaX_blocoY/
```

O deck só pode ser empacotado quando o validador retornar zero violações
`[hard]`. Warnings `[soft]` indicam shapes que extrapolam a zona segura
recomendada da Aula 1 — aceitáveis em diagramas full-bleed e em casos
específicos, mas precisam ser justificados.

```bash
uv run python .cursor/skills/build-aula-pptx/scripts/pack_pptx.py \
  /tmp/deck_aulaX_blocoY/ aulas/aula_X/slides/aulaX_blocoY_jurimetria.pptx
```

O script preserva timestamps e a estrutura ZIP exatamente como o PowerPoint
espera (incluindo `[Content_Types].xml` na raiz).

### 9. QA visual + textual

Delegue para a skill `pptx-qa`:

```bash
uv run python .cursor/skills/pptx-qa/scripts/render_to_pdf.py \
  aulas/aula_X/slides/aulaX_blocoY_jurimetria.pptx /tmp/qa/

uv run python .cursor/skills/pptx-qa/scripts/render_to_jpegs.py \
  /tmp/qa/aulaX_blocoY_jurimetria.pdf /tmp/qa/

uv run python .cursor/skills/build-aula-pptx/scripts/extract_slide_text.py \
  aulas/aula_X/slides/aulaX_blocoY_jurimetria.pptx

uv run python .cursor/skills/pptx-qa/scripts/check_no_emdash.py \
  aulas/aula_X/slides/aulaX_blocoY_jurimetria.pptx
```

Inspecione pelo menos: capa, 1 transição, 3 slides de conteúdo variados,
o slide de referências e o de encerramento. Procure por:

- Texto cortado ou invadindo a faixa amarela.
- Sobreposição com a moldura cinza ou logo.
- Contraste ruim (texto navy sobre fundo escuro, etc.).
- Travessões ou hífens em função parentética (corrigir todos).

### 10. Correção iterativa até zero violações visuais

Aplique os ajustes apontados no QA e itere: **monta → renderiza →
analisa → corrige → re-renderiza → analisa → corrige**, até que:

- `check_useful_area.py` retorne **zero hard violations**.
- `check_no_emdash.py` retorne **zero ocorrências proibidas**.
- A inspeção visual dos JPEGs não mostre **nenhuma sobreposição** entre
  caixas de texto, cards, ícones, números ou diagramas; nem texto
  **cortado**, **invadindo a moldura cinza**, **invadindo o logo
  ibmec** ou **transbordando o card** que o contém. Tem que existir
  **um pequeno espaço (≥ 60000 EMU)** entre elementos vizinhos.

Não pare antes de zerar as três checagens. **Não confunda iterar com
loop perfeccionista**: o critério de parada é objetivo (as três
verificações zeradas), não estético. Se um slide entrar em loop com a
mesma classe de erro 3 vezes, **rebaixe a densidade do conteúdo**
(menos bullets, fonte um ponto menor, encurtar texto) em vez de
empurrar margens.

Esse ciclo iterativo é a regra 12 da disciplina e substitui a antiga
política de "1 ciclo só". Ver também `pptx-qa/SKILL.md` §"Loop
iterativo de correção visual".

## Convenção de nomes

- Arquivo final: `aulaX_blocoY_jurimetria.pptx` (X em 1–6, Y em 1–2).
- Diretório: `aulas/aula_X/slides/`.
- Diretório de trabalho do XML desempacotado: `/tmp/deck_aulaX_blocoY/`
  (não commitar; é descartável).

## Checklist final (antes de entregar ao usuário)

- [ ] Existe exatamente um `.pptx` em `aulas/aula_X/slides/aulaX_blocoY_jurimetria.pptx`.
- [ ] **Exatamente 40 slides** (regra inviolável; não 35, não 45).
- [ ] Capa, transições de tópico e encerramento usam fundo `image1.png` intacto.
- [ ] Demais slides (agenda, objetivos, conexão, conteúdo, síntese, ponte, referências, atividade prática, correção) usam fundo `image2.png` intacto.
- [ ] **`md5sum ppt/media/image1.png` no `.pptx` final = `b0987cbbb2c05a7cebbd3bac3576c0bb`** (canônico Aula 1). Se não bater, o swap não rodou ou rodou em dobro — não entregar.
- [ ] Nenhum slide invade faixa amarela ou cobre logo.
- [ ] **`check_useful_area.py` retorna zero hard violations** (área útil canônica respeitada — ver `layout-canonical.md` seção 0).
- [ ] Paleta respeitada (navy `#1B2A4A`, amarelo `#E8A317`, cinza, branco).
- [ ] Todos os tópicos do bloco do plano presentes e na ordem.
- [ ] Nenhum slide só de texto (todos têm ícone, forma, número, card, chart ou diagrama).
- [ ] Zero travessões (`—`, `–`) ou hífens como separador parentético.
- [ ] Cada conceito relevante tem citação `Autor (ano)` no rodapé interno.
- [ ] Slide consolidado de referências antes do "Obrigado".
- [ ] **Layouts canônicos:** agenda, objetivos, transição, atividade,
      correção (quando houver), síntese e encerramento **espelham Aula 1**
      (`layout-canonical.md`); slides de conteúdo com H1 têm **faixa amarela**
      sob o título.
- [ ] **Atividade Prática só aparece em Bloco 2 (Aulas 1 a 4); nunca em Bloco 1.** É **um único slide**.
- [ ] **Toda Atividade Prática tem exatamente 3 questões numeradas (Q1, Q2, Q3).**
- [ ] **Bloco 1 das Aulas 2 a 5 começa com correção da atividade do Bloco 2 anterior.**
- [ ] **A correção do Bloco 1 (Aulas 2 a 5) tem 3 slides dedicados, 1 por questão, na mesma ordem da atividade.**
- [ ] **Faixa amarela canônica** sob todo H1, com altura `54900` EMU.
- [ ] **Combinações de cor proibidas evitadas:** nenhum texto amarelo sobre fundo navy (use branco); nenhum texto navy sobre fundo amarelo (use branco). Cards brancos têm borda navy `w=12700`.
- [ ] **Mini-caso prático** apresentado antes de formalizar cada novo método (regra 9).
- [ ] **Sem sobreposição de elementos** em nenhum slide (≥ 60000 EMU de respiro entre formas vizinhas) — verificado em renderização JPEG.
- [ ] `extract_slide_text.py` não retorna placeholders nem "Lorem ipsum".

## Recursos auxiliares

- [`layout-canonical.md`](layout-canonical.md) — paridade visual com a Aula 1.
- [`design-system.md`](design-system.md) — paleta, tipografia, áreas úteis, regras invioláveis.
- [`content-rules.md`](content-rules.md) — travessões, citações, registro de língua, XY&A.
- [`pedagogical-structure.md`](pedagogical-structure.md) — macroestrutura de ~40 slides.
- [`slide-templates.md`](slide-templates.md) — snippets XML por layout.
- `scripts/unpack_pptx.py`, `scripts/pack_pptx.py`, `scripts/add_slide.py`,
  `scripts/extract_block_from_plan.py`, `scripts/extract_slide_text.py`.
