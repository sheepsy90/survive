# -*- coding:utf-8 -*-
import unittest
import errno
from client.network.LoginServiceClient import AccountResponse
from server.xmlrpc_services.login.LoginServerHandler import LoginServerHandler
from socket import error as socket_error


class LoginHandlerTest(unittest.TestCase):

    def test_login_procedure_dry(self):
        try:
            lsh = LoginServerHandler(":memory:")

            account_response = lsh.general_login("Sheepy", "sheepy")
            self.assertEqual(False, account_response.success)
            self.assertEqual("Incorrect Credentials", account_response.reason)
            self.assertEqual(AccountResponse.INCORRECT_CREDENTIALS, account_response.code)

            account_response = lsh.general_login("sheepy", "sheepy")
            self.assertEqual(True, account_response.success)
            self.assertEqual(1, account_response.account_id)
            self.assertEqual(AccountResponse.NO_ERROR, account_response.code)
        except socket_error as serr:
            if serr.errno != errno.ECONNREFUSED:
                raise serr
