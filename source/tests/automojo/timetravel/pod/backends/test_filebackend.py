"""
    Tests for the F2.1 File Stream Backend module.
"""

import os
import tempfile
import unittest

from ccai.timetravel.pod.backends.filebackend import FileStreamBackend
from ccai.timetravel.pod.backends.filebackend import DEFAULT_MAX_FILE_SIZE


class TestFileStreamBackend(unittest.TestCase):
    """
        Tests for the FileStreamBackend class.
    """

    def setUp(self):
        self._temp_dir = tempfile.mkdtemp()
        self._file_path = os.path.join(self._temp_dir, "trace.bin")
        return

    def tearDown(self):
        # Clean up temp files
        for f in os.listdir(self._temp_dir):
            os.remove(os.path.join(self._temp_dir, f))
        os.rmdir(self._temp_dir)
        return

    def test_write_creates_file_with_data(self):
        """
            Verify write creates a file and stores data.
        """
        backend = FileStreamBackend(file_path=self._file_path)
        backend.write(b"hello trace")
        backend.close()

        with open(self._file_path, "rb") as f:
            content = f.read()

        self.assertEqual(content, b"hello trace")

        return

    def test_multiple_writes_accumulate(self):
        """
            Verify multiple writes accumulate in the file.
        """
        backend = FileStreamBackend(file_path=self._file_path)
        backend.write(b"aaa")
        backend.write(b"bbb")
        backend.close()

        with open(self._file_path, "rb") as f:
            content = f.read()

        self.assertEqual(content, b"aaabbb")

        return

    def test_append_mode_preserves_existing_data(self):
        """
            Verify append mode preserves existing file data.
        """
        # Write initial data
        backend = FileStreamBackend(file_path=self._file_path)
        backend.write(b"initial")
        backend.close()

        # Reopen in append mode
        backend = FileStreamBackend(file_path=self._file_path, append=True)
        backend.write(b"_appended")
        backend.close()

        with open(self._file_path, "rb") as f:
            content = f.read()

        self.assertEqual(content, b"initial_appended")

        return

    def test_overwrite_mode_replaces_existing_data(self):
        """
            Verify default (non-append) mode replaces existing data.
        """
        backend = FileStreamBackend(file_path=self._file_path)
        backend.write(b"original_data_long")
        backend.close()

        backend = FileStreamBackend(file_path=self._file_path, append=False)
        backend.write(b"new")
        backend.close()

        with open(self._file_path, "rb") as f:
            content = f.read()

        self.assertEqual(content, b"new")

        return

    def test_rotation_creates_new_files(self):
        """
            Verify file rotation creates numbered files when size limit exceeded.
        """
        backend = FileStreamBackend(
            file_path=self._file_path, max_file_size=10
        )
        backend.write(b"x" * 15)  # 15 bytes exceeds 10 limit -> rotate
        backend.write(b"y" * 5)   # written to rotated file
        backend.close()

        rotated_path = f"{self._file_path}.1"
        self.assertTrue(os.path.exists(self._file_path))
        self.assertTrue(os.path.exists(rotated_path))

        with open(rotated_path, "rb") as f:
            rotated_content = f.read()

        self.assertEqual(rotated_content, b"y" * 5)

        return

    def test_creates_parent_directories(self):
        """
            Verify parent directories are created if they don't exist.
        """
        nested_path = os.path.join(self._temp_dir, "sub", "dir", "trace.bin")
        backend = FileStreamBackend(file_path=nested_path)
        backend.write(b"nested")
        backend.close()

        with open(nested_path, "rb") as f:
            content = f.read()

        self.assertEqual(content, b"nested")

        # Clean up nested dirs
        os.remove(nested_path)
        os.rmdir(os.path.join(self._temp_dir, "sub", "dir"))
        os.rmdir(os.path.join(self._temp_dir, "sub"))

        return

    def test_close_is_idempotent(self):
        """
            Verify close can be called multiple times without error.
        """
        backend = FileStreamBackend(file_path=self._file_path)
        backend.write(b"data")
        backend.close()
        backend.close()  # should not raise

        return

    def test_default_max_file_size_constant(self):
        """
            Verify DEFAULT_MAX_FILE_SIZE is 100 MB.
        """
        self.assertEqual(DEFAULT_MAX_FILE_SIZE, 100 * 1024 * 1024)

        return


if __name__ == "__main__":
    unittest.main()
