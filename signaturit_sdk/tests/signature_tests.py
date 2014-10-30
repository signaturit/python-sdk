import unittest
import os
from signaturit_sdk.signaturit_client import SignaturitClient
from signaturit_sdk.resources.parser import Parser
import httpretty
import json

class SignatureTest(unittest.TestCase):
    TEST_FILE_URL = '/tmp/test.pdf'

    def test_create_signature_with_invalid_params_should_raise_exception(self):
        client = SignaturitClient('TOKEN')
        self.assertRaises(Exception, client.create_signature_request, {'testing': 'some_value'})

    def test_create_signature_with_valid_params_should_format_the_params_correctly(self):
        client = SignaturitClient('TOKEN')
        parser = Parser(client.CREATE_SIGN_PARAMS, [])

        open(self.TEST_FILE_URL, 'a').close()

        sign_params = {'subject': 'Receipt number 215',
                       'in_person_sign': 1,
                       'mandatory_photo': 1,
                       'sequential': 1,
                       'body': 'Please, can you sign this receipt? Just click the button!',
                       'mandatory_pages': [2, 5],
                       'recipients': [{'email': 'pau.soler@signatur.it', 'fullname': 'Pau'},
                                      {'email': 'john.doe@signatur.it', 'fullname': 'John'}],
                       'files': [self.TEST_FILE_URL]}

        expected_params = {'body': 'Please, can you sign this receipt? Just click the button!',
                           'mandatory_pages[0]': '2',
                           'mandatory_photo': '1',
                           'recipients[1][fullname]': 'John',
                           'mandatory_pages[1]': '5',
                           'recipients[1][email]': 'john.doe@signatur.it',
                           'sequential': '1',
                           'recipients[0][email]': 'pau.soler@signatur.it',
                           'recipients[0][fullname]': 'Pau',
                           'in_person_sign': '1',
                           'subject': 'Receipt number 215'}

        parsed_data, files = parser.parse_data(sign_params)

        self.assertEquals(expected_params, parsed_data)
        self.assertEquals(1, len(files))

        os.unlink(self.TEST_FILE_URL)

    @httpretty.activate
    def test_cancel_signature_request(self):
        httpretty.register_uri(httpretty.PATCH, "http://api.sandbox.signaturit.com/v2/signs/SIGN_ID/cancel.json",
                               body='{"id": "SIGN_ID", "recipients": [{"email": "test@test.com", "fullname": "Mr Test"}], "subject": "Testing"}',
                               content_type="application/json")

        signaturit_client = SignaturitClient('SOME_TOKEN')

        response = signaturit_client.cancel_signature_request('SIGN_ID')

        self.assertEqual('Testing', response['subject'])
        self.assertEqual([{"email": "test@test.com", "fullname": "Mr Test"}], response['recipients'])

    @httpretty.activate
    def test_send_reminder(selfself):
        httpretty.register_uri(httpretty.POST, "http://api.sandbox.signaturit.com/v2/signs/SIGN_ID/documents/JOB_ID/reminder.json",
                               body='{}',
                               content_type="application/json")

        signaturit_client = SignaturitClient('SOME_TOKEN')

        signaturit_client.send_reminder('SIGN_ID', 'JOB_ID')

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

        response = signaturit_client.create_signature_request([self.TEST_FILE_URL], [{"email": "test@test.com", "fullname": "Mr Test"}], {})

        self.assertEqual('Testing', response['subject'])
        self.assertEqual('SIGN_ID', response['id'])
        self.assertEqual([{"email": "test@test.com", "fullname": "Mr Test"}], response['recipients'])

        os.unlink(self.TEST_FILE_URL)

if __name__ == '__main__':
    unittest.main()
