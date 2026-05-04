# Layouts canônicos (referência obrigatória)

A **Aula 1** (Bloco 1 e Bloco 2) é a **fonte de verdade visual** da
disciplina (padrão ouro, edição mais recente). Todo deck de qualquer
aula deve **replicar literalmente** geometria (EMU), tipografia
(`sz`/fonte), cores (`srgbClr`) e ordem das formas dos slides
equivalentes da Aula 1.

Arquivos de referência:

- `aulas/aula_01/slides/aula1_bloco1_jurimetria.pptx`
- `aulas/aula_01/slides/aula1_bloco2_jurimetria.pptx`

**Antes de autorar slides novos:** desempacote o `.pptx` correspondente
da Aula 1 e copie do XML do slide-fonte indicado na tabela de cada
seção. Não re-derive medidas; copie. Todas as medidas das seções
abaixo foram extraídas diretamente do XML do gold standard.

---

## 0. Área útil obrigatória (regra absoluta)

Toda forma (`<p:sp>`, `<p:pic>`, `<p:graphicFrame>`, `<p:cxnSp>`) precisa
caber dentro da **área útil canônica do tipo do slide**, medida em EMU.
As caixas abaixo foram extraídas medindo a moldura branca do template
(`docs/templates/layout.pptx`, ambos os PNGs de fundo) e os 49+42 slides
da Aula 1 publicada. Slide 16:9 = `9144000 × 5143500` EMU.

A regra opera em **duas camadas**:

- **Hard limit (obrigatório):** delimita a moldura branca do template.
  Qualquer shape com `(x, y, x+cx, y+cy)` fora desta caixa **invade a
  moldura cinza ou a faixa amarela direita do template** e o slide está
  em violação. Sem exceções.
- **Soft limit (recomendado):** zona em que a Aula 1 mantém ~95% do
  conteúdo. Use sempre que possível; saídas só são aceitáveis para
  diagramas/imagens full-bleed (ver Aula 1 B1 slide 22).

> **Regra de ouro.** Para qualquer shape `S` em um slide do tipo `T`:
> `S.x ≥ x_min_hard(T)`, `S.y ≥ y_min_hard(T)`,
> `S.x + S.cx ≤ x_max_hard(T)`, `S.y + S.cy ≤ y_max_hard(T)`.
> Se extrapolar o hard limit, o slide está em violação — encurte texto,
> reduza `cx/cy` ou recoloque, **não** empurre o limite.

### 0.1 Slides padrão (estruturais) e slides de conteúdo

Aplica-se a: agenda, objetivos, conexão, síntese, ponte, referências,
atividade prática **e** a todo slide de conteúdo com cabeçalho padrão.
Fundo: `image2.png`. Cabeçalho padrão (seção 2) é obrigatório quando
houver H1 textual.

| Camada | x_min | y_min | x_max | y_max | Largura | Altura |
|---|---|---|---|---|---|---|
| **Hard limit (não passar)** | `400000` | `400000` | `7970000` | `4685000` | 7570000 | 4285000 |
| **Soft limit (recomendado)** | `750000` | `500000` | `7700000` | `4650000` | 6950000 | 4150000 |

> **Importante (correção 2026-05-04):** todo conteúdo de slide
> estrutural (H1, subtítulo amarelo, cards, caixas navy de definição,
> tabelas, listas) deve **preencher a largura útil** `cx ≈ 6700800` a
> `6950000` EMU (do `x=750000` ao `x=7450800`–`7700000`), **não**
> ficar estreito em `cx=5950000`. O gold standard B1 slide 3 usa
> `H1.cx=6700800` como padrão; itens da agenda chegam até `x=7929372`
> (que entra em soft warning mas é tolerado por ser réplica do gold).
> Estreitar caixas para `cx=5950000` deixa o conteúdo "espremido à
> esquerda" e quebra a paridade visual com a Aula 1.

Subzonas internas (top-down) — usar dentro do soft limit:

| Subzona | y_min | y_max | Uso |
|---|---|---|---|
| Cabeçalho (H1 + faixa amarela + subtítulo amarelo opcional) | `500000` | `1700000` | Conteúdo do tipo "título" — ver seção 2. |
| Corpo | `1700000` | `4300000` | Cards, listas, diagramas, comparações. |
| Citação de rodapé | `4350000` | `4650000` | `Autor (ano)` em Arial Italic, ver seção 15. |

> Para diagramas full-bleed sem H1 (raríssimos, ver Aula 1 B1 slide 22),
> shapes podem chegar até o **hard limit**. Slides com H1 textual sempre
> respeitam o soft limit.

### 0.2 Slides especiais (capa, transição, encerramento)

Cada um tem geometria própria — duplicam de `slide2.xml` do template
(fundo `image1.png`). Os limites abaixo são obrigatórios:

| Tipo | Camada | x_min | y_min | x_max | y_max |
|---|---|---|---|---|---|
| **Capa do bloco** | hard | `400000` | `400000` | `7970000` | `4685000` |
| Capa do bloco | soft (Aula 1) | `1097275` | `914400` | `7887775` | `3900000` |
| **Transição de tópico (01, 02, …)** | hard | `400000` | `400000` | `7970000` | `4685000` |
| Transição | soft (Aula 1) | `1097275` | `900000` | `7600000` | `3905000` |
| **Encerramento ("Fim do Bloco N"/"Aula N")** | hard | `400000` | `400000` | `7970000` | `4685000` |
| Encerramento | soft (Aula 1) | `820000` | `914400` | `7745000` | `3300000` |

Capa, transição e encerramento usam o **mesmo hard limit** dos demais
(é a mesma moldura branca). O soft limit é mais apertado por **design**:
o eixo de texto fica deslocado à direita (alinhado a `x≈1097275` em
capa/transição, `x≈822950` em encerramento) para criar a respiração
canônica desses slides especiais.

### 0.3 Validação automática (obrigatória)

Antes de empacotar, rode o validador de área útil:

```bash
uv run python .cursor/skills/build-aula-pptx/scripts/check_useful_area.py \
  /tmp/deck_aulaX_blocoY/
```

