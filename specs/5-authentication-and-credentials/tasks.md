# F5.2 — Authentication and Credentials: Tasks

## Implementation Tasks

- [x] 1. Create the module `source/packages/ccai/timetravel/pod/remote/auth.py`
- [x] 2. Implement `verify_credential()` with `hmac.compare_digest`
- [x] 3. Integrate `verify_credential` into `RemoteControlServer._dispatch`

## Testing Tasks

- [x] 4. Create test file `source/tests/ccai/timetravel/pod/remote/test_auth.py`
- [x] 5. Test: matching credential returns `True`
- [x] 6. Test: non-matching credential returns `False`
- [x] 7. Test: `None` expected credential allows all (returns `True`)
- [x] 8. Test: `None` provided credential with non-None expected returns `False`
