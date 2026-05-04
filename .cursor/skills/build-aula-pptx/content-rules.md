# Regras de conteúdo

## Títulos e rótulos padronizados

Use **exatamente** os mesmos títulos de slide da Aula 1 para os tipos
canônicos, salvo correção explícita do professor. Exemplos: **Agenda do
Bloco**, **Objetivos de Aprendizagem**, **Atividade Prática N**,
**Referências do bloco**. A lista completa e o layout associado estão em
[`layout-canonical.md`](layout-canonical.md).

## Fidelidade ao plano (regra 9)

Todos os itens listados no bloco dentro de `docs/plano_curso.docx`
(seção "Cronograma Detalhado das Aulas") devem aparecer, **na ordem
sugerida**. Você pode expandir, exemplificar e intercalar slides
adicionais, mas:

- não pode **omitir** tópicos;
- não pode **reordenar** a sequência pedagógica;
- não pode trocar conceitos do plano por sinônimos sem checar com o usuário.

## Mini-casos práticos antes da formalização (regra 9)

Toda vez que um método novo for introduzido, **apresente antes um
mini-caso prático** que torne a intuição concreta. A formalização
estatística/matemática vem **depois** do mini-caso, não antes. Esta
ordem é regra da disciplina (público de advogados sem formação
matemática) e está em todas as aulas do gold standard.

### Exemplos canônicos do professor (replicar fielmente quando aplicável)

| Conteúdo do plano | Mini-caso de abertura | Pivô para a teoria |
|---|---|---|
| **Testes de hipóteses (Aula 4)** | Lançar uma moeda 10 vezes (5 caras × 5 coroas: a moeda é honesta?) versus lançar 10.000 vezes (5.123 caras × 4.877 coroas: e agora?). | Mostra intuitivamente que **tamanho da amostra** muda a confiança da decisão. Daí define `H0`, `H1`, `p-value`, "ônus da prova estatístico". |
| **Modelos estatísticos de desfecho, tempo e valor (Aula 4)** | Caso "real" do escritório que reduziu **R$ 12 mi de provisão** após substituir intuição por modelo combinado de probabilidade de êxito × tempo médio de tramitação × valor esperado da condenação. | Mostra o **impacto financeiro** de provisionamento estratégico apoiado em modelos. Daí entra o aparato técnico (regressão logística, sobrevivência, regressão linear). |
| **Falácia do promotor (armadilhas estatísticas)** | Caso Sally Clark (Reino Unido, 1999): morte súbita de dois bebês, condenação errada por inversão de probabilidades condicionais. | Mostra o custo concreto de errar `P(prova\|inocência)` por `P(inocência\|prova)`. Daí entra Bayes. |
| **Paradoxo de Simpson** | Admissões de pós-graduação Berkeley 1973: agregado mostra discriminação contra mulheres, mas por departamento o efeito some ou se inverte. | Mostra que **agregação esconde a verdade**. Daí entra estratificação e variável de confusão. |
| **Distinção população × amostra** | Slide 43 do gold standard (Aula 1 B1): "ônus da prova × ônus da amostragem". O juiz decide sobre fatos que não presenciou; o analista conclui sobre casos que não leu um a um. | Analogia jurídica direta. Daí entra inferência estatística. |
| **IA generativa no Direito (Aula 5)** | Demonstração ao vivo: pedir resumo de processo a um chatbot e pedir o mesmo a um RAG conectado à base TJSP. Comparar acertos e alucinações. | Mostra **onde** a IA acelera e **onde** o operador humano decide. Daí entra o pipeline (chat / RAG / output estruturado / agentes / dashboards). |

Sempre que possível, traga **um caso concreto com cifras reais** ou
inspirado em escritórios reais. Quando não houver caso real, use o
escritório fictício **XY&A** (perfil na seção 7 do plano), já calibrado
para a disciplina.

### Estrutura recomendada para um mini-caso

1. **Slide 1 do bloco-mini-caso:** descrição do caso em 2 a 4 bullets (situação, conflito, pergunta).
2. **Slide 2:** dado quantitativo central do caso (stat callout — número grande amarelo + label cinza).
3. **Slide 3:** resolução intuitiva (sem fórmulas), apenas o raciocínio.
4. **Slide 4 em diante:** formalização (a teoria que o método representa).

## Caso XY&A como fio condutor

Sempre que couber, traga exemplos e menções ao escritório fictício
**X, Y & Associados (XY&A)** (perfil na seção 7 do plano) e à base real
de **16.110 julgados de revisão e renovatória de locação do TJSP
(2010–2024)** (seção 8). XY&A é o cenário recorrente das atividades em
sala e o pano de fundo do trabalho final.

## Registro de língua

- **Português do Brasil**, formal-didático.
- Sem gerundismo excessivo, sem jargão estatístico/computacional
  desnecessário.
- Público: advogados **sem formação matemática ou em programação**.
  Toda quantificação precisa vir com analogia jurídica (ônus da prova,
  presunção, padrão de prova, etc.).