O script falha (exit 1) se algum shape ultrapassa o **hard limit**.
Soft-limit é apenas avisado (warning prefixado por `[soft]`). O deck só
deve ser empacotado quando o validador retornar zero erros hard.

### 0.4 Espaçamento mínimo entre formas (regra 12)

Para garantir que **não haja sobreposição** nem aglomeração de texto,
todo par de formas adjacentes (cards, caixas de texto, ícones, números)
deve ter um respiro de **no mínimo `60000` EMU** (≈ 0,17 cm) entre as
bordas. Em pares de cards lado a lado da Aula 1, o gap medido é:

| Par de formas | Gap horizontal (EMU) |
|---|---|
| Cards conexão (FCE5CD) — Aula 1 B1 slide 5 | `~178000` (entre `750000+2255100=3005100` e `3183033`) |
| Cards 2×2 com selo (slide 16) | `180834` (entre `750000+3435300=4185300` e `4366134`) |
| Cards atividade (slide 38 B2) — não há (1 card único) | — |

| Par de formas | Gap vertical (EMU) |
|---|---|
| Faixa amarela canônica (`y=905100`, `cy=54900`) → Subtítulo amarelo (`y=1330000`) | `370000` |
| Subtítulo amarelo → Início do corpo (`y=1700000`) | `~370000` (`y=1700000` − fim do subtítulo) |
| Linhas da agenda 2×4 | `600000` (item para item, `1700000`, `2300000`, `2900000`, `3500000`) |
| Linhas da síntese | `570000` (`1750000`, `2320000`, `2890000`, `3460000`, `4030000`) |

Gaps menores que `60000` em qualquer direção são **proibidos** (pode
gerar texto com aparência colada). Gaps maiores que os medidos da Aula
1 também são desencorajados (rompem o ritmo visual canônico).

A inspeção JPEG (item 9 da `pptx-qa`) é onde a sobreposição de **texto
sobre texto** (causada por fonte que não cabe na caixa, ou por texto
mais longo do que o esperado) é detectada. Quando aparecer, encurte o
texto ou reduza a fonte um ponto, **não** aumente a caixa para fora do
soft limit.

---

## 1. Regra de fundos (image1.png × image2.png)

A Aula 1 (gold standard) fixa o seguinte uso (regras 4 e 5 da
disciplina). **As referências `image1.png` e `image2.png` aqui se
referem aos nomes finais no `.pptx` empacotado**, após o swap
idempotente do build script:

| Tipo de slide | Fundo (no `.pptx` final) | Razão |
|---|---|---|
| Capa do bloco | `image1.png` | Fundo "forte": faixa amarela cheia + logo no amarelo. |
| Transição de tópico (01, 02, 03…) | `image1.png` | Mesmo fundo "forte" para abrir cada seção. |
| Encerramento ("Fim do Bloco N", "Fim da Aula N") | `image1.png` | Fechamento alinhado à abertura. |
| Agenda do bloco | `image2.png` | Fundo "suave": logo no branco. |
| Objetivos de aprendizagem | `image2.png` | Idem. |
| Conexão / "Voltando do intervalo" | `image2.png` | Idem. |
| Síntese, Ponte, Referências | `image2.png` | Idem. |
| Atividade Prática | `image2.png` | Idem. |
| Slides de correção da atividade (Q1, Q2, Q3) | `image2.png` | Idem. |
| Demais slides de **conteúdo** (conceito, stat, tabela, comparação, etc.) | `image2.png` | Idem. |

### Equivalência template ↔ `.pptx` final

O `docs/templates/layout.pptx` (não-swapped) tem os PNGs **com nomes
trocados** em relação à convenção visual da disciplina. A
correspondência é:

| Conteúdo visual | Nome no `layout.pptx` | Nome no `.pptx` final (após swap) |
|---|---|---|
| Fundo "forte" (capa/transição/fim) | `image2.png` | `image1.png` |
| Fundo "suave" (conteúdo) | `image1.png` | `image2.png` |

> **Quando o usuário pedir "use o image2.png do `layout.pptx` para
> capa"**, está se referindo ao **conteúdo visual do PNG físico no
> template** (o "forte"). Esse mesmo conteúdo, depois do swap
> idempotente, fica salvo como `image1.png` no `.pptx` final. **Os
> `.rels` finais sempre referenciam pelos nomes finais** (`image1.png`
> para capa/transição/fim, `image2.png` para o resto).

A regra técnica continua: **não altere o bloco `<p:bg>...</p:bg>`** dos
slides; mude apenas o `Target` do `rId3` em `slideN.xml.rels` quando
precisar trocar o fundo de uma cópia.

### 1.1 Bug do template e protocolo obrigatório de build

O `docs/templates/layout.pptx` foi exportado com os PNGs físicos
**trocados** em relação à convenção canônica acima:

| Arquivo no template | Conteúdo visual real |
|---|---|
| `layout.pptx::ppt/media/image1.png` | fundo "suave" (deveria ser image2) |
| `layout.pptx::ppt/media/image2.png` | fundo "forte" (deveria ser image1) |

Por isso, **todo build script de aula nova precisa, no `main()`**:

1. **Unpack fresco do template**, sempre com `--force` (apaga
   `/tmp/deck_aulaX_blocoY/` antes). Isso garante que a função de swap
   parte de um estado conhecido. Esquecer essa etapa foi causa de
   double-swap em build anterior (incidente 2026-05-02).
2. **Rodar `swap_media_para_aula1()` idempotente**: troca
   `image1.png` ↔ `image2.png` apenas se `md5(image1.png) !=
   b0987cbbb2c05a7cebbd3bac3576c0bb` (md5 canônico da Aula 1
   publicada). Se já estiver no estado canônico, a função retorna sem
   tocar nos arquivos. Idempotência elimina o double-swap mesmo se a
   função for chamada múltiplas vezes.
