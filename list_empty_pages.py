"""
Lists and optionally removes any empty notes (or other files)
"""

from argparse import ArgumentParser
import argparse
from pathlib import Path

from util import git_rm, recursive_file_generator

parser = argparse.ArgumentParser()
parser.add_argument("--rm", action="store_true", help="Remove empty files")

args = parser.parse_args()
empty = []
notes_path = Path(__file__).parents[1]
for file in recursive_file_generator(notes_path):
    if file.is_file() and not file.read_text().strip():
        empty.append(file)

for e in empty:
    if args.rm:
        print(f"Removing {e.relative_to(notes_path)}")
        git_rm(e.relative_to(notes_path))
    else:
        print(e.relative_to(notes_path))
