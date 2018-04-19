import os
import json
import pprint
import difflib
import pytest


class Record(object):
    """ The Record object is a small test helper. Working similarly to
        vcrpy etc.

    You give it a recording path (filename) now when calling record(..)
    the following will happen:

    1. If a "recording" already suggests we check to see if the data
       matches
    2. If no "recording" exists we store it in the file.

    The file can be committed to version control. To accept a change in the
    output just delete the existing recording and make a new one.
    """

    def __init__(self, filename, recording_path, mismatch_path):
        """ Create a new instance.

        :param filename: The filename of the recording. Note the extension
            will determine the type of recorder used.
        :param recording_path: The directory to where the recording should
            be stored. E.g. /tmp/record note that typically recordings are
            put under version control.
        :param mismatch_path: The directory to where the mismatched
            recording should be stored. E.g. /tmp/mismatch note these should NOT
            be placed under version control.
        """

        assert os.path.isdir(recording_path)
        assert os.path.isdir(mismatch_path)

        _, extension = os.path.splitext(filename)

        if not extension in extension_map:
            raise NotImplementedError("We have no mapping for {}".format(
                extension))

        recording_path = os.path.join(recording_path, filename)
        mismatch_path = os.path.join(mismatch_path, filename)

        assert recording_path != mismatch_path

        recorder_cls = extension_map[extension]

        self.recorder = recorder_cls(recording_path=recording_path,
                                     mismatch_path=mismatch_path)

    def record(self, data):
        self.recorder.record(data=data)


class RecordError(Exception):
    """Basic exception for errors raised when running commands."""

    def __init__(self, recording_path, recording_data, mismatch_path,
                 mismatch_data):

        # Unified diff expects a list of strings
        recording_lines = recording_data.split('\n')
        mismatch_lines = mismatch_data.split('\n')

        diff = difflib.unified_diff(
            a=recording_lines,
            b=mismatch_lines,
            fromfile=recording_path,
            tofile=mismatch_path)

        # unified_diff(...) returns a generator so we need to force the
        # data by interation - and then convert back to one string
        diff = "\n".join(list(diff))

        result = "Diff:\n{}".format(diff)

        super(RecordError, self).__init__(result)


class TextRecord(object):

    def __init__(self, recording_path, mismatch_path):
        self.recording_path = recording_path
        self.mismatch_path = mismatch_path

    def record(self, data):

        if not os.path.isfile(self.recording_path):

            with open(self.recording_path, 'w') as recording_file:
                recording_file.write(data)

            return

        # A recording exists
        with open(self.recording_path, 'r') as recording_file:
            recording_data = recording_file.read()

        if recording_data == data:
            return

        # There is a recording mismatch
        with open(self.mismatch_path, 'w') as mismatch_file:
            mismatch_file.write(data)

        raise RecordError(
            recording_path=self.recording_path, recording_data=recording_data,
            mismatch_path=self.mismatch_path, mismatch_data=data)


class JsonRecord(TextRecord):

    def __init__(self, recording_path, mismatch_path):
        self.recording_path = recording_path
        self.mismatch_path = mismatch_path

    def record(self, data):

        # Convert the data to json
        data = json.dumps(data, indent=2, sort_keys=True)

        super(JsonRecord, self).record(data=data)


extension_map = {
    '.json': JsonRecord,
    '.rst': TextRecord
}
