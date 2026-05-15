# Sistema de design — slides da disciplina

Estas regras são herdadas de `docs/instrucao_geral.md` e definem a
identidade visual da disciplina. **Nenhuma exceção.**

## Regras invioláveis do layout

1. **Preservar `image1.png` e `image2.png` como fundos.** Essas imagens
   trazem a moldura cinza, a faixa amarela lateral, o logo ibmec e o selo
   "ibmec.br". Elas **nunca** são redesenhadas, substituídas, cobertas por
   retângulos de fundo, recortadas ou alteradas.
   - `image1.png` (fundo "forte", faixa amarela cheia + logo no amarelo)
     → fundo dos slides de **capa do bloco**, **transição de tópico**
     (numerados 01, 02, …) e **encerramento** ("Fim do Bloco N", "Fim da
     Aula N").
   - `image2.png` (fundo "suave", logo no branco) → fundo de **todos os
     demais slides**: agenda, objetivos, conexão, síntese, ponte,
     referências, atividade prática, exercícios dirigidos (enunciado e
     resposta) e todo slide de conteúdo regular.

   > Padrão fixado pela **Aula 1 publicada**. Versões anteriores deste
   > arquivo indicavam o oposto; ver `layout-canonical.md` seção 1 para
   > a tabela completa.

2. **Editar o XML diretamente** em `unpacked/ppt/slides/slideN.xml`,
   mantendo intacto o bloco:

   ```xml
   <p:bg>
     <p:bgPr>
       <a:blipFill>
         <a:blip r:embed="rId3"/>
         ...
       </a:blipFill>
     </p:bgPr>
   </p:bg>
   ```

   E mantendo `rId3` apontando para a mídia correta em
   `slideN.xml.rels` (`image1.png` em capa/transição/encerramento;
   `image2.png` em todo o resto).

3. **Dimensões do slide:** `9144000 × 5143500` EMU (16:9). Nunca alterar.

4. **Área útil obrigatória.** Toda forma precisa caber dentro do **hard
   limit** da moldura branca do template (calibrado pelos extremos da
   Aula 1 publicada). Use o **soft limit** para conteúdo regular:
   - **Hard limit (não passar):** `x ∈ [400000, 7970000]`,
     `y ∈ [400000, 4685000]`. Vale para qualquer tipo de slide (a moldura
     branca é a mesma).
   - **Soft limit (recomendado para conteúdo regular):**
     `x ∈ [750000, 7700000]`, `y ∈ [500000, 4650000]`.
   - **Soft limit por tipo especial** (capa, transição, encerramento):
     ver `layout-canonical.md` seção 0.2.

   Validador obrigatório antes de empacotar:
   ```bash
   uv run python .cursor/skills/build-aula-pptx/scripts/check_useful_area.py \
     /tmp/deck_aulaX_blocoY/
   ```
   O deck só pode ser empacotado quando o validador retornar zero erros
   `[hard]`.

5. **Eixo dos slides especiais** (`image1.png`): eixo de texto alinhado a
   `x≈1097275` (capa e transição) ou `x≈822950` (encerramento), com títulos
   grandes como na Aula 1. Detalhes em `layout-canonical.md` seções 3, 4 e 11.

6. **Logo ibmec e selo "ibmec.br"** já estão dentro das imagens de fundo.
   Não adicionar outro logo. Não cobrir os cantos onde eles aparecem.

## Paleta (usar EXCLUSIVAMENTE estas cores + neutros)

| Uso | Hex |
|-----|-----|
| Primária / títulos / textos fortes | `#1B2A4A` (navy ibmec) |
| Acento / destaque / números grandes / ícones | `#E8A317` (amarelo/laranja ibmec) |
| Texto secundário / legendas | `#666666` |
| Texto corrido | `#333333` ou `#1B2A4A` |
| Fundos de cards, blocos suaves | `#F4F4F4` ou `#FFF7E6` (pastel do amarelo) |
| Branco | `#FFFFFF` |

**Regra 60/30/10:** navy domina, cinza/branco apoia, amarelo é acento
pontual. **Nunca** preencher mais de ~15% do slide com amarelo sólido.

## Tipografia

| Elemento | Fonte | Peso | Tamanho | Cor |
|----------|-------|------|---------|-----|
| Títulos H1 | Arial Black | bold | 24pt (Aula 1) ou 32–40pt | navy `#1B2A4A` |
| Subtítulos / cabeçalhos de seção | Arial Black ou Arial Bold | bold | 20–24pt | navy ou amarelo |
| Corpo | Arial ou Calibri | regular | 14–18pt | `#333333` ou `#1B2A4A` |
| Legendas / rodapés / citações de fonte | Arial | regular | 10–12pt | cinza `#666666` |
| Destaques de citação/tema | Arial Italic | itálico | 14–18pt | cinza |

## Motivos visuais permitidos (carry-over do layout)

- **Faixa horizontal amarela `#E8A317` (regra 11 — inegociável)**:
  altura **fixa** `54900` EMU, posição **fixa** `y=905100`,
  `x≈750005`/`750006`. A largura `cx` **varia** conforme a largura do
  H1 (intervalo observado no gold standard: `1500000` a `1808100` EMU).
  Aparece **sob o H1** em **todos** os slides de **conteúdo** e
  estruturais (Agenda, Objetivos, Conexão, Síntese, Ponte,
  Referências, Atividade Prática, slides de correção, conceitos,
  etc.). Também aparece nas **capas** e **transições de tópico** (com
  geometria própria; ver `layout-canonical.md` §§3 e 4). Só pode ser
  omitida em diagramas full-bleed sem H1 (raríssimos).
- Números grandes em amarelo com rótulo pequeno em cinza abaixo
  (stat callouts).
- Ícones simples (formas geométricas, não emojis) em círculos navy ou
  amarelos.
- Cards com borda fina navy ou fundo `#F4F4F4`.
- **Cards brancos com borda navy (regra 10):** `roundRect` fill
  `#FFFFFF` + `<a:ln w="12700">` solid `#1B2A4A`. Padrão obrigatório
  para qualquer card com fundo branco. Slide-fonte canônico:
  `aula1_bloco1/slide16.xml` (4 cards 2×2 com selo numerado amarelo).
- **Caixas de definição navy com texto branco (regra 10):** `rect` ou
  `roundRect` fundo `#1B2A4A` + texto `#FFFFFF` Arial Black centralizado.
  Use sempre que houver definição, conceito-chave ou texto em destaque.
- Setas, timelines e fluxos em navy com nós amarelos.

### Combinações de cor proibidas (regra 10)

| Combinação | Permitida? | Alternativa |
|---|---|---|
| Texto amarelo `#E8A317` sobre fundo navy `#1B2A4A` | ❌ NÃO | Usar texto branco `#FFFFFF` |
| Texto navy `#1B2A4A` sobre fundo amarelo `#E8A317` | ❌ NÃO | Usar texto branco `#FFFFFF` |
| Texto branco sobre fundo branco | ❌ NÃO (invisível) | Mudar fundo |
| Texto cinza claro sobre fundo cinza | ❌ NÃO (contraste ruim) | Usar `#333333` ou `#1B2A4A` |
| Texto navy sobre fundo branco | ✅ Sim | — |
| Texto amarelo sobre fundo branco | ✅ Sim (subtítulos curtos) | Negrito recomendado |
| Texto branco sobre fundo navy | ✅ Sim | — |
| Texto branco sobre fundo amarelo | ✅ Sim (com bold/Arial Black) | — |

#### Aplicações canônicas dessas regras (gold standard Aula 1)

| Local | Forma | Cor de fundo | Cor do texto |
|---|---|---|---|
| Selo numerado da agenda (slide 3) | `ellipse` | navy `#1B2A4A` | **branco `#FFFFFF`** (não amarelo!) |
| Selo numerado da síntese (slide 46) | `ellipse` | amarelo `#E8A317` | **branco `#FFFFFF`** |
| Selo numerado em cards 2×2 (slides 16, 36) | `ellipse` | amarelo `#E8A317` | **branco `#FFFFFF`** |
| Cabeçalho de coluna em comparação navy | `rect` | navy `#1B2A4A` | **branco `#FFFFFF`** |
| Cabeçalho de coluna em comparação amarela | `rect` | amarelo `#E8A317` | **branco `#FFFFFF`** (não navy!) |
| Tag em caps "HOJE" / "AULAS X-Y" sobre card pastel | `rect` ou texto livre | pastel `#FCE5CD` | amarelo `#E8A317` (sobre pastel funciona) |

> **Erro comum corrigido em 2026-05-04:** o número dentro da elipse navy
> da agenda estava em **amarelo** em decks gerados por scripts. O gold
> standard usa **branco** (`schemeClr lt1` no XML). Sempre use branco.

**Hierarquia canônica de cores (regra 10):** títulos sempre em **navy
ibmec `#1B2A4A`**; subtítulos amarelos sempre em **amarelo ibmec
`#E8A317`** sobre fundo branco.

### Bullets estilizados (regra 10)

Sempre que listar itens, use **círculos amarelos `#E8A317` ou navy
`#1B2A4A`** como marcadores visuais (em vez de bullet padrão `•`).
Tamanhos canônicos do gold standard:

| Local | Forma | Cor | Dimensões |
|---|---|---|---|
| Objetivos | `ellipse` | `#E8A317` | `160000×160000` |
| Ponte | `ellipse` | `#E8A317` | `217800×180000` |
| Agenda B1 (selo numerado) | `ellipse` | `#1B2A4A` | `473100×420000` |
| Agenda B2 (selo numerado) | `ellipse` | `#1B2A4A` | `505200×420000` |
| Síntese (selo numerado) | `ellipse` | `#E8A317` | `600900×500100` |
| Cards 2×2 (slide 16/36) | `ellipse` | `#E8A317` | `553500×459900` a `602700×500100` |

### Design "estiloso" da Aula 1 — replicável em conteúdo

A Aula 1 publicada usa, **dentro da paleta e tipografia canônicas**,
composições mais elaboradas (Venn de 3 círculos com sobreposição,
cards 2×2 com selo numerado, comparação em 2 cards de cores diferentes,
tabela com coluna semântica e caixa de insight pastel, etc.). **Esse
tipo de design pode e deve ser replicado em slides de conteúdo de
qualquer aula** sempre que ajudar a explicação, **desde que** o
cabeçalho padrão (H1 + faixa amarela), a paleta acima e os limites de
área útil sejam respeitados.

Catálogo com slide-fonte de cada padrão e princípios de uso:
[`layout-canonical.md` §14a](layout-canonical.md).

## O que NUNCA fazer

- Barras coloridas de cabeçalho/rodapé sobrepostas ao fundo.
- Retângulos coloridos full-width decorativos.
- Fundo bege/creme.
- Omitir a **faixa amarela canônica** sob o H1 em slides de conteúdo
  que seguem o cabeçalho padrão da Aula 1 (regra 11; exceto diagramas
  full-bleed sem título).
- Bullets `•` literais — use `<a:buChar char="•"/>` ou `<a:buAutoNum>`.
- Texto navy pequeno sobre a faixa amarela (a faixa NÃO é lugar para texto).
- **Texto amarelo sobre fundo navy** (use branco — regra 10).
- **Texto navy sobre fundo amarelo** (use branco — regra 10).
- Cards com fundo branco **sem borda navy** (regra 10).
- Slides só de texto: todo slide deve ter **algum elemento visual**
  (ícone, forma, número grande, card, chart, diagrama, tabela, imagem).
- Sobreposição de elementos ou texto cortado (regra 12). Espaço mínimo
  entre formas adjacentes: `60000` EMU.

## Conversão rápida de unidades

- 1 polegada = 914400 EMU
- 1 cm = 360000 EMU
- 1 pt (tamanho de fonte) ≠ EMU; em XML de fonte usa-se centésimos de pt
  (`sz="2400"` = 24pt).

Slide 16:9 padrão = 9144000 × 5143500 EMU = 25.4 cm × 14.29 cm.

## Layouts padronizados entre aulas (obrigatório)

Os **tipos de slide** (capa, agenda, objetivos, transição, atividade,
exercício dirigido, síntese, referências, encerramento) e a **pilha
tipográfica** da Aula 1 são **norma** para todas as aulas. Leia e siga:

- [`layout-canonical.md`](layout-canonical.md) — catálogo com referência aos
  `slideN.xml` da Aula 1 e checklist.
