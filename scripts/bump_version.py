#!/usr/bin/env python3
"""Bump the application version. Usage: python scripts/bump_version.py [major|minor|patch]"""
import sys
import re
from pathlib import Path

VERSION_FILE = Path(__file__).parent.parent / "app" / "version.py"

def read_version():
    content = VERSION_FILE.read_text()
    match = re.search(r'__version__ = "(\d+)\.(\d+)\.(\d+)"', content)
    if not match:
        raise ValueError("Could not parse version from app/version.py")
    return tuple(int(x) for x in match.groups())

def write_version(major, minor, patch):
    VERSION_FILE.write_text(f'__version__ = "{major}.{minor}.{patch}"\n')

def main():
    part = sys.argv[1] if len(sys.argv) > 1 else "patch"
    major, minor, patch = read_version()
    old = f"{major}.{minor}.{patch}"

    if part == "major":
        major, minor, patch = major + 1, 0, 0
    elif part == "minor":
        major, minor, patch = major, minor + 1, 0
    else:
        major, minor, patch = major, minor, patch + 1

    new = f"{major}.{minor}.{patch}"
    write_version(major, minor, patch)
    print(f"Version bumped: {old} → {new}")

if __name__ == "__main__":
    main()
