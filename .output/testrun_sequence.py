"""
    ======================================= CODE GENERATED - DO NOT EDIT =======================================
    This is a code generated execution sequence document, do not manually edit this document.  The 'testbase'
    test framework generates this document in order to layout the test run scopes, parameter creations, and
    test calls in a user ledgible way which is easy to read and also to debug.
"""

__traceback_format_policy__ = "Brief"

import logging

from ccai.xmodules.xlogging.enhancedloggers import getEnhancedLogger

from ccai.testbase.constraints import ConstraintsCatalog

logger = getEnhancedLogger()

constraints_catalog = ConstraintsCatalog()



def session(sequencer):
    """
    This is the entry point for the test run sequence document.
    """

    with sequencer.enter_session_scope_context() as ssc:


        scope_ccai(sequencer)

    return

def scope_ccai(sequencer):
    """
    This is the entry point for the 'ccai' test scope.
    """

    with sequencer.enter_module_scope_context("ccai") as msc:
        scope_ccai_tests(sequencer)

    return

def scope_ccai_tests(sequencer):
    """
    This is the entry point for the 'ccai_tests' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests") as msc:
        scope_ccai_tests_singlehost(sequencer)

    return

def scope_ccai_tests_singlehost(sequencer):
    """
    This is the entry point for the 'ccai_tests_singlehost' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.singlehost") as msc:
        scope_ccai_tests_singlehost_timetravel(sequencer)

    return

def scope_ccai_tests_singlehost_timetravel(sequencer):
    """
    This is the entry point for the 'ccai_tests_singlehost_timetravel' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.singlehost.timetravel") as msc:
        scope_ccai_tests_singlehost_timetravel_pod(sequencer)

    return

def scope_ccai_tests_singlehost_timetravel_pod(sequencer):
    """
    This is the entry point for the 'ccai_tests_singlehost_timetravel_pod' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.singlehost.timetravel.pod") as msc:
        scope_ccai_tests_singlehost_timetravel_pod_backends(sequencer)
        scope_ccai_tests_singlehost_timetravel_pod_remote(sequencer)
        scope_ccai_tests_singlehost_timetravel_pod_test_bufferedwriter(sequencer)
        scope_ccai_tests_singlehost_timetravel_pod_test_configuration(sequencer)
        scope_ccai_tests_singlehost_timetravel_pod_test_decorators(sequencer)
        scope_ccai_tests_singlehost_timetravel_pod_test_gateway(sequencer)
        scope_ccai_tests_singlehost_timetravel_pod_test_portal(sequencer)
        scope_ccai_tests_singlehost_timetravel_pod_test_portal_expression(sequencer)
        scope_ccai_tests_singlehost_timetravel_pod_test_portalfilter(sequencer)
        scope_ccai_tests_singlehost_timetravel_pod_test_portalregistry(sequencer)
        scope_ccai_tests_singlehost_timetravel_pod_test_reader(sequencer)
        scope_ccai_tests_singlehost_timetravel_pod_test_timeline(sequencer)
        scope_ccai_tests_singlehost_timetravel_pod_test_traceclock(sequencer)
        scope_ccai_tests_singlehost_timetravel_pod_test_traceconfiguration(sequencer)
        scope_ccai_tests_singlehost_timetravel_pod_test_traceevents(sequencer)
        scope_ccai_tests_singlehost_timetravel_pod_test_tracehookmanager(sequencer)
        scope_ccai_tests_singlehost_timetravel_pod_test_tracerecorder(sequencer)
        scope_ccai_tests_singlehost_timetravel_pod_test_traceserializer(sequencer)
        scope_ccai_tests_singlehost_timetravel_pod_test_tracingstate(sequencer)

    return

def scope_ccai_tests_singlehost_timetravel_pod_backends(sequencer):
    """
    This is the entry point for the 'ccai_tests_singlehost_timetravel_pod_backends' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.singlehost.timetravel.pod.backends") as msc:
        scope_ccai_tests_singlehost_timetravel_pod_backends_test_filebackend(sequencer)
        scope_ccai_tests_singlehost_timetravel_pod_backends_test_registry(sequencer)
        scope_ccai_tests_singlehost_timetravel_pod_backends_test_tcpbackend(sequencer)
        scope_ccai_tests_singlehost_timetravel_pod_backends_test_unixbackend(sequencer)

    return

def scope_ccai_tests_singlehost_timetravel_pod_backends_test_filebackend(sequencer):
    """
    This is the entry point for the 'ccai_tests_singlehost_timetravel_pod_backends_test_filebackend' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.singlehost.timetravel.pod.backends.test_filebackend") as msc:
        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.backends.test_filebackend#test_append_mode_preserves_existing_data ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.backends.test_filebackend#test_append_mode_preserves_existing_data"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.backends.test_filebackend import test_append_mode_preserves_existing_data

            test_append_mode_preserves_existing_data()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.backends.test_filebackend#test_close_is_idempotent ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.backends.test_filebackend#test_close_is_idempotent"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.backends.test_filebackend import test_close_is_idempotent

            test_close_is_idempotent()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.backends.test_filebackend#test_creates_parent_directories ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.backends.test_filebackend#test_creates_parent_directories"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.backends.test_filebackend import test_creates_parent_directories

            test_creates_parent_directories()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.backends.test_filebackend#test_default_max_file_size_constant ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.backends.test_filebackend#test_default_max_file_size_constant"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.backends.test_filebackend import test_default_max_file_size_constant

            test_default_max_file_size_constant()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.backends.test_filebackend#test_multiple_writes_accumulate ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.backends.test_filebackend#test_multiple_writes_accumulate"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.backends.test_filebackend import test_multiple_writes_accumulate

            test_multiple_writes_accumulate()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.backends.test_filebackend#test_overwrite_mode_replaces_existing_data ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.backends.test_filebackend#test_overwrite_mode_replaces_existing_data"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.backends.test_filebackend import test_overwrite_mode_replaces_existing_data

            test_overwrite_mode_replaces_existing_data()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.backends.test_filebackend#test_rotation_creates_new_files ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.backends.test_filebackend#test_rotation_creates_new_files"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.backends.test_filebackend import test_rotation_creates_new_files

            test_rotation_creates_new_files()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.backends.test_filebackend#test_write_creates_file_with_data ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.backends.test_filebackend#test_write_creates_file_with_data"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.backends.test_filebackend import test_write_creates_file_with_data

            test_write_creates_file_with_data()


    return

