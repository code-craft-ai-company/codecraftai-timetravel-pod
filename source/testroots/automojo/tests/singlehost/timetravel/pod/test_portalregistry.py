"""
    Tests for the F3.3 Portal Registry module.
"""

import threading

from automojo.timetravel.pod.portalregistry import PortalRegistry
from automojo.timetravel.pod.portalregistry import get_portal_registry


def test_activate_and_is_active_round_trip() -> None:
    """
        Verify activate_portal and is_portal_active round-trip.
    """
    registry = PortalRegistry()

    registry.activate_portal("test_portal")

    assert registry.is_portal_active("test_portal")

    return


def test_deactivate_sets_portal_inactive() -> None:
    """
        Verify deactivate_portal sets portal to inactive.
    """
    registry = PortalRegistry()

    registry.activate_portal("test_portal")
    registry.deactivate_portal("test_portal")

    assert not registry.is_portal_active("test_portal")

    return


def test_unknown_portal_returns_false() -> None:
    """
        Verify unknown portal name returns False.
    """
    registry = PortalRegistry()

    assert not registry.is_portal_active("nonexistent")

    return


def test_activate_portals_bulk() -> None:
    """
        Verify activate_portals bulk activates multiple portals.
    """
    registry = PortalRegistry()

    registry.activate_portals(["portal_a", "portal_b", "portal_c"])

    assert registry.is_portal_active("portal_a")
    assert registry.is_portal_active("portal_b")
    assert registry.is_portal_active("portal_c")

    return


def test_deactivate_all() -> None:
    """
        Verify deactivate_all deactivates all portals.
    """
    registry = PortalRegistry()

    registry.activate_portals(["portal_a", "portal_b"])
    registry.deactivate_all()

    assert not registry.is_portal_active("portal_a")
    assert not registry.is_portal_active("portal_b")

    return


def test_list_portals_returns_correct_pairs() -> None:
    """
        Verify list_portals returns correct name/active pairs.
    """
    registry = PortalRegistry()

    registry.activate_portal("active_one")
    registry.activate_portal("inactive_one")
    registry.deactivate_portal("inactive_one")

    portals = registry.list_portals()
    portal_dict = {p["name"]: p["active"] for p in portals}

    assert portal_dict["active_one"]
    assert not portal_dict["inactive_one"]

    return


def test_concurrent_access_does_not_corrupt_state() -> None:
    """
        Verify concurrent access from multiple threads does not corrupt state.
    """
    registry = PortalRegistry()
    errors = []

    def activate_many(start_index):
        try:
            for i in range(100):
                name = f"portal_{start_index}_{i}"
                registry.activate_portal(name)
                is_active = registry.is_portal_active(name)
                if not is_active:
                    errors.append(f"{name} should be active")
        except Exception as ex:
            errors.append(str(ex))
        return

    threads = []
    for t in range(4):
        thread = threading.Thread(target=activate_many, args=(t,))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    assert len(errors) == 0, f"Errors during concurrent access: {errors}"

    # Verify all portals are registered
    portals = registry.list_portals()
    assert len(portals) == 400

    return


def test_returns_same_instance() -> None:
    """
        Verify get_portal_registry returns the same instance on repeated calls.
    """
    reg_a = get_portal_registry()
    reg_b = get_portal_registry()

    assert reg_a is reg_b

    return
