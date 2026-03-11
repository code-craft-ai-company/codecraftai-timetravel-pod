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

    def activate_portal(self, name: str) -> None:
        """
            Activate a single portal by name.

            :param name: The portal name to activate.
        """
        with self._lock:
            self._portals[name] = True
        return

    def deactivate_portal(self, name: str) -> None:
        """
            Deactivate a single portal by name.

            :param name: The portal name to deactivate.
        """
        with self._lock:
            self._portals[name] = False
        return

    def is_portal_active(self, name: str) -> bool:
        """
            Check whether a portal is active.

            Returns False for unknown portal names.

            :param name: The portal name to check.

            :returns: True if the portal is active, False otherwise.
        """
        with self._lock:
            rtnval = self._portals.get(name, False)
        return rtnval

    def activate_portals(self, names: list) -> None:
        """
            Activate multiple portals at once.

            :param names: A list of portal names to activate.
        """
        with self._lock:
            for name in names:
                self._portals[name] = True
        return

    def deactivate_all(self) -> None:
        """
            Deactivate all registered portals.
        """
        with self._lock:
            for name in self._portals:
                self._portals[name] = False
        return

    def list_portals(self) -> list:
        """
            List all registered portals and their activation state.

            :returns: A list of dicts with 'name' and 'active' keys.
        """
        with self._lock:
            rtnval = [
                {"name": name, "active": active}
                for name, active in self._portals.items()
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
