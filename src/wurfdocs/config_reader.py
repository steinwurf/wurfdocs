import wurfdocs.python_config
import wurfdocs.variables_reader


class ConfigReader(object):

    def __init__(self, config, context):
        """ Create a new config reader.

        :param config: Config object containing the config
        :param context: Dict containing the context
        """
        self.config = config
        self.variables = wurfdocs.variables_reader.VariablesReader(
            variables=config.variables, context=context)

    def __getattr__(self, attribute):

        if not attribute in self.config:
            raise AttributeError("Not found")

        element = self.config[attribute]

        return self._expand(element=element)

    def _expand(self, element):

        if type(element) == str:
            return self.variables.expand(element=element)

        if type(element) == list:

            values = []
            for e in element:
                values.append(self._expand(element=e))

            return values

        return element