def scope_ccai_tests_singlehost_timetravel_pod_backends_test_registry(sequencer):
    """
    This is the entry point for the 'ccai_tests_singlehost_timetravel_pod_backends_test_registry' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.singlehost.timetravel.pod.backends.test_registry") as msc:
        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.backends.test_registry#test_default_registry_has_file_tcp_unix_schemes ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.backends.test_registry#test_default_registry_has_file_tcp_unix_schemes"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.backends.test_registry import test_default_registry_has_file_tcp_unix_schemes

            test_default_registry_has_file_tcp_unix_schemes()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.backends.test_registry#test_file_scheme_creates_file_backend ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.backends.test_registry#test_file_scheme_creates_file_backend"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.backends.test_registry import test_file_scheme_creates_file_backend

            test_file_scheme_creates_file_backend()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.backends.test_registry#test_register_and_create_backend ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.backends.test_registry#test_register_and_create_backend"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.backends.test_registry import test_register_and_create_backend

            test_register_and_create_backend()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.backends.test_registry#test_registered_schemes_returns_scheme_list ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.backends.test_registry#test_registered_schemes_returns_scheme_list"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.backends.test_registry import test_registered_schemes_returns_scheme_list

            test_registered_schemes_returns_scheme_list()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.backends.test_registry#test_unknown_scheme_raises_value_error ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.backends.test_registry#test_unknown_scheme_raises_value_error"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.backends.test_registry import test_unknown_scheme_raises_value_error

            test_unknown_scheme_raises_value_error()


    return

def scope_ccai_tests_singlehost_timetravel_pod_backends_test_tcpbackend(sequencer):
    """
    This is the entry point for the 'ccai_tests_singlehost_timetravel_pod_backends_test_tcpbackend' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.singlehost.timetravel.pod.backends.test_tcpbackend") as msc:
        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.backends.test_tcpbackend#test_close_without_error ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.backends.test_tcpbackend#test_close_without_error"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.backends.test_tcpbackend import test_close_without_error

            test_close_without_error()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.backends.test_tcpbackend#test_connection_refused_raises_error ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.backends.test_tcpbackend#test_connection_refused_raises_error"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.backends.test_tcpbackend import test_connection_refused_raises_error

            test_connection_refused_raises_error()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.backends.test_tcpbackend#test_multiple_writes_accumulate ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.backends.test_tcpbackend#test_multiple_writes_accumulate"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.backends.test_tcpbackend import test_multiple_writes_accumulate

            test_multiple_writes_accumulate()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.backends.test_tcpbackend#test_write_sends_data_to_server ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.backends.test_tcpbackend#test_write_sends_data_to_server"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.backends.test_tcpbackend import test_write_sends_data_to_server

            test_write_sends_data_to_server()


    return

def scope_ccai_tests_singlehost_timetravel_pod_backends_test_unixbackend(sequencer):
    """
    This is the entry point for the 'ccai_tests_singlehost_timetravel_pod_backends_test_unixbackend' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.singlehost.timetravel.pod.backends.test_unixbackend") as msc:
        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.backends.test_unixbackend#test_close_without_error ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.backends.test_unixbackend#test_close_without_error"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.backends.test_unixbackend import test_close_without_error

            test_close_without_error()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.backends.test_unixbackend#test_connection_to_nonexistent_socket_raises_error ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.backends.test_unixbackend#test_connection_to_nonexistent_socket_raises_error"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.backends.test_unixbackend import test_connection_to_nonexistent_socket_raises_error

            test_connection_to_nonexistent_socket_raises_error()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.backends.test_unixbackend#test_multiple_writes_accumulate ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.backends.test_unixbackend#test_multiple_writes_accumulate"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.backends.test_unixbackend import test_multiple_writes_accumulate

            test_multiple_writes_accumulate()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.backends.test_unixbackend#test_write_sends_data_to_server ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.backends.test_unixbackend#test_write_sends_data_to_server"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.backends.test_unixbackend import test_write_sends_data_to_server

            test_write_sends_data_to_server()


    return

def scope_ccai_tests_singlehost_timetravel_pod_remote(sequencer):
    """
    This is the entry point for the 'ccai_tests_singlehost_timetravel_pod_remote' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.singlehost.timetravel.pod.remote") as msc:
        scope_ccai_tests_singlehost_timetravel_pod_remote_test_auth(sequencer)
        scope_ccai_tests_singlehost_timetravel_pod_remote_test_heartbeat(sequencer)
        scope_ccai_tests_singlehost_timetravel_pod_remote_test_mcpserver(sequencer)
        scope_ccai_tests_singlehost_timetravel_pod_remote_test_registration(sequencer)
        scope_ccai_tests_singlehost_timetravel_pod_remote_test_server(sequencer)

    return

