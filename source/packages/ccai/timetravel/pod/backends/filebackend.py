"""
    Provides the file stream backend for writing trace data to disk.

    This module contains the :class:`FileStreamBackend` class which writes
    serialized trace data to files with optional file rotation.
"""

import os

from typing import Optional


DEFAULT_MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB


class FileStreamBackend:
    """
        Stream backend that writes trace data to files on disk.

        Supports optional file rotation when a maximum file size is configured.
    """

    def __init__(self, file_path: str, append: bool = False,
                 max_file_size: Optional[int] = None) -> None:
        """
            Create a FileStreamBackend.

            :param file_path: The path to the trace file.
            :param append: If True, append to existing file; otherwise overwrite.
            :param max_file_size: Maximum bytes per file before rotation. None disables rotation.
        """
        self._base_path = file_path
        self._append = append
        self._max_file_size = max_file_size
        self._rotation_index = 0
        self._bytes_written = 0
        self._file = None

        self._ensure_parent_directory(file_path)
        self._open_file(file_path)
        return

    def _ensure_parent_directory(self, file_path: str) -> None:
        """
            Create the parent directory if it does not exist.

            :param file_path: The file path whose parent directory to create.
        """
        parent_dir = os.path.dirname(file_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
        return

    def _open_file(self, file_path: str) -> None:
        """
            Open the file for writing.

            :param file_path: The file path to open.
        """
        if self._append:
            mode = "ab"
        else:
            mode = "wb"
        self._file = open(file_path, mode)
        self._bytes_written = 0
        return

    def _rotate(self) -> None:
        """
            Close the current file and open a new rotated file.
        """
        self._file.close()
        self._rotation_index += 1
        rotated_path = f"{self._base_path}.{self._rotation_index}"
        self._ensure_parent_directory(rotated_path)
        self._open_file(rotated_path)
        return

    def write(self, data: bytes) -> None:
        """
            Write data to the file, rotating if the size limit is exceeded.

            :param data: The bytes to write.
        """
        self._file.write(data)
        self._bytes_written += len(data)
        if self._max_file_size is not None and self._bytes_written >= self._max_file_size:
            self._rotate()
        return

    def close(self) -> None:
        """
            Flush and close the file.
        """
        if self._file is not None:
            self._file.flush()
            self._file.close()
            self._file = None
        return
