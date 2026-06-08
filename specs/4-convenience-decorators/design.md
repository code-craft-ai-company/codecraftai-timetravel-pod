# F4.2 — Convenience Decorators: Design

## Technical Design

### Module Location
`source/packages/ccai/timetravel/pod/decorators.py`

### trace_portal Decorator

```python
import functools
import inspect
from ccai.timetravel.pod.portal import TimeTravelPortal


def trace_portal(name: str):
    """Decorator that wraps a function body in a TimeTravelPortal."""

    def decorator(func):
        if inspect.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                with TimeTravelPortal(name):
                    rtnval = await func(*args, **kwargs)
                return rtnval
            return async_wrapper
        else:
            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                with TimeTravelPortal(name):
                    rtnval = func(*args, **kwargs)
                return rtnval
            return sync_wrapper

    return decorator
```

### Gateway Factory

```python
from ccai.timetravel.pod.gateway import TimeTravelGateway
from ccai.timetravel.pod.traceconfiguration import TraceConfiguration


def create_gateway(
    trace_calls: bool = True,
    trace_lines: bool = False,
    trace_variables: bool = False,
    record_inner_portals: bool = False,
    backend_uri: str | None = None,
) -> TimeTravelGateway:
    """Create a TimeTravelGateway with common defaults."""
    configuration = TraceConfiguration(
        trace_calls=trace_calls,
        trace_lines=trace_lines,
        trace_variables=trace_variables,
        record_inner_portals=record_inner_portals,
    )
    rtnval = TimeTravelGateway(
        configuration=configuration,
        backend_uri=backend_uri,
    )
    return rtnval
```

### Design Rationale

- `functools.wraps` preserves the original function's metadata for introspection.
- Async detection via `inspect.iscoroutinefunction` ensures the decorator works
  transparently with both sync and async code.
- The `create_gateway` factory flattens the most common configuration parameters
  into keyword arguments, avoiding the need to construct `TraceConfiguration` manually.
