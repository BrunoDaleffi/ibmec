"""Detecta travessões e hífens em função parentética nos slides.

Uso:
    uv run python .cursor/skills/pptx-qa/scripts/check_no_emdash.py \\
        aulas/aula_X/slides/aulaX_blocoY_jurimetria.pptx

Lê apenas o conteúdo dentro de `<a:t>...</a:t>` (texto visível dos
slides), não o XML cru. Para cada caractere candidato (`—`, `–`, `-`),
classifica como:

- **PROIBIDO**: separador parentético (espaço antes E espaço depois).
- **OK**: intervalo numérico (`2010–2024`), palavra composta
  (`teórico-prática`), travessão de diálogo no início de linha.

Saída por slide com o trecho destacado e a classificação. Exit code 1
se houver pelo menos uma ocorrência proibida.
"""

from __future__ import annotations

import argparse
import io
import re
import sys
import zipfile
from pathlib import Path

SLIDE_PATH = re.compile(r"^ppt/(slides/slide\d+\.xml|notesSlides/notesSlide\d+\.xml)$")
DASH_RE = re.compile(r"[—–\-]")
INTERVAL_RE = re.compile(r"\d\s*[—–\-]\s*\d")


def text_blocks(xml: str) -> list[str]:
    blocks: list[str] = []
    for m in re.finditer(r"<a:t[^>]*>(.*?)</a:t>", xml, flags=re.DOTALL):
        raw = m.group(1)
        raw = (
            raw.replace("&amp;", "&")
            .replace("&quot;", '"')
            .replace("&lt;", "<")
            .replace("&gt;", ">")
            .replace("&apos;", "'")
        )
        blocks.append(raw)
    return blocks


def classify(text: str, idx: int) -> tuple[str, str]:
    """Classifica a ocorrência do dash no índice `idx` em `text`.

    Devolve (categoria, motivo). categoria ∈ {"PROIBIDO", "OK"}.
    """
    char = text[idx]
    left = text[max(0, idx - 1) : idx]
    right = text[idx + 1 : idx + 2]

    if INTERVAL_RE.search(text[max(0, idx - 5) : idx + 5]):
        return ("OK", "intervalo numérico")

    if char == "-" and left.isalpha() and right.isalpha():
        return ("OK", "hífen em palavra composta")

    if idx == 0 and char in "—–":
        return ("OK", "travessão de diálogo (início de linha)")

    if left == " " and right == " ":
        return ("PROIBIDO", "separador parentético")

    if (not left or left == " ") and right == " " and char in "—–":
        return ("PROIBIDO", "separador parentético no início")

    if left == " " and (not right or right == " ") and char in "—–":
        return ("PROIBIDO", "separador parentético no fim")

    return ("OK", "uso aceitável")


def scan_xml(name: str, xml: str) -> tuple[list[dict], list[dict]]:
    issues: list[dict] = []
    oks: list[dict] = []
    for block in text_blocks(xml):
        for m in DASH_RE.finditer(block):
            cat, reason = classify(block, m.start())
            ctx_start = max(0, m.start() - 30)
            ctx_end = min(len(block), m.end() + 30)
            ctx = block[ctx_start:ctx_end].replace("\n", " ")
            entry = {
                "slide": name,
                "char": block[m.start()],
                "reason": reason,
                "context": ctx,
            }
            (issues if cat == "PROIBIDO" else oks).append(entry)
    return issues, oks


def slide_iter(pptx: Path):
    if pptx.is_file():
        with zipfile.ZipFile(pptx) as zf:
            for name in sorted(zf.namelist()):
                if SLIDE_PATH.match(name):
                    with zf.open(name) as f:
                        yield name, io.TextIOWrapper(f, encoding="utf-8").read()
    elif pptx.is_dir():
        for sub in ("ppt/slides", "ppt/notesSlides"):
            d = pptx / sub
            if not d.is_dir():
                continue
            for p in sorted(d.glob("*.xml")):
                yield p.relative_to(pptx).as_posix(), p.read_text(encoding="utf-8")
    else:
        sys.exit(f"erro: caminho não encontrado: {pptx}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help=".pptx ou diretório desempacotado")
    parser.add_argument("--show-ok", action="store_true", help="lista também os usos legítimos")
    args = parser.parse_args()

    all_issues: list[dict] = []
    all_oks: list[dict] = []
    for name, xml in slide_iter(args.source):
        issues, oks = scan_xml(name, xml)
        all_issues.extend(issues)
        all_oks.extend(oks)

    if args.show_ok and all_oks:
        print(f"\n=== {len(all_oks)} ocorrência(s) legítima(s) (OK) ===")
        for e in all_oks:
            print(f"  [{e['slide']}] '{e['char']}' ({e['reason']}): ...{e['context']}...")

    if all_issues:
        print(f"\n=== {len(all_issues)} ocorrência(s) PROIBIDA(s) ===")
        for e in all_issues:
            print(f"  [{e['slide']}] '{e['char']}' ({e['reason']}): ...{e['context']}...")
        print(
            "\nCorrija substituindo por vírgulas, parênteses ou nova frase. "
            "Veja .cursor/skills/build-aula-pptx/content-rules.md."
        )
        sys.exit(1)

    print("OK nenhum travessão ou hífen em função parentética encontrado.")


if __name__ == "__main__":
    main()
