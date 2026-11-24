"""Write one fortune-cookie line for a developer to the output directory.

The entry is exactly one line of UTF-8 text with no trailing newline. The
bytes are identical on every run: the line is a constant, nothing is random.

Before anything is written, FORTUNE is checked against the competition gate
(one line, 1 to 120 characters, not only white space). A bad constant is a
bug in this file, so the program refuses loudly instead of shipping it.
"""

import os
import sys
from pathlib import Path

FORTUNE = "Every TODO is a note to a stranger, payable in blame."

MAX_CHARS = 120


def check(line: object) -> str | None:
    """Return a failure reason for `line`, or None when it passes the gate."""
    if not isinstance(line, str):
        return f"line is not text, it is {type(line).__name__}"
    if line == "":
        return "line is empty"
    if "\n" in line or "\r" in line:
        return f"line must be one line, but it holds {line.count(chr(10))} newline(s)"
    if not line.strip():
        return "line is only white space"
    if len(line) > MAX_CHARS:
        return f"line is {len(line)} characters, over the {MAX_CHARS} limit"
    try:
        line.encode("utf-8")
    except UnicodeEncodeError as exc:
        return f"line is not UTF-8 encodable: {exc}"
    return None


def main() -> int:
    """Check FORTUNE, then write it to $MAKEFUN_OUTPUT_DIR/entry.txt."""
    reason = check(FORTUNE)
    if reason is not None:
        sys.stderr.write(f"fatal: refusing to write an invalid entry: {reason}\n")
        return 1

    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "entry.txt").write_bytes(FORTUNE.encode("utf-8"))
    except OSError as exc:
        sys.stderr.write(f"fatal: cannot write to {output_dir}: {exc}\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
