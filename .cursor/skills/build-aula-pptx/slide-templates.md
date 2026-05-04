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
<!-- Número grande amarelo. cx=1800000 (gold standard Aula 1 B1 slide 6). -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="300" name="TransicaoNumero"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="1097275" y="900000"/><a:ext cx="1800000" cy="1100000"/></a:xfrm>
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
<!-- Elipse navy com número BRANCO (medidas gold standard B1: ext=473100×420000).
     Regra 10: fundo navy = texto branco. NÃO usar amarelo. -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="400" name="AgendaElipse1"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="785321" y="1700000"/><a:ext cx="473100" cy="420000"/></a:xfrm>
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
          <a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>
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
    <a:xfrm><a:off x="1370945" y="1760000"/><a:ext cx="2703000" cy="399900"/></a:xfrm>
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

Demais posições (gold standard B1, `x` da elipse / `x` do título / `y`):

| Coluna E elipse | Coluna D elipse | y elipse | y título |
|---|---|---|---|
| `785321` | `4640749` | `1700000` | `1760000` |
| `785321` | `4640749` | `2300000` | `2360000` |
| `785321` | `4640749` | `2900000` | `2960000` |
| `785321` | `4640749` | `3500000` | `3560000` |

`x título`: `1370945` (E) / `5226372` (D).

Para B2 use a variante: elipse `505200×420000`, x esquerda `750000`,
x direita `4358824`; título x esquerda `1375529`, x direita `4984353`;
y começa em `1750000` (passo `600000`).

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
    <a:xfrm><a:off x="750000" y="2150000"/><a:ext cx="2255100" cy="2000100"/></a:xfrm>
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

- Card centro: `off x` do retângulo = `3183033`; `off x` do conteúdo interno = `3361059`.
- Card direita: `off x` do retângulo = `5616064`; `off x` do conteúdo interno = `5794091`.

Gap horizontal entre cards: `~178000` EMU.

---

## 7. Síntese (selo amarelo numerado + texto)

Slide-fonte: `aula1_bloco1/slide46.xml`. Cabeçalho padrão + repetir item.

```xml
<!-- Selo amarelo (ELIPSE, não rect) com número branco -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="700" name="SinteseSelo1"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="750000" y="1750000"/><a:ext cx="600900" cy="500100"/></a:xfrm>
    <a:prstGeom prst="ellipse"><a:avLst/></a:prstGeom>
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
    <a:xfrm><a:off x="1471034" y="1810000"/><a:ext cx="6369000" cy="450000"/></a:xfrm>
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

## 17a. Card branco com borda navy + selo numerado (regra 10)

Slide-fonte: `aula1_bloco1/slide16.xml`. Padrão obrigatório quando o
card tiver fundo branco. Selo amarelo numerado é opcional.

```xml
<!-- Card branco com borda navy -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="1600" name="CardBranco1"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="750000" y="1750000"/><a:ext cx="3435300" cy="1179900"/></a:xfrm>
    <a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val 6500"/></a:avLst></a:prstGeom>
    <a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>
    <a:ln cap="flat" cmpd="sng" w="12700">
      <a:solidFill><a:srgbClr val="1B2A4A"/></a:solidFill>
      <a:prstDash val="solid"/>
      <a:round/>
    </a:ln>
  </p:spPr>
  <p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr lang="pt-BR"/></a:p></p:txBody>
</p:sp>

<!-- Selo amarelo elíptico com número branco -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="1601" name="CardBrancoSelo1"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="894645" y="1850000"/><a:ext cx="602700" cy="500100"/></a:xfrm>
    <a:prstGeom prst="ellipse"><a:avLst/></a:prstGeom>
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

<!-- Título do card (Arial Black navy) -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="1602" name="CardBrancoTit1"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="1617872" y="1870000"/><a:ext cx="2410800" cy="350100"/></a:xfrm>
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
        <a:t>Título do card</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>

<!-- Descrição do card (Arial cinza) -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="1603" name="CardBrancoDesc1"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="930807" y="2400000"/><a:ext cx="3073800" cy="450000"/></a:xfrm>
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
        <a:t>Descrição do card em até 2 linhas.</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>
```

Para a grade 2×2 do slide 16, use `x=750000` e `x=4366134`,
`y=1750000` e `y=3070000`.

---

## 17a-bis. Card branco com barra navy de título (single column)

Padrão de "card premium" para single column (mini-caso, exemplo
prático, exercício, síntese de etapa). Inspirado no padrão do gold
standard slide 43 (que usa headers coloridos em 2 colunas) e adaptado
para 1 coluna larga. **Substitui** o card cinza claro `#F4F4F4` para
slides em que se quer mais peso visual.

Estrutura:

1. **Card externo** (`roundRect` `adj≈6500`, fill `#FFFFFF`, borda
   navy `<a:ln w="12700">`) ocupando toda a largura útil
   (`x=750000`, `cx=6950000`).
2. **Barra navy de título no topo** (`roundRect` `adj≈6500`, fill
   `#1B2A4A`, sem borda) com texto **branco** Arial Black centralizado
   (regra 10).
3. **Parágrafos do corpo** dentro do card branco, abaixo da barra.