3. **Os `.rels` dos slides devem apontar diretamente** para
   `image1.png` (capa, transição, fim) ou `image2.png` (todo o resto).
   Não inverta os nomes nos `.rels` — a função de swap já cuida do
   mapeamento físico.

Implementação de referência (copie em todo build novo):

```python
CANONICAL_IMAGE1_MD5 = "b0987cbbb2c05a7cebbd3bac3576c0bb"

def unpack_layout_fresh() -> None:
    import shutil, subprocess
    if DECK.exists():
        shutil.rmtree(DECK)
    layout = Path("docs/templates/layout.pptx").resolve()
    subprocess.run(
        [
            "uv", "run", "python",
            ".cursor/skills/build-aula-pptx/scripts/unpack_pptx.py",
            "--force",
            str(layout),
            str(DECK),
        ],
        check=True,
    )

def swap_media_para_aula1() -> None:
    import hashlib
    media = DECK / "ppt/media"
    img1 = media / "image1.png"
    img2 = media / "image2.png"
    if not (img1.is_file() and img2.is_file()):
        return
    if hashlib.md5(img1.read_bytes()).hexdigest() == CANONICAL_IMAGE1_MD5:
        return  # já está canônico, idempotente
    tmp = media / ".swap.png"
    img1.rename(tmp)
    img2.rename(img1)
    tmp.rename(img2)

def main() -> None:
    unpack_layout_fresh()    # sempre primeiro
    swap_media_para_aula1()  # idempotente
    # ... gerar slides ...
```

**Verificação obrigatória após empacotar:** `md5sum
ppt/media/image1.png` no `.pptx` final deve bater com
`b0987cbbb2c05a7cebbd3bac3576c0bb`. Se não bater, o swap foi pulado ou
duplicado e o deck está com fundos invertidos — **não entregar**.

---

## 2. Cabeçalho padrão dos slides estruturais

Replicado **idêntico** em **Agenda, Objetivos, Conexão, Síntese, Ponte
para o próximo bloco/aula, Referências do bloco, Atividade Prática e
todo slide de conteúdo com H1**. Coordenadas extraídas de `aula1_bloco1`
slides 3, 4, 5, 46, 47 e 48.

| Camada | off x | off y | cx | cy | sz | Fonte | Cor | Texto |
|---|---|---|---|---|---|---|---|---|
| **H1** | `750000` | `500000` | **`6700800`** (canônico) ou até `7172100` | `900000` | `2400` (caso bem largo: `2200` ou `2000`) | Arial Black | `#1B2A4A` | Título do slide |
| **Faixa amarela** (regra 11) | `750005`–`750006` | `905100` | `1500000`–`1808100` (varia com largura do H1) | `54900` (fixo) | — | — | `#E8A317` | (vazio) |
| **Subtítulo amarelo** (opcional) | `750000` | `1330000` | mesma largura do H1 (canônico `6700800`) | `399900`–`400000` | `1400` | Arial regular | `#E8A317` | Frase curta de apoio |
| **Início do corpo** | `750000` | `~1500000`–`1780000` | livre, **alvo `6950000`** (até `x=7700000`) | livre | `1200`–`1400` | Arial | `#333333` | Conteúdo |

> **Largura do H1 e da faixa amarela.** Os slides estruturais da Aula 1
> ajustam a `cx` do H1 para acomodar o título inteiro em uma única
> linha, dentro do soft limit. Valores observados na Aula 1 B1: agenda
> `cx=6700800`, objetivos `cx=5950000`, conexão `cx=6201900`, síntese
> `cx=7150200`, ponte `cx=7135500`, referências `cx=7143000`,
> atividade prática `cx=6960600`. **A faixa amarela acompanha** com
> `cx` proporcional (entre `1500000` e `1808100`), sempre alinhada a
> `x=750005`/`750006` e altura fixa `54900`. Só o **comprimento da
> faixa varia** — `y` e `cy` são fixos.

A faixa amarela sob o H1 é **inegociável** em qualquer slide com título
textual (regra 11). Só pode ser omitida em diagramas full-bleed sem H1
(raro).

### Subtítulos amarelos canônicos (frases-fórmula)

Use exatamente esta redação por tipo de slide:

| Slide | Subtítulo amarelo |
|---|---|
| Agenda | `O que vamos percorrer nas próximas 1h50min` |
| Objetivos | `Ao final deste bloco, você será capaz de` |
| Síntese | `N pontos para levar para casa` (N = qtd de itens) |
| Ponte (Bloco 1 → Bloco 2 da mesma aula) | `O que vem a seguir, depois do intervalo` |
| Ponte (Bloco 2 → próxima aula) | `O que vem na semana que vem` |
| Referências | `Fontes citadas ao longo do conteúdo` |
| Conexão (B1) | `Como este bloco se conecta ao que vocês vão apresentar na Aula 6` (ou variante coerente com o tema) |
| Conexão / "Voltando do intervalo" (B2) | `Onde paramos no Bloco 1` |
| Atividade Prática | `Entrega até a Aula N+1` |

---

## 3. Capa do bloco

Slide-fonte: `aula1_bloco1/slide1.xml`, `aula1_bloco2/slide1.xml`.

Geometria diferente do cabeçalho estrutural — eixo horizontal alinhado a
`x=1097275` (área branca da capa, mais à direita).

| Camada | off x | off y | cx | cy | sz | Fonte | Cor | Texto |
|---|---|---|---|---|---|---|---|---|
| Título da disciplina (caixa alta) | `1097275` | `914400` | `6790500` | `1828800` | **`3200`** | Arial Black | `#1B2A4A` | `JURIMETRIA E ANÁLISE DE DADOS PARA DECISÕES ESTRATÉGICAS` |
| Faixa amarela horizontal | `1097280` | `2788920` | `1828800` | `54864` | — | — | `#E8A317` | (vazio) |
| Linha "Aula X – Bloco Y" | `1097280` | `2926080` | `5486400` | `457200` | `2000` | Arial | `#E8A317` | `Aula X – Bloco Y` |
| Subtítulo do bloco (cinza) | `1097280` | `3337560` | `5486400` | `365760`–`550000` | `1400` | Arial | `#666666` | Frase do tema, máx. 2 linhas |

