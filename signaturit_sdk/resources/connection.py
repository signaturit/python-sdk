import requests
import json


class Connection:
    """
    Class to handle all the GET, POST, PUT, DELETE & PATCH operations
    """
    def __init__(self, token):
        self.__base_url = None
        self.__params = None
        self.__files = None
        self.__headers = {'Authorization': 'Bearer %s' % token, 'user-agent': 'signaturit-python-sdk 1.1.0'}

    def add_header(self, header, value):
        self.__headers[header] = value

    def add_params(self, params, json_format=None):
        if json_format is True:
            self.__params = json.dumps(params)
        else:
            self.__params = params

    def add_files(self, files):
        self.__files = files

    def set_url(self, prod, url):
        if prod is False:
            self.__base_url = 'https://api.sandbox.signaturit.com'
        else:
            self.__base_url = 'https://api.signaturit.com'

        self.__base_url += url

    def get_request(self):
        response = requests.get(
            self.__base_url,
            headers=self.__headers)

        return json.loads(response.text)

    def post_request(self):
        response = requests.post(
            self.__base_url,
            headers=self.__headers,
            files=self.__files,
            data=self.__params
        )

        return json.loads(response.text)

    def put_request(self):
        raw = self.__files['files'].read()

        response = requests.put(
            self.__base_url,
            headers=self.__headers,
            data=raw)

        return json.loads(response.text)

    def delete_request(self):
        response = requests.delete(
            self.__base_url,
            headers=self.__headers)

        return json.loads(response.text)

    def patch_request(self):
        response = requests.patch(
            self.__base_url,
            headers=self.__headers,
            data=json.dumps(self.__params))

        return json.loads(response.text)

    def file_request(self):
        """
        Request that retrieve a binary file
        """
        response = requests.get(
            self.__base_url,
            headers=self.__headers,
            stream=True)

        return response.raw.read(), response.headers
