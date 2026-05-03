# Snippets XML por layout canônico

Trechos prontos para copiar dentro de `<p:spTree>` em
`ppt/slides/slideN.xml`. **Nunca** mexa em `<p:bg>...</p:bg>` nem em
`<p:nvGrpSpPr>` / `<p:grpSpPr>` que abrem o `spTree`. Insira novas
formas como filhas de `<p:spTree>`, depois do grupo que já vem do
modelo.

Toda medida abaixo é **literalmente extraída da Aula 1** e deve ser
preservada. Se algum encaixe pedir variação, verifique antes contra
o slide-fonte indicado em [`layout-canonical.md`](layout-canonical.md).

## Convenções de coordenadas (EMU)

Slide 16:9 = `9144000 × 5143500` EMU.

Para slides de **conteúdo** (fundo `image2.png`):

- `x` ∈ [`750000`, `6700000`] (largura útil ≈ 5950000)
- `y` ∈ [`500000`, `4500000`] (H1 da Aula 1 em **`500000`**)

Para slides de **capa, transição e encerramento** (fundo `image1.png`):
mesma área branca à esquerda, mas eixo de texto em `x≈1097275` (capa e
transição) ou `x≈822950` (encerramento), conforme cada seção abaixo.

---

## 1. Cabeçalho padrão (H1 + faixa amarela + subtítulo opcional)

**Norma:** todo slide com H1 textual replica esta pilha. Vale para
Agenda, Objetivos, Conexão, Síntese, Ponte, Referências, Atividade
Prática, slides de correção, conceito, stat callout, comparação,
diagrama, tabela e citação.

```xml
<!-- H1 -->
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="100" name="H1"/>
    <p:cNvSpPr txBox="1"/>
    <p:nvPr/>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm>
      <a:off x="750000" y="500000"/>
      <a:ext cx="5950000" cy="900000"/>
    </a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="t"/>
    <a:lstStyle/>
    <a:p>
      <a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="2400" b="1">
          <a:solidFill><a:srgbClr val="1B2A4A"/></a:solidFill>
          <a:latin typeface="Arial Black"/>
        </a:rPr>
        <a:t>Título do slide</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>

<!-- Faixa amarela canônica -->
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="101" name="FaixaTitulo"/>
    <p:cNvSpPr/>
    <p:nvPr/>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm>
      <a:off x="750005" y="905100"/>
      <a:ext cx="1500000" cy="54900"/>
    </a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
    <a:solidFill><a:srgbClr val="E8A317"/></a:solidFill>
    <a:ln><a:noFill/></a:ln>
  </p:spPr>
  <p:txBody>
    <a:bodyPr anchor="ctr"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="l"/><a:endParaRPr lang="pt-BR" sz="1400"/></a:p>
  </p:txBody>
</p:sp>

<!-- Subtítulo amarelo (opcional, mas recomendado em slides estruturais) -->
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="102" name="Subtitulo"/>
    <p:cNvSpPr txBox="1"/>
    <p:nvPr/>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm>
      <a:off x="750000" y="1330000"/>
      <a:ext cx="5950000" cy="400000"/>
    </a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="t"/>
    <a:lstStyle/>
    <a:p>
      <a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="1400" b="1">
          <a:solidFill><a:srgbClr val="E8A317"/></a:solidFill>
          <a:latin typeface="Arial"/>
        </a:rPr>
        <a:t>Frase-fórmula do subtítulo</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>
```

Subtítulos amarelos canônicos por tipo de slide: ver tabela na seção 2
de `layout-canonical.md`.

---

## 2. Capa do bloco

Slide-fonte: `aula1_blocoY/slide1.xml`. Fundo: `image1.png`.

