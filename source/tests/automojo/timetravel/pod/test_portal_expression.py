import unittest

from ccai.timetravel.pod.portal import TimeTravelPortal
from ccai.timetravel.pod.portalregistry import get_portal_registry
from ccai.timetravel.pod.tracingstate import get_tracing_state, set_gateway_active
from ccai.timetravel.pod.gateway import TimeTravelGateway, set_active_gateway
from ccai.timetravel.pod.traceconfiguration import TraceConfiguration

class TestPortalExpressionAndOnce(unittest.TestCase):
    def setUp(self):
        self.registry = get_portal_registry()
        self.registry.deactivate_all()

    def tearDown(self):
        self.registry.deactivate_all()
        set_gateway_active(False)
        set_active_gateway(None)
        state = get_tracing_state()
        state.reset()

    def test_expression_true_activates(self):
        self.registry.activate_portal("expr_portal", expression="my_var > 5")

        config = TraceConfiguration()
        gateway = TimeTravelGateway(configuration=config)
        with gateway:
            my_var = 10
            with TimeTravelPortal("expr_portal"):
                state = get_tracing_state()
                self.assertTrue(state.is_tracing)

    def test_expression_false_does_not_activate(self):
        self.registry.activate_portal("expr_portal", expression="my_var > 15")

        config = TraceConfiguration()
        gateway = TimeTravelGateway(configuration=config)
        with gateway:
            my_var = 10
            with TimeTravelPortal("expr_portal"):
                state = get_tracing_state()
                self.assertFalse(state.is_tracing)

    def test_expression_evaluation_error_does_not_activate(self):
        self.registry.activate_portal("expr_portal", expression="unknown_var > 15")

        config = TraceConfiguration()
        gateway = TimeTravelGateway(configuration=config)
        with gateway:
            with TimeTravelPortal("expr_portal"):
                state = get_tracing_state()
                self.assertFalse(state.is_tracing)

    def test_once_flag_deactivates_portal(self):
        self.registry.activate_portal("once_portal", once=True)
        self.assertTrue(self.registry.is_portal_active("once_portal"))

        config = TraceConfiguration()
        gateway = TimeTravelGateway(configuration=config)
        with gateway:
            with TimeTravelPortal("once_portal"):
                state = get_tracing_state()
                self.assertTrue(state.is_tracing)
                # Ensure it remains active while IN the portal block
                self.assertTrue(self.registry.is_portal_active("once_portal"))

            # The portal should be deactivated now
            self.assertFalse(self.registry.is_portal_active("once_portal"))

            # Subsequence uses should not trace
            with TimeTravelPortal("once_portal"):
                state = get_tracing_state()
                self.assertFalse(state.is_tracing)

if __name__ == "__main__":
    unittest.main()
