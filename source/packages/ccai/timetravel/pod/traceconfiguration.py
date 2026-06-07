"""
    Provides the immutable trace configuration model for the time travel pod.

    This module contains the :class:`TraceConfiguration` class which controls
    trace granularity (calls, lines, variables) and whether inner portal
    boundaries are recorded.
"""


class TraceConfiguration:
    """
        Immutable configuration controlling trace granularity and behavior.

        Uses ``__slots__`` with private backing fields and read-only properties
        to enforce immutability. To change configuration, create a new instance.
    """

    __slots__ = ("_trace_calls", "_trace_lines", "_trace_variables", "_record_inner_portals")

    def __init__(
        self,
        trace_calls: bool = True,
        trace_lines: bool = False,
        trace_variables: bool = False,
        record_inner_portals: bool = False,
    ) -> None:
        self._trace_calls = trace_calls
        self._trace_lines = trace_lines
        self._trace_variables = trace_variables
        self._record_inner_portals = record_inner_portals
        return

    @property
    def trace_calls(self) -> bool:
        """
            Whether function call and return events are traced.
        """
        rtnval = self._trace_calls
        return rtnval

    @property
    def trace_lines(self) -> bool:
        """
            Whether line execution events are traced.
        """
        rtnval = self._trace_lines
        return rtnval

    @property
    def trace_variables(self) -> bool:
        """
            Whether variable snapshot events are captured at each traced line.
        """
        rtnval = self._trace_variables
        return rtnval

    @property
    def record_inner_portals(self) -> bool:
        """
            Whether nested portal enter/exit events are recorded as annotations.
        """
        rtnval = self._record_inner_portals
        return rtnval

    def as_dict(self) -> dict:
        """
            Convert the configuration to a dictionary.

            :returns: A dictionary representation of the configuration.
        """
        rtnval = {
            "trace_calls": self._trace_calls,
            "trace_lines": self._trace_lines,
            "trace_variables": self._trace_variables,
            "record_inner_portals": self._record_inner_portals,
        }
        return rtnval

    @classmethod
    def from_dict(cls, data: dict) -> "TraceConfiguration":
        """
            Create a TraceConfiguration from a dictionary.

            Missing keys use the constructor defaults.

            :param data: A dictionary of configuration values.

            :returns: A new TraceConfiguration instance.
        """
        rtnval = cls(
            trace_calls=data.get("trace_calls", True),
            trace_lines=data.get("trace_lines", False),
            trace_variables=data.get("trace_variables", False),
            record_inner_portals=data.get("record_inner_portals", False),
        )
        return rtnval


DEFAULT_TRACE_CONFIGURATION = TraceConfiguration()
