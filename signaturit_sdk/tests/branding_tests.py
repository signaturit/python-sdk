import unittest
import os
from signaturit_sdk.signaturit_client import SignaturitClient
from signaturit_sdk.resources.parser import Parser

class BrandingTest(unittest.TestCase):
    TEST_FILE_URL = '/tmp/test.gif'

    def test_create_branding_with_invalid_params_should_raise_exception(self):
        client = SignaturitClient('TOKEN')
        self.assertRaises(Exception, client.create_branding, {'testing': 'some_value'})

    def test_update_branding_with_invalid_params_should_raise_exception(self):
        client = SignaturitClient('TOKEN')
        self.assertRaises(Exception, client.update_branding, ('SOME_ID', {'testing': 'some_value'}))

    def test_put_branding_should_return_file_but_no_params(self):
        client = SignaturitClient('TOKEN')
        parser = Parser(client.TOUCH_BRANDING_PARAMS, [])

        open(self.TEST_FILE_URL, 'a').close()

        params = {'files': self.TEST_FILE_URL}

        params, files = parser.parse_data(params)

        self.assertEquals(1, len(files))
        self.assertEquals(1, len(params))

        os.unlink(self.TEST_FILE_URL)

if __name__ == '__main__':
    unittest.main()