def scope_ccai_tests_singlehost_timetravel_pod_remote_test_auth(sequencer):
    """
    This is the entry point for the 'ccai_tests_singlehost_timetravel_pod_remote_test_auth' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.singlehost.timetravel.pod.remote.test_auth") as msc:
        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.remote.test_auth#test_matching_credential_returns_true ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.remote.test_auth#test_matching_credential_returns_true"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.remote.test_auth import test_matching_credential_returns_true

            test_matching_credential_returns_true()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.remote.test_auth#test_non_matching_credential_returns_false ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.remote.test_auth#test_non_matching_credential_returns_false"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.remote.test_auth import test_non_matching_credential_returns_false

            test_non_matching_credential_returns_false()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.remote.test_auth#test_none_expected_denies ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.remote.test_auth#test_none_expected_denies"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.remote.test_auth import test_none_expected_denies

            test_none_expected_denies()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.remote.test_auth#test_none_expected_denies_none_provided ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.remote.test_auth#test_none_expected_denies_none_provided"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.remote.test_auth import test_none_expected_denies_none_provided

            test_none_expected_denies_none_provided()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.remote.test_auth#test_none_provided_with_expected_returns_false ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.remote.test_auth#test_none_provided_with_expected_returns_false"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.remote.test_auth import test_none_provided_with_expected_returns_false

            test_none_provided_with_expected_returns_false()


    return

def scope_ccai_tests_singlehost_timetravel_pod_remote_test_heartbeat(sequencer):
    """
    This is the entry point for the 'ccai_tests_singlehost_timetravel_pod_remote_test_heartbeat' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.singlehost.timetravel.pod.remote.test_heartbeat") as msc:
        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.remote.test_heartbeat#test_default_heartbeat_interval_constant ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.remote.test_heartbeat#test_default_heartbeat_interval_constant"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.remote.test_heartbeat import test_default_heartbeat_interval_constant

            test_default_heartbeat_interval_constant()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.remote.test_heartbeat#test_failed_heartbeat_does_not_crash ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.remote.test_heartbeat#test_failed_heartbeat_does_not_crash"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.remote.test_heartbeat import test_failed_heartbeat_does_not_crash

            test_failed_heartbeat_does_not_crash()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.remote.test_heartbeat#test_heartbeat_payload_contains_required_fields ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.remote.test_heartbeat#test_heartbeat_payload_contains_required_fields"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.remote.test_heartbeat import test_heartbeat_payload_contains_required_fields

            test_heartbeat_payload_contains_required_fields()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.remote.test_heartbeat#test_start_sends_heartbeats ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.remote.test_heartbeat#test_start_sends_heartbeats"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.remote.test_heartbeat import test_start_sends_heartbeats

            test_start_sends_heartbeats()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.remote.test_heartbeat#test_stop_terminates_heartbeat_thread ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.remote.test_heartbeat#test_stop_terminates_heartbeat_thread"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.remote.test_heartbeat import test_stop_terminates_heartbeat_thread

            test_stop_terminates_heartbeat_thread()


    return

def scope_ccai_tests_singlehost_timetravel_pod_remote_test_mcpserver(sequencer):
    """
    This is the entry point for the 'ccai_tests_singlehost_timetravel_pod_remote_test_mcpserver' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.singlehost.timetravel.pod.remote.test_mcpserver") as msc:
        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.remote.test_mcpserver#test_close_session ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.remote.test_mcpserver#test_close_session"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.remote.test_mcpserver import test_close_session

            test_close_session()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.remote.test_mcpserver#test_create_session ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.remote.test_mcpserver#test_create_session"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.remote.test_mcpserver import test_create_session

            test_create_session()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.remote.test_mcpserver#test_list_captures_empty ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.remote.test_mcpserver#test_list_captures_empty"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.remote.test_mcpserver import test_list_captures_empty

            test_list_captures_empty()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.remote.test_mcpserver#test_renew_session ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.remote.test_mcpserver#test_renew_session"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.remote.test_mcpserver import test_renew_session

            test_renew_session()


    return

def scope_ccai_tests_singlehost_timetravel_pod_remote_test_registration(sequencer):
    """
    This is the entry point for the 'ccai_tests_singlehost_timetravel_pod_remote_test_registration' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.singlehost.timetravel.pod.remote.test_registration") as msc:
        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.remote.test_registration#test_instance_id_is_valid_uuid ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.remote.test_registration#test_instance_id_is_valid_uuid"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.remote.test_registration import test_instance_id_is_valid_uuid

            test_instance_id_is_valid_uuid()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.remote.test_registration#test_register_sends_correct_payload ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.remote.test_registration#test_register_sends_correct_payload"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.remote.test_registration import test_register_sends_correct_payload

            test_register_sends_correct_payload()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.remote.test_registration#test_registration_failure_returns_false ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.remote.test_registration#test_registration_failure_returns_false"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.remote.test_registration import test_registration_failure_returns_false

            test_registration_failure_returns_false()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.remote.test_registration#test_unregister_is_noop_if_not_registered ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.remote.test_registration#test_unregister_is_noop_if_not_registered"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.remote.test_registration import test_unregister_is_noop_if_not_registered

            test_unregister_is_noop_if_not_registered()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.remote.test_registration#test_unregister_sends_correct_payload ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.remote.test_registration#test_unregister_sends_correct_payload"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.remote.test_registration import test_unregister_sends_correct_payload

            test_unregister_sends_correct_payload()


    return

def scope_ccai_tests_singlehost_timetravel_pod_remote_test_server(sequencer):
    """
    This is the entry point for the 'ccai_tests_singlehost_timetravel_pod_remote_test_server' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.singlehost.timetravel.pod.remote.test_server") as msc:
        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.remote.test_server#test_activate_portal_command ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.remote.test_server#test_activate_portal_command"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.remote.test_server import test_activate_portal_command

            test_activate_portal_command()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.remote.test_server#test_auth_accepts_correct_token ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.remote.test_server#test_auth_accepts_correct_token"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.remote.test_server import test_auth_accepts_correct_token

            test_auth_accepts_correct_token()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.remote.test_server#test_auth_rejects_wrong_token ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.remote.test_server#test_auth_rejects_wrong_token"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.remote.test_server import test_auth_rejects_wrong_token

            test_auth_rejects_wrong_token()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.remote.test_server#test_deactivate_portal_command ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.remote.test_server#test_deactivate_portal_command"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.remote.test_server import test_deactivate_portal_command

            test_deactivate_portal_command()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.remote.test_server#test_list_portals_returns_portal_data ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.remote.test_server#test_list_portals_returns_portal_data"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.remote.test_server import test_list_portals_returns_portal_data

            test_list_portals_returns_portal_data()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.remote.test_server#test_server_accepts_connections ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.remote.test_server#test_server_accepts_connections"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.remote.test_server import test_server_accepts_connections

            test_server_accepts_connections()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.remote.test_server#test_stop_cleanly_shuts_down ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.remote.test_server#test_stop_cleanly_shuts_down"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.remote.test_server import test_stop_cleanly_shuts_down

            test_stop_cleanly_shuts_down()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.remote.test_server#test_unknown_command_returns_error ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.remote.test_server#test_unknown_command_returns_error"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.remote.test_server import test_unknown_command_returns_error

            test_unknown_command_returns_error()


    return

def scope_ccai_tests_singlehost_timetravel_pod_test_bufferedwriter(sequencer):
    """
    This is the entry point for the 'ccai_tests_singlehost_timetravel_pod_test_bufferedwriter' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.singlehost.timetravel.pod.test_bufferedwriter") as msc:
        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_bufferedwriter#test_close_flushes_then_closes_stream ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_bufferedwriter#test_close_flushes_then_closes_stream"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_bufferedwriter import test_close_flushes_then_closes_stream

            test_close_flushes_then_closes_stream()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_bufferedwriter#test_custom_buffer_size_is_respected ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_bufferedwriter#test_custom_buffer_size_is_respected"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_bufferedwriter import test_custom_buffer_size_is_respected

            test_custom_buffer_size_is_respected()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_bufferedwriter#test_default_buffer_size_constant ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_bufferedwriter#test_default_buffer_size_constant"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_bufferedwriter import test_default_buffer_size_constant

            test_default_buffer_size_constant()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_bufferedwriter#test_exceeding_buffer_triggers_auto_flush ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_bufferedwriter#test_exceeding_buffer_triggers_auto_flush"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_bufferedwriter import test_exceeding_buffer_triggers_auto_flush

            test_exceeding_buffer_triggers_auto_flush()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_bufferedwriter#test_flush_writes_buffered_data_immediately ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_bufferedwriter#test_flush_writes_buffered_data_immediately"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_bufferedwriter import test_flush_writes_buffered_data_immediately

            test_flush_writes_buffered_data_immediately()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_bufferedwriter#test_multiple_small_writes_accumulate ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_bufferedwriter#test_multiple_small_writes_accumulate"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_bufferedwriter import test_multiple_small_writes_accumulate

            test_multiple_small_writes_accumulate()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_bufferedwriter#test_small_write_does_not_trigger_stream_write ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_bufferedwriter#test_small_write_does_not_trigger_stream_write"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_bufferedwriter import test_small_write_does_not_trigger_stream_write

            test_small_write_does_not_trigger_stream_write()


    return

