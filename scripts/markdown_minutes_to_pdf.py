#!/usr/bin/env python3
"""Convert a Chinese meeting-minutes Markdown file to PDF.

Usage:
  python markdown_minutes_to_pdf.py input.md output.pdf

This is intentionally small and dependency-light. It supports headings,
paragraphs, simple numbered/bulleted lists, and pipe tables.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


FONT = "STSong-Light"
FORBIDDEN_TERMS = ("ChatGPT", "Gemini", "AI", "人工智慧", "由模型整理", "由機器生成")


def register_font() -> None:
    pdfmetrics.registerFont(UnicodeCIDFont(FONT))


def escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("**", "")
    )


def para(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(escape(text), style)


def parse_table(lines: list[str], start: int) -> tuple[list[list[str]], int]:
    table_lines = []
    idx = start
    while idx < len(lines) and lines[idx].strip().startswith("|"):
        table_lines.append(lines[idx].strip())
        idx += 1

    rows = []
    for raw in table_lines:
        cells = [cell.strip() for cell in raw.strip("|").split("|")]
        if cells and all(set(cell) <= {"-", ":", " "} for cell in cells):
            continue
        rows.append(cells)
    return rows, idx


def styles():
    base = getSampleStyleSheet()
    title = ParagraphStyle(
        "TitleZh",
        parent=base["Title"],
        fontName=FONT,
        fontSize=20,
        leading=26,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#0B2545"),
        spaceAfter=16,
    )
    h2 = ParagraphStyle(
        "H2Zh",
        parent=base["Heading2"],
        fontName=FONT,
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#1F4D78"),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True,
    )
    h3 = ParagraphStyle(
        "H3Zh",
        parent=base["Heading3"],
        fontName=FONT,
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor("#2E74B5"),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True,
    )
    body = ParagraphStyle(
        "BodyZh",
        parent=base["BodyText"],
        fontName=FONT,
        fontSize=10,
        leading=15,
        alignment=TA_LEFT,
        spaceAfter=6,
    )
    bullet = ParagraphStyle("BulletZh", parent=body, leftIndent=14, firstLineIndent=-10)
    table = ParagraphStyle("TableZh", parent=body, fontSize=8.5, leading=12, spaceAfter=0)
    return title, h2, h3, body, bullet, table


def build_pdf(input_md: Path, output_pdf: Path) -> None:
    register_font()
    source = input_md.read_text(encoding="utf-8")
    found = [term for term in FORBIDDEN_TERMS if term in source]
    if found:
        raise SystemExit(f"Forbidden source/AI terms found in Markdown: {', '.join(found)}")

    title, h2, h3, body, bullet, table_style = styles()
    doc = SimpleDocTemplate(
        str(output_pdf),
        pagesize=A4,
        rightMargin=1.6 * cm,
        leftMargin=1.6 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
        title=input_md.stem,
        author="",
    )

    story = []
    lines = source.splitlines()
    idx = 0
    while idx < len(lines):
        line = lines[idx].strip()
        if not line:
            idx += 1
            continue
        if line.startswith("|"):
            rows, idx = parse_table(lines, idx)
            if rows:
                rendered = [[para(cell, table_style) for cell in row] for row in rows]
                col_count = max(len(row) for row in rows)
                available = A4[0] - 3.2 * cm
                if col_count == 2:
                    widths = [3.1 * cm, available - 3.1 * cm]
                elif col_count == 5:
                    widths = [1.1 * cm, 5.7 * cm, 3.4 * cm, 3.0 * cm, available - 13.2 * cm]
                else:
                    widths = [available / col_count] * col_count
                tbl = Table(rendered, colWidths=widths, repeatRows=1)
                tbl.setStyle(
                    TableStyle(
                        [
                            ("FONTNAME", (0, 0), (-1, -1), FONT),
                            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EAF2F8")),
                            ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#0B2545")),
                            ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#D9E2EC")),
                            ("VALIGN", (0, 0), (-1, -1), "TOP"),
                            ("LEFTPADDING", (0, 0), (-1, -1), 5),
                            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                            ("TOPPADDING", (0, 0), (-1, -1), 5),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                        ]
                    )
                )
                story.append(tbl)
                story.append(Spacer(1, 8))
            continue
        if line.startswith("# "):
            story.append(para(line[2:].strip(), title))
        elif line.startswith("## "):
            story.append(para(line[3:].strip(), h2))
        elif line.startswith("### "):
            story.append(para(line[4:].strip(), h3))
        elif line[:2].isdigit() and ". " in line[:4]:
            story.append(para(line, bullet))
        elif line.startswith("- "):
            story.append(para("- " + line[2:].strip(), bullet))
        else:
            story.append(para(line, body))
        idx += 1

    doc.build(story)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_md", type=Path)
    parser.add_argument("output_pdf", type=Path)
    args = parser.parse_args()
    build_pdf(args.input_md, args.output_pdf)


if __name__ == "__main__":
    main()
