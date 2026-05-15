"""Extrai os tópicos de um bloco específico do plano de ensino (.docx).

Uso:
    uv run python .cursor/skills/build-aula-pptx/scripts/extract_block_from_plan.py \\
        docs/plano_curso.docx --aula 2 --bloco 1

Saída:
    Aula 2 — O Ciclo da Ciência de Dados Aplicado ao Direito (Parte 1)
    Bloco 1 (1h50)

    1. Introdução ao ciclo da ciência de dados aplicado ao Direito: ...
    2. Por que pensar em ciclo importa: ...
    ...

A extração faz parsing do XML do .docx (não usa python-docx) para evitar
dependências extras. Identifica a "Aula N" pelo cabeçalho com travessão
em U+2014, e "Bloco K" pelos rótulos "Bloco 1 (1h50)" / "Bloco 2 (1h50)".
"""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path


def docx_to_paragraphs(docx_path: Path) -> list[str]:
    """Extrai os parágrafos do .docx como strings limpas."""
    if not docx_path.is_file():
        sys.exit(f"erro: arquivo .docx não encontrado: {docx_path}")
    with zipfile.ZipFile(docx_path) as z, z.open("word/document.xml") as f:
        xml = f.read().decode("utf-8")
    text = re.sub(r"</w:p>", "\n", xml)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("&amp;", "&").replace("&quot;", '"')
    text = text.replace("&lt;", "<").replace("&gt;", ">")
    return [ln.strip() for ln in text.split("\n")]


def extract_block(paragraphs: list[str], aula: int, bloco: int) -> tuple[str, list[str]]:
    """Encontra a aula e o bloco pedidos e devolve (titulo_aula, lista_de_topicos)."""
    aula_pat = re.compile(rf"^Aula\s+{aula}\b\s*[—\-–]\s*(.+)$")
    next_aula_pat = re.compile(rf"^Aula\s+{aula + 1}\b\s*[—\-–]")
    bloco_pat = re.compile(rf"^Bloco\s+{bloco}\b")
    other_bloco_pat = re.compile(r"^Bloco\s+\d+\b")

    aula_idx = next((i for i, p in enumerate(paragraphs) if aula_pat.match(p)), -1)
    if aula_idx < 0:
        sys.exit(f"erro: 'Aula {aula}' não encontrada no plano.")
    aula_title = aula_pat.match(paragraphs[aula_idx]).group(0)

    end_idx = next(
        (
            i
            for i, p in enumerate(paragraphs[aula_idx + 1 :], start=aula_idx + 1)
            if next_aula_pat.match(p)
        ),
        len(paragraphs),
    )

    bloco_idx = next(
        (
            i
            for i, p in enumerate(paragraphs[aula_idx + 1 : end_idx], start=aula_idx + 1)
            if bloco_pat.match(p)
        ),
        -1,
    )
    if bloco_idx < 0:
        sys.exit(f"erro: 'Bloco {bloco}' não encontrado dentro da Aula {aula}.")

    bloco_end = next(
        (
            i
            for i, p in enumerate(paragraphs[bloco_idx + 1 : end_idx], start=bloco_idx + 1)
            if other_bloco_pat.match(p) or p.startswith("☕ Intervalo")
        ),
        end_idx,
    )

    skip = {
        "#",
        "Bloco",
        "Conteúdo",
        f"Bloco {bloco} (1h50)",
        "1",
    }
    topics: list[str] = []
    for raw in paragraphs[bloco_idx + 1 : bloco_end]:
        line = raw.strip()
        if not line or line in skip:
            continue
        if re.fullmatch(r"\d+", line):
            continue
        if line.lower().startswith("bloco "):
            continue
        topics.append(line)

    return aula_title, topics


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("docx", type=Path, help="caminho do plano de ensino .docx")
    parser.add_argument("--aula", type=int, required=True, help="número da aula (1 a 6)")
    parser.add_argument("--bloco", type=int, required=True, help="número do bloco (1 ou 2)")
    args = parser.parse_args()

    if args.aula < 1 or args.aula > 6:
        sys.exit("erro: --aula deve estar entre 1 e 6.")
    if args.bloco not in (1, 2):
        sys.exit("erro: --bloco deve ser 1 ou 2.")

    paragraphs = docx_to_paragraphs(args.docx)
    aula_title, topics = extract_block(paragraphs, args.aula, args.bloco)

    print(aula_title)
    print(f"Bloco {args.bloco} (1h50)")
    print()
    for i, t in enumerate(topics, start=1):
        print(f"{i:>2}. {t}")


if __name__ == "__main__":
    main()
