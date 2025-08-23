import os
import tempfile
import unittest
from functions.write_file import write_file

class TestWriteFile(unittest.TestCase):
    def test_write_file_successful(self):
        with tempfile.TemporaryDirectory() as cwd:
            fpath = os.path.join(cwd, "temp.txt")

            # Create an initial file
            with open(fpath, "w") as f:
                f.write("Hello, World")

            # Call write_file with relative path
            result = write_file(cwd, "temp.txt", "Hello")

            # Check the function returned a success message
            self.assertIn("Successfully wrote", result)

            # Verify that the file contents were updated
            with open(fpath) as f:
                self.assertEqual(f.read(), "Hello")
    
    def test_file_outside_cwd(self):
        with tempfile.TemporaryDirectory() as cwd:
            fpath = os.path.join(cwd, "../temp.txt")
            result = write_file(cwd, fpath, "Hello, World")
            self.assertIn("Error:", result)

    def test_is_not_file(self):
        with tempfile.TemporaryDirectory() as cwd:
            folder_path = os.path.join(cwd, "temp_folder")
            os.mkdir(folder_path)
            result = write_file(cwd, folder_path, "")
            self.assertIn("Error:", result)