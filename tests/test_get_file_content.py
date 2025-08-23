import unittest
from functions.get_file_content import get_file_content
import tempfile, os
from config import MAX_CHARS

class TestGetFileContent(unittest.TestCase):
    def test_get_file_content_succeed(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fpath = os.path.join(tmpdir, "temp.txt")
            with open(fpath, "w") as f:
                f.write("Hello, World")

            result = get_file_content(tmpdir, "temp.txt")
            self.assertEqual("Hello, World", result)

    def test_file_not_found(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            result = get_file_content(tmpdir, "nonexistentfile.txt")
            self.assertIn("Error:", result)
    
    def test_exceeded_length(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fpath = os.path.join(tmpdir, "big.txt")
    
            long_text = "A" * 15000
            with open(fpath, "w") as f:
                f.write(long_text)

            result = get_file_content(tmpdir, "big.txt")

            self.assertTrue(result.startswith("A" * MAX_CHARS))
            self.assertIn("truncated at 10000 characters", result)