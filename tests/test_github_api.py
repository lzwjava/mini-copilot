import unittest
from unittest.mock import MagicMock, patch

from iclaw import github_api


class TestGithubApi(unittest.TestCase):
    @patch("iclaw.github_api.requests.get")
    def test_get_copilot_token_success(self, mock_get):
        mock_get.return_value = MagicMock(ok=True, json=lambda: {"token": "t"})
        self.assertEqual(github_api.get_copilot_token("gt"), "t")

    @patch("iclaw.github_api.requests.get")
    def test_get_copilot_token_failure(self, mock_get):
        mock_get.return_value = MagicMock(
            ok=False, status_code=401, reason="Unauthorized"
        )
        with self.assertRaises(RuntimeError):
            github_api.get_copilot_token("it")

    @patch("iclaw.github_api.requests.get")
    def test_get_models(self, mock_get):
        mock_get.return_value = MagicMock(ok=True, json=lambda: {"data": [{"id": "m"}]})
        self.assertEqual(github_api.get_models("t")[0]["id"], "m")

    @patch("iclaw.github_api.requests.get")
    def test_get_models_failure(self, mock_get):
        mock_get.return_value = MagicMock(ok=False, status_code=403, reason="Forbidden")
        with self.assertRaises(RuntimeError):
            github_api.get_models("t")

    @patch("iclaw.github_api.requests.post")
    def test_chat(self, mock_post):
        mock_post.return_value = MagicMock(
            ok=True, json=lambda: {"choices": [{"message": {"content": "h"}}]}
        )
        self.assertEqual(github_api.chat([], "t")["content"], "h")

    @patch("iclaw.github_api.requests.post")
    def test_chat_with_tools(self, mock_post):
        mock_post.return_value = MagicMock(
            ok=True, json=lambda: {"choices": [{"message": {"content": "h"}}]}
        )
        result = github_api.chat([], "t", tools=[{"type": "function"}])
        self.assertEqual(result["content"], "h")

    @patch("iclaw.github_api.requests.post")
    def test_chat_failure(self, mock_post):
        mock_post.return_value = MagicMock(
            ok=False, status_code=500, reason="Server Error", text="err"
        )
        with self.assertRaises(RuntimeError):
            github_api.chat([], "t")


if __name__ == "__main__":
    unittest.main()
