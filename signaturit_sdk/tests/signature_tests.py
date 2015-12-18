import unittest
import os
from signaturit_sdk.signaturit_client import SignaturitClient
import httpretty


class SignatureTest(unittest.TestCase):
    TEST_FILE_URL = '/tmp/test.pdf'

    def test_create_signature_with_invalid_params_should_raise_exception(self):
        client = SignaturitClient('TOKEN')
        self.assertRaises(Exception, client.create_signature, {'testing': 'some_value'})

    @httpretty.activate
    def test_cancel_signature(self):
        httpretty.register_uri(httpretty.PATCH, "http://api.sandbox.signaturit.com/v2/signs/SIGN_ID/cancel.json",
                               body='{"id": "SIGN_ID", "recipients": [{"email": "test@test.com", "fullname": "Mr Test"}], "subject": "Testing"}',
                               content_type="application/json")

        signaturit_client = SignaturitClient('SOME_TOKEN')

        response = signaturit_client.cancel_signature('SIGN_ID')

        self.assertEqual('Testing', response['subject'])
        self.assertEqual([{"email": "test@test.com", "fullname": "Mr Test"}], response['recipients'])

    @httpretty.activate
    def test_send_signature_reminder(self):
        httpretty.register_uri(httpretty.POST, "http://api.sandbox.signaturit.com/v2/signs/SIGN_ID/documents/JOB_ID/reminder.json",
                               body='{}',
                               content_type="application/json")

        signaturit_client = SignaturitClient('SOME_TOKEN')

        signaturit_client.send_signature_reminder('SIGN_ID', 'JOB_ID')

    @httpretty.activate
    def test_get_signatures(self):
        httpretty.register_uri(httpretty.GET, "http://api.sandbox.signaturit.com/v2/signs.json",
                               body='{"recipients": [{"email": "test@test.com", "fullname": "Mr Test"}],"subject": "Testing"}',
                               content_type="application/json")

        signaturit_client = SignaturitClient('SOME_TOKEN')

        response = signaturit_client.get_signatures()

        self.assertEqual('Testing', response['subject'])
        self.assertEqual([{"email": "test@test.com", "fullname": "Mr Test"}], response['recipients'])

    @httpretty.activate
    def test_count_signatures(self):
        httpretty.register_uri(httpretty.GET, "http://api.sandbox.signaturit.com/v2/signs/count.json",
                               body='3',
                               content_type="application/json")

        signaturit_client = SignaturitClient('SOME_TOKEN')

        response = signaturit_client.count_signatures()

        self.assertEqual(3, response)

    @httpretty.activate
    def test_get_signature(self):
        httpretty.register_uri(httpretty.GET, "http://api.sandbox.signaturit.com/v2/signs/SIGN_ID.json",
                               body='{"id": "SIGN_ID", ' +
                                    '"recipients": [{"email": "test@test.com", "fullname": "Mr Test"}], ' +
                                    '"subject": "Testing"}',
                               content_type="application/json")

        signaturit_client = SignaturitClient('SOME_TOKEN')

        response = signaturit_client.get_signature('SIGN_ID')

        self.assertEqual('Testing', response['subject'])
        self.assertEqual('SIGN_ID', response['id'])
        self.assertEqual([{"email": "test@test.com", "fullname": "Mr Test"}], response['recipients'])

    @httpretty.activate
    def test_create_signature(self):
        open(self.TEST_FILE_URL, 'a').close()

        httpretty.register_uri(httpretty.POST, "http://api.sandbox.signaturit.com/v2/signs.json",
                               body='{"id": "SIGN_ID", ' +
                                    '"recipients": [{"email": "test@test.com", "fullname": "Mr Test"}],' +
                                    '"subject": "Testing"}')

        signaturit_client = SignaturitClient('SOME_CLIENT')

        response = signaturit_client.create_signature([self.TEST_FILE_URL], [{"email": "test@test.com", "fullname": "Mr Test"}], {})

        self.assertEqual('Testing', response['subject'])
        self.assertEqual('SIGN_ID', response['id'])
        self.assertEqual([{"email": "test@test.com", "fullname": "Mr Test"}], response['recipients'])

        os.unlink(self.TEST_FILE_URL)

if __name__ == '__main__':
    unittest.main()
