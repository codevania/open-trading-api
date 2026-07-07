"""Small file I/O helpers shared by Quant generators."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def write_text_lf(path: Path, text: str, *, encoding: str = "utf-8") -> None:
    """Write text with stable LF newlines on Windows and Unix."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding=encoding, newline="\n") as handle:
        handle.write(text)


def write_json_lf(
    path: Path,
    payload: Any,
    *,
    encoding: str = "utf-8",
    indent: int = 2,
    sort_keys: bool = False,
) -> None:
    write_text_lf(
        path,
        json.dumps(payload, ensure_ascii=False, indent=indent, sort_keys=sort_keys) + "\n",
        encoding=encoding,
    )
