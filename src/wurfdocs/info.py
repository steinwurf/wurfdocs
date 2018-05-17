#! /usr/bin/env python
# encoding: utf-8

import os


class Info(object):
    """ Stores information about a specific build or settings

    Information is added by different steps in the build / configuration
    process in a write once fashion. Such that we avoid accidental
    overwrites.

    """

    def __init__(self):
        # Because we override __setattr__ we have to call the
        # __setattr__ in the base to avoid recursion
        object.__setattr__(self, 'info', {})

    def __getattr__(self, attribute):
        """ Return the value corresponding to the attribute.
        :param attribute: The name of the attribute to return as a string.
        :return: The attribute value, if the attribute does not exist
            return None
        """
        self._check_key(attribute=attribute)

        if attribute in self.info:
            return self.info[attribute]
        else:
            raise AttributeError("No key {}".format(attribute))

    def __setattr__(self, attribute, value):
        """ Sets a dependency attribute.
        :param attribute: The name of the attribute as a string
        :param value: The value of the attribute
        """
        self._check_key(attribute=attribute)

        if attribute in self.info:
            raise AttributeError("Attribute {} read-only.".format(attribute))
        else:
            self.info[attribute] = value

    def __contains__(self, attribute):
        """ Checks if the attribute is available.
        :return: True if the attribute is available otherwise False
        """
        self._check_key(attribute=attribute)

        return (attribute in self.info)

    def _check_key(self, attribute):
        pass