```xml
<!-- Título da disciplina (caixa alta) -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="200" name="CapaTitulo"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="1097275" y="914400"/><a:ext cx="6790500" cy="1828800"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="t"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="3200" b="1">
          <a:solidFill><a:srgbClr val="1B2A4A"/></a:solidFill>
          <a:latin typeface="Arial Black"/>
        </a:rPr>
        <a:t>JURIMETRIA E ANÁLISE DE DADOS PARA DECISÕES ESTRATÉGICAS</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>

<!-- Faixa amarela horizontal -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="201" name="CapaFaixa"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="1097280" y="2788920"/><a:ext cx="1828800" cy="54864"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
    <a:solidFill><a:srgbClr val="E8A317"/></a:solidFill>
    <a:ln><a:noFill/></a:ln>
  </p:spPr>
  <p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr lang="pt-BR"/></a:p></p:txBody>
</p:sp>

<!-- Linha "Aula X – Bloco Y" em amarelo -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="202" name="CapaAulaBloco"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="1097280" y="2926080"/><a:ext cx="5486400" cy="457200"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="t"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="2000">
          <a:solidFill><a:srgbClr val="E8A317"/></a:solidFill>
          <a:latin typeface="Arial"/>
        </a:rPr>
        <a:t>Aula X – Bloco Y</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>

<!-- Subtítulo do bloco em cinza -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="203" name="CapaSubtitulo"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="1097280" y="3337560"/><a:ext cx="5486400" cy="365760"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="t"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="1400">
          <a:solidFill><a:srgbClr val="666666"/></a:solidFill>
          <a:latin typeface="Arial"/>
        </a:rPr>
        <a:t>Tema do bloco em até 2 linhas</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>
```

---

## 3. Transição de tópico (01, 02, 03…)

Slide-fonte: `aula1_bloco1/slide6.xml`. Fundo: `image1.png`.

```xml
<!-- Número grande amarelo. cx=2400000 (não 1800000) para evitar quebra
     horizontal de "01" a 96pt em renderizadores com Arial Black real. -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="300" name="TransicaoNumero"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="1097275" y="900000"/><a:ext cx="2400000" cy="1100000"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="t"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="9600" b="1">
          <a:solidFill><a:srgbClr val="E8A317"/></a:solidFill>
          <a:latin typeface="Arial Black"/>
        </a:rPr>
        <a:t>01</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>

<!-- Título do tópico -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="301" name="TransicaoTitulo"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="1097275" y="2100000"/><a:ext cx="6500000" cy="1100000"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="t"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="3600" b="1">
          <a:solidFill><a:srgbClr val="1B2A4A"/></a:solidFill>
          <a:latin typeface="Arial Black"/>
        </a:rPr>
        <a:t>Nome do tópico</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>

<!-- Faixa amarela -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="302" name="TransicaoFaixa"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="1097280" y="3250000"/><a:ext cx="1500000" cy="54864"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
    <a:solidFill><a:srgbClr val="E8A317"/></a:solidFill>
    <a:ln><a:noFill/></a:ln>
  </p:spPr>
  <p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr lang="pt-BR"/></a:p></p:txBody>
</p:sp>

<!-- Subtítulo cinza -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="303" name="TransicaoSubtitulo"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="1097280" y="3400000"/><a:ext cx="5486400" cy="500000"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="t"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="1400">
          <a:solidFill><a:srgbClr val="666666"/></a:solidFill>
          <a:latin typeface="Arial"/>
        </a:rPr>
        <a:t>Frase de contexto do tópico</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>
```

---

## 4. Item de Agenda (elipse navy + número amarelo + título)

Slide-fonte: `aula1_bloco1/slide3.xml`. Use o cabeçalho padrão (seção 1)
+ replicar o item abaixo nas posições da grade 2×4 (ver
`layout-canonical.md` seção 5).

```xml
<!-- Elipse navy com número amarelo -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="400" name="AgendaElipse1"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="781363" y="1700000"/><a:ext cx="420000" cy="420000"/></a:xfrm>
    <a:prstGeom prst="ellipse"><a:avLst/></a:prstGeom>
    <a:solidFill><a:srgbClr val="1B2A4A"/></a:solidFill>
    <a:ln><a:noFill/></a:ln>
  </p:spPr>
  <p:txBody>
    <a:bodyPr anchor="ctr"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="ctr"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="1600" b="1">
          <a:solidFill><a:srgbClr val="E8A317"/></a:solidFill>
          <a:latin typeface="Arial Black"/>
        </a:rPr>
        <a:t>1</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>

<!-- Título do item -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="401" name="AgendaTitulo1"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="1301363" y="1760000"/><a:ext cx="2400000" cy="399900"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="ctr"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="1200">
          <a:solidFill><a:srgbClr val="1B2A4A"/></a:solidFill>
          <a:latin typeface="Arial"/>
        </a:rPr>
        <a:t>Texto curto do item de agenda</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>
```

