"""
    Provides portal-scoped event filtering.

    This module contains the :func:`filter_by_portal` function which extracts
    events that occur within the scope of a named portal's enter/exit markers.
"""

from automojo.timetravel.pod.traceevents import PortalEnterEvent
from automojo.timetravel.pod.traceevents import PortalExitEvent


def filter_by_portal(events: list, portal_name: str) -> list:
    """
        Filter events to only those occurring within the named portal scope.

        Handles multiple enter/exit pairs for the same portal name, returning
        events from all occurrences in their original chronological order.

        :param events: A list of TraceEvent objects (should be pre-sorted).
        :param portal_name: The portal name to filter by.

        :returns: A list of TraceEvent objects within the portal scope.
    """
    rtnval = []
    inside = False

    for event in events:
        if isinstance(event, PortalEnterEvent) and event.portal_name == portal_name:
            inside = True
            rtnval.append(event)
            continue

        if isinstance(event, PortalExitEvent) and event.portal_name == portal_name:
            rtnval.append(event)
            inside = False
            continue

        if inside:
            rtnval.append(event)

    return rtnval
