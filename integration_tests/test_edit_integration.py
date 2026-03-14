import os
import unittest
from mini_copilot.main import MiniCopilot
from tools.patch_tool import PatchTool


class TestEditToolIntegration(unittest.TestCase):
    def setUp(self):
        self.copilot = MiniCopilot()
        self.test_file = "integration_test_file.py"
        with open(self.test_file, "w") as f:
            f.write("def hello():\n    print('hello world')\n")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_apply_patch_integration(self):
        # We simulate what the agent would do: generate a patch and call PatchTool
        patch = f"""--- {self.test_file}
+++ {self.test_file}
@@ -1,2 +1,2 @@
 def hello():
-    print('hello world')
+    print('hello integration')
"""
        new_content = PatchTool.apply_patch(self.test_file, patch)

        with open(self.test_file, "w") as f:
            f.write(new_content)

        with open(self.test_file, "r") as f:
            updated_content = f.read()

        self.assertIn("print('hello integration')", updated_content)
        self.assertNotIn("print('hello world')", updated_content)


if __name__ == "__main__":
    unittest.main()
