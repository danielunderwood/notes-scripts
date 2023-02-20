"""
Common utilities to use in scripts, such as enumerating all notes
"""

import re
import subprocess
from pathlib import Path

import requests

NOTES_ROOT = Path(__file__).parents[1]

def git_move(source, dest):
    return subprocess.run(["git", "mv", source, dest], capture_output=True)


def git_rm(file):
    return subprocess.run(["git", "rm", file], capture_output=True)

def download_file(url, output):
    if not isinstance(output, Path):
        output = Path(output)

    filename_re = re.compile(r".*?(?P<filename>[\w-]+\.(png|gif|jpe?g|mp4|pdf))\?.*")
    if not filename_re.match(url):
        print(f"Could not match {url}")

    filename = filename_re.match(url).groupdict()["filename"]
    output_file = output / filename

    if output_file.exists():
        print(f"{output_file} for {url} already exists!")
        return output_file

    print(f"Downloading {url} to {output_file}")
    with open(output_file, "wb") as f:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            for chunk in r.iter_content():
                f.write(chunk)

    return output_file



def recursive_file_generator(p: Path = NOTES_ROOT, types=[".md"]):
    for file in p.iterdir():
        if file.is_file() and any(file.name.endswith(file_type) for file_type in types):
            yield file
        elif file.is_file():
            pass
        elif file.is_dir() and ".git" in file.parts:
            pass
        elif file.is_dir():
            for sub_file in recursive_file_generator(file):
                yield sub_file
        else:
            raise ValueError(f"Unexpected path type for {p}")