```xml
<!-- 1) Card externo branco com borda navy -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="1650" name="CardWhite"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="750000" y="1500000"/><a:ext cx="6950000" cy="2600000"/></a:xfrm>
    <a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val 6500"/></a:avLst></a:prstGeom>
    <a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>
    <a:ln cap="flat" cmpd="sng" w="12700">
      <a:solidFill><a:srgbClr val="1B2A4A"/></a:solidFill>
      <a:prstDash val="solid"/><a:round/>
    </a:ln>
  </p:spPr>
  <p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr lang="pt-BR"/></a:p></p:txBody>
</p:sp>

<!-- 2) Barra navy de título com texto branco centralizado -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="1651" name="CardWhiteHeader"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="830000" y="1580000"/><a:ext cx="6790000" cy="600000"/></a:xfrm>
    <a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val 6500"/></a:avLst></a:prstGeom>
    <a:solidFill><a:srgbClr val="1B2A4A"/></a:solidFill>
    <a:ln><a:noFill/></a:ln>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="ctr" lIns="180000" rIns="180000"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="1700" b="1">
          <a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>
          <a:latin typeface="Arial Black"/>
        </a:rPr>
        <a:t>Título do card (em até 1 linha)</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>

<!-- 3) Corpo do card (parágrafos navy/cinza) -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="1652" name="CardWhiteBody"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="950000" y="2330000"/><a:ext cx="6550000" cy="1690000"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="t"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="l"><a:lnSpc><a:spcPct val="125000"/></a:lnSpc></a:pPr>
      <a:r>
        <a:rPr lang="pt-BR" sz="1400">
          <a:solidFill><a:srgbClr val="333333"/></a:solidFill>
          <a:latin typeface="Arial"/>
        </a:rPr>
        <a:t>Primeiro parágrafo do conteúdo do card.</a:t>
      </a:r>
    </a:p>
    <a:p><a:pPr algn="l"><a:lnSpc><a:spcPct val="125000"/></a:lnSpc><a:spcBef><a:spcPts val="400"/></a:spcBef></a:pPr>
      <a:r>
        <a:rPr lang="pt-BR" sz="1400">
          <a:solidFill><a:srgbClr val="333333"/></a:solidFill>
          <a:latin typeface="Arial"/>
        </a:rPr>
        <a:t>Segundo parágrafo.</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>
```

Recomendações de uso:

- **Sem subtítulo amarelo**: o título do card vai dentro da barra
  navy, então o cabeçalho padrão usa só H1 + faixa amarela (sem
  `subtítulo amarelo` separado).
- `card_y` começa em `1500000` (logo abaixo da faixa amarela
  canônica), ganhando ~250000 EMU de altura extra para o card.
- `card_h` típico: `2600000` (3-4 parágrafos de texto), `2750000`
  (mini-casos com 4+ parágrafos longos).
- Citação `Autor (ano)` em rodapé `y=4350000` (regra 6) — garanta gap
  ≥ 50000 EMU entre o card e a citação.

---

## 17b. Caixa de definição navy com texto branco (regra 10)

Use sempre que houver definição, conceito-chave ou texto em destaque.
**Nunca** texto amarelo sobre navy — sempre branco.

```xml
<p:sp>
  <p:nvSpPr><p:cNvPr id="1700" name="DefNavy"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="750000" y="2200000"/><a:ext cx="6850000" cy="900000"/></a:xfrm>
    <a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val 6500"/></a:avLst></a:prstGeom>
    <a:solidFill><a:srgbClr val="1B2A4A"/></a:solidFill>
    <a:ln><a:noFill/></a:ln>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="ctr" lIns="200000" rIns="200000" tIns="180000" bIns="180000"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="ctr"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="1600" b="1">
          <a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>
          <a:latin typeface="Arial Black"/>
        </a:rPr>
        <a:t>Texto da definição em destaque, sempre em branco sobre o navy.</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>
```

---

## 17c. Tabela "manual" com cabeçalho navy + linhas zebradas

Slide-fonte: `aula1_bloco1/slide38.xml`. Linhas como pares de `rect`,
sem gap (linhas coladas para parecer tabela).

```xml
<!-- Cabeçalho da coluna 1 (navy) -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="1800" name="TblHdrCol1"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="750000" y="1700000"/><a:ext cx="2034600" cy="360000"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
    <a:solidFill><a:srgbClr val="1B2A4A"/></a:solidFill>
    <a:ln><a:noFill/></a:ln>
  </p:spPr>
  <p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr lang="pt-BR"/></a:p></p:txBody>
</p:sp>
<!-- Texto do cabeçalho (branco sobre navy) -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="1801" name="TblHdrCol1Txt"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="845748" y="1760000"/><a:ext cx="1843200" cy="260100"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="ctr"/>
    <a:p><a:pPr algn="l"/>
      <a:r>
        <a:rPr lang="pt-BR" sz="1100" b="1">
          <a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>
          <a:latin typeface="Arial Black"/>
        </a:rPr>
        <a:t>Cabeçalho</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>

<!-- Linha 1 da coluna 1 (fundo branco) -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="1802" name="TblRow1Col1"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="750000" y="2060000"/><a:ext cx="2034600" cy="360000"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
    <a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>
    <a:ln><a:noFill/></a:ln>
  </p:spPr>
  <p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr lang="pt-BR"/></a:p></p:txBody>
</p:sp>
<!-- Linha 2 (fundo F4F4F4 - zebrado) -->
<!-- ... mesma estrutura, fill F4F4F4 a y=2420000 ... -->
```

Coordenadas das 4 colunas (Aula 1 B1 slide 38):
`x=750000` (col 1, cx=2034600), `x=2784636` (col 2, cx=1675500),
`x=4460218` (col 3, cx=1675500), `x=6135800` (col 4, cx=1735500).
Altura por linha: `360000`. Texto interno cx ligeiramente menor com
inset `~95748` x.

Para destacar valor semanticamente positivo/negativo na última coluna:
fill verde `#2D7D4F`, navy `#1B2A4A`, ou amarelo `#E8A317`.

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
