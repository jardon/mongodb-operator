import unittest
from unittest import mock

# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.
from src import machine_helpers


class TestCharm(unittest.TestCase):
    def test_generate_service_args(self):
        service_args_auth = " ".join(
            [
                "ExecStart=/usr/bin/mongod",
                "--bind_ip_all",
                "--replSet=my_repl_set",
                "--auth",
                "--clusterAuthMode=keyFile",
                f"--keyFile={machine_helpers.KEY_FILE}",
                "\n",
            ]
        )

        config = mock.Mock()
        config.replset = "my_repl_set"
        config.tls_external = False
        config.tls_internal = False
        self.assertEqual(
            machine_helpers.generate_service_args(True, "1.1.1.1", config),
            service_args_auth,
        )

        service_args = " ".join(
            [
                "ExecStart=/usr/bin/mongod",
                # bind to localhost and external interfaces
                "--bind_ip_all",
                # part of replicaset
                "--replSet=my_repl_set",
                "\n",
            ]
        )
        self.assertEqual(
            machine_helpers.generate_service_args(False, "1.1.1.1", config),
            service_args,
        )
