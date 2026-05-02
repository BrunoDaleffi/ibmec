"""Renderiza um .pptx para .pdf usando LibreOffice headless.

Uso:
    uv run python .cursor/skills/pptx-qa/scripts/render_to_pdf.py \\
        aulas/aula_X/slides/aulaX_blocoY_jurimetria.pptx /tmp/qa/

Requer `soffice` no PATH (pacote `libreoffice` em Debian/Ubuntu).
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def render(pptx: Path, out_dir: Path) -> Path:
    if not pptx.is_file():
        sys.exit(f"erro: .pptx não encontrado: {pptx}")
    if shutil.which("soffice") is None:
        sys.exit(
            "erro: 'soffice' não está no PATH. Instale com:\n  sudo apt install -y libreoffice"
        )

    out_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        "soffice",
        "--headless",
        "--convert-to",
        "pdf",
        "--outdir",
        str(out_dir),
        str(pptx),
    ]
    print(f"$ {' '.join(cmd)}")
    res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if res.returncode != 0:
        sys.stderr.write(res.stderr)
        sys.exit(f"erro: soffice retornou {res.returncode}")

    out_pdf = out_dir / f"{pptx.stem}.pdf"
    if not out_pdf.is_file():
        sys.exit(f"erro: PDF esperado não foi gerado: {out_pdf}")

    print(f"OK PDF gerado: {out_pdf} ({out_pdf.stat().st_size:,} bytes)")
    return out_pdf


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pptx", type=Path)
    parser.add_argument("out_dir", type=Path)
    args = parser.parse_args()
    render(args.pptx, args.out_dir)


if __name__ == "__main__":
    main()
