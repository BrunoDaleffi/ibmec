# ruff: noqa: E501
"""Gera o pptx de Aula 3 · Bloco 2 — O Ciclo da Ciência de Dados (Parte 2).

Layout canônico replicado da Aula 1 publicada (ver
`.cursor/skills/build-aula-pptx/layout-canonical.md`).

Convenção de fundos:
- image1.png → capa, transição de tópico (01, 02, …) e encerramento ("Fim da Aula N").
- image2.png → todos os demais slides (agenda, objetivos, conexão, conteúdo,
  síntese, ponte, referências, exercícios dirigidos).

O `layout.pptx` original tem o mapeamento invertido tanto nas rels quanto nos
arquivos de mídia em si: o que está salvo como `image1.png` é o fundo "suave"
(conteúdo) e o que está salvo como `image2.png` é o fundo "forte" (capa). Para
alinhar à convenção da Aula 1 publicada (image1=capa/transição/fim,
image2=conteúdo), `swap_media_para_aula1()` troca os dois arquivos físicos no
deck desempacotado antes da geração dos slides.

Pré-requisito: rodar antes
    uv run python .cursor/skills/build-aula-pptx/scripts/unpack_pptx.py \
        docs/templates/layout.pptx /tmp/deck_aula3_bloco2/

Depois:
    uv run python .cursor/skills/build-aula-pptx/scripts/pack_pptx.py \
        /tmp/deck_aula3_bloco2/ aulas/aula_03/slides/aula3_bloco2_jurimetria.pptx
"""

from __future__ import annotations

import re
from pathlib import Path

DECK = Path("/tmp/deck_aula3_bloco2")
SLIDES = DECK / "ppt/slides"
RELS = SLIDES / "_rels"
CT = DECK / "[Content_Types].xml"
PRES = DECK / "ppt/presentation.xml"
PRES_RELS = DECK / "ppt/_rels/presentation.xml.rels"

XML_HEADER = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
    'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
)
XML_FOOTER = "<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>"

BG_BLOCK = (
    '<p:cSld><p:bg><p:bgPr><a:blipFill><a:blip r:embed="rId3">'
    "<a:alphaModFix/></a:blip><a:stretch><a:fillRect/></a:stretch>"
    "</a:blipFill></p:bgPr></p:bg>"
)
TREE_OPEN = (
    "<p:spTree>"
    '<p:nvGrpSpPr><p:cNvPr id="1" name="grp"/>'
    "<p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>"
    '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
    '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
)
TREE_CLOSE = "</p:spTree></p:cSld>"

# Paleta canônica
NAVY = "1B2A4A"
YELLOW = "E8A317"
GREY = "666666"
TEXT = "333333"
LIGHT = "F4F4F4"
PASTEL = "FCE5CD"
WHITE = "FFFFFF"

# Cabeçalho padrão da Aula 1 (slides estruturais)
H1_X = 750000
H1_Y = 500000
H1_W = 5950000
H1_H = 900000
H1_SZ = 2400

FAIXA_X = 750005
FAIXA_Y = 905100
FAIXA_W = 1500000
FAIXA_H = 54900

SUB_X = 750000
SUB_Y = 1330000
SUB_W = 5950000
SUB_H = 400000
SUB_SZ = 1400

CONTENT_X_MIN = 750000
CONTENT_X_MAX = 6700000
CONTENT_W = CONTENT_X_MAX - CONTENT_X_MIN  # 5950000
CONTENT_Y_MIN = 1700000
CONTENT_Y_MAX = 4500000

# Eixo de capa, transição e encerramento (alinhado à área branca específica)
HERO_X = 1097275
END_X = 822950


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------------------------------------------------------------------
# Primitivas de forma
# ---------------------------------------------------------------------------


def text_box(
    sp_id: int,
    x: int,
    y: int,
    cx: int,
    cy: int,
    runs: list[dict],
    *,
    anchor: str = "t",
    align: str = "l",
    bullet: str | None = None,
    bullet_color: str = YELLOW,
    line_spc: int = 100000,
    para_spc_before: int = 0,
) -> str:
    bul = ""
    if bullet:
        bul = (
            f'<a:buClr><a:srgbClr val="{bullet_color}"/></a:buClr>'
            f'<a:buFont typeface="Arial"/>'
            f'<a:buChar char="{bullet}"/>'
        )
    else:
        bul = "<a:buNone/>"

    para_pieces = []
    for r in runs:
        t = esc(r["text"])
        sz = r.get("sz", 1600)
        b = "1" if r.get("b") else "0"
        i = "1" if r.get("i") else "0"
        color = r.get("color", TEXT)
        font = r.get("font", "Arial")
        para_pieces.append(
            f'<a:r><a:rPr lang="pt-BR" sz="{sz}" b="{b}" i="{i}">'
            f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
            f'<a:latin typeface="{font}"/>'
            f'<a:ea typeface="{font}"/>'
            f'<a:cs typeface="{font}"/>'
            f"</a:rPr><a:t>{t}</a:t></a:r>"
        )
    paragraph = (
        f'<a:p><a:pPr lvl="0" marL="{285750 if bullet else 0}" '
        f'indent="{-285750 if bullet else 0}" algn="{align}">'
        f'<a:lnSpc><a:spcPct val="{line_spc}"/></a:lnSpc>'
        f'<a:spcBef><a:spcPts val="{para_spc_before}"/></a:spcBef>'
        f"{bul}</a:pPr>" + "".join(para_pieces) + "</a:p>"
    )

    return (
        f'<p:sp><p:nvSpPr><p:cNvPr id="{sp_id}" name="tb{sp_id}"/>'
        f'<p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/>'
        f'<a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
        f"<a:noFill/></p:spPr>"
        f'<p:txBody><a:bodyPr wrap="square" anchor="{anchor}" '
        f'lIns="91440" rIns="91440" tIns="45720" bIns="45720"/>'
        f"<a:lstStyle/>"
        f"{paragraph}</p:txBody></p:sp>"
    )


def multi_para_box(
    sp_id: int,
    x: int,
    y: int,
    cx: int,
    cy: int,
    paragraphs: list[list[dict]],
    *,
    anchor: str = "t",
    align: str = "l",
    bullet: str | None = None,
    bullet_color: str = YELLOW,
    line_spc: int = 110000,
    para_spc_before: int = 400,
) -> str:
    bul = ""
    if bullet:
        bul = (
            f'<a:buClr><a:srgbClr val="{bullet_color}"/></a:buClr>'
            f'<a:buFont typeface="Arial"/>'
            f'<a:buChar char="{bullet}"/>'
        )
    else:
        bul = "<a:buNone/>"

    p_xml: list[str] = []
    for runs in paragraphs:
        rs = []
        for r in runs:
            t = esc(r["text"])
            sz = r.get("sz", 1600)
            b = "1" if r.get("b") else "0"
            i = "1" if r.get("i") else "0"
            color = r.get("color", TEXT)
            font = r.get("font", "Arial")
            rs.append(
                f'<a:r><a:rPr lang="pt-BR" sz="{sz}" b="{b}" i="{i}">'
                f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
                f'<a:latin typeface="{font}"/>'
                f'<a:ea typeface="{font}"/>'
                f'<a:cs typeface="{font}"/>'
                f"</a:rPr><a:t>{t}</a:t></a:r>"
            )
        p_xml.append(
            f'<a:p><a:pPr lvl="0" marL="{285750 if bullet else 0}" '
            f'indent="{-285750 if bullet else 0}" algn="{align}">'
            f'<a:lnSpc><a:spcPct val="{line_spc}"/></a:lnSpc>'
            f'<a:spcBef><a:spcPts val="{para_spc_before}"/></a:spcBef>'
            f"{bul}</a:pPr>" + "".join(rs) + "</a:p>"
        )

    return (
        f'<p:sp><p:nvSpPr><p:cNvPr id="{sp_id}" name="tb{sp_id}"/>'
        f'<p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/>'
        f'<a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
        f"<a:noFill/></p:spPr>"
        f'<p:txBody><a:bodyPr wrap="square" anchor="{anchor}" '
        f'lIns="91440" rIns="91440" tIns="45720" bIns="45720"/>'
        f"<a:lstStyle/>" + "".join(p_xml) + "</p:txBody></p:sp>"
    )


def filled_rect(
    sp_id: int,
    x: int,
    y: int,
    cx: int,
    cy: int,
    fill: str,
    *,
    line: str | None = None,
    line_w: int = 9525,
    rounded: bool = False,
    text_runs: list[dict] | None = None,
    text_align: str = "l",
    text_anchor: str = "ctr",
    multi_paragraphs: list[list[dict]] | None = None,
) -> str:
    geom = (
        '<a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val 6500"/></a:avLst></a:prstGeom>'
        if rounded
        else '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
    )
    line_xml = (
        f'<a:ln w="{line_w}"><a:solidFill><a:srgbClr val="{line}"/></a:solidFill></a:ln>'
        if line
        else "<a:ln><a:noFill/></a:ln>"
    )

    body_inner = '<a:p><a:endParaRPr lang="pt-BR"/></a:p>'
    if multi_paragraphs:
        ps = []
        for runs in multi_paragraphs:
            rs = []
            for r in runs:
                t = esc(r["text"])
                sz = r.get("sz", 1600)
                b = "1" if r.get("b") else "0"
                i = "1" if r.get("i") else "0"
                color = r.get("color", TEXT)
                font = r.get("font", "Arial")
                rs.append(
                    f'<a:r><a:rPr lang="pt-BR" sz="{sz}" b="{b}" i="{i}">'
                    f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
                    f'<a:latin typeface="{font}"/>'
                    f"</a:rPr><a:t>{t}</a:t></a:r>"
                )
            ps.append(
                f'<a:p><a:pPr algn="{text_align}">'
                f'<a:lnSpc><a:spcPct val="110000"/></a:lnSpc>'
                f'<a:spcBef><a:spcPts val="200"/></a:spcBef>'
                "</a:pPr>" + "".join(rs) + "</a:p>"
            )
        body_inner = "".join(ps)
    elif text_runs:
        rs = []
        for r in text_runs:
            t = esc(r["text"])
            sz = r.get("sz", 1600)
            b = "1" if r.get("b") else "0"
            i = "1" if r.get("i") else "0"
            color = r.get("color", TEXT)
            font = r.get("font", "Arial")
            rs.append(
                f'<a:r><a:rPr lang="pt-BR" sz="{sz}" b="{b}" i="{i}">'
                f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
                f'<a:latin typeface="{font}"/>'
                f"</a:rPr><a:t>{t}</a:t></a:r>"
            )
        body_inner = f'<a:p><a:pPr algn="{text_align}"/>' + "".join(rs) + "</a:p>"

    return (
        f'<p:sp><p:nvSpPr><p:cNvPr id="{sp_id}" name="rect{sp_id}"/>'
        f"<p:cNvSpPr/><p:nvPr/></p:nvSpPr>"
        f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/>'
        f'<a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        f"{geom}"
        f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>'
        f"{line_xml}</p:spPr>"
        f'<p:txBody><a:bodyPr wrap="square" anchor="{text_anchor}" '
        f'lIns="180000" rIns="180000" tIns="120000" bIns="120000"/>'
        f"<a:lstStyle/>" + body_inner + "</p:txBody></p:sp>"
    )


