"""
    Provides the named portal context manager for scoped time travel tracing.

    This module contains the :class:`TimeTravelPortal` class which manages
    per-thread tracing activation, nested portal depth tracking, and
    trace hook installation.
"""

import threading
import sys

from typing import Optional

from automojo.timetravel.pod.tracingstate import get_tracing_state
from automojo.timetravel.pod.tracingstate import is_gateway_active
from automojo.timetravel.pod.portalregistry import get_portal_registry
from automojo.timetravel.pod.gateway import get_active_gateway
from automojo.timetravel.pod.tracehookmanager import TraceHookManager
from automojo.timetravel.pod.traceevents import PortalEnterEvent
from automojo.timetravel.pod.traceevents import PortalExitEvent
from automojo.timetravel.pod.traceclock import get_trace_clock


class TimeTravelPortal:
    """
        Named portal context manager for scoped time travel tracing.

        When entered, checks if the gateway is active and if this portal
        is activated. If so, installs a trace hook on the current thread.
        Nested portals increment a depth counter without installing
        additional hooks.
    """

    __slots__ = ("_name", "_activated_tracing", "_hook_manager", "_expression", "_once")

    def __init__(self, name: str, expression: Optional[str] = None, once: bool = False) -> None:
        """
            Create a TimeTravelPortal.

            :param name: The name of this portal.
            :param expression: An optional Python expression to evaluate dynamically.
            :param once: If True, this portal will only activate tracing once and then deactivate itself.
        """
        self._name = name
        self._expression = expression
        self._once = once
        self._activated_tracing = False
        self._hook_manager: Optional[TraceHookManager] = None
        return

    @property
    def name(self) -> str:
        """
            The name of this portal.
        """
        rtnval = self._name
        return rtnval

    def __enter__(self):
        """
            Enter the portal.

            If the gateway is not active or the portal is not activated,
            this is a no-op. If already tracing (nested portal), increments
            depth. Otherwise, activates tracing on this thread.

            :returns: This portal instance.
        """
        # Fast path: if gateway is not active, do nothing
        if not is_gateway_active():
            rtnval = self
            return rtnval

        state = get_tracing_state()

        if state.is_tracing:
            # Already inside an active portal — this is a nested portal
            state.portal_depth += 1
            gateway = get_active_gateway()
            if gateway is not None and gateway.configuration.record_inner_portals:
                clock = get_trace_clock()
                event = PortalEnterEvent(
                    timestamp_ns=clock.timestamp(),
                    thread_id=threading.get_ident(),
                    portal_name=self._name,
                )
                state.recorder.record(event)
            rtnval = self
            return rtnval

        # Check if this portal is activated
        registry = get_portal_registry()
        if not registry.is_portal_active(self._name):
            rtnval = self
            return rtnval

        if self._expression is not None:
            try:
                frame = sys._getframe(1)
                result = eval(self._expression, frame.f_globals, frame.f_locals)
                if not result:
                    rtnval = self
                    return rtnval
            except Exception:
                # If evaluation fails, do not activate tracing
                rtnval = self
                return rtnval

        if self._once:
            registry.deactivate_portal(self._name)

        # Activate tracing on this thread
        gateway = get_active_gateway()
        if gateway is None:
            rtnval = self
            return rtnval

        # Create hook manager and install
        hook_manager = TraceHookManager(
            configuration=gateway.configuration,
            record_callback=self._create_record_callback(gateway),
        )

        self._hook_manager = hook_manager
        self._activated_tracing = True

        state.is_tracing = True
        state.portal_depth = 1
        state.active_portal_name = self._name

        hook_manager.install()

        rtnval = self
        return rtnval

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
            Exit the portal.

            If this portal was not the outermost activating portal, decrements
            depth. Otherwise, tears down tracing on this thread.

            :returns: False to propagate exceptions.
        """
        if not self._activated_tracing:
            # This portal did not activate tracing
            state = get_tracing_state()
            if state.is_tracing and state.portal_depth > 1:
                # Nested portal exit
                state.portal_depth -= 1
                gateway = get_active_gateway()
                if gateway is not None and gateway.configuration.record_inner_portals:
                    clock = get_trace_clock()
                    event = PortalExitEvent(
                        timestamp_ns=clock.timestamp(),
                        thread_id=threading.get_ident(),
                        portal_name=self._name,
                    )
                    state.recorder.record(event)
            rtnval = False
            return rtnval

        # This portal activated tracing — tear down
        try:
            if self._hook_manager is not None:
                self._hook_manager.uninstall()

            state = get_tracing_state()
            state.reset()
        finally:
            self._activated_tracing = False
            self._hook_manager = None

        rtnval = False
        return rtnval

    def _create_record_callback(self, gateway):
        """
            Create a record callback that captures events.

            For now, this creates a list-based collector. In integration with
            the full system, this would delegate to a TraceRecorder.

            :param gateway: The active gateway.

            :returns: A callable that accepts a TraceEvent.
        """
        collected_events = []

        def record_callback(event):
            collected_events.append(event)
            return

        # Store on the tracing state for access
        state = get_tracing_state()
        state.recorder = _ListRecorder(collected_events)

        rtnval = record_callback
        return rtnval


class _ListRecorder:
    """
        A minimal recorder that collects events into a list for testing
        and initial integration purposes.
    """

    def __init__(self, events_list: list) -> None:
        self._events = events_list
        return

    def record(self, event) -> None:
        """
            Record an event into the list.

            :param event: The trace event.
        """
        self._events.append(event)
        return

    def flush(self) -> None:
        """
            No-op flush.
        """
        return

    def close(self) -> None:
        """
            No-op close.
        """
        return
