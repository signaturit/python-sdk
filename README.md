========================
DO NOT USE MASTER BRANCH
========================

Signaturit Python SDK
=====================
This package is a wrapper for Signaturit Api. If you didn't read the documentation yet, maybe it's time to take a look [here](https://docs.signaturit.com/v3).

You can install the package through pip.

```bash
sudo pip install signaturit_sdk
```

Configuration
-------------
Just import the Signaturit Client this way

```python
from signaturit_sdk.signaturit_client import SignaturitClient
```

Then you can authenticate yourself using your AuthToken

```python
client = SignaturitClient('TOKEN')
```

Remember, the default calls are made to our Sandbox server. If you want to do in production, just set the flag when you do the call.

```python
client = SignaturitClient('TOKEN', SignaturitClient.PRODUCTION)
```

Examples
--------

## Signature request

### Get all signature requests

Retrieve all data from your signature requests using different filters.

##### All signatures

```python
response = client.get_signatures()
```

##### Getting the last 50 signatures

```python
response = client.get_signatures(limit=50)
```

##### Getting the following last 50 signatures

```python
response = client.get_signatures(limit=50, offset=50)
```

##### Getting only the finished signatures

```python
response = client.get_signatures(conditions={'status': 3})
```

##### Getting the finished signatures created since July 20th of 2014

```python
response = client.get_signatures(conditions={'since': '2014-7-20', 'status': 3})
```

##### Getting signatures with custom field "crm_id"

```python
response = client.get_signatures(conditions={'crm_id': 'CUSTOM_ID'})
```
##### Getting signatures inside a set of ids

```python
response = client.get_signatures(conditions={'ids': ['ID1', 'ID2]})
```

##### Count signature requests

```python
response = client.count_signatures()
```

##### Get a signature request

```python
response = client.get_signature('SIGNATURE_ID')
```

### Signature request

Create a new signature request. You can check all signature [params](https://docs.signaturit.com/api/v3#sign_create_sign).

```python
recipients =  [{'name': 'Bob', 'email': 'bobsoap@signatur.it'}]
sign_params = {'subject': 'Receipt number 250', 'body': 'Please, can you sign this document?'}
file_path = '/documents/contracts/125932_important.pdf'
response = client.create_signature(file_path, recipients, sign_params)
```

You can enable the security mode, by setting the recipient phone.

```python
recipients =  [{'name': 'Bob', 'email': 'bobsoap@signatur.it', 'phone': 'XXXXX}]'}]
```

Then, the user will receive a SMS in the phone number with a security code, needed to begin the sign process.

And if you have some templates created, you can use them too.

```python
recipients =  [{'name': 'Bob', 'email': 'bobsoap@signatur.it'}]
sign_params = {'subject': 'Receipt number 250', 'body': 'Please, can you sign this document?', 'templates': ['id1',...]}
file_path = []
response = client.create_signature(file_path, recipients, sign_params)
```


You can send templates with the fields filled

```python
recipients =  [{'name': 'Bob', 'email': 'bobsoap@signatur.it'}]
sign_params = {'subject': 'Receipt number 250', 'body': 'Please, can you sign this document?', 'templates': {'TEMPLATE_ID'}, 'data': {'WIDGET_ID': 'DEFAULT_VALUE'}}

response = client.create_signature({}, recipients, sign_params)
```

You can add custom info in your requests

```python
recipients =  [{'name': 'Bob', 'email': 'bobsoap@signatur.it'}]
sign_params = {'subject': 'Receipt number 250', 'body': 'Please, can you sign this document?', 'data': {'crm_id': '45673'}}
file_path = '/documents/contracts/125932_important.pdf'
response = client.create_signature(file_path, recipients, sign_params)
```

##### Cancel signature request

```python
response = client.cancel_signature('SIGNATURE_ID');
```

##### Send reminder email

```python
response = client.send_signature_reminder('SIGNATURE_ID');
```

##### Get audit trail

Get the audit trail of a signature request document

```python
response = client.download_audit_trail('SIGNATURE_ID','DOCUMENT_ID')
```

##### Get signed document

Get the signed document of a signature request document

```python
response = client.download_signed_document('SIGNATURE_ID','DOCUMENT_ID')
```

## Branding

#### Get brandings

Get all account brandings.

```python
response = client.get_brandings()
```

#### Get a single branding

Get a single account branding.

```python
response = client.get_branding('BRANDING_ID')
```

#### Create branding

Create a new account branding. You can check all branding [params](https://docs.signaturit.com/api/v3#set_branding).`

```python
branding_params = {'layout_color': '#FFBF00',
                   'text_color': '#2A1B0A',
                   'application_texts': {'sign_button': 'Sign!'}
}
response = client.create_branding(branding_params)
```

#### Update a single branding

Update a single account branding

```python
branding_params = {'application_texts': {'send_button': 'Send!'}}
response = client.update_branding('BRANDING_ID', branding_params)
```

## Templates

#### Get templates

Retrieve all data from an accounts templates.

```python
response = client.get_templates()
```

## Emails

#### Get emails

Get all certified emails

```python
response = client.get_emails()
```

#### Get last 50 emails

```python
response = client.get_emails(50)
```

#### Navigate through all emails in blocks of 50 results

```python
response = client.get_emails(50, 50)
```

#### Count emails

Count all certified emails

```python
response = client.count_emails()
```

#### Get email

Get a single email

```python
client.get_email('EMAIL_ID')
```

#### Create email

Create a new certified emails.

```python
response = client.create_email(
    [ 'demo.pdf', 'receipt.pdf' ],
    [{'email': 'john.doe@signaturit.com', 'name': 'Mr John'}],
    'Python subject',
    'Python body',
    {}
)
```

#### Get audit trail document

Get the audit trail document of an email request

```python
response = client.download_email_audit_trail('EMAIL_ID','CERTIFICATE_ID')
```

## SMS

### Get sms

#### Get all certified sms

```python
response = client.get_sms()
```

#### Get last 50 sms

```python
response = client.get_sms(50)
```

#### Navigate through all sms in blocks of 50 results

```python
response = client.get_sms(50, 50)
```

#### Count all sms

```python
response = client.count_sms()
```

#### Get single sms

```python
client.get_single_sms('SMS_ID')
```

#### Create a new certified sms.

```python
response = client.create_sms(
    [],
    [{'phone': '34123456', 'name': 'Mr John'}],
    'Python body',
    {}
)
```

#### Get audit trail document

Get the audit trail document of an sms request

```python
response = client.download_sms_audit_trail('SMS_ID','CERTIFICATE_ID')
```

## Team

#### Get users

```python
response = client.get_users()
```

#### Get user

```python
response = client.get_user(USER_ID)
```

#### Invite user to your team

```python
response = client.invite_user('bob.soap@signaturit.com', 'admin')
```

#### Change user role

```python
response = client.change_role(USER_ID, 'member')
```

#### Delete a user from your team

```python
response = client.remove_user(USER_ID)
```

#### Get groups

```python
response = client.get_groups()
```

#### Get group

```python
response = client.get_group(GROUP_ID)
```

#### Create group

```python
response = client.crate_group('SDK group')
```

#### Update group

```python
response = client.update_group(GROUP_ID, 'SDK updated group')
```

#### Delete a group from your team

```python
response = client.delete_group(GROUP_ID)
```

#### Add user to a group as a manager

```python
response = client.add_manager_to_group(GROUP_ID, USER_ID)
```

#### Add user to a group as a member

```python
response = client.add_member_to_group(GROUP_ID, USER_ID)
```

#### Remove user from group managers

```python
response = client.remove_manager_from_group(GROUP_ID, USER_ID)
```

#### Remove user from group members

```python
response = client.remove_members_from_group(GROUP_ID, USER_ID)
```

## Subscriptions

#### Get subscriptions

```python
response = client.get_subscriptions()
```

#### Get subscription

```python
response = client.get_subscription(SUBSCRIPTION_ID)
```

#### Create subscription

```python
response = client.create_subscription('https://example_url.json', ['email_delivered'])
```

#### Update subscription

```python
response = client.update_subscription(subscription_id=SUBSCRIPTION_ID, url='https://new_example_url.json')
```

#### Delete subscription
```python
response = client.delete_subscription(SUBSCRIPTION_ID)
```

## Contacts

#### Get contacts

```python
response = client.get_contacts()
```

#### Get contact

```python
response = client.get_contact(CONTACT_ID)
```

#### Create contact

```python
response = client.create_contact('bob.soap@signaturit.com', 'bob')
```

#### Update contact

```python
response = client.update_contact(contact_id=CONTACT_ID, name='Bob')
```

#### Delete contact
```python
response = client.delete_contact(CONTACT_ID)
```