**Fundo:** `image1.png` (após swap; corresponde ao `image2.png` do
`layout.pptx` original).

> **Por que `sz=3200` e não `sz=3600`?** O XML do gold standard (Aula 1
> B1/B2 slide 1) está com `sz=3600`. Em renderizadores que carregam a
> Arial Black real (PowerPoint, LibreOffice GUI, Keynote), `sz=3600`
> faz o título de 53 caracteres quebrar em **4 linhas** e a 4ª linha
> (`ESTRATÉGICAS`) sobrepõe a faixa amarela e a linha `Aula X – Bloco
> Y` (regra 12 violada). O `soffice --headless` usado no QA local cai
> num fallback de fonte mais estreito e não detecta o estouro.
> `sz=3200` reduz o título 11% mas garante 3 linhas em qualquer
> renderizador. **Aula 1 publicada está marcada para retrabalho neste
> ponto** (mesma sobreposição). Incidente confirmado em PowerPoint em
> 2026-05-03.

---

## 4. Transição de tópico (01, 02, 03…)

Slide-fonte: `aula1_bloco1/slide6.xml` (transição "01 | A disciplina").
Mesma geometria nas demais transições da Aula 1 (slides 12, 17, 20, 26, 31, 34, 40 do B1; 5, 11, 17, 21, 26, 32, 36 do B2).

| Camada | off x | off y | cx | cy | sz | Fonte | Cor | Texto |
|---|---|---|---|---|---|---|---|---|
| Número grande | `1097275` | `900000` | **`1800000`** | `1100000` | **`9600`** (96pt) | Arial Black | `#E8A317` | `01`, `02`, … |
| Título do tópico | `1097275` | `2100000` | `6500000` | `1100000` | `3600` | Arial Black | `#1B2A4A` | Nome do tópico |
| Faixa amarela | `1097280` | `3250000` | `1500000` | `54864` | — | — | `#E8A317` | (vazio) |
| Subtítulo cinza | `1097280` | `3400000` | `5486400` | `500000` | `1400` | Arial | `#666666` | Frase de contexto |

**Fundo:** `image1.png` (após swap; corresponde ao `image2.png` do
`layout.pptx` original).

> **Tamanho `cx=1800000` é o canônico.** Confirmado no XML do gold
> standard (Aula 1 B1 slide 6, edição mais recente). Com 96pt, "01"
> ocupa ~1.7M EMU e cabe em `cx=1800000` na fonte real e nos
> renderizadores comuns. **Não aumente** para `cx=2400000`: a Aula 1
> (gold standard) usa `1800000`.

---

## 5. Agenda do bloco

Slide-fonte: `aula1_bloco1/slide3.xml` (B1, 8 itens) e
`aula1_bloco2/slide2.xml` (B2, 8 itens). Cabeçalho padrão (seção 2).

Corpo: **grade de 8 itens em 2 colunas × 4 linhas** (alvo da Aula 1).

Coordenadas dos itens (cada item é um par "elipse + título"):

| Linha | y elipse | y título |
|---|---|---|
| 1 | `1700000` (B1) / `1750000` (B2) | `1760000` (B1) / `1810000` (B2) |
| 2 | `2300000` / `2350000` | `2360000` / `2410000` |
| 3 | `2900000` / `2950000` | `2960000` / `3010000` |
| 4 | `3500000` / `3550000` | `3560000` / `3610000` |

Passo vertical fixo: `600000` EMU.

| Coluna | off x da elipse | off x do título |
|---|---|---|
| Esquerda | `750000`–`785321` | `1370945`–`1375529` |
| Direita | `4358824`–`4640749` | `4984353`–`5226372` |

Forma de cada item (medidas observadas no gold standard):

- **Elipse navy** (`prstGeom prst="ellipse"`, fill `#1B2A4A`):
  `cx=473100`–`505200`, `cy=420000`. Note que **é elíptica, não
  circular** (a Aula 1 usa proporção ligeiramente alongada). Dentro:
  número `sz=1600`, Arial Black, **cor `#FFFFFF` (branco — `schemeClr
  lt1` no XML do gold standard)**, alinhado ao centro. **Regra 10:
  fundo navy = texto branco, nunca amarelo.** Erro comum: usar
  `#E8A317` na numeração — viola a regra de combinação de cores.
- **Título do item**: caixa de texto `cx=2703000`–`2887200`,
  `cy=399900`, `sz=1200`, Arial, cor `#1B2A4A`, alinhado à esquerda,
  ancorado ao centro vertical.

> **Por que 8 itens?** Os blocos do gold standard listam todos os
> tópicos do plano (até 8). Se o bloco real tiver menos tópicos
> agrupáveis, **mantenha** a grade 2×4 e o passo vertical, preenchendo
> só as linhas necessárias começando em `y=1700000`. Não comprima nem
> centralize verticalmente.

---

## 6. Objetivos de aprendizagem

Slide-fonte: `aula1_bloco1/slide4.xml`. Cabeçalho padrão.

Corpo: **lista vertical de 3 a 5 itens** em verbos de ação.

| Camada por item | off x | off y | cx | cy | sz | Fonte | Cor |
|---|---|---|---|---|---|---|---|
| Círculo amarelo (`prstGeom prst="ellipse"`) | `790000` | `y_item` (ver abaixo) | `160000` | `160000` | — | — | `#E8A317` |
| Verbo de ação (Compreender, Identificar…) | `1060000` | `y_item - 30000` | `1800000` | `300000` | `1500` | Arial Black | `#1B2A4A` |
| Texto descritivo | `~2050000`–`~2570000` (varia conforme largura do verbo) | `y_item - 30000` | restante até `~7600000` | `500100` | `1300` | Arial | `#333333` |

`y_item` por linha (5 itens):

```
1750000, 2270000, 2790000, 3310000, 3830000
```

Passo vertical fixo de `520000` EMU.

---

## 7. Conexão / "Voltando do intervalo"

