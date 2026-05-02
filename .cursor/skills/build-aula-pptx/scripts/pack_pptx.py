"""Empacota um diretório de volta em um arquivo .pptx (zip).

Uso:
    uv run python .cursor/skills/build-aula-pptx/scripts/pack_pptx.py \\
        /tmp/deck/ aulas/aula_2/slides/aula2_bloco1_jurimetria.pptx

Garante que `[Content_Types].xml` seja o primeiro entry do zip, como o
PowerPoint espera. Cria o diretório de saída se não existir e
sobrescreve o arquivo final.
"""

from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path

CONTENT_TYPES = "[Content_Types].xml"


def pack(src: Path, out_pptx: Path) -> None:
    if not src.is_dir():
        sys.exit(f"erro: diretório de origem não encontrado: {src}")

    ct_path = src / CONTENT_TYPES
    if not ct_path.is_file():
        sys.exit(f"erro: faltando {CONTENT_TYPES} em {src}")

    out_pptx.parent.mkdir(parents=True, exist_ok=True)

    files: list[Path] = sorted(p for p in src.rglob("*") if p.is_file())

    with zipfile.ZipFile(out_pptx, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(ct_path, CONTENT_TYPES)
        for fp in files:
            arcname = fp.relative_to(src).as_posix()
            if arcname == CONTENT_TYPES:
                continue
            zf.write(fp, arcname)

    print(f"OK empacotado: {src} -> {out_pptx}")
    print(f"   {len(files)} arquivos zipados ({out_pptx.stat().st_size:,} bytes)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("src", type=Path, help="diretório com a estrutura desempacotada")
    parser.add_argument("out", type=Path, help="caminho do .pptx final")
    args = parser.parse_args()
    pack(args.src, args.out)


if __name__ == "__main__":
    main()