def scope_ccai_tests_singlehost_timetravel_pod_test_configuration(sequencer):
    """
    This is the entry point for the 'ccai_tests_singlehost_timetravel_pod_test_configuration' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.singlehost.timetravel.pod.test_configuration") as msc:
        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_configuration#test_activates_specified_portals ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_configuration#test_activates_specified_portals"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_configuration import test_activates_specified_portals

            test_activates_specified_portals()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_configuration#test_active_portals_returns_copy ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_configuration#test_active_portals_returns_copy"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_configuration import test_active_portals_returns_copy

            test_active_portals_returns_copy()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_configuration#test_as_dict_excludes_credentials ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_configuration#test_as_dict_excludes_credentials"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_configuration import test_as_dict_excludes_credentials

            test_as_dict_excludes_credentials()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_configuration#test_as_dict_from_dict_round_trip ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_configuration#test_as_dict_from_dict_round_trip"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_configuration import test_as_dict_from_dict_round_trip

            test_as_dict_from_dict_round_trip()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_configuration#test_defaults_are_correct ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_configuration#test_defaults_are_correct"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_configuration import test_defaults_are_correct

            test_defaults_are_correct()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_configuration#test_from_dict_with_empty_dict ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_configuration#test_from_dict_with_empty_dict"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_configuration import test_from_dict_with_empty_dict

            test_from_dict_with_empty_dict()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_configuration#test_no_backend_uri_does_not_create_backend ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_configuration#test_no_backend_uri_does_not_create_backend"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_configuration import test_no_backend_uri_does_not_create_backend

            test_no_backend_uri_does_not_create_backend()


    return

def scope_ccai_tests_singlehost_timetravel_pod_test_decorators(sequencer):
    """
    This is the entry point for the 'ccai_tests_singlehost_timetravel_pod_test_decorators' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.singlehost.timetravel.pod.test_decorators") as msc:
        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_decorators#test_async_function_works ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_decorators#test_async_function_works"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_decorators import test_async_function_works

            test_async_function_works()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_decorators#test_custom_parameters_create_correct_configuration ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_decorators#test_custom_parameters_create_correct_configuration"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_decorators import test_custom_parameters_create_correct_configuration

            test_custom_parameters_create_correct_configuration()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_decorators#test_decorated_function_executes_normally ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_decorators#test_decorated_function_executes_normally"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_decorators import test_decorated_function_executes_normally

            test_decorated_function_executes_normally()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_decorators#test_decorated_function_with_args_and_kwargs ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_decorators#test_decorated_function_with_args_and_kwargs"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_decorators import test_decorated_function_with_args_and_kwargs

            test_decorated_function_with_args_and_kwargs()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_decorators#test_preserves_function_name_and_docstring ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_decorators#test_preserves_function_name_and_docstring"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_decorators import test_preserves_function_name_and_docstring

            test_preserves_function_name_and_docstring()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_decorators#test_returns_gateway_with_correct_defaults ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_decorators#test_returns_gateway_with_correct_defaults"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_decorators import test_returns_gateway_with_correct_defaults

            test_returns_gateway_with_correct_defaults()


    return

