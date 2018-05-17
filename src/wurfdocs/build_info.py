#! /usr/bin/env python
# encoding: utf-8

import os

import wurfdocs.info


class BuildInfo(wurfdocs.info.Info):
    """ Stores information about a specific build.

    Information is added by different steps in the build process in a
    write once fashion. Such that we avoid accidental overwrites.

    """

    valid_keys = {
        "config_file": "filename of the Sphinx configuration \
            file as a string",
        "config_dir": "The directory containing the config_file \
            as a string",
        "config_file_path": "The full path to the config_file \
            as a string",
        "sphinx_env": "Dict like os.environ, but where the PATH and PYTHONPATH \
            variables have been modified to contains the necessary tools \
            for building the docs.",
        "slug": "Human readable name for a specific version of the docs",
        "repository_path": "Path to the repsository",
        "source_path": "Path to the documentation sources",
        "output_path": "Path to the output",
        "type": "The type of build"
    }

    def _check_key(self, attribute):
        if attribute not in BuildInfo.valid_keys.keys():
            raise AttributeError("Invalid attribute key {} valid {}".format(
                attribute, BuildInfo.valid_keys.keys()))
