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
| Título da disciplina (caixa alta) | `1097275` | `914400` | `6790500` | `1828800` | `3600` | Arial Black | `#1B2A4A` | `JURIMETRIA E ANÁLISE DE DADOS PARA DECISÕES ESTRATÉGICAS` |
| Faixa amarela horizontal | `1097280` | `2788920` | `1828800` | `54864` | — | — | `#E8A317` | (vazio) |
| Linha "Aula X – Bloco Y" | `1097280` | `2926080` | `5486400` | `457200` | `2000` | Arial | `#E8A317` | `Aula X – Bloco Y` |
| Subtítulo do bloco (cinza) | `1097280` | `3337560` | `5486400` | `365760` | `1400` | Arial | `#666666` | Frase do tema, máx. 2 linhas |

**Fundo:** `image1.png`.

---

## 4. Transição de tópico (01, 02, 03…)

Slide-fonte: `aula1_bloco1/slide6.xml` (transição "01 | A disciplina").
Mesma geometria nas demais transições da Aula 1 (slides 12, 17, 20, 26, 31, 34, 40 do B1; 5, 11, 17, 21, 26, 32, 36 do B2).

| Camada | off x | off y | cx | cy | sz | Fonte | Cor | Texto |
|---|---|---|---|---|---|---|---|---|
| Número grande | `1097275` | `900000` | `1800000` | `1100000` | **`9600`** (96pt) | Arial Black | `#E8A317` | `01`, `02`, … |
| Título do tópico | `1097275` | `2100000` | `6500000` | `1100000` | `3600` | Arial Black | `#1B2A4A` | Nome do tópico |
| Faixa amarela | `1097280` | `3250000` | `1500000` | `54864` | — | — | `#E8A317` | (vazio) |
| Subtítulo cinza | `1097280` | `3400000` | `5486400` | `500000` | `1400` | Arial | `#666666` | Frase de contexto |

**Fundo:** `image1.png`.

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
