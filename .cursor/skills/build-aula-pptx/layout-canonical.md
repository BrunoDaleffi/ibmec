# Layouts canônicos (referência obrigatória)

A **Aula 1** (Bloco 1 e Bloco 2) é a **fonte de verdade visual** da disciplina.
Todo deck de qualquer aula deve **replicar literalmente** geometria (EMU),
tipografia (`sz`/fonte), cores (`srgbClr`) e ordem das formas dos slides
equivalentes da Aula 1.

Arquivos de referência:

- `aulas/aula_01/slides/aula1_bloco1_jurimetria.pptx`
- `aulas/aula_01/slides/aula1_bloco2_jurimetria.pptx`

**Antes de autorar slides novos:** desempacote o `.pptx` correspondente da
Aula 1 e copie do XML do slide-fonte indicado na tabela de cada seção. Não
re-derive medidas; copie.

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

---

## 1. Regra de fundos (image1.png × image2.png)

A Aula 1 fixa o seguinte uso (e este é o padrão da disciplina):

| Tipo de slide | Fundo | Razão |
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

A regra técnica continua: **não altere o bloco `<p:bg>...</p:bg>`** dos
slides; mude apenas o `Target` do `rId3` em `slideN.xml.rels` quando
precisar trocar o fundo de uma cópia.

> **Aviso histórico:** versões anteriores de `instrucao_geral.md` e
> `pedagogical-structure.md` indicavam o oposto (`image2` para
> capa/transição/fim, `image1` para conteúdo). A Aula 1 publicada usa o
> que está acima e passa a ser **norma**. A Aula 2 · Bloco 1 já entregue
> está com os fundos invertidos e está marcada para retrabalho.

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
| **H1** | `750000` | `500000` | `5950000` | `900000` | `2400` | Arial Black | `#1B2A4A` | Título do slide |
| **Faixa amarela** | `750005` | `905100` | `1500000` | `54900` | — | — | `#E8A317` | (vazio) |
| **Subtítulo amarelo** (opcional) | `750000` | `1330000` | `5950000` | `400000` | `1400` | Arial bold | `#E8A317` | Frase curta de apoio |
| **Início do corpo** | `750000` | `~1700000`–`1780000` | `5950000` | livre | `1200`–`1400` | Arial | `#333333` | Conteúdo |

A faixa amarela sob o H1 é **inegociável** em qualquer slide com título
textual. Só pode ser omitida em diagramas full-bleed sem H1 (raro).

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
| Subtítulo do bloco (cinza) | `1097280` | `3337560` | `5486400` | `365760` | `1400` | Arial | `#666666` | Frase do tema, máx. 2 linhas |

**Fundo:** `image1.png`.

> **Por que `sz=3200` e não `sz=3600`?** A versão original (Aula 1
> publicada) usa `sz=3600`. Em renderizadores que carregam a Arial Black
> real (PowerPoint, LibreOffice GUI, Keynote), `sz=3600` faz o título de
> 53 caracteres quebrar em **4 linhas** e a 4ª linha (`ESTRATÉGICAS`)
> sobrepõe a faixa amarela e a linha `Aula X – Bloco Y`. O `soffice
> --headless` usado no QA local cai num fallback de fonte mais estreito
> e não detecta o estouro. `sz=3200` reduz o título 11% mas garante 3
> linhas em qualquer renderizador. **Este é o tamanho canônico a partir
> de 2026-05-02; a Aula 1 publicada está marcada para retrabalho neste
> ponto.**

---

## 4. Transição de tópico (01, 02, 03…)

Slide-fonte: `aula1_bloco1/slide6.xml` (transição "01 | A disciplina").
Mesma geometria nas demais transições da Aula 1 (slides 12, 17, 20, 26, 31, 34, 40 do B1; 5, 11, 17, 21, 26, 32, 36 do B2).

| Camada | off x | off y | cx | cy | sz | Fonte | Cor | Texto |
|---|---|---|---|---|---|---|---|---|
| Número grande | `1097275` | `900000` | **`2400000`** | `1100000` | **`9600`** (96pt) | Arial Black | `#E8A317` | `01`, `02`, … |
| Título do tópico | `1097275` | `2100000` | `6500000` | `1100000` | `3600` | Arial Black | `#1B2A4A` | Nome do tópico |
| Faixa amarela | `1097280` | `3250000` | `1500000` | `54864` | — | — | `#E8A317` | (vazio) |
| Subtítulo cinza | `1097280` | `3400000` | `5486400` | `500000` | `1400` | Arial | `#666666` | Frase de contexto |

**Fundo:** `image1.png`.

