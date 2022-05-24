"""
Converts daily note of the format YYYY/MM - MMMM/DD.md to YYYY/MM - MMMM/YYYY-MM-DD.md
"""
from os import path
import re
from datetime import date

from util import NOTES_ROOT, recursive_file_generator, git_move

path_re = re.compile(r".*?(?P<year>\d{4})/(?P<month>\d{2}) - \w+/(?P<day>\d{2}).md")


for file in recursive_file_generator():
    if match := path_re.match(file.as_posix()):
        groups = {k: int(v) for k, v in match.groupdict().items()}
        note_day = date(groups['year'], groups['month'], groups['day'])
        new_path = file.parent / note_day.strftime("%Y-%m-%d.md")
        print(file, '->', new_path)
        git_move(file, new_path)