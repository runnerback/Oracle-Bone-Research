"""Locate inscription references in a local PDF or render one page for inspection."""

import argparse
from contextlib import closing
from io import BytesIO
import json
from pathlib import Path
import re
import sys


def search_pages(document, args):
    if args.clause is not None:
        if not re.fullmatch(r"[0-9]+\.[0-9]+", args.clause):
            raise ValueError("Use a clause like 28.7, or use --term for other formats.")
        # A text layer can omit the space between the identifier and a glyph.
        pattern = re.compile(r"(?m)^[^\S\n]*" + re.escape(args.clause) + r"(?![0-9A-Za-z.])")
    else:
        words = args.term.split()
        if not words:
            raise ValueError("--term needs at least one non-space character.")
        pattern = re.compile(r"\s+".join(map(re.escape, words)), re.IGNORECASE)

    matches = []
    pages_with_text = 0
    for index in range(len(document)):
        with closing(document[index]) as page, closing(page.get_textpage()) as text_page:
            text = text_page.get_text_bounded().replace("\r\n", "\n").replace("\r", "\n")
        if text.strip():
            pages_with_text += 1
        match = pattern.search(text)
        if match:
            start = max(0, match.start() - 24)
            end = min(len(text), match.end() + 54)
            item = {"pdf_page": index + 1, "excerpt": " ".join(text[start:end].split())}
            if args.first_printed is not None:
                item["estimated_printed_page"] = args.first_printed + index
            matches.append(item)
    print(json.dumps({
        "file": args.pdf.name,
        "query": args.clause if args.clause is not None else args.term,
        "pages_checked": len(document),
        "pages_with_extractable_text": pages_with_text,
        "matching_pages": matches,
    }, ensure_ascii=False, indent=2))


def render_page(document, args):
    if not 1 <= args.page <= len(document):
        raise ValueError(f"PDF page must be between 1 and {len(document)}.")
    with closing(document[args.page - 1]) as page, closing(page.render(scale=2)) as bitmap:
        with bitmap.to_pil() as image, BytesIO() as buffer:
            image.save(buffer, format="PNG")
            with args.output.open("xb") as dest:
                dest.write(buffer.getvalue())
    print(args.output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    find = commands.add_parser("find", help="List pages containing a phrase or a clause heading.")
    find.add_argument("pdf", type=Path)
    query = find.add_mutually_exclusive_group(required=True)
    query.add_argument("--clause", help="Number at start of line, e.g. 28.7.")
    query.add_argument("--term", help="Literal text, case-insensitive, allowing wrapped spaces.")
    find.add_argument("--first-printed", type=int, help="Printed number of the first PDF page.")
    render = commands.add_parser("render", help="Render a one-based PDF page to a new PNG.")
    render.add_argument("pdf", type=Path)
    render.add_argument("page", type=int)
    render.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    try:
        import pypdfium2 as pdfium
    except ImportError:
        parser.exit(2, "Install the PDF helper dependency with: python3 -m pip install pypdfium2 Pillow\n")
    try:
        with pdfium.PdfDocument(args.pdf) as document:
            if args.command == "find":
                search_pages(document, args)
            else:
                render_page(document, args)
    except (OSError, ValueError, pdfium.PdfiumError, ImportError) as exc:
        print(f"{args.command}: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