> **Por que `cx=2400000` e não `cx=1800000`?** A versão original
> (Aula 1 publicada) usa `cx=1800000`. Com Arial Black real a 96pt,
> "01"/"02"/... ocupa ~1.7M EMU; com `cx=1800000` e os insets padrão
> (lIns=rIns=91440), a largura útil cai para ~1.62M EMU e o segundo
> dígito quebra para a linha de baixo, sobrepondo o título. `cx=2400000`
> dá margem segura. Vale o mesmo aviso da capa: o `soffice --headless`
> não detecta a quebra. **Tamanho canônico a partir de 2026-05-02; Aula 1
> publicada está marcada para retrabalho.**

---

## 5. Agenda do bloco

Slide-fonte: `aula1_bloco1/slide3.xml`. Cabeçalho padrão (seção 2).

Corpo: **grade de até 8 itens em 2 colunas × 4 linhas**.

Coordenadas dos itens (cada item é um par "elipse + título"):

| Linha | y (elipse e título) |
|---|---|
| 1 | `1700000` (elipse) / `1760000` (título) |
| 2 | `2300000` / `2360000` |
| 3 | `2900000` / `2960000` |
| 4 | `3500000` / `3560000` |

| Coluna | off x da elipse | off x do título |
|---|---|---|
| Esquerda | `781363` | `1301363` |
| Direita | `4204761` | `4724761` |

Forma de cada item:

- **Elipse navy** (`prstGeom prst="ellipse"`, fill `#1B2A4A`): `cx=420000`, `cy=420000`. Dentro: número `sz=1600`, Arial Black, cor `#E8A317`, alinhado ao centro.
- **Título do item**: caixa de texto `cx=2400000`, `cy=399900`, `sz=1200`, Arial, cor `#1B2A4A`, alinhado à esquerda, ancorado ao centro vertical.

Se a agenda tiver menos itens, **mantenha** o passo vertical e use só as
linhas necessárias começando em `y=1700000`.

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

Corpo (B1): **3 cards pastel `#FCE5CD`** lado a lado.

| Card | off x | cx | cy | y |
|---|---|---|---|---|
| Esquerda | `750000` | `2163600` | `2000100` | `2150000` |
| Centro | `3084250` | `2163600` | `2000100` | `2150000` |
| Direita | `5418499` | `2163600` | `2000100` | `2150000` |

Dentro de cada card (off x interno = card_x + 170799):

- **Tag amarela em caps** (HOJE / AULAS X-Y / AULA Z): `y=2300000`, `cx=1821900`, `cy=300000`, `sz=1200`, Arial Black, `#E8A317`.
- **Título do card** (Fundamentos / Método e aceleração / Apresentação): `y=2630000`, `cy=500100`, `sz=1400`, Arial Black, `#1B2A4A`.
- **Descrição**: `y=3200000`, `cy=900000`, `sz=1200`, Arial, `#333333`.

> Variantes (ex.: B2 com layout de "Onde paramos"): mantenha o cabeçalho
> padrão e adapte o corpo, mas prefira reutilizar a geometria de cards
> sempre que houver 2 ou 3 colunas equivalentes a comparar.

---

## 8. Síntese do bloco

Slide-fonte: `aula1_bloco1/slide46.xml`. Cabeçalho padrão.

Corpo: **5 itens verticais** com selo numerado amarelo + texto.

| Camada por item | off x | cx | cy | sz | Fonte | Cor |
|---|---|---|---|---|---|---|
| Quadrado amarelo (`prstGeom prst="rect"`) | `750000` | `500000` | `500000` | — | — | `#E8A317` |
| Número branco dentro do quadrado | (mesma caixa) | (mesma) | (mesma) | `2000` | Arial Black | `#FFFFFF` |
| Texto descritivo | `1350000` | `5300000` | `450000` | `1250` | Arial | `#333333` |

`y_item` por linha (5 itens):

```
1750000, 2320000, 2890000, 3460000, 4030000
```

Passo vertical de `570000` EMU.

> Se o bloco gerar 3 ou 4 pontos-chave em vez de 5, mantenha o mesmo
> passo e termine em y mais alto. Não comprima para encher 5.

---

## 9. Ponte para o próximo bloco/aula

Slide-fonte: `aula1_bloco1/slide47.xml`. Cabeçalho padrão.

Corpo: **hero esquerda** (seta gigante) + **lista de 4 itens**.

Hero (esquerda):

| Camada | off x | off y | cx | cy | sz | Fonte | Cor |
|---|---|---|---|---|---|---|---|
| Seta `➜` | `750000` | `1585100` | `1500000` | `594900` | `6000` | Arial Black | `#E8A317` |
| Título de destaque | `2200000` | `1780000` | `4500000` | `400000` | `2000` | Arial Black | `#1B2A4A` |
| Descrição cinza | `2200000` | `2100000` | `4500000` | `399900` | `1250` | Arial | `#666666` |

Lista de 4 itens (passo vertical `430000` a partir de `y=2600000`):