Slides-fonte: `aula1_bloco1/slide5.xml` ("Do Conceito ao Trabalho Final"),
`aula1_bloco2/slide4.xml` ("Voltando do intervalo").

Cabeçalho padrão + linha de texto introdutório navy:

| Camada | off x | off y | cx | cy | sz | Fonte | Cor |
|---|---|---|---|---|---|---|---|
| Texto introdutório | `750000` | `1730000` | `5950000` | `340000` | `1400` | Arial | `#333333` |

Corpo (B1, slide 5): **3 cards pastel `#FCE5CD`** (`roundRect`,
`adj≈6500`) lado a lado.

| Card | off x | cx | cy | y |
|---|---|---|---|---|
| Esquerda | `750000` | `2255100` | `2000100` | `2150000` |
| Centro | `3183033` | `2255100` | `2000100` | `2150000` |
| Direita | `5616064` | `2255100` | `2000100` | `2150000` |

Gap horizontal entre cards: `~178000` EMU.

Dentro de cada card (off x interno = card_x + 178027):

- **Tag amarela em caps** (HOJE / AULAS X-Y / AULA Z): `y=2300000`, `cx=1899000`, `cy=300000`, `sz=1200`, Arial Black, `#E8A317`.
- **Título do card** (Fundamentos / Método e aceleração / Apresentação): `y=2630000`, `cy=500100`, `sz=1400`, Arial Black, `#1B2A4A`.
- **Descrição**: `y=3200000`, `cy=900000`, `sz=1200`, Arial, `#333333`.

Corpo (B2, slide 4 — "Voltando do intervalo"): **3 cards
alternados `#F4F4F4` / `#FFF7E6` / `#F4F4F4`**, mesma geometria base
mas `cy=1850100` a `y=2400000`. Tag amarela em caps (`Bloco 1` / `Bloco
2` / `Aula 2`), título em maiúsculas navy (`FUNDAMENTOS`), descrição
cinza. Ver `aula1_bloco2/slide4.xml`.

> Sempre que houver 2 ou 3 colunas equivalentes a comparar, prefira
> reutilizar a geometria desses cards.

---

## 8. Síntese do bloco

Slide-fonte: `aula1_bloco1/slide46.xml`. Cabeçalho padrão.

Corpo: **5 itens verticais** com selo numerado amarelo (**elipse**, não
quadrado) + texto.

| Camada por item | off x | cx | cy | sz | Fonte | Cor |
|---|---|---|---|---|---|---|
| **Elipse** amarela (`prstGeom prst="ellipse"`) | `750000` | `600900` | `500100` | — | — | `#E8A317` |
| Número branco dentro da elipse | (mesma caixa) | (mesma) | (mesma) | `2000` | Arial Black | `#FFFFFF` |
| Texto descritivo | `1471034` | `6369000` | `450000` | `1250` | Arial | `#333333` |

`y_item` por linha (5 itens):

```
1750000, 2320000, 2890000, 3460000, 4030000
```

Passo vertical de `570000` EMU.

> **Atenção:** o gold standard usa **elipse** (não quadrado/rect) como
> selo. Versões anteriores deste arquivo descreviam um `rect` 500×500.
> Substitua para `ellipse` 600900×500100.

> Se o bloco gerar 3 ou 4 pontos-chave em vez de 5, mantenha o mesmo
> passo e termine em y mais alto. Não comprima para encher 5.

---

## 9. Ponte para o próximo bloco/aula

Slide-fonte: `aula1_bloco1/slide47.xml`. Cabeçalho padrão.

Corpo: **hero esquerda** (seta gigante) + **lista de 4 itens**.

Hero (esquerda):

| Camada | off x | off y | cx | cy | sz | Fonte | Cor |
|---|---|---|---|---|---|---|---|
| Seta `➜` | `750000` | `1585100` | `1652100` | `594900` | `6000` | Arial Black | `#E8A317` |
| Título de destaque | `2346910` | `1780000` | `4956000` | `399900` | `2000` | Arial Black | `#1B2A4A` |
| Descrição cinza | `2346910` | `2100000` | `4956000` | `399900` | `1250` | Arial | `#666666` |

Lista de 4 itens (passo vertical `430000` a partir de `y=2600000`):

| Camada por item | off x | cx | cy | sz | Fonte | Cor |
|---|---|---|---|---|---|---|
| Bullet amarelo (`prstGeom prst="ellipse"`) | `794053` | `217800` | `180000` | — | — | `#E8A317` |
| Título do item | `1108694` | `2904600` | `300000` | `1250` | Arial | `#1B2A4A` |
| Descrição do item | `4134087` | `3751500` | `300000` | `1150` | Arial | `#333333` |

`y` por item: `2600000`, `3030000`, `3460000`, `3890000` (bullet a `+50000` y).

---

## 10. Referências do bloco

Slide-fonte: `aula1_bloco1/slide48.xml`. Cabeçalho padrão.

Corpo:

| Camada | off x | off y | cx | cy | sz | Fonte | Cor |
|---|---|---|---|---|---|---|---|
| Caixa única com referências em ABNT | `750000` | `1780000` | `7143000` | `2799900` | `1150` | Arial | `#333333` |
| Rodapé cinza explicativo | `750000` | `4300000` | `6049800` | `300000` | `1000` | Arial | `#666666` |

Cada referência ABNT em parágrafo separado. Rodapé padrão sugerido:
`Leituras complementares estarão indicadas ao longo dos próximos blocos.`

---

## 11. Encerramento — duas variantes fixas

### 11a. Fim do Bloco 1 ("Intervalo")

Slide-fonte: `aula1_bloco1/slide49.xml`. **Fundo:** `image1.png`.

| Camada | off x | off y | cx | cy | sz | Fonte | Cor |
|---|---|---|---|---|---|---|---|
| Título | `822960` | `914400` | `5486400` | `731400` | `3600` | Arial Black | `#1B2A4A` |
| Faixa amarela | `822960` | `1691640` | `1828800` | `54900` | — | — | `#E8A317` |
| Linha "Intervalo de 15 minutos" | `822960` | `2391995` | `5486400` | `457200` | `2000` | Arial | `#E8A317` |
| Subtítulo "No Bloco 2: …" | `822955` | `2849200` | `5486400` | `360000` | `1300` | Arial | `#666666` |

