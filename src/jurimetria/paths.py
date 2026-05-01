"""Caminhos canônicos do projeto.

Centraliza referências de diretórios para que notebooks e scripts não dependam
de caminhos relativos frágeis (que quebram conforme o cwd muda).
"""

from __future__ import annotations

from pathlib import Path

ROOT_DIR: Path = Path(__file__).resolve().parents[2]
"""Raiz do repositório (acima de ``src/``)."""

DATA_DIR: Path = ROOT_DIR / "data"
RAW_DATA_DIR: Path = DATA_DIR / "raw"
PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
EXTERNAL_DATA_DIR: Path = DATA_DIR / "external"

AULAS_DIR: Path = ROOT_DIR / "aulas"
DOCS_DIR: Path = ROOT_DIR / "docs"
