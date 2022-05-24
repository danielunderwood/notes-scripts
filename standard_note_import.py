import argparse
import json
import re
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("dir", help="Directory for standard note export")
parser.add_argument("output_dir", help="Note export path")

args = parser.parse_args()

sn_path = Path(args.dir)
output_path = Path(args.output_dir)
tag_path = sn_path / "Tag"
note_path = sn_path / "Note"
tags = []
notes = {}
note_uuid = re.compile(r".*?-([a-z0-9]{8})\.txt$")
for path in tag_path.iterdir():
    with path.open("r") as f:
        tag = json.load(f)
        tags.append(tag)
        # print(tags)

if not output_path.exists():
    output_path.mkdir(parents=True)

for note in note_path.iterdir():
    match = note_uuid.findall(note.name)[0]
    note_tags = [
        t["title"]
        for t in tags
        if any(r["uuid"].startswith(match) for r in t["references"])
    ]
    print(note.name, note_tags)

    new_name = note.name.split("-")[0] + ".md"
    new_path = output_path / new_name
    if new_path.exists():
        raise FileExistsError("Path already exists!")

    with new_path.open("w") as out_file:
        if note_tags:
            out_file.writelines(
                [
                    "---\n",
                    "tag:\n",
                    *[f'  - {"-".join(tag.split())}\n' for tag in note_tags],
                    "---\n\n",
                ]
            )

        out_file.writelines(note.read_text())