===============================
Automation Mojo TimeTravel Pod
===============================

The ``automojo-timetravel-pod`` is a Python package that provides time-travel debugging capabilities to applications. It introduces the concept of "named portals" that enable dynamic activation of different scopes of time-travel debugging. A developer places a portal in the form of a ``with`` scope into the code, associated with a uniquely named portal. When a thread enters the scope of the portal and the portal was activated by name early in the program's startup, time-travel debugging is activated for that thread for the duration of the portal scope. This mechanism allows applications to run at full performance when portals are inactive while still capturing debug traces at runtime — and portals can be turned on and off at any time without restarting the application.

Highlights
==========

- Named-portal activation model with ``TimeTravelGateway``, ``TimeTravelPortal``, and a thread-safe portal registry.
- Trace recording engine with ``TraceHookManager`` (wrapping ``sys.settrace``), a ``TraceRecorder`` ABC, a hybrid ``struct``+``pickle`` serialization format, and a buffered writer.
- Stream backends for file, TCP, and Unix-domain-socket destinations, resolved through a URI-scheme registry.
- Remote control interface (TCP, JSON-lines) with token-based authentication, service registration, and heartbeat support.
- Configuration-driven startup API and ``@trace_portal("name")`` convenience decorator.

Repository Structure
====================

- ``development/`` - Runtime environment scripts.
- ``repository-setup/`` - Repository homing and setup scripts.
- ``source/packages/`` - Package source code.
- ``source/tests/`` - ``unittest``-based tests.
- ``specs/`` - Requirements and design documentation organised by feature layer.
- ``userguide/`` - Standards, conventions, and documentation.

Environment Setup
=================

When working in a Codex container:

.. code-block:: bash

   ./development/setup-agent-container

For local development:

.. code-block:: bash

   ./repository-setup/rehome-repository
   ./development/setup-envrionment

Running Tests
=============

Activate the virtual environment:

.. code-block:: bash

   source .venv/bin/activate

Run ``unittest`` tests:

.. code-block:: bash

   python -m unittest discover -s source/tests -p "test_*.py"

Standards and Conventions
=========================

- Naming conventions: ``userguide/10-02-naming-conventions.rst``
- Code organization: ``userguide/10-01-code-organization.rst``
- Coding standards: ``userguide/10-00-coding-standards.rst``

Additional Resources
====================

- User guide entry point: ``userguide/userguide.rst``
- Feature specifications under ``specs/`` are organised by layer (``0-*`` core primitives, ``1-*`` trace recording, ``2-*`` stream backends, and so on).
