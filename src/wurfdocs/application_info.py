#! /usr/bin/env python
# encoding: utf-8

import os

import wurfdocs.info


class ApplicationInfo(wurfdocs.info.Info):
    """ Stores information about a specific build.

    Information is added by different steps in the build process in a
    write once fashion. Such that we avoid accidental overwrites.

    """

    valid_keys = {
        "data_path": "",
        "clone_path": "",
        "virtualenv_root_path": ""
    }

    def _check_key(self, attribute):
        if attribute not in ApplicationInfo.valid_keys.keys():
            raise AttributeError("Invalid attribute key {} valid {}".format(
                attribute, ApplicationInfo.valid_keys.keys()))
