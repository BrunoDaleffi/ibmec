"""Valida áreas úteis (hard + soft) de cada slide num deck desempacotado.

Lê `ppt/slides/slideN.xml` e confere se cada shape (`p:sp`, `p:pic`,
`p:graphicFrame`, `p:cxnSp`) cabe nas caixas canônicas (ver
`.cursor/skills/build-aula-pptx/layout-canonical.md` seção 0).

Uso:

    uv run python .cursor/skills/build-aula-pptx/scripts/check_useful_area.py \\
        /tmp/deck_aula2_bloco1/

Saída: violações `[hard]` (erros, exit 1) e `[soft]` (warnings).

Hard limits (idênticos para todos os tipos — moldura branca do template,
calibrados para abranger 100% dos slides da Aula 1 publicada):
    x ∈ [400000, 7970000], y ∈ [400000, 4685000]

Soft limits (zona segura recomendada, padrão da Aula 1 publicada):
    padrao/conteudo: x ∈ [750000, 7700000],  y ∈ [500000, 4650000]
    capa:            x ∈ [1097275, 7887775], y ∈ [914400, 3900000]
    transicao:       x ∈ [1097275, 7600000], y ∈ [900000, 3905000]
    encerramento:    x ∈ [820000, 7745000],  y ∈ [914400, 3300000]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HARD = (400000, 400000, 7970000, 4685000)

SOFT = {
    "padrao":      (750000,  500000, 7700000, 4650000),
    "conteudo":    (750000,  500000, 7700000, 4650000),
    "capa":        (1097275, 914400, 7887775, 3900000),
    "transicao":   (1097275, 900000, 7600000, 3905000),
    "encerramento":(820000,  914400, 7745000, 3300000),
}

SHAPE_RE = re.compile(
    r"<p:(?P<tag>sp|pic|cxnSp|graphicFrame)\b[^>]*>(?P<body>.*?)</p:(?P=tag)>",
    re.DOTALL,
)
NAME_RE = re.compile(r'<p:cNvPr\s+id="(\d+)"\s+name="([^"]*)"')
XFRM_RE = re.compile(
    r'<a:xfrm[^>]*>\s*<a:off x="(-?\d+)" y="(-?\d+)"/>\s*'
    r'<a:ext cx="(\d+)" cy="(\d+)"/>',
)


def detect_type(xml: str, rels: str) -> str:
    """Infere o tipo do slide a partir do fundo (image1/image2) e do
    primeiro título textual."""
    image1 = "image1.png" in rels
    title = ""
    m = re.search(r"<a:t>([^<]+)</a:t>", xml)
    if m:
        title = m.group(1).strip().lower()
    if image1:
        if any(w in title for w in ("fim do bloco", "fim da aula", "intervalo")):
            return "encerramento"
        if re.match(r"^\d{2}$", title):
            return "transicao"
        return "capa"
    return "conteudo"


def check_box(box: tuple[int, int, int, int], x: int, y: int, x2: int, y2: int) -> list[str]:
    x_min, y_min, x_max, y_max = box
    issues = []
    if x < x_min:
        issues.append(f"x={x} < {x_min}")
    if y < y_min:
        issues.append(f"y={y} < {y_min}")
    if x2 > x_max:
        issues.append(f"x+cx={x2} > {x_max}")
    if y2 > y_max:
        issues.append(f"y+cy={y2} > {y_max}")
    return issues


def check_slide(path: Path, n: int) -> tuple[list[str], list[str]]:
    xml = path.read_text(encoding="utf-8")
    rels_path = path.parent / "_rels" / f"{path.name}.rels"
    rels = rels_path.read_text(encoding="utf-8") if rels_path.is_file() else ""
    tipo = detect_type(xml, rels)
    soft = SOFT[tipo]
    hard_errs: list[str] = []
    soft_warns: list[str] = []
    for m in SHAPE_RE.finditer(xml):
        body = m.group("body")
        nm = NAME_RE.search(body)
        sid, name = (nm.group(1), nm.group(2)) if nm else ("?", "?")
        xf = XFRM_RE.search(body)
        if not xf:
            continue
        x, y, cx, cy = (int(xf.group(i)) for i in range(1, 5))
        if cx == 0 or cy == 0:
            continue
        x2, y2 = x + cx, y + cy
        h = check_box(HARD, x, y, x2, y2)
        if h:
            hard_errs.append(
                f"[hard] slide{n} [{tipo}] sp#{sid} {name!r}: " + "; ".join(h)
            )
        else:
            s = check_box(soft, x, y, x2, y2)
            if s:
                soft_warns.append(
                    f"[soft] slide{n} [{tipo}] sp#{sid} {name!r}: " + "; ".join(s)
                )
    return hard_errs, soft_warns


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deck", type=Path, help="diretório do deck desempacotado")
    parser.add_argument(
        "--quiet-soft", action="store_true",
        help="suprime warnings [soft]; só imprime erros [hard]",
    )
    args = parser.parse_args()
    slides_dir = args.deck / "ppt" / "slides"
    if not slides_dir.is_dir():
        sys.exit(f"erro: {slides_dir} não existe")

    hard_errs: list[str] = []
    soft_warns: list[str] = []
    slides = sorted(
        slides_dir.glob("slide*.xml"),
        key=lambda p: int(re.search(r"\d+", p.name).group(0)),
    )
    for path in slides:
        n = int(re.search(r"slide(\d+)", path.name).group(1))
        h, s = check_slide(path, n)
        hard_errs.extend(h)
        soft_warns.extend(s)

    if not args.quiet_soft:
        for w in soft_warns:
            print(w)
    for e in hard_errs:
        print(e)
    print(
        f"\n{len(slides)} slide(s); "
        f"hard violations: {len(hard_errs)}; soft warnings: {len(soft_warns)}."
    )
    if hard_errs:
        sys.exit(1)


if __name__ == "__main__":
    main()
