import tempfile
import unittest
from pathlib import Path

from click.testing import CliRunner

from filerename.cli import main


class CliTests(unittest.TestCase):
    def test_dry_run_prints_one_rename_per_line_without_renaming(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "file one.txt"
            source.write_text("x", encoding="utf-8")

            runner = CliRunner()
            result = runner.invoke(main, [str(root), "--dry-run"])

            self.assertEqual(result.exit_code, 0)
            self.assertNotIn("Dry run:", result.output)
            output_lines = [line for line in result.output.strip().splitlines() if line]
            self.assertEqual(len(output_lines), 1)
            self.assertIn("file one.txt", output_lines[0])
            self.assertIn("file_one.txt", output_lines[0])
            self.assertTrue(source.exists())
            self.assertFalse((root / "file_one.txt").exists())


if __name__ == "__main__":
    unittest.main()
