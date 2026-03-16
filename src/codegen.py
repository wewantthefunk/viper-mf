"""
Code generation abstraction for Cobra translator.
Centralizes Python output so all emission goes through a single writer.
"""
from typing import List, Optional

from cobol_lexicon import INDENT, NEWLINE


class CodeWriter:
    """
    Writes generated Python source to a file or an in-memory buffer.
    Handles indentation and provides a single abstraction for all code emission.
    """

    def __init__(self, output_path: str, buffer: Optional[List[str]] = None):
        """
        Args:
            output_path: Full path to the output .py file (e.g. "HELLO.py" or "converted/HELLO.py").
            buffer: If provided, append to this list instead of writing to disk (for tests).
        """
        self._output_path = output_path
        self._buffer: Optional[List[str]] = buffer
        self._indent_str = INDENT

    @property
    def output_path(self) -> str:
        return self._output_path

    def write(self, data: str) -> None:
        """Append raw string to output (file or buffer)."""
        if self._buffer is not None:
            self._buffer.append(data)
        else:
            from util import append_file
            append_file(self._output_path, data)

    def write_overwrite(self, data: str) -> None:
        """Write data from the start (overwrite file). Used for initial write."""
        if self._buffer is not None:
            self._buffer.clear()
            self._buffer.append(data)
        else:
            from util import write_file
            write_file(self._output_path, data)

    def indent(self, level: int) -> str:
        """Return padding string for the given indentation level."""
        return self._indent_str * level

    def write_line(self, text: str) -> None:
        """Append a line (no extra newline; caller adds NEWLINE if needed)."""
        self.write(text)

    def write_line_indent(self, level: int, text: str) -> None:
        """Append a line with the given indentation level."""
        self.write(self.indent(level) + text)

    def get_content(self) -> str:
        """Return full content so far. Only valid when using buffer mode."""
        if self._buffer is None:
            raise RuntimeError("get_content() only available when CodeWriter was created with a buffer")
        return "".join(self._buffer)