Demais posições (`x` da elipse / `x` do título / `y`):

| Coluna E | Coluna D | y elipse | y título |
|---|---|---|---|
| `781363` | `4204761` | `1700000` | `1760000` |
| `781363` | `4204761` | `2300000` | `2360000` |
| `781363` | `4204761` | `2900000` | `2960000` |
| `781363` | `4204761` | `3500000` | `3560000` |

`x título`: `1301363` (E) / `4724761` (D).

---

## 5. Item de Objetivos (círculo amarelo + verbo + descrição)

Slide-fonte: `aula1_bloco1/slide4.xml`. Cabeçalho padrão + repetir item.

```xml
<!-- Círculo amarelo -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="500" name="ObjMarker1"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="790000" y="1780000"/><a:ext cx="160000" cy="160000"/></a:xfrm>
    <a:prstGeom prst="ellipse"><a:avLst/></a:prstGeom>
    <a:solidFill><a:srgbClr val="E8A317"/></a:solidFill>
    <a:ln><a:noFill/></a:ln>
  </p:spPr>
  <p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr lang="pt-BR"/></a:p></p:txBody>
</p:sp>

<!-- Verbo de ação -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="501" name="ObjVerbo1"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="1060000" y="1750000"/><a:ext cx="1800000" cy="300000"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="t"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="1500" b="1">
          <a:solidFill><a:srgbClr val="1B2A4A"/></a:solidFill>
          <a:latin typeface="Arial Black"/>
        </a:rPr>
        <a:t>Compreender</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>

<!-- Texto descritivo -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="502" name="ObjTexto1"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="2900000" y="1750000"/><a:ext cx="4900000" cy="500100"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="t"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="1300">
          <a:solidFill><a:srgbClr val="333333"/></a:solidFill>
          <a:latin typeface="Arial"/>
        </a:rPr>
        <a:t>texto que completa o verbo de ação</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>
```

`y` por linha (5 itens): `1750000`, `2270000`, `2790000`, `3310000`, `3830000`.
Passo vertical fixo: `520000`. `y` do círculo = `y` do verbo + `30000`.

---

## 6. Conexão (3 cards pastel HOJE / AULAS X-Y / AULA Z)

Slide-fonte: `aula1_bloco1/slide5.xml`. Cabeçalho padrão + texto
introdutório navy + 3 cards.

```xml
<!-- Texto introdutório navy -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="600" name="ConexaoIntro"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="750000" y="1730000"/><a:ext cx="5950000" cy="340000"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="t"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="1400">
          <a:solidFill><a:srgbClr val="333333"/></a:solidFill>
          <a:latin typeface="Arial"/>
        </a:rPr>
        <a:t>Frase de contexto sobre a conexão.</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>

<!-- Card 1 (esquerda) -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="601" name="CardEsq"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="750000" y="2150000"/><a:ext cx="2163600" cy="2000100"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
    <a:solidFill><a:srgbClr val="FCE5CD"/></a:solidFill>
    <a:ln><a:noFill/></a:ln>
  </p:spPr>
  <p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr lang="pt-BR"/></a:p></p:txBody>
</p:sp>
<!-- Tag amarela em caps -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="602" name="CardEsqTag"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="920799" y="2300000"/><a:ext cx="1821900" cy="300000"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="t"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="1200" b="1">
          <a:solidFill><a:srgbClr val="E8A317"/></a:solidFill>
          <a:latin typeface="Arial Black"/>
        </a:rPr>
        <a:t>HOJE</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>
<!-- Título do card -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="603" name="CardEsqTitulo"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="920799" y="2630000"/><a:ext cx="1821900" cy="500100"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="t"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="1400" b="1">
          <a:solidFill><a:srgbClr val="1B2A4A"/></a:solidFill>
          <a:latin typeface="Arial Black"/>
        </a:rPr>
        <a:t>Fundamentos</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>
<!-- Descrição do card -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="604" name="CardEsqTexto"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="920799" y="3200000"/><a:ext cx="1821900" cy="900000"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="t"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="1200">
          <a:solidFill><a:srgbClr val="333333"/></a:solidFill>
          <a:latin typeface="Arial"/>
        </a:rPr>
        <a:t>Descrição do que acontece nesta etapa do curso.</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>
```

