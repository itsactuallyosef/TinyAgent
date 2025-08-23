import os
import tempfile
import unittest
from functions.run_python import run_python_file
from functions.write_file import write_file

class TestRunPythonFile(unittest.TestCase):
    def test_run_python_file_stdout(self):
        with tempfile.TemporaryDirectory() as cwd:
            py_file = os.path.join(cwd, "temp.py")
            write_file(cwd, py_file, "print('Hello, World')")

            result = run_python_file(cwd, py_file)
            self.assertIn("STDOUT", result)
            self.assertNotIn("STDERR", result)
            self.assertIn("Hello, World", result)

    def test_run_python_file_stderr(self):
        with tempfile.TemporaryDirectory() as cwd:
            py_file = os.path.join(cwd, "temp.py")
            write_file(cwd, py_file, "non_existent_function('Hello, World')")

            result = run_python_file(cwd, py_file)
            self.assertIn("STDERR", result)
            self.assertNotIn("STDOUT", result)
            self.assertIn("Process exited with code 1", result)
            self.assertIn("NameError", result)

    def test_file_out_of_my_bound(self):
        with tempfile.TemporaryDirectory() as cwd:
            py_file = os.path.join(cwd, "../temp.py")

            with open(py_file, "w") as f:
                f.write("print('Hello, World')")
            
            result = run_python_file(cwd, py_file)
            self.assertIn("Error:", result)
            self.assertIn("outside the permitted working directory", result)

    def test_file_does_not_end_with_py(self):
        with tempfile.TemporaryDirectory() as cwd:
            non_py_file = os.path.join(cwd, "temp.txt")
            write_file(cwd, non_py_file, "print('Hello, World')")

            result = run_python_file(cwd, non_py_file)
            self.assertIn("Error", result)
            self.assertIn("is not a Python file", result)