def scope_ccai_tests_singlehost_timetravel_pod_test_gateway(sequencer):
    """
    This is the entry point for the 'ccai_tests_singlehost_timetravel_pod_test_gateway' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.singlehost.timetravel.pod.test_gateway") as msc:
        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_gateway#test_configuration_property ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_gateway#test_configuration_property"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_gateway import test_configuration_property

            test_configuration_property()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_gateway#test_entering_starts_clock_and_sets_active_flag ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_gateway#test_entering_starts_clock_and_sets_active_flag"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_gateway import test_entering_starts_clock_and_sets_active_flag

            test_entering_starts_clock_and_sets_active_flag()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_gateway#test_exceptions_propagate_after_cleanup ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_gateway#test_exceptions_propagate_after_cleanup"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_gateway import test_exceptions_propagate_after_cleanup

            test_exceptions_propagate_after_cleanup()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_gateway#test_exiting_stops_clock_and_clears_active_flag ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_gateway#test_exiting_stops_clock_and_clears_active_flag"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_gateway import test_exiting_stops_clock_and_clears_active_flag

            test_exiting_stops_clock_and_clears_active_flag()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_gateway#test_gateway_start_event_has_timestamp_zero ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_gateway#test_gateway_start_event_has_timestamp_zero"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_gateway import test_gateway_start_event_has_timestamp_zero

            test_gateway_start_event_has_timestamp_zero()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_gateway#test_gateway_stop_event_is_emitted ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_gateway#test_gateway_stop_event_is_emitted"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_gateway import test_gateway_stop_event_is_emitted

            test_gateway_stop_event_is_emitted()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_gateway#test_get_active_gateway_inside_and_outside ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_gateway#test_get_active_gateway_inside_and_outside"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_gateway import test_get_active_gateway_inside_and_outside

            test_get_active_gateway_inside_and_outside()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_gateway#test_registered_recorders_are_flushed_and_closed ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_gateway#test_registered_recorders_are_flushed_and_closed"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_gateway import test_registered_recorders_are_flushed_and_closed

            test_registered_recorders_are_flushed_and_closed()


    return

def scope_ccai_tests_singlehost_timetravel_pod_test_portal(sequencer):
    """
    This is the entry point for the 'ccai_tests_singlehost_timetravel_pod_test_portal' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.singlehost.timetravel.pod.test_portal") as msc:
        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_portal#test_entering_activated_portal_activates_tracing ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_portal#test_entering_activated_portal_activates_tracing"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_portal import test_entering_activated_portal_activates_tracing

            test_entering_activated_portal_activates_tracing()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_portal#test_exceptions_propagate_through_portal ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_portal#test_exceptions_propagate_through_portal"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_portal import test_exceptions_propagate_through_portal

            test_exceptions_propagate_through_portal()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_portal#test_exiting_outermost_portal_resets_state ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_portal#test_exiting_outermost_portal_resets_state"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_portal import test_exiting_outermost_portal_resets_state

            test_exiting_outermost_portal_resets_state()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_portal#test_inactive_portal_is_noop ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_portal#test_inactive_portal_is_noop"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_portal import test_inactive_portal_is_noop

            test_inactive_portal_is_noop()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_portal#test_name_property ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_portal#test_name_property"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_portal import test_name_property

            test_name_property()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_portal#test_nested_portals_increment_decrement_depth ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_portal#test_nested_portals_increment_decrement_depth"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_portal import test_nested_portals_increment_decrement_depth

            test_nested_portals_increment_decrement_depth()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_portal#test_portal_without_gateway_is_noop ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_portal#test_portal_without_gateway_is_noop"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_portal import test_portal_without_gateway_is_noop

            test_portal_without_gateway_is_noop()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_portal#test_record_inner_portals_false_no_annotation_events ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_portal#test_record_inner_portals_false_no_annotation_events"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_portal import test_record_inner_portals_false_no_annotation_events

            test_record_inner_portals_false_no_annotation_events()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_portal#test_record_inner_portals_true_emits_events ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_portal#test_record_inner_portals_true_emits_events"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_portal import test_record_inner_portals_true_emits_events

            test_record_inner_portals_true_emits_events()


    return

def scope_ccai_tests_singlehost_timetravel_pod_test_portal_expression(sequencer):
    """
    This is the entry point for the 'ccai_tests_singlehost_timetravel_pod_test_portal_expression' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.singlehost.timetravel.pod.test_portal_expression") as msc:
        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_portal_expression#test_expression_evaluation_error_does_not_activate ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_portal_expression#test_expression_evaluation_error_does_not_activate"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_portal_expression import test_expression_evaluation_error_does_not_activate

            test_expression_evaluation_error_does_not_activate()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_portal_expression#test_expression_false_does_not_activate ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_portal_expression#test_expression_false_does_not_activate"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_portal_expression import test_expression_false_does_not_activate

            test_expression_false_does_not_activate()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_portal_expression#test_expression_true_activates ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_portal_expression#test_expression_true_activates"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_portal_expression import test_expression_true_activates

            test_expression_true_activates()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_portal_expression#test_once_flag_deactivates_portal ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_portal_expression#test_once_flag_deactivates_portal"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_portal_expression import test_once_flag_deactivates_portal

            test_once_flag_deactivates_portal()


    return

def scope_ccai_tests_singlehost_timetravel_pod_test_portalfilter(sequencer):
    """
    This is the entry point for the 'ccai_tests_singlehost_timetravel_pod_test_portalfilter' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.singlehost.timetravel.pod.test_portalfilter") as msc:
        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_portalfilter#test_events_in_chronological_order ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_portalfilter#test_events_in_chronological_order"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_portalfilter import test_events_in_chronological_order

            test_events_in_chronological_order()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_portalfilter#test_filters_events_within_enter_exit_markers ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_portalfilter#test_filters_events_within_enter_exit_markers"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_portalfilter import test_filters_events_within_enter_exit_markers

            test_filters_events_within_enter_exit_markers()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_portalfilter#test_multiple_enter_exit_pairs ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_portalfilter#test_multiple_enter_exit_pairs"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_portalfilter import test_multiple_enter_exit_pairs

            test_multiple_enter_exit_pairs()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_portalfilter#test_nonexistent_portal_returns_empty ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_portalfilter#test_nonexistent_portal_returns_empty"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_portalfilter import test_nonexistent_portal_returns_empty

            test_nonexistent_portal_returns_empty()


    return