Para os outros dois cards, repita as 4 formas alterando apenas o `off x`:

- Card centro: `off x` do retângulo = `3084250`; `off x` do conteúdo interno = `3255048`.
- Card direita: `off x` do retângulo = `5418499`; `off x` do conteúdo interno = `5589298`.

---

## 7. Síntese (selo amarelo numerado + texto)

Slide-fonte: `aula1_bloco1/slide46.xml`. Cabeçalho padrão + repetir item.

```xml
<!-- Selo amarelo com número branco -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="700" name="SinteseSelo1"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="750000" y="1750000"/><a:ext cx="500000" cy="500000"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
    <a:solidFill><a:srgbClr val="E8A317"/></a:solidFill>
    <a:ln><a:noFill/></a:ln>
  </p:spPr>
  <p:txBody>
    <a:bodyPr anchor="ctr"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="ctr"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="2000" b="1">
          <a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>
          <a:latin typeface="Arial Black"/>
        </a:rPr>
        <a:t>1</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>

<!-- Texto descritivo -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="701" name="SinteseTexto1"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="1350000" y="1810000"/><a:ext cx="5300000" cy="450000"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="t"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="1250">
          <a:solidFill><a:srgbClr val="333333"/></a:solidFill>
          <a:latin typeface="Arial"/>
        </a:rPr>
        <a:t>Ponto-chave 1.</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>
```

`y` por item: `1750000`, `2320000`, `2890000`, `3460000`, `4030000` (passo `570000`).

---

## 8. Ponte (hero seta + lista de 4 itens)

Slide-fonte: `aula1_bloco1/slide47.xml`. Cabeçalho padrão.

```xml
<!-- Seta hero -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="800" name="PonteSeta"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="750000" y="1585100"/><a:ext cx="1500000" cy="594900"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="ctr"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="6000" b="1">
          <a:solidFill><a:srgbClr val="E8A317"/></a:solidFill>
          <a:latin typeface="Arial Black"/>
        </a:rPr>
        <a:t>➜</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>

<!-- Título de destaque -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="801" name="PonteHeroTitulo"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="2200000" y="1780000"/><a:ext cx="4500000" cy="400000"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="t"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="2000" b="1">
          <a:solidFill><a:srgbClr val="1B2A4A"/></a:solidFill>
          <a:latin typeface="Arial Black"/>
        </a:rPr>
        <a:t>Frase de destaque da ponte</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>

<!-- Descrição cinza do hero -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="802" name="PonteHeroSub"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="2200000" y="2100000"/><a:ext cx="4500000" cy="399900"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="t"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="1250">
          <a:solidFill><a:srgbClr val="666666"/></a:solidFill>
          <a:latin typeface="Arial"/>
        </a:rPr>
        <a:t>Descrição curta do que vem a seguir.</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>

<!-- Item de lista (repetir 4 vezes alterando y) -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="803" name="PonteBullet1"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="790000" y="2650000"/><a:ext cx="197700" cy="180000"/></a:xfrm>
    <a:prstGeom prst="ellipse"><a:avLst/></a:prstGeom>
    <a:solidFill><a:srgbClr val="E8A317"/></a:solidFill>
    <a:ln><a:noFill/></a:ln>
  </p:spPr>
  <p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr lang="pt-BR"/></a:p></p:txBody>
</p:sp>
<p:sp>
  <p:nvSpPr><p:cNvPr id="804" name="PonteItem1Tit"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="1075695" y="2600000"/><a:ext cx="2637300" cy="300000"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="t"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="1250">
          <a:solidFill><a:srgbClr val="1B2A4A"/></a:solidFill>
          <a:latin typeface="Arial"/>
        </a:rPr>
        <a:t>Item da ponte</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>
<p:sp>
  <p:nvSpPr><p:cNvPr id="805" name="PonteItem1Desc"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="3822762" y="2600000"/><a:ext cx="3406500" cy="300000"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="t"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="1150">
          <a:solidFill><a:srgbClr val="333333"/></a:solidFill>
          <a:latin typeface="Arial"/>
        </a:rPr>
        <a:t>Descrição complementar.</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>
```

`y` por item: `2600000`, `3030000`, `3460000`, `3890000` (bullet em `y_item + 50000`).

