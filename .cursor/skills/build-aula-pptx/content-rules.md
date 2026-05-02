# Regras de conteúdo

## Títulos e rótulos padronizados

Use **exatamente** os mesmos títulos de slide da Aula 1 para os tipos
canônicos, salvo correção explícita do professor. Exemplos: **Agenda do
Bloco**, **Objetivos de Aprendizagem**, **Atividade Prática N**,
**Referências do bloco**. A lista completa e o layout associado estão em
[`layout-canonical.md`](layout-canonical.md).

## Fidelidade ao plano

Todos os itens listados no bloco dentro de `docs/plano_curso.docx`
(seção "Cronograma Detalhado das Aulas") devem aparecer, **na ordem
sugerida**. Você pode expandir, exemplificar e intercalar slides
adicionais, mas:

- não pode **omitir** tópicos;
- não pode **reordenar** a sequência pedagógica;
- não pode trocar conceitos do plano por sinônimos sem checar com o usuário.

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

- Quando usar números/percentuais reais (CNJ, TJSP, ABJ), traga ano e
  fonte explícitos.
- Ao apresentar testes de hipóteses ou modelos preditivos, sempre faça
  a **analogia jurídica** antes da definição estatística.
- Ao mostrar pipeline com IA (Aula 5), explicite onde o operador humano
  decide e onde a IA acelera. A IA nunca substitui análise crítica.
- Termos em inglês (`p-value`, `feature`, `outlier`) devem ter glosa
  curta em português na primeira menção.
