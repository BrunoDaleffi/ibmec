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

## 1. Fundos

`image1.png` e `image2.png` definem a identidade visual (moldura cinza,
faixa amarela lateral, logo ibmec, selo "ibmec.br") e **nunca** são
redesenhadas, substituídas ou cobertas.

| Tipo de slide | Fundo |
|---------------|-------|
| Capa do bloco | `image2.png` |
| Transição de tópico | `image2.png` |
| Encerramento ("Obrigado / Perguntas") | `image2.png` |
| Todo o resto (conteúdo) | `image1.png` |

Em cada `ppt/slides/slideN.xml`, mantenha intacto o bloco:

```xml
<p:bg><p:bgPr><a:blipFill><a:blip r:embed="rId3"/>...</a:blipFill></p:bgPr></p:bg>
```

E `rId3` apontando para a mídia correta em `slideN.xml.rels`.

## 2. Dimensões e área útil

- **Slide:** `9144000 × 5143500` EMU (16:9). Nunca alterar.
- **Conteúdo (`image1.png`):** `x ∈ [750000, 6700000]`, `y ∈ [500000, 4500000]`
  (H1 da Aula 1 começa em **500000** EMU).
- **Capa/transição (`image2.png`):** mesma caixa branca à esquerda, mas
  aproveite para títulos grandes.

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

- **Faixa amarela horizontal** (`#E8A317`, ~54900–55000 EMU de altura): (1)
  **sob o H1** em slides de **conteúdo** (padrão Aula 1); (2) em **capas** e
  **transições**, com geometria própria. Detalhes em
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
  seguem o cabeçalho padrão da Aula 1 (exceto slides só diagrama sem H1).
- ❌ Bullets com `•` literal — use `<a:buChar>` ou `<a:buAutoNum>`.
- ❌ Texto navy pequeno sobre a faixa amarela.
- ❌ Slides só de texto: todo slide tem ao menos 1 elemento visual
  (ícone, forma, número grande, card, chart, diagrama).
- ❌ Travessões (`—`, `–`) ou hífens como separador parentético.
  Detalhes em `.cursor/skills/build-aula-pptx/content-rules.md`.

## 7. Como aplicar ao revisar um slide

Use este checklist rápido em qualquer revisão:

```
- [ ] Fundo correto (image1 vs image2) e bloco <p:bg> intacto
- [ ] Texto dentro da área útil (x ≤ 6700000, y ≤ 4500000)
- [ ] Cores apenas da paleta (navy, amarelo, cinza, branco)
- [ ] Hierarquia tipográfica respeitada (Arial Black em H1, Arial em corpo)
- [ ] Faixa amarela sob H1 em conteúdo quando o slide segue o padrão Aula 1
      (`layout-canonical.md`)
- [ ] Pelo menos 1 elemento visual além de texto
- [ ] Nenhuma barra colorida cobrindo a moldura/faixa amarela
- [ ] Rodapé interno com citação Autor (ano), 10–12pt, cinza, itálico
      (quando o slide introduz conceito)
- [ ] Sem travessões ou hífens parentéticos no texto
```

## Referência cruzada

- `.cursor/skills/build-aula-pptx/layout-canonical.md` — layouts padronizados
  e referência à Aula 1.
- `.cursor/skills/build-aula-pptx/SKILL.md` — fluxo de construção do bloco.
- `.cursor/skills/build-aula-pptx/slide-templates.md` — snippets XML por layout.
- `.cursor/skills/build-aula-pptx/content-rules.md` — regras de conteúdo
  (PT-BR, citações, XY&A, proibição de travessões).
- `.cursor/skills/pptx-qa/SKILL.md` — fluxo de QA visual e textual.