def ellipse(
    sp_id: int,
    x: int,
    y: int,
    cx: int,
    cy: int,
    fill: str,
    *,
    text: str = "",
    text_color: str = WHITE,
    text_size: int = 2000,
    text_bold: bool = True,
) -> str:
    body = '<a:p><a:endParaRPr lang="pt-BR"/></a:p>'
    if text:
        body = (
            f'<a:p><a:pPr algn="ctr"/>'
            f'<a:r><a:rPr lang="pt-BR" sz="{text_size}" '
            f'b="{"1" if text_bold else "0"}">'
            f'<a:solidFill><a:srgbClr val="{text_color}"/></a:solidFill>'
            f'<a:latin typeface="Arial Black"/>'
            f"</a:rPr><a:t>" + esc(text) + "</a:t></a:r></a:p>"
        )
    return (
        f'<p:sp><p:nvSpPr><p:cNvPr id="{sp_id}" name="el{sp_id}"/>'
        f"<p:cNvSpPr/><p:nvPr/></p:nvSpPr>"
        f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/>'
        f'<a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        f'<a:prstGeom prst="ellipse"><a:avLst/></a:prstGeom>'
        f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>'
        f"<a:ln><a:noFill/></a:ln></p:spPr>"
        f'<p:txBody><a:bodyPr wrap="square" anchor="ctr" '
        f'lIns="36000" rIns="36000" tIns="36000" bIns="36000"/>'
        f"<a:lstStyle/>" + body + "</p:txBody></p:sp>"
    )


# ---------------------------------------------------------------------------
# Cabeçalho canônico (H1 + faixa amarela + subtítulo opcional)
# ---------------------------------------------------------------------------


def canonical_header(title: str, yellow_subtitle: str | None = None) -> list[str]:
    """Pilha canônica replicada da Aula 1: H1, faixa amarela e subtítulo opcional."""
    parts: list[str] = []
    parts.append(
        text_box(
            10,
            H1_X,
            H1_Y,
            H1_W,
            H1_H,
            [
                {
                    "text": title,
                    "sz": H1_SZ,
                    "b": True,
                    "color": NAVY,
                    "font": "Arial Black",
                }
            ],
            anchor="t",
            align="l",
        )
    )
    parts.append(filled_rect(11, FAIXA_X, FAIXA_Y, FAIXA_W, FAIXA_H, YELLOW))
    if yellow_subtitle:
        parts.append(
            text_box(
                12,
                SUB_X,
                SUB_Y,
                SUB_W,
                SUB_H,
                [
                    {
                        "text": yellow_subtitle,
                        "sz": SUB_SZ,
                        "b": True,
                        "color": YELLOW,
                        "font": "Arial",
                    }
                ],
                anchor="t",
                align="l",
            )
        )
    return parts


def footer_citation(sp_id: int, text: str) -> str:
    return text_box(
        sp_id,
        CONTENT_X_MIN,
        4350000,
        CONTENT_W,
        220000,
        [{"text": text, "sz": 1000, "i": True, "color": GREY, "font": "Arial"}],
        align="l",
        anchor="b",
    )


# ---------------------------------------------------------------------------
# Salvamento de slides
# ---------------------------------------------------------------------------


def slide_xml(spt_inner: str) -> str:
    return XML_HEADER + BG_BLOCK + TREE_OPEN + spt_inner + TREE_CLOSE + XML_FOOTER


def save_slide(n: int, body: str, *, image: int) -> None:
    """`image=1` para capa/transição/fim; `image=2` para todos os demais."""
    (SLIDES / f"slide{n}.xml").write_text(slide_xml(body), encoding="utf-8")
    media = "image1.png" if image == 1 else "image2.png"
    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" '
        'Target="../slideLayouts/slideLayout1.xml"/>'
        f'<Relationship Id="rId3" '
        f'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
        f'Target="../media/{media}"/>'
        "</Relationships>"
    )
    (RELS / f"slide{n}.xml.rels").write_text(rels, encoding="utf-8")


# ---------------------------------------------------------------------------
# Slides especiais — capa, transição, encerramento
# ---------------------------------------------------------------------------


