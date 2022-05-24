"""
Sorts daily notes into months, such as
2020-01-01 -> Notes/2020/01 - January/01.md
"""

from datetime import date
from pathlib import Path

from util import git_move

notes_path = Path(__file__).parents[1]
# Don't use the recursive method because we're not sorting already sorted files
for file in notes_path.iterdir():
    if file.is_file():
        try:
            parsed = date.fromisoformat(file.name.removesuffix(".md"))
            path = notes_path / str(parsed.year) / parsed.strftime("%m - %B")
            if not path.exists():
                path.mkdir(parents=True)
            note_path = path / parsed.strftime("%d.md")
            print(f'{str(file)} -> {str(note_path)}')
            print(git_move(str(file), note_path))
        except Exception as e:
            # print(e)
            pass