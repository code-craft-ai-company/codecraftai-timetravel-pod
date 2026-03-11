# F5.4 — Health and Heartbeat: Tasks

## Implementation Tasks

- [x] 1. Create the module `source/packages/automojo/timetravel/pod/remote/heartbeat.py`
- [x] 2. Implement `HeartbeatSender.__init__` with service URL, credential, instance ID, interval
- [x] 3. Implement `start()` and `stop()` with daemon thread and `threading.Event`
- [x] 4. Implement `_heartbeat_loop()` and `_send_heartbeat()`

## Testing Tasks

- [x] 5. Create test file `source/tests/automojo/timetravel/pod/remote/test_heartbeat.py`
- [x] 6. Test: `start()` begins sending heartbeats (using mock HTTP server)
- [x] 7. Test: `stop()` terminates the heartbeat thread
- [x] 8. Test: failed heartbeat does not crash, logs a warning
- [x] 9. Test: heartbeat payload contains instance_id and timestamp
