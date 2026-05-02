"""Duplica um slide existente em um pacote .pptx desempacotado.

Uso:
    uv run python .cursor/skills/build-aula-pptx/scripts/add_slide.py \\
        /tmp/deck/ slide2.xml

Onde `slide2.xml` é o slide modelo (de conteúdo, fundo image1.png).
Para criar um slide de capa/transição, passe `slide1.xml` (fundo image2.png).

Faz, em ordem:
1. Encontra o próximo número de slide disponível (slideN.xml).
2. Copia `slideX.xml` -> `slideN.xml` em `ppt/slides/`.
3. Copia `_rels/slideX.xml.rels` -> `_rels/slideN.xml.rels`.
4. Adiciona uma `<Override PartName="/ppt/slides/slideN.xml" .../>` em
   `[Content_Types].xml`.
5. Adiciona `<Relationship Id="rIdSlideN" Type="...slide" Target="slides/slideN.xml"/>`
   em `ppt/_rels/presentation.xml.rels` e devolve o `rIdSlideN`.

**NÃO** modifica `<p:sldIdLst>` em `ppt/presentation.xml`. Cabe ao chamador
inserir o novo `<p:sldId id="..." r:id="rIdSlideN"/>` na posição desejada.

Imprime um JSON com:
    {
      "slide_xml": "slide7.xml",
      "rels_xml": "slide7.xml.rels",
      "rId": "rIdSlide7",
      "p_sldId_xml": "<p:sldId id=\"...\" r:id=\"rIdSlide7\"/>"
    }
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

CT_NS_OVERRIDE = (
    '<Override PartName="/ppt/slides/{slide_xml}" '
    'ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
)
REL_TYPE_SLIDE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide"


def next_slide_number(slides_dir: Path) -> int:
    pat = re.compile(r"slide(\d+)\.xml$")
    nums = [int(m.group(1)) for p in slides_dir.iterdir() if (m := pat.match(p.name))]
    return max(nums, default=0) + 1


def next_rid(rels_path: Path) -> tuple[str, int]:
    txt = rels_path.read_text(encoding="utf-8")
    rids = [int(m) for m in re.findall(r'Id="rId(\d+)"', txt)]
    n = max(rids, default=0) + 1
    return f"rId{n}", n


def reserved_p_sld_id(presentation_xml: Path, new_slide_number: int) -> int:
    """Devolve um p:sldId/@id único e estável.

    PowerPoint exige `id >= 256` e único. Para evitar colisões quando o
    chamador roda várias chamadas seguidas sem editar `presentation.xml`,
    usamos `max(existentes, 255 + new_slide_number) + offset_se_necessário`.
    """
    txt = presentation_xml.read_text(encoding="utf-8")
    used = {int(m) for m in re.findall(r'<p:sldId\s+id="(\d+)"', txt)}
    candidate = max(255 + new_slide_number, 256)
    while candidate in used:
        candidate += 1
    return candidate


def add_slide(deck: Path, model: str) -> dict[str, str]:
    if not deck.is_dir():
        sys.exit(f"erro: diretório do deck não encontrado: {deck}")

    slides_dir = deck / "ppt" / "slides"
    rels_dir = slides_dir / "_rels"
    ct_path = deck / "[Content_Types].xml"
    pres_rels_path = deck / "ppt" / "_rels" / "presentation.xml.rels"
    pres_xml_path = deck / "ppt" / "presentation.xml"

    src_slide = slides_dir / model
    src_rels = rels_dir / f"{model}.rels"
    if not src_slide.is_file():
        sys.exit(f"erro: slide modelo não encontrado: {src_slide}")
    if not src_rels.is_file():
        sys.exit(f"erro: rels do modelo não encontrado: {src_rels}")
    for required in (ct_path, pres_rels_path, pres_xml_path):
        if not required.is_file():
            sys.exit(f"erro: arquivo essencial não encontrado: {required}")

    n = next_slide_number(slides_dir)
    new_slide_name = f"slide{n}.xml"
    new_rels_name = f"{new_slide_name}.rels"
    new_slide_path = slides_dir / new_slide_name
    new_rels_path = rels_dir / new_rels_name

    shutil.copy2(src_slide, new_slide_path)
    shutil.copy2(src_rels, new_rels_path)

    ct_text = ct_path.read_text(encoding="utf-8")
    override = CT_NS_OVERRIDE.format(slide_xml=new_slide_name)
    if override not in ct_text:
        ct_text = ct_text.replace("</Types>", f"  {override}\n</Types>")
        ct_path.write_text(ct_text, encoding="utf-8")

    rid, _ = next_rid(pres_rels_path)
    rels_text = pres_rels_path.read_text(encoding="utf-8")
    new_rel = f'<Relationship Id="{rid}" Type="{REL_TYPE_SLIDE}" Target="slides/{new_slide_name}"/>'
    if new_rel not in rels_text:
        rels_text = rels_text.replace("</Relationships>", f"  {new_rel}\n</Relationships>")
        pres_rels_path.write_text(rels_text, encoding="utf-8")

    p_sld_id = reserved_p_sld_id(pres_xml_path, n)
    p_sld_xml = f'<p:sldId id="{p_sld_id}" r:id="{rid}"/>'

    return {
        "slide_xml": new_slide_name,
        "rels_xml": new_rels_name,
        "rId": rid,
        "p_sldId_id": str(p_sld_id),
        "p_sldId_xml": p_sld_xml,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deck", type=Path, help="diretório do .pptx desempacotado")
    parser.add_argument(
        "model",
        help="nome do slide modelo a duplicar (ex.: slide1.xml ou slide2.xml)",
    )
    args = parser.parse_args()
    info = add_slide(args.deck, args.model)
    print(json.dumps(info, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
