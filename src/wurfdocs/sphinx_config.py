#! /usr/bin/env python
# encoding: utf-8

import os


class SphinxConfig(object):
    """ Returns the path the Sphinx conf.py object.

    The reason we've split this into a seperate object is to provide
    extensability e.g. if a project uses a different name for the
    Sphinx conf.py file. Then they can provide a different SphinxConfig
    object to find it.
    """

    def update_build(self, build_info):
        """ Find the Sphinx conf.py file.

        :return: The path to the Sphinx configuration file.
        """
        config_file = 'conf.py'

        for root, _, filenames in os.walk(build_info.repository_path):
            if config_file in filenames:

                build_info.config_file = config_file
                build_info.config_dir = root
                build_info.config_file_path = os.path.join(root, config_file)

                # We assume the that documentation sources are next to the
                # config file
                build_info.source_path = root

                return

        raise RuntimeError("No {} found in {}".format(
            config_file, build_info.repository_path))
