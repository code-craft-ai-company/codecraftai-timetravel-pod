"""
    Provides the thread-safe portal registry for managing portal activation state.

    This module contains the :class:`PortalRegistry` class which tracks which
    named portals are activated for tracing, and provides a process-wide
    singleton accessor.
"""

import threading


class PortalRegistry:
    """
        Thread-safe registry of portal names and their activation state.

        Uses a ``threading.Lock`` to protect the internal dictionary from
        concurrent access.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._portals: dict = {}
        return

    def activate_portal(self, name: str, expression: str = None, once: bool = False) -> None:
        """
            Activate a single portal by name.

            :param name: The portal name to activate.
            :param expression: Optional Python expression to dynamically determine tracing.
            :param once: If True, trace exactly once and deactivate the portal.
        """
        with self._lock:
            self._portals[name] = {
                "active": True,
                "expression": expression,
                "once": once,
            }
        return

    def deactivate_portal(self, name: str) -> None:
        """
            Deactivate a single portal by name.

            :param name: The portal name to deactivate.
        """
        with self._lock:
            if name in self._portals:
                self._portals[name]["active"] = False
            else:
                self._portals[name] = {"active": False, "expression": None, "once": False}
        return

    def is_portal_active(self, name: str) -> bool:
        """
            Check whether a portal is active.

            Returns False for unknown portal names.

            :param name: The portal name to check.

            :returns: True if the portal is active, False otherwise.
        """
        with self._lock:
            portal_info = self._portals.get(name, {})
            rtnval = portal_info.get("active", False)
        return rtnval

    def get_portal_info(self, name: str) -> dict:
        """
            Return a portal's dictionary info.

            :param name: The portal name.

            :returns: The portal info dict, or an empty dict if not configured.
        """
        with self._lock:
            rtnval = self._portals.get(name, {})
            # Make a copy to avoid exposing the internal structure
            rtnval = dict(rtnval)
        return rtnval

    def activate_portals(self, names: list) -> None:
        """
            Activate multiple portals at once.

            :param names: A list of portal names to activate.
        """
        with self._lock:
            for name in names:
                self._portals[name] = {
                    "active": True,
                    "expression": None,
                    "once": False,
                }
        return

    def deactivate_all(self) -> None:
        """
            Deactivate all registered portals.
        """
        with self._lock:
            for name in self._portals:
                self._portals[name]["active"] = False
        return

    def list_portals(self) -> list:
        """
            List all registered portals and their activation state.

            :returns: A list of dicts with 'name', 'active', 'expression', and 'once' keys.
        """
        with self._lock:
            rtnval = [
                {
                    "name": name,
                    "active": info.get("active", False),
                    "expression": info.get("expression", None),
                    "once": info.get("once", False)
                }
                for name, info in self._portals.items()
            ]
        return rtnval


_portal_registry = PortalRegistry()


def get_portal_registry() -> PortalRegistry:
    """
        Return the process-wide singleton PortalRegistry instance.

        :returns: The singleton PortalRegistry.
    """
    rtnval = _portal_registry
    return rtnval
