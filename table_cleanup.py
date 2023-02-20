"""
Cleans up tables in markdown files to have proper spacing
"""

import re
from collections import defaultdict
from pathlib import Path

from util import recursive_file_generator

table_re = re.compile(r"^(\|.*?)+$")

notes_path = Path(__file__).parents[1]
for file in recursive_file_generator(notes_path):
    name = False
    if file.is_file():
        table = []
        for line in file.open("r"):
            if table_re.match(line):
                if not name:
                    print(file)
                    name = True
                table.append(line.strip())
            elif table:
                print(table)
                parts = [x.split("|") for x in table]
                maxes = defaultdict(int)
                for p in parts:
                    for i, x in enumerate(p):
                        maxes[i] = max(maxes[i], len(x))
                for p in parts:
                    if set(p[1]) == {'-'}:
                        spaced = ['-' * maxes[i] for i, _ in enumerate(p)]
                    else:
                        spaced = [f'{x.strip():<{maxes[i]}s}' for i, x in enumerate(p)]
                    print(' | '.join(spaced).strip())
                table = []