Fórmula textual:

```
Fim do Bloco 1
Intervalo de 15 minutos
No Bloco 2: <gancho do tema do Bloco 2>.
```

### 11b. Fim da Aula N (Bloco 2 — com lembrete da atividade)

Slide-fonte: `aula1_bloco2/slide42.xml`. **Fundo:** `image1.png`.

| Camada | off x | off y | cx | cy | sz | Fonte | Cor |
|---|---|---|---|---|---|---|---|
| Título "Fim da Aula N" | `822950` | `914400` | `5486400` | `702600` | `3600` | Arial Black | `#1B2A4A` |
| Faixa amarela | `822950` | `1661173` | `1828800` | `52800` | — | — | `#E8A317` |
| "Lembrete:" | `822950` | `1836884` | `5486400` | `351300` | `1600` | Arial | `#E8A317` |
| Linha de entrega "Entregar a Atividade N até a próxima aula." | `822950` | `2188307` | `5486400` | `351300` | `1400` | Arial | `#666666` |
| "Próxima aula: …" | `822950` | `2697950` | `6915900` | `351300` | `1500` | Arial | `#1B2A4A` |

Fórmula textual:

```
Fim da Aula N
Lembrete: Entregar a Atividade N até a próxima aula.
Próxima aula: <ementa em uma frase>.
```

