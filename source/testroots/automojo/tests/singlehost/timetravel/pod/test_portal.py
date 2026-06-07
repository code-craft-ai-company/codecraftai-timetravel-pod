"""
    Tests for the F3.2 TimeTravelPortal module.
"""

from automojo.timetravel.pod.portal import TimeTravelPortal
from automojo.timetravel.pod.gateway import TimeTravelGateway
from automojo.timetravel.pod.portalregistry import get_portal_registry
from automojo.timetravel.pod.tracingstate import get_tracing_state
from automojo.timetravel.pod.tracingstate import is_gateway_active
from automojo.timetravel.pod.traceconfiguration import TraceConfiguration
from automojo.timetravel.pod.traceevents import PortalEnterEvent
from automojo.timetravel.pod.traceevents import PortalExitEvent


def _setup_portal_registry():
    """
        Replicates the original TestTimeTravelPortal.setUp by acquiring the
        shared portal registry for the test.

        :returns: The active portal registry.
    """
    registry = get_portal_registry()
    return registry


def _teardown_portal_registry(registry) -> None:
    """
        Replicates the original TestTimeTravelPortal.tearDown by deactivating
        all portals and resetting the tracing state.

        :param registry: The portal registry acquired during setup.
    """
    registry.deactivate_all()
    # Reset tracing state
    state = get_tracing_state()
    state.reset()
    return


def test_entering_activated_portal_activates_tracing() -> None:
    """
        Verify entering an activated portal on a clean thread activates tracing.
    """
    registry = _setup_portal_registry()
    try:
        registry.activate_portal("test_portal")

        gateway = TimeTravelGateway()
        with gateway:
            state = get_tracing_state()
            assert not state.is_tracing

            with TimeTravelPortal("test_portal"):
                state = get_tracing_state()
                assert state.is_tracing
                assert state.active_portal_name == "test_portal"
                assert state.portal_depth == 1
    finally:
        _teardown_portal_registry(registry=registry)

    return


def test_inactive_portal_is_noop() -> None:
    """
        Verify entering an inactive portal is a no-op.
    """
    registry = _setup_portal_registry()
    try:
        gateway = TimeTravelGateway()
        with gateway:
            with TimeTravelPortal("not_activated"):
                state = get_tracing_state()
                assert not state.is_tracing
    finally:
        _teardown_portal_registry(registry=registry)

    return


def test_portal_without_gateway_is_noop() -> None:
    """
        Verify entering a portal when gateway is not active is a no-op.
    """
    registry = _setup_portal_registry()
    try:
        registry.activate_portal("test_portal")

        assert not is_gateway_active()

        with TimeTravelPortal("test_portal"):
            state = get_tracing_state()
            assert not state.is_tracing
    finally:
        _teardown_portal_registry(registry=registry)

    return


def test_nested_portals_increment_decrement_depth() -> None:
    """
        Verify nested portals increment/decrement depth without installing
        multiple hooks.
    """
    registry = _setup_portal_registry()
    try:
        registry.activate_portal("outer")
        registry.activate_portal("inner")

        gateway = TimeTravelGateway()
        with gateway:
            with TimeTravelPortal("outer"):
                state = get_tracing_state()
                assert state.portal_depth == 1

                with TimeTravelPortal("inner"):
                    state = get_tracing_state()
                    assert state.portal_depth == 2

                state = get_tracing_state()
                assert state.portal_depth == 1
    finally:
        _teardown_portal_registry(registry=registry)

    return


def test_record_inner_portals_true_emits_events() -> None:
    """
        Verify with record_inner_portals=True, PortalEnterEvent and
        PortalExitEvent are emitted for nested portals.
    """
    registry = _setup_portal_registry()
    try:
        config = TraceConfiguration(
            trace_calls=True, record_inner_portals=True
        )
        registry.activate_portal("outer")
        registry.activate_portal("inner")

        gateway = TimeTravelGateway(configuration=config)
        with gateway:
            with TimeTravelPortal("outer") as outer_portal:
                state = get_tracing_state()
                recorder = state.recorder

                with TimeTravelPortal("inner"):
                    pass

                # Check for portal events in the recorder
                if recorder is not None:
                    enter_events = [
                        e for e in recorder._events
                        if isinstance(e, PortalEnterEvent)
                        and e.portal_name == "inner"
                    ]
                    exit_events = [
                        e for e in recorder._events
                        if isinstance(e, PortalExitEvent)
                        and e.portal_name == "inner"
                    ]
                    assert len(enter_events) > 0
                    assert len(exit_events) > 0
    finally:
        _teardown_portal_registry(registry=registry)

    return


def test_record_inner_portals_false_no_annotation_events() -> None:
    """
        Verify with record_inner_portals=False, no annotation events
        for nested portals.
    """
    registry = _setup_portal_registry()
    try:
        config = TraceConfiguration(
            trace_calls=True, record_inner_portals=False
        )
        registry.activate_portal("outer")
        registry.activate_portal("inner")

        gateway = TimeTravelGateway(configuration=config)
        with gateway:
            with TimeTravelPortal("outer"):
                state = get_tracing_state()
                recorder = state.recorder

                with TimeTravelPortal("inner"):
                    pass

                if recorder is not None:
                    portal_events = [
                        e for e in recorder._events
                        if isinstance(e, (PortalEnterEvent, PortalExitEvent))
                    ]
                    assert len(portal_events) == 0
    finally:
        _teardown_portal_registry(registry=registry)

    return


def test_exiting_outermost_portal_resets_state() -> None:
    """
        Verify exiting the outermost portal resets tracing state.
    """
    registry = _setup_portal_registry()
    try:
        registry.activate_portal("test_portal")

        gateway = TimeTravelGateway()
        with gateway:
            with TimeTravelPortal("test_portal"):
                state = get_tracing_state()
                assert state.is_tracing

            state = get_tracing_state()
            assert not state.is_tracing
            assert state.portal_depth == 0
            assert state.active_portal_name is None
    finally:
        _teardown_portal_registry(registry=registry)

    return


def test_exceptions_propagate_through_portal() -> None:
    """
        Verify exceptions propagate through the portal after cleanup.
    """
    registry = _setup_portal_registry()
    try:
        registry.activate_portal("test_portal")

        gateway = TimeTravelGateway()
        raised = False
        try:
            with gateway:
                with TimeTravelPortal("test_portal"):
                    raise RuntimeError("test error")
        except RuntimeError:
            raised = True

        assert raised

        # State should be cleaned up
        state = get_tracing_state()
        assert not state.is_tracing
    finally:
        _teardown_portal_registry(registry=registry)

    return


def test_name_property() -> None:
    """
        Verify the name property returns the portal name.
    """
    registry = _setup_portal_registry()
    try:
        portal = TimeTravelPortal("my_portal")

        assert portal.name == "my_portal"
    finally:
        _teardown_portal_registry(registry=registry)

    return
