---
name: pptx-design-system
description: >-
  Sistema de design e regras invioláveis dos slides .pptx da disciplina
  "Jurimetria e Análise de Dados para Decisões Estratégicas". Define
  paleta, tipografia, áreas úteis em EMU, motivos visuais permitidos e
  proibições. Use quando estiver editando, revisando ou criando qualquer
  slide do projeto, ou quando o usuário perguntar sobre paleta, fontes,
  layout, fundo (image1.png/image2.png), cores ibmec ou regras de design
  da disciplina.
---

# Sistema de design — slides da disciplina

Os slides nascem do `docs/templates/layout.pptx`. As regras aqui são
**invioláveis**: qualquer violação invalida o entregável.

## 1. Fundos (regras 4 e 5 da disciplina)

`image1.png` e `image2.png` definem a identidade visual (moldura cinza,
faixa amarela lateral, logo ibmec, selo "ibmec.br") e **nunca** são
redesenhadas, substituídas ou cobertas.

A convenção canônica fixada pela **Aula 1 publicada (gold standard)**:

| Tipo de slide | Fundo (no `.pptx` final) |
|---------------|-------|
| Capa do bloco | `image1.png` (forte) |
| Transição de tópico (01, 02, …) | `image1.png` (forte) |
| Encerramento ("Fim do Bloco N", "Fim da Aula N") | `image1.png` (forte) |
| Todo o resto: agenda, objetivos, conexão, síntese, ponte, referências, atividade prática, correção, conteúdo | `image2.png` (suave) |

> **Atenção ao bug do template.** O `docs/templates/layout.pptx` tem os
> PNGs físicos **trocados** em relação à convenção acima
> (`layout.pptx::image1.png` é o suave, `layout.pptx::image2.png` é o
> forte). O build script da `build-aula-pptx` faz um **swap idempotente**
> antes de gerar o deck para que o `.pptx` final fique no padrão
> canônico (`image1.png` = forte). Detalhes em
> `.cursor/skills/build-aula-pptx/layout-canonical.md` §1 e §1.1.

Em cada `ppt/slides/slideN.xml`, mantenha intacto o bloco:

```xml
<p:bg><p:bgPr><a:blipFill><a:blip r:embed="rId3"/>...</a:blipFill></p:bgPr></p:bg>
```

E `rId3` apontando para a mídia correta em `slideN.xml.rels` (referência
sempre pelo nome final do `.pptx`, não pelo nome do template).

## 2. Dimensões e área útil

- **Slide:** `9144000 × 5143500` EMU (16:9). Nunca alterar.
- **Conteúdo (fundo `image2.png` no `.pptx` final):** hard limit
  `x ∈ [400000, 7970000]`, `y ∈ [400000, 4685000]`; soft limit
  `x ∈ [750000, 7700000]`, `y ∈ [500000, 4650000]` (H1 da Aula 1
  começa em `y=500000` EMU).
- **Capa, transição e encerramento (fundo `image1.png` no `.pptx`
  final):** mesmo hard limit; soft limit mais apertado, eixo de texto
  alinhado a `x≈1097275` (capa/transição) ou `x≈822950` (encerramento).
  Detalhes em
  `.cursor/skills/build-aula-pptx/layout-canonical.md` §0.

Conversão: 914400 EMU = 1 polegada; 360000 EMU = 1 cm; sz="2400" = 24pt
em XML de fontes.

## 3. Paleta

| Uso | Hex |
|-----|-----|
| Primária / títulos / textos fortes | `#1B2A4A` (navy ibmec) |
| Acento / destaque / números grandes / ícones | `#E8A317` (amarelo/laranja ibmec) |
| Texto secundário / legendas / citações de fonte | `#666666` |
| Texto corrido | `#333333` ou `#1B2A4A` |
| Fundo de cards | `#F4F4F4` ou `#FFF7E6` |
| Branco | `#FFFFFF` |

**Regra 60/30/10:** navy domina, cinza/branco apoia, amarelo é acento.
**Nunca** mais de ~15% do slide com amarelo sólido.

## 4. Tipografia

| Elemento | Fonte | Tamanho | Cor |
|----------|-------|---------|-----|
| Títulos H1 | Arial Black bold | 24pt (Aula 1) ou 32–40pt | navy `#1B2A4A` |
| Subtítulo sob H1 (Agenda, Objetivos) | Arial Bold | 14pt | amarelo `#E8A317` |
| Outros subtítulos | Arial Black ou Arial Bold | 20–24pt | navy ou amarelo |
| Corpo | Arial / Calibri | 14–18pt | `#333333` ou `#1B2A4A` |
| Legendas / rodapés / citação de fonte | Arial | 10–12pt | cinza `#666666` |
| Citação temática | Arial Italic | 14–18pt | cinza |