def scope_ccai_tests_singlehost_timetravel_pod_test_portalregistry(sequencer):
    """
    This is the entry point for the 'ccai_tests_singlehost_timetravel_pod_test_portalregistry' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.singlehost.timetravel.pod.test_portalregistry") as msc:
        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_portalregistry#test_activate_and_is_active_round_trip ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_portalregistry#test_activate_and_is_active_round_trip"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_portalregistry import test_activate_and_is_active_round_trip

            test_activate_and_is_active_round_trip()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_portalregistry#test_activate_portals_bulk ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_portalregistry#test_activate_portals_bulk"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_portalregistry import test_activate_portals_bulk

            test_activate_portals_bulk()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_portalregistry#test_concurrent_access_does_not_corrupt_state ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_portalregistry#test_concurrent_access_does_not_corrupt_state"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_portalregistry import test_concurrent_access_does_not_corrupt_state

            test_concurrent_access_does_not_corrupt_state()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_portalregistry#test_deactivate_all ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_portalregistry#test_deactivate_all"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_portalregistry import test_deactivate_all

            test_deactivate_all()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_portalregistry#test_deactivate_sets_portal_inactive ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_portalregistry#test_deactivate_sets_portal_inactive"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_portalregistry import test_deactivate_sets_portal_inactive

            test_deactivate_sets_portal_inactive()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_portalregistry#test_list_portals_returns_correct_pairs ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_portalregistry#test_list_portals_returns_correct_pairs"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_portalregistry import test_list_portals_returns_correct_pairs

            test_list_portals_returns_correct_pairs()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_portalregistry#test_returns_same_instance ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_portalregistry#test_returns_same_instance"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_portalregistry import test_returns_same_instance

            test_returns_same_instance()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_portalregistry#test_unknown_portal_returns_false ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_portalregistry#test_unknown_portal_returns_false"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_portalregistry import test_unknown_portal_returns_false

            test_unknown_portal_returns_false()


    return

def scope_ccai_tests_singlehost_timetravel_pod_test_reader(sequencer):
    """
    This is the entry point for the 'ccai_tests_singlehost_timetravel_pod_test_reader' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.singlehost.timetravel.pod.test_reader") as msc:
        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_reader#test_bytesio_source ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_reader#test_bytesio_source"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_reader import test_bytesio_source

            test_bytesio_source()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_reader#test_context_manager ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_reader#test_context_manager"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_reader import test_context_manager

            test_context_manager()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_reader#test_multiple_file_sources ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_reader#test_multiple_file_sources"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_reader import test_multiple_file_sources

            test_multiple_file_sources()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_reader#test_round_trip_file ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_reader#test_round_trip_file"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_reader import test_round_trip_file

            test_round_trip_file()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_reader#test_scan_headers ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_reader#test_scan_headers"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_reader import test_scan_headers

            test_scan_headers()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_reader#test_unsupported_source_raises_type_error ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_reader#test_unsupported_source_raises_type_error"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_reader import test_unsupported_source_raises_type_error

            test_unsupported_source_raises_type_error()


    return

def scope_ccai_tests_singlehost_timetravel_pod_test_timeline(sequencer):
    """
    This is the entry point for the 'ccai_tests_singlehost_timetravel_pod_test_timeline' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.singlehost.timetravel.pod.test_timeline") as msc:
        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_timeline#test_event_types_filter ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_timeline#test_event_types_filter"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_timeline import test_event_types_filter

            test_event_types_filter()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_timeline#test_multiple_sources_merge_sorted ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_timeline#test_multiple_sources_merge_sorted"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_timeline import test_multiple_sources_merge_sorted

            test_multiple_sources_merge_sorted()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_timeline#test_single_source_sorted_by_timestamp ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_timeline#test_single_source_sorted_by_timestamp"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_timeline import test_single_source_sorted_by_timestamp

            test_single_source_sorted_by_timestamp()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_timeline#test_stable_sort_preserves_order_for_equal_timestamps ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_timeline#test_stable_sort_preserves_order_for_equal_timestamps"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_timeline import test_stable_sort_preserves_order_for_equal_timestamps

            test_stable_sort_preserves_order_for_equal_timestamps()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_timeline#test_thread_id_filter ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_timeline#test_thread_id_filter"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_timeline import test_thread_id_filter

            test_thread_id_filter()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_timeline#test_time_range_filter ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_timeline#test_time_range_filter"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_timeline import test_time_range_filter

            test_time_range_filter()


    return

def scope_ccai_tests_singlehost_timetravel_pod_test_traceclock(sequencer):
    """
    This is the entry point for the 'ccai_tests_singlehost_timetravel_pod_test_traceclock' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.singlehost.timetravel.pod.test_traceclock") as msc:
        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceclock#test_is_running_reflects_clock_state ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceclock#test_is_running_reflects_clock_state"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceclock import test_is_running_reflects_clock_state

            test_is_running_reflects_clock_state()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceclock#test_returns_same_instance_on_repeated_calls ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceclock#test_returns_same_instance_on_repeated_calls"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceclock import test_returns_same_instance_on_repeated_calls

            test_returns_same_instance_on_repeated_calls()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceclock#test_returns_trace_clock_instance ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceclock#test_returns_trace_clock_instance"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceclock import test_returns_trace_clock_instance

            test_returns_trace_clock_instance()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceclock#test_successive_timestamps_are_non_decreasing ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceclock#test_successive_timestamps_are_non_decreasing"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceclock import test_successive_timestamps_are_non_decreasing

            test_successive_timestamps_are_non_decreasing()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceclock#test_timestamp_after_start_returns_non_negative_integer ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceclock#test_timestamp_after_start_returns_non_negative_integer"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceclock import test_timestamp_after_start_returns_non_negative_integer

            test_timestamp_after_start_returns_non_negative_integer()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceclock#test_timestamp_after_stop_raises_runtime_error ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceclock#test_timestamp_after_stop_raises_runtime_error"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceclock import test_timestamp_after_stop_raises_runtime_error

            test_timestamp_after_stop_raises_runtime_error()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceclock#test_timestamp_before_start_raises_runtime_error ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceclock#test_timestamp_before_start_raises_runtime_error"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceclock import test_timestamp_before_start_raises_runtime_error

            test_timestamp_before_start_raises_runtime_error()


    return