| Camada por item | off x | cx | cy | sz | Fonte | Cor |
|---|---|---|---|---|---|---|
| Bullet amarelo (`prstGeom prst="ellipse"`) | `790000` | `197700` | `180000` | — | — | `#E8A317` |
| Título do item | `1075695` | `2637300` | `300000` | `1250` | Arial | `#1B2A4A` |
| Descrição do item | `3822762` | `3406500` | `300000` | `1150` | Arial | `#333333` |

`y` por item: `2600000`, `3030000`, `3460000`, `3890000` (bullet a `+50000` y).

---

## 10. Referências do bloco

Slide-fonte: `aula1_bloco1/slide48.xml`. Cabeçalho padrão.

Corpo:

| Camada | off x | off y | cx | cy | sz | Fonte | Cor |
|---|---|---|---|---|---|---|---|
| Caixa única com referências em ABNT | `750000` | `1780000` | `7025100` | `2799900` | `1150` | Arial | `#333333` |
| Rodapé cinza explicativo | `750000` | `4300000` | `5950000` | `300000` | `1000` | Arial | `#666666` |

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

Slide-fonte: `aula1_bloco2/slide38.xml`. Cabeçalho padrão (H1 + faixa amarela). Subtítulo amarelo "Entrega até a Aula N+1".

Corpo:

| Camada | off x | off y | cx | cy | sz | Fonte | Cor |
|---|---|---|---|---|---|---|---|
| Card navy alto (`prstGeom prst="rect"`, fill `#1B2A4A`) | `750000` | `1522612` | `6847800` | `800100` | — | — | `#1B2A4A` |
| Título da atividade dentro do card | `922633` | `1592612` | `6502500` | `660000` | `1700` | Arial Black | `#E8A317` |
| Caixa "Você deverá produzir" (fundo navy) | `750000` | `2472612` | `6847800` | `300000` | `1400` | Arial Black | `#FFFFFF` |
| Bloco com Pergunta 1./2./3. | `750000` | `2772600` | `7020000` | `1861200` | `1100` | Arial | `#E8A317` (numeração) / `#333333` (texto) |

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
| **Diagrama de Venn 3 círculos** | `aula1_bloco1/slide22.xml` | 3 elipses semitransparentes (navy, amarelo, azul claro) sobrepostas + rótulos brancos no centro de cada uma + card lateral cinza com legenda das interseções. |
| **Cards 2×2 com selo numerado** | `aula1_bloco1/slide36.xml` | 4 `roundRect` com borda navy fina + elipse amarela com número branco + título navy + descrição cinza. Grade 2 colunas × 2 linhas. |
| **Comparação 2 colunas com cards coloridos** | `aula1_bloco1/slide43.xml` | 2 `roundRect` lado a lado: esquerda fundo `#F4F4F4`, direita fundo `#FCE5CD` (pastel amarelo). Tag em caps no topo, bullets quadrados amarelos, frase de fechamento em italic abaixo. |
| **Tabela com coluna semântica** | `aula1_bloco1/slide38.xml` | Tabela `<a:tbl>` com cabeçalho navy + linhas zebradas + última coluna com cores semânticas (verde negativo, navy base, amarelo positivo) + caixa de "Insight" com fundo `#FCE5CD` abaixo. |
| **Comparação 2 colunas (tabela)** | `aula1_bloco1/slide29.xml` | Tabela `<a:tbl>` com primeira coluna em bold navy (rótulo da dimensão) e duas colunas de comparação. Cabeçalho navy. |
| **Quadro de stat secundário** | `aula1_bloco1/slide14.xml` (Panorama Financeiro) | 3 stat callouts pequenos lado a lado: número grande amarelo + label cinza, com leve `roundRect` de fundo. |

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

- **Citação no rodapé interno**: `off x=750000`, `off y=4350000`, `cx=5950000`, `cy=200000`, `sz=1000`, Arial Italic, `#666666`. Obrigatória sempre que o slide introduzir um conceito relevante (ver `content-rules.md`).
- **Stat callout**: número em Arial Black `sz=9600` `#E8A317` + label Arial `sz=1600` `#666666`.
- **Cards genéricos**: `roundRect` `adj≈6500`, fundo `#F4F4F4` ou `#FCE5CD` (pastel amarelo), borda navy `9525`.
- **Bullets**: `<a:buChar>` ou `<a:buAutoNum>`. **Nunca** `•` literal.
- **Bullets numerados visuais**: elipse navy `420000×420000` com número `sz=1600` Arial Black `#E8A317`.
- **Marcadores de objetivo**: círculo amarelo `160000×160000`.
- **Marcadores de síntese**: quadrado amarelo `500000×500000` com número branco `sz=2000`.
- **Tag em caps**: Arial Black `sz=1200` `#E8A317` em caixa de `300000` de altura.

Cores: navy `#1B2A4A`, amarelo `#E8A317`, cinza `#666666`/`#333333`,
pastel amarelo `#FCE5CD`, fundo neutro `#F4F4F4`. Branco `#FFFFFF` apenas
para texto sobre cards navy.

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
