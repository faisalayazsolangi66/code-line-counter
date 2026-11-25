#!/usr/bin/env python3
"""Count lines of code by language in a project directory.

Reports total, code, blank and comment lines per language, plus a
grand total. Skips common generated/vendor directories by default.
"""
import argparse
import os
import sys
from collections import defaultdict

EXTENSIONS = {
    ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript",
    ".jsx": "JavaScript", ".tsx": "TypeScript", ".java": "Java",
    ".c": "C", ".h": "C", ".cpp": "C++", ".hpp": "C++", ".cs": "C#",
    ".go": "Go", ".rs": "Rust", ".rb": "Ruby", ".php": "PHP",
    ".html": "HTML", ".css": "CSS", ".scss": "SCSS", ".sql": "SQL",
    ".sh": "Shell", ".bash": "Shell", ".lua": "Lua", ".kt": "Kotlin",
    ".swift": "Swift", ".md": "Markdown", ".json": "JSON",
    ".yaml": "YAML", ".yml": "YAML", ".toml": "TOML", ".xml": "XML",
}

COMMENT_MARKERS = {
    "Python": "#", "JavaScript": "//", "TypeScript": "//", "Java": "//",
    "C": "//", "C++": "//", "C#": "//", "Go": "//", "Rust": "//",
    "Ruby": "#", "PHP": "//", "Shell": "#", "SQL": "--", "Lua": "--",
    "Kotlin": "//", "Swift": "//", "CSS": "/*", "SCSS": "//",
}

DEFAULT_IGNORE = {".git", "__pycache__", "node_modules", "venv", ".venv",
                  "dist", "build", ".idea", ".tox", "vendor", "target"}


def count_file(path, language):
    code = blank = comment = 0
    marker = COMMENT_MARKERS.get(language)
    try:
        with open(path, encoding="utf-8", errors="ignore") as fh:
            for line in fh:
                stripped = line.strip()
                if not stripped:
                    blank += 1
                elif marker and stripped.startswith(marker):
                    comment += 1
                else:
                    code += 1
    except OSError:
        return None
    return code, blank, comment


def main():
    parser = argparse.ArgumentParser(
        description="Count lines of code by language in a project.")
    parser.add_argument("path", nargs="?", default=".",
                        help="Directory to scan (default: current directory)")
    parser.add_argument("--ignore", default="",
                        help="Extra comma-separated directory names to skip")
    parser.add_argument("--extensions", default="",
                        help="Extra mappings, e.g. '.vue:Vue,.zig:Zig'")
    parser.add_argument("--sort", choices=["lines", "files", "name"],
                        default="lines", help="Sort order (default: lines)")
    args = parser.parse_args()

    ext_map = dict(EXTENSIONS)
    for item in args.extensions.split(","):
        if ":" in item:
            ext, lang = item.split(":", 1)
            ext_map[ext.strip()] = lang.strip()

    ignore = set(DEFAULT_IGNORE)
    ignore.update(d for d in args.ignore.split(",") if d.strip())

    stats = defaultdict(lambda: {"files": 0, "code": 0, "blank": 0, "comment": 0})
    if not os.path.isdir(args.path):
        print(f"Error: {args.path} is not a directory", file=sys.stderr)
        return 1

    for root, dirs, files in os.walk(args.path):
        dirs[:] = [d for d in dirs if d not in ignore and not d.startswith(".git")]
        for name in files:
            ext = os.path.splitext(name)[1].lower()
            if ext not in ext_map:
                continue
            language = ext_map[ext]
            result = count_file(os.path.join(root, name), language)
            if result is None:
                continue
            code, blank, comment = result
            entry = stats[language]
            entry["files"] += 1
            entry["code"] += code
            entry["blank"] += blank
            entry["comment"] += comment

    if not stats:
        print(f"No recognized code files found under {args.path}.")
        return 0

    rows = []
    for lang, s in stats.items():
        total = s["code"] + s["blank"] + s["comment"]
        rows.append((lang, s["files"], total, s["code"], s["blank"], s["comment"]))
    if args.sort == "lines":
        rows.sort(key=lambda r: r[2], reverse=True)
    elif args.sort == "files":
        rows.sort(key=lambda r: r[1], reverse=True)
    else:
        rows.sort(key=lambda r: r[0])

    print(f"{'Language':<14}{'Files':>7}{'Total':>8}{'Code':>8}"
          f"{'Blank':>8}{'Comment':>9}")
    print("-" * 54)
    totals = [0] * 5
    for lang, files, total, code, blank, comment in rows:
        print(f"{lang:<14}{files:>7}{total:>8}{code:>8}{blank:>8}{comment:>9}")
        for i, v in enumerate((files, total, code, blank, comment)):
            totals[i] += v
    print("-" * 54)
    print(f"{'TOTAL':<14}{totals[0]:>7}{totals[1]:>8}{totals[2]:>8}"
          f"{totals[3]:>8}{totals[4]:>9}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
