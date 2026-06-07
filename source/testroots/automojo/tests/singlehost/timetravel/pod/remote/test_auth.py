"""
    Tests for the F5.2 Authentication and Credentials module.
"""

from automojo.timetravel.pod.remote.auth import verify_credential


def test_matching_credential_returns_true() -> None:
    """
        Verify matching credential returns True.
    """
    result = verify_credential("secret123", "secret123")

    assert result

    return


def test_non_matching_credential_returns_false() -> None:
    """
        Verify non-matching credential returns False.
    """
    result = verify_credential("wrong", "secret123")

    assert not result

    return


def test_none_expected_allows_all() -> None:
    """
        Verify None expected credential allows all (returns True).
    """
    result = verify_credential("anything", None)

    assert result

    return


def test_none_expected_allows_none_provided() -> None:
    """
        Verify None expected credential allows None provided (returns True).
    """
    result = verify_credential(None, None)

    assert result

    return


def test_none_provided_with_expected_returns_false() -> None:
    """
        Verify None provided credential with non-None expected returns False.
    """
    result = verify_credential(None, "secret123")

    assert not result

    return
