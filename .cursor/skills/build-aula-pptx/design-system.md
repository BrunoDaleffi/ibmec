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
     referências, atividade prática, slides de correção e todo slide de
     conteúdo regular.

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

- **Faixa horizontal amarela `#E8A317`** (~**54900** a **55000** EMU de altura,
  largura inicial ~**1 500 000** EMU, `x ≈ 750005`): aparece **sob o H1** em
  quase todos os slides de **conteúdo** da Aula 1 (Agenda, Objetivos,
  conceitos, Atividade Prática, etc.). **É obrigatória** no cabeçalho padrão
  de conteúdo. Também aparece nas **capas** e **transições de tópico** (com
  geometria própria; ver `layout-canonical.md`).
- Números grandes em amarelo com rótulo pequeno em cinza abaixo
  (stat callouts).
- Ícones simples (formas geométricas, não emojis) em círculos navy ou
  amarelos.
- Cards com borda fina navy ou fundo `#F4F4F4`.
- Setas, timelines e fluxos em navy com nós amarelos.

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
- Omitir a **faixa amarela canônica** sob o H1 em slides de conteúdo que
  seguem o cabeçalho padrão da Aula 1 (exceto diagramas full-bleed sem título).
- Bullets `•` literais — use `<a:buChar char="•"/>` ou `<a:buAutoNum>`.
- Texto navy pequeno sobre a faixa amarela (a faixa NÃO é lugar para texto).
- Slides só de texto: todo slide deve ter **algum elemento visual**
  (ícone, forma, número grande, card, chart, diagrama).

## Conversão rápida de unidades

- 1 polegada = 914400 EMU
- 1 cm = 360000 EMU
- 1 pt (tamanho de fonte) ≠ EMU; em XML de fonte usa-se centésimos de pt
  (`sz="2400"` = 24pt).

Slide 16:9 padrão = 9144000 × 5143500 EMU = 25.4 cm × 14.29 cm.

## Layouts padronizados entre aulas (obrigatório)

Os **tipos de slide** (capa, agenda, objetivos, transição, correção,
atividade, síntese, referências, encerramento) e a **pilha tipográfica** da
Aula 1 são **norma** para todas as aulas. Leia e siga:

- [`layout-canonical.md`](layout-canonical.md) — catálogo com referência aos
  `slideN.xml` da Aula 1 e checklist.
