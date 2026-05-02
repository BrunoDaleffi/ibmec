# ruff: noqa: E501
"""Gera o pptx de Aula 2 · Bloco 1 — O Ciclo da Ciência de Dados (Parte 1).

Lê /tmp/deck_aula2_bloco1/ (já desempacotado pelo unpack_pptx.py) e:
1. Sobrescreve slide1.xml com a capa do bloco.
2. Cria slide3..slide39 com cada layout customizado (39 slides no total).
3. Atualiza .rels (rId3 -> image1.png ou image2.png).
4. Atualiza [Content_Types].xml com Override para cada slideN.
5. Atualiza ppt/_rels/presentation.xml.rels com Relationship para cada slide.
6. Substitui o <p:sldIdLst> em ppt/presentation.xml na ordem desejada.

Não cria notesSlides (notas ficam para próxima iteração).

Pré-requisito: rodar antes
    uv run python .cursor/skills/build-aula-pptx/scripts/unpack_pptx.py \
        docs/templates/layout.pptx /tmp/deck_aula2_bloco1/

Depois:
    uv run python .cursor/skills/build-aula-pptx/scripts/pack_pptx.py \
        /tmp/deck_aula2_bloco1/ aulas/aula_02/slides/aula2_bloco1_jurimetria.pptx
"""

from __future__ import annotations

import re
from pathlib import Path

DECK = Path("/tmp/deck_aula2_bloco1")
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

NAVY = "1B2A4A"
YELLOW = "E8A317"
GREY = "666666"
TEXT = "333333"
LIGHT = "F4F4F4"
WHITE = "FFFFFF"

CONTENT_X_MIN = 750000
CONTENT_X_MAX = 6700000
CONTENT_W = CONTENT_X_MAX - CONTENT_X_MIN
CONTENT_Y_MIN = 600000
CONTENT_Y_MAX = 4500000


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


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
    """`runs` é uma lista de dicts: {text, sz, b, i, color, font}."""
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
    """Cada parágrafo é uma lista de runs."""
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


def title_box(sp_id: int, text: str) -> str:
    return text_box(
        sp_id,
        CONTENT_X_MIN,
        650000,
        CONTENT_W,
        850000,
        [{"text": text, "sz": 2400, "b": True, "color": NAVY, "font": "Arial Black"}],
        align="l",
    )


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


def slide_xml(spt_inner: str) -> str:
    return XML_HEADER + BG_BLOCK + TREE_OPEN + spt_inner + TREE_CLOSE + XML_FOOTER


def save_slide(n: int, body: str, *, image: int) -> None:
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


