"""
    Tests for the F4.1 Startup Configuration module.
"""

import unittest

from automojo.timetravel.pod.configuration import TimeTravelConfig
from automojo.timetravel.pod.configuration import configure_timetravel
from automojo.timetravel.pod.traceconfiguration import TraceConfiguration
from automojo.timetravel.pod.traceconfiguration import DEFAULT_TRACE_CONFIGURATION
from automojo.timetravel.pod.portalregistry import PortalRegistry
from automojo.timetravel.pod.portalregistry import get_portal_registry


class TestTimeTravelConfig(unittest.TestCase):
    """
        Tests for the TimeTravelConfig class.
    """

    def test_defaults_are_correct(self):
        """
            Verify TimeTravelConfig defaults are correct.
        """
        config = TimeTravelConfig()

        self.assertEqual(config.active_portals, [])
        self.assertIs(config.trace_configuration, DEFAULT_TRACE_CONFIGURATION)
        self.assertIsNone(config.backend_uri)
        self.assertFalse(config.remote_enabled)
        self.assertEqual(config.remote_host, "127.0.0.1")
        self.assertEqual(config.remote_port, 9876)
        self.assertIsNone(config.remote_credential)
        self.assertIsNone(config.service_url)
        self.assertIsNone(config.service_credential)

        return

    def test_as_dict_from_dict_round_trip(self):
        """
            Verify as_dict() / from_dict() round-trip.
        """
        trace_config = TraceConfiguration(
            trace_calls=True, trace_lines=True, trace_variables=True
        )
        original = TimeTravelConfig(
            active_portals=["portal_a", "portal_b"],
            trace_configuration=trace_config,
            backend_uri="file:///tmp/trace.bin",
            remote_enabled=True,
            remote_host="0.0.0.0",
            remote_port=8080,
        )

        data = original.as_dict()
        restored = TimeTravelConfig.from_dict(data)

        self.assertEqual(restored.active_portals, ["portal_a", "portal_b"])
        self.assertEqual(restored.backend_uri, "file:///tmp/trace.bin")
        self.assertTrue(restored.remote_enabled)
        self.assertEqual(restored.remote_host, "0.0.0.0")
        self.assertEqual(restored.remote_port, 8080)
        self.assertTrue(restored.trace_configuration.trace_calls)
        self.assertTrue(restored.trace_configuration.trace_lines)
        self.assertTrue(restored.trace_configuration.trace_variables)

        return

    def test_as_dict_excludes_credentials(self):
        """
            Verify credentials are excluded from as_dict().
        """
        config = TimeTravelConfig(
            remote_credential="secret", service_credential="token"
        )

        data = config.as_dict()

        self.assertNotIn("remote_credential", data)
        self.assertNotIn("service_credential", data)

        return

    def test_active_portals_returns_copy(self):
        """
            Verify active_portals returns a copy, not the internal list.
        """
        config = TimeTravelConfig(active_portals=["a", "b"])

        portals = config.active_portals
        portals.append("c")

        self.assertEqual(len(config.active_portals), 2)

        return


class TestConfigureTimetravel(unittest.TestCase):
    """
        Tests for the configure_timetravel function.
    """

    def setUp(self):
        self._registry = get_portal_registry()
        return

    def tearDown(self):
        self._registry.deactivate_all()
        return

    def test_activates_specified_portals(self):
        """
            Verify configure_timetravel activates specified portals in the registry.
        """
        config = TimeTravelConfig(
            active_portals=["portal_x", "portal_y"]
        )

        configure_timetravel(config)

        self.assertTrue(self._registry.is_portal_active("portal_x"))
        self.assertTrue(self._registry.is_portal_active("portal_y"))

        return

    def test_no_backend_uri_does_not_create_backend(self):
        """
            Verify configure_timetravel with no backend URI does not create
            a backend (no error occurs).
        """
        config = TimeTravelConfig()

        # This should not raise
        configure_timetravel(config)

        return

    def test_from_dict_with_empty_dict(self):
        """
            Verify from_dict with empty dict uses defaults.
        """
        config = TimeTravelConfig.from_dict({})

        self.assertEqual(config.active_portals, [])
        self.assertIsNone(config.backend_uri)
        self.assertFalse(config.remote_enabled)

        return


if __name__ == "__main__":
    unittest.main()
