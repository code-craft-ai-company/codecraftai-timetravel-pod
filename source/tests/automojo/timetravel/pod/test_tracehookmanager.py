"""
    Tests for the F1.1 Trace Hook Manager module.
"""

import threading
import unittest

from ccai.timetravel.pod.tracehookmanager import TraceHookManager
from ccai.timetravel.pod.traceconfiguration import TraceConfiguration
from ccai.timetravel.pod.traceclock import TraceClock
from ccai.timetravel.pod.traceclock import get_trace_clock
from ccai.timetravel.pod.traceevents import CallEvent
from ccai.timetravel.pod.traceevents import ReturnEvent
from ccai.timetravel.pod.traceevents import LineEvent
from ccai.timetravel.pod.traceevents import VariableSnapshotEvent
from ccai.timetravel.pod.traceevents import ExceptionEvent


class TestTraceHookManager(unittest.TestCase):
    """
        Tests for the TraceHookManager class.
    """

    def setUp(self):
        self._clock = get_trace_clock()
        self._clock.start()
        self._recorded_events = []
        return

    def tearDown(self):
        if self._clock.is_running:
            self._clock.stop()
        return

    def _record_callback(self, event):
        self._recorded_events.append(event)
        return

    def test_install_and_call_produces_call_and_return_events(self):
        """
            Verify installing the hook and calling a function produces
            CallEvent and ReturnEvent.
        """
        config = TraceConfiguration(trace_calls=True)
        manager = TraceHookManager(
            configuration=config, record_callback=self._record_callback
        )

        def simple_function():
            return 42

        manager.install()
        result = simple_function()
        manager.uninstall()

        call_events = [e for e in self._recorded_events if isinstance(e, CallEvent)]
        return_events = [e for e in self._recorded_events if isinstance(e, ReturnEvent)]

        self.assertGreater(len(call_events), 0)
        self.assertGreater(len(return_events), 0)

        # Find the call event for our function
        simple_calls = [e for e in call_events if e.function_name == "simple_function"]
        self.assertEqual(len(simple_calls), 1)

        return

    def test_trace_lines_true_produces_line_events(self):
        """
            Verify with trace_lines=True, executing code produces LineEvent objects.
        """
        config = TraceConfiguration(trace_calls=True, trace_lines=True)
        manager = TraceHookManager(
            configuration=config, record_callback=self._record_callback
        )

        def multi_line():
            a = 1
            b = 2
            c = a + b
            return c

        manager.install()
        multi_line()
        manager.uninstall()

        line_events = [e for e in self._recorded_events if isinstance(e, LineEvent)]

        self.assertGreater(len(line_events), 0)

        return

    def test_trace_lines_false_no_line_events(self):
        """
            Verify with trace_lines=False, no LineEvent objects are produced.
        """
        config = TraceConfiguration(trace_calls=True, trace_lines=False)
        manager = TraceHookManager(
            configuration=config, record_callback=self._record_callback
        )

        def multi_line():
            a = 1
            b = 2
            return a + b

        manager.install()
        multi_line()
        manager.uninstall()

        line_events = [e for e in self._recorded_events if isinstance(e, LineEvent)]

        self.assertEqual(len(line_events), 0)

        return

    def test_trace_variables_produces_snapshot_events(self):
        """
            Verify with trace_variables=True, VariableSnapshotEvent contains local
            variable data.
        """
        config = TraceConfiguration(
            trace_calls=True, trace_lines=True, trace_variables=True
        )
        manager = TraceHookManager(
            configuration=config, record_callback=self._record_callback
        )

        def var_function():
            x = 42
            y = "hello"
            return x

        manager.install()
        var_function()
        manager.uninstall()

        snapshot_events = [
            e for e in self._recorded_events
            if isinstance(e, VariableSnapshotEvent)
        ]

        self.assertGreater(len(snapshot_events), 0)

        # At least one snapshot should have our variables
        has_x = False
        for snap in snapshot_events:
            if "x" in snap.local_variables:
                has_x = True
                break

        self.assertTrue(has_x)

        return

    def test_exceptions_produce_exception_events(self):
        """
            Verify exceptions produce ExceptionEvent objects.
        """
        config = TraceConfiguration(trace_calls=True)
        manager = TraceHookManager(
            configuration=config, record_callback=self._record_callback
        )

        def failing_function():
            raise ValueError("test error")

        manager.install()
        try:
            failing_function()
        except ValueError:
            pass
        manager.uninstall()

        exception_events = [
            e for e in self._recorded_events if isinstance(e, ExceptionEvent)
        ]

        self.assertGreater(len(exception_events), 0)

        # Find the exception for our ValueError
        value_errors = [
            e for e in exception_events if e.exception_type == "ValueError"
        ]
        self.assertGreater(len(value_errors), 0)

        return

    def test_uninstall_stops_event_production(self):
        """
            Verify uninstall() stops all event production.
        """
        config = TraceConfiguration(trace_calls=True)
        manager = TraceHookManager(
            configuration=config, record_callback=self._record_callback
        )

        def func_a():
            return 1

        def func_b():
            return 2

        manager.install()
        func_a()
        manager.uninstall()

        count_after_uninstall = len(self._recorded_events)

        func_b()

        self.assertEqual(len(self._recorded_events), count_after_uninstall)

        return

    def test_events_carry_correct_thread_id(self):
        """
            Verify events carry the correct thread ID.
        """
        config = TraceConfiguration(trace_calls=True)
        manager = TraceHookManager(
            configuration=config, record_callback=self._record_callback
        )
        expected_thread_id = threading.get_ident()

        def simple():
            return 1

        manager.install()
        simple()
        manager.uninstall()

        for event in self._recorded_events:
            self.assertEqual(event.thread_id, expected_thread_id)

        return


if __name__ == "__main__":
    unittest.main()
