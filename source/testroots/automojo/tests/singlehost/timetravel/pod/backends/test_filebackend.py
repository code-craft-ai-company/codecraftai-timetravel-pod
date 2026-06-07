"""
    Tests for the F2.1 File Stream Backend module.
"""

import os
import tempfile

from automojo.timetravel.pod.backends.filebackend import FileStreamBackend
from automojo.timetravel.pod.backends.filebackend import DEFAULT_MAX_FILE_SIZE


def _setup_temp_dir() -> str:
    """
        Create a fresh temporary directory for a single test.

        :returns: The path to the newly created temporary directory.
    """
    temp_dir = tempfile.mkdtemp()
    return temp_dir


def _teardown_temp_dir(temp_dir: str) -> None:
    """
        Remove every file in the temporary directory and then the directory.

        :param temp_dir: The temporary directory to clean up.
    """
    # Clean up temp files
    for f in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, f))
    os.rmdir(temp_dir)
    return


def test_write_creates_file_with_data() -> None:
    """
        Verify write creates a file and stores data.
    """
    temp_dir = _setup_temp_dir()
    file_path = os.path.join(temp_dir, "trace.bin")
    try:
        backend = FileStreamBackend(file_path=file_path)
        backend.write(b"hello trace")
        backend.close()

        with open(file_path, "rb") as f:
            content = f.read()

        assert content == b"hello trace"
    finally:
        _teardown_temp_dir(temp_dir=temp_dir)

    return


def test_multiple_writes_accumulate() -> None:
    """
        Verify multiple writes accumulate in the file.
    """
    temp_dir = _setup_temp_dir()
    file_path = os.path.join(temp_dir, "trace.bin")
    try:
        backend = FileStreamBackend(file_path=file_path)
        backend.write(b"aaa")
        backend.write(b"bbb")
        backend.close()

        with open(file_path, "rb") as f:
            content = f.read()

        assert content == b"aaabbb"
    finally:
        _teardown_temp_dir(temp_dir=temp_dir)

    return


def test_append_mode_preserves_existing_data() -> None:
    """
        Verify append mode preserves existing file data.
    """
    temp_dir = _setup_temp_dir()
    file_path = os.path.join(temp_dir, "trace.bin")
    try:
        # Write initial data
        backend = FileStreamBackend(file_path=file_path)
        backend.write(b"initial")
        backend.close()

        # Reopen in append mode
        backend = FileStreamBackend(file_path=file_path, append=True)
        backend.write(b"_appended")
        backend.close()

        with open(file_path, "rb") as f:
            content = f.read()

        assert content == b"initial_appended"
    finally:
        _teardown_temp_dir(temp_dir=temp_dir)

    return


def test_overwrite_mode_replaces_existing_data() -> None:
    """
        Verify default (non-append) mode replaces existing data.
    """
    temp_dir = _setup_temp_dir()
    file_path = os.path.join(temp_dir, "trace.bin")
    try:
        backend = FileStreamBackend(file_path=file_path)
        backend.write(b"original_data_long")
        backend.close()

        backend = FileStreamBackend(file_path=file_path, append=False)
        backend.write(b"new")
        backend.close()

        with open(file_path, "rb") as f:
            content = f.read()

        assert content == b"new"
    finally:
        _teardown_temp_dir(temp_dir=temp_dir)

    return


def test_rotation_creates_new_files() -> None:
    """
        Verify file rotation creates numbered files when size limit exceeded.
    """
    temp_dir = _setup_temp_dir()
    file_path = os.path.join(temp_dir, "trace.bin")
    try:
        backend = FileStreamBackend(
            file_path=file_path, max_file_size=10
        )
        backend.write(b"x" * 15)  # 15 bytes exceeds 10 limit -> rotate
        backend.write(b"y" * 5)   # written to rotated file
        backend.close()

        rotated_path = f"{file_path}.1"
        assert os.path.exists(file_path)
        assert os.path.exists(rotated_path)

        with open(rotated_path, "rb") as f:
            rotated_content = f.read()

        assert rotated_content == b"y" * 5
    finally:
        _teardown_temp_dir(temp_dir=temp_dir)

    return


def test_creates_parent_directories() -> None:
    """
        Verify parent directories are created if they don't exist.
    """
    temp_dir = _setup_temp_dir()
    try:
        nested_path = os.path.join(temp_dir, "sub", "dir", "trace.bin")
        backend = FileStreamBackend(file_path=nested_path)
        backend.write(b"nested")
        backend.close()

        with open(nested_path, "rb") as f:
            content = f.read()

        assert content == b"nested"

        # Clean up nested dirs
        os.remove(nested_path)
        os.rmdir(os.path.join(temp_dir, "sub", "dir"))
        os.rmdir(os.path.join(temp_dir, "sub"))
    finally:
        _teardown_temp_dir(temp_dir=temp_dir)

    return


def test_close_is_idempotent() -> None:
    """
        Verify close can be called multiple times without error.
    """
    temp_dir = _setup_temp_dir()
    file_path = os.path.join(temp_dir, "trace.bin")
    try:
        backend = FileStreamBackend(file_path=file_path)
        backend.write(b"data")
        backend.close()
        backend.close()  # should not raise
    finally:
        _teardown_temp_dir(temp_dir=temp_dir)

    return


def test_default_max_file_size_constant() -> None:
    """
        Verify DEFAULT_MAX_FILE_SIZE is 100 MB.
    """
    temp_dir = _setup_temp_dir()
    try:
        assert DEFAULT_MAX_FILE_SIZE == 100 * 1024 * 1024
    finally:
        _teardown_temp_dir(temp_dir=temp_dir)

    return