---

## 9. Encerramento — Bloco 1 ("Intervalo")

Slide-fonte: `aula1_bloco1/slide49.xml`. Fundo: `image1.png`.

```xml
<p:sp>
  <p:nvSpPr><p:cNvPr id="900" name="FimTitulo"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="822960" y="914400"/><a:ext cx="5486400" cy="731400"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="t"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="3600" b="1">
          <a:solidFill><a:srgbClr val="1B2A4A"/></a:solidFill>
          <a:latin typeface="Arial Black"/>
        </a:rPr>
        <a:t>Fim do Bloco 1</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>

<p:sp>
  <p:nvSpPr><p:cNvPr id="901" name="FimFaixa"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="822960" y="1691640"/><a:ext cx="1828800" cy="54900"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
    <a:solidFill><a:srgbClr val="E8A317"/></a:solidFill>
    <a:ln><a:noFill/></a:ln>
  </p:spPr>
  <p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr lang="pt-BR"/></a:p></p:txBody>
</p:sp>

<p:sp>
  <p:nvSpPr><p:cNvPr id="902" name="FimIntervalo"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="822960" y="2391995"/><a:ext cx="5486400" cy="457200"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="t"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="2000">
          <a:solidFill><a:srgbClr val="E8A317"/></a:solidFill>
          <a:latin typeface="Arial"/>
        </a:rPr>
        <a:t>Intervalo de 15 minutos</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>

<p:sp>
  <p:nvSpPr><p:cNvPr id="903" name="FimSub"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="822955" y="2849200"/><a:ext cx="5486400" cy="360000"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="t"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="1300">
          <a:solidFill><a:srgbClr val="666666"/></a:solidFill>
          <a:latin typeface="Arial"/>
        </a:rPr>
        <a:t>No Bloco 2: gancho do tema do próximo bloco.</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>
```

---

## 10. Encerramento — Bloco 2 ("Fim da Aula N")

Slide-fonte: `aula1_bloco2/slide42.xml`. Fundo: `image1.png`.

```xml
<p:sp>
  <p:nvSpPr><p:cNvPr id="950" name="FimAulaTitulo"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="822950" y="914400"/><a:ext cx="5486400" cy="702600"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="t"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="3600" b="1">
          <a:solidFill><a:srgbClr val="1B2A4A"/></a:solidFill>
          <a:latin typeface="Arial Black"/>
        </a:rPr>
        <a:t>Fim da Aula N</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>

<p:sp>
  <p:nvSpPr><p:cNvPr id="951" name="FimAulaFaixa"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="822950" y="1661173"/><a:ext cx="1828800" cy="52800"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
    <a:solidFill><a:srgbClr val="E8A317"/></a:solidFill>
    <a:ln><a:noFill/></a:ln>
  </p:spPr>
  <p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr lang="pt-BR"/></a:p></p:txBody>
</p:sp>

<p:sp>
  <p:nvSpPr><p:cNvPr id="952" name="FimAulaLembrete"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="822950" y="1836884"/><a:ext cx="5486400" cy="351300"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="t"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="1600">
          <a:solidFill><a:srgbClr val="E8A317"/></a:solidFill>
          <a:latin typeface="Arial"/>
        </a:rPr>
        <a:t>Lembrete:</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>

<p:sp>
  <p:nvSpPr><p:cNvPr id="953" name="FimAulaEntrega"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="822950" y="2188307"/><a:ext cx="5486400" cy="351300"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="t"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="1400">
          <a:solidFill><a:srgbClr val="666666"/></a:solidFill>
          <a:latin typeface="Arial"/>
        </a:rPr>
        <a:t>Entregar a Atividade N até a próxima aula.</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>

<p:sp>
  <p:nvSpPr><p:cNvPr id="954" name="FimAulaProxima"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="822950" y="2697950"/><a:ext cx="6915900" cy="351300"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="t"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="1500">
          <a:solidFill><a:srgbClr val="1B2A4A"/></a:solidFill>
          <a:latin typeface="Arial"/>
        </a:rPr>
        <a:t>Próxima aula: ementa em uma frase.</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>
```

> Em Aulas 5 (Bloco 2 sem atividade) e 6, troque "Lembrete: Entregar a
> Atividade N…" pela frase apropriada (preparação do trabalho final ou
> encerramento da disciplina).