- Speaker notes (`notesSlideN.xml`) recomendados em slides densos com
  pontos de fala que o professor possa usar.

## PROIBIÇÃO DE TRAVESSÕES NO TEXTO DOS SLIDES

**Em nenhuma hipótese** use travessões (`—` U+2014, `–` U+2013) ou hífens
como **separador parentético** no conteúdo dos slides. Vale para corpo,
títulos, subtítulos, legendas, bullets e speaker notes. Travessão é
marcação característica de texto gerado por IA.

### O que NÃO fazer

- ❌ "A Jurimetria — campo que aplica ciência de dados ao Direito — nasceu nos anos 1960."
- ❌ "O ciclo tem 6 etapas – a primeira é transformar a pergunta – e deve ser percorrido na ordem."
- ❌ "XY&A - escritório fictício usado em sala - tem 16.110 processos."

### Como reescrever corretamente

- ✅ **Vírgulas:** "A Jurimetria, campo que aplica ciência de dados ao Direito, nasceu nos anos 1960."
- ✅ **Parênteses:** "A Jurimetria (campo que aplica ciência de dados ao Direito) nasceu nos anos 1960."
- ✅ **Duas frases:** "A Jurimetria é o campo que aplica ciência de dados ao Direito. Ela nasceu nos anos 1960."
- ✅ **Dois pontos** quando há introdução de explicação: "O ciclo tem 6 etapas. A primeira: transformar a pergunta."

### Usos legítimos e permitidos

- Intervalos numéricos com `–`: `2010–2024`, `3–5 objetivos`, `14–18pt`.
- Hífen em palavra composta: `teórico-prática`, `passo a passo`.
- Travessão de diálogo (não ocorre nesta disciplina).

Antes de empacotar, rode `check_no_emdash.py` (ver skill `pptx-qa`) e
substitua **toda** ocorrência fora dos usos legítimos.

## Referência bibliográfica em cada conceito relevante

Todo **conceito**, **método**, **armadilha estatística**, **marco
histórico** ou **afirmação quantitativa** apresentado deve trazer a
referência bibliográfica de origem **junto do conceito**, no slide em
que ele é introduzido. Não basta concentrar tudo no slide final.

### Forma de citação dentro do slide

- Em legenda discreta no rodapé interno do slide.
- Tamanho 10–12pt, cor cinza `#666666`, itálico.
- Formato curto: `Autor (ano)` ou `Órgão (ano)`.
  - Exemplos: `Nunes (2019)`, `CNJ (2024)`, `Huff (2016)`,
    `Katz e Bommarito (2013)`.
- Mais de uma fonte no mesmo slide → separar por ponto e vírgula:
  `Nunes (2019); ABJ (2023)`.

### Tabela de citações esperadas (não exaustiva)

| Conceito introduzido | Citação esperada |
|----------------------|------------------|
| Definição de Jurimetria, histórico, ABJ | Nunes (2019); Zabala e Silveira (2014) |
| Previsão jurídica quantitativa, modelos preditivos no Direito | Katz e Bommarito (2013) |
| Falácia do promotor, paradoxo de Simpson, armadilhas estatísticas | Huff (2016); Silver (2013) |
| Estatística descritiva, média, mediana, distribuições | Wheelan (2016) |
| Justiça em Números, DataJud, painéis do Judiciário | CNJ (relatórios e painéis) |
| Futuro da advocacia, tecnologia jurídica | Susskind (2023) |
| Inferência, regressão logística, sobrevivência (base teórica) | James et al. (2021) — ISLR |
| IA generativa (Claude, Claude Code, ChatGPT, Codex) | Documentação oficial Anthropic / OpenAI |

### Slide consolidado de referências

Mantém-se obrigatório (item 10 da macroestrutura). Lista **todas** as
referências usadas no bloco em formato ABNT-like. Não repete as menções
discretas dos slides anteriores; é a consolidação.

### Quando NÃO precisa citar

- Slide de agenda do bloco.
- Síntese final do bloco (sem novo conceito).
- Exercícios práticos sobre XY&A.
- Slide de objetivos de aprendizagem.
- Menções internas ao caso XY&A (que é fictício, criado para a disciplina).

## Cuidados específicos da disciplina

- **Referências reais sempre que possível (regra 6).** Quando usar
  números/percentuais reais (CNJ, TJSP, ABJ), traga ano e fonte
  explícitos no rodapé do slide. Não invente números. Quando for
  hipotético (caso XY&A), deixe claro que é cenário ilustrativo.
- Ao apresentar testes de hipóteses ou modelos preditivos, sempre faça
  a **analogia jurídica** antes da definição estatística.
- Ao mostrar pipeline com IA (Aula 5), explicite onde o operador humano
  decide e onde a IA acelera. A IA nunca substitui análise crítica.
- Termos em inglês (`p-value`, `feature`, `outlier`) devem ter glosa
  curta em português na primeira menção.
