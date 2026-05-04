# ruff: noqa: E501
"""Gera o pptx de Aula 2 · Bloco 2 — Etapa 3 do Ciclo (Coletar).

Cobre o Bloco 2 completo do plano de ensino (Aula 2): fontes públicas
(DataJud, tribunais), internas e externas; tipos de coleta (manual, web
scraping, APIs); cuidados de LGPD; vieses de amostragem; construção
da base de 16.110 julgados de locação do TJSP; documentação da coleta;
e Atividade Prática 2 (3 questões, entrega até a Aula 3).

Reutiliza os helpers tipográficos e de geometria de
`build_aula2_bloco1.py`, aponta o deck para `/tmp/deck_aula2_bloco2/` e
adiciona dois construtores específicos do Bloco 2: `build_atividade_pratica`
(Atividade Prática N, 3 questões) e `build_encerramento_b2` (Fim da Aula N
com lembrete da atividade e gancho para a próxima aula).

Depois:
    uv run python .cursor/skills/build-aula-pptx/scripts/pack_pptx.py \
        /tmp/deck_aula2_bloco2/ aulas/aula_02/slides/aula2_bloco2_jurimetria.pptx
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS_DIR))

import build_aula2_bloco1 as a2b1  # noqa: E402

# Reaponta os globals do módulo importado para o deck deste bloco.
DECK = Path("/tmp/deck_aula2_bloco2")
a2b1.DECK = DECK
a2b1.SLIDES = DECK / "ppt/slides"
a2b1.RELS = a2b1.SLIDES / "_rels"
a2b1.CT = DECK / "[Content_Types].xml"
a2b1.PRES = DECK / "ppt/presentation.xml"
a2b1.PRES_RELS = DECK / "ppt/_rels/presentation.xml.rels"

from build_aula2_bloco1 import (  # noqa: E402
    CONTENT_W,
    CONTENT_X_MIN,
    END_X,
    GREY,
    LIGHT,
    NAVY,
    TEXT,
    WHITE,
    YELLOW,
    build_agenda,
    build_capa,
    build_card,
    build_comparacao,
    build_conceito,
    build_conexao_voltando,
    build_armadilhas,
    build_lista_numerada,
    build_objetivos,
    build_referencias,
    build_sintese,
    build_stat,
    build_tabela,
    build_transicao,
    canonical_header,
    ellipse,
    filled_rect,
    footer_citation,
    multi_para_box,
    save_slide,
    swap_media_para_aula1,
    text_box,
    update_content_types,
    update_presentation,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


# ---------------------------------------------------------------------------
# Construtores específicos do Bloco 2
# ---------------------------------------------------------------------------


def build_atividade_pratica(
    n: int,
    titulo: str,
    contexto: str,
    questoes: list[str],
    *,
    citation: str | None = None,
) -> None:
    """Slide de Atividade Prática (3 questões numeradas Q1, Q2, Q3).

    Estrutura: cabeçalho canônico + linha de contexto + 3 cards
    verticais com selo amarelo (Q1/Q2/Q3) + enunciado curto.
    """
    parts = canonical_header(
        titulo,
        "Compõe o Instrumento 1 (média das 4 atividades, peso 3,0)",
    )

    parts.append(
        text_box(
            50,
            CONTENT_X_MIN,
            1730000,
            CONTENT_W,
            340000,
            [
                {
                    "text": contexto,
                    "sz": 1300,
                    "i": True,
                    "color": GREY,
                    "font": "Arial",
                }
            ],
            anchor="t",
            align="l",
        )
    )

    card_h = 700000
    gap = 40000
    base_y = 2120000
    badge_w = 900000

    for i, q in enumerate(questoes[:3]):
        y = base_y + i * (card_h + gap)
        # Fundo do card (cinza claro com borda navy)
        parts.append(
            filled_rect(
                60 + i * 3,
                CONTENT_X_MIN,
                y,
                CONTENT_W,
                card_h,
                LIGHT,
                line=NAVY,
                line_w=12700,
                rounded=True,
            )
        )
        # Selo amarelo Q1/Q2/Q3
        parts.append(
            filled_rect(
                61 + i * 3,
                CONTENT_X_MIN + 60000,
                y + 60000,
                badge_w,
                card_h - 120000,
                YELLOW,
                rounded=True,
                text_runs=[
                    {
                        "text": f"Q{i + 1}",
                        "sz": 2000,
                        "b": True,
                        "color": WHITE,
                        "font": "Arial Black",
                    }
                ],
                text_align="ctr",
                text_anchor="ctr",
            )
        )
        # Enunciado da questão
        parts.append(
            text_box(
                62 + i * 3,
                CONTENT_X_MIN + 60000 + badge_w + 180000,
                y + 60000,
                CONTENT_W - badge_w - 320000,
                card_h - 120000,
                [
                    {
                        "text": q,
                        "sz": 1200,
                        "color": TEXT,
                        "font": "Arial",
                    }
                ],
                anchor="ctr",
                align="l",
            )
        )

    if citation:
        parts.append(footer_citation(90, citation))
    save_slide(n, "".join(parts), image=2)


def build_ponte_proxima_aula(
    n: int,
    proxima_aula_label: str,
    titulo_destaque: str,
    descricao_destaque: str,
    items: list[tuple[str, str]],
) -> None:
    """Ponte para a próxima aula (Bloco 2 → Aula seguinte).

    Mesmo layout visual do `build_ponte` (hero seta + 4 itens), mas
    com cabeçalho que aponta para a aula seguinte em vez do bloco.
    """
    parts = canonical_header(
        f"Ponte para a {proxima_aula_label}",
        "O que vem a seguir na próxima semana",
    )

    parts.append(
        text_box(
            50,
            750000,
            1585100,
            1500000,
            594900,
            [
                {
                    "text": "➜",
                    "sz": 6000,
                    "b": True,
                    "color": YELLOW,
                    "font": "Arial Black",
                }
            ],
            anchor="ctr",
            align="l",
        )
    )
    parts.append(
        text_box(
            51,
            2200000,
            1780000,
            4500000,
            400000,
            [
                {
                    "text": titulo_destaque,
                    "sz": 2000,
                    "b": True,
                    "color": NAVY,
                    "font": "Arial Black",
                }
            ],
            anchor="t",
            align="l",
        )
    )
    parts.append(
        text_box(
            52,
            2200000,
            2100000,
            4500000,
            399900,
            [
                {
                    "text": descricao_destaque,
                    "sz": 1250,
                    "color": GREY,
                    "font": "Arial",
                }
            ],
            anchor="t",
            align="l",
        )
    )

    y_positions = [2600000, 3030000, 3460000, 3890000]
    base_id = 53
    for i, (titulo_item, descricao_item) in enumerate(items[:4]):
        y = y_positions[i]
        parts.append(
            ellipse(
                base_id + i * 3,
                790000,
                y + 50000,
                197700,
                180000,
                YELLOW,
                text="",
            )
        )
        parts.append(
            text_box(
                base_id + i * 3 + 1,
                1075695,
                y,
                2637300,
                300000,
                [
                    {
                        "text": titulo_item,
                        "sz": 1250,
                        "color": NAVY,
                        "font": "Arial",
                    }
                ],
                anchor="t",
                align="l",
            )
        )
        parts.append(
            text_box(
                base_id + i * 3 + 2,
                3822762,
                y,
                3406500,
                300000,
                [
                    {
                        "text": descricao_item,
                        "sz": 1150,
                        "color": TEXT,
                        "font": "Arial",
                    }
                ],
                anchor="t",
                align="l",
            )
        )

    save_slide(n, "".join(parts), image=2)


def build_encerramento_b2(
    n: int,
    aula_n: int,
    lembrete_atividade: str,
    proxima_aula: str,
) -> None:
    """Encerramento da Aula N (fundo image1.png).

    Geometria espelhada do `build_encerramento_b1`, mas o texto principal
    abaixo da faixa amarela é o lembrete da atividade, e a linha cinza
    aponta para a próxima aula.
    """
    parts: list[str] = []
    parts.append(
        text_box(
            30,
            END_X,
            914400,
            5486400,
            731400,
            [
                {
                    "text": f"Fim da Aula {aula_n}",
                    "sz": 3600,
                    "b": True,
                    "color": NAVY,
                    "font": "Arial Black",
                }
            ],
            anchor="t",
            align="l",
        )
    )
    parts.append(filled_rect(31, END_X, 1691640, 1828800, 54900, YELLOW))
    parts.append(
        text_box(
            32,
            END_X,
            2391995,
            5486400,
            520000,
            [
                {
                    "text": lembrete_atividade,
                    "sz": 1800,
                    "color": YELLOW,
                    "font": "Arial",
                }
            ],
            anchor="t",
            align="l",
        )
    )
    parts.append(
        text_box(
            33,
            END_X - 5,
            2920000,
            5486400,
            360000,
            [
                {
                    "text": f"Próxima aula: {proxima_aula}",
                    "sz": 1300,
                    "color": GREY,
                    "font": "Arial",
                }
            ],
            anchor="t",
            align="l",
        )
    )
    save_slide(n, "".join(parts), image=1)


# ---------------------------------------------------------------------------
# Setup do deck
# ---------------------------------------------------------------------------


def unpack_layout_fresh() -> None:
    """Garante que /tmp/deck_aula2_bloco2/ é um unpack limpo do layout.pptx."""
    if DECK.exists():
        shutil.rmtree(DECK)
    layout = REPO_ROOT / "jurimetria/docs/templates/layout.pptx"
    unpack_script = REPO_ROOT / ".cursor/skills/build-aula-pptx/scripts/unpack_pptx.py"
    subprocess.run(
        [
            "uv",
            "run",
            "python",
            str(unpack_script),
            "--force",
            str(layout),
            str(DECK),
        ],
        check=True,
    )


# ---------------------------------------------------------------------------
# Construção do bloco
# ---------------------------------------------------------------------------


def main() -> None:
    unpack_layout_fresh()
    a2b1.SLIDES.mkdir(parents=True, exist_ok=True)
    a2b1.RELS.mkdir(parents=True, exist_ok=True)
    swap_media_para_aula1()

    # 1. Capa
    build_capa(
        1,
        "Aula 2 · Bloco 2",
        "O Ciclo da Ciência de Dados Aplicado ao Direito (Parte 1)",
        "Etapa 3: coletar com método, ética e cuidado com vieses",
    )

    # 2. Agenda
    build_agenda(
        2,
        [
            "Etapa 3: o que é coletar",
            "3 fontes: pública, interna, externa",
            "3 tipos: manual, scraping, API",
            "Web scraping e seus limites",
            "APIs públicas e DataJud",
            "LGPD e vieses de amostragem",
            "Como nasceu a base de 16.110 julgados",
            "Atividade Prática 2 e fechamento",
        ],
    )

    # 3. Objetivos
    build_objetivos(
        3,
        [
            ("Identificar", "as 3 grandes fontes de dados jurídicos no Brasil"),
            ("Distinguir", "coleta manual, web scraping e uso de APIs públicas"),
            ("Avaliar", "limites legais e éticos da coleta de dados judiciais"),
            ("Reconhecer", "vieses de amostragem comuns na prática jurídica"),
            ("Documentar", "uma coleta de modo reproduzível e defensável"),
        ],
    )

    # 4. Voltando do intervalo
    build_conexao_voltando(
        4,
        "Voltando do intervalo",
        "Da pergunta e do mapeamento à coleta",
        "No Bloco 1, saímos com uma pergunta investigável e uma tabela analítica mínima como destino.",
        [
            "Agora a tarefa é encher essa tabela com dados reais. É a Etapa 3 do ciclo.",
            "Coletar com método é o que separa um estudo jurimétrico defensável de uma planilha improvisada.",
            "Vamos ver fontes, tipos de coleta, limites legais e como construímos a base de 16.110 julgados do XY&A.",
        ],
        citation="Nunes (2019); CNJ (2024)",
    )

    # ---- Tópico 01: Etapa 3 e suas fontes ----

    # 5. Transição 01
    build_transicao(
        5,
        "01",
        "Etapa 3: coletar",
        "Onde estão os dados e como eles chegam até a tabela analítica",
    )

    # 6. O que é coletar
    build_conceito(
        6,
        "O que é coletar",
        [
            "Coletar é ir buscar, em fontes confiáveis, os valores que vão preencher cada coluna da tabela analítica desenhada na Etapa 2.",
            "É a etapa em que o plano vira dado. Por isso, depende diretamente da qualidade da pergunta e do mapeamento feitos antes.",
            "Coleta sem pergunta clara é pesca. E peixe demais na rede atrapalha tanto quanto peixe de menos.",
        ],
        citation="Nunes (2019); Wheelan (2016)",
    )

    # 7. Stat — Justiça em Números
    build_stat(
        7,
        "O universo a coletar",
        "84,8 mi",
        "processos em tramitação no Judiciário brasileiro em 2023, segundo o Justiça em Números do CNJ. Coletar é, antes de tudo, recortar.",
        citation="CNJ, Justiça em Números (2024)",
    )

    # 8. Coleta começa pela tabela
    build_card(
        8,
        "Coleta começa pela tabela",
        "Princípio: a tabela do Bloco 1 vira plano de coleta",
        [
            "Cada coluna da tabela analítica é uma busca a ser feita: qual fonte fornece esse dado, em que formato e com que cobertura.",
            "Cada linha é uma unidade de observação: tipicamente um processo, uma sentença ou um movimento processual.",
            "Sem essa correspondência tabela → fontes, a coleta vira improviso e a análise herda o improviso.",
        ],
        citation="Nunes (2019)",
    )

    # 9. Tabela — 3 fontes brasileiras
    build_tabela(
        9,
        "Três grandes fontes",
        ["Fonte", "Exemplos", "O que esperar"],
        [
            ["Pública", "DataJud (CNJ), JusBrasil, e-SAJ, PJe, painéis de tribunais", "Padronizada, com cobertura nacional, mas variável por tribunal"],
            ["Interna", "Sistema do escritório, planilhas de controle, e-mails", "Próxima da realidade do caso, porém pouco padronizada"],
            ["Externa", "IBGE, Receita Federal, Bacen, Censo, dados de mercado", "Contexto socioeconômico para enriquecer a base jurídica"],
        ],
        citation="CNJ (2024); ABJ (relatórios)",
        col_widths=[1300000, 2700000, 2950000],
    )

    # 10. Mini-caso XY&A: combinando fontes
    build_card(
        10,
        "Mini-caso XY&A",
        "Combinando fontes em uma única tabela",
        [
            "Fonte interna: planilhas do XY&A com número do processo, cliente e valor da causa estimado.",
            "Fonte pública: DataJud para classe, assunto, vara, datas de movimentos e desfecho oficial.",
            "Fonte externa: Bacen para corrigir valores históricos e IBGE para contextualizar comarcas.",
        ],
        citation="CNJ / DataJud (2024)",
    )

    # ---- Tópico 02: Tipos de coleta ----

    # 11. Transição 02
    build_transicao(
        11,
        "02",
        "Tipos de coleta",
        "Manual, web scraping e APIs públicas",
    )

    # 12. Conceito — 3 tipos
    build_conceito(
        12,
        "Três tipos de coleta",
        [
            "Manual: o operador lê e tabula processo a processo. Demorado, mas viável para o advogado sem programação.",
            "Web scraping: um programa visita páginas públicas e extrai informação. Acelera muito, exige cuidado técnico e jurídico.",
            "API: o tribunal ou órgão expõe os dados em formato estruturado e estável. É o caminho mais limpo, quando existe.",
        ],
        citation="Nunes (2019); CNJ (2024)",
    )

    # 13. Card — Coleta manual e amostragem
    build_card(
        13,
        "Coleta manual",
        "A saída do advogado sem programação",
        [
            "Faz sentido quando o número de processos é pequeno ou quando só uma fração da informação está em texto livre.",
            "Combine com amostragem aleatória, vista na Aula 1: 100 processos bem escolhidos podem responder mais que 10.000 mal lidos.",
            "Padronize a planilha de tabulação antes de começar. Toda mudança de critério no meio do caminho gera dado sujo.",
        ],
        citation="Wheelan (2016); Nunes (2019)",
    )

    # 14. Card — Web scraping
    build_card(
        14,
        "Web scraping",
        "Quando o tribunal não oferece API",
        [
            "Programa abre a página pública de consulta processual, lê o conteúdo e grava em uma tabela. Repete para milhares de processos.",
            "Útil para tribunais que ainda não publicam dados estruturados, mas cuja consulta processual é aberta.",
            "Não é mágica: páginas mudam, captchas aparecem, e o ritmo precisa ser respeitoso para não derrubar o serviço.",
        ],
        citation="Nunes (2019)",
    )

    # 15. Card — APIs públicas
    build_card(
        15,
        "APIs públicas",
        "O caminho mais limpo, quando existe",
        [
            "API é um endereço que devolve dados já organizados (JSON), em vez de uma página de consulta.",
            "DataJud, do CNJ, é a principal API jurídica brasileira hoje, com cobertura de todos os tribunais cadastrados.",
            "Tribunais como TJSP e TJRJ também publicam APIs próprias para consultas específicas, com regras de uso e limites.",
        ],
        citation="CNJ / DataJud (2024)",
    )

    # 16. Tabela — Quando cada tipo faz sentido
    build_tabela(
        16,
        "Quando cada tipo faz sentido",
        ["Cenário", "Recomendado", "Por quê"],
        [
            ["Até ~200 processos, com leitura de teor", "Manual + amostragem", "Volume cabe na mão; nuances exigem leitura"],
            ["Milhares, sem API, página pública", "Web scraping responsável", "API ausente, mas dado existe em HTML"],
            ["Cobertura nacional ou multi-tribunal", "API (DataJud)", "Padroniza colunas e evita raspar 90 sites"],
            ["Dado interno do escritório", "Exportação direta", "Já está em sistema próprio"],
        ],
        citation="CNJ (2024); ABJ (relatórios)",
        col_widths=[2400000, 1700000, 2850000],
    )

    # ---- Tópico 03: Scraping e APIs em detalhe ----

    # 17. Transição 03
    build_transicao(
        17,
        "03",
        "Scraping e APIs",
        "Como funcionam, quando valem a pena, quais os limites",
    )

    # 18. Conceito — Web scraping na prática
    build_conceito(
        18,
        "Web scraping na prática",
        [
            "Um robô abre a consulta processual pública, identifica os campos de interesse (vara, partes, datas) e copia para uma planilha.",
            "Para o advogado, raramente é trabalho de fazer sozinho. Mais comum: contratar um time técnico ou uma plataforma especializada.",
            "Mesmo terceirizada, a coleta é responsabilidade do escritório: o que entra na base define a qualidade de tudo que vier depois.",
        ],
        citation="Nunes (2019); ABJ (relatórios)",
    )

    # 19. Armadilhas — Cuidados no scraping
    build_armadilhas(
        19,
        "Cuidados ao raspar dados públicos",
        [
            (
                "Termos de uso e robots.txt",
                "Páginas públicas podem proibir coleta automatizada. Verifique termos de uso e o arquivo robots.txt antes de raspar.",
            ),
            (
                "Ritmo e impacto",
                "Raspar rápido demais derruba o serviço público. Use intervalos, paralelismo moderado e identificação clara do robô.",
            ),
            (
                "Dados sensíveis pelo caminho",
                "Mesmo em consulta pública, segredo de justiça e dados de pessoas físicas exigem filtros antes de armazenar e compartilhar.",
            ),
        ],
        citation="LGPD, Lei 13.709/2018; CNJ (2024)",
    )

    # 20. Conceito — APIs públicas no Direito
    build_conceito(
        20,
        "APIs públicas no Direito brasileiro",
        [
            "DataJud é a base nacional de dados do Poder Judiciário, mantida pelo CNJ, com microdados de processos de quase todos os tribunais.",
            "Permite filtrar por tribunal, classe processual, assunto, datas e movimentos, com cadastro prévio e respeito aos limites de consulta.",
            "Painéis derivados, como o Justiça em Números, mostram o agregado, mas a API entrega o microdado para análise jurimétrica própria.",
        ],
        citation="CNJ / DataJud (2024)",
    )

    # 21. Stat — DataJud
    build_stat(
        21,
        "DataJud em números",
        "+90",
        "tribunais brasileiros publicam microdados processuais via DataJud, viabilizando estudos jurimétricos de cobertura nacional.",
        citation="CNJ, DataJud (2024)",
    )

    # 22. Comparação — Scraping x API
    build_comparacao(
        22,
        "Scraping vs. API",
        "Web scraping",
        [
            "Funciona quando não há API.",
            "Frágil: muda o site, quebra a coleta.",
            "Custo técnico recorrente.",
            "Limites legais e éticos a respeitar.",
        ],
        "API pública",
        [
            "Estável e estruturada.",
            "Dados padronizados, prontos para tabela.",
            "Cobertura definida pelo provedor.",
            "Cadastro e regras de uso explícitas.",
        ],
        citation="CNJ (2024); ABJ (relatórios)",
    )

    # ---- Tópico 04: Ética, LGPD e vieses ----

    # 23. Transição 04
    build_transicao(
        23,
        "04",
        "Ética, LGPD e vieses",
        "O que coletar com responsabilidade exige do advogado",
    )

    # 24. Conceito — LGPD na coleta jurídica
    build_conceito(
        24,
        "LGPD para o jurimetrista",
        [
            "A LGPD se aplica a dados pessoais, mesmo quando vêm de fontes públicas como tribunais. Ser público não é sinônimo de ser livre para qualquer uso.",
            "Tratamento legítimo exige base legal, finalidade clara, limitação ao necessário e cuidados de segurança no armazenamento.",
            "Para advogados, o exercício regular do direito e o cumprimento de obrigação legal são bases típicas, mas pesquisa e estudo jurimétrico exigem análise específica.",
        ],
        citation="LGPD, Lei 13.709/2018; CNJ (2024)",
    )

    # 25. Armadilhas — 3 cuidados LGPD
    build_armadilhas(
        25,
        "Três cuidados práticos",
        [
            (
                "Anonimizar quando possível",
                "Para análises agregadas (taxas, médias por vara), nomes de partes não agregam valor. Substitua por identificadores antes de compartilhar.",
            ),
            (
                "Finalidade declarada",
                "Coletar para gestão da carteira é finalidade. Coletar para depois decidir o que fazer não é. Documente a finalidade antes da coleta.",
            ),
            (
                "Compartilhamento controlado",
                "Bases jurimétricas circulam por e-mail e nuvem com facilidade. Trate a base como peça processual: acesso restrito e log de quem acessou.",
            ),
        ],
        citation="LGPD, Lei 13.709/2018",
    )

    # 26. Conceito — Vieses de amostragem
    build_conceito(
        26,
        "Vieses de amostragem",
        [
            "Viés de amostragem aparece quando a base que temos não representa o universo sobre o qual queremos concluir.",
            "Muitas vezes não está nos dados em si, e sim em como foram coletados: que processos chegam ao escritório, que decisões aparecem em painel, que casos viram notícia.",
            "Em juízo, é o equivalente a usar prova testemunhal selecionada apenas pelo lado que convém. O resultado parece sólido, mas não sustenta análise crítica.",
        ],
        citation="Huff (2016); Silver (2013)",
    )

    # 27. Armadilhas — 3 vieses clássicos
    build_armadilhas(
        27,
        "Três vieses clássicos na coleta jurídica",
        [
            (
                "Viés de seleção",
                "A carteira do escritório é resultado de captação, não amostra aleatória do TJSP. Conclusões valem para a carteira, não para o tribunal inteiro.",
            ),
            (
                "Viés de sobrevivência",
                "Análise só sobre casos transitados em julgado ignora os ainda em curso, que podem ter perfil diferente. A média do que terminou não é a média do que existe.",
            ),
            (
                "Viés de publicação",
                "Decisões que viram acórdão e aparecem em painel não são uma amostra neutra. Sentenças de 1º grau, especialmente as não recorridas, somem do radar.",
            ),
        ],
        citation="Huff (2016); Silver (2013); Nunes (2019)",
    )

    # 28. Mini-caso XY&A — Viés na carteira
    build_card(
        28,
        "Mini-caso XY&A",
        "Viés escondido na carteira de renovatórias",
        [
            "Sócio do XY&A afirma: nossa taxa de êxito em renovatória é alta, então o tribunal tende a favorecer locador.",
            "Viés de seleção: os 13.201 processos de renovatória do XY&A vêm de clientes que já chegaram dispostos a litigar, não de uma amostra aleatória do TJSP.",
            "Conclusão correta: a taxa é da carteira do XY&A. Para inferir sobre o tribunal, é preciso comparar com a base nacional, vinda do DataJud.",
        ],
        citation="Huff (2016); CNJ (2024)",
    )

    # ---- Tópico 05: Construindo a base TJSP ----

    # 29. Transição 05
    build_transicao(
        29,
        "05",
        "Como nasceu a base",
        "16.110 julgados de locação do TJSP, 2010 a 2024",
    )

    # 30. Card — Critérios da base
    build_card(
        30,
        "Critérios da base do trabalho final",
        "Decisões de coleta que definem a população analítica",
        [
            "Tribunal: TJSP. Recorte permite comparar comarcas e varas dentro de um mesmo regime processual.",
            "Matéria: ações de revisão de aluguel e renovatória de locação, com a parte figurando como pessoa jurídica.",
            "Período: 2010 a 2024. Cobre dois ciclos econômicos relevantes para o mercado de locação comercial.",
            "Natureza: a base é tratada como população completa para fins do exercício, não como amostra.",
        ],
        citation="CNJ / DataJud (2024); TJSP",
    )

    # 31. Tabela — Filtros aplicados
    build_tabela(
        31,
        "Filtros aplicados na coleta",
        ["Filtro", "Valor", "Por quê"],
        [
            ["Tribunal", "TJSP", "Maior volume de locação comercial do país"],
            ["Classe", "Revisão e renovatória", "Foco da carteira XY&A"],
            ["Parte", "Pessoa jurídica", "Recorte do contencioso de massa do XY&A"],
            ["Período", "2010 a 2024", "15 anos cobrem ciclos de mercado"],
            ["Status", "Com sentença", "Permite analisar desfecho"],
        ],
        citation="CNJ / DataJud (2024); TJSP",
        col_widths=[1500000, 1900000, 3550000],
    )

    # 32. Lista numerada — Checklist de documentação
    build_lista_numerada(
        32,
        "Checklist de documentação da coleta",
        [
            "Fonte: nome do sistema ou API consultada e data de extração.",
            "Filtros: cada parâmetro aplicado, com o valor exato.",
            "Volume: total bruto coletado e total final após limpeza.",
            "Exclusões: critérios de descarte e quantos casos foram descartados.",
            "Limitações: o que a base permite e o que ela não permite responder.",
        ],
        citation="Nunes (2019); CNJ (2024)",
        accent="Reproduzível e defensável: o que registrar antes de analisar",
    )

    # 33. Card — Quando a pergunta muda no caminho
    build_card(
        33,
        "Quando a pergunta muda no caminho",
        "Replanejar é parte do método",
        [
            "Acontece: durante a coleta, surgem variáveis novas, ou a pergunta original se mostra inviável com os dados disponíveis.",
            "Não vale ajustar a pergunta para encaixar no que já se tem. Isso é torcer o teste para concluir o que se queria.",
            "Vale registrar a mudança no caderno da coleta, refazer o mapeamento da Etapa 2 e voltar ao plano com a pergunta nova.",
        ],
        citation="Nunes (2019); Silver (2013)",
    )

    # ---- Fechamento ----

    # 34. Exercício dirigido em sala
    build_card(
        34,
        "Exercício dirigido em sala",
        "10 minutos · em duplas",
        [
            "Retomem a pergunta investigável escolhida no Bloco 1 (slide 22 do bloco anterior, ou nova).",
            "Para cada variável da tabela analítica, indiquem fonte (interna XY&A, DataJud, scraping) e tipo de coleta (manual, automatizada).",
            "Apontem 1 risco de LGPD e 1 risco de viés que vocês teriam que vigiar nessa coleta.",
        ],
    )

    # 35. Síntese
    build_sintese(
        35,
        [
            "Coletar é encher de dado real a tabela analítica desenhada na Etapa 2.",
            "Três fontes (pública, interna, externa) e três tipos (manual, scraping, API) cobrem o repertório.",
            "DataJud é o caminho mais limpo para coleta multi-tribunal no Brasil.",
            "LGPD e vieses de amostragem são vigias permanentes da Etapa 3.",
            "Documentar a coleta hoje é o que defende a análise amanhã.",
        ],
    )

    # 36. Atividade Prática 2
    build_atividade_pratica(
        36,
        "Atividade Prática 2 (entrega até a Aula 3)",
        "Aplique as Etapas 1 a 3 do ciclo a uma pergunta para o trabalho final do grupo.",
        [
            "Q1. Escreva uma pergunta investigável sobre a base de locação do TJSP, com tema, recorte (período e jurisdição), variável central e ponto de comparação.",
            "Q2. Esboce a tabela analítica mínima da Etapa 2: 1 linha por processo e ao menos 5 colunas, classificando cada coluna como categórica, numérica ou temporal.",
            "Q3. Monte um plano de coleta de no máximo 5 linhas: para cada variável, qual fonte (interna, DataJud, scraping) e 1 cuidado de LGPD ou de viés a vigiar.",
        ],
        citation="Nunes (2019); CNJ (2024); LGPD",
    )

    # 37. Ponte para Aula 3
    build_ponte_proxima_aula(
        37,
        "Aula 3",
        "Da coleta à análise",
        "Percorremos as Etapas 4, 5 e 6 do ciclo no Excel, sobre a base de 16.110 julgados.",
        [
            ("Etapa 4: tratar", "Padronizar datas, valores, categorias e textos da base."),
            ("Etapa 5: analisar", "Estatística descritiva no Excel, com tabelas dinâmicas."),
            ("Etapa 6: apresentar", "Gráficos certos para responder cada tipo de pergunta."),
            ("Atividade 2 corrigida", "Em sala, no início do Bloco 1 da Aula 3."),
        ],
    )

    # 38. Referências
    build_referencias(
        38,
        [
            "NUNES, Marcelo Guedes. Jurimetria: como a estatística pode reinventar o Direito. 2. ed. São Paulo: Revista dos Tribunais, 2019.",
            "WHEELAN, Charles. Estatística: o que é, para que serve, como funciona. Rio de Janeiro: Zahar, 2016.",
            "HUFF, Darrell. Como mentir com estatística. Rio de Janeiro: Intrínseca, 2016.",
            "SILVER, Nate. O sinal e o ruído. Rio de Janeiro: Intrínseca, 2013.",
            "CONSELHO NACIONAL DE JUSTIÇA (CNJ). Justiça em Números e DataJud, 2024. Disponível em cnj.jus.br.",
            "BRASIL. Lei nº 13.709, de 14 de agosto de 2018. Lei Geral de Proteção de Dados Pessoais (LGPD).",
            "ASSOCIAÇÃO BRASILEIRA DE JURIMETRIA (ABJ). Relatórios e publicações em abj.org.br.",
            "KATZ, Daniel Martin; BOMMARITO, Michael J. Quantitative Legal Prediction. Emory Law Journal, v. 62, 2013.",
            "SUSSKIND, Richard. Tomorrow's Lawyers. 3rd ed. Oxford University Press, 2023.",
        ],
    )

    # 39. Fim da Aula 2
    build_encerramento_b2(
        39,
        aula_n=2,
        lembrete_atividade="Atividade Prática 2 · entrega até a Aula 3",
        proxima_aula="Aula 3 · Tratar, analisar e apresentar (Etapas 4 a 6)",
    )

    update_content_types(39)
    update_presentation(39)
    print("OK 39 slides gerados.")


if __name__ == "__main__":
    main()
