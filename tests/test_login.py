import unittest
from unittest.mock import MagicMock, patch
from iclaw import login


class TestLogin(unittest.TestCase):
    @patch("iclaw.login.requests.post")
    def test_login_flow(self, mock_post):
        mock_post.return_value = MagicMock(
            ok=True,
            json=lambda: {
                "device_code": "dc",
                "user_code": "uc",
                "verification_uri": "v",
            },
        )
        self.assertEqual(login.get_device_code()["device_code"], "dc")

        mock_post.side_effect = [
            MagicMock(ok=True, json=lambda: {"access_token": "at"})
        ]
        with patch("iclaw.login.time.sleep"):
            self.assertEqual(login.poll_for_access_token("dc", 1), "at")

    @patch("iclaw.login.requests.post")
    @patch("iclaw.login.time.sleep")
    def test_poll_authorization_pending(self, mock_sleep, mock_post):
        mock_post.side_effect = [
            MagicMock(ok=True, json=lambda: {"error": "authorization_pending"}),
            MagicMock(ok=True, json=lambda: {"access_token": "at"}),
        ]
        with patch("sys.stdout"):
            result = login.poll_for_access_token("dc", 1)
        self.assertEqual(result, "at")

    @patch("iclaw.login.requests.post")
    @patch("iclaw.login.time.sleep")
    def test_poll_slow_down(self, mock_sleep, mock_post):
        mock_post.side_effect = [
            MagicMock(ok=True, json=lambda: {"error": "slow_down"}),
            MagicMock(ok=True, json=lambda: {"access_token": "at"}),
        ]
        result = login.poll_for_access_token("dc", 1)
        self.assertEqual(result, "at")

    @patch("iclaw.login.requests.post")
    @patch("iclaw.login.time.sleep")
    def test_poll_expired_token(self, mock_sleep, mock_post):
        mock_post.return_value = MagicMock(
            ok=True, json=lambda: {"error": "expired_token"}
        )
        with self.assertRaises(RuntimeError):
            login.poll_for_access_token("dc", 1)

    @patch("iclaw.login.requests.post")
    @patch("iclaw.login.time.sleep")
    def test_poll_unknown_error(self, mock_sleep, mock_post):
        mock_post.return_value = MagicMock(
            ok=True, json=lambda: {"error": "something_else"}
        )
        with self.assertRaises(RuntimeError):
            login.poll_for_access_token("dc", 1)


if __name__ == "__main__":
    unittest.main()
