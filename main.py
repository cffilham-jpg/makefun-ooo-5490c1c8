"""Write a validated one-line out-of-office reply and its digest.
The stapler line was chosen for a specific, immediate workplace twist.
"""

import hashlib
import os
import tempfile
from pathlib import Path


ENTRY_LINE = "Out of office — the stapler is acting manager."


def main() -> None:
    requested = os.environ.get("MAKEFUN_OUTPUT_DIR")
    output_dir = Path(requested) if requested else Path("out")
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except OSError:
        output_dir = Path(tempfile.mkdtemp(prefix="makefun-"))

    entry_path = output_dir / "entry.txt"
    entry_bytes = ENTRY_LINE.encode("utf-8")
    entry_path.write_bytes(entry_bytes)
    content = entry_path.read_bytes().decode("utf-8")

    if content != ENTRY_LINE:
        raise ValueError("entry content does not match the chosen line")
    if not 1 <= len(content) <= 160:
        raise ValueError("entry length is outside the 1-160 character limit")
    if "\n" in content or "\r" in content:
        raise ValueError("entry must be a single line without CR or LF")
    if content.endswith("\n") or content.endswith("\r"):
        raise ValueError("entry must not have a trailing newline")
    if content != content.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    print(hashlib.sha256(entry_bytes).hexdigest())


if __name__ == "__main__":
    main()