def build_capa(
    n: int,
    aula_bloco: str,
    tema: str,
    subtitulo: str,
) -> None:
    """Capa do bloco — fundo image1.png. Geometria da Aula 1 slide 1."""
    parts: list[str] = []
    parts.append(
        text_box(
            10,
            HERO_X,
            914400,
            6790500,
            1828800,
            [
                {
                    "text": "JURIMETRIA E ANÁLISE DE DADOS PARA DECISÕES ESTRATÉGICAS",
                    "sz": 3200,
                    "b": True,
                    "color": NAVY,
                    "font": "Arial Black",
                }
            ],
            anchor="t",
            align="l",
        )
    )
    parts.append(filled_rect(11, 1097280, 2788920, 1828800, 54864, YELLOW))
    parts.append(
        text_box(
            12,
            1097280,
            2926080,
            5486400,
            457200,
            [
                {
                    "text": aula_bloco,
                    "sz": 2000,
                    "b": False,
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
            13,
            1097280,
            3337560,
            5486400,
            500000,
            [
                {
                    "text": tema,
                    "sz": 1400,
                    "color": GREY,
                    "font": "Arial",
                }
            ],
            anchor="t",
            align="l",
        )
    )
    if subtitulo:
        parts.append(
            text_box(
                14,
                1097280,
                3700000,
                5486400,
                400000,
                [
                    {
                        "text": subtitulo,
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
    save_slide(n, "".join(parts), image=1)


def build_transicao(n: int, numero: str, titulo: str, subtitulo: str) -> None:
    """Transição de tópico — fundo image1.png. Geometria da Aula 1 slide 6.

    cx do número grande alargado para 2400000 EMU para evitar quebra
    horizontal de "01"/"02" em renderizadores que usam Arial Black real
    (PowerPoint, LibreOffice GUI). O soffice headless usado no QA local
    falha em detectar essa quebra porque cai num fallback de fonte mais
    estreito.
    """
    parts: list[str] = []
    parts.append(
        text_box(
            20,
            HERO_X,
            900000,
            2400000,
            1100000,
            [
                {
                    "text": numero,
                    "sz": 9600,
                    "b": True,
                    "color": YELLOW,
                    "font": "Arial Black",
                }
            ],
            anchor="t",
            align="l",
        )
    )
    parts.append(
        text_box(
            21,
            HERO_X,
            2100000,
            6500000,
            1100000,
            [
                {
                    "text": titulo,
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
    parts.append(filled_rect(22, 1097280, 3250000, 1500000, 54864, YELLOW))
    parts.append(
        text_box(
            23,
            1097280,
            3400000,
            5486400,
            500000,
            [
                {
                    "text": subtitulo,
                    "sz": 1400,
                    "color": GREY,
                    "font": "Arial",
                }
            ],
            anchor="t",
            align="l",
        )
    )
    save_slide(n, "".join(parts), image=1)


def build_encerramento_b1(
    n: int,
    bloco_n: int,
    proximo_bloco_gancho: str,
) -> None:
    """Encerramento do Bloco 1 — fundo image1.png. Replica Aula 1 slide 49."""
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
                    "text": f"Fim do Bloco {bloco_n}",
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
            457200,
            [
                {
                    "text": "Intervalo de 15 minutos",
                    "sz": 2000,
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
            2849200,
            5486400,
            360000,
            [
                {
                    "text": f"No Bloco 2: {proximo_bloco_gancho}",
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


def build_encerramento_aula(
    n: int,
    aula_n: int,
    proxima_aula_gancho: str,
    *,
    atividade_n: int | None = None,
) -> None:
    """Encerramento da Aula N (Bloco 2) — fundo image1.png. Replica Aula 1
    B2 slide 42, com lembrete da Atividade.

    Se ``atividade_n`` for fornecida, mostra "Atividade N: responda em casa
    e entregue junto com o trabalho final (Aula 6)." na linha de entrega.
    Se ``atividade_n`` for ``None`` (Aulas 5 e 6, sem atividade nova),
    troca por mensagem alternativa indicada por ``proxima_aula_gancho``
    (o chamador é responsável por ajustar o texto)."""
    parts: list[str] = []
    parts.append(
        text_box(
            30,
            END_X,
            914400,
            5486400,
            702600,
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
    parts.append(filled_rect(31, END_X, 1661173, 1828800, 52800, YELLOW))
    parts.append(
        text_box(
            32,
            END_X,
            1836884,
            5486400,
            351300,
            [
                {
                    "text": "Lembrete:",
                    "sz": 1600,
                    "color": YELLOW,
                    "font": "Arial",
                }
            ],
            anchor="t",
            align="l",
        )
    )
    if atividade_n is not None:
        entrega_txt = (
            f"Atividade {atividade_n}: responda em casa e entregue junto com o "
            "trabalho final (Aula 6)."
        )
    else:
        entrega_txt = "Prepare a entrega consolidada do trabalho final."
    parts.append(
        text_box(
            33,
            END_X,
            2188307,
            6915900,
            351300,
            [
                {
                    "text": entrega_txt,
                    "sz": 1400,
                    "color": GREY,
                    "font": "Arial",
                }
            ],
            anchor="t",
            align="l",
        )
    )
    parts.append(
        text_box(
            34,
            END_X,
            2697950,
            6915900,
            351300,
            [
                {
                    "text": f"Próxima aula: {proxima_aula_gancho}",
                    "sz": 1500,
                    "color": NAVY,
                    "font": "Arial",
                }
            ],
            anchor="t",
            align="l",
        )
    )
    save_slide(n, "".join(parts), image=1)


def build_atividade_pratica(
    n: int,
    atividade_n: int,
    titulo_atividade: str,
    perguntas: list[str],
) -> None:
    """Slide único de Atividade Prática N (Bloco 2 das Aulas 1 a 4).
    Replica Aula 1 B2 slide 38. Cabeçalho padrão com subtítulo amarelo
    ``Entrega junto com o trabalho final (Aula 6)``.

    ``perguntas`` deve ter exatamente 3 itens (Q1, Q2, Q3)."""
    if len(perguntas) != 3:
        raise ValueError("Atividade Prática exige exatamente 3 perguntas.")

    parts = canonical_header(
        f"Atividade Prática {atividade_n}",
        "Entrega junto com o trabalho final (Aula 6)",
    )

    # Card navy com o título da atividade
    parts.append(
        filled_rect(
            50,
            CONTENT_X_MIN,
            1700000,
            6847800,
            720000,
            NAVY,
            multi_paragraphs=[
                [
                    {
                        "text": titulo_atividade,
                        "sz": 1700,
                        "b": True,
                        "color": YELLOW,
                        "font": "Arial Black",
                    }
                ]
            ],
            text_align="l",
            text_anchor="ctr",
        )
    )

    # Caixa "Você deverá responder"
    parts.append(
        text_box(
            51,
            CONTENT_X_MIN,
            2520000,
            6847800,
            300000,
            [
                {
                    "text": "Você deverá responder, individualmente, em casa",
                    "sz": 1300,
                    "b": True,
                    "color": NAVY,
                    "font": "Arial Black",
                }
            ],
            anchor="t",
            align="l",
        )
    )

    # Bloco com Pergunta 1./2./3.
    paragraphs = []
    for i, p in enumerate(perguntas, start=1):
        paragraphs.append(
            [
                {
                    "text": f"Pergunta {i}. ",
                    "sz": 1200,
                    "b": True,
                    "color": YELLOW,
                    "font": "Arial Black",
                },
                {
                    "text": p,
                    "sz": 1200,
                    "color": TEXT,
                    "font": "Arial",
                },
            ]
        )
    parts.append(
        multi_para_box(
            52,
            CONTENT_X_MIN,
            2880000,
            7020000,
            1500000,
            paragraphs,
            line_spc=125000,
            para_spc_before=400,
        )
    )

    # Lembrete do peso
    parts.append(
        text_box(
            53,
            CONTENT_X_MIN,
            4400000,
            7020000,
            260000,
            [
                {
                    "text": "Peso: 4 atividades = 3,0 pts (média aritmética simples).",
                    "sz": 1000,
                    "i": True,
                    "color": GREY,
                    "font": "Arial",
                }
            ],
            anchor="t",
            align="l",
        )
    )
    save_slide(n, "".join(parts), image=2)


# ---------------------------------------------------------------------------
# Slides estruturais — Agenda, Objetivos, Conexão, Síntese, Ponte, Referências
# ---------------------------------------------------------------------------


def build_agenda(n: int, items: list[str]) -> None:
    """Agenda do Bloco — grade 2×4 (até 8 itens). Replica Aula 1 B1 slide 3."""
    parts = canonical_header("Agenda do Bloco", "O que vamos percorrer nas próximas 1h50min")

    # grade 2×4: 4 linhas, 2 colunas
    y_positions = [1700000, 2300000, 2900000, 3500000]
    el_x_left = 781363
    el_x_right = 4204761
    title_x_left = 1301363
    title_x_right = 4724761

    base_id = 50
    for i, item in enumerate(items[:8]):
        col = i % 2  # 0 = esquerda, 1 = direita
        row = i // 2
        if row >= len(y_positions):
            break
        y = y_positions[row]
        el_x = el_x_left if col == 0 else el_x_right
        t_x = title_x_left if col == 0 else title_x_right

        parts.append(
            ellipse(
                base_id + i * 2,
                el_x,
                y,
                420000,
                420000,
                NAVY,
                text=str(i + 1),
                text_color=YELLOW,
                text_size=1600,
                text_bold=True,
            )
        )
        parts.append(
            text_box(
                base_id + i * 2 + 1,
                t_x,
                y + 60000,
                2400000,
                399900,
                [
                    {
                        "text": item,
                        "sz": 1200,
                        "color": NAVY,
                        "font": "Arial",
                    }
                ],
                anchor="ctr",
                align="l",
            )
        )

    save_slide(n, "".join(parts), image=2)


def build_objetivos(n: int, items: list[tuple[str, str]]) -> None:
    """Objetivos de aprendizagem — círculo amarelo + verbo + descrição.

    `items` é uma lista de pares (verbo, descrição). Replica Aula 1 B1 slide 4.
    """
    parts = canonical_header(
        "Objetivos de Aprendizagem",
        "Ao final deste bloco, você será capaz de",
    )

    y_positions = [1750000, 2270000, 2790000, 3310000, 3830000]
    base_id = 50

    for i, (verbo, descricao) in enumerate(items[:5]):
        y = y_positions[i]
        # Círculo amarelo pequeno
        parts.append(
            ellipse(
                base_id + i * 3,
                790000,
                y + 30000,
                160000,
                160000,
                YELLOW,
                text="",
            )
        )
        # Verbo
        parts.append(
            text_box(
                base_id + i * 3 + 1,
                1060000,
                y,
                1800000,
                300000,
                [
                    {
                        "text": verbo,
                        "sz": 1500,
                        "b": True,
                        "color": NAVY,
                        "font": "Arial Black",
                    }
                ],
                anchor="t",
                align="l",
            )
        )
        # Descrição
        parts.append(
            text_box(
                base_id + i * 3 + 2,
                2900000,
                y,
                3500000,
                500100,
                [
                    {
                        "text": descricao,
                        "sz": 1250,
                        "color": TEXT,
                        "font": "Arial",
                    }
                ],
                anchor="t",
                align="l",
            )
        )

    save_slide(n, "".join(parts), image=2)


def build_conexao_voltando(
    n: int,
    titulo: str,
    subtitulo_amarelo: str,
    intro: str,
    paragrafos: list[str],
    *,
    citation: str | None = None,
) -> None:
    """Conexão / 'Voltando do intervalo' — variante texto corrido.

    Replica padrão de Aula 1 B2 slide 4 (texto corrido sob o cabeçalho).
    """
    parts = canonical_header(titulo, subtitulo_amarelo)

    parts.append(
        text_box(
            50,
            CONTENT_X_MIN,
            1730000,
            CONTENT_W,
            340000,
            [
                {
                    "text": intro,
                    "sz": 1400,
                    "color": TEXT,
                    "font": "Arial",
                }
            ],
            anchor="t",
            align="l",
        )
    )

    paragraphs = [
        [{"text": p, "sz": 1500, "color": TEXT, "font": "Arial"}] for p in paragrafos
    ]
    parts.append(
        multi_para_box(
            51,
            CONTENT_X_MIN,
            2200000,
            CONTENT_W,
            2050000,
            paragraphs,
            line_spc=130000,
            para_spc_before=600,
        )
    )
    if citation:
        parts.append(footer_citation(52, citation))
    save_slide(n, "".join(parts), image=2)


def build_sintese(n: int, items: list[str]) -> None:
    """Síntese do Bloco — 5 itens com selo amarelo numerado. Replica Aula 1 B1 slide 46."""
    parts = canonical_header(
        "Síntese do Bloco",
        f"{['Um', 'Dois', 'Três', 'Quatro', 'Cinco'][min(len(items), 5) - 1]} pontos para levar para casa",
    )

    y_positions = [1750000, 2320000, 2890000, 3460000, 4030000]
    base_id = 50

    for i, txt in enumerate(items[:5]):
        y = y_positions[i]
        # Selo amarelo com número branco
        parts.append(
            filled_rect(
                base_id + i * 2,
                750000,
                y,
                500000,
                500000,
                YELLOW,
                text_runs=[
                    {
                        "text": str(i + 1),
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
        # Texto descritivo
        parts.append(
            text_box(
                base_id + i * 2 + 1,
                1350000,
                y + 60000,
                5300000,
                450000,
                [
                    {
                        "text": txt,
                        "sz": 1250,
                        "color": TEXT,
                        "font": "Arial",
                    }
                ],
                anchor="t",
                align="l",
            )
        )

    save_slide(n, "".join(parts), image=2)


def build_ponte(
    n: int,
    titulo_destaque: str,
    descricao_destaque: str,
    items: list[tuple[str, str]],
    *,
    titulo: str = "Ponte para o Bloco 2",
    subtitulo: str = "O que vem a seguir, depois do intervalo",
) -> None:
    """Ponte (Bloco 1 → Bloco 2 ou Bloco 2 → próxima aula) — hero seta + lista
    de até 4 itens. Replica Aula 1 B1 slide 47. `items` = lista de (título, descrição).

    Para Ponte do Bloco 2 → próxima aula, passar
    ``titulo="Ponte para a próxima aula"`` e
    ``subtitulo="O que vem na semana que vem"``.
    """
    parts = canonical_header(titulo, subtitulo)

    # Hero seta amarela
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
    # Título de destaque
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
    # Descrição cinza do hero
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

    # Itens (até 4)
    y_positions = [2600000, 3030000, 3460000, 3890000]
    base_id = 53
    for i, (titulo_item, descricao_item) in enumerate(items[:4]):
        y = y_positions[i]
        # Bullet amarelo
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
        # Título do item
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
        # Descrição do item
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


def build_referencias(n: int, items: list[str]) -> None:
    """Referências do bloco — caixa única com texto ABNT. Replica Aula 1 B1 slide 48."""
    parts = canonical_header("Referências do Bloco", "Fontes citadas ao longo do conteúdo")

    paragraphs = [
        [{"text": item, "sz": 1000, "color": TEXT, "font": "Arial"}] for item in items
    ]
    parts.append(
        multi_para_box(
            50,
            CONTENT_X_MIN,
            1780000,
            7025100,
            2350000,
            paragraphs,
            line_spc=115000,
            para_spc_before=250,
        )
    )
    parts.append(
        text_box(
            51,
            CONTENT_X_MIN,
            4250000,
            CONTENT_W,
            300000,
            [
                {
                    "text": "Leituras complementares estarão indicadas ao longo dos próximos blocos.",
                    "sz": 1000,
                    "color": GREY,
                    "font": "Arial",
                }
            ],
            anchor="t",
            align="l",
        )
    )
    save_slide(n, "".join(parts), image=2)


# ---------------------------------------------------------------------------
# Slides de conteúdo (cabeçalho padrão + corpo)
# ---------------------------------------------------------------------------


def build_conceito(
    n: int,
    title: str,
    paragrafos: list[str],
    *,
    citation: str | None = None,
    accent: str | None = None,
) -> None:
    """Conceito + parágrafos sob cabeçalho padrão."""
    parts = canonical_header(title, accent)
    body_y = 1730000 if accent else 1700000

    paragraphs = [
        [{"text": p, "sz": 1500, "color": TEXT, "font": "Arial"}] for p in paragrafos
    ]
    parts.append(
        multi_para_box(
            50,
            CONTENT_X_MIN,
            body_y,
            CONTENT_W,
            CONTENT_Y_MAX - body_y - 350000,
            paragraphs,
            line_spc=130000,
            para_spc_before=600,
        )
    )
    if citation:
        parts.append(footer_citation(51, citation))
    save_slide(n, "".join(parts), image=2)


def build_card(
    n: int,
    title: str,
    card_title: str,
    card_paragraphs: list[str],
    *,
    citation: str | None = None,
    card_h: int = 2400000,
    card_title_size: int = 1700,
    card_text_size: int = 1400,
) -> None:
    """Card cinza claro com borda navy, sob cabeçalho padrão."""
    parts = canonical_header(title, card_title)
    card_paras = []
    for p in card_paragraphs:
        card_paras.append(
            [{"text": p, "sz": card_text_size, "color": TEXT, "font": "Arial"}]
        )
    parts.append(
        filled_rect(
            50,
            CONTENT_X_MIN + 50000,
            1800000,
            CONTENT_W - 100000,
            card_h,
            LIGHT,
            line=NAVY,
            rounded=True,
            multi_paragraphs=card_paras,
            text_align="l",
            text_anchor="t",
        )
    )
    if citation:
        parts.append(footer_citation(51, citation))
    save_slide(n, "".join(parts), image=2)


def build_stat(
    n: int,
    title: str,
    big_number: str,
    label: str,
    *,
    citation: str | None = None,
) -> None:
    """Stat callout: número grande + label."""
    parts = canonical_header(title)
    parts.append(
        text_box(
            50,
            CONTENT_X_MIN,
            1800000,
            5800000,
            1400000,
            [
                {
                    "text": big_number,
                    "sz": 7200,
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
            CONTENT_X_MIN,
            3300000,
            CONTENT_W,
            900000,
            [
                {
                    "text": label,
                    "sz": 1600,
                    "color": GREY,
                    "font": "Arial",
                }
            ],
            anchor="t",
            align="l",
        )
    )
    if citation:
        parts.append(footer_citation(52, citation))
    save_slide(n, "".join(parts), image=2)


def build_comparacao(
    n: int,
    title: str,
    left_label: str,
    left_items: list[str],
    right_label: str,
    right_items: list[str],
    *,
    citation: str | None = None,
) -> None:
    """Comparação em 2 colunas (header navy + amarelo, body com bullets)."""
    parts = canonical_header(title)

    col_w = 2870000
    gap = 210000
    left_x = CONTENT_X_MIN
    right_x = CONTENT_X_MIN + col_w + gap
    header_y = 1780000
    header_h = 480000
    body_y = header_y + header_h
    body_h = 1850000

    max_len = max((len(s) for s in left_items + right_items), default=0)
    if max_len > 80:
        item_size = 1100
    elif max_len > 50:
        item_size = 1250
    else:
        item_size = 1400

    parts.append(
        filled_rect(
            50,
            left_x,
            header_y,
            col_w,
            header_h,
            NAVY,
            text_runs=[
                {
                    "text": left_label,
                    "sz": 1700,
                    "b": True,
                    "color": WHITE,
                    "font": "Arial Black",
                }
            ],
            text_align="l",
            text_anchor="ctr",
        )
    )
    parts.append(
        filled_rect(
            51,
            right_x,
            header_y,
            col_w,
            header_h,
            YELLOW,
            text_runs=[
                {
                    "text": right_label,
                    "sz": 1700,
                    "b": True,
                    "color": NAVY,
                    "font": "Arial Black",
                }
            ],
            text_align="l",
            text_anchor="ctr",
        )
    )

    left_paras = [
        [{"text": item, "sz": item_size, "color": TEXT, "font": "Arial"}] for item in left_items
    ]
    right_paras = [
        [{"text": item, "sz": item_size, "color": TEXT, "font": "Arial"}] for item in right_items
    ]
    parts.append(
        multi_para_box(
            52,
            left_x,
            body_y,
            col_w,
            body_h,
            left_paras,
            bullet="•",
            bullet_color=NAVY,
            line_spc=120000,
            para_spc_before=400,
        )
    )
    parts.append(
        multi_para_box(
            53,
            right_x,
            body_y,
            col_w,
            body_h,
            right_paras,
            bullet="•",
            bullet_color=YELLOW,
            line_spc=120000,
            para_spc_before=400,
        )
    )
    if citation:
        parts.append(footer_citation(54, citation))
    save_slide(n, "".join(parts), image=2)


def build_diagrama_6_etapas(
    n: int,
    title: str,
    etapas: list[str],
    *,
    destaque: int | None = None,
    citation: str | None = None,
) -> None:
    """Diagrama horizontal de 6 etapas em círculos navy/amarelos."""
    parts = canonical_header(title)
    nodes = 6
    diam = 700000
    spacing = (CONTENT_W - diam) / (nodes - 1)
    y_circ = 2000000
    label_y = y_circ + diam + 80000

    base_id = 50
    for i in range(nodes):
        cx = CONTENT_X_MIN + int(i * spacing)
        is_focus = destaque is not None and (i + 1) == destaque
        fill = YELLOW if is_focus else NAVY
        text_color = NAVY if is_focus else WHITE
        parts.append(
            ellipse(
                base_id + i,
                cx,
                y_circ,
                diam,
                diam,
                fill,
                text=str(i + 1),
                text_color=text_color,
                text_size=2400,
                text_bold=True,
            )
        )
        if i < nodes - 1:
            arrow_x = cx + diam + 30000
            arrow_w = int(spacing) - diam - 60000
            arrow_y = y_circ + diam // 2 - 25000
            parts.append(filled_rect(base_id + 100 + i, arrow_x, arrow_y, arrow_w, 50000, NAVY))

        label_x = cx - 350000
        label_w = diam + 700000
        parts.append(
            text_box(
                base_id + 200 + i,
                label_x,
                label_y,
                label_w,
                700000,
                [
                    {
                        "text": etapas[i],
                        "sz": 1100,
                        "b": True,
                        "color": NAVY,
                        "font": "Arial",
                    }
                ],
                anchor="t",
                align="ctr",
            )
        )
    if citation:
        parts.append(footer_citation(60, citation))
    save_slide(n, "".join(parts), image=2)


def build_tabela(
    n: int,
    title: str,
    header: list[str],
    rows: list[list[str]],
    *,
    citation: str | None = None,
    col_widths: list[int] | None = None,
) -> None:
    """Tabela zebrada com header navy."""
    parts = canonical_header(title)

    n_cols = len(header)
    if col_widths is None:
        col_widths = [CONTENT_W // n_cols] * n_cols
    assert len(col_widths) == n_cols

    row_h = 320000
    header_h = 380000
    base_y = 1780000

    base_id = 50
    sp_id = base_id

    x = CONTENT_X_MIN
    for ci, col_w in enumerate(col_widths):
        parts.append(
            filled_rect(
                sp_id,
                x,
                base_y,
                col_w,
                header_h,
                NAVY,
                text_runs=[
                    {
                        "text": header[ci],
                        "sz": 1300,
                        "b": True,
                        "color": WHITE,
                        "font": "Arial Black",
                    }
                ],
                text_align="l",
                text_anchor="ctr",
            )
        )
        sp_id += 1
        x += col_w

    for ri, row in enumerate(rows):
        x = CONTENT_X_MIN
        y = base_y + header_h + ri * row_h
        zebra = LIGHT if ri % 2 == 0 else WHITE
        for ci, val in enumerate(row):
            parts.append(
                filled_rect(
                    sp_id,
                    x,
                    y,
                    col_widths[ci],
                    row_h,
                    zebra,
                    text_runs=[
                        {
                            "text": val,
                            "sz": 1200,
                            "color": TEXT,
                            "font": "Arial",
                        }
                    ],
                    text_align="l",
                    text_anchor="ctr",
                )
            )
            sp_id += 1
            x += col_widths[ci]

    if citation:
        parts.append(footer_citation(sp_id, citation))
    save_slide(n, "".join(parts), image=2)


def build_armadilhas(
    n: int,
    title: str,
    items: list[tuple[str, str]],
    *,
    citation: str | None = None,
    card_h: int | None = None,
    base_y: int = 1700000,
) -> None:
    """Armadilhas em N cards verticais com borda amarela.

    Se ``card_h`` não for passado, calcula a altura automaticamente para
    caber dentro do hard limit (y_max=4685000) considerando o número de
    items, mantendo um gap fixo entre os cards.
    """
    parts = canonical_header(title)
    gap = 30000
    n_items = len(items)
    if card_h is None:
        # Hard limit y_max = 4685000; reserva 35000 de folga
        max_total = 4685000 - base_y - 35000
        card_h = (max_total - (n_items - 1) * gap) // n_items
        # Mínimo razoável para acomodar label + 1 linha de body
        card_h = max(card_h, 620000)

    for i, (label, body) in enumerate(items):
        y = base_y + i * (card_h + gap)
        parts.append(
            filled_rect(
                50 + i * 3,
                CONTENT_X_MIN,
                y,
                CONTENT_W,
                card_h,
                LIGHT,
                line=YELLOW,
                line_w=15000,
                rounded=True,
                multi_paragraphs=[
                    [
                        {
                            "text": f"⚠  {label}",
                            "sz": 1400,
                            "b": True,
                            "color": NAVY,
                            "font": "Arial Black",
                        }
                    ],
                    [{"text": body, "sz": 1150, "color": TEXT, "font": "Arial"}],
                ],
                text_align="l",
                text_anchor="t",
            )
        )

    if citation:
        parts.append(footer_citation(80, citation))
    save_slide(n, "".join(parts), image=2)


def build_lista_numerada(
    n: int,
    title: str,
    items: list[str],
    *,
    citation: str | None = None,
    item_size: int = 1300,
    accent: str | None = None,
) -> None:
    """Lista numerada simples (cabeçalho padrão + parágrafos numerados em amarelo)."""
    parts = canonical_header(title, accent)
    paragraphs = []
    for i, txt in enumerate(items, start=1):
        paragraphs.append(
            [
                {
                    "text": f"{i:>2}.  ",
                    "sz": item_size,
                    "b": True,
                    "color": YELLOW,
                    "font": "Arial Black",
                },
                {"text": txt, "sz": item_size, "color": TEXT, "font": "Arial"},
            ]
        )
    parts.append(
        multi_para_box(
            50,
            CONTENT_X_MIN,
            1780000,
            CONTENT_W,
            2700000,
            paragraphs,
            line_spc=120000,
            para_spc_before=600,
        )
    )
    if citation:
        parts.append(footer_citation(51, citation))
    save_slide(n, "".join(parts), image=2)


def build_recap_atividade(
    n: int,
    aula_n: int,
    intro: str,
    questoes: list[str],
    *,
    citation: str | None = None,
) -> None:
    """Recap da Atividade N (slide 2 do bloco de correção)."""
    parts = canonical_header(
        f"O que foi pedido na Atividade {aula_n - 1}",
        f"Atividade Prática {aula_n - 1} (Bloco 2 da Aula {aula_n - 1}) · 3 questões",
    )

    paragraphs = [[{"text": intro, "sz": 1400, "color": TEXT, "font": "Arial"}]]
    for i, q in enumerate(questoes[:3], start=1):
        paragraphs.append(
            [
                {
                    "text": f"Q{i}. ",
                    "sz": 1400,
                    "b": True,
                    "color": YELLOW,
                    "font": "Arial Black",
                },
                {"text": q, "sz": 1400, "color": TEXT, "font": "Arial"},
            ]
        )

    parts.append(
        multi_para_box(
            50,
            CONTENT_X_MIN,
            1780000,
            CONTENT_W,
            2520000,
            paragraphs,
            line_spc=125000,
            para_spc_before=600,
        )
    )
    if citation:
        parts.append(footer_citation(51, citation))
    save_slide(n, "".join(parts), image=2)


def build_correcao_questao(
    n: int,
    aula_n: int,
    questao_num: int,
    enunciado: str,
    pontos: list[str],
    *,
    citation: str | None = None,
) -> None:
    """Slide de correção (1 por questão). Cabeçalho padrão + enunciado + bullets."""
    parts = canonical_header(
        f"Atividade {aula_n - 1} · Questão {questao_num}",
        "Caminho de resposta esperado e armadilhas observadas",
    )

    # Card amarelo com enunciado
    parts.append(
        filled_rect(
            50,
            CONTENT_X_MIN,
            1780000,
            CONTENT_W,
            720000,
            YELLOW,
            multi_paragraphs=[
                [
                    {
                        "text": enunciado,
                        "sz": 1400,
                        "b": True,
                        "color": NAVY,
                        "font": "Arial Black",
                    }
                ]
            ],
            text_align="l",
            text_anchor="ctr",
        )
    )

    paragraphs = [
        [
            {
                "text": "▶  ",
                "sz": 1200,
                "b": True,
                "color": YELLOW,
                "font": "Arial Black",
            },
            {"text": p, "sz": 1200, "color": TEXT, "font": "Arial"},
        ]
        for p in pontos
    ]
    parts.append(
        multi_para_box(
            51,
            CONTENT_X_MIN,
            2560000,
            CONTENT_W,
            1700000,
            paragraphs,
            line_spc=115000,
            para_spc_before=300,
        )
    )
    if citation:
        parts.append(footer_citation(52, citation))
    save_slide(n, "".join(parts), image=2)


# ---------------------------------------------------------------------------
# Exercício dirigido (enunciado + resposta nos slides seguintes)
# Padrão obrigatório de aulas online: o slide de enunciado é seguido
# imediatamente pelo slide de resposta-modelo comentada pelo professor.
# ---------------------------------------------------------------------------


def build_exercicio_enunciado(
    n: int,
    titulo: str,
    enunciado: str,
    contexto: str | None = None,
    *,
    citation: str | None = None,
) -> None:
    """Slide de enunciado de exercício dirigido. Cabeçalho padrão + card pastel
    com a pergunta destacada. A resposta vem no slide seguinte."""
    parts = canonical_header(titulo, "Vamos pensar juntos")

    if contexto:
        parts.append(
            text_box(
                50,
                CONTENT_X_MIN,
                1740000,
                CONTENT_W,
                400000,
                [
                    {
                        "text": contexto,
                        "sz": 1300,
                        "color": GREY,
                        "font": "Arial",
                    }
                ],
                anchor="t",
                align="l",
            )
        )
        card_y = 2200000
    else:
        card_y = 1800000

    # Card pastel com a pergunta destacada
    parts.append(
        filled_rect(
            51,
            CONTENT_X_MIN,
            card_y,
            CONTENT_W,
            1700000,
            PASTEL,
            line=YELLOW,
            line_w=12700,
            rounded=True,
            multi_paragraphs=[
                [
                    {
                        "text": "Pergunta dirigida",
                        "sz": 1200,
                        "b": True,
                        "color": YELLOW,
                        "font": "Arial Black",
                    }
                ],
                [
                    {
                        "text": enunciado,
                        "sz": 1500,
                        "b": True,
                        "color": NAVY,
                        "font": "Arial Black",
                    }
                ],
            ],
            text_align="l",
            text_anchor="t",
        )
    )

    # Linha-rodapé "→ resposta no próximo slide"
    parts.append(
        text_box(
            52,
            CONTENT_X_MIN,
            4080000,
            CONTENT_W,
            260000,
            [
                {
                    "text": "→ Caminho de resposta no próximo slide.",
                    "sz": 1100,
                    "i": True,
                    "color": GREY,
                    "font": "Arial",
                }
            ],
            anchor="t",
            align="l",
        )
    )

    if citation:
        parts.append(footer_citation(60, citation))
    save_slide(n, "".join(parts), image=2)


def build_exercicio_resposta(
    n: int,
    titulo: str,
    recap: str,
    bullets: list[str],
    *,
    citation: str | None = None,
) -> None:
    """Slide de resposta-modelo do exercício dirigido. Cabeçalho padrão com
    chip 'Resposta', recap curto da pergunta e bullets com o caminho."""
    parts = canonical_header(titulo, "Caminho de resposta comentado")

    # Card amarelo claro com o recap da pergunta
    parts.append(
        filled_rect(
            50,
            CONTENT_X_MIN,
            1780000,
            CONTENT_W,
            560000,
            YELLOW,
            multi_paragraphs=[
                [
                    {
                        "text": recap,
                        "sz": 1300,
                        "b": True,
                        "color": NAVY,
                        "font": "Arial Black",
                    }
                ]
            ],
            text_align="l",
            text_anchor="ctr",
        )
    )

    paragraphs = [
        [
            {
                "text": "▶  ",
                "sz": 1100,
                "b": True,
                "color": YELLOW,
                "font": "Arial Black",
            },
            {"text": p, "sz": 1200, "color": TEXT, "font": "Arial"},
        ]
        for p in bullets
    ]
    parts.append(
        multi_para_box(
            51,
            CONTENT_X_MIN,
            2400000,
            CONTENT_W,
            1850000,
            paragraphs,
            line_spc=120000,
            para_spc_before=300,
        )
    )
    if citation:
        parts.append(footer_citation(52, citation))
    save_slide(n, "".join(parts), image=2)


# ---------------------------------------------------------------------------
# Atualizações em [Content_Types].xml e presentation.xml
# ---------------------------------------------------------------------------


def update_content_types(slide_count: int) -> None:
    text = CT.read_text(encoding="utf-8")
    new_overrides = []
    for i in range(1, slide_count + 1):
        if f"/ppt/slides/slide{i}.xml" not in text:
            new_overrides.append(
                f'<Override PartName="/ppt/slides/slide{i}.xml" '
                f'ContentType="application/vnd.openxmlformats-officedocument.'
                f'presentationml.slide+xml"/>'
            )
    if new_overrides:
        text = text.replace("</Types>", "".join(new_overrides) + "</Types>")
    CT.write_text(text, encoding="utf-8")


def update_presentation(slide_count: int) -> None:
    rels = PRES_RELS.read_text(encoding="utf-8")
    used_rids = {int(m) for m in re.findall(r'Id="rId(\d+)"', rels)}
    next_rid = max(used_rids) + 1
    slide_to_rid: dict[int, int] = {}

    for n in range(1, slide_count + 1):
        target = f"slides/slide{n}.xml"
        m = re.search(rf'Id="(rId\d+)"[^/]*Target="{re.escape(target)}"', rels)
        if m:
            slide_to_rid[n] = int(m.group(1)[3:])
        else:
            slide_to_rid[n] = next_rid
            new_rel = (
                f'<Relationship Id="rId{next_rid}" '
                f'Type="http://schemas.openxmlformats.org/officeDocument/'
                f'2006/relationships/slide" Target="{target}"/>'
            )
            rels = rels.replace("</Relationships>", new_rel + "</Relationships>")
            next_rid += 1

    PRES_RELS.write_text(rels, encoding="utf-8")

    pres = PRES.read_text(encoding="utf-8")
    new_lst_items = []
    for i, n in enumerate(range(1, slide_count + 1), start=0):
        sld_id = 256 + i
        new_lst_items.append(f'<p:sldId id="{sld_id}" r:id="rId{slide_to_rid[n]}"/>')
    new_lst = "<p:sldIdLst>" + "".join(new_lst_items) + "</p:sldIdLst>"

    pres = re.sub(r"<p:sldIdLst>.*?</p:sldIdLst>", new_lst, pres, count=1, flags=re.DOTALL)
    PRES.write_text(pres, encoding="utf-8")


# ---------------------------------------------------------------------------
# Construção do bloco
# ---------------------------------------------------------------------------


CANONICAL_IMAGE1_MD5 = "b0987cbbb2c05a7cebbd3bac3576c0bb"
"""md5 do image1.png da Aula 1 publicada (fundo "forte"
capa/transição/fim). Se o image1.png do deck já tiver este hash, o
swap não precisa rodar — função é idempotente."""


def swap_media_para_aula1() -> None:
    """Garante que image1.png seja o fundo "forte" (capa/transição/fim)
    e image2.png o "suave" (conteúdo), conforme a Aula 1 publicada.

    O `layout.pptx` template foi exportado com os PNGs físicos trocados
    em relação à convenção canônica. Esta função alinha o estado físico
    à convenção. **É idempotente:** se image1.png já é o canônico
    "forte" (md5 == CANONICAL_IMAGE1_MD5), não faz nada. Isso evita o
    bug de double-swap quando a função roda mais de uma vez no mesmo
    deck unpacked.
    """
    import hashlib

    media = DECK / "ppt/media"
    img1 = media / "image1.png"
    img2 = media / "image2.png"
    if not (img1.is_file() and img2.is_file()):
        return
    current_md5 = hashlib.md5(img1.read_bytes()).hexdigest()
    if current_md5 == CANONICAL_IMAGE1_MD5:
        return
    tmp = media / ".swap.png"
    img1.rename(tmp)
    img2.rename(img1)
    tmp.rename(img2)


def unpack_layout_fresh() -> None:
    """Garante que /tmp/deck_aula3_bloco2/ é um unpack limpo do
    layout.pptx oficial. Sempre rm -rf antes de unpack para evitar
    estado residual de execuções anteriores (que podia causar
    double-swap em image1/image2)."""
    import shutil
    import subprocess

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


def main() -> None:
    unpack_layout_fresh()
    SLIDES.mkdir(parents=True, exist_ok=True)
    RELS.mkdir(parents=True, exist_ok=True)
    swap_media_para_aula1()

    # 1. Capa
    build_capa(
        1,
        "Aula 3 \u00b7 Bloco 2",
        "O Ciclo da Ci\u00eancia de Dados Aplicado ao Direito (Parte 2)",
        "Da TABELA ao insight: distribui\u00e7\u00f5es, visualiza\u00e7\u00e3o e leitura cr\u00edtica de gr\u00e1ficos",
    )

    # 2. Agenda
    build_agenda(
        2,
        [
            "Distribui\u00e7\u00f5es: Normal, Poisson, Weibull",
            "Etapa 6: qual gr\u00e1fico para qual pergunta",
            "Boas pr\u00e1ticas de visualiza\u00e7\u00e3o",
            "Demonstra\u00e7\u00e3o em XY&A",
            "Leitura cr\u00edtica de gr\u00e1ficos",
            "Exerc\u00edcios dirigidos",
            "Atividade Pr\u00e1tica 3",
            "Ponte para Aula 4",
        ],
    )

    # 3. Objetivos
    build_objetivos(
        3,
        [
            ("Reconhecer", "as distribui\u00e7\u00f5es Normal, Poisson e Weibull em vari\u00e1veis jur\u00eddicas t\u00edpicas"),
            ("Escolher", "o tipo de gr\u00e1fico adequado para cada pergunta jurim\u00e9trica"),
            ("Aplicar", "boas pr\u00e1ticas de visualiza\u00e7\u00e3o aos gr\u00e1ficos da base XY&A"),
            ("Identificar", "armadilhas em gr\u00e1ficos (eixos truncados, escalas log, correla\u00e7\u00f5es esp\u00farias)"),
            ("Produzir", "uma an\u00e1lise explorat\u00f3ria simples ligada a uma decis\u00e3o concreta"),
        ],
    )

    # 4. Conex\u00e3o / Voltando do intervalo
    build_conexao_voltando(
        4,
        "Voltando do intervalo",
        "Onde paramos no Bloco 1",
        "No Bloco 1 tratamos a base (Etapa 4) e fizemos a primeira leitura descritiva (Etapa 5).",
        [
            "Agora completamos o ciclo: Etapa 6, apresentar resultados em gr\u00e1ficos defens\u00e1veis.",
            "Antes, 3 distribui\u00e7\u00f5es que aparecem no Direito: valor, volume e tempo.",
            "Fechamos com leitura cr\u00edtica de gr\u00e1ficos e a Atividade Pr\u00e1tica 3.",
        ],
        citation="Wheelan (2016); Nunes (2019)",
    )

    # =================================================================
    # T\u00f3pico 01 \u2014 Distribui\u00e7\u00f5es de probabilidade relevantes
    # =================================================================

    # 5. Transi\u00e7\u00e3o 01
    build_transicao(
        5,
        "01",
        "Distribui\u00e7\u00f5es",
        "Normal, Poisson e Weibull com analogias jur\u00eddicas (valor, volume, tempo)",
    )

    # 6. O que \u00e9 distribui\u00e7\u00e3o
    build_conceito(
        6,
        "O que \u00e9 uma distribui\u00e7\u00e3o",
        [
            "Distribui\u00e7\u00e3o \u00e9 a forma como os valores de uma vari\u00e1vel se espalham: onde se concentram, onde s\u00e3o raros, qual a cara do hist\u00f3rico.",
            "Reconhecer a distribui\u00e7\u00e3o ajuda a escolher a medida certa (m\u00e9dia ou mediana), o gr\u00e1fico certo (histograma, boxplot) e a interpreta\u00e7\u00e3o jur\u00eddica certa.",
            "No Direito, tr\u00eas fam\u00edlias bastam para a maior parte das an\u00e1lises descritivas: Normal, Poisson e Weibull.",
        ],
        citation="Wheelan (2016); James et al. (2021)",
    )

    # 7. As 3 distribui\u00e7\u00f5es jur\u00eddicas (vis\u00e3o geral)
    build_card(
        7,
        "Tr\u00eas distribui\u00e7\u00f5es, tr\u00eas perguntas",
        "Cada distribui\u00e7\u00e3o responde a um tipo de pergunta",
        [
            "Normal: valores cont\u00ednuos e sim\u00e9tricos em torno de uma m\u00e9dia. Pergunta t\u00edpica: qual o valor t\u00edpico de uma condena\u00e7\u00e3o?",
            "Poisson: contagem de eventos em um per\u00edodo. Pergunta t\u00edpica: quantos processos novos chegam por m\u00eas a uma vara?",
            "Weibull: tempo at\u00e9 um evento (sentencia, acordo, baixa). Pergunta t\u00edpica: em quanto tempo um processo sai daqui?",
        ],
        citation="Wheelan (2016); James et al. (2021)",
        card_h=2300000,
    )

    # 8. Normal: valor da causa
    build_conceito(
        8,
        "Normal: o valor t\u00edpico",
        [
            "Distribui\u00e7\u00e3o sim\u00e9trica em torno da m\u00e9dia. A maioria dos valores fica perto do centro; extremos s\u00e3o raros.",
            "Em variantes jur\u00eddicas, modela bem indicadores que somam muitos efeitos pequenos: notas de avalia\u00e7\u00e3o, \u00edndices, scores de risco.",
            "Cuidado: valor da causa raramente \u00e9 Normal (\u00e9 assim\u00e9trico, com cauda longa \u00e0 direita). N\u00e3o force a Normal onde ela n\u00e3o cabe.",
        ],
        citation="Wheelan (2016)",
        accent="Quando a Normal cabe e quando engana",
    )

    # 9. Poisson: contagem de eventos
    build_conceito(
        9,
        "Poisson: contagem em um per\u00edodo",
        [
            "Distribui\u00e7\u00e3o discreta de contagem: 0, 1, 2, 3 eventos em uma janela de tempo ou espa\u00e7o.",
            "Em jurimetria, modela bem a chegada de processos novos a uma vara, despachos por dia, audi\u00eancias por semana.",
            "Pergunta t\u00edpica: dada a m\u00e9dia hist\u00f3rica de 12 distribui\u00e7\u00f5es por dia em uma vara, qual a chance de um pico de 25 amanh\u00e3?",
        ],
        citation="Wheelan (2016); James et al. (2021)",
        accent="Modela volume",
    )

    # 10. Weibull: tempo at\u00e9 evento
    build_conceito(
        10,
        "Weibull: tempo at\u00e9 um evento",
        [
            "Distribui\u00e7\u00e3o positiva e assim\u00e9trica para tempo at\u00e9 a ocorr\u00eancia de um evento (sentencia, acordo, baixa).",
            "Lida bem com assimetria \u00e0 direita: muitos processos r\u00e1pidos, alguns muito longos. \u00c9 a base da an\u00e1lise de sobreviv\u00eancia que voltaremos a ver na Aula 4.",
            "Pergunta t\u00edpica: dado o hist\u00f3rico do XY&A, em quanto tempo metade das renovat\u00f3rias sai? Em quanto tempo 75% saem?",
        ],
        citation="James et al. (2021); Nunes (2019)",
        accent="Modela tempo",
    )

    # 11. Comparativo Normal x Poisson x Weibull
    build_tabela(
        11,
        "Normal, Poisson, Weibull lado a lado",
        ["Distribui\u00e7\u00e3o", "Tipo", "Vari\u00e1vel jur\u00eddica t\u00edpica"],
        [
            ["Normal", "Cont\u00ednua, sim\u00e9trica", "\u00cdndices, scores, notas."],
            ["Poisson", "Discreta, contagem", "Processos novos por dia/m\u00eas."],
            ["Weibull", "Cont\u00ednua, assim\u00e9trica", "Tempo at\u00e9 senten\u00e7a, acordo ou baixa."],
        ],
        citation="Wheelan (2016); James et al. (2021)",
        col_widths=[1700000, 2025000, 3225000],
    )

    # 12. Stat callout: % das renovat\u00f3rias que cabem em Weibull
    build_stat(
        12,
        "Forma t\u00edpica do tempo de tramita\u00e7\u00e3o",
        "~92%",
        "das renovat\u00f3rias do XY&A se ajustam razoavelmente a uma Weibull. A m\u00e9dia n\u00e3o serve, mas a forma da curva permite estimar prazos com mais defesa.",
        citation="James et al. (2021); CNJ (2024)",
    )

    # =================================================================
    # T\u00f3pico 02 \u2014 Etapa 6: apresenta\u00e7\u00e3o dos resultados
    # =================================================================

    # 13. Transi\u00e7\u00e3o 02
    build_transicao(
        13,
        "02",
        "Etapa 6: apresenta\u00e7\u00e3o",
        "Qual gr\u00e1fico responde a qual pergunta jurim\u00e9trica",
    )

    # 14. O gr\u00e1fico responde a uma pergunta
    build_conceito(
        14,
        "O gr\u00e1fico responde a uma pergunta",
        [
            "Etapa 6 n\u00e3o \u00e9 \"escolher um gr\u00e1fico bonito\". \u00c9 escolher o gr\u00e1fico que responde, da forma mais direta poss\u00edvel, \u00e0 pergunta investig\u00e1vel da Etapa 1.",
            "Antes de abrir o Excel, escreva a pergunta em uma linha. Sem pergunta clara, qualquer gr\u00e1fico parece interessante.",
            "Cada tipo de gr\u00e1fico responde bem a um tipo de pergunta. Usar o gr\u00e1fico errado for\u00e7a o leitor a fazer um trabalho que voc\u00ea deveria ter feito por ele.",
        ],
        citation="Wheelan (2016); Tufte (2001)",
    )

    # 15. Tabela: que gr\u00e1fico para qual pergunta
    build_tabela(
        15,
        "Que gr\u00e1fico para qual pergunta",
        ["Pergunta", "Gr\u00e1fico", "Exemplo XY&A"],
        [
            ["Comparar grupos", "Barras", "Procedencia por vara."],
            ["Evolu\u00e7\u00e3o no tempo", "Linhas", "Volume de a\u00e7\u00f5es por ano."],
            ["Forma da distribui\u00e7\u00e3o", "Histograma", "Valor da causa em renovat\u00f3rias."],
            ["Dispers\u00e3o e outliers", "Boxplot", "Tempo de tramita\u00e7\u00e3o por comarca."],
            ["Rela\u00e7\u00e3o entre 2 vari\u00e1veis", "Dispers\u00e3o", "Valor da causa vs. tempo at\u00e9 senten\u00e7a."],
        ],
        citation="Wheelan (2016)",
        col_widths=[1900000, 1500000, 2550000],
    )

    # 16. Barras
    build_conceito(
        16,
        "Barras: para comparar grupos",
        [
            "Use barras quando a pergunta \u00e9 \"qual grupo tem mais X?\". O olho compara comprimentos com facilidade.",
            "Ordene as barras por valor (do maior para o menor), n\u00e3o por ordem alfab\u00e9tica do nome do grupo.",
            "Em jurimetria: taxa de proced\u00eancia por vara, n\u00famero de processos por comarca, valor m\u00e9dio por tipo de a\u00e7\u00e3o.",
        ],
        citation="Tufte (2001); Wheelan (2016)",
    )

    # 17. Linhas
    build_conceito(
        17,
        "Linhas: para evolu\u00e7\u00e3o no tempo",
        [
            "Linhas conectam pontos ao longo de uma escala temporal. S\u00e3o a forma natural de mostrar tend\u00eancia.",
            "Evite mais de 4 a 5 linhas no mesmo gr\u00e1fico: vira espaguete e ningu\u00e9m enxerga padr\u00e3o.",
            "Em XY&A: volume mensal de novas a\u00e7\u00f5es de revis\u00e3o e renovat\u00f3ria, propor\u00e7\u00e3o de acordos por trimestre.",
        ],
        citation="Tufte (2001)",
    )

    # 18. Histograma
    build_conceito(
        18,
        "Histograma: para a forma da distribui\u00e7\u00e3o",
        [
            "Histograma mostra como os valores se distribuem em faixas. Revela assimetria, m\u00faltiplas modas e caudas pesadas.",
            "Escolha a largura do bin com cuidado: muito fina vira ru\u00eddo, muito grossa esconde estrutura.",
            "Em XY&A: histograma do valor da causa revela cauda longa e justifica usar mediana, n\u00e3o m\u00e9dia.",
        ],
        citation="Wheelan (2016)",
    )

    # 19. Boxplot
    build_conceito(
        19,
        "Boxplot: para dispers\u00e3o e outliers",
        [
            "Boxplot resume a distribui\u00e7\u00e3o em 5 n\u00fameros: m\u00ednimo, P25, mediana, P75, m\u00e1ximo. Outliers aparecem como pontos isolados.",
            "Permite comparar dispers\u00f5es entre grupos sem precisar mostrar a base inteira.",
            "Em XY&A: boxplot do tempo de tramita\u00e7\u00e3o por vara mostra qual juízo decide r\u00e1pido e qual decide errado.",
        ],
        citation="Wheelan (2016); James et al. (2021)",
    )

    # 20. Dispers\u00e3o (scatter)
    build_conceito(
        20,
        "Dispers\u00e3o: para rela\u00e7\u00e3o entre vari\u00e1veis",
        [
            "Cada ponto \u00e9 um processo; cada eixo, uma vari\u00e1vel. Revela rela\u00e7\u00f5es lineares, n\u00e3o-lineares e ag\u00f3lomera\u00e7\u00f5es.",
            "Cuidado com correla\u00e7\u00e3o: associa\u00e7\u00e3o n\u00e3o \u00e9 causalidade. Ver leitura cr\u00edtica adiante.",
            "Em XY&A: valor da causa vs. tempo at\u00e9 senten\u00e7a; tempo de tramita\u00e7\u00e3o vs. desfecho; rela\u00e7\u00f5es para suspeitar de padr\u00f5es.",
        ],
        citation="Wheelan (2016); Silver (2013)",
    )

    # =================================================================
    # T\u00f3pico 03 \u2014 Boas pr\u00e1ticas de visualiza\u00e7\u00e3o
    # =================================================================

    # 21. Transi\u00e7\u00e3o 03
    build_transicao(
        21,
        "03",
        "Boas pr\u00e1ticas",
        "O que comunica e o que distrai em um gr\u00e1fico jur\u00eddico",
    )

    # 22. 5 princ\u00edpios da boa visualiza\u00e7\u00e3o
    build_lista_numerada(
        22,
        "Cinco princ\u00edpios da boa visualiza\u00e7\u00e3o",
        [
            "Uma pergunta por gr\u00e1fico. T\u00edtulo do gr\u00e1fico \u00e9 a resposta em uma frase.",
            "Eixos rotulados, com unidade e per\u00edodo expl\u00edcitos.",
            "Sem 3D, sem efeitos de sombra, sem fatias decorativas.",
            "Cor com sem\u00e2ntica: navy = base, amarelo = destaque, cinza = comparativo.",
            "Citar a fonte da base (CNJ, TJSP, XY&A) no rodap\u00e9 do gr\u00e1fico.",
        ],
        citation="Tufte (2001); Wheelan (2016)",
    )

    # 23. O que comunica x o que distrai
    build_comparacao(
        23,
        "O que comunica e o que distrai",
        "Comunica",
        [
            "T\u00edtulo claro respondendo \u00e0 pergunta.",
            "Eixos com unidade e per\u00edodo.",
            "Cor com sem\u00e2ntica fixa.",
            "Anota\u00e7\u00f5es destacando o achado.",
        ],
        "Distrai",
        [
            "Efeitos 3D, sombras, gradientes.",
            "Legendas redundantes ou ausentes.",
            "Excesso de cores sem fun\u00e7\u00e3o.",
            "Linhas de grade densas demais.",
        ],
        citation="Tufte (2001)",
    )

    # 24. Mini-caso: gr\u00e1fico ruim x bom (XY&A)
    build_card(
        24,
        "XY&A: o mesmo dado, dois gr\u00e1ficos",
        "Como reescrever um gr\u00e1fico para o cliente",
        [
            "Gr\u00e1fico ruim: pizza 3D com 12 fatias coloridas, sem t\u00edtulo claro, ordenadas alfabeticamente. O cliente n\u00e3o sabe o que ler primeiro.",
            "Gr\u00e1fico bom: barras horizontais ordenadas pelo valor, t\u00edtulo \"As 5 comarcas com maior tempo de tramita\u00e7\u00e3o (XY&A, 2018-2024)\", anota\u00e7\u00e3o destacando o outlier.",
            "Mesmos dados, leituras opostas: o segundo j\u00e1 sugere a decis\u00e3o (\"reposicionar a equipe nessas 5 comarcas\"). O primeiro empurra a decis\u00e3o para o cliente.",
        ],
        citation="Tufte (2001); Wheelan (2016)",
        card_h=2400000,
        card_text_size=1300,
    )

    # =================================================================
    # T\u00f3pico 04 \u2014 Demonstra\u00e7\u00e3o em XY&A
    # =================================================================

    # 25. Transi\u00e7\u00e3o 04
    build_transicao(
        25,
        "04",
        "Demonstra\u00e7\u00e3o em XY&A",
        "Quatro perguntas, quatro gr\u00e1ficos sobre a base de loca\u00e7\u00e3o",
    )

    # 26. Pergunta 1: evolu\u00e7\u00e3o do volume por ano
    build_card(
        26,
        "Pergunta 1: volume por ano",
        "Gr\u00e1fico de linhas (volume por ano, 2010\u20132024)",
        [
            "Eixo X: ano de distribui\u00e7\u00e3o (2010-2024). Eixo Y: contagem de novas a\u00e7\u00f5es.",
            "Achado: queda de ~28% em 2020 e recupera\u00e7\u00e3o em 2022, com pico em 2023 (alta nos contratos comerciais).",
            "Decis\u00e3o derivada: dimensionar a equipe para o pico de 2023 ou ajustar para a m\u00e9dia hist\u00f3rica? O gr\u00e1fico mostra que o pico n\u00e3o se sustentou.",
        ],
        citation="CNJ (2024)",
        card_h=2200000,
    )

    # 27. Pergunta 2: tempo por vara (boxplot)
    build_card(
        27,
        "Pergunta 2: que vara decide mais r\u00e1pido?",
        "Boxplot do tempo de tramita\u00e7\u00e3o por vara",
        [
            "Eixo X: 5 varas com mais a\u00e7\u00f5es do XY&A. Eixo Y: tempo (dias) entre distribui\u00e7\u00e3o e senten\u00e7a.",
            "Achado: a Vara C parece r\u00e1pida na m\u00e9dia, mas a mediana mostra o contr\u00e1rio. Tem alguns extintos sem m\u00e9rito puxando a m\u00e9dia.",
            "Decis\u00e3o derivada: ajustar provis\u00e3o e estrat\u00e9gia de prazo pela mediana, n\u00e3o pela m\u00e9dia.",
        ],
        citation="Wheelan (2016)",
        card_h=2200000,
    )

    # 28. Pergunta 3: forma do valor (histograma)
    build_card(
        28,
        "Pergunta 3: qual a cara do valor da causa?",
        "Histograma do valor da causa (renovat\u00f3rias)",
        [
            "Eixo X: faixa de valor (em R$ mil). Eixo Y: contagem de processos por faixa.",
            "Achado: distribui\u00e7\u00e3o fortemente assim\u00e9trica \u00e0 direita. 80% dos casos abaixo de R$ 250 mil; cauda longa at\u00e9 R$ 18 milh\u00f5es.",
            "Decis\u00e3o derivada: comunicar valor t\u00edpico ao cliente pela mediana e P75, n\u00e3o pela m\u00e9dia. Provisionar por faixa.",
        ],
        citation="Wheelan (2016); Huff (2016)",
        card_h=2200000,
    )

    # 29. Pergunta 4: rela\u00e7\u00e3o desfecho x tipo de a\u00e7\u00e3o (barras agrupadas)
    build_card(
        29,
        "Pergunta 4: desfecho por tipo de a\u00e7\u00e3o",
        "Barras agrupadas: desfecho por tipo de a\u00e7\u00e3o",
        [
            "Eixo X: tipo de a\u00e7\u00e3o (revisional vs. renovat\u00f3ria). Cada grupo: barras coloridas para procedente, parcial, improcedente, extinto.",
            "Achado: renovat\u00f3rias t\u00eam ~12 pontos percentuais a mais de proced\u00eancia integral; revisionais t\u00eam mais extintos sem m\u00e9rito.",
            "Decis\u00e3o derivada: estrat\u00e9gia de tese diferenciada, com revis\u00e3o exigindo prepara\u00e7\u00e3o probat\u00f3ria mais s\u00f3lida desde a inicial.",
        ],
        citation="Nunes (2019); CNJ (2024)",
        card_h=2200000,
    )

    # =================================================================
    # T\u00f3pico 05 \u2014 Leitura cr\u00edtica de gr\u00e1ficos
    # =================================================================

    # 30. Transi\u00e7\u00e3o 05
    build_transicao(
        30,
        "05",
        "Leitura cr\u00edtica",
        "Como n\u00e3o ser enganado por gr\u00e1ficos",
    )

    # 31. Eixos truncados
    build_conceito(
        31,
        "Eixos truncados: o cl\u00e1ssico",
        [
            "Quando o eixo Y come\u00e7a em valor diferente de zero, diferen\u00e7as pequenas parecem enormes.",
            "Em barras, isso \u00e9 quase sempre um problema. Em linhas (s\u00e9rie temporal), pode ser leg\u00edtimo, mas exige rotular o corte.",
            "Em discusses jur\u00eddicas, eixo truncado vira \"prova\" pol\u00edtica de explos\u00e3o ou queda. Sempre confira de onde o eixo come\u00e7a.",
        ],
        citation="Huff (2016); Tufte (2001)",
    )

    # 32. Escala log
    build_conceito(
        32,
        "Escala log: amiga ou inimiga?",
        [
            "Escala log comprime ordens de grandeza. \u00datil quando os valores variam de R$ mil a R$ milh\u00f5es no mesmo gr\u00e1fico.",
            "Risco: para o leigo, escala log esconde o tamanho real da diferen\u00e7a. \"Sobe pouco no gr\u00e1fico\" pode ser \"multiplica por 10 na realidade\".",
            "Regra: escala log s\u00f3 com r\u00f3tulo expl\u00edcito (\"Eixo Y: log10\") e nota explicando o que cada passo significa.",
        ],
        citation="Wheelan (2016); Silver (2013)",
    )

    # 33. Correla\u00e7\u00f5es esp\u00farias
    build_conceito(
        33,
        "Correla\u00e7\u00f5es esp\u00farias",
        [
            "Correla\u00e7\u00e3o n\u00e3o \u00e9 causalidade. Duas s\u00e9ries podem subir juntas por acaso, por uma causa comum ou pela mesma tend\u00eancia temporal.",
            "Em jurimetria, \u00e9 f\u00e1cil correlacionar tempo de tramita\u00e7\u00e3o com qualquer indicador macroecon\u00f4mico se ambos crescerem com o tempo. Quase sempre \u00e9 espurio.",
            "Antes de afirmar causalidade, pergunte: existe um caminho concreto que liga A a B? Existe uma terceira vari\u00e1vel que explica os dois?",
        ],
        citation="Silver (2013); Huff (2016)",
    )

    # 34. As 4 armadilhas em um \u00fanico slide
    build_armadilhas(
        34,
        "As 4 armadilhas em gr\u00e1ficos",
        [
            ("Eixo Y truncado", "Diferen\u00e7a pequena vira montanha. Pergunte de onde o eixo come\u00e7a."),
            ("Escala log sem aviso", "Sobe pouco no papel, mas multiplica por 10 na realidade."),
            ("Cherry-picking de per\u00edodo", "2019-2021 conta uma hist\u00f3ria; 2010-2024, outra. Pe\u00e7a a s\u00e9rie toda."),
            ("Correla\u00e7\u00e3o como causalidade", "Duas curvas crescendo juntas n\u00e3o provam causa. Pe\u00e7a o mecanismo."),
        ],
        citation="Huff (2016); Silver (2013)",
        card_h=580000,
    )

    # =================================================================
    # Exerc\u00edcios dirigidos (2 mini-sequ\u00eancias)
    # =================================================================

    # 35. Exerc\u00edcio 1 \u2014 enunciado: escolher pergunta + gr\u00e1fico
    build_exercicio_enunciado(
        35,
        "Exerc\u00edcio 1: pergunta e gr\u00e1fico",
        "Voc\u00ea precisa apresentar 1 achado da base XY&A para um cliente locador em 1 minuto. Qual pergunta voc\u00ea responde e qual gr\u00e1fico voc\u00ea usa?",
        contexto="Lembre: 1 pergunta clara + 1 gr\u00e1fico que entrega a resposta + 1 decis\u00e3o concreta apoiada pelo achado.",
        citation="Wheelan (2016)",
    )

    # 36. Exerc\u00edcio 1 \u2014 resposta dirigida
    build_exercicio_resposta(
        36,
        "Exerc\u00edcio 1: resposta dirigida",
        "Que pergunta + gr\u00e1fico voc\u00ea apresenta ao cliente em 1 minuto?",
        [
            "Pergunta: qual a faixa t\u00edpica de valor de uma renovat\u00f3ria do XY&A e onde o caso do cliente cai dentro dela?",
            "Gr\u00e1fico: histograma do valor da causa, com linha vertical destacando o caso espec\u00edfico do cliente.",
            "Achado: 80% das renovat\u00f3rias ficam abaixo de R$ 250 mil; o caso do cliente est\u00e1 no P90.",
            "Decis\u00e3o apoiada: provis\u00e3o e estrat\u00e9gia de acordo calibradas para um caso fora do padr\u00e3o, n\u00e3o no \"caso m\u00e9dio\".",
        ],
        citation="Wheelan (2016); Nunes (2019)",
    )

    # 37. Exerc\u00edcio 2 \u2014 enunciado: an\u00e1lise mais \u00fatil para advogados imobili\u00e1rios
    build_exercicio_enunciado(
        37,
        "Exerc\u00edcio 2: an\u00e1lise para advogados imobili\u00e1rios",
        "Que an\u00e1lise descritiva sobre a base de loca\u00e7\u00e3o seria mais \u00fatil para um advogado imobili\u00e1rio que estima viabilidade de a\u00e7\u00e3o?",
        contexto="Pense em 1 indicador, 1 gr\u00e1fico e 1 leitura jur\u00eddica.",
        citation="Susskind (2023)",
    )

    # 38. Exerc\u00edcio 2 \u2014 resposta dirigida
    build_exercicio_resposta(
        38,
        "Exerc\u00edcio 2: resposta dirigida",
        "Qual an\u00e1lise descritiva mais \u00fatil para o advogado imobili\u00e1rio?",
        [
            "Indicador: taxa de proced\u00eancia integral em renovat\u00f3rias por comarca, considerando apenas casos PJ.",
            "Gr\u00e1fico: barras horizontais ordenadas, com cor destacando comarcas onde o XY&A atua.",
            "Leitura jur\u00eddica: comarcas com taxa baixa demandam mais prepara\u00e7\u00e3o probat\u00f3ria; taxa alta sugere viabilidade direta.",
            "Apoia decis\u00e3o: priorizar a\u00e7\u00f5es nas comarcas favor\u00e1veis e calibrar honor\u00e1rios e prazos nas demais.",
        ],
        citation="Susskind (2023); Nunes (2019)",
    )

    # =================================================================
    # Fechamento \u2014 S\u00edntese, Atividade Pr\u00e1tica 3, Ponte, Refer\u00eancias, Encerramento
    # =================================================================

    # 39. S\u00edntese
    build_sintese(
        39,
        [
            "Tr\u00eas distribui\u00e7\u00f5es bastam para a maior parte da jurimetria descritiva: Normal (valor), Poisson (volume), Weibull (tempo).",
            "O gr\u00e1fico responde a uma pergunta: barras comparam, linhas mostram tend\u00eancia, histograma revela forma, boxplot mostra dispers\u00e3o.",
            "Boas pr\u00e1ticas: 1 pergunta por gr\u00e1fico, eixos rotulados, sem 3D, cor com sem\u00e2ntica, fonte citada no rodap\u00e9.",
            "Leitura cr\u00edtica: cuidado com eixos truncados, escala log sem aviso, recortes de per\u00edodo e correla\u00e7\u00f5es esp\u00farias.",
            "O ciclo da Aula 2 e 3 fecha aqui em modo raiz: na Aula 5 ele volta com IA generativa em cada etapa.",
        ],
    )

    # 40. Atividade Pr\u00e1tica 3
    build_atividade_pratica(
        40,
        3,
        "Aplique as Etapas 4 a 6 a uma pergunta sobre a base XY&A",
        [
            "Escolha 1 pergunta investig\u00e1vel sobre a base XY&A (revis\u00e3o ou renovat\u00f3ria) e descreva, em at\u00e9 5 linhas, o tratamento m\u00ednimo necess\u00e1rio (Etapa 4) para respond\u00ea-la.",
            "Indique a medida descritiva (Etapa 5) e o tipo de gr\u00e1fico (Etapa 6) que voc\u00ea usaria, com 1 justificativa em uma frase para cada escolha.",
            "Escreva 1 frase de t\u00edtulo do gr\u00e1fico que j\u00e1 entregue a resposta ao cliente e nomeie 1 decis\u00e3o concreta que muda com o achado.",
        ],
    )

    # 41. Ponte para Aula 4
    build_ponte(
        41,
        "Da descri\u00e7\u00e3o \u00e0 infer\u00eancia",
        "Aula 4: testes de hip\u00f3tese e 4 modelos preditivos",
        [
            ("Infer\u00eancia", "p-valor e intervalo de confian\u00e7a com analogia jur\u00eddica."),
            ("Desfecho", "regress\u00e3o log\u00edstica para taxa de proced\u00eancia."),
            ("Tempo e valor", "sobreviv\u00eancia (Weibull volta) e estimativas de valor."),
            ("Acordo", "propens\u00e3o de acordo e faixa aceit\u00e1vel."),
        ],
        titulo="Ponte para a pr\u00f3xima aula",
        subtitulo="O que vem na semana que vem",
    )

    # 42. Refer\u00eancias
    build_referencias(
        42,
        [
            "TUFTE, E. R. The Visual Display of Quantitative Information. 2. ed. Cheshire: Graphics Press, 2001.",
            "WHEELAN, C. Estat\u00edstica: o que \u00e9, para que serve, como funciona. Rio de Janeiro: Zahar, 2016.",
            "HUFF, D. Como mentir com estat\u00edstica. Rio de Janeiro: Intr\u00ednseca, 2016. (Original: How to Lie with Statistics, 1954.)",
            "SILVER, N. O sinal e o ru\u00eddo: por que tantas previs\u00f5es falham e outras n\u00e3o. Rio de Janeiro: Intr\u00ednseca, 2013.",
            "JAMES, G.; WITTEN, D.; HASTIE, T.; TIBSHIRANI, R. An Introduction to Statistical Learning. 2. ed. New York: Springer, 2021.",
            "NUNES, M. Jurimetria: como a estat\u00edstica pode reinventar o Direito. 2. ed. S\u00e3o Paulo: Revista dos Tribunais, 2019.",
            "CONSELHO NACIONAL DE JUSTI\u00c7A. Justi\u00e7a em N\u00fameros 2024. Bras\u00edlia: CNJ, 2024.",
            "SUSSKIND, R. Tomorrow's Lawyers: An Introduction to Your Future. 3. ed. Oxford: Oxford University Press, 2023.",
        ],
    )

    # 43. Encerramento da Aula 3
    build_encerramento_aula(
        43,
        3,
        "Infer\u00eancia, 4 modelos preditivos e estrat\u00e9gia de acordo.",
        atividade_n=3,
    )

    update_content_types(43)
    update_presentation(43)
    print("OK 43 slides gerados.")

if __name__ == "__main__":
    main()
