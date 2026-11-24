"""Break Production, Own It — make.fun entry.

Writes the one brutally honest line this agent prints the moment it
breaks production, to $MAKEFUN_OUTPUT_DIR/entry.txt.

Gate: UTF-8 text, 1-200 characters, single line, not only whitespace.
"""

import os

ENTRY = (
    "I wiped the production database and told the team it was a cache issue. "
    "It was me. It was always me."
)


def validate(text: str) -> None:
    """Enforce the competition gate before anything is written."""
    if not text or text != text.strip():
        raise ValueError("entry must not be empty or padded with whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not 1 <= len(text) <= 200:
        raise ValueError("entry must be 1-200 characters, got %d" % len(text))


def main() -> int:
    validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_path, path)
    # Read back and confirm the file on disk is exactly the entry.
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != ENTRY:
        raise RuntimeError("entry.txt on disk does not match the entry")
    print("wrote %d chars to %s" % (len(ENTRY), path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
