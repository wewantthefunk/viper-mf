"""
Regression tests for the Cobra COBOL-to-Python translator.

Run from project root:
  pytest tests/ -v
  or (without pytest):  python tests/test_cobra_regression.py

These tests ensure the pipeline runs and produces valid Python for known programs,
guarding against regressions when refactoring the translator.
"""
import os
import sys
import subprocess
import tempfile
import unittest
from pathlib import Path

# Project root and src on path (run from project root)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


class TestCobraRegression(unittest.TestCase):
    """Regression tests for Cobra translator pipeline and generated Python."""

    def setUp(self):
        self._orig_cwd = os.getcwd()
        os.chdir(PROJECT_ROOT)

    def tearDown(self):
        os.chdir(self._orig_cwd)

    def test_translator_produces_python_for_hellowo1(self):
        """Running the translator on hellowo1_basic.cbl produces a .py file with expected structure."""
        from parse_cobol_file import parse_cobol_file

        cobol_file = "examples/hellowo1_basic.cbl"
        self.assertTrue((PROJECT_ROOT / cobol_file).exists(), f"Fixture {cobol_file} missing")

        with tempfile.TemporaryDirectory() as out_dir:
            out_dir = out_dir + os.sep
            dep_dir = ""
            parse_cobol_file(cobol_file, out_dir, dep_dir)

            out_py = Path(out_dir) / "HELLOWO1.py"
            self.assertTrue(out_py.exists(), "Translator should produce HELLOWO1.py")

            content = out_py.read_text()
            self.assertIn("class HELLOWO1Class:", content)
            self.assertIn("def __init__(self):", content)
            self.assertTrue(
                "def main(self,caller" in content or "def main(self, caller" in content,
                "Expected def main(self, caller...)",
            )
            self.assertIn("if __name__ == '__main__':", content)
            self.assertTrue(
                "hello world" in content or "Display_Variable" in content,
                "Expected program to display hello world",
            )

    def test_translator_produces_valid_python_for_hellowo2(self):
        """Running the translator on hellowo2_variable.cbl produces valid Python with data division and MOVE/DISPLAY."""
        from parse_cobol_file import parse_cobol_file

        cobol_file = "examples/hellowo2_variable.cbl"
        self.assertTrue((PROJECT_ROOT / cobol_file).exists(), f"Fixture {cobol_file} missing")

        with tempfile.TemporaryDirectory() as out_dir:
            out_dir = out_dir + os.sep
            dep_dir = ""
            parse_cobol_file(cobol_file, out_dir, dep_dir)

            out_py = Path(out_dir) / "HELLOWO2.py"
            self.assertTrue(out_py.exists())
            content = out_py.read_text()
            self.assertIn("class HELLOWO2Class:", content)
            self.assertTrue(
                "def main(self,caller" in content or "def main(self, caller" in content,
            )
            self.assertTrue(
                "HELLO-WORLD" in content or "HELLO_WORLD" in content or "hello_world" in content.lower(),
                "Expected variable reference in output",
            )

    def test_generated_hellowo1_runs_and_produces_expected_output(self):
        """Generated HELLOWO1.py runs successfully and prints the expected literal."""
        from parse_cobol_file import parse_cobol_file

        cobol_file = "examples/hellowo1_basic.cbl"
        with tempfile.TemporaryDirectory() as out_dir:
            out_dir_path = Path(out_dir)
            out_dir_str = out_dir + os.sep
            parse_cobol_file(cobol_file, out_dir_str, "")

            out_py = out_dir_path / "HELLOWO1.py"
            cobol_variable = out_dir_path / "cobol_variable.py"
            self.assertTrue(out_py.exists())
            self.assertTrue(cobol_variable.exists(), "cobol_variable.py should be copied to output dir")

            result = subprocess.run(
                [sys.executable, str(out_py)],
                cwd=str(out_dir_path),
                capture_output=True,
                text=True,
                timeout=10,
            )
            self.assertEqual(result.returncode, 0, f"Generated script failed: {result.stderr or result.stdout}")
            self.assertIn("hello world", (result.stdout + result.stderr).lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
