"""Desempacota um arquivo .pptx em um diretório, preservando a estrutura.

Uso:
    uv run python .cursor/skills/build-aula-pptx/scripts/unpack_pptx.py \\
        docs/templates/layout.pptx /tmp/deck/

O diretório de destino é criado se não existir. Se já existir e contiver
arquivos, o script falha por segurança (passe --force para sobrescrever).
"""

from __future__ import annotations

import argparse
import shutil
import sys
import zipfile
from pathlib import Path


def unpack(pptx_path: Path, dest: Path, force: bool = False) -> None:
    if not pptx_path.is_file():
        sys.exit(f"erro: arquivo .pptx não encontrado: {pptx_path}")

    if dest.exists() and any(dest.iterdir()):
        if not force:
            sys.exit(
                f"erro: diretório de destino não está vazio: {dest}\nuse --force para sobrescrever."
            )
        shutil.rmtree(dest)

    dest.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(pptx_path) as zf:
        zf.extractall(dest)

    print(f"OK desempacotado: {pptx_path} -> {dest}")
    print(f"   {sum(1 for _ in dest.rglob('*') if _.is_file())} arquivos extraídos")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pptx", type=Path, help="caminho do .pptx de origem")
    parser.add_argument("dest", type=Path, help="diretório de destino")
    parser.add_argument(
        "--force",
        action="store_true",
        help="sobrescreve o diretório de destino se ele já existir",
    )
    args = parser.parse_args()
    unpack(args.pptx, args.dest, force=args.force)


if __name__ == "__main__":
    main()
