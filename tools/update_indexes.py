#!/usr/bin/env python3
"""Update per-folder index.html pages based on available HTML files."""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

CATEGORIES = [
    {
        "slug": "addition",
        "title": "Addition",
        "description": "Core number bonds and quick sums.",
    },
    {
        "slug": "subtraction",
        "title": "Subtraction",
        "description": "Difference, borrowing, and mental methods.",
    },
    {
        "slug": "multiplication-division",
        "title": "Multiplication and Division",
        "description": "Times tables, factors, and sharing.",
    },
    {
        "slug": "percentage",
        "title": "Percentage",
        "description": "Percent change, discounts, and rates.",
    },
    {
        "slug": "ratio",
        "title": "Ratio",
        "description": "Proportion, scaling, and simplification.",
    },
    {
        "slug": "square-roots",
        "title": "Square Roots",
        "description": "Square numbers and roots practice.",
    },
    {
        "slug": "algebra",
        "title": "Algebra",
        "description": "Expressions, equations, and sequences.",
    },
    {
        "slug": "geometry",
        "title": "Geometry",
        "description": "Shapes, angles, and measures.",
    },
    {
        "slug": "trigonometry",
        "title": "Trigonometry",
        "description": "Sine, cosine, and tangent basics.",
    },
    {
        "slug": "miscellaneous",
        "title": "Miscellaneous",
        "description": "Mixed practice and challenges.",
    },
]


def title_from_filename(filename: str) -> str:
    stem = Path(filename).stem
    if not stem:
        return filename
    words = re.sub(r"[-_]+", " ", stem).strip()
    return words.title() if words else stem


def build_page(title: str, description: str, items: list[Path]) -> str:
    cards = []
    if items:
        for path in items:
            label = title_from_filename(path.name)
            cards.append(
                f"""
      <a class=\"page-card\" href=\"{path.name}\">
        <strong>{label}</strong>
        <small>{path.name}</small>
      </a>"""
            )
        grid = "\n".join(cards)
    else:
        grid = (
            "\n".join(
                [
                    "    <div class=\"empty-state\">",
                    "      No pages yet. Add a new HTML file in this folder and run tools/update_indexes.py.",
                    "    </div>",
                ]
            )
        )

    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>{title} - Maths Aide</title>
  <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">
  <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>
  <link href=\"https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap\" rel=\"stylesheet\">
  <link rel=\"stylesheet\" href=\"../assets/styles.css\">
</head>
<body>
  <main class=\"container\">
    <div class=\"breadcrumb\">
      <a href=\"../index.html\">Home</a> / {title}
    </div>
    <h1 class=\"category-title\">{title}</h1>
    <p class=\"category-desc\">{description}</p>

    <section class=\"page-grid\">{grid}
    </section>
  </main>
</body>
</html>
"""


def main() -> None:
    for category in CATEGORIES:
        folder = ROOT / category["slug"]
        folder.mkdir(parents=True, exist_ok=True)
        html_files = sorted(
            [p for p in folder.glob("*.html") if p.name.lower() != "index.html"],
            key=lambda p: p.name.lower(),
        )
        page = build_page(category["title"], category["description"], html_files)
        (folder / "index.html").write_text(page, encoding="utf-8")


if __name__ == "__main__":
    main()
