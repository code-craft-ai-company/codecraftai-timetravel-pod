from automojo.timetravel.pod.portalregistry import get_portal_registry

def test():
    r = get_portal_registry()
    r.activate_portal("test1", expression="x>1", once=True)
    assert r.is_portal_active("test1")
    assert r.get_portal_info("test1")["expression"] == "x>1"
    assert r.get_portal_info("test1")["once"] == True

    r.deactivate_portal("test1")
    assert not r.is_portal_active("test1")
    assert not r.list_portals()[0]["active"]

    print("pass")

if __name__ == "__main__":
    test()
