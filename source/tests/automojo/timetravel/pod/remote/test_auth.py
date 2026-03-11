"""
    Tests for the F5.2 Authentication and Credentials module.
"""

import unittest

from automojo.timetravel.pod.remote.auth import verify_credential


class TestVerifyCredential(unittest.TestCase):
    """
        Tests for the verify_credential function.
    """

    def test_matching_credential_returns_true(self):
        """
            Verify matching credential returns True.
        """
        result = verify_credential("secret123", "secret123")

        self.assertTrue(result)

        return

    def test_non_matching_credential_returns_false(self):
        """
            Verify non-matching credential returns False.
        """
        result = verify_credential("wrong", "secret123")

        self.assertFalse(result)

        return

    def test_none_expected_allows_all(self):
        """
            Verify None expected credential allows all (returns True).
        """
        result = verify_credential("anything", None)

        self.assertTrue(result)

        return

    def test_none_expected_allows_none_provided(self):
        """
            Verify None expected credential allows None provided (returns True).
        """
        result = verify_credential(None, None)

        self.assertTrue(result)

        return

    def test_none_provided_with_expected_returns_false(self):
        """
            Verify None provided credential with non-None expected returns False.
        """
        result = verify_credential(None, "secret123")

        self.assertFalse(result)

        return


if __name__ == "__main__":
    unittest.main()
