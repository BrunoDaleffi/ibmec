# ruff: noqa: E501
"""Gera o pptx de Aula 2 · Bloco 1 — O Ciclo da Ciência de Dados (Parte 1).

Layout canônico replicado da Aula 1 publicada (ver
`.cursor/skills/build-aula-pptx/layout-canonical.md`).

Convenção de fundos:
- image1.png → capa, transição de tópico (01, 02, …) e encerramento ("Fim do Bloco N").
- image2.png → todos os demais slides (agenda, objetivos, conexão, conteúdo,
  síntese, ponte, referências, slides de correção).

O `layout.pptx` original tem o mapeamento invertido tanto nas rels quanto nos
arquivos de mídia em si: o que está salvo como `image1.png` é o fundo "suave"
(conteúdo) e o que está salvo como `image2.png` é o fundo "forte" (capa). Para
alinhar à convenção da Aula 1 publicada (image1=capa/transição/fim,
image2=conteúdo), `swap_media_para_aula1()` troca os dois arquivos físicos no
deck desempacotado antes da geração dos slides.

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

# Paleta canônica
NAVY = "1B2A4A"
YELLOW = "E8A317"
GREY = "666666"
TEXT = "333333"
LIGHT = "F4F4F4"
PASTEL = "FCE5CD"
WHITE = "FFFFFF"

# Cabeçalho padrão da Aula 1 (slides estruturais).
# Largura `H1_W=6700800` é a medida exata do gold standard B1 slide 3
# (Agenda do Bloco). Soft limit do `check_useful_area`: x ≤ 7700000.
H1_X = 750000
H1_Y = 500000
H1_W = 6700800
H1_H = 900000
H1_SZ = 2400

FAIXA_X = 750005
FAIXA_Y = 905100
FAIXA_W = 1500000
FAIXA_H = 54900

SUB_X = 750000
SUB_Y = 1330000
SUB_W = 6700800
SUB_H = 400000
SUB_SZ = 1400

CONTENT_X_MIN = 750000
CONTENT_X_MAX = 7700000  # soft limit (gold standard agenda chega a x≈7929372 com itens à direita)
CONTENT_W = CONTENT_X_MAX - CONTENT_X_MIN  # 6950000
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
    lIns: int = 91440,
    rIns: int = 91440,
    tIns: int = 45720,
    bIns: int = 45720,
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
        f'lIns="{lIns}" rIns="{rIns}" tIns="{tIns}" bIns="{bIns}"/>'
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
    """Transição de tópico — fundo image1.png. Geometria do gold standard
    Aula 1 B1 slide 6 (cx=1800000 para o número, sz=9600)."""
    parts: list[str] = []
    parts.append(
        text_box(
            20,
            HERO_X,
            900000,
            1800000,
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
            anchor="ctr",
            align="l",
            lIns=0,
            rIns=0,
            tIns=0,
            bIns=0,
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


# ---------------------------------------------------------------------------
# Slides estruturais — Agenda, Objetivos, Conexão, Síntese, Ponte, Referências
# ---------------------------------------------------------------------------


def build_agenda(n: int, items: list[str]) -> None:
    """Agenda do Bloco — grade 2×4 (até 8 itens). Replica Aula 1 B1 slide 3."""
    parts = canonical_header("Agenda do Bloco", "O que vamos percorrer nas próximas 1h50min")

    # grade 2×4: 4 linhas, 2 colunas (medidas gold standard B1 slide 3)
    y_positions = [1700000, 2300000, 2900000, 3500000]
    el_x_left = 785321
    el_x_right = 4640749
    title_x_left = 1370945
    title_x_right = 5226372

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
                473100,
                420000,
                NAVY,
                text=str(i + 1),
                text_color=WHITE,  # regra 10: fundo navy = texto branco (gold standard usa schemeClr lt1)
                text_size=1600,
                text_bold=True,
            )
        )
        parts.append(
            text_box(
                base_id + i * 2 + 1,
                t_x,
                y + 60000,
                2703000,
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
        # Selo amarelo (ELIPSE, gold standard B1 slide 46) com número branco
        parts.append(
            ellipse(
                base_id + i * 2,
                750000,
                y,
                600900,
                500100,
                YELLOW,
                text=str(i + 1),
                text_color=WHITE,
                text_size=2000,
                text_bold=True,
            )
        )
        # Texto descritivo
        parts.append(
            text_box(
                base_id + i * 2 + 1,
                1471034,
                y + 60000,
                6369000,
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
) -> None:
    """Ponte para o Bloco 2 — hero seta + lista de até 4 itens.

    Replica Aula 1 B1 slide 47. `items` = lista de (título, descrição).
    """
    parts = canonical_header("Ponte para o Bloco 2", "O que vem a seguir, depois do intervalo")

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
    card_h: int = 2600000,
    card_title_size: int = 1700,
    card_text_size: int = 1400,
) -> None:
    """Card branco com borda navy + barra navy de título + texto navy.

    Padrão "estiloso" inspirado no slide 22 do gold standard (cards lado
    a lado com cabeçalho colorido). Aqui adaptado para card único:

    - Outer card: roundRect FFFFFF com borda navy (regra 10: fundo
      branco exige borda navy).
    - Header bar interno: rect navy com título em Arial Black branco
      (regra 10: fundo navy = texto branco).
    - Corpo: parágrafos em texto navy/cinza dentro do card branco.
    """
    # Sem subtítulo amarelo (o título do card vai dentro do header navy).
    parts = canonical_header(title)

    card_x = CONTENT_X_MIN
    card_y = 1500000  # logo abaixo da faixa amarela canônica (y=960000)
    card_w = CONTENT_W
    header_h = 600000
    inner_pad_x = 200000
    inner_pad_y = 150000

    # 1) Card externo (branco com borda navy)
    parts.append(
        filled_rect(
            50,
            card_x,
            card_y,
            card_w,
            card_h,
            WHITE,
            line=NAVY,
            line_w=12700,
            rounded=True,
        )
    )
    # 2) Header bar navy com título branco
    parts.append(
        filled_rect(
            51,
            card_x + 80000,
            card_y + 80000,
            card_w - 160000,
            header_h,
            NAVY,
            rounded=True,
            text_runs=[
                {
                    "text": card_title,
                    "sz": card_title_size,
                    "b": True,
                    "color": WHITE,
                    "font": "Arial Black",
                }
            ],
            text_align="l",
            text_anchor="ctr",
        )
    )
    # 3) Parágrafos do corpo (dentro do card branco, abaixo do header)
    body_y = card_y + 80000 + header_h + inner_pad_y
    body_x = card_x + inner_pad_x
    body_w = card_w - 2 * inner_pad_x
    body_h = card_h - 80000 - header_h - inner_pad_y - 80000
    card_paras = [
        [{"text": p, "sz": card_text_size, "color": TEXT, "font": "Arial"}]
        for p in card_paragraphs
    ]
    parts.append(
        multi_para_box(
            52,
            body_x,
            body_y,
            body_w,
            body_h,
            card_paras,
            line_spc=125000,
            para_spc_before=400,
        )
    )
    if citation:
        parts.append(footer_citation(53, citation))
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
            CONTENT_W,
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

    gap = 210000
    col_w = (CONTENT_W - gap) // 2  # divide a área útil em 2 colunas com 1 gap
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
                    "color": WHITE,
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

        label_x = max(CONTENT_X_MIN, cx - 200000)
        label_w = min(diam + 400000, 7970000 - label_x)
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
) -> None:
    """Armadilhas em 3 cards verticais com borda amarela."""
    parts = canonical_header(title)
    card_h = 820000
    gap = 30000
    base_y = 1750000

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
        f"Recap da Atividade {aula_n - 1}",
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

    # Caixa navy com enunciado em branco (regra 10: nunca navy sobre amarelo)
    parts.append(
        filled_rect(
            50,
            CONTENT_X_MIN,
            1780000,
            CONTENT_W,
            720000,
            NAVY,
            rounded=True,
            multi_paragraphs=[
                [
                    {
                        "text": enunciado,
                        "sz": 1400,
                        "b": True,
                        "color": WHITE,
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


REPO_ROOT = Path(__file__).resolve().parents[4]
"""Diretório raiz do repositório (onde vivem `.cursor/skills/...`).
A partir daqui o script monta os paths absolutos para `unpack_pptx.py`
e para `docs/templates/layout.pptx` (que vive em `jurimetria/docs/`)."""


def unpack_layout_fresh() -> None:
    """Garante que /tmp/deck_aula2_bloco1/ é um unpack limpo do
    layout.pptx oficial. Sempre rm -rf antes de unpack para evitar
    estado residual de execuções anteriores (que podia causar
    double-swap em image1/image2)."""
    import shutil
    import subprocess

    if DECK.exists():
        shutil.rmtree(DECK)
    layout = REPO_ROOT / "jurimetria/docs/templates/layout.pptx"
    unpack_script = REPO_ROOT / ".cursor/skills/build-aula-pptx/scripts/unpack_pptx.py"
    subprocess.run(
        [
            "uv", "run", "python",
            str(unpack_script),
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
        "Aula 2 · Bloco 1",
        "O Ciclo da Ciência de Dados Aplicado ao Direito (Parte 1)",
        "Do problema à coleta: perguntar e mapear no modo raiz",
    )

    # 2. Agenda
    build_agenda(
        2,
        [
            "Correção das 3 questões da Atividade 1",
            "Visão geral das 6 etapas do ciclo",
            "Por que pensar em ciclo importa",
            "Etapa 1: pergunta jurídica em investigável",
            "Critérios de boa pergunta e exemplos",
            "Etapa 2: mapear as informações",
            "Variáveis na base de locação do TJSP",
            "Exercício dirigido e fechamento",
        ],
    )

    # 3. Objetivos
    build_objetivos(
        3,
        [
            ("Compreender", "o ciclo da ciência de dados aplicado ao Direito em suas 6 etapas"),
            ("Reconhecer", "os critérios de uma pergunta jurimétrica investigável"),
            ("Reescrever", "uma pergunta jurídica vaga em pergunta de dados"),
            ("Mapear", "as variáveis e fontes necessárias a partir de uma pergunta"),
            ("Construir", "uma tabela analítica mínima como ponto de partida da análise"),
        ],
    )

    # 4. Conexão / Voltando do intervalo
    build_conexao_voltando(
        4,
        "Onde estamos no curso",
        "Da fundamentação ao método",
        "Na Aula 1, vimos por que dados importam para o operador do Direito e o que é Jurimetria.",
        [
            "Agora começa o método: o ciclo da ciência de dados em modo raiz, percorrido nas Aulas 2 e 3.",
            "Toda a aula opera sobre a base do trabalho final (16.110 julgados de locação do TJSP) e sobre o caso XY&A.",
            "Depois, na Aula 5, o mesmo ciclo será revisitado com IA generativa em cada etapa.",
        ],
        citation="Nunes (2019); CNJ (2024)",
    )

    # 5. Transição 01 — Correção da atividade
    build_transicao(
        5,
        "01",
        "Atividade 1: revisão",
        "Correção comentada das 3 questões e ponte para o método desta aula",
    )

    # 6. Recap da Atividade 1
    build_recap_atividade(
        6,
        2,  # aula_n=2 → corrige Atividade 1
        "Pano de fundo: caso XY&A e a base de 16.110 julgados de locação do TJSP, sobre os fundamentos da Aula 1.",
        [
            "Listar 3 perguntas jurimétricas do XY&A em ao menos 2 áreas (contencioso, gestão, provisionamento).",
            "Reescrever uma das 3 perguntas em formato investigável: tema, recorte, variável central e comparação.",
            "Apontar que decisão concreta do escritório a resposta apoiaria, e por quê.",
        ],
    )

    # 7. Correção Q1
    build_correcao_questao(
        7,
        2,
        1,
        "Q1. Listar 3 perguntas jurimétricas do XY&A em ao menos 2 áreas (contencioso, gestão, provisionamento).",
        [
            "Caminho de resposta: cobrir pelo menos 2 das 3 áreas e dar a cada pergunta um recorte mínimo (matéria, jurisdição ou período).",
            "Exemplos no XY&A: contencioso, 'taxa de procedência por vara em revisão'; gestão, 'concentração de despejos por comarca'; provisão, 'valor mediano de condenação'.",
            "Armadilhas frequentes: 3 perguntas todas no mesmo plano operacional, perguntas de opinião sem variável, ou perguntas grandes demais sem ancoragem.",
        ],
        citation="Nunes (2019); ABJ (relatórios)",
    )

    # 8. Correção Q2
    build_correcao_questao(
        8,
        2,
        2,
        "Q2. Reescrever uma das 3 perguntas em formato investigável: tema, recorte, variável central e comparação.",
        [
            "Caminho de resposta: tema (matéria e tipo de ação), recorte (jurisdição e período), variável central (taxa, mediana, valor) e ponto de comparação (média ou outro grupo).",
            "Exemplo XY&A: 'Em renovatórias do TJSP, parte PJ, 2018 a 2024, qual a taxa de procedência em favor do locador comparada à média do tribunal?'.",
            "Armadilhas frequentes: pergunta investigável que ainda mistura opinião e métrica, ausência de ponto de comparação ou recorte vago.",
        ],
        citation="Nunes (2019); Katz e Bommarito (2013)",
    )

    # 9. Correção Q3
    build_correcao_questao(
        9,
        2,
        3,
        "Q3. Que decisão concreta do escritório a resposta apoiaria, e por quê.",
        [
            "Caminho de resposta: nomear uma decisão específica que mudaria com a resposta. Exemplos: política de acordo, recalibrar provisão, redistribuir equipe, mudar tese.",
            "Exemplo XY&A: se a taxa de procedência em renovatórias caiu, a decisão pode ser revisar a estratégia de litígio e priorizar acordos por faixa de valor.",
            "Armadilhas frequentes: respostas vagas como 'a empresa fica mais informada', sem nomear a decisão concreta que muda com o número.",
        ],
        citation="Susskind (2023); Nunes (2019)",
    )

    # 10. Insight / ponte para o conteúdo novo
    build_conceito(
        10,
        "Da intuição à pergunta de dados",
        [
            "Toda intuição jurídica relevante pode ser convertida em uma pergunta investigável.",
            "Quando a pergunta é boa, a sequência fica clara: variáveis, fonte, coleta, análise e entrega. É o ciclo da próxima seção.",
            "Quando a pergunta é ruim, qualquer dado parece interessante. É aí que estatística vira marketing.",
        ],
        citation="Huff (2016); Silver (2013)",
        accent="Insight da correção e ponte para o ciclo",
    )

    # 11. Transição 02 — O ciclo da ciência de dados
    build_transicao(
        11,
        "02",
        "Ciclo da ciência de dados",
        "Visão geral das 6 etapas que estruturam o resto do curso",
    )

    # 12. O que é o ciclo
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

    # 13. As 6 etapas do ciclo
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

    # 14. Etapas 1 e 2
    build_card(
        14,
        "Etapas 1 e 2 do ciclo",
        "Pergunta e mapeamento: onde tudo começa",
        [
            "Etapa 1, transformar a pergunta jurídica em pergunta investigável: foco do bloco de hoje.",
            "Etapa 2, mapear as informações necessárias: identificar quais variáveis e fontes responderiam à pergunta.",
            "Sem essas duas etapas bem feitas, todo o resto do ciclo fica frágil ou enviesado.",
        ],
        citation="Nunes (2019)",
    )

    # 15. Etapas 3 e 4
    build_card(
        15,
        "Etapas 3 e 4 do ciclo",
        "Coletar e tratar: construindo a base analítica",
        [
            "Etapa 3, coletar: fontes públicas (DataJud, tribunais), internas (sistemas) e, quando preciso, scraping.",
            "Etapa 4, tratar: padronizar datas, valores, classificações e textos em uma TABELA estruturada e saneada.",
            "Veremos as duas em detalhe no Bloco 2 (coleta) e na Aula 3 (tratamento).",
        ],
        citation="CNJ (2024)",
    )

    # 16. Etapas 5 e 6
    build_card(
        16,
        "Etapas 5 e 6 do ciclo",
        "Analisar e apresentar: da TABELA ao insight",
        [
            "Etapa 5, analisar: estatística descritiva no Excel. Medidas de posição, dispersão e gráficos.",
            "Etapa 6, apresentar: gráficos e tabelas com boas práticas de visualização para o público jurídico.",
            "Aprofundamos as duas na Aula 3 e voltamos a elas na Aula 5 com IA generativa.",
        ],
        citation="Wheelan (2016)",
    )

    # 17. Por que pensar em ciclo
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

    # 18. Cadeia de custódia
    build_conceito(
        18,
        "Cadeia de custódia analítica",
        [
            "No processo penal, a cadeia de custódia garante que a prova chegue íntegra ao julgamento.",
            "Na Jurimetria, o ciclo cumpre o mesmo papel: cada etapa preserva e documenta a integridade dos dados.",
            "Quem pula etapas perde rastreabilidade. Quem documenta, defende a análise como defenderia uma prova pericial.",
        ],
        citation="Nunes (2019); CNJ (2024)",
        accent="Analogia jurídica",
    )

    # 19. Transição 03 — Etapa 1
    build_transicao(
        19,
        "03",
        "Etapa 1: a pergunta",
        "Da pergunta jurídica vaga à pergunta investigável",
    )

    # 20. O que é uma pergunta investigável
    build_conceito(
        20,
        "Pergunta investigável",
        [
            "É uma pergunta que aponta com clareza para um dado mensurável e para um critério de resposta.",
            "Em vez de pedir uma opinião, pede uma comparação, uma proporção, uma frequência ou uma evolução.",
            "Sem pergunta investigável, qualquer análise ou IA tende a produzir um número aparentemente preciso, mas sem ancoragem.",
        ],
        citation="Nunes (2019); Katz e Bommarito (2013)",
    )

    # 21. Critérios de uma boa pergunta
    build_card(
        21,
        "Critérios de uma boa pergunta",
        "Quatro critérios não negociáveis",
        [
            "Específica: define matéria, período e jurisdição.",
            "Verificável: aponta para uma variável que existe ou é coletável.",
            "Comparável: traz um ponto de referência (média, outro juízo, outro período).",
            "Útil: a resposta muda alguma decisão concreta de litígio, negociação ou provisão.",
        ],
        citation="Nunes (2019); Katz e Bommarito (2013)",
    )

    # 22. Antes e depois
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
            "Revisões TJSP 2018-2024: procedência do juízo X vs. média?",
            "Renovatórias: tempo mediano até sentença subiu de 2019 a 2024?",
            "Revisão 2020-2024: proporção de reformas a favor do recorrente?",
            "Acordos 2022-2024: valor acordado vs. valor da causa?",
        ],
        citation="Nunes (2019); ABJ (relatórios)",
    )

    # 23. Stat — alcance da pergunta certa
    build_stat(
        23,
        "O alcance da pergunta certa",
        "16.110",
        "julgados de revisão e renovatória de locação do TJSP, 2010 a 2024 (parte PJ), à disposição do XY&A para responder boas perguntas.",
        citation="CNJ (2024); TJSP",
    )

    # 24. Armadilhas comuns
    build_armadilhas(
        24,
        "Armadilhas ao formular",
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

    # 25. Mini-caso XY&A
    build_card(
        25,
        "Mini-caso XY&A",
        "Da intuição à pergunta investigável",
        [
            "Intuição do sócio: estamos perdendo mais renovatórias do que antes.",
            "Pergunta investigável: nas renovatórias do TJSP, 2018 a 2024, com parte PJ, qual a evolução anual da taxa de procedência em favor do locador?",
            "Variáveis necessárias (já aparecem na Etapa 2): tipo de ação, ano da sentença, parte, desfecho.",
        ],
    )

    # 26. Síntese da Etapa 1 (checklist)
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

    # 27. Transição 04 — Etapa 2
    build_transicao(
        27,
        "04",
        "Etapa 2: mapeamento",
        "Que variáveis responderiam à pergunta?",
    )

    # 28. O que significa mapear
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

    # 29. Tipos de variável (revisita Aula 1)
    build_comparacao(
        29,
        "Tipos de variável",
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
            "Quantidade de recursos, partes, audiências.",
        ],
        citation="Wheelan (2016)",
    )

    # 30. Tabela — variáveis na base TJSP
    build_tabela(
        30,
        "Variáveis na base TJSP",
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

    # 31. De pergunta a variáveis
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

    # 32. Três exemplos de mapeamento
    build_lista_numerada(
        32,
        "Três exemplos de mapeamento",
        [
            "Existe diferença entre acordos e sentenças no valor envolvido? → tipo de ação, desfecho, valor da causa, valor de condenação ou acordado.",
            "Há concentração de ações em poucas varas? → comarca, vara, ano de distribuição.",
            "A taxa de procedência mudou após 2020? → tipo de ação, ano da sentença, desfecho.",
        ],
        citation="Nunes (2019); ABJ (relatórios)",
        accent="Da pergunta às variáveis necessárias",
    )

    # 33. Exercício dirigido em sala
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

    # 34. Tudo começa com uma TABELA
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

    # 35. Tabela analítica como petição inicial
    build_conceito(
        35,
        "A tabela é a petição inicial",
        [
            "A petição inicial define o que está em juízo. Tudo o que não estiver nela, em regra, não pode ser decidido.",
            "A tabela analítica define o que pode ser respondido. Tudo o que não estiver nela, em regra, não pode ser analisado.",
            "Por isso, mapear bem na Etapa 2 é desenhar a competência da análise, antes de qualquer coleta.",
        ],
        citation="Nunes (2019)",
        accent="Analogia jurídica",
    )

    # 36. Mini-caso completo XY&A (regra 9: mini-caso prático antes da síntese)
    build_card(
        36,
        "Mini-caso completo · XY&A",
        "Da intuição à tabela em 4 movimentos",
        [
            "Movimento 1 (Etapa 1): intuição vira pergunta. 'Estamos perdendo mais renovatórias' vira 'Nas renovatórias do TJSP, parte PJ, 2018 a 2024, qual a evolução anual da taxa de procedência em favor do locador?'.",
            "Movimento 2 (Etapa 2): pergunta vira variáveis. Tipo de ação, ano da sentença, parte (PJ/PF), desfecho, jurisdição.",
            "Movimento 3 (Etapa 2): variáveis viram tabela. 1 linha por processo, 5 colunas, ano da sentença como recorte temporal e desfecho como variável central.",
            "Movimento 4 (próximo bloco): tabela viabiliza coleta planejada na DataJud e na base interna do XY&A.",
        ],
        citation="Nunes (2019); CNJ (2024)",
        card_h=2750000,
        card_text_size=1050,
    )

    # 37. Síntese do Bloco 1
    build_sintese(
        37,
        [
            "Toda análise jurimétrica começa por uma pergunta investigável e termina em uma decisão concreta.",
            "O ciclo de 6 etapas é o método reproduzível, rastreável e defensável que sustenta cada análise.",
            "Etapa 1: pergunta específica, verificável, comparável e útil.",
            "Etapa 2: tabela com 1 linha por processo e 1 coluna por variável, saneada e completa.",
            "Sem Etapa 1 e 2 bem feitas, análise vira opinião com cara de número.",
        ],
    )

    # 38. Ponte para o Bloco 2
    build_ponte(
        38,
        "Da Etapa 2 à coleta",
        "No próximo bloco entramos na Etapa 3: como obter os dados em fontes públicas e internas.",
        [
            ("DataJud, CNJ e tribunais", "Fontes públicas e como ler os campos dos microdados."),
            ("Coleta interna e scraping", "Quando construir, quando comprar e quando raspar."),
            ("LGPD e vieses de amostragem", "Cuidados antes de prometer resposta."),
            ("Atividade Prática 2", "3 questões sobre a base do XY&A, entrega até a Aula 3."),
        ],
    )

    # 39. Referências do Bloco
    build_referencias(
        39,
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

    # 40. Fim do Bloco 1
    build_encerramento_b1(
        40,
        bloco_n=1,
        proximo_bloco_gancho="Etapa 3 (coletar), LGPD, vieses e a Atividade Prática 2.",
    )

    update_content_types(40)
    update_presentation(40)
    print("OK 40 slides gerados.")


if __name__ == "__main__":
    main()
