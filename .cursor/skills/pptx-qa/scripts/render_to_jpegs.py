"""Renderiza um .pdf para uma sequência de JPEGs (1 por página).

Uso:
    uv run python .cursor/skills/pptx-qa/scripts/render_to_jpegs.py \\
        /tmp/qa/aulaX_blocoY_jurimetria.pdf /tmp/qa/

Saída: arquivos `slide-001.jpg`, `slide-002.jpg`, ... no diretório
de destino.

Requer `pdftoppm` no PATH (pacote `poppler-utils`).
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def render(pdf: Path, out_dir: Path, dpi: int = 120) -> list[Path]:
    if not pdf.is_file():
        sys.exit(f"erro: PDF não encontrado: {pdf}")
    if shutil.which("pdftoppm") is None:
        sys.exit(
            "erro: 'pdftoppm' não está no PATH. Instale com:\n  sudo apt install -y poppler-utils"
        )

    out_dir.mkdir(parents=True, exist_ok=True)

    for old in out_dir.glob("slide-*.jpg"):
        old.unlink()

    prefix = out_dir / "slide"
    cmd = ["pdftoppm", "-jpeg", "-r", str(dpi), str(pdf), str(prefix)]
    print(f"$ {' '.join(cmd)}")
    res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if res.returncode != 0:
        sys.stderr.write(res.stderr)
        sys.exit(f"erro: pdftoppm retornou {res.returncode}")

    jpegs = sorted(out_dir.glob("slide-*.jpg"))
    if not jpegs:
        sys.exit("erro: nenhum JPEG foi gerado.")
    print(f"OK {len(jpegs)} JPEG(s) em {out_dir}")
    for j in jpegs[:3]:
        print(f"   {j.name}")
    if len(jpegs) > 3:
        print(f"   ... e mais {len(jpegs) - 3}")
    return jpegs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("out_dir", type=Path)
    parser.add_argument("--dpi", type=int, default=120)
    args = parser.parse_args()
    render(args.pdf, args.out_dir, dpi=args.dpi)


if __name__ == "__main__":
    main()