def build_capa(n: int, aula_bloco: str, tema_top: str, tema_bot: str) -> None:
    parts: list[str] = []
    parts.append(
        text_box(
            10,
            1097275,
            914400,
            6790500,
            1828800,
            [
                {
                    "text": "JURIMETRIA E ANÁLISE DE DADOS PARA DECISÕES ESTRATÉGICAS",
                    "sz": 3600,
                    "b": True,
                    "color": NAVY,
                    "font": "Arial Black",
                }
            ],
            anchor="ctr",
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
            500000,
            [
                {
                    "text": aula_bloco,
                    "sz": 2400,
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
            13,
            1097280,
            3450000,
            5486400,
            900000,
            [
                {
                    "text": tema_top,
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
            14,
            1097280,
            4000000,
            5486400,
            500000,
            [
                {
                    "text": tema_bot,
                    "sz": 1400,
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


def build_transicao(n: int, label: str, title: str, subtitle: str) -> None:
    parts: list[str] = []
    parts.append(
        text_box(
            20,
            1097280,
            1300000,
            5486400,
            450000,
            [
                {
                    "text": label,
                    "sz": 2000,
                    "b": True,
                    "color": YELLOW,
                    "font": "Arial Black",
                }
            ],
            anchor="ctr",
            align="l",
        )
    )
    parts.append(filled_rect(21, 1097280, 1800000, 1828800, 54864, YELLOW))
    parts.append(
        text_box(
            22,
            1097280,
            1950000,
            6500000,
            1300000,
            [
                {
                    "text": title,
                    "sz": 4000,
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
            23,
            1097280,
            3300000,
            6000000,
            500000,
            [
                {
                    "text": subtitle,
                    "sz": 1600,
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


def build_encerramento(n: int) -> None:
    parts: list[str] = []
    parts.append(
        text_box(
            30,
            1097280,
            1500000,
            5486400,
            900000,
            [
                {
                    "text": "Obrigado!",
                    "sz": 6000,
                    "b": True,
                    "color": NAVY,
                    "font": "Arial Black",
                }
            ],
            anchor="ctr",
            align="l",
        )
    )
    parts.append(filled_rect(31, 1097280, 2700000, 1828800, 54864, YELLOW))
    parts.append(
        text_box(
            32,
            1097280,
            2800000,
            5486400,
            600000,
            [
                {
                    "text": "Perguntas?",
                    "sz": 3200,
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
            33,
            1097280,
            3500000,
            5486400,
            400000,
            [
                {
                    "text": "Aula 2 · Bloco 1 · IBMEC",
                    "sz": 1400,
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


def build_lista_numerada(
    n: int,
    title: str,
    items: list[str],
    *,
    citation: str | None = None,
    item_size: int = 1500,
) -> None:
    parts: list[str] = [title_box(40, title)]
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
            41,
            CONTENT_X_MIN,
            1650000,
            CONTENT_W,
            2700000,
            paragraphs,
            line_spc=115000,
            para_spc_before=600,
        )
    )
    if citation:
        parts.append(footer_citation(42, citation))
    save_slide(n, "".join(parts), image=1)


def build_objetivos(n: int, title: str, items: list[str]) -> None:
    parts: list[str] = [title_box(40, title)]
    paragraphs = [
        [
            {
                "text": "✓  ",
                "sz": 1800,
                "b": True,
                "color": YELLOW,
                "font": "Arial Black",
            },
            {"text": txt, "sz": 1800, "color": TEXT, "font": "Arial"},
        ]
        for txt in items
    ]
    parts.append(
        multi_para_box(
            41,
            CONTENT_X_MIN,
            1700000,
            CONTENT_W,
            2500000,
            paragraphs,
            line_spc=130000,
            para_spc_before=800,
        )
    )
    save_slide(n, "".join(parts), image=1)


def build_conceito(
    n: int,
    title: str,
    paragraphs_text: list[str],
    *,
    citation: str | None = None,
    accent: str | None = None,
) -> None:
    parts: list[str] = [title_box(40, title)]
    if accent:
        parts.append(
            text_box(
                41,
                CONTENT_X_MIN,
                1620000,
                CONTENT_W,
                400000,
                [
                    {
                        "text": accent,
                        "sz": 1600,
                        "b": True,
                        "color": YELLOW,
                        "font": "Arial Black",
                    }
                ],
                align="l",
            )
        )
        body_y = 2050000
    else:
        body_y = 1700000

    paragraphs = [
        [{"text": p, "sz": 1600, "color": TEXT, "font": "Arial"}] for p in paragraphs_text
    ]
    parts.append(
        multi_para_box(
            42,
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
        parts.append(footer_citation(43, citation))
    save_slide(n, "".join(parts), image=1)


def build_card(
    n: int,
    title: str,
    card_title: str,
    card_paragraphs: list[str],
    *,
    citation: str | None = None,
    card_h: int = 2550000,
    card_title_size: int = 1800,
    card_text_size: int = 1500,
) -> None:
    parts: list[str] = [title_box(40, title)]
    card_paras = [
        [
            {
                "text": card_title,
                "sz": card_title_size,
                "b": True,
                "color": NAVY,
                "font": "Arial Black",
            }
        ]
    ]
    for p in card_paragraphs:
        card_paras.append(
            [{"text": p, "sz": card_text_size, "color": TEXT, "font": "Arial"}]
        )
    parts.append(
        filled_rect(
            41,
            CONTENT_X_MIN + 50000,
            1650000,
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
        parts.append(footer_citation(42, citation))
    save_slide(n, "".join(parts), image=1)


def build_stat(
    n: int,
    title: str,
    big_number: str,
    label: str,
    *,
    citation: str | None = None,
) -> None:
    parts: list[str] = [title_box(40, title)]
    parts.append(
        text_box(
            41,
            CONTENT_X_MIN,
            1750000,
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
            42,
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
        parts.append(footer_citation(43, citation))
    save_slide(n, "".join(parts), image=1)


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
    parts: list[str] = [title_box(40, title)]
    col_w = 2870000
    gap = 210000
    left_x = CONTENT_X_MIN
    right_x = CONTENT_X_MIN + col_w + gap
    header_y = 1650000
    header_h = 480000
    body_y = header_y + header_h
    body_h = 2300000

    max_len = max((len(s) for s in left_items + right_items), default=0)
    if max_len > 80:
        item_size = 1200
    elif max_len > 50:
        item_size = 1300
    else:
        item_size = 1500

    parts.append(
        filled_rect(
            41,
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
            42,
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
            43,
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
            44,
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
        parts.append(footer_citation(45, citation))
    save_slide(n, "".join(parts), image=1)


def build_diagrama_6_etapas(
    n: int,
    title: str,
    etapas: list[str],
    *,
    destaque: int | None = None,
    citation: str | None = None,
) -> None:
    parts: list[str] = [title_box(40, title)]
    nodes = 6
    diam = 700000
    spacing = (CONTENT_W - diam) / (nodes - 1)
    y_circ = 1900000
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
    save_slide(n, "".join(parts), image=1)


def build_tabela(
    n: int,
    title: str,
    header: list[str],
    rows: list[list[str]],
    *,
    citation: str | None = None,
    col_widths: list[int] | None = None,
) -> None:
    parts: list[str] = [title_box(40, title)]

    n_cols = len(header)
    if col_widths is None:
        col_widths = [CONTENT_W // n_cols] * n_cols
    assert len(col_widths) == n_cols

    row_h = 330000
    header_h = 380000
    base_y = 1650000

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
    save_slide(n, "".join(parts), image=1)


def build_armadilhas(
    n: int,
    title: str,
    items: list[tuple[str, str]],
    *,
    citation: str | None = None,
) -> None:
    parts: list[str] = [title_box(40, title)]
    card_h = 830000
    gap = 50000
    base_y = 1650000

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
                            "sz": 1500,
                            "b": True,
                            "color": NAVY,
                            "font": "Arial Black",
                        }
                    ],
                    [{"text": body, "sz": 1250, "color": TEXT, "font": "Arial"}],
                ],
                text_align="l",
                text_anchor="t",
            )
        )

    if citation:
        parts.append(footer_citation(80, citation))
    save_slide(n, "".join(parts), image=1)


def build_correcao_questao(
    n: int,
    questao_num: int,
    enunciado: str,
    pontos: list[str],
    *,
    citation: str | None = None,
) -> None:
    """Slide de correção de uma questão da atividade anterior.

    Layout: título, caixa amarela com o enunciado da questão e bullets
    com o caminho de resposta esperado, exemplo XY&A e armadilhas.
    Usado no Bloco 1 das Aulas 2 a 5 (1 slide por questão, sempre 3 questões).
    """
    parts: list[str] = [title_box(40, f"Atividade 1 · Questão {questao_num}")]
    parts.append(
        filled_rect(
            41,
            CONTENT_X_MIN + 50000,
            1620000,
            CONTENT_W - 100000,
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
                "sz": 1300,
                "b": True,
                "color": YELLOW,
                "font": "Arial Black",
            },
            {"text": p, "sz": 1300, "color": TEXT, "font": "Arial"},
        ]
        for p in pontos
    ]
    parts.append(
        multi_para_box(
            42,
            CONTENT_X_MIN,
            2380000,
            CONTENT_W,
            1900000,
            paragraphs,
            line_spc=118000,
            para_spc_before=350,
        )
    )
    if citation:
        parts.append(
            text_box(
                43,
                CONTENT_X_MIN,
                4400000,
                CONTENT_W,
                170000,
                [{"text": citation, "sz": 1000, "i": True, "color": GREY, "font": "Arial"}],
                align="l",
                anchor="b",
            )
        )
    save_slide(n, "".join(parts), image=1)


def build_atividade(
    n: int,
    titulo_curto: str,
    enunciado: list[str],
    lembrete: str,
) -> None:
    parts: list[str] = [title_box(40, titulo_curto)]
    parts.append(
        text_box(
            41,
            CONTENT_X_MIN,
            1620000,
            CONTENT_W,
            400000,
            [
                {
                    "text": "Entrega até a Aula 3",
                    "sz": 1500,
                    "b": True,
                    "color": YELLOW,
                    "font": "Arial Black",
                }
            ],
            align="l",
        )
    )
    paragraphs = [
        [
            {
                "text": "▶  ",
                "sz": 1400,
                "b": True,
                "color": YELLOW,
                "font": "Arial Black",
            },
            {"text": item, "sz": 1400, "color": TEXT, "font": "Arial"},
        ]
        for item in enunciado
    ]
    parts.append(
        multi_para_box(
            42,
            CONTENT_X_MIN,
            2050000,
            CONTENT_W,
            1900000,
            paragraphs,
            line_spc=125000,
            para_spc_before=500,
        )
    )
    parts.append(
        text_box(
            43,
            CONTENT_X_MIN,
            4100000,
            CONTENT_W,
            350000,
            [
                {
                    "text": lembrete,
                    "sz": 1100,
                    "i": True,
                    "color": GREY,
                    "font": "Arial",
                }
            ],
            align="l",
        )
    )
    save_slide(n, "".join(parts), image=1)


def build_referencias(n: int, title: str, items: list[str]) -> None:
    parts: list[str] = [title_box(40, title)]
    paragraphs = [[{"text": item, "sz": 1100, "color": TEXT, "font": "Arial"}] for item in items]
    parts.append(
        multi_para_box(
            41,
            CONTENT_X_MIN,
            1650000,
            CONTENT_W,
            2700000,
            paragraphs,
            line_spc=120000,
            para_spc_before=400,
            bullet="•",
            bullet_color=NAVY,
        )
    )
    save_slide(n, "".join(parts), image=1)


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


def main() -> None:
    SLIDES.mkdir(parents=True, exist_ok=True)
    RELS.mkdir(parents=True, exist_ok=True)

    build_capa(
        1,
        "Aula 2 · Bloco 1",
        "O Ciclo da Ciência de Dados Aplicado ao Direito (Parte 1)",
        "Do problema à coleta: perguntar e mapear no modo raiz",
    )

    build_lista_numerada(
        2,
        "Agenda do Bloco",
        [
            "Correção das 3 questões da Atividade 1",
            "Visão geral das 6 etapas do ciclo",
            "Por que pensar em ciclo importa",
            "Etapa 1: transformar pergunta jurídica em investigável",
            "Critérios de boa pergunta e exemplos práticos",
            "Etapa 2: mapear as informações necessárias",
            "Demonstração: variáveis na base de locação do TJSP",
            "Exercício dirigido e fechamento da Etapa 2",
        ],
        item_size=1500,
    )

    build_objetivos(
        3,
        "Objetivos de aprendizagem",
        [
            "Compreender o ciclo da ciência de dados aplicado ao Direito em suas 6 etapas",
            "Reconhecer os critérios de uma pergunta jurimétrica investigável",
            "Reescrever uma pergunta jurídica vaga em pergunta de dados",
            "Mapear, a partir de uma pergunta, as variáveis e fontes necessárias",
        ],
    )

    build_card(
        4,
        "Onde estamos no curso",
        "Da fundamentação ao método",
        [
            "Na Aula 1, vimos por que dados importam para o operador do Direito e o que é Jurimetria.",
            "Agora começa o método: o ciclo da ciência de dados em modo raiz, que será percorrido nas Aulas 2 e 3.",
            "Toda a aula opera sobre a base do trabalho final (16.110 julgados de locação do TJSP) e sobre o caso XY&A.",
        ],
        citation="Nunes (2019); CNJ (2024)",
    )

    build_transicao(
        5,
        "Tópico 1",
        "Atividade 1: o que aprendemos",
        "Correção comentada das 3 questões e ponte para o método desta aula",
    )

    build_card(
        6,
        "O que foi pedido na Atividade 1",
        "Atividade Prática 1 (Bloco 2 da Aula 1) · 3 questões",
        [
            "Pano de fundo: caso XY&A e a base de 16.110 julgados de locação do TJSP, sobre os fundamentos de dados da Aula 1.",
            "Q1. Listar 3 perguntas jurimétricas do XY&A em ao menos 2 áreas (contencioso, gestão, provisionamento).",
            "Q2. Reescrever uma das 3 perguntas em formato investigável (tema, recorte, variável central, comparação).",
            "Q3. Apontar que decisão concreta do escritório a resposta apoiaria, e por quê.",
        ],
        card_h=2650000,
        card_title_size=1700,
        card_text_size=1400,
    )

    build_correcao_questao(
        7,
        1,
        "Q1. Listar 3 perguntas jurimétricas do XY&A em ao menos 2 áreas (contencioso, gestão, provisionamento).",
        [
            "Caminho de resposta: cobrir pelo menos 2 das 3 áreas e dar a cada pergunta um recorte mínimo (matéria, jurisdição ou período).",
            "Exemplos no XY&A: contencioso, 'taxa de procedência por vara em revisão'; gestão, 'concentração de despejos por comarca'; provisão, 'valor mediano de condenação'.",
            "Armadilhas frequentes: 3 perguntas todas no mesmo plano operacional, perguntas de opinião sem variável, ou perguntas grandes demais sem ancoragem.",
        ],
        citation="Nunes (2019); ABJ (relatórios)",
    )

    build_correcao_questao(
        8,
        2,
        "Q2. Reescrever uma das 3 perguntas em formato investigável: tema, recorte, variável central e comparação.",
        [
            "Caminho de resposta: tema = matéria e tipo de ação; recorte = jurisdição e período; variável central = o que será medido (taxa, mediana, valor); comparação = média ou outro grupo.",
            "Exemplo XY&A: 'Em renovatórias do TJSP, parte PJ, 2018 a 2024, qual a taxa de procedência em favor do locador?'.",
            "Armadilhas frequentes: pergunta 'investigável' que ainda mistura opinião e métrica, ausência de ponto de comparação ou recorte vago.",
        ],
        citation="Nunes (2019); Katz e Bommarito (2013)",
    )

    build_correcao_questao(
        9,
        3,
        "Q3. Que decisão concreta do escritório (litígio, negociação, provisionamento, gestão) a resposta apoiaria, e por quê.",
        [
            "Caminho de resposta: nomear uma decisão específica que mudaria com a resposta. Exemplos: política de acordo, recalibrar provisão, redistribuir equipe, mudar tese.",
            "Exemplo XY&A: se a taxa de procedência em renovatórias caiu, a decisão pode ser revisar a estratégia de litígio e priorizar acordos.",
            "Armadilhas frequentes: respostas vagas como 'a empresa fica mais informada', sem nomear a decisão concreta que muda.",
        ],
        citation="Susskind (2023); Nunes (2019)",
    )

    build_conceito(
        10,
        "Da pergunta solta à pergunta de dados",
        [
            "Toda intuição jurídica relevante pode ser convertida em uma pergunta investigável.",
            "Quando a pergunta é boa, a sequência fica clara: variáveis, fonte, coleta, análise e entrega. É o ciclo da próxima seção.",
            "Quando a pergunta é ruim, qualquer dado parece interessante. É aí que estatística vira marketing.",
        ],
        citation="Huff (2016); Silver (2013)",
        accent="Insight do Bloco e ponte para o ciclo",
    )

    build_transicao(
        11,
        "Tópico 2",
        "O ciclo da ciência de dados",
        "Visão geral das 6 etapas que estruturam o resto do curso",
    )

    build_conceito(
        12,
        "O que é o ciclo",
        [
            "É a espinha dorsal metodológica da disciplina: 6 etapas executadas em sequência, com idas e voltas controladas.",
            "Será percorrido duas vezes: primeiro no modo raiz (Aulas 2 e 3, com Excel) e depois no modo com IA (Aula 5).",
            "Em sala, sempre que abrirmos uma análise, vamos identificar em que etapa estamos.",
        ],
        citation="Nunes (2019); James et al. (2021)",
    )

    build_diagrama_6_etapas(
        13,
        "As 6 etapas do ciclo",
        [
            "Pergunta",
            "Mapear",
            "Coletar",
            "Tratar",
            "Analisar",
            "Apresentar",
        ],
        citation="Nunes (2019)",
    )

    build_card(
        14,
        "Etapas 1 e 2: pergunta e mapeamento",
        "Onde tudo começa",
        [
            "Etapa 1, transformar a pergunta jurídica em pergunta investigável: foco do bloco de hoje.",
            "Etapa 2, mapear as informações necessárias: identificar quais variáveis e fontes responderiam à pergunta.",
            "Sem essas duas etapas bem feitas, todo o resto do ciclo fica frágil ou enviesado.",
        ],
        citation="Nunes (2019)",
    )

    build_card(
        15,
        "Etapas 3 e 4: coletar e tratar",
        "Construindo a base analítica",
        [
            "Etapa 3, coletar: fontes públicas (DataJud, tribunais), internas (sistemas) e, quando preciso, scraping.",
            "Etapa 4, tratar: padronizar datas, valores, classificações e textos em uma TABELA estruturada e saneada.",
            "Veremos as duas em detalhe no Bloco 2 (coleta) e na Aula 3 (tratamento).",
        ],
        citation="CNJ (2024)",
    )

    build_card(
        16,
        "Etapas 5 e 6: analisar e apresentar",
        "Da TABELA ao insight",
        [
            "Etapa 5, analisar: estatística descritiva no Excel. Medidas de posição, dispersão e gráficos.",
            "Etapa 6, apresentar: gráficos e tabelas com boas práticas de visualização para o público jurídico.",
            "Aprofundamos as duas na Aula 3 e voltamos a elas na Aula 5 com IA generativa.",
        ],
        citation="Wheelan (2016)",
    )

    build_comparacao(
        17,
        "Por que pensar em ciclo?",
        "Sem método (pura intuição)",
        [
            "Resultado depende da pessoa, não do processo.",
            "Difícil de replicar e auditar.",
            "Indefensável quando contestado em juízo.",
            "Decisões aleatórias, sem rastro.",
        ],
        "Com ciclo (método reproduzível)",
        [
            "Mesmo procedimento gera mesma resposta.",
            "Cada etapa documentada e revisável.",
            "Defensável: mostra como se chegou ao número.",
            "Permite escalar para a equipe inteira.",
        ],
        citation="Nunes (2019); Susskind (2023)",
    )

    build_conceito(
        18,
        "Cadeia de custódia: do processo ao dado",
        [
            "No processo penal, a cadeia de custódia garante que a prova chegue íntegra ao julgamento.",
            "Na Jurimetria, o ciclo cumpre o mesmo papel: cada etapa preserva e documenta a integridade dos dados.",
            "Quem pula etapas perde rastreabilidade. Quem documenta, defende a análise como defenderia uma prova pericial.",
        ],
        citation="Nunes (2019); CNJ (2024)",
        accent="Analogia jurídica",
    )

    build_transicao(
        19,
        "Tópico 3",
        "Etapa 1: transformar a pergunta",
        "Da pergunta jurídica vaga à pergunta investigável",
    )

    build_conceito(
        20,
        "O que é uma pergunta investigável",
        [
            "É uma pergunta que aponta com clareza para um dado mensurável e para um critério de resposta.",
            "Em vez de pedir uma opinião, pede uma comparação, uma proporção, uma frequência ou uma evolução.",
            "Sem pergunta investigável, qualquer análise ou IA tende a produzir um número aparentemente preciso, mas sem ancoragem.",
        ],
        citation="Nunes (2019); Katz e Bommarito (2013)",
    )

    build_card(
        21,
        "Critérios de uma boa pergunta",
        "4 critérios não negociáveis",
        [
            "Específica: define matéria, período e jurisdição.",
            "Verificável: aponta para uma variável que existe ou é coletável.",
            "Comparável: traz um ponto de referência (média, outro juízo, outro período).",
            "Útil: a resposta muda alguma decisão concreta de litígio, negociação ou provisão.",
        ],
        citation="Nunes (2019); Katz e Bommarito (2013)",
    )

    build_comparacao(
        22,
        "Antes e depois",
        "Pergunta vaga",
        [
            "Esse juiz é duro?",
            "Renovatórias demoram mais?",
            "Vale a pena recorrer?",
            "Acordos saem por quanto?",
        ],
        "Pergunta investigável",
        [
            "Revisões no TJSP, 2018–2024: a taxa de procedência do juízo X difere da média?",
            "Renovatórias: o tempo mediano até sentença subiu entre 2019 e 2024 na Capital?",
            "Recursos de revisão, 2020–2024: qual a proporção de reformas a favor do recorrente?",
            "Acordos, 2022–2024: o valor acordado é qual fração do valor da causa?",
        ],
        citation="Nunes (2019); ABJ (relatórios)",
    )

    build_stat(
        23,
        "O alcance da pergunta certa",
        "16.110",
        "julgados de revisão e renovatória de locação do TJSP, 2010 a 2024 (parte PJ), à disposição do XY&A para responder boas perguntas.",
        citation="CNJ (2024); TJSP",
    )

    build_armadilhas(
        24,
        "Armadilhas comuns ao formular perguntas",
        [
            (
                "Pergunta de mão dupla disfarçada",
                "Pedir 'taxa de êxito' sem definir o que conta como êxito (procedência total, parcial, acordo) inviabiliza a contagem.",
            ),
            (
                "Comparar sem grupo de controle",
                "'Esse juiz decide pior?' sem referência: pior comparado a quê? Sempre fixe o ponto de comparação antes de coletar.",
            ),
            (
                "Pergunta interessante e impossível",
                "Variáveis necessárias não estão na base nem em fonte pública. Cheque viabilidade na Etapa 2 antes de prometer resposta.",
            ),
        ],
        citation="Huff (2016); Silver (2013)",
    )

    build_card(
        25,
        "Mini-caso XY&A",
        "Da intuição à pergunta investigável",
        [
            "Intuição do sócio: 'estamos perdendo mais renovatórias do que antes'.",
            "Pergunta investigável: nas renovatórias do TJSP, 2018–2024, com parte PJ, qual a evolução anual da taxa de procedência em favor do locador?",
            "Variáveis necessárias (já aparecem na Etapa 2): tipo de ação, ano da sentença, parte, desfecho.",
        ],
    )

    build_card(
        26,
        "Síntese da Etapa 1",
        "Checklist da boa pergunta",
        [
            "Especifiquei matéria, jurisdição e período?",
            "Defini a variável central da resposta (taxa, mediana, evolução)?",
            "Tenho um ponto de comparação (média, outra vara, outro ano)?",
            "Sei qual decisão concreta vai mudar com a resposta?",
        ],
        citation="Nunes (2019)",
    )

    build_transicao(
        27,
        "Tópico 4",
        "Etapa 2: mapear as informações",
        "Que variáveis responderiam à pergunta?",
    )

    build_conceito(
        28,
        "O que significa mapear",
        [
            "Mapear é traduzir a pergunta em variáveis concretas: cada palavra-chave da pergunta vira uma coluna da futura tabela.",
            "Variáveis vêm de duas perguntas espelhadas: o que precisa estar na linha (cada processo, cada sentença) e o que precisa estar na coluna (cada atributo).",
            "Sem mapeamento, a coleta vira pesca: se traz tudo, complica; se traz pouco, falta para responder.",
        ],
        citation="Nunes (2019); Wheelan (2016)",
    )

    build_comparacao(
        29,
        "Tipos de variável (revisita da Aula 1)",
        "Categóricas",
        [
            "Tipo de ação: revisão ou renovatória.",
            "Comarca, vara, classe processual.",
            "Desfecho: procedência, improcedência, acordo, extinção.",
            "Parte: pessoa jurídica ou física.",
        ],
        "Numéricas e temporais",
        [
            "Valor da causa, valor de condenação, valor acordado.",
            "Data de distribuição, data da sentença, data de baixa.",
            "Tempo de tramitação, em dias.",
            "Quantidade de recursos, de partes, de audiências.",
        ],
        citation="Wheelan (2016)",
    )

    build_tabela(
        30,
        "Variáveis disponíveis na base TJSP",
        ["Variável", "Tipo", "O que ela permite responder"],
        [
            ["Tipo de ação", "Categórica", "Comparar revisão x renovatória"],
            ["Comarca / vara", "Categórica", "Concentração geográfica e por juízo"],
            ["Data de distribuição", "Temporal", "Volume e sazonalidade ao longo do tempo"],
            ["Data da sentença", "Temporal", "Tempo de tramitação"],
            ["Desfecho", "Categórica", "Taxa de êxito por recorte"],
            ["Valor da causa", "Numérica", "Distribuição financeira da carteira"],
        ],
        citation="CNJ / DataJud (2024); TJSP",
        col_widths=[1700000, 1300000, 2950000],
    )

    build_card(
        31,
        "De pergunta a variáveis",
        "Exemplo prático",
        [
            "Pergunta: o tempo mediano até a sentença em renovatórias do TJSP cresceu de 2019 a 2024?",
            "Variáveis necessárias: tipo de ação (renovatória), data de distribuição, data de sentença, ano da sentença.",
            "Operação derivada: tempo de tramitação = data de sentença − data de distribuição. Mediana por ano da sentença.",
        ],
        citation="CNJ (2024); Wheelan (2016)",
    )

    build_lista_numerada(
        32,
        "Três exemplos de mapeamento",
        [
            "Pergunta: existe diferença entre acordos e sentenças no valor envolvido? → tipo de ação, desfecho, valor da causa, valor de condenação ou acordado.",
            "Pergunta: há concentração de ações em poucas varas? → comarca, vara, ano de distribuição.",
            "Pergunta: a taxa de procedência mudou após 2020? → tipo de ação, ano da sentença, desfecho.",
        ],
        citation="Nunes (2019); ABJ (relatórios)",
        item_size=1300,
    )

    build_card(
        33,
        "Exercício dirigido em sala",
        "10 minutos · em duplas",
        [
            "Escolha uma das 4 perguntas investigáveis do slide 'Antes e depois' (slide 22).",
            "Liste em uma folha as variáveis necessárias para respondê-la, separando categóricas, numéricas e temporais.",
            "Indique se cada variável existe na base do XY&A, se viria de fonte pública (DataJud, CNJ) ou se precisaria ser construída.",
        ],
    )

    build_conceito(
        34,
        "Tudo começa com uma TABELA",
        [
            "Para iniciar a análise, basta uma tabela: 1 linha por unidade de observação (em geral, um processo) e 1 coluna por variável.",
            "Linhas comparáveis e colunas com valores no mesmo formato. Datas como datas, valores como números, categorias como categorias.",
            "Toda análise descritiva da Aula 3, e todos os modelos da Aula 4, partem dessa mesma forma: linhas e colunas saneadas.",
        ],
        citation="Wheelan (2016); Nunes (2019)",
        accent="Insight da Etapa 2",
    )

    build_conceito(
        35,
        "Tabela analítica como petição inicial",
        [
            "A petição inicial define o que está em juízo. Tudo o que não estiver nela, em regra, não pode ser decidido.",
            "A tabela analítica define o que pode ser respondido. Tudo o que não estiver nela, em regra, não pode ser analisado.",
            "Por isso, mapear bem na Etapa 2 é desenhar a competência da análise, antes de qualquer coleta.",
        ],
        citation="Nunes (2019)",
        accent="Analogia jurídica",
    )

    build_lista_numerada(
        36,
        "Síntese do Bloco 1",
        [
            "Toda análise jurimétrica começa por uma pergunta investigável e termina em uma decisão concreta.",
            "O ciclo de 6 etapas é o método reproduzível, rastreável e defensável que sustenta cada análise.",
            "Etapa 1: pergunta específica, verificável, comparável e útil.",
            "Etapa 2: tabela com 1 linha por processo e 1 coluna por variável, saneada e completa.",
        ],
        citation="Nunes (2019); Wheelan (2016)",
        item_size=1500,
    )

    build_card(
        37,
        "Ponte para o Bloco 2",
        "O que vem agora",
        [
            "No próximo bloco entramos na Etapa 3 do ciclo: coletar as informações em fontes públicas (DataJud, tribunais), internas, scraping e APIs.",
            "Discutiremos LGPD, vieses de amostragem e como foi montada a base dos 16.110 julgados do XY&A.",
            "Ao final do Bloco 2 vem a Atividade Prática 2, com 3 questões (entrega até a Aula 3).",
        ],
    )

    # Atividade Prática 2 não vai aqui: por regra, atividade só aparece no
    # Bloco 2 das aulas, e sempre com 3 questões numeradas. Ela será
    # apresentada no slide de Atividade do build_aula2_bloco2.py.

    build_referencias(
        38,
        "Referências do bloco",
        [
            "NUNES, Marcelo Guedes. Jurimetria: como a estatística pode reinventar o Direito. 2. ed. São Paulo: Revista dos Tribunais, 2019.",
            "WHEELAN, Charles. Estatística: o que é, para que serve, como funciona. Rio de Janeiro: Zahar, 2016.",
            "HUFF, Darrell. Como mentir com estatística. Rio de Janeiro: Intrínseca, 2016.",
            "SILVER, Nate. O sinal e o ruído. Rio de Janeiro: Intrínseca, 2013.",
            "KATZ, Daniel Martin; BOMMARITO, Michael J. Quantitative Legal Prediction. Emory Law Journal, v. 62, 2013.",
            "CONSELHO NACIONAL DE JUSTIÇA (CNJ). Justiça em Números e painéis do DataJud, 2024.",
            "ASSOCIAÇÃO BRASILEIRA DE JURIMETRIA (ABJ). Relatórios e publicações em abj.org.br.",
            "SUSSKIND, Richard. Tomorrow's Lawyers. 3rd ed. Oxford University Press, 2023.",
            "JAMES, Gareth et al. An Introduction to Statistical Learning. 2nd ed. Springer, 2021.",
        ],
    )

    build_encerramento(39)

    update_content_types(39)
    update_presentation(39)
    print("OK 39 slides gerados.")


if __name__ == "__main__":
    main()
