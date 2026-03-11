"""
    Provides per-thread tracing state management for the time travel pod.

    This module contains the :class:`TracingState` class which tracks whether
    a thread is currently tracing, the active recorder, portal depth, and the
    active portal name. It also provides the gateway-active flag which is a
    process-wide (not thread-local) state.
"""

import threading

from typing import Optional


class TracingState:
    """
        Per-thread tracing state container.

        Stores the tracing status, active recorder reference, portal nesting
        depth, and the name of the outermost active portal for a single thread.
    """

    def __init__(self) -> None:
        self.is_tracing: bool = False
        self.recorder = None
        self.portal_depth: int = 0
        self.active_portal_name: Optional[str] = None
        return

    def reset(self) -> None:
        """
            Reset the tracing state to defaults.
        """
        self.is_tracing = False
        self.recorder = None
        self.portal_depth = 0
        self.active_portal_name = None
        return


_thread_local = threading.local()


def get_tracing_state() -> TracingState:
    """
        Return the TracingState for the current thread, creating it if needed.

        :returns: The per-thread TracingState instance.
    """
    state = getattr(_thread_local, "tracing_state", None)
    if state is None:
        state = TracingState()
        _thread_local.tracing_state = state
    rtnval = state
    return rtnval


_gateway_active: bool = False


def is_gateway_active() -> bool:
    """
        Return whether the gateway is currently active.

        :returns: True if the gateway has been entered, False otherwise.
    """
    rtnval = _gateway_active
    return rtnval


def set_gateway_active(active: bool) -> None:
    """
        Set the gateway-active flag.

        :param active: True if the gateway is being entered, False if exiting.
    """
    global _gateway_active
    _gateway_active = active
    return
