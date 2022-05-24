"""
Downloads firebase images from roam to a local directory and fixes links
"""

import re

from util import NOTES_ROOT, download_file, recursive_file_generator

# Note that there's an issue here where we replace more than needed
# This is because roam sometimes used resources embedded in ways other than `![](url)`
#  such as {{pdf: https://...pdf}}
firebase_re = re.compile(r"https://firebase[^()]+")
export_path = NOTES_ROOT / "images" / "firebase"

if not export_path.exists():
    export_path.mkdir()

for file in recursive_file_generator():
    text = file.read_text()
    if matches := firebase_re.findall(text):
        mappings = {}
        for match in matches:
            mappings[match] = str(download_file(match, export_path).relative_to(NOTES_ROOT))

        print(f"Replacing {len(mappings)} links in {file.name}")
        for old, new in mappings.items():
            text = text.replace(old, new)

        file.write_text(text)