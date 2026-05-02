"""Extrai o texto de cada slide de um .pptx (ou de um diretório desempacotado).

Uso:
    uv run python .cursor/skills/build-aula-pptx/scripts/extract_slide_text.py \\
        aulas/aula_2/slides/aula2_bloco1_jurimetria.pptx
    uv run python .cursor/skills/build-aula-pptx/scripts/extract_slide_text.py \\
        /tmp/deck/

Útil para QA textual: confere se todos os tópicos do plano foram cobertos,
se não sobrou placeholder ("Lorem ipsum", "Texto do exemplo") e se os
títulos batem com a tabela planejada.
"""

from __future__ import annotations

import argparse
import io
import re
import sys
import zipfile
from pathlib import Path

SLIDE_PATH = re.compile(r"^ppt/slides/slide(\d+)\.xml$")


def text_from_xml(xml: str) -> str:
    """Concatena o texto dos `<a:t>...</a:t>` na ordem em que aparecem."""
    pieces: list[str] = []
    for m in re.finditer(r"<a:t[^>]*>(.*?)</a:t>", xml, flags=re.DOTALL):
        raw = m.group(1)
        raw = (
            raw.replace("&amp;", "&")
            .replace("&quot;", '"')
            .replace("&lt;", "<")
            .replace("&gt;", ">")
            .replace("&apos;", "'")
        )
        pieces.append(raw)
    text = "\n".join(pieces)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def from_pptx(path: Path) -> dict[int, str]:
    out: dict[int, str] = {}
    with zipfile.ZipFile(path) as zf:
        for name in zf.namelist():
            m = SLIDE_PATH.match(name)
            if not m:
                continue
            with zf.open(name) as f:
                xml = io.TextIOWrapper(f, encoding="utf-8").read()
            out[int(m.group(1))] = text_from_xml(xml)
    return out


def from_dir(deck: Path) -> dict[int, str]:
    out: dict[int, str] = {}
    slides_dir = deck / "ppt" / "slides"
    if not slides_dir.is_dir():
        sys.exit(f"erro: {slides_dir} não existe (esperado um deck desempacotado).")
    for p in slides_dir.iterdir():
        m = re.match(r"slide(\d+)\.xml$", p.name)
        if not m:
            continue
        out[int(m.group(1))] = text_from_xml(p.read_text(encoding="utf-8"))
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help=".pptx ou diretório desempacotado")
    parser.add_argument(
        "--only",
        type=int,
        nargs="*",
        help="lista opcional de slides para imprimir (ex.: --only 1 7 12)",
    )
    args = parser.parse_args()

    if not args.source.exists():
        sys.exit(f"erro: caminho não encontrado: {args.source}")

    slides = from_pptx(args.source) if args.source.is_file() else from_dir(args.source)
    if not slides:
        sys.exit("erro: nenhum slideN.xml encontrado.")

    selected = sorted(args.only) if args.only else sorted(slides.keys())
    for n in selected:
        text = slides.get(n, "<slide ausente>")
        sep = "=" * 60
        print(f"\n{sep}\nSLIDE {n}\n{sep}\n{text}")


if __name__ == "__main__":
    main()