> Em Aulas 5 e 6 (Bloco 2 sem atividade nova), trocar o bloco
> "Lembrete/Atividade" pela respectiva combinação ("Lembrete: prepare o
> trabalho final" na Aula 5 e "Encerramento da disciplina" na Aula 6).

---

## 12. Atividade Prática (apenas Bloco 2 das Aulas 1 a 4)

Slide-fonte: `aula1_bloco2/slide38.xml`. Cabeçalho padrão (H1 + faixa
amarela). Subtítulo amarelo "Entrega até a Aula N+1" — note que o
**subtítulo amarelo da atividade fica em `y=1102612`** (mais próximo do
H1 do que nos demais slides estruturais), porque o card navy começa
logo abaixo a `y=1522612`.

Corpo (medidas extraídas do gold standard `aula1_bloco2/slide38.xml`):

| Camada | off x | off y | cx | cy | sz | Fonte | Cor |
|---|---|---|---|---|---|---|---|
| H1 "Atividade Prática N" | `750000` | `500000` | `6960600` | `900000` | `2400` | Arial Black | `#1B2A4A` |
| Subtítulo amarelo "Entrega até a Aula N+1" | `750000` | `1102612` | `6960600` | `399900` | `1400` | Arial | `#E8A317` |
| Faixa amarela canônica | `750005` | `905100` | `1524600` | `54900` | — | — | `#E8A317` |
| Card navy alto (`roundRect`, `adj≈6500`, fill `#1B2A4A`) | `750000` | `1522612` | `6960600` | `800100` | — | — | `#1B2A4A` |
| Título da atividade dentro do card | `925479` | `1592612` | `6609600` | `660000` | `1700` | Arial Black | `#E8A317` |
| Caixa "Você deverá produzir" (texto navy bold sobre fundo do slide) | `750000` | `2472612` | `6960600` | `300000` | `1400` | Arial Black | `#1B2A4A` |
| Bloco com Pergunta 1./2./3. | `750000` | `2772600` | `7135800` | `1861200` | `1100` | Arial | `#E8A317` (numeração bold) / `#333333` (texto regular) |

Estrutura textual obrigatória (3 questões, sempre nesta forma):

```
Pergunta 1. <enunciado em até 2 linhas>
Pergunta 2. <enunciado em até 2 linhas>
Pergunta 3. <enunciado em até 2 linhas>
```

Speaker notes do slide devem trazer instrução de entrega, peso da
atividade na média (3,0 pts em 4 atividades) e critério de correção
por questão.

---

## 13. Slides de correção da atividade (apenas Bloco 1 das Aulas 2 a 5)

Estrutura **fixa de 5 a 6 slides** abrindo o Bloco 1 (antes do conteúdo
novo da aula). Cabeçalho padrão (seção 2) em todos eles.

| # | Tipo | Fundo | Título | Conteúdo |
|---|---|---|---|---|
| 1 | Transição "Atividade N: o que aprendemos" | `image1.png` | Padrão de transição (seção 4), sem número | Subtítulo: `Correção comentada das 3 questões e ponte para o método desta aula` |
| 2 | Recap | `image2.png` | `O que foi pedido na Atividade N` | Subtítulo amarelo `Atividade Prática N (Bloco 2 da Aula N) · 3 questões`. Lembrete das 3 questões na ordem original e do peso. |
| 3 | Correção Q1 | `image2.png` | `Atividade N · Questão 1` | Bloco superior: enunciado curto. Bloco inferior: 2–4 bullets (caminho de resposta, exemplo XY&A, armadilhas). |
| 4 | Correção Q2 | `image2.png` | `Atividade N · Questão 2` | Mesmo template. |
| 5 | Correção Q3 | `image2.png` | `Atividade N · Questão 3` | Mesmo template. |
| 6 | Insight / ponte | `image2.png` | Frase-síntese + gancho para o conteúdo novo | Conecta o que foi corrigido ao próximo tópico do Bloco 1. |

Os 3 slides de correção (Q1, Q2, Q3) **espelham a numeração e a ordem**
das 3 questões da Atividade Prática do Bloco 2 anterior.

---

## 14. Slides de conteúdo (conceito, stat, comparação, tabela, etc.)

**Sempre** usam o cabeçalho padrão da seção 2 quando há H1 textual.
Para os corpos específicos (stat callout, comparação 2 colunas, card,
tabela, citação), use os snippets em
[`slide-templates.md`](slide-templates.md).

### 14a. Design "estiloso" da Aula 1 — replicável em qualquer slide de conteúdo

A Aula 1 publicada usa, **dentro do cabeçalho padrão e da paleta
canônica**, composições mais elaboradas que misturam caixas, formas,
cores e geometria. **Esse tipo de design é permitido e encorajado em
qualquer slide de conteúdo** (Aulas 2 a 6) sempre que ajudar a
explicação. O cabeçalho padrão (H1 + faixa amarela + subtítulo
amarelo) e a paleta da seção 6.0 do `instrucao_geral.md` continuam
obrigatórios; o que varia é o **corpo** do slide.

Catálogo de padrões já validados na Aula 1 (com slide-fonte para copiar):

| Padrão | Slide-fonte | Composição |
|---|---|---|
| **Cards brancos com borda navy + selo numerado** ⭐ | `aula1_bloco1/slide16.xml` | 4 `roundRect` fill `#FFFFFF` + `<a:ln w="12700">` navy `#1B2A4A` + elipse amarela `602700×500100` com número branco `sz=2000` + título navy + descrição cinza. Grade 2 colunas × 2 linhas a `x=750000`/`4366134`, `y=1750000`/`3070000`, ext `3435300×1179900`. Padrão da regra 10 (cards com fundo branco devem ter borda navy). |
| **Card branco + barra navy de título** ⭐ (single column) | inspirado em `aula1_bloco1/slide43.xml` (comparação de 2 cards com headers coloridos) | 1 `roundRect` externo fill `#FFFFFF` + borda navy `w=12700` + barra interna no topo `rect`/`roundRect` fill `#1B2A4A` com texto **branco** Arial Black centralizado (regra 10) + parágrafos navy/cinza no corpo. Substitui o card cinza `#F4F4F4` para conceitos que precisam de mais destaque visual. Ideal para slides de mini-caso, exemplos práticos, exercícios dirigidos e síntese de etapa. |
| **Diagrama de Venn 3 círculos** | `aula1_bloco1/slide22.xml` | 3 elipses semitransparentes (navy, amarelo, azul claro) sobrepostas + rótulos brancos no centro de cada uma + card lateral cinza com legenda das interseções. Citação `Fonte: ABJ` em rodapé `sz=800` cinza `#999999`. |
| **Cards 2×2 com selo numerado** | `aula1_bloco1/slide36.xml` | 4 `roundRect` fill `#FFFFFF` com borda navy + elipse amarela `553500×459900` com número branco + título navy + descrição cinza `sz=1050`. Grade 2×2 a `x=750000`/`4358824`, `y=1750000`/`3030000`, ext `3428400×1179900`. |
| **Comparação 2 colunas com cards coloridos** | `aula1_bloco1/slide43.xml` | 2 `roundRect` lado a lado: esquerda fundo `#F4F4F4` (`x=750000`), direita fundo `#FFF7E6` (pastel amarelo, `x=4404092`), ambos `ext=3414600×2199900` a `y=1570575`. Tag em caps no topo (`NO DIREITO` navy / `NA JURIMETRIA` amarela), descrição cinza, frase de fechamento em italic navy a `y=4094375`. |
| **Tabela "manual" com cabeçalho navy + zebrado** | `aula1_bloco1/slide38.xml` | Linhas como pares de `rect`: cabeçalho `fill=#1B2A4A` com texto branco; linhas alternadas `fill=#FFFFFF` e `fill=#F4F4F4`. Última coluna pode ter cores semânticas (verde `#2D7D4F`, navy, amarelo). Geometria: 4 colunas a `x=750000`/`2784636`/`4460218`/`6135800`, alturas `360000` por linha, gap zero (linhas coladas para parecer tabela). |
| **Comparação 2 colunas (tabela nativa)** | `aula1_bloco1/slide29.xml` | Tabela `<a:tbl>` com primeira coluna em bold navy (rótulo da dimensão) e duas colunas de comparação. Cabeçalho navy. |
| **Quadro de stat secundário** | `aula1_bloco1/slide14.xml` (Panorama Financeiro) | 3 stat callouts pequenos lado a lado: número grande amarelo + label cinza, com leve `roundRect` de fundo. |
| **Caixa de definição navy com texto branco** | qualquer slide de definição (regra 10) | `rect` ou `roundRect` fill `#1B2A4A` (navy ibmec) + texto branco `#FFFFFF` `sz=1400` Arial Black centralizado. Usar para destacar definições e textos importantes. **Nunca** texto amarelo sobre navy — usar branco. |

Princípios para usar livremente:

- **Mantenha a paleta** (`#1B2A4A` navy, `#E8A317` amarelo, `#666666`/
  `#333333` cinza, `#F4F4F4` neutro, `#FCE5CD` pastel amarelo,
  `#FFFFFF` branco). Nunca introduzir cor nova.
- **Mantenha a tipografia** da seção 6 do `design-system.md`. Variações
  são em peso (bold/regular), tamanho e cor — não em fonte.
- **Use `prstGeom`** para formas: `rect`, `roundRect` (`adj≈6500`),
  `ellipse`, `triangle`, `chevron`, `arrow`, `diamond`. Combinações
  geométricas são bem-vindas (ex.: elipses sobrepostas para Venn,
  `roundRect` aninhados para card-em-card).
- **Limites de área útil da seção 0.1 valem igual.** O design pode ser
  rico, mas tem que caber dentro do `(750000–7700000) × (500000–4650000)`
  EMU do soft limit (ou no hard limit em casos excepcionais).
- **Faixa amarela canônica sob o H1 segue obrigatória** em todo slide
  com H1 textual, mesmo nos mais elaborados.
- **Citação `Autor (ano)` no rodapé interno** continua obrigatória
  quando o slide introduz conceito.

Quando duplicar um padrão, **desempacote o `.pptx` da Aula 1 e copie o
XML do slide-fonte** indicado na tabela. As medidas estão lá, calibradas.

---

## 15. Outros padrões visuais da Aula 1 incorporados como regra

- **Citação no rodapé interno**: `off x=556250`–`750000`, `off y≈4339343`–`4350000`, `cx=3639300`–`5950000`, `cy=200000`–`270600`, `sz=800`–`1000`, Arial (italic opcional), `#666666` ou `#999999`. Obrigatória sempre que o slide introduzir um conceito relevante (ver `content-rules.md`). Exemplo Aula 1 B1 slide 22: `off=(556250, 4339343)`, `ext=(3639300, 270600)`, `sz=800`, `#999999`.
- **Stat callout**: número em Arial Black `sz=9600` `#E8A317` + label Arial `sz=1600` `#666666`.
- **Cards genéricos cinza/pastel**: `roundRect` `adj≈6500`, fundo `#F4F4F4` ou `#FCE5CD` ou `#FFF7E6` (pastel amarelo), sem borda explícita.
- **Cards brancos com borda navy** (regra 10): `roundRect` `adj≈6500`, fundo `#FFFFFF`, borda `<a:ln w="12700">` `#1B2A4A`. Padrão obrigatório quando o card tiver fundo branco.
- **Caixa de definição navy com texto branco** (regra 10): `rect` ou `roundRect` fundo `#1B2A4A`, texto `#FFFFFF` Arial Black centralizado. Usar para definições, conceitos-chave e textos em destaque. **Nunca usar texto amarelo sobre navy** — sempre branco.
- **Bullets**: `<a:buChar>` ou `<a:buAutoNum>`. **Nunca** `•` literal.
- **Bullets estilizados (regra 10)**: círculos amarelos (`ellipse` `#E8A317`) ou navy (`ellipse` `#1B2A4A`) como marcadores. Tamanhos típicos: `160000×160000` (objetivos), `217800×180000` (ponte), `473100×420000` (agenda), `600900×500100` (síntese).
- **Bullets numerados visuais (agenda)**: elipse navy `473100×420000` (B1) ou `505200×420000` (B2) com número `sz=1600` Arial Black `#E8A317`.
- **Marcadores de objetivo**: círculo amarelo `160000×160000`.
- **Marcadores de síntese**: **elipse** amarela `600900×500100` com número branco `sz=2000`.
- **Tag em caps**: Arial Black `sz=1200` `#E8A317` em caixa de `300000` de altura.

Cores: navy `#1B2A4A`, amarelo `#E8A317`, cinza `#666666`/`#333333`/`#999999`,
pastel amarelo `#FCE5CD`/`#FFF7E6`, fundo neutro `#F4F4F4`. Branco `#FFFFFF` apenas
para texto sobre cards navy ou amarelos.

### Combinações de cor proibidas (regra 10)

| Combinação | Permitida? | Alternativa |
|---|---|---|
| Texto amarelo `#E8A317` sobre fundo navy `#1B2A4A` | ❌ NÃO | Usar texto branco `#FFFFFF` |
| Texto navy `#1B2A4A` sobre fundo amarelo `#E8A317` | ❌ NÃO | Usar texto branco `#FFFFFF` |
| Texto branco sobre fundo branco | ❌ NÃO (invisível) | Mudar fundo |
| Texto cinza claro sobre fundo cinza | ❌ NÃO (contraste ruim) | Usar `#333333` ou `#1B2A4A` |
| Texto navy sobre fundo branco | ✅ Sim | — |
| Texto amarelo sobre fundo branco | ✅ Sim (apenas para subtítulos curtos) | Negrito recomendado |
| Texto branco sobre fundo navy | ✅ Sim | — |
| Texto branco sobre fundo amarelo | ✅ Sim (com bold/Black) | — |

---

## 16. Checklist de paridade visual com a Aula 1 (obrigatório)

Antes de fechar qualquer bloco, confronte cada slide do tipo abaixo com
o slide-fonte indicado:

- [ ] **Área útil canônica:** `check_useful_area.py` retorna 0 hard violations (seção 0).
- [ ] **Capa** confronta com `aula1_blocoY/slide1.xml` (medidas seção 3).
- [ ] **Agenda** confronta com `aula1_blocoY/slide{3 ou 2}.xml` (seção 5).
- [ ] **Objetivos** confronta com `aula1_blocoY/slide{4 ou 3}.xml` (seção 6).
- [ ] **Conexão** confronta com `aula1_blocoY/slide{5 ou 4}.xml` (seção 7).
- [ ] **Cada Transição de tópico** confronta com `aula1_bloco1/slide6.xml` (seção 4).
- [ ] **Síntese** confronta com `aula1_bloco1/slide46.xml` (seção 8).
- [ ] **Ponte** confronta com `aula1_bloco1/slide47.xml` (seção 9).
- [ ] **Referências** confronta com `aula1_bloco1/slide48.xml` (seção 10).
- [ ] **Encerramento** confronta com `aula1_bloco1/slide49.xml` (B1) ou `aula1_bloco2/slide42.xml` (B2) (seção 11).
- [ ] **Atividade Prática** (apenas B2 das Aulas 1–4) confronta com `aula1_bloco2/slide38.xml` (seção 12).
- [ ] **Slides de correção** (apenas B1 das Aulas 2–5) seguem a sequência fixa da seção 13.
- [ ] **Slides de conteúdo com H1** trazem a faixa amarela canônica nas medidas da seção 2.
- [ ] **Fundos** seguem o mapa da seção 1 (`image1` em capa/transição/encerramento; `image2` no resto).
- [ ] Nenhum slide só de texto: todo slide tem ao menos 1 elemento visual.
- [ ] Cita `Autor (ano)` no rodapé interno em todo slide que introduz conceito.

## 17. Onde está o XML de referência

Após `unpack_pptx.py` nos `.pptx` da Aula 1:

- `ppt/slides/slideN.xml` — formas e textos.
- `ppt/slides/_rels/slideN.xml.rels` — confirma `image1.png` ou `image2.png` em `rId3`.

Para snippets reutilizáveis (cabeçalho, capa, transição, conexão,
síntese, ponte, encerramento, atividade prática), veja
[`slide-templates.md`](slide-templates.md).
