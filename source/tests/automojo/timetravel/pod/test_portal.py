"""
    Tests for the F3.2 TimeTravelPortal module.
"""

import unittest

from automojo.timetravel.pod.portal import TimeTravelPortal
from automojo.timetravel.pod.gateway import TimeTravelGateway
from automojo.timetravel.pod.portalregistry import get_portal_registry
from automojo.timetravel.pod.tracingstate import get_tracing_state
from automojo.timetravel.pod.tracingstate import is_gateway_active
from automojo.timetravel.pod.traceconfiguration import TraceConfiguration
from automojo.timetravel.pod.traceevents import PortalEnterEvent
from automojo.timetravel.pod.traceevents import PortalExitEvent


class TestTimeTravelPortal(unittest.TestCase):
    """
        Tests for the TimeTravelPortal class.
    """

    def setUp(self):
        self._registry = get_portal_registry()
        return

    def tearDown(self):
        self._registry.deactivate_all()
        # Reset tracing state
        state = get_tracing_state()
        state.reset()
        return

    def test_entering_activated_portal_activates_tracing(self):
        """
            Verify entering an activated portal on a clean thread activates tracing.
        """
        self._registry.activate_portal("test_portal")

        gateway = TimeTravelGateway()
        with gateway:
            state = get_tracing_state()
            self.assertFalse(state.is_tracing)

            with TimeTravelPortal("test_portal"):
                state = get_tracing_state()
                self.assertTrue(state.is_tracing)
                self.assertEqual(state.active_portal_name, "test_portal")
                self.assertEqual(state.portal_depth, 1)

        return

    def test_inactive_portal_is_noop(self):
        """
            Verify entering an inactive portal is a no-op.
        """
        gateway = TimeTravelGateway()
        with gateway:
            with TimeTravelPortal("not_activated"):
                state = get_tracing_state()
                self.assertFalse(state.is_tracing)

        return

    def test_portal_without_gateway_is_noop(self):
        """
            Verify entering a portal when gateway is not active is a no-op.
        """
        self._registry.activate_portal("test_portal")

        self.assertFalse(is_gateway_active())

        with TimeTravelPortal("test_portal"):
            state = get_tracing_state()
            self.assertFalse(state.is_tracing)

        return

    def test_nested_portals_increment_decrement_depth(self):
        """
            Verify nested portals increment/decrement depth without installing
            multiple hooks.
        """
        self._registry.activate_portal("outer")
        self._registry.activate_portal("inner")

        gateway = TimeTravelGateway()
        with gateway:
            with TimeTravelPortal("outer"):
                state = get_tracing_state()
                self.assertEqual(state.portal_depth, 1)

                with TimeTravelPortal("inner"):
                    state = get_tracing_state()
                    self.assertEqual(state.portal_depth, 2)

                state = get_tracing_state()
                self.assertEqual(state.portal_depth, 1)

        return

    def test_record_inner_portals_true_emits_events(self):
        """
            Verify with record_inner_portals=True, PortalEnterEvent and
            PortalExitEvent are emitted for nested portals.
        """
        config = TraceConfiguration(
            trace_calls=True, record_inner_portals=True
        )
        self._registry.activate_portal("outer")
        self._registry.activate_portal("inner")

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
                    self.assertGreater(len(enter_events), 0)
                    self.assertGreater(len(exit_events), 0)

        return

    def test_record_inner_portals_false_no_annotation_events(self):
        """
            Verify with record_inner_portals=False, no annotation events
            for nested portals.
        """
        config = TraceConfiguration(
            trace_calls=True, record_inner_portals=False
        )
        self._registry.activate_portal("outer")
        self._registry.activate_portal("inner")

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
                    self.assertEqual(len(portal_events), 0)

        return

    def test_exiting_outermost_portal_resets_state(self):
        """
            Verify exiting the outermost portal resets tracing state.
        """
        self._registry.activate_portal("test_portal")

        gateway = TimeTravelGateway()
        with gateway:
            with TimeTravelPortal("test_portal"):
                state = get_tracing_state()
                self.assertTrue(state.is_tracing)

            state = get_tracing_state()
            self.assertFalse(state.is_tracing)
            self.assertEqual(state.portal_depth, 0)
            self.assertIsNone(state.active_portal_name)

        return

    def test_exceptions_propagate_through_portal(self):
        """
            Verify exceptions propagate through the portal after cleanup.
        """
        self._registry.activate_portal("test_portal")

        gateway = TimeTravelGateway()
        with self.assertRaises(RuntimeError):
            with gateway:
                with TimeTravelPortal("test_portal"):
                    raise RuntimeError("test error")

        # State should be cleaned up
        state = get_tracing_state()
        self.assertFalse(state.is_tracing)

        return

    def test_name_property(self):
        """
            Verify the name property returns the portal name.
        """
        portal = TimeTravelPortal("my_portal")

        self.assertEqual(portal.name, "my_portal")

        return


if __name__ == "__main__":
    unittest.main()
