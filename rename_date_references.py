"""
Finds roam references (e.g., January 1st, 2020) and replaces them with our daily note format
"""

import re
from datetime import date

from util import recursive_file_generator

months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

months = {month: i + 1 for i, month in enumerate(months)}
reference_re = re.compile(
    r"(\[\[(?P<month>"
    + "|".join(months)
    + r") (?P<day>\d{1,2})(st|nd|rd|th), (?P<year>\d{4})\]\])"
)

for file in recursive_file_generator():
    text = file.read_text()
    if matches := reference_re.findall(text):
        substitutions = {}
        for full, month, day, _, year in matches:
            month = months[month]
            day = int(day)
            year = int(year)
            ref_date = date(year, month, day)
            substitutions[full] = ref_date.strftime("[[%Y-%m-%d]]")

        for old, new in substitutions.items():
            print(file.name, old, "->", new)
            text = text.replace(old, new)

        file.write_text(text)
