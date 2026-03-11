# F2.1 — File Stream Backend: Tasks

## Implementation Tasks

- [x] 1. Create the `source/packages/automojo/timetravel/pod/backends/` package with `__init__.py`
- [x] 2. Create the module `source/packages/automojo/timetravel/pod/backends/filebackend.py`
- [x] 3. Implement `FileStreamBackend.__init__` with path, append, max_file_size, and parent directory creation
- [x] 4. Implement `write()` with byte counting and rotation trigger
- [x] 5. Implement `_rotate()` for size-based file rotation
- [x] 6. Implement `close()` with flush and file handle cleanup
- [x] 7. Export public symbols from the backends package

## Testing Tasks

- [x] 8. Create test file `source/tests/automojo/timetravel/pod/backends/test_filebackend.py`
- [x] 9. Test: writing data creates a file at the specified path
- [x] 10. Test: data written can be read back from the file
- [x] 11. Test: with rotation enabled, exceeding max size creates rotated file
- [x] 12. Test: rotation naming follows `{base}.{index}` pattern
- [x] 13. Test: parent directories are created if they don't exist
- [x] 14. Test: `close()` makes the file handle unavailable
- [x] 15. Test: append mode appends to existing file
