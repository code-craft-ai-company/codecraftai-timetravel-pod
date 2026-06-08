"""
    Tests for the F0.1 Thread-Local Tracing State module.
"""

import threading
import unittest

from ccai.timetravel.pod.tracingstate import TracingState
from ccai.timetravel.pod.tracingstate import get_tracing_state
from ccai.timetravel.pod.tracingstate import is_gateway_active
from ccai.timetravel.pod.tracingstate import set_gateway_active


class TestTracingState(unittest.TestCase):
    """
        Tests for the TracingState class.
    """

    def test_default_initialization(self):
        """
            Verify the default TracingState has correct initial values.
        """
        state = TracingState()

        self.assertFalse(state.is_tracing)
        self.assertIsNone(state.recorder)
        self.assertEqual(state.portal_depth, 0)
        self.assertIsNone(state.active_portal_name)

        return

    def test_reset_restores_defaults(self):
        """
            Verify reset() restores all fields to their default values.
        """
        state = TracingState()

        state.is_tracing = True
        state.recorder = "mock_recorder"
        state.portal_depth = 3
        state.active_portal_name = "test_portal"

        state.reset()

        self.assertFalse(state.is_tracing)
        self.assertIsNone(state.recorder)
        self.assertEqual(state.portal_depth, 0)
        self.assertIsNone(state.active_portal_name)

        return


class TestGetTracingState(unittest.TestCase):
    """
        Tests for the get_tracing_state() function.
    """

    def test_returns_same_instance_on_same_thread(self):
        """
            Verify get_tracing_state() returns the same instance on repeated
            calls from the same thread.
        """
        state_a = get_tracing_state()
        state_b = get_tracing_state()

        self.assertIs(state_a, state_b)

        return

    def test_returns_different_instances_for_different_threads(self):
        """
            Verify get_tracing_state() returns different instances for different
            threads.
        """
        main_state = get_tracing_state()
        other_state_holder = [None]

        def get_state_on_other_thread():
            other_state_holder[0] = get_tracing_state()
            return

        thread = threading.Thread(target=get_state_on_other_thread)
        thread.start()
        thread.join()

        other_state = other_state_holder[0]

        self.assertIsNotNone(other_state)
        self.assertIsNot(main_state, other_state)

        return

    def test_modifying_state_on_one_thread_does_not_affect_another(self):
        """
            Verify that modifying state on one thread does not affect another
            thread's state.
        """
        main_state = get_tracing_state()
        main_state.is_tracing = True
        main_state.portal_depth = 5

        other_state_holder = [None]

        def check_state_on_other_thread():
            other_state = get_tracing_state()
            other_state_holder[0] = other_state
            return

        thread = threading.Thread(target=check_state_on_other_thread)
        thread.start()
        thread.join()

        other_state = other_state_holder[0]

        self.assertFalse(other_state.is_tracing)
        self.assertEqual(other_state.portal_depth, 0)

        # Clean up main thread state
        main_state.reset()

        return


class TestGatewayActive(unittest.TestCase):
    """
        Tests for the is_gateway_active() and set_gateway_active() functions.
    """

    def setUp(self):
        set_gateway_active(False)
        return

    def tearDown(self):
        set_gateway_active(False)
        return

    def test_defaults_to_false(self):
        """
            Verify is_gateway_active() defaults to False.
        """
        self.assertFalse(is_gateway_active())

        return

    def test_set_gateway_active_true(self):
        """
            Verify set_gateway_active(True) makes is_gateway_active() return True.
        """
        set_gateway_active(True)

        self.assertTrue(is_gateway_active())

        return

    def test_set_gateway_active_false_after_true(self):
        """
            Verify set_gateway_active(False) after True makes it return False.
        """
        set_gateway_active(True)
        set_gateway_active(False)

        self.assertFalse(is_gateway_active())

        return


if __name__ == "__main__":
    unittest.main()
