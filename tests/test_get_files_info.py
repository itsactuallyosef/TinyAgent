
import unittest
import tempfile
import os
from functions.get_files_info import get_files_info

class TestGetFilesInfo(unittest.TestCase):
    def test_lists_files_in_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # create some test cases
            fpath = os.path.join(tmpdir, "temp.txt")
            with open(fpath, "w") as f:
                f.write("hello")

            result = get_files_info(tmpdir)
            self.assertIn("temp.txt", result)

    def test_non_existent_directory(self):
        result = get_files_info("/nonexistent/path")
        self.assertIn("Error:", result)

    def test_directory_outside_working_directory(self):
        with tempfile.TemporaryDirectory() as tempdir:
            result = get_files_info(tempdir, "../")
            self.assertIn("Error", result)

    def test_nested_directory(self):
        with tempfile.TemporaryDirectory() as tempdir:
            with tempfile.TemporaryDirectory(dir=tempdir) as nested_dir:
                fpath = os.path.join(nested_dir, "test.py")
                with open(fpath, "w") as f:
                    f.write("print('Hello, World')")

                result = get_files_info(tempdir, nested_dir)
                self.assertIn("test.py", result)


if __name__ == "__main__":
    unittest.main()