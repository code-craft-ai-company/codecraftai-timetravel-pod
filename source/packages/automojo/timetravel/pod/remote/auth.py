"""
    Provides authentication utilities for the remote control server.

    This module contains the :func:`verify_credential` function which
    performs constant-time credential comparison using ``hmac.compare_digest``.
"""

import hmac

from typing import Optional


def verify_credential(provided: Optional[str], expected: Optional[str]) -> bool:
    """
        Verify a provided credential against the expected credential.

        Uses constant-time comparison via ``hmac.compare_digest`` to prevent
        timing attacks. Returns True if authentication passes.

        :param provided: The credential provided in the request.
        :param expected: The expected credential configured on the server.

        :returns: True if authentication passes, False otherwise.
    """
    if expected is None:
        # No credential configured — allow all
        rtnval = True
        return rtnval

    if provided is None:
        rtnval = False
        return rtnval

    rtnval = hmac.compare_digest(provided, expected)
    return rtnval