def scope_ccai_tests_singlehost_timetravel_pod_test_traceconfiguration(sequencer):
    """
    This is the entry point for the 'ccai_tests_singlehost_timetravel_pod_test_traceconfiguration' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.singlehost.timetravel.pod.test_traceconfiguration") as msc:
        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceconfiguration#test_as_dict_returns_correct_dictionary ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceconfiguration#test_as_dict_returns_correct_dictionary"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceconfiguration import test_as_dict_returns_correct_dictionary

            test_as_dict_returns_correct_dictionary()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceconfiguration#test_default_constant_has_expected_values ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceconfiguration#test_default_constant_has_expected_values"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceconfiguration import test_default_constant_has_expected_values

            test_default_constant_has_expected_values()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceconfiguration#test_default_construction_values ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceconfiguration#test_default_construction_values"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceconfiguration import test_default_construction_values

            test_default_construction_values()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceconfiguration#test_explicit_construction_preserves_values ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceconfiguration#test_explicit_construction_preserves_values"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceconfiguration import test_explicit_construction_preserves_values

            test_explicit_construction_preserves_values()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceconfiguration#test_from_dict_round_trips_with_as_dict ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceconfiguration#test_from_dict_round_trips_with_as_dict"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceconfiguration import test_from_dict_round_trips_with_as_dict

            test_from_dict_round_trips_with_as_dict()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceconfiguration#test_from_dict_with_partial_data_uses_defaults ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceconfiguration#test_from_dict_with_partial_data_uses_defaults"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceconfiguration import test_from_dict_with_partial_data_uses_defaults

            test_from_dict_with_partial_data_uses_defaults()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceconfiguration#test_properties_are_read_only ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceconfiguration#test_properties_are_read_only"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceconfiguration import test_properties_are_read_only

            test_properties_are_read_only()


    return

def scope_ccai_tests_singlehost_timetravel_pod_test_traceevents(sequencer):
    """
    This is the entry point for the 'ccai_tests_singlehost_timetravel_pod_test_traceevents' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.singlehost.timetravel.pod.test_traceevents") as msc:
        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceevents#test_all_constants_are_unique_integers ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceevents#test_all_constants_are_unique_integers"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceevents import test_all_constants_are_unique_integers

            test_all_constants_are_unique_integers()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceevents#test_base_fields_are_set_correctly ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceevents#test_base_fields_are_set_correctly"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceevents import test_base_fields_are_set_correctly

            test_base_fields_are_set_correctly()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceevents#test_constructible_with_documented_fields_callevent ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceevents#test_constructible_with_documented_fields_callevent"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceevents import test_constructible_with_documented_fields_callevent

            test_constructible_with_documented_fields_callevent()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceevents#test_constructible_with_documented_fields_lineevent ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceevents#test_constructible_with_documented_fields_lineevent"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceevents import test_constructible_with_documented_fields_lineevent

            test_constructible_with_documented_fields_lineevent()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceevents#test_constructible_with_documented_fields_returnevent ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceevents#test_constructible_with_documented_fields_returnevent"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceevents import test_constructible_with_documented_fields_returnevent

            test_constructible_with_documented_fields_returnevent()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceevents#test_constructible_with_documented_fields_variablesnapshotevent ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceevents#test_constructible_with_documented_fields_variablesnapshotevent"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceevents import test_constructible_with_documented_fields_variablesnapshotevent

            test_constructible_with_documented_fields_variablesnapshotevent()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceevents#test_default_args_and_kwargs ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceevents#test_default_args_and_kwargs"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceevents import test_default_args_and_kwargs

            test_default_args_and_kwargs()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceevents#test_expected_type_values ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceevents#test_expected_type_values"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceevents import test_expected_type_values

            test_expected_type_values()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceevents#test_gateway_start_event ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceevents#test_gateway_start_event"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceevents import test_gateway_start_event

            test_gateway_start_event()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceevents#test_gateway_stop_event ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceevents#test_gateway_stop_event"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceevents import test_gateway_stop_event

            test_gateway_stop_event()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceevents#test_portal_enter_event ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceevents#test_portal_enter_event"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceevents import test_portal_enter_event

            test_portal_enter_event()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceevents#test_portal_exit_event ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceevents#test_portal_exit_event"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceevents import test_portal_exit_event

            test_portal_exit_event()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceevents#test_slots_prevents_arbitrary_attribute ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceevents#test_slots_prevents_arbitrary_attribute"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceevents import test_slots_prevents_arbitrary_attribute

            test_slots_prevents_arbitrary_attribute()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceevents#test_slots_prevents_arbitrary_attribute_addition ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceevents#test_slots_prevents_arbitrary_attribute_addition"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceevents import test_slots_prevents_arbitrary_attribute_addition

            test_slots_prevents_arbitrary_attribute_addition()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceevents#test_stores_exception_details_as_strings ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceevents#test_stores_exception_details_as_strings"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceevents import test_stores_exception_details_as_strings

            test_stores_exception_details_as_strings()


    return

def scope_ccai_tests_singlehost_timetravel_pod_test_tracehookmanager(sequencer):
    """
    This is the entry point for the 'ccai_tests_singlehost_timetravel_pod_test_tracehookmanager' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.singlehost.timetravel.pod.test_tracehookmanager") as msc:
        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_tracehookmanager#test_events_carry_correct_thread_id ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_tracehookmanager#test_events_carry_correct_thread_id"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_tracehookmanager import test_events_carry_correct_thread_id

            test_events_carry_correct_thread_id()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_tracehookmanager#test_exceptions_produce_exception_events ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_tracehookmanager#test_exceptions_produce_exception_events"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_tracehookmanager import test_exceptions_produce_exception_events

            test_exceptions_produce_exception_events()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_tracehookmanager#test_install_and_call_produces_call_and_return_events ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_tracehookmanager#test_install_and_call_produces_call_and_return_events"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_tracehookmanager import test_install_and_call_produces_call_and_return_events

            test_install_and_call_produces_call_and_return_events()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_tracehookmanager#test_trace_lines_false_no_line_events ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_tracehookmanager#test_trace_lines_false_no_line_events"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_tracehookmanager import test_trace_lines_false_no_line_events

            test_trace_lines_false_no_line_events()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_tracehookmanager#test_trace_lines_true_produces_line_events ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_tracehookmanager#test_trace_lines_true_produces_line_events"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_tracehookmanager import test_trace_lines_true_produces_line_events

            test_trace_lines_true_produces_line_events()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_tracehookmanager#test_trace_variables_produces_snapshot_events ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_tracehookmanager#test_trace_variables_produces_snapshot_events"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_tracehookmanager import test_trace_variables_produces_snapshot_events

            test_trace_variables_produces_snapshot_events()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_tracehookmanager#test_uninstall_stops_event_production ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_tracehookmanager#test_uninstall_stops_event_production"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_tracehookmanager import test_uninstall_stops_event_production

            test_uninstall_stops_event_production()


    return

def scope_ccai_tests_singlehost_timetravel_pod_test_tracerecorder(sequencer):
    """
    This is the entry point for the 'ccai_tests_singlehost_timetravel_pod_test_tracerecorder' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.singlehost.timetravel.pod.test_tracerecorder") as msc:
        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_tracerecorder#test_cannot_instantiate_directly ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_tracerecorder#test_cannot_instantiate_directly"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_tracerecorder import test_cannot_instantiate_directly

            test_cannot_instantiate_directly()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_tracerecorder#test_complete_subclass_can_be_instantiated ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_tracerecorder#test_complete_subclass_can_be_instantiated"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_tracerecorder import test_complete_subclass_can_be_instantiated

            test_complete_subclass_can_be_instantiated()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_tracerecorder#test_subclass_missing_abstract_method_cannot_be_instantiated ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_tracerecorder#test_subclass_missing_abstract_method_cannot_be_instantiated"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_tracerecorder import test_subclass_missing_abstract_method_cannot_be_instantiated

            test_subclass_missing_abstract_method_cannot_be_instantiated()


    return