---

## 11. Atividade Prática (B2 das Aulas 1 a 4)

Slide-fonte: `aula1_bloco2/slide38.xml`. Cabeçalho padrão (H1 + faixa
amarela) com subtítulo amarelo `Entrega até a Aula N+1`.

```xml
<!-- Card navy alto -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="1000" name="AtivCard"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="750000" y="1522612"/><a:ext cx="6847800" cy="800100"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
    <a:solidFill><a:srgbClr val="1B2A4A"/></a:solidFill>
    <a:ln><a:noFill/></a:ln>
  </p:spPr>
  <p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr lang="pt-BR"/></a:p></p:txBody>
</p:sp>
<!-- Título da atividade dentro do card -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="1001" name="AtivTituloCard"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="922633" y="1592612"/><a:ext cx="6502500" cy="660000"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="ctr"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="1700" b="1">
          <a:solidFill><a:srgbClr val="E8A317"/></a:solidFill>
          <a:latin typeface="Arial Black"/>
        </a:rPr>
        <a:t>Resumo do desafio em uma linha</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>

<!-- Caixa "Você deverá produzir" -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="1002" name="AtivProduzir"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="750000" y="2472612"/><a:ext cx="6847800" cy="300000"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="t"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="1400" b="1">
          <a:solidFill><a:srgbClr val="1B2A4A"/></a:solidFill>
          <a:latin typeface="Arial Black"/>
        </a:rPr>
        <a:t>Você deverá produzir</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>

<!-- Bloco com Pergunta 1./2./3. -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="1003" name="AtivPerguntas"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="750000" y="2772600"/><a:ext cx="7020000" cy="1861200"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="t"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="1100" b="1">
          <a:solidFill><a:srgbClr val="E8A317"/></a:solidFill>
          <a:latin typeface="Arial"/>
        </a:rPr>
        <a:t>Pergunta 1. </a:t>
      </a:r>
      <a:r>
        <a:rPr lang="pt-BR" sz="1100">
          <a:solidFill><a:srgbClr val="333333"/></a:solidFill>
          <a:latin typeface="Arial"/>
        </a:rPr>
        <a:t>Enunciado em até 2 linhas.</a:t>
      </a:r>
    </a:p>
    <!-- Repetir <a:p> para Pergunta 2 e Pergunta 3 -->
  </p:txBody>
</p:sp>
```

---

## 12. Citação no rodapé interno (referência discreta)

Obrigatório em todo slide que introduz conceito relevante (ver
`content-rules.md`).

```xml
<p:sp>
  <p:nvSpPr><p:cNvPr id="1100" name="Citacao"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="750000" y="4350000"/><a:ext cx="5950000" cy="200000"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="b"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="1000" i="1">
          <a:solidFill><a:srgbClr val="666666"/></a:solidFill>
          <a:latin typeface="Arial"/>
        </a:rPr>
        <a:t>Nunes (2019); ABJ (2023)</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>
```

---

## 13. Stat callout (número grande)

Para números de impacto. `sz=9600` (96pt) é forte; ajuste para `7200`
quando o número for muito largo (ex.: "1.234.567").

```xml
<p:sp>
  <p:nvSpPr><p:cNvPr id="1200" name="StatNumero"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="900000" y="1700000"/><a:ext cx="3000000" cy="1500000"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="ctr"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="9600" b="1">
          <a:solidFill><a:srgbClr val="E8A317"/></a:solidFill>
          <a:latin typeface="Arial Black"/>
        </a:rPr>
        <a:t>16.110</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>
<p:sp>
  <p:nvSpPr><p:cNvPr id="1201" name="StatLabel"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="900000" y="3200000"/><a:ext cx="3000000" cy="600000"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="t"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="1600">
          <a:solidFill><a:srgbClr val="666666"/></a:solidFill>
          <a:latin typeface="Arial"/>
        </a:rPr>
        <a:t>julgados de revisão e renovatória de locação no TJSP, 2010 a 2024</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>
```

---

## 14. Comparação em 2 colunas

Largura útil = `5950000`. Cada coluna ≈ `2900000` com gap de `150000`.

