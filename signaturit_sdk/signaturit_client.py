from signaturit_sdk.resources.connection import Connection
from signaturit_sdk.resources.parser import Parser

class SignaturitClient:
    BRANDINGS_URL = '/v3/brandings.json'
    BRANDINGS_ID_URL = '/v3/brandings/%s.json'

    CONTACTS_URL = '/v3/contacts.json'
    CONTACTS_ID_URL = '/v3/contacts/%s.json'

    EMAILS_URL = '/v3/emails.json'
    EMAILS_COUNT_URL = '/v3/emails/count.json'
    EMAILS_ID_URL = '/v3/emails/%s.json'
    EMAILS_AUDIT_TRAIL = '/v3/emails/%s/certificates/%s/download/audit_trail'

    PACKAGES_URL = '/v3/packages.json'
    PACKAGES_ID_URL = '/v3/packages/%s.json'
    PACKAGES_SIGNATURE_URL = '/v3/packages/signatures.json'
    PACKAGES_EMAIL_URL = '/v3/packages/emails.json'
    PACKAGES_SMS_URL = '/v3/packages/sms.json'
    PACKAGES_AUDIT_TRAIL_URL = '/v3/packages/%s/download/audit_trail'

    PRODUCTION = True

    SMS_URL = '/v3/sms.json'
    SMS_COUNT_URL = '/v3/sms/count.json'
    SMS_ID_URL = '/v3/sms/%s.json'
    SMS_AUDIT_TRAIL = '/v3/sms/%s/certificates/%s/download/audit_trail'

    SUBSCRIPTIONS_URL = '/v3/subscriptions.json'
    SUBSCRIPTIONS_COUNT_URL = '/v3/subscriptions/count.json'
    SUBSCRIPTIONS_ID_URL = '/v3/subscriptions/%s.json'

    SIGNS_URL = '/v3/signatures.json'
    SIGNS_CANCEL_URL = '/v3/signatures/%s/cancel.json'
    SIGNS_COUNT_URL = '/v3/signatures/count.json'
    SIGNS_ID_URL = '/v3/signatures/%s.json'
    SIGNS_DOCUMENTS_AUDIT_URL = '/v3/signatures/%s/documents/%s/download/audit_trail'
    SIGNS_DOCUMENTS_SIGNED_URL = '/v3/signatures/%s/documents/%s/download/signed'
    SIGNS_SEND_REMINDER_URL = '/v3/signatures/%s/reminder.json'

    TEMPLATES_URL = '/v3/templates.json'

    TEAM_USERS_URL = '/v3/team/users.json'
    TEAM_SEATS_URL = '/v3/team/seats.json'
    TEAM_SEATS_ID_URL = '/v3/team/seats/%s.json'
    TEAM_USERS_ID_URL = '/v3/team/users/%s.json'
    TEAM_MANAGERS_URL = '/v3/team/groups/%s/managers/%s.json'
    TEAM_MEMBERS_URL = '/v3/team/groups/%s/members/%s.json'
    TEAM_GROUPS_URL = '/v3/team/groups.json'
    TEAM_GROUPS_ID_URL = '/v3/team/groups/%s.json'

    def __init__(self, token, production=False):
        self.token = token
        self.production = production

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

    def get_signature(self, signature_id):
        """
        Get a concrete Signature
        @return Signature data
        """
        connection = Connection(self.token)
        connection.set_url(self.production, self.SIGNS_ID_URL % signature_id)

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

        files = files if isinstance(files, list) else [files]

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

    def count_SMS(self, conditions={}):
        """
        Count all certified sms
        """
        url = self.SMS_COUNT_URL + "?"

        for key, value in conditions.items():
            if key is 'ids':
                value = ",".join(value)

            url += '&%s=%s' % (key, value)

        connection = Connection(self.token)
        connection.set_url(self.production, url)
        connection.set_url(self.production, url)

        return connection.get_request()

    def get_SMS(self, limit=100, offset=0, conditions={}):
        """
        Get all certified sms
        """
        url = self.SMS_URL + "?limit=%s&offset=%s" % (limit, offset)

        for key, value in conditions.items():
            if key is 'ids':
                value = ",".join(value)

            url += '&%s=%s' % (key, value)

        connection = Connection(self.token)
        connection.set_url(self.production, url)

        return connection.get_request()

    def get_single_SMS(self, sms_id):
        """
        Get a specific sms
        """
        connection = Connection(self.token)

        connection.set_url(self.production, self.SMS_ID_URL % sms_id)

        return connection.get_request()

    def download_SMS_audit_trail(self, sms_id, certificate_id):
        connection = Connection(self.token)

        connection.set_url(self.production, self.SMS_AUDIT_TRAIL % (sms_id, certificate_id))

        response, headers = connection.file_request()

        if headers['content-type'] == 'application/json':
            return response

        return response

    def create_SMS(self, files, recipients, body, params={}):
        """
        Create a new certified sms

        @files
             Files to send
                ex: ['/documents/internet_contract.pdf', ... ]
        @recipients
            A dictionary with the phone and name of the person you want to sign. Phone must be always with prefix
            If you wanna send only to one person:
               - [{"phone": "34123456", "name": "John"}]
            For multiple recipients, yo need to submit a list of dicts:
               - [{"email": "34123456, "name": "John"}, {"email":"34654321", "name": "Bob"}]
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

        parameters['body'] = body

        connection = Connection(self.token)
        connection.set_url(self.production, self.SMS_URL)
        connection.add_params(parameters)
        connection.add_files(documents)

        return connection.post_request()

    def get_users(self, limit=100, offset=0):
        """
        Get all users from your current team
        """
        url = self.TEAM_USERS_URL + "?limit=%s&offset=%s" % (limit, offset)

        connection = Connection(self.token)
        connection.set_url(self.production, url)

        return connection.get_request()

    def get_seats(self, limit=100, offset=0):
        """
        Get all seats from your current team
        """
        url = self.TEAM_SEATS_URL + "?limit=%s&offset=%s" % (limit, offset)

        connection = Connection(self.token)
        connection.set_url(self.production, url)

        return connection.get_request()

    def get_user(self, user_id):
        """
           Get a single user
        """
        url = self.TEAM_USERS_ID_URL % user_id

        connection = Connection(self.token)
        connection.set_url(self.production, url)

        return connection.get_request()

    def invite_user(self, email, role):
        """
        Send an invitation to email with a link to join your team
        :param email: Email to add to your team
        :param role: Can be admin or member
        """
        parameters = {
            'email': email,
            'role': role
        }

        connection = Connection(self.token)
        connection.set_url(self.production, self.TEAM_USERS_URL)
        connection.add_params(parameters)

        return connection.post_request()

    def change_user_role(self, user_id, role):
        """
        Change role of current user
        :param user_id: Id of user
        :param role: Can be admin or member
        """
        parameters = {
            'role': role
        }

        url = self.TEAM_USERS_ID_URL % user_id

        connection = Connection(self.token)
        connection.set_url(self.production, url)
        connection.add_params(parameters)

        return connection.patch_request()

    def remove_user(self, user_id):
        """
        Remove a user from your team
        :param user_id: Id of user
        """

        url = self.TEAM_USERS_ID_URL % user_id

        connection = Connection(self.token)
        connection.set_url(self.production, url)

        return connection.delete_request()

    def remove_seat(self, seat_id):
        """
        Remove a seat from your team
        :param seat_id: Id of user
        """

        url = self.TEAM_SEATS_ID_URL % seat_id

        connection = Connection(self.token)
        connection.set_url(self.production, url)

        return connection.delete_request()

    def get_groups(self, limit=100, offset=0):
        """
        Get all groups from your current team
        """
        url = self.TEAM_GROUPS_URL + "?limit=%s&offset=%s" % (limit, offset)

        connection = Connection(self.token)
        connection.set_url(self.production, url)

        return connection.get_request()

    def get_group(self, group_id):
        """
        Get a single group
        """
        url = self.TEAM_GROUPS_ID_URL % group_id

        connection = Connection(self.token)
        connection.set_url(self.production, url)

        return connection.get_request()

    def create_group(self, name):
        """
        Create group
        :param name: Group name
        """
        parameters = {
            'name': name
        }

        url = self.TEAM_GROUPS_URL

        connection = Connection(self.token)
        connection.set_url(self.production, url)
        connection.add_params(parameters)

        return connection.post_request()

    def update_group(self, group_id, name):
        """
        Change group name
        :param group_id: Id of group
        :param name: Group name
        """
        parameters = {
            'name': name
        }

        url = self.TEAM_GROUPS_ID_URL % group_id

        connection = Connection(self.token)
        connection.set_url(self.production, url)
        connection.add_header('Content-Type', 'application/json')
        connection.add_params(parameters)

        return connection.patch_request()

    def delete_group(self, group_id):
        """
        Remove a group from your team
        :param group_id: Id of group
        """

        url = self.TEAM_GROUPS_ID_URL % group_id

        connection = Connection(self.token)
        connection.set_url(self.production, url)

        return connection.delete_request()

    def add_member_to_group(self, group_id, user_id):
        """
        Add a user to a group as a member
        :param group_id:
        :param user_id:
        """
        url = self.TEAM_MEMBERS_URL % (group_id, user_id)

        connection = Connection(self.token)
        connection.set_url(self.production, url)

        return connection.post_request()

    def remove_member_from_group(self, group_id, user_id):
        """
        Add a user to a group as a member
        :param group_id:
        :param user_id:
        """
        url = self.TEAM_MEMBERS_URL % (group_id, user_id)

        connection = Connection(self.token)
        connection.set_url(self.production, url)

        return connection.delete_request()

    def add_manager_to_group(self, group_id, user_id):
        """
        Add a user to a group as a member
        :param group_id:
        :param user_id:
        """
        url = self.TEAM_MANAGERS_URL % (group_id, user_id)

        connection = Connection(self.token)
        connection.set_url(self.production, url)

        return connection.post_request()

    def remove_manager_from_group(self, group_id, user_id):
        """
        Add a user to a group as a member
        :param group_id:
        :param user_id:
        """
        url = self.TEAM_MANAGERS_URL % (group_id, user_id)

        connection = Connection(self.token)
        connection.set_url(self.production, url)

        return connection.delete_request()

    def get_subscriptions(self, limit=100, offset=0, params={}):
        """
        Get all subscriptions
        """
        url = self.SUBSCRIPTIONS_URL + "?limit=%s&offset=%s" % (limit, offset)

        for key, value in params.items():
            if key is 'ids':
                value = ",".join(value)

            url += '&%s=%s' % (key, value)

        connection = Connection(self.token)
        connection.set_url(self.production, url)

        return connection.get_request()

    def count_subscriptions(self, params={}):
        """
        Count all subscriptions
        """
        url = self.SUBSCRIPTIONS_COUNT_URL + '?'

        for key, value in params.items():
            if key is 'ids':
                value = ",".join(value)

            url += '&%s=%s' % (key, value)

        connection = Connection(self.token)
        connection.set_url(self.production, url)

        return connection.get_request()

    def get_subscription(self, subscription_id):
        """
        Get single subscription
        """
        url = self.SUBSCRIPTIONS_ID_URL % subscription_id

        connection = Connection(self.token)
        connection.set_url(self.production, url)

        return connection.get_request()

    def create_subscription(self, url, events):
        """
        Create subscription
        :param events: Events to subscribe
        :param url: Url to send events
        """
        params = {
            'url': url,
            'events': events
        }

        url = self.SUBSCRIPTIONS_URL

        connection = Connection(self.token)
        connection.set_url(self.production, url)
        connection.add_header('Content-Type', 'application/json')
        connection.add_params(params, json_format=True)

        return connection.post_request()

    def update_subscription(self, subscription_id, url=None, events=None):
        """
        Create subscription
        :param subscription_id: Subscription to update
        :param events: Events to subscribe
        :param url: Url to send events
        """
        params = {}

        if url is not None:
            params['url'] = url

        if events is not None:
            params['events'] = events

        url = self.SUBSCRIPTIONS_ID_URL % subscription_id

        connection = Connection(self.token)
        connection.set_url(self.production, url)
        connection.add_header('Content-Type', 'application/json')
        connection.add_params(params)

        return connection.patch_request()

    def delete_subscription(self, subscription_id):
        """
        Delete single subscription
        """
        url = self.SUBSCRIPTIONS_ID_URL % subscription_id

        connection = Connection(self.token)
        connection.set_url(self.production, url)

        return connection.delete_request()

    def get_contacts(self, limit=100, offset=0, params={}):
        """
        Get all account contacts
        """
        url = self.CONTACTS_URL + "?limit=%s&offset=%s" % (limit, offset)

        for key, value in params.items():
            if key is 'ids':
                value = ",".join(value)

            url += '&%s=%s' % (key, value)

        connection = Connection(self.token)
        connection.set_url(self.production, url)

        return connection.get_request()

    def get_contact(self, contact_id):
        """
        Get single contact
        """
        url = self.CONTACTS_ID_URL % contact_id

        connection = Connection(self.token)
        connection.set_url(self.production, url)

        return connection.get_request()

    def create_contact(self, email, name):
        """
        Create a new contact
        :param email: user email
        :param name: user name
        """
        params = {'email': email, 'name': name}

        url = self.CONTACTS_URL

        connection = Connection(self.token)
        connection.set_url(self.production, url)
        connection.add_header('Content-Type', 'application/json')
        connection.add_params(params, json_format=True)

        return connection.post_request()

    def update_contact(self, contact_id, email=None, name=None):
        """
        Update a current contact
        :param contact_id: contact id
        :param email: user email
        :param name: user name
        """
        params = {}

        if email is not None:
            params['email'] = email

        if name is not None:
            params['name'] = name

        url = self.CONTACTS_ID_URL % contact_id

        connection = Connection(self.token)
        connection.set_url(self.production, url)
        connection.add_header('Content-Type', 'application/json')
        connection.add_params(params)

        return connection.patch_request()

    def delete_contact(self, contact_id):
        """
        Delete single contact
        """
        url = self.CONTACTS_ID_URL % contact_id

        connection = Connection(self.token)
        connection.set_url(self.production, url)

        return connection.delete_request()