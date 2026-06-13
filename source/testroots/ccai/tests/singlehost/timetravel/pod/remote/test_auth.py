"""
    Tests for the F5.2 Authentication and Credentials module.
"""

from ccai.timetravel.pod.remote.auth import verify_credential


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


def test_none_expected_denies() -> None:
    """
        Verify that with NO credential configured the server fails closed
        (returns False) rather than allowing all -- the remote-control surface
        can activate an eval()'d portal expression, so it must not be open.
    """
    result = verify_credential("anything", None)

    assert not result

    return


def test_none_expected_denies_none_provided() -> None:
    """
        Verify that with no credential configured, a None-provided credential is
        also denied (fail closed).
    """
    result = verify_credential(None, None)

    assert not result

    return


def test_none_provided_with_expected_returns_false() -> None:
    """
        Verify None provided credential with non-None expected returns False.
    """
    result = verify_credential(None, "secret123")

    assert not result

    return