```xml
<!-- Coluna esquerda: cabeçalho navy -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="1300" name="ColEsqHeader"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="750000" y="1780000"/><a:ext cx="2900000" cy="500000"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
    <a:solidFill><a:srgbClr val="1B2A4A"/></a:solidFill>
    <a:ln><a:noFill/></a:ln>
  </p:spPr>
  <p:txBody>
    <a:bodyPr anchor="ctr" lIns="180000" rIns="180000"/>
    <a:p><a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="2000" b="1">
          <a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>
          <a:latin typeface="Arial Black"/>
        </a:rPr>
        <a:t>Modo raiz</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>
<!-- Repetir para coluna direita ajustando off x="3800000" -->
```

---

## 15. Card simples (fundo cinza claro com borda navy)

```xml
<p:sp>
  <p:nvSpPr><p:cNvPr id="1400" name="Card"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="800000" y="2200000"/><a:ext cx="5850000" cy="1700000"/></a:xfrm>
    <a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val 6500"/></a:avLst></a:prstGeom>
    <a:solidFill><a:srgbClr val="F4F4F4"/></a:solidFill>
    <a:ln w="9525"><a:solidFill><a:srgbClr val="1B2A4A"/></a:solidFill></a:ln>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="t" lIns="200000" rIns="200000" tIns="180000" bIns="180000"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="2000" b="1">
          <a:solidFill><a:srgbClr val="1B2A4A"/></a:solidFill>
          <a:latin typeface="Arial Black"/>
        </a:rPr>
        <a:t>Caso XY&amp;A</a:t>
      </a:r>
    </a:p>
    <a:p><a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="1600">
          <a:solidFill><a:srgbClr val="333333"/></a:solidFill>
          <a:latin typeface="Arial"/>
        </a:rPr>
        <a:t>Texto do exemplo aplicado ao escritório fictício.</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>
```

> Em XML, `&` → `&amp;`. Use `XY&amp;A` e `X, Y &amp; Associados`.

---

## 16. Bloco de bullets

Use `<a:buChar>` (ou `<a:buAutoNum>` para listas numeradas). **Nunca**
prefixe `•` literal.

```xml
<p:sp>
  <p:nvSpPr><p:cNvPr id="1500" name="Bullets"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="750000" y="1780000"/><a:ext cx="5950000" cy="2400000"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="t"/>
    <a:lstStyle/>
    <a:p>
      <a:pPr marL="285750" indent="-285750" algn="l">
        <a:buClr><a:srgbClr val="E8A317"/></a:buClr>
        <a:buFont typeface="Arial"/>
        <a:buChar char="•"/>
      </a:pPr>
      <a:r>
        <a:rPr lang="pt-BR" sz="1400">
          <a:solidFill><a:srgbClr val="333333"/></a:solidFill>
          <a:latin typeface="Arial"/>
        </a:rPr>
        <a:t>Primeiro item da lista.</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>
```

---

## 17. Tabela simples

Para tabelas curtas, prefira 3 caixas alinhadas como cabeçalho navy +
linhas em retângulos cinza alternados (zebrado). Para tabelas com muitas
linhas, use o elemento nativo `<a:graphicFrame><a:tbl>...</a:tbl></a:graphicFrame>`.

---

## 18. Padrões "estilosos" da Aula 1 (catálogo)

Para composições mais elaboradas (Venn 3 círculos, cards 2×2 numerados,
comparação em cards de cores diferentes, tabela com coluna semântica,
caixa de insight pastel), o catálogo está em
[`layout-canonical.md` §14a](layout-canonical.md), com o slide-fonte da
Aula 1 para cada padrão. Em vez de re-derivar medidas, **desempacote o
`.pptx` da Aula 1 e copie o XML do slide-fonte indicado** — geometria,
cores e tipografia já estão calibradas e validadas em sala.

---

## Speaker notes (`notesSlideN.xml`)

1. Copie `notesSlide1.xml` para `notesSlideN.xml`.
2. Atualize `notesSlideN.xml.rels` apontando para o slide correto.
3. Adicione `notesSlideN.xml` ao `[Content_Types].xml` quando necessário.
4. Edite o `<a:t>` do corpo com 3–6 linhas de pontos de fala.

> O script `add_slide.py` cobre o slide e seu `.rels`. Notas ainda
> precisam ser feitas à mão; mantenha-as nos slides densos.
