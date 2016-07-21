from signaturit_sdk.resources.connection import Connection
from signaturit_sdk.resources.parser import Parser


class SignaturitClient:
    BRANDINGS_URL = '/v3/brandings.json'
    BRANDINGS_ID_URL = '/v3/brandings/%s.json'

    EMAILS_URL = '/v3/emails.json'
    EMAILS_COUNT_URL = '/v3/emails/count.json'
    EMAILS_ID_URL = '/v3/emails/%s.json'
    EMAILS_AUDIT_TRAIL = '/v3/emails/%s/certificates/%s/download/audit_trail'

    PRODUCTION = True

    SIGNS_URL = '/v3/signatures.json'
    SIGNS_CANCEL_URL = '/v3/signatures/%s/cancel.json'
    SIGNS_COUNT_URL = '/v3/signatures/count.json'
    SIGNS_ID_URL = '/v3/signatures/%s.json'
    SIGNS_DOCUMENTS_AUDIT_URL = '/v3/signatures/%s/documents/%s/download/audit_trail'
    SIGNS_DOCUMENTS_SIGNED_URL = '/v3/signatures/%s/documents/%s/download/signed'
    SIGNS_SEND_REMINDER_URL = '/v3/signatures/%s/reminder.json'

    TEMPLATES_URL = '/v3/templates.json'

    def __init__(self, token, production=False):
        self.token = token
        self.production = production

    def get_signature(self, signature_id):
        """
        Get a concrete Signature
        @return Signature data
        """
        connection = Connection(self.token)
        connection.set_url(self.production, self.SIGNS_ID_URL % signature_id)

        return connection.get_request()

    def get_signatures(self, limit=100, offset=0, conditions={}):
        """
        Get all signatures
        """
        url = self.SIGNS_URL + "?limit=%s&offset=%s" % (limit, offset)

        for key, value in conditions.items():
            if key is 'ids':
                value = ",".join(value)

            url += '&%s=%s' % (key, value)

        connection = Connection(self.token)
        connection.set_url(self.production, url)

        return connection.get_request()

    def count_signatures(self, conditions={}):
        """
        Count all signatures
        """
        url = self.SIGNS_COUNT_URL + '?'

        for key, value in conditions.items():
            if key is 'ids':
                value = ",".join(value)

            url += '&%s=%s' % (key, value)

        connection = Connection(self.token)
        connection.set_url(self.production, url)

        return connection.get_request()

    def download_audit_trail(self, signature_id, document_id):
        """
        Get the audit trail of concrete document
        @signature_id: Id of signature
        @document_id: Id of document
        """
        connection = Connection(self.token)
        connection.set_url(self.production, self.SIGNS_DOCUMENTS_AUDIT_URL % (signature_id, document_id))

        response, headers = connection.file_request()

        if headers['content-type'] == 'application/json':
            return response

        return response

    def download_signed_document(self, signature_id, document_id):
        """
        Get the audit trail of concrete document
        @signature_id: Id of signature
        @document_id: Id of document
        """
        connection = Connection(self.token)

        connection.set_url(self.production, self.SIGNS_DOCUMENTS_SIGNED_URL % (signature_id, document_id))

        response, headers = connection.file_request()

        if headers['content-type'] == 'application/json':
            return response

        return response

    def create_signature(self, files, recipients, params):
        """
        Create a new Signature request.
        @files
            Files to send
                ex: ['/documents/internet_contract.pdf', ... ]
        @recipients
            A dictionary with the email and fullname of the person you want to sign.
            If you wanna send only to one person:
               - [{"email": "john_doe@gmail.com", "fullname": "John"}]
            For multiple recipients, yo need to submit a list of dicts:
               - [{"email": "john_doe@gmail.com", "fullname": "John"}, {"email":"bob@gmail.com", "fullname": "Bob"}]
        @params: An array of params
        """
        parameters = {}

        parser = Parser()

        recipients = recipients if isinstance(recipients, list) else [recipients]

        index = 0
        for recipient in recipients:
            parser.fill_array(parameters, recipient, 'recipients[%i]' % index)

            index += 1

        parser.fill_array(parameters, params, '')

        documents = {}

        parser.fill_array(documents, files, 'files')

        connection = Connection(self.token)
        connection.set_url(self.production, self.SIGNS_URL)
        connection.add_params(parameters)
        connection.add_files(documents)

        return connection.post_request()

    def cancel_signature(self, signature_id):
        """
        Cancel a concrete Signature
        @signature_id: Id of signature
        @return Signature data
        """
        connection = Connection(self.token)

        connection.set_url(self.production, self.SIGNS_CANCEL_URL % signature_id)

        return connection.patch_request()

    def send_signature_reminder(self, signature_id):
        """
        Send a reminder email
        @signature_id: Id of signature
        @document_id: Id of document
        """
        connection = Connection(self.token)

        connection.set_url(self.production, self.SIGNS_SEND_REMINDER_URL % signature_id)

        return connection.post_request()

    def get_branding(self, branding_id):
        """
        Get a concrete branding
        @branding_id: Id of the branding to fetch
        @return Branding
        """
        connection = Connection(self.token)

        connection.set_url(self.production, self.BRANDINGS_ID_URL % branding_id)

        return connection.get_request()

    def get_brandings(self):
        """
        Get all account brandings
        @return List of brandings
        """
        connection = Connection(self.token)

        connection.set_url(self.production, self.BRANDINGS_URL)

        return connection.get_request()

    def create_branding(self, params):
        """
        Create a new branding
        @params: An array of params (all params are optional)
            - layout: Default color for all application widgets (hex code)
            - text: Default text color for all application widgets (hex code)
            - application_texts: A dict with the new text values
            - sign_button: Text for sign button
            - send_button: Text for send button
            - decline_button: Text for decline button:
            - decline_modal_title: Title for decline modal (when you click decline button)
            - decline_modal_body: Body for decline modal (when you click decline button)
            - photo: Photo message text, which tells the user that a photo is needed in the current process
            - multi_pages: Header of the document, which tells the user the number of pages to sign
            ex: { 'photo': 'Hey! Take a photo of yourself to validate the process!'}
        """
        connection = Connection(self.token)

        connection.add_header('Content-Type', 'application/json')
        connection.set_url(self.production, self.BRANDINGS_URL)
        connection.add_params(params, json_format=True)

        return connection.post_request()

    def update_branding(self, branding_id, params):
        """
        Update a existing branding
        @branding_id: Id of the branding to update
        @params: Same params as method create_branding, see above
        @return: A dict with updated branding data
        """
        connection = Connection(self.token)

        connection.add_header('Content-Type', 'application/json')
        connection.set_url(self.production, self.BRANDINGS_ID_URL % branding_id)
        connection.add_params(params)

        return connection.patch_request()

    def get_templates(self, limit=100, offset=0):
        """
        Get all account templates
        """
        url = self.TEMPLATES_URL + "?limit=%s&offset=%s" % (limit, offset)

        connection = Connection(self.token)

        connection.set_url(self.production, url)

        return connection.get_request()

    def get_emails(self, limit=100, offset=0, conditions={}):
        """
        Get all certified emails
        """
        url = self.EMAILS_URL + "?limit=%s&offset=%s" % (limit, offset)

        for key, value in conditions.items():
            if key is 'ids':
                value = ",".join(value)

            url += '&%s=%s' % (key, value)

        connection = Connection(self.token)
        connection.set_url(self.production, url)

        return connection.get_request()

    def count_emails(self, conditions={}):
        """
        Count all certified emails
        """
        url = self.EMAILS_COUNT_URL + "?"

        for key, value in conditions.items():
            if key is 'ids':
                value = ",".join(value)

            url += '&%s=%s' % (key, value)

        connection = Connection(self.token)
        connection.set_url(self.production, url)
        connection.set_url(self.production, url)

        return connection.get_request()

    def get_email(self, email_id):
        """
        Get a specific email
        """
        connection = Connection(self.token)

        connection.set_url(self.production, self.EMAILS_ID_URL % email_id)

        return connection.get_request()

    def download_email_audit_trail(self, email_id, certificate_id):
        connection = Connection(self.token)

        connection.set_url(self.production, self.EMAILS_AUDIT_TRAIL % (email_id, certificate_id))

        response, headers = connection.file_request()

        if headers['content-type'] == 'application/json':
            return response

        return response

    def create_email(self, files, recipients, subject, body, params={}):
        """
        Create a new certified email

        @files
             Files to send
                ex: ['/documents/internet_contract.pdf', ... ]
        @recipients
            A dictionary with the email and fullname of the person you want to sign.
            If you wanna send only to one person:
               - [{"email": "john_doe@gmail.com", "fullname": "John"}]
            For multiple recipients, yo need to submit a list of dicts:
               - [{"email": "john_doe@gmail.com", "fullname": "John"}, {"email":"bob@gmail.com", "fullname": "Bob"}]
        @subject
            Email subject
        @body
            Email body
        @params
        """
        parameters = {}

        parser = Parser()

        documents = {}

        parser.fill_array(documents, files, 'files')

        recipients = recipients if isinstance(recipients, list) else [recipients]

        index = 0
        for recipient in recipients:
            parser.fill_array(parameters, recipient, 'recipients[%i]' % index)

            index += 1

        parser.fill_array(parameters, params, '')

        parameters['subject'] = subject
        parameters['body'] = body

        connection = Connection(self.token)
        connection.set_url(self.production, self.EMAILS_URL)
        connection.add_params(parameters)
        connection.add_files(documents)

        return connection.post_request()
