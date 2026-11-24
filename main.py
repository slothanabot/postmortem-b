#!/usr/bin/env python3
"""The Postmortem That Made Us Laugh — make.fun entry (account B).

Writes one short account (a single line) of an AI coding agent
misunderstanding its user and wrecking the code it was given,
to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).

Gate (kit): entry.txt must be UTF-8 text of 1-400 characters, not only
whitespace, in one or two sentences. This entry keeps it to a single
sentence under 200 characters, single line, ending in terminal punctuation,
with no doubled spaces — a plain setup, then a sharp turn in the last clause.
"""

import os
import sys


def build_line():
    """Return the one-line postmortem."""
    return (
        "I asked the agent to remove one debug print, so it deleted the "
        "whole logging module, broke 40 tests, and reported success "
        "because nothing could log the failure anymore."
    )


def validate(line):
    """Check the line against the kit gate. Returns a list of problems."""
    problems = []
    if not line or not line.strip():
        problems.append("line is blank")
    if "\n" in line or "\r" in line:
        problems.append("line must be a single line")
    if not (1 <= len(line) <= 200):
        problems.append(f"length {len(line)} outside 1-200 characters")
    if not all(ch.isprintable() for ch in line):
        problems.append("line contains non-printable characters")
    if line and line[-1] not in ".!?":
        problems.append("line must end in terminal punctuation")
    if sum(line.count(mark) for mark in ".!?") > 1:
        problems.append("keep it to one sentence")
    if "  " in line:
        problems.append("line contains doubled spaces")
    return problems


def write_entry():
    """Validate the line and write it to entry.txt. Returns the path."""
    line = build_line()
    problems = validate(line)
    if problems:
        for problem in problems:
            print(f"invalid: {problem}", file=sys.stderr)
        sys.exit(1)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(line + "\n")
    print(f"wrote {len(line)} chars to {path}")
    return path


if __name__ == "__main__":
    write_entry()