def scope_ccai_tests_singlehost_timetravel_pod_test_traceserializer(sequencer):
    """
    This is the entry point for the 'ccai_tests_singlehost_timetravel_pod_test_traceserializer' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.singlehost.timetravel.pod.test_traceserializer") as msc:
        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceserializer#test_call_event_round_trips_with_all_fields ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceserializer#test_call_event_round_trips_with_all_fields"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceserializer import test_call_event_round_trips_with_all_fields

            test_call_event_round_trips_with_all_fields()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceserializer#test_envelope_size_is_29_bytes ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceserializer#test_envelope_size_is_29_bytes"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceserializer import test_envelope_size_is_29_bytes

            test_envelope_size_is_29_bytes()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceserializer#test_gateway_start_preserves_wall_clock_time ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceserializer#test_gateway_start_preserves_wall_clock_time"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceserializer import test_gateway_start_preserves_wall_clock_time

            test_gateway_start_preserves_wall_clock_time()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceserializer#test_gateway_stop_preserves_wall_clock_time ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceserializer#test_gateway_stop_preserves_wall_clock_time"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceserializer import test_gateway_stop_preserves_wall_clock_time

            test_gateway_stop_preserves_wall_clock_time()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceserializer#test_line_event_has_zero_length_payload ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceserializer#test_line_event_has_zero_length_payload"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceserializer import test_line_event_has_zero_length_payload

            test_line_event_has_zero_length_payload()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceserializer#test_portal_enter_preserves_name ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceserializer#test_portal_enter_preserves_name"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceserializer import test_portal_enter_preserves_name

            test_portal_enter_preserves_name()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceserializer#test_portal_exit_preserves_name ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceserializer#test_portal_exit_preserves_name"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceserializer import test_portal_exit_preserves_name

            test_portal_exit_preserves_name()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceserializer#test_preserves_exception_details ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceserializer#test_preserves_exception_details"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceserializer import test_preserves_exception_details

            test_preserves_exception_details()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceserializer#test_preserves_local_variables_dict ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceserializer#test_preserves_local_variables_dict"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceserializer import test_preserves_local_variables_dict

            test_preserves_local_variables_dict()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceserializer#test_read_header_returns_envelope_fields ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceserializer#test_read_header_returns_envelope_fields"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceserializer import test_read_header_returns_envelope_fields

            test_read_header_returns_envelope_fields()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceserializer#test_return_event_preserves_return_value ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceserializer#test_return_event_preserves_return_value"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceserializer import test_return_event_preserves_return_value

            test_return_event_preserves_return_value()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_traceserializer#test_skip_event_advances_to_next_event ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_traceserializer#test_skip_event_advances_to_next_event"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_traceserializer import test_skip_event_advances_to_next_event

            test_skip_event_advances_to_next_event()


    return

def scope_ccai_tests_singlehost_timetravel_pod_test_tracingstate(sequencer):
    """
    This is the entry point for the 'ccai_tests_singlehost_timetravel_pod_test_tracingstate' test scope.
    """

    with sequencer.enter_module_scope_context("ccai.tests.singlehost.timetravel.pod.test_tracingstate") as msc:
        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_tracingstate#test_default_initialization ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_tracingstate#test_default_initialization"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_tracingstate import test_default_initialization

            test_default_initialization()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_tracingstate#test_defaults_to_false ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_tracingstate#test_defaults_to_false"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_tracingstate import test_defaults_to_false

            test_defaults_to_false()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_tracingstate#test_modifying_state_on_one_thread_does_not_affect_another ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_tracingstate#test_modifying_state_on_one_thread_does_not_affect_another"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_tracingstate import test_modifying_state_on_one_thread_does_not_affect_another

            test_modifying_state_on_one_thread_does_not_affect_another()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_tracingstate#test_reset_restores_defaults ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_tracingstate#test_reset_restores_defaults"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_tracingstate import test_reset_restores_defaults

            test_reset_restores_defaults()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_tracingstate#test_returns_different_instances_for_different_threads ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_tracingstate#test_returns_different_instances_for_different_threads"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_tracingstate import test_returns_different_instances_for_different_threads

            test_returns_different_instances_for_different_threads()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_tracingstate#test_returns_same_instance_on_same_thread ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_tracingstate#test_returns_same_instance_on_same_thread"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_tracingstate import test_returns_same_instance_on_same_thread

            test_returns_same_instance_on_same_thread()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_tracingstate#test_set_gateway_active_false_after_true ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_tracingstate#test_set_gateway_active_false_after_true"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_tracingstate import test_set_gateway_active_false_after_true

            test_set_gateway_active_false_after_true()

        # ================ Test Scope: ccai.tests.singlehost.timetravel.pod.test_tracingstate#test_set_gateway_active_true ================

        test_scope_name = "ccai.tests.singlehost.timetravel.pod.test_tracingstate#test_set_gateway_active_true"

        with sequencer.enter_test_scope_context(test_scope_name) as tscope:
            from ccai.tests.singlehost.timetravel.pod.test_tracingstate import test_set_gateway_active_true

            test_set_gateway_active_true()


    return
