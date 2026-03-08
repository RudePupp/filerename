import os
import tempfile
import unittest
from pathlib import Path

from filerename.renamer import rename_files


class RenameFilesTests(unittest.TestCase):
    def test_renames_files_with_spaces_recursively(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            nested = root / "nested folder"
            nested.mkdir()

            file_a = root / "my file.txt"
            file_b = nested / "another file.csv"
            file_a.write_text("a", encoding="utf-8")
            file_b.write_text("b", encoding="utf-8")

            renamed = rename_files(root)

            self.assertEqual(len(renamed), 2)
            self.assertTrue((root / "my_file.txt").exists())
            self.assertTrue((nested / "another_file.csv").exists())

    def test_no_recursive_only_changes_top_level(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            nested = root / "nested"
            nested.mkdir()

            top_file = root / "top file.txt"
            nested_file = nested / "nested file.txt"
            top_file.write_text("a", encoding="utf-8")
            nested_file.write_text("b", encoding="utf-8")

            renamed = rename_files(root, recursive=False)

            self.assertEqual(len(renamed), 1)
            self.assertTrue((root / "top_file.txt").exists())
            self.assertTrue((nested / "nested file.txt").exists())

    def test_dry_run_only_reports_changes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            original = root / "report one.txt"
            original.write_text("a", encoding="utf-8")

            planned = rename_files(root, dry_run=True)

            self.assertEqual(len(planned), 1)
            self.assertEqual(planned[0][0], original)
            self.assertEqual(planned[0][1], root / "report_one.txt")
            self.assertTrue(original.exists())
            self.assertFalse((root / "report_one.txt").exists())

    def test_raises_when_destination_exists(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "my file.txt").write_text("a", encoding="utf-8")
            (root / "my_file.txt").write_text("b", encoding="utf-8")

            with self.assertRaises(FileExistsError):
                rename_files(root)

    @unittest.skipUnless(os.name == "nt", "Windows-only case-insensitive behavior")
    def test_windows_case_insensitive_collision(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "My file.txt").write_text("a", encoding="utf-8")
            (root / "my_file.txt").write_text("b", encoding="utf-8")

            with self.assertRaises(FileExistsError):
                rename_files(root)


if __name__ == "__main__":
    unittest.main()
