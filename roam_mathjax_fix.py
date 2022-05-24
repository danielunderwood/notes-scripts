"""
Roam uses double dollar signs everywhere for math. Obsidian uses single for inline and double for
multi-line. This converts any lines with double dollar signs to single dollar signs unless they're
the only thing on the line (you were writing multi-line math in Roam)

!!! Back up your notes before running this. It should be pretty safe, but who knows !!!
"""

from pathlib import Path
import re

from util import recursive_file_generator


notes_path = Path(__file__).parents[1]
for file in recursive_file_generator(notes_path):
    output = []
    try:
        with file.open("r") as f:
            for line in f:
                if "$$" in line and line.strip() != "$$":
                    output.append(re.sub(r"\${2}", "$", line))
                else:
                    output.append(line)

        print(f"Rewriting {file}")
        file.write_text("".join(l for l in output))
    except Exception as e:
        print(file, e)
