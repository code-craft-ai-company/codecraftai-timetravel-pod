"""
    Tests for the F0.2 Trace Configuration Model module.
"""

import unittest

from automojo.timetravel.pod.traceconfiguration import TraceConfiguration
from automojo.timetravel.pod.traceconfiguration import DEFAULT_TRACE_CONFIGURATION


class TestTraceConfiguration(unittest.TestCase):
    """
        Tests for the TraceConfiguration class.
    """

    def test_default_construction_values(self):
        """
            Verify default construction yields trace_calls=True, all others False.
        """
        config = TraceConfiguration()

        self.assertTrue(config.trace_calls)
        self.assertFalse(config.trace_lines)
        self.assertFalse(config.trace_variables)
        self.assertFalse(config.record_inner_portals)

        return

    def test_explicit_construction_preserves_values(self):
        """
            Verify explicit construction with all flags set preserves values.
        """
        config = TraceConfiguration(
            trace_calls=False,
            trace_lines=True,
            trace_variables=True,
            record_inner_portals=True,
        )

        self.assertFalse(config.trace_calls)
        self.assertTrue(config.trace_lines)
        self.assertTrue(config.trace_variables)
        self.assertTrue(config.record_inner_portals)

        return

    def test_properties_are_read_only(self):
        """
            Verify that setting properties raises AttributeError.
        """
        config = TraceConfiguration()

        with self.assertRaises(AttributeError):
            config.trace_calls = False

        with self.assertRaises(AttributeError):
            config.trace_lines = True

        with self.assertRaises(AttributeError):
            config.trace_variables = True

        with self.assertRaises(AttributeError):
            config.record_inner_portals = True

        return

    def test_as_dict_returns_correct_dictionary(self):
        """
            Verify as_dict() returns the expected dictionary.
        """
        config = TraceConfiguration(
            trace_calls=True,
            trace_lines=True,
            trace_variables=False,
            record_inner_portals=True,
        )

        result = config.as_dict()

        expected = {
            "trace_calls": True,
            "trace_lines": True,
            "trace_variables": False,
            "record_inner_portals": True,
        }
        self.assertEqual(result, expected)

        return

    def test_from_dict_round_trips_with_as_dict(self):
        """
            Verify from_dict() round-trips with as_dict().
        """
        original = TraceConfiguration(
            trace_calls=False,
            trace_lines=True,
            trace_variables=True,
            record_inner_portals=False,
        )

        data = original.as_dict()
        restored = TraceConfiguration.from_dict(data)

        self.assertEqual(restored.trace_calls, original.trace_calls)
        self.assertEqual(restored.trace_lines, original.trace_lines)
        self.assertEqual(restored.trace_variables, original.trace_variables)
        self.assertEqual(restored.record_inner_portals, original.record_inner_portals)

        return

    def test_from_dict_with_partial_data_uses_defaults(self):
        """
            Verify from_dict() with partial data uses defaults for missing keys.
        """
        partial_data = {"trace_lines": True}
        config = TraceConfiguration.from_dict(partial_data)

        self.assertTrue(config.trace_calls)  # default
        self.assertTrue(config.trace_lines)  # provided
        self.assertFalse(config.trace_variables)  # default
        self.assertFalse(config.record_inner_portals)  # default

        return


class TestDefaultTraceConfiguration(unittest.TestCase):
    """
        Tests for the DEFAULT_TRACE_CONFIGURATION constant.
    """

    def test_default_constant_has_expected_values(self):
        """
            Verify DEFAULT_TRACE_CONFIGURATION has the expected default values.
        """
        self.assertTrue(DEFAULT_TRACE_CONFIGURATION.trace_calls)
        self.assertFalse(DEFAULT_TRACE_CONFIGURATION.trace_lines)
        self.assertFalse(DEFAULT_TRACE_CONFIGURATION.trace_variables)
        self.assertFalse(DEFAULT_TRACE_CONFIGURATION.record_inner_portals)

        return


if __name__ == "__main__":
    unittest.main()
