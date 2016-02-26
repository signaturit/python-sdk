class Parser:
    """
    Parser: A class used to parse all the incoming data from user to a request-friendly format.
    The parser also validates that the info is correct and there aren't missing or wrong params.
    """
    def __init__(self):
        pass

    def fill_array(self, form_array, parameters, parent):
        iterable = parameters.items() if isinstance(parameters, dict) else enumerate(parameters)

        for key, value in iterable:
            parent_key = "%s[%s]" % (parent, key) if len(parent) else key

            if isinstance(value, dict):
                self.fill_array(form_array, value, parent_key)
            elif isinstance(value, list):
                self.fill_array(form_array, value, parent_key)
            else:
                if parent is 'files':
                    value = open(value, 'rb')

                form_array[parent_key] = value