## 5. Motivos visuais permitidos

- **Faixa amarela horizontal (regra 11)** (`#E8A317`, altura **fixa**
  `54900` EMU, `y=905100` fixo, `x≈750005`/`750006`, `cx` variando de
  `1500000` a `1808100` EMU conforme largura do H1): (1) **sob o H1**
  em slides de **conteúdo e estruturais** (padrão Aula 1); (2) em
  **capas** e **transições**, com geometria própria. Detalhes em
  `.cursor/skills/build-aula-pptx/layout-canonical.md`.
- Stat callouts: número grande amarelo + rótulo cinza pequeno abaixo.
- Ícones: formas geométricas em círculos navy ou amarelos. Sem emojis.
- Cards: borda fina navy ou fundo `#F4F4F4` / `#FFF7E6`.
- Setas, timelines e fluxos em navy com nós amarelos.

## 6. Proibições

- ❌ Barras coloridas full-width sobre o fundo.
- ❌ Retângulos coloridos decorativos.
- ❌ Fundo bege/creme.
- ❌ Omitir a **faixa amarela canônica** sob o H1 em slides de conteúdo que
  seguem o cabeçalho padrão da Aula 1 (regra 11; exceto slides só diagrama sem H1).
- ❌ Bullets com `•` literal — use `<a:buChar>` ou `<a:buAutoNum>`.
- ❌ Texto navy pequeno sobre a faixa amarela.
- ❌ **Texto amarelo `#E8A317` sobre fundo navy `#1B2A4A`** (use branco — regra 10).
- ❌ **Texto navy `#1B2A4A` sobre fundo amarelo `#E8A317`** (use branco — regra 10).
- ❌ **Cards com fundo branco sem borda navy** (regra 10).
- ❌ Slides só de texto: todo slide tem ao menos 1 elemento visual
  (ícone, forma, número grande, card, chart, diagrama, tabela, imagem).
- ❌ **Sobreposição de elementos ou texto cortado** (regra 12). Espaço
  mínimo entre formas adjacentes: `60000` EMU.
- ❌ Travessões (`—`, `–`) ou hífens como separador parentético.
  Detalhes em `.cursor/skills/build-aula-pptx/content-rules.md`.

## 7. Como aplicar ao revisar um slide

Use este checklist rápido em qualquer revisão:

```
- [ ] Fundo correto (image1=forte para capa/transição/fim;
      image2=suave para o resto) e bloco <p:bg> intacto
- [ ] Texto dentro da área útil (hard limit x ≤ 7970000, y ≤ 4685000)
- [ ] Cores apenas da paleta (navy, amarelo, cinza, branco)
- [ ] Combinações proibidas evitadas (sem amarelo sobre navy, sem
      navy sobre amarelo; texto branco quando contrastar com cor cheia)
- [ ] Cards brancos têm borda navy w=12700 (regra 10)
- [ ] Hierarquia tipográfica respeitada (Arial Black em H1, Arial em corpo)
- [ ] Faixa amarela sob H1 (cy=54900 fixo) presente em todo slide com
      título (regra 11)
- [ ] Pelo menos 1 elemento visual além de texto
- [ ] Nenhuma barra colorida cobrindo a moldura/faixa amarela
- [ ] Rodapé interno com citação Autor (ano), 10–12pt, cinza, itálico
      (quando o slide introduz conceito)
- [ ] Sem travessões ou hífens parentéticos no texto
- [ ] Sem sobreposição entre formas vizinhas (≥ 60000 EMU de respiro)
```

## Referência cruzada

- `.cursor/skills/build-aula-pptx/layout-canonical.md` — layouts padronizados
  e referência à Aula 1.
- `.cursor/skills/build-aula-pptx/SKILL.md` — fluxo de construção do bloco.
- `.cursor/skills/build-aula-pptx/slide-templates.md` — snippets XML por layout.
- `.cursor/skills/build-aula-pptx/content-rules.md` — regras de conteúdo
  (PT-BR, citações, XY&A, proibição de travessões).
- `.cursor/skills/pptx-qa/SKILL.md` — fluxo de QA visual e textual.
