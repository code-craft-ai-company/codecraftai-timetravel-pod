"""
    Tests for the F0.2 Trace Configuration Model module.
"""

from automojo.timetravel.pod.traceconfiguration import TraceConfiguration
from automojo.timetravel.pod.traceconfiguration import DEFAULT_TRACE_CONFIGURATION


def test_default_construction_values() -> None:
    """
        Verify default construction yields trace_calls=True, all others False.
    """
    config = TraceConfiguration()

    assert config.trace_calls
    assert not config.trace_lines
    assert not config.trace_variables
    assert not config.record_inner_portals

    return


def test_explicit_construction_preserves_values() -> None:
    """
        Verify explicit construction with all flags set preserves values.
    """
    config = TraceConfiguration(
        trace_calls=False,
        trace_lines=True,
        trace_variables=True,
        record_inner_portals=True,
    )

    assert not config.trace_calls
    assert config.trace_lines
    assert config.trace_variables
    assert config.record_inner_portals

    return


def test_properties_are_read_only() -> None:
    """
        Verify that setting properties raises AttributeError.
    """
    config = TraceConfiguration()

    raised = False
    try:
        config.trace_calls = False
    except AttributeError:
        raised = True
    assert raised

    raised = False
    try:
        config.trace_lines = True
    except AttributeError:
        raised = True
    assert raised

    raised = False
    try:
        config.trace_variables = True
    except AttributeError:
        raised = True
    assert raised

    raised = False
    try:
        config.record_inner_portals = True
    except AttributeError:
        raised = True
    assert raised

    return


def test_as_dict_returns_correct_dictionary() -> None:
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
    assert result == expected

    return


def test_from_dict_round_trips_with_as_dict() -> None:
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

    assert restored.trace_calls == original.trace_calls
    assert restored.trace_lines == original.trace_lines
    assert restored.trace_variables == original.trace_variables
    assert restored.record_inner_portals == original.record_inner_portals

    return


def test_from_dict_with_partial_data_uses_defaults() -> None:
    """
        Verify from_dict() with partial data uses defaults for missing keys.
    """
    partial_data = {"trace_lines": True}
    config = TraceConfiguration.from_dict(partial_data)

    assert config.trace_calls  # default
    assert config.trace_lines  # provided
    assert not config.trace_variables  # default
    assert not config.record_inner_portals  # default

    return


def test_default_constant_has_expected_values() -> None:
    """
        Verify DEFAULT_TRACE_CONFIGURATION has the expected default values.
    """
    assert DEFAULT_TRACE_CONFIGURATION.trace_calls
    assert not DEFAULT_TRACE_CONFIGURATION.trace_lines
    assert not DEFAULT_TRACE_CONFIGURATION.trace_variables
    assert not DEFAULT_TRACE_CONFIGURATION.record_inner_portals

    return
