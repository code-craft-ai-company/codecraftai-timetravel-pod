"""
    Tests for the F2 portal expression evaluation and once-flag behaviour.
"""

import threading
import sys

from automojo.timetravel.pod.portal import TimeTravelPortal
from automojo.timetravel.pod.portalregistry import get_portal_registry
from automojo.timetravel.pod.portalregistry import PortalRegistry
from automojo.timetravel.pod.tracingstate import get_tracing_state, set_gateway_active
from automojo.timetravel.pod.gateway import TimeTravelGateway, set_active_gateway
from automojo.timetravel.pod.traceconfiguration import TraceConfiguration


def _setup_portal_expression_and_once() -> PortalRegistry:
    """
        Replicates the TestPortalExpressionAndOnce.setUp behaviour, acquiring
        the portal registry and deactivating all portals to ensure isolation.

        :returns: The portal registry instance.
    """
    registry = get_portal_registry()
    registry.deactivate_all()
    return registry


def _teardown_portal_expression_and_once(registry: PortalRegistry) -> None:
    """
        Replicates the TestPortalExpressionAndOnce.tearDown behaviour, resetting
        the registry, gateway-active flag, active gateway, and tracing state.

        :param registry: The portal registry instance acquired during setup.
    """
    registry.deactivate_all()
    set_gateway_active(False)
    set_active_gateway(None)
    state = get_tracing_state()
    state.reset()
    return


def test_expression_true_activates() -> None:
    """
        Verify a portal whose expression evaluates true activates tracing.
    """
    registry = _setup_portal_expression_and_once()

    try:
        registry.activate_portal("expr_portal", expression="my_var > 5")

        config = TraceConfiguration()
        gateway = TimeTravelGateway(configuration=config)
        with gateway:
            my_var = 10
            with TimeTravelPortal("expr_portal"):
                state = get_tracing_state()
                assert state.is_tracing
    finally:
        _teardown_portal_expression_and_once(registry=registry)

    return


def test_expression_false_does_not_activate() -> None:
    """
        Verify a portal whose expression evaluates false does not activate
        tracing.
    """
    registry = _setup_portal_expression_and_once()

    try:
        registry.activate_portal("expr_portal", expression="my_var > 15")

        config = TraceConfiguration()
        gateway = TimeTravelGateway(configuration=config)
        with gateway:
            my_var = 10
            with TimeTravelPortal("expr_portal"):
                state = get_tracing_state()
                assert not state.is_tracing
    finally:
        _teardown_portal_expression_and_once(registry=registry)

    return


def test_expression_evaluation_error_does_not_activate() -> None:
    """
        Verify a portal whose expression raises an evaluation error does not
        activate tracing.
    """
    registry = _setup_portal_expression_and_once()

    try:
        registry.activate_portal("expr_portal", expression="unknown_var > 15")

        config = TraceConfiguration()
        gateway = TimeTravelGateway(configuration=config)
        with gateway:
            with TimeTravelPortal("expr_portal"):
                state = get_tracing_state()
                assert not state.is_tracing
    finally:
        _teardown_portal_expression_and_once(registry=registry)

    return


def test_once_flag_deactivates_portal() -> None:
    """
        Verify a once-flagged portal deactivates after a single use.
    """
    registry = _setup_portal_expression_and_once()

    try:
        registry.activate_portal("once_portal", once=True)
        assert registry.is_portal_active("once_portal")

        config = TraceConfiguration()
        gateway = TimeTravelGateway(configuration=config)
        with gateway:
            with TimeTravelPortal("once_portal"):
                state = get_tracing_state()
                assert state.is_tracing
                # Ensure it remains active while IN the portal block
                assert registry.is_portal_active("once_portal")

            # The portal should be deactivated now
            assert not registry.is_portal_active("once_portal")

            # Subsequence uses should not trace
            with TimeTravelPortal("once_portal"):
                state = get_tracing_state()
                assert not state.is_tracing
    finally:
        _teardown_portal_expression_and_once(registry=registry)

    return
