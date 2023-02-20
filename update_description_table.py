"""
Script that generates docs table
"""

import ast
import sys
from pathlib import Path
from subprocess import run

HERE = Path(__file__).parents[0]
README = HERE / "README.md"


def get_current_files() -> list[Path]:
    output = run(["git", "ls-tree", "-r", "--name-only", "HEAD"],
                 capture_output=True)
    if output.returncode != 0:
        print(
            f"Failed to execute command:\n:{output.stderr.decode()}", file=sys.stdout)
        exit(output.returncode)
    return [HERE / filename for filename in output.stdout.decode().split() if filename.endswith(".py")]


def get_insert_start_end() -> tuple[int, int, list[str]]:
    start, end = None, None
    lines = []
    for i, line in enumerate(README.open()):
        if "<!-- BEGIN DESCRIPTION TABLE -->" in line:
            start = i
        elif "<!-- END DESCRIPTION TABLE -->" in line:
            end = i

        lines.append(line)

    if start is None or end is None:
        print("Error: could not find start and end of table", file=sys.stderr)
        exit(1)

    return start, end, lines


def get_docstring(filename: Path) -> str:
    module = ast.parse(filename.read_text())
    return " ".join((ast.get_docstring(module) or "").split("\n"))


if __name__ == "__main__":
    script_files = get_current_files()
    print(
        f"Updating description for {', '.join([str(f.relative_to(HERE)) for f in script_files])}")
    start, end, lines = get_insert_start_end()
    # Drop any current lines that are tables
    lines = lines[:start + 1] + lines[end:]
    rows = [(file.name, get_docstring(file)) for file in script_files]
    name_width = max(len('File'), max(len(name) for name, _ in rows))
    docstring_width = max(len('Description'), max(
        len(docstring) for _, docstring in rows))
    row_strings = [
        f"| {'Name':<{name_width}} | {'Description':<{docstring_width}} |",
        f"| {'-' * (name_width)} | {'-' * (docstring_width)}",

        *[f"| {name:<{name_width}} | {docstring:<{docstring_width}} |" for name, docstring in rows]
    ]
    print(f"Updating table from lines {start} to {end}")
    for i, line in enumerate(row_strings):
        lines.insert(start + 1 + i, line + "\n")
    print("\n".join(lines))
    out_str = ""
    for line in lines:
        out_str += line
    README.write_text(out_str)
