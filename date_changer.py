"""
Converts from the Roam format of January 1st, 2000 to a format of 2020-01-01
"""

from datetime import datetime
from pathlib import Path
import re

from util import git_move, recursive_file_generator


notes_path = Path(__file__).parents[1]

for file in recursive_file_generator(notes_path):
    name = re.findall(r"(\w+) (\d{1,2})[a-z]{2}, (\d{4})\.md", file.name)
    if name:
        parsed = datetime.strptime(" ".join(name[0]), "%B %d %Y")
        print(f'{" ".join(name[0])} -> {parsed.strftime("%Y-%m-%d")}')
        git_move(file.name, f'{parsed.strftime("%Y-%m-%d")}.md')
