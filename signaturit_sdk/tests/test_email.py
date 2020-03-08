import unittest
import os
from signaturit_sdk.signaturit_client import SignaturitClient
from signaturit_sdk.resources.parser import Parser
import httpretty
import warnings


class TestEmail(unittest.TestCase):
    TEST_FILE_URL = '/tmp/test.pdf'

    def setUp(self):
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*")

    def test_create_email_with_invalid_params_should_raise_exception(self):
        client = SignaturitClient('TOKEN')
        self.assertRaises(Exception, client.create_email, {'testing': 'some_value'})

    @httpretty.activate
    def test_get_emails(self):
        httpretty.register_uri(httpretty.GET, "https://api.sandbox.signaturit.com/v3/emails.json",
                               body='{"recipients": [{"email": "test@test.com", "fullname": "Mr Test"}],"subject": "Testing"}',
                               content_type="application/json")

        signaturit_client = SignaturitClient('SOME_TOKEN')

        response = signaturit_client.get_emails()

        self.assertEqual('Testing', response['subject'])
        self.assertEqual([{"email": "test@test.com", "fullname": "Mr Test"}], response['recipients'])

    @httpretty.activate
    def test_count_emails(self):
        httpretty.register_uri(httpretty.GET, "https://api.sandbox.signaturit.com/v3/emails/count.json",
                               body='3',
                               content_type="application/json")

        signaturit_client = SignaturitClient('SOME_TOKEN')

        response = signaturit_client.count_emails()

        self.assertEqual(3, response)

    @httpretty.activate
    def get_email(self):
        httpretty.register_uri(httpretty.GET, "https://api.sandbox.signaturit.com/v2/email/EMAIL_ID.json",
                               body='{"id": "SIGN_ID", ' +
                                    '"recipients": [{"email": "test@test.com", "fullname": "Mr Test"}], ' +
                                    '"subject": "Testing"}',
                               content_type="application/json")

        signaturit_client = SignaturitClient('SOME_TOKEN')

        response = signaturit_client.get_email('SIGN_ID')

        self.assertEqual('Testing', response['subject'])
        self.assertEqual('SIGN_ID', response['id'])
        self.assertEqual([{"email": "test@test.com", "fullname": "Mr Test"}], response['recipients'])


if __name__ == '__main__':
    unittest.main()
