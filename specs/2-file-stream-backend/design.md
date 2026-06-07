# F2.1 — File Stream Backend: Design

## Technical Design

### Module Location
`source/packages/ccai/timetravel/pod/backends/filebackend.py`

### Class Design

```python
import os

DEFAULT_MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB


class FileStreamBackend:
    """Stream backend that writes trace data to files on disk."""

    def __init__(self, file_path: str, append: bool = False,
                 max_file_size: int | None = None):
        self._base_path = file_path
        self._append = append
        self._max_file_size = max_file_size
        self._rotation_index = 0
        self._bytes_written = 0
        self._file = None

        self._ensure_parent_directory(file_path)
        self._open_file(file_path)

    def _ensure_parent_directory(self, file_path: str) -> None:
        parent_dir = os.path.dirname(file_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)

    def _open_file(self, file_path: str) -> None:
        mode = "ab" if self._append else "wb"
        self._file = open(file_path, mode)
        self._bytes_written = 0

    def _rotate(self) -> None:
        self._file.close()
        self._rotation_index += 1
        rotated_path = f"{self._base_path}.{self._rotation_index}"
        self._ensure_parent_directory(rotated_path)
        self._open_file(rotated_path)

    def write(self, data: bytes) -> None:
        self._file.write(data)
        self._bytes_written += len(data)
        if self._max_file_size is not None and self._bytes_written >= self._max_file_size:
            self._rotate()

    def close(self) -> None:
        if self._file is not None:
            self._file.flush()
            self._file.close()
            self._file = None
```

### Package Structure

Stream backends are placed in a `backends` sub-package:
```
source/packages/ccai/timetravel/pod/backends/
    __init__.py
    file_backend.py
    tcp_backend.py
    unix_backend.py
    registry.py
```

### Design Rationale

- Binary mode (`wb` / `ab`) is used because trace data is pre-serialized bytes.
- Rotation checks happen after each `write()` call from the `BufferedTraceWriter`,
  which means rotation granularity is at the buffer-flush level (64 KB default),
  not per-event.
- `os.makedirs(exist_ok=True)` handles the parent directory creation idempotently.
