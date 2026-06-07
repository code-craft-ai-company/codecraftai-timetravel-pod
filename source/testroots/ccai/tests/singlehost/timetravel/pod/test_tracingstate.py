"""
    Tests for the F0.1 Thread-Local Tracing State module.
"""

import threading

from ccai.timetravel.pod.tracingstate import TracingState
from ccai.timetravel.pod.tracingstate import get_tracing_state
from ccai.timetravel.pod.tracingstate import is_gateway_active
from ccai.timetravel.pod.tracingstate import set_gateway_active


def _setup_gateway_active() -> None:
    """
        Replicate the original TestGatewayActive.setUp behaviour by forcing
        the gateway-active state to False before a test runs.
    """
    set_gateway_active(False)
    return


def _teardown_gateway_active() -> None:
    """
        Replicate the original TestGatewayActive.tearDown behaviour by forcing
        the gateway-active state back to False after a test runs.
    """
    set_gateway_active(False)
    return


def test_default_initialization() -> None:
    """
        Verify the default TracingState has correct initial values.
    """
    state = TracingState()

    assert not state.is_tracing
    assert state.recorder is None
    assert state.portal_depth == 0
    assert state.active_portal_name is None

    return


def test_reset_restores_defaults() -> None:
    """
        Verify reset() restores all fields to their default values.
    """
    state = TracingState()

    state.is_tracing = True
    state.recorder = "mock_recorder"
    state.portal_depth = 3
    state.active_portal_name = "test_portal"

    state.reset()

    assert not state.is_tracing
    assert state.recorder is None
    assert state.portal_depth == 0
    assert state.active_portal_name is None

    return


def test_returns_same_instance_on_same_thread() -> None:
    """
        Verify get_tracing_state() returns the same instance on repeated
        calls from the same thread.
    """
    state_a = get_tracing_state()
    state_b = get_tracing_state()

    assert state_a is state_b

    return


def test_returns_different_instances_for_different_threads() -> None:
    """
        Verify get_tracing_state() returns different instances for different
        threads.
    """
    main_state = get_tracing_state()
    other_state_holder = [None]

    def get_state_on_other_thread() -> None:
        other_state_holder[0] = get_tracing_state()
        return

    thread = threading.Thread(target=get_state_on_other_thread)
    thread.start()
    thread.join()

    other_state = other_state_holder[0]

    assert other_state is not None
    assert main_state is not other_state

    return


def test_modifying_state_on_one_thread_does_not_affect_another() -> None:
    """
        Verify that modifying state on one thread does not affect another
        thread's state.
    """
    main_state = get_tracing_state()
    main_state.is_tracing = True
    main_state.portal_depth = 5

    other_state_holder = [None]

    def check_state_on_other_thread() -> None:
        other_state = get_tracing_state()
        other_state_holder[0] = other_state
        return

    thread = threading.Thread(target=check_state_on_other_thread)
    thread.start()
    thread.join()

    other_state = other_state_holder[0]

    assert not other_state.is_tracing
    assert other_state.portal_depth == 0

    # Clean up main thread state
    main_state.reset()

    return


def test_defaults_to_false() -> None:
    """
        Verify is_gateway_active() defaults to False.
    """
    _setup_gateway_active()
    try:
        assert not is_gateway_active()
    finally:
        _teardown_gateway_active()

    return


def test_set_gateway_active_true() -> None:
    """
        Verify set_gateway_active(True) makes is_gateway_active() return True.
    """
    _setup_gateway_active()
    try:
        set_gateway_active(True)

        assert is_gateway_active()
    finally:
        _teardown_gateway_active()

    return


def test_set_gateway_active_false_after_true() -> None:
    """
        Verify set_gateway_active(False) after True makes it return False.
    """
    _setup_gateway_active()
    try:
        set_gateway_active(True)
        set_gateway_active(False)

        assert not is_gateway_active()
    finally:
        _teardown_gateway_active()

    return
