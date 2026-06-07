# F6.3 — Portal-Scoped Filtering: Design

## Technical Design

### Module Location
`source/packages/ccai/timetravel/pod/portalfilter.py`

### Function Design

```python
from ccai.timetravel.pod.traceevents import (
    TraceEvent, PortalEnterEvent, PortalExitEvent, EventType,
)


def filter_by_portal(events: list[TraceEvent], portal_name: str) -> list[TraceEvent]:
    """Filter events to only those occurring within the named portal scope.

    Handles multiple enter/exit pairs for the same portal name.
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
```

### Design Rationale

- A stateless function is used rather than a class because filtering is a single-pass
  operation with no persistent state.
- `isinstance` checks are used for portal boundary detection because they are the most
  readable and reliable approach.
- The function handles multiple enter/exit pairs naturally by toggling the `inside` flag.
- Events are returned in their original order (the input should already be sorted).
