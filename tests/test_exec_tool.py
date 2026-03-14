import unittest
from unittest.mock import patch
from iclaw.exec_tool import exec_command


class TestExecTool(unittest.TestCase):
    def test_exec_echo(self):
        output = exec_command("echo 'hello world'")
        self.assertEqual(output.strip(), "hello world")

    def test_exec_ls(self):
        output = exec_command("ls pyproject.toml")
        self.assertIn("pyproject.toml", output)

    def test_exec_error(self):
        output = exec_command("non_existent_command_12345")
        self.assertIn("not found", output.lower())

    def test_exec_empty_output_nonzero(self):
        output = exec_command("bash -c 'exit 42'")
        self.assertIn("Process exited with code 42", output)

    @patch("iclaw.exec_tool.subprocess.run", side_effect=Exception("unexpected"))
    def test_exec_exception(self, mock_run):
        output = exec_command("anything")
        self.assertIn("Error executing command", output)

    def test_exec_timeout(self):
        import subprocess

        with patch(
            "iclaw.exec_tool.subprocess.run",
            side_effect=subprocess.TimeoutExpired("cmd", 30),
        ):
            output = exec_command("sleep 999")
        self.assertIn("timed out", output)


if __name__ == "__main__":
    unittest.main()
