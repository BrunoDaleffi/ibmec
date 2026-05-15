# ruff: noqa: E501
"""Gera o pptx de Aula 3 · Bloco 1 — O Ciclo da Ciência de Dados (Parte 2).

Layout canônico replicado da Aula 1 publicada (ver
`.cursor/skills/build-aula-pptx/layout-canonical.md`).

Convenção de fundos:
- image1.png → capa, transição de tópico (01, 02, …) e encerramento ("Fim do Bloco N").
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
        docs/templates/layout.pptx /tmp/deck_aula3_bloco1/

Depois:
    uv run python .cursor/skills/build-aula-pptx/scripts/pack_pptx.py \
        /tmp/deck_aula3_bloco1/ aulas/aula_02/slides/aula2_bloco1_jurimetria.pptx
"""

from __future__ import annotations

import re
from pathlib import Path

DECK = Path("/tmp/deck_aula3_bloco1")
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
    """Garante que /tmp/deck_aula3_bloco1/ é um unpack limpo do
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
        "Aula 3 · Bloco 1",
        "O Ciclo da Ciência de Dados Aplicado ao Direito (Parte 2)",
        "Da base ao insight: tratar e estruturar (Etapa 4) e analisar com estatística descritiva (Etapa 5)",
    )

    # 2. Agenda
    build_agenda(
        2,
        [
            "Etapa 4: tratar e estruturar a base",
            "Excel como ferramenta de tratamento",
            "Tratamento na prática (XY&A)",
            "Armadilhas no tratamento de dados",
            "Etapa 5: análise descritiva",
            "Posição: média, mediana, moda, percentis",
            "Dispersão: amplitude, desvio, quartis",
            "Quando a média engana e a mediana ajuda",
        ],
    )

    # 3. Objetivos
    build_objetivos(
        3,
        [
            ("Compreender", "o que envolve tratar e estruturar uma base de dados jurídica analítica"),
            ("Identificar", "as principais armadilhas do tratamento de dados em planilhas Excel"),
            ("Aplicar", "padronização de datas, valores e classificações sobre a base XY&A"),
            ("Distinguir", "medidas de posição e de dispersão e os contextos em que cada uma serve"),
            ("Decidir", "quando a média engana e quando a mediana é a leitura correta"),
        ],
    )

    # 4. Conexão / Onde estamos no ciclo
    build_conexao_voltando(
        4,
        "Onde estamos no ciclo",
        "Da base aos achados",
        "Na Aula 2 percorremos as Etapas 1, 2 e 3: pergunta investigável, mapeamento de variáveis e coleta da base.",
        [
            "Hoje seguimos para as Etapas 4 e 5: tratar a base que coletamos e descrever os primeiros achados com estatística descritiva.",
            "O cenário continua sendo o XY&A e a base de 16.110 julgados de revisão e renovatória de locação do TJSP entre 2010 e 2024.",
            "No Bloco 2 fechamos com Etapa 6 (apresentação dos resultados) e a leitura crítica de gráficos.",
        ],
        citation="Nunes (2019); Wheelan (2016)",
    )

    # =================================================================
    # Tópico 01 — Etapa 4: tratar e estruturar a base
    # =================================================================

    # 5. Transição 01
    build_transicao(
        5,
        "01",
        "Etapa 4: tratar a base",
        "De dados crus a uma tabela analítica defensável",
    )

    # 6. O que é tratar e estruturar
    build_conceito(
        6,
        "O que é tratar e estruturar",
        [
            "Tratar é transformar dados crus, heterogêneos e cheios de ruído em uma tabela única, padronizada e auditável.",
            "Estruturar é definir, dentro dessa tabela, as variáveis certas para responder à pergunta investigável definida na Etapa 1.",
            "Sem essa etapa, qualquer análise herda os erros, as duplicatas e as inconsistências da fonte. O tratamento é a fundação do resto do ciclo.",
        ],
        citation="Nunes (2019); Wheelan (2016)",
    )

    # 7. Stat callout: tempo gasto em tratamento
    build_stat(
        7,
        "Tempo gasto em tratamento",
        "60–80%",
        "do tempo de um projeto de análise é consumido na coleta e no tratamento da base, não na análise propriamente dita.",
        citation="Wheelan (2016); Nunes (2019)",
    )

    # 8. As 4 dimensões do tratamento
    build_card(
        8,
        "As 4 dimensões do tratamento",
        "O que precisa estar pronto antes de analisar",
        [
            "Limpeza: remover linhas vazias, processos duplicados, registros incompletos ou fora do recorte.",
            "Padronização: deixar datas, valores monetários e textos em formatos uniformes (ISO 8601, ponto decimal, caixa única).",
            "Criação de variáveis: derivar campos que respondem à pergunta (tempo de tramitação em dias, faixa de valor, ano de distribuição).",
            "Validação: conferir que totais, distribuições e amostras batem com a fonte e com a expectativa do operador.",
        ],
        citation="Nunes (2019)",
        card_h=2300000,
    )

    # 9. Comparação: dados crus × tabela analítica
    build_comparacao(
        9,
        "Dados crus × tabela analítica",
        "Dados crus (como chegam)",
        [
            "Linhas heterogêneas, vindas de fontes diferentes.",
            "Datas em formatos misturados, valores como texto.",
            "Categorias livres, com sinônimos e erros de digitação.",
            "Não dá para somar, agrupar ou comparar com confiança.",
        ],
        "Tabela analítica (depois do tratamento)",
        [
            "Cada linha é um processo, cada coluna é uma variável.",
            "Datas em ISO 8601, valores em número, categorias fechadas.",
            "Variáveis derivadas (tempo, faixa, ano) já calculadas.",
            "Pronta para descrever, agrupar, comparar e visualizar.",
        ],
        citation="Wheelan (2016); CNJ (2024)",
    )

    # 10. Mini-caso XY&A: planilha bruta → tabela analítica
    build_card(
        10,
        "XY&A: planilha bruta vs. base analítica",
        "O que muda entre o sistema do escritório e a base analítica",
        [
            "Sistema interno do XY&A: cada linha pode ser um andamento, com datas em formatos misturados e valores como texto livre.",
            "Base analítica: cada linha vira um processo, com data de distribuição e de sentença em ISO, valor da causa em número e desfecho categórico.",
            "Toda transformação é registrada em uma planilha-irmã de Documentação, para que outro advogado consiga reproduzir.",
        ],
        citation="Nunes (2019); CNJ (2024)",
        card_h=2200000,
    )

    # =================================================================
    # Tópico 02 — Excel como ferramenta de tratamento
    # =================================================================

    # 11. Transição 02
    build_transicao(
        11,
        "02",
        "Excel como ferramenta",
        "Filtros, fórmulas e tabelas dinâmicas para tratar uma base jurídica",
    )

    # 12. Por que Excel
    build_card(
        12,
        "Por que Excel no Direito",
        "Três razões práticas",
        [
            "Universal: roda em qualquer escritório e em qualquer máquina, com curva de aprendizado baixa para quem já trabalha com planilha.",
            "Suficiente: para uma base de 16 mil linhas como a do XY&A, Excel cobre coleta manual, padronização, agregações e gráficos sem precisar de Python ou R.",
            "Auditável: a sequência de fórmulas, filtros e abas é visível e revisável, ao contrário de scripts que escondem a lógica do tratamento.",
        ],
        citation="Nunes (2019); Wheelan (2016)",
        card_h=2400000,
    )

    # 13. Os 3 instrumentos do Excel
    build_comparacao(
        13,
        "Os três instrumentos no Excel",
        "Filtros e classificações",
        [
            "Recortar a base por matéria, vara, período e desfecho.",
            "Encontrar inconsistências e linhas-órfãs.",
            "Inspecionar uma amostra antes de aplicar uma transformação.",
            "Útil quando a pergunta exige um subconjunto.",
        ],
        "Fórmulas e tabelas dinâmicas",
        [
            "Fórmulas (SE, PROCV, ARRUMAR, TEXTO) padronizam datas, valores e textos.",
            "Tabelas dinâmicas resumem milhares de linhas em painéis.",
            "Substituem dezenas de cálculos manuais.",
            "Útil para agregar e comparar grupos.",
        ],
        citation="Wheelan (2016)",
    )

    # 14. Tabela: pipeline de tratamento em 5 passos
    build_tabela(
        14,
        "Pipeline de tratamento em 5 passos",
        ["#", "Passo", "Resultado"],
        [
            ["1", "Importar e identificar a unidade da linha", "Sei se cada linha é processo, andamento ou parte"],
            ["2", "Padronizar datas (ISO 8601)", "Sei calcular tempo entre eventos com confiança"],
            ["3", "Padronizar valores monetários", "Posso somar, calcular média e mediana sem erro"],
            ["4", "Categorizar texto livre (vara, desfecho, tipo)", "Posso agrupar e comparar grupos"],
            ["5", "Criar variáveis derivadas (tempo, faixa, ano)", "Tenho colunas prontas para a Etapa 5"],
        ],
        citation="Nunes (2019)",
        col_widths=[400000, 2400000, 3150000],
    )

    # 15. Demonstração: campos antes × depois
    build_tabela(
        15,
        "Antes e depois do tratamento",
        ["Campo", "Antes (cru)", "Depois (analítico)"],
        [
            ["Distribuição", "01/03/2018", "2018-03-01"],
            ["Valor da causa", "R$ 1.234,56", "1234.56"],
            ["Vara", "1ª vara cíveL  Sp", "VARA_CIVEL_01_SP"],
            ["Desfecho", "Procedente em parte", "PARCIAL"],
            ["Tipo de ação", "renovatoria", "RENOVATORIA"],
        ],
        citation="Wheelan (2016)",
        col_widths=[1700000, 2125000, 2125000],
    )

    # =================================================================
    # Tópico 03 — Tratamento na prática (XY&A)
    # =================================================================

    # 16. Transição 03
    build_transicao(
        16,
        "03",
        "Tratamento na prática",
        "Aplicando os 5 passos sobre a base XY&A",
    )

    # 17. Tratando datas
    build_conceito(
        17,
        "Tratando datas",
        [
            "Bases jurídicas brasileiras misturam DD/MM/YYYY, DD-MM-YY e até MM/DD/YYYY (importadas de sistemas em inglês).",
            "Padronizamos tudo em ISO 8601 (YYYY-MM-DD) para que ordenação e cálculos de tempo entre eventos funcionem sem ambiguidade.",
            "No Excel, TEXTO combinada com DATA.VALOR resolve a maior parte. As linhas sobrantes vão para uma aba de Exceções e revisão manual.",
        ],
        citation="Wheelan (2016)",
    )

    # 18. Tratando valores
    build_conceito(
        18,
        "Tratando valores monetários",
        [
            "Valores como R$ 1.234,56 chegam como texto. Para somar, calcular média ou mediana, precisam virar número.",
            "A combinação de SUBSTITUIR (tira R$ e ponto de milhar) e VALOR (converte a vírgula em número) padroniza a coluna em poucos passos.",
            "Sempre que houver arredondamento, registre a regra (truncar, arredondar para cima/baixo) na aba de Documentação da base.",
        ],
        citation="Nunes (2019)",
    )

    # 19. Tratando texto inconsistente
    build_conceito(
        19,
        "Tratando texto inconsistente",
        [
            "Textos livres como vara e comarca chegam com variações: caixa misturada, espaços extras, acentuação diferente, abreviações.",
            "ARRUMAR remove espaços extras; MAIÚSCULA e MINÚSCULA padronizam a caixa; SUBSTITUIR limpa acentos quando preciso.",
            "Para variações reais de grafia (1ª Vara Cível vs. 1a Vara Civel, por exemplo), use uma planilha-dicionário com mapeamento canônico.",
        ],
        citation="CNJ (2024)",
    )

    # 20. Classificações: desfecho e tipo de ação
    build_card(
        20,
        "Categorias fechadas: desfecho e tipo",
        "Do texto livre ao categórico controlado",
        [
            "Desfecho: 4 categorias derivadas do dispositivo (PROCEDENTE, PARCIAL_PROCEDENTE, IMPROCEDENTE, EXTINTO_SEM_MERITO).",
            "Tipo de ação: REVISIONAL e RENOVATORIA, pois o desfecho costuma ter dinâmica diferente nos dois ritos.",
            "Quem fez a classificação, quando e com que critério vai junto na aba de Documentação. Sem isso, a categoria perde defesa em juízo.",
        ],
        citation="Nunes (2019); CNJ (2024)",
        card_h=2300000,
        card_text_size=1300,
    )

    # 21. Exercício dirigido — enunciado (padronização de "vara")
    build_exercicio_enunciado(
        21,
        "Exercício dirigido: padronizar 'vara'",
        "Como você padronizaria a coluna 'vara' do XY&A para que ela permita agrupar processos e comparar juízos?",
        contexto="A coluna chega com 412 valores únicos, com variações como: '1a vara civel sp', '1ª Vara CÍVEL SP', 'Vara Cível 1 SP', 'sao paulo, 1ª vara cível' etc.",
        citation="Nunes (2019)",
    )

    # 22. Exercício dirigido — resposta
    build_exercicio_resposta(
        22,
        "Padronizar 'vara': resposta dirigida",
        "Como padronizar a coluna 'vara' para agrupar e comparar juízos?",
        [
            "Normalizar: ARRUMAR + MAIÚSCULA + remoção de acentos uniformizam caixa e ortografia.",
            "Decompor: separar número da vara, foro (cível, criminal) e comarca em colunas distintas.",
            "Dicionário: planilha de_para com as variações observadas; aplicar PROCV para mapear no canônico.",
            "Validar: se 412 valores únicos viraram ~60, a comparação entre juízos é mais confiável.",
        ],
        citation="Nunes (2019); Wheelan (2016)",
    )

    # =================================================================
    # Tópico 04 — Armadilhas no tratamento
    # =================================================================

    # 23. Transição 04
    build_transicao(
        23,
        "04",
        "Armadilhas do tratamento",
        "Erros comuns que viram problemas grandes na análise",
    )

    # 24. As 4 armadilhas mais comuns
    build_armadilhas(
        24,
        "As 4 armadilhas mais comuns",
        [
            ("Datas reinterpretadas pelo Excel", "03/05/2018 lido como 5 de março quebra todo cálculo de tempo."),
            ("Vírgulas e pontos misturados", "R$ 1.234,56 vira 1234.56 ou 1234560,00. Erro de mil vezes silencioso."),
            ("Duplicatas que parecem únicas", "Processos iguais com espaço, acento ou caixa diferentes inflam a base."),
            ("Padronização que perde nuance", "Colapsar 412 varas em 5 grupos esconde o juízo com o achado relevante."),
        ],
        citation="Huff (2016); Silver (2013)",
        card_h=580000,
    )

    # 25. Boas práticas: documentar e versionar
    build_card(
        25,
        "Boas práticas: documentar e versionar",
        "O que separa um tratamento defensável de um tratamento perdido",
        [
            "Mantenha sempre a base bruta intacta em uma aba/arquivo separado. Toda transformação acontece em uma cópia.",
            "Documente cada decisão de padronização (regra, motivo, autor, data) em uma aba 'Documentação'. Esse é o equivalente jurídico da cadeia de custódia.",
            "Versione: salve cópias da base após cada etapa do pipeline (1_importada, 2_datas, 3_valores, 4_categorias, 5_derivadas), para conseguir voltar.",
        ],
        citation="Nunes (2019); CNJ (2024)",
        card_h=2300000,
    )

    # 26. Citação Huff (1954) sobre dados que mentem
    build_conceito(
        26,
        "Dados não mentem; quem mente é quem trata mal os dados.",
        [
            "A frase de Huff (1954/2016) é uma síntese da Etapa 4: a maior parte dos números enganosos não nasce de má-fé na análise, mas de tratamento descuidado da base.",
            "Para o operador do Direito, isso significa que defender um número exige defender o tratamento que produziu o número. Sem rastro, não há defesa.",
            "Por isso, todo trabalho final desta disciplina exige documentação explícita da Etapa 4.",
        ],
        citation="Huff (2016); Silver (2013)",
        accent="Por que a Etapa 4 sustenta o resto do ciclo",
    )

    # =================================================================
    # Tópico 05 — Etapa 5: análise descritiva
    # =================================================================

    # 27. Transição 05
    build_transicao(
        27,
        "05",
        "Etapa 5: análise",
        "Estatística descritiva como primeira leitura da base",
    )

    # 28. Descrever × inferir × prever
    build_comparacao(
        28,
        "Três modos de olhar para os dados",
        "Descrever (foco de hoje)",
        [
            "Resumir o que está na base: médias, medianas, frequências.",
            "Não pretende generalizar para fora da base.",
            "É a leitura inicial obrigatória de qualquer projeto.",
            "Aula 3 inteira gira em torno daqui.",
        ],
        "Inferir e prever (Aula 4)",
        [
            "Inferir: testar hipóteses sobre a população a partir de uma amostra.",
            "Prever: estimar desfecho, tempo, valor e propensão de acordo.",
            "Exigem que a Etapa 4 tenha sido bem feita.",
            "Voltam na Aula 4 com p-valor, regressão e sobrevivência.",
        ],
        citation="Wheelan (2016); James et al. (2021)",
    )

    # 29. Medidas de posição
    build_card(
        29,
        "Medidas de posição",
        "Onde está o 'centro' da distribuição",
        [
            "Média: soma dos valores dividida pela quantidade. É sensível a valores extremos.",
            "Mediana: valor que divide a base ao meio quando ordenada. É robusta a outliers.",
            "Moda: valor mais frequente. Útil em variáveis categóricas (ex.: vara que mais aparece).",
            "Percentis (p25, p50, p75): pontos de corte que mostram como a base se distribui.",
        ],
        citation="Wheelan (2016)",
        card_h=2300000,
    )

    # 30. Medidas de dispersão
    build_card(
        30,
        "Medidas de dispersão",
        "Quão espalhada está a distribuição",
        [
            "Amplitude: diferença entre o maior e o menor valor. Dá a ordem de grandeza, mas é dominada por extremos.",
            "Desvio-padrão: quão longe, em média, cada valor está da média. Útil quando a distribuição é simétrica.",
            "Quartis e intervalo interquartílico (IQR, definido como p75 menos p25): janela onde estão 50% dos casos, preferida em distribuições assimétricas como tempo de processo.",
        ],
        citation="Wheelan (2016)",
        card_h=2200000,
    )

    # 31. Tabela: tempo de tramitação no XY&A (exemplo numérico)
    build_tabela(
        31,
        "Tempo de tramitação (XY&A)",
        ["Medida", "Valor (dias)", "Leitura jurídica"],
        [
            ["Média", "742", "Puxada por casos extremos."],
            ["Mediana", "612", "Metade termina em até ~1 ano e 8 meses."],
            ["P25", "415", "25% mais rápidos: até ~1 ano e 1 mês."],
            ["P75", "894", "25% mais lentos: a partir de ~2 anos e 5 meses."],
            ["IQR (P75-P25)", "479", "Janela típica: ~14 a ~30 meses."],
        ],
        citation="CNJ (2024); Wheelan (2016)",
        col_widths=[1500000, 1300000, 3150000],
    )

    # 32. Stat callout: diferença média × mediana
    build_stat(
        32,
        "Quando a média engana",
        "+130 dias",
        "é a diferença entre a média e a mediana do tempo entre distribuição e sentença no XY&A. Casos muito longos puxam a média; a mediana descreve melhor a realidade da maioria.",
        citation="Wheelan (2016); CNJ (2024)",
    )

    # 33. Comparação: quando média engana × quando ajuda
    build_comparacao(
        33,
        "Média ou mediana?",
        "Quando a média engana",
        [
            "Distribuições assimétricas (tempo, valor da condenação).",
            "Bases com poucos extremos muito altos.",
            "Comparações entre juízos com perfis distintos.",
            "Cliente perguntando pelo 'caso típico'.",
        ],
        "Quando a média ajuda",
        [
            "Distribuições aproximadamente simétricas.",
            "Cálculos que dependem de soma (provisão total).",
            "Indicadores estáveis, com pouca variação.",
            "Quando o que importa é o total por casos.",
        ],
        citation="Wheelan (2016)",
    )

    # 34. Mini-caso: avaliando um juízo com tempo médio enganoso
    build_card(
        34,
        "XY&A: o juízo que parecia rápido",
        "Quando a média leva a uma decisão errada",
        [
            "Em uma comarca específica, a média do tempo de tramitação é 510 dias, abaixo da média geral. Parece um juízo rápido.",
            "Olhando a mediana: 720 dias. A média foi puxada para baixo por 6 processos extintos sem mérito em menos de 30 dias.",
            "A decisão correta de provisão e de estratégia é usar a mediana, não a média. A diferença muda a recomendação para o cliente.",
        ],
        citation="Huff (2016); Wheelan (2016)",
        card_h=2200000,
    )

    # 35. Exercício dirigido — enunciado (escolha de medida)
    build_exercicio_enunciado(
        35,
        "Exercício dirigido: que medida usar?",
        "Para descrever o 'valor da causa' das renovatórias do XY&A para um cliente locador, qual medida você usaria e por quê?",
        contexto="A base tem valores entre R$ 6 mil e R$ 18 milhões, com 80% concentrados abaixo de R$ 250 mil.",
        citation="Wheelan (2016)",
    )

    # 36. Exercício dirigido — resposta
    build_exercicio_resposta(
        36,
        "Que medida usar? Resposta dirigida",
        "Como descrever 'valor da causa' das renovatórias para um cliente locador?",
        [
            "Diagnóstico: distribuição assimétrica, com valores extremos (R$ 18 mi) puxando a média.",
            "Mediana é a primeira leitura: valor central que 50% dos casos não ultrapassam.",
            "P25 e P75 mostram a janela típica: comunicam volatilidade sem esconder os extremos.",
            "Média entra como informação complementar, sempre rotulada como 'puxada por extremos'.",
        ],
        citation="Wheelan (2016); Huff (2016)",
    )

    # =================================================================
    # Fechamento — Síntese, Ponte, Referências, Encerramento
    # =================================================================

    # 37. Síntese
    build_sintese(
        37,
        [
            "Tratar e estruturar consome 60–80% do tempo: é a fundação do ciclo, não um detalhe operacional.",
            "Padronização disciplinada de datas, valores e categorias é o que separa uma base defensável de uma base perdida.",
            "Documentar cada decisão é o equivalente jurídico da cadeia de custódia: sem rastro, o número não se sustenta.",
            "Estatística descritiva é a primeira leitura obrigatória: posição (onde está o centro) e dispersão (quão espalhado).",
            "A escolha entre média e mediana muda a decisão prática: em distribuições assimétricas, a mediana fala a verdade.",
        ],
    )

    # 38. Ponte para o Bloco 2
    build_ponte(
        38,
        "Da descrição à apresentação",
        "Etapa 6 do ciclo no Bloco 2",
        [
            ("Distribuições", "Normal, Poisson, Weibull e analogias jurídicas."),
            ("Visualização", "Qual gráfico para qual pergunta."),
            ("Boas práticas", "O que comunica e o que distrai."),
            ("Leitura crítica", "Como não ser enganado por gráficos."),
        ],
    )

    # 39. Referências
    build_referencias(
        39,
        [
            "HUFF, D. Como mentir com estatística. Rio de Janeiro: Intrínseca, 2016. (Original: How to Lie with Statistics, 1954.)",
            "WHEELAN, C. Estatística: o que é, para que serve, como funciona. Rio de Janeiro: Zahar, 2016.",
            "NUNES, M. Jurimetria: como a estatística pode reinventar o Direito. 2. ed. São Paulo: Revista dos Tribunais, 2019.",
            "SILVER, N. O sinal e o ruído: por que tantas previsões falham e outras não. Rio de Janeiro: Intrínseca, 2013.",
            "JAMES, G.; WITTEN, D.; HASTIE, T.; TIBSHIRANI, R. An Introduction to Statistical Learning. 2. ed. New York: Springer, 2021.",
            "CONSELHO NACIONAL DE JUSTIÇA. Justiça em Números 2024. Brasília: CNJ, 2024.",
            "KATZ, D.; BOMMARITO, M. Quantitative Legal Prediction. Emory Law Journal, v. 62, 2013.",
        ],
    )

    # 40. Encerramento Bloco 1
    build_encerramento_b1(
        40,
        1,
        "Etapa 6 do ciclo (apresentação dos resultados), distribuições e visualização para o operador do Direito.",
    )

    update_content_types(40)
    update_presentation(40)
    print("OK 40 slides gerados.")

if __name__ == "__main__":
    main()
