import unittest
from signaturit_sdk.signaturit_client import SignaturitClient

class AccountTest(unittest.TestCase):
    def test_set_account_storage_with_invalid_params_should_raise_exception(self):
        client = SignaturitClient('TOKEN')
        self.assertRaises(Exception, client.set_document_storage, ('SOME_ID', {'testing': 'some_value'}))

if __name__ == '__main__':
    unittest.main()
