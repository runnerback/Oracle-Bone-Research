"""Build an installable skill ZIP from the maintained source files."""

import argparse
import json
from pathlib import Path
from tempfile import NamedTemporaryFile
from zipfile import ZIP_DEFLATED, ZipFile


NAME = "oracle-bone-research"
ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / NAME
EXAMPLE_PLATES = {"h00052.jpg", "h00659.jpg", "h05377.jpg"}
RESOURCES = (
    "SKILL.md", "references/sources.md", "references/worked-example.md",
    "references/glyph-case.md", "references/acknowledgments.md",
    "scripts/source_pages.py", "scripts/glyph_case.py", "LICENSE", "requirements.txt",
    "assets/obimd/LICENSE",
    "assets/alphaoracle/LICENSE", "assets/alphaoracle/CITATION.cff",
    "assets/alphaoracle/images/h00659.jpg", "assets/alphaoracle/images/合52拓片.png",
)


def workbuddy_manifest(source, author, version):
    header, body = source.split("\n---\n", 1)
    fields = {
        "display_name": "甲骨文考释助手",
        "display_name_en": "Oracle Bone Inscription Research",
        "description_zh": "结合 OBIMD 标注与 AlphaOracle 字形候选，核对片号、辞例和已有释读。",
        "description_en": "Compare disputed oracle bone readings against glyphs, parallel inscriptions, and prior scholarship.",
        "author": author,
        "version": version,
    }
    for key, value in fields.items():
        header += f"\n{key}: {json.dumps(value, ensure_ascii=False)}"
    for resource in RESOURCES:
        if resource.startswith("references/"):
            body = body.replace(f"]({resource})", f"]({resource}) @{resource}")
    return header + "\n---\n" + body


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("platform", choices=("standard", "workbuddy"))
    parser.add_argument("--author", help="Publisher name for the WorkBuddy package.")
    parser.add_argument("--version", default="0.3.2", help="WorkBuddy release version.")
    parser.add_argument("--out-dir", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    if args.platform == "workbuddy" and not (args.author and args.author.strip()):
        parser.error("For WorkBuddy, supply the intended publisher name with --author.")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    dest = args.out_dir / f"{NAME}-{args.platform}.zip"
    files = list(RESOURCES)
    if args.platform == "standard":
        files.append("agents/openai.yaml")
    with NamedTemporaryFile(dir=dest.parent, delete=False) as temp:
        temp_path = Path(temp.name)
    try:
        with ZipFile(temp_path, "w", compression=ZIP_DEFLATED) as archive:
            with (SKILL / "assets/obimd/all_dataset.json").open(encoding="utf-8") as src:
                samples = [row for row in json.load(src) if row["name"] in EXAMPLE_PLATES]
            if {row["name"] for row in samples} != EXAMPLE_PLATES:
                raise ValueError("Missing OBIMD example plates")
            archive.writestr(f"{NAME}/assets/obimd/example_plates.json", json.dumps(samples, ensure_ascii=False))
            for filename in files:
                content = (SKILL / filename).read_bytes()
                if args.platform == "workbuddy" and filename == "SKILL.md":
                    content = workbuddy_manifest(content.decode("utf-8"), args.author.strip(), args.version).encode("utf-8")
                archive.writestr(f"{NAME}/{filename}", content)
        temp_path.replace(dest)
    finally:
        temp_path.unlink(missing_ok=True)
    print(dest)


if __name__ == "__main__":
    main()
