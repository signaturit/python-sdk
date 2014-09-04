class Parser:
    """
    Parser: A class used to parse all the incoming data from user to a request-friendly format.
    The parser also validates that the info is correct and there aren't missing or wrong params.
    """
    def __init__(self, all_params, mandatory_params):
        """
        @all_params: All params that the user can submit in the request. If the param is not here, then, its wrong.
        @mandatory_params: All params that the user must submit in the request.
        """
        self.all = all_params
        self.mandatory = mandatory_params

    def add_mandatory_params(self, mandatory_params):
        """
        Add a new mandatory param in the validation process
        """
        self.mandatory += mandatory_params

    def add_params(self, params):
        """
        Add a new param in the validation process
        """
        self.all += params

    def validate_data(self, params):
        """
        Validate that all the data must be correct (only values in @all_params) and there's no missing mandatory data
        """
        params_submitted = []
        params_required = len(self.mandatory)

        for key, value in params.items():
                if key not in self.all:
                    raise Exception('Invalid key %s' % key)

                if key in self.mandatory:
                    params_submitted.append(key)

        if len(params_submitted) is not params_required:
            diff = list(set(self.mandatory) - set(params_submitted))
            raise Exception('Mandatory keys %s missing' % diff)

    def parse_data(self, params):
        """
        Transform user params to correct values for a api request that upload files too
        @params: Request params
        ex:
            [{'recipients': {'fullname': 'John', 'email': 'john.doe@signatur.it'}}]

            will turn into multi-form like data

            {'recipients[0][fullname]': 'John', 'recipients[0][email]': 'john.doe@signatur.it'}

        @return: The params in form-type format, and the uploaded files
        """
        parsed_params = {}
        parsed_files = {}
        params_submitted = []
        params_required = len(self.mandatory)

        for key, value in params.items():
                if key not in self.all:
                    raise Exception('Invalid key %s' % key)

                if key in self.mandatory:
                    params_submitted.append(key)

                if key is 'files':
                    if isinstance(value, list):
                        for index, element in enumerate(value):
                            parsed_files['%s[%s]' % (key, index)] = open(element, 'rb')
                        continue
                    else:
                        parsed_files[key] = open(value, 'rb')

                if key is 'recipients' and isinstance(value, dict):
                    for inner_key, inner_value in value.items():
                            parsed_params['%s[0][%s]' % (key, inner_key)] = inner_value

                    continue

                if isinstance(value, list):
                    for index, element in enumerate(value):
                        if isinstance(element, dict):
                            for inner_key, inner_value in element.items():
                                parsed_params['%s[%d][%s]' % (key, index, inner_key)] = str(inner_value)

                        else:
                            parsed_params["%s[%d]" % (key, index)] = str(element)

                    continue

                if isinstance(value, dict):
                    for inner_key, inner_value in value.items():
                            parsed_params['%s[%s]' % (key, inner_key)] = str(inner_value)

                    continue

                parsed_params[key] = str(value)

        if len(params_submitted) is not params_required:
            diff = list(set(self.mandatory) - set(params_submitted))
            raise Exception('Mandatory keys %s missing' % diff)

        return parsed_params, parsed_files
