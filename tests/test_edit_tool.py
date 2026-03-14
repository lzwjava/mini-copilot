import unittest
import os
from iclaw.tools.edit_tool import EditTool


class TestEditTool(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_file.txt"
        with open(self.test_file, "w") as f:
            f.write("Line 1\nLine 2\nLine 3\nLine 4\nLine 5\n")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_basic_replace(self):
        edit = """--- test_file.txt
+++ test_file.txt
@@ -2,1 +2,1 @@
-Line 2
+Line Two Modified
"""
        new_content = EditTool.edit(self.test_file, edit)
        self.assertIn("Line Two Modified\n", new_content)
        self.assertNotIn("Line 2\n", new_content)
        self.assertEqual(new_content.splitlines()[1], "Line Two Modified")

    def test_multi_line_hunk(self):
        edit = """--- test_file.txt
+++ test_file.txt
@@ -3,2 +3,3 @@
-Line 3
-Line 4
+Line Three
+Line Three.Five
+Line Four
"""
        new_content = EditTool.edit(self.test_file, edit)
        lines = new_content.splitlines()
        self.assertEqual(lines[2], "Line Three")
        self.assertEqual(lines[3], "Line Three.Five")
        self.assertEqual(lines[4], "Line Four")
        self.assertEqual(len(lines), 6)

    def test_multiple_hunks(self):
        edit = """--- test_file.txt
+++ test_file.txt
@@ -1,1 +1,1 @@
-Line 1
+First Line
@@ -5,1 +5,1 @@
-Line 5
+Last Line
"""
        new_content = EditTool.edit(self.test_file, edit)
        lines = new_content.splitlines()
        self.assertEqual(lines[0], "First Line")
        self.assertEqual(lines[-1], "Last Line")

    def test_new_file(self):
        new_file = "test_new_file.txt"
        try:
            edit = """--- /dev/null
+++ test_new_file.txt
@@ -1,0 +1,2 @@
+New line 1
+New line 2
"""
            new_content = EditTool.edit(new_file, edit)
            self.assertIn("New line 1", new_content)
            self.assertIn("New line 2", new_content)
        finally:
            if os.path.exists(new_file):
                os.remove(new_file)

    def test_context_lines(self):
        edit = """--- test_file.txt
+++ test_file.txt
@@ -1,3 +1,3 @@
 Line 1
-Line 2
+Line TWO
 Line 3
"""
        new_content = EditTool.edit(self.test_file, edit)
        lines = new_content.splitlines()
        self.assertEqual(lines[0], "Line 1")
        self.assertEqual(lines[1], "Line TWO")
        self.assertEqual(lines[2], "Line 3")

    def test_delete_lines(self):
        edit = """--- test_file.txt
+++ test_file.txt
@@ -2,2 +2,0 @@
-Line 2
-Line 3
"""
        new_content = EditTool.edit(self.test_file, edit)
        lines = new_content.splitlines()
        self.assertEqual(len(lines), 3)
        self.assertEqual(lines[0], "Line 1")
        self.assertEqual(lines[1], "Line 4")

    def test_add_lines(self):
        edit = """--- test_file.txt
+++ test_file.txt
@@ -2,0 +2,2 @@
+Inserted A
+Inserted B
"""
        new_content = EditTool.edit(self.test_file, edit)
        self.assertIn("Inserted A", new_content)
        self.assertIn("Inserted B", new_content)


if __name__ == "__main__":
    unittest.main()
