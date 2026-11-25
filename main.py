#!/usr/bin/env python3
"""The Excuse That Almost Works — make.fun bounty entry.

Writes the single excuse line to $MAKEFUN_OUTPUT_DIR/entry.txt.
Stdlib only. No trailing newline: the gate counts 1-140 characters.
"""

import os
import sys

LINE = "bank froze my card, been on hold two hours, can't hang up or i lose my place"

# The sealed gate: 1-140 characters, at most 20 words, one line.
MAX_CHARS = 140
MAX_WORDS = 20


def check_gate(line: str) -> None:
    if not 1 <= len(line.encode("utf-8")) <= MAX_CHARS:
        raise ValueError("entry is %d bytes, gate allows 1-%d" % (len(line.encode("utf-8")), MAX_CHARS))
    if len(line.split()) > MAX_WORDS:
        raise ValueError("entry is %d words, gate allows at most %d" % (len(line.split()), MAX_WORDS))
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")


def main() -> int:
    check_gate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = LINE.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    with open(path, "rb") as f:
        back = f.read()
    if back != data:
        print("round-trip mismatch", file=sys.stderr)
        return 1
    print("wrote %d bytes to %s" % (len(data), path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
