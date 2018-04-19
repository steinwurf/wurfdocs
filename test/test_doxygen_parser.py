import pyquery
import os
import pprint
import mock

import wurfdocs
import wurfdocs.doxygen_parser
import wurfdocs.doxygen_generator
import wurfdocs.run

import record


def generate_coffee_xml(testdirectory):
    """ Test helper - generate the XML. """

    output_dir = testdirectory.mkdir('xml_output')
    coffee_dir = testdirectory.copy_dir('test/data/cpp_coffee')
    src_dir = coffee_dir.join('src')

    generator = wurfdocs.doxygen_generator.DoxygenGenerator(
        runner=wurfdocs.run,
        recursive=True,
        source_path=src_dir.path(),
        output_path=output_dir.path())

    return src_dir.path(), generator.generate()


def test_index_file(testdirectory):

    src_dir, xml_dir = generate_coffee_xml(testdirectory)
    index = wurfdocs.doxygen_parser.DoxygenParser.xml_from_path(
        doxygen_path=xml_dir)

    # There should be multiple "compounddef" elements in the generated
    # XML
    assert len(index) > 0


def test_read_class(testdirectory):

    src_dir, xml_dir = generate_coffee_xml(testdirectory)
    log = mock.Mock()

    parsers = {
        'parse_class': wurfdocs.doxygen_parser.parse_class_or_struct,
    }

    reader = wurfdocs.doxygen_parser.DoxygenParser(
        parsers=parsers, project_path=src_dir, log=log)

    actual_api = reader.parse_api(doxygen_path=xml_dir)

    mismatch_path = testdirectory.mkdir('mismatch')

    recorder = record.Record(
        filename='read_class.json',
        recording_path='test/data/parser_recordings',
        mismatch_path=mismatch_path.path())

    recorder.record(data=actual_api)


def test_read_struct(testdirectory):

    src_dir, xml_dir = generate_coffee_xml(testdirectory)
    log = mock.Mock()

    parsers = {
        'parse_struct': wurfdocs.doxygen_parser.parse_class_or_struct,
    }

    parser = wurfdocs.doxygen_parser.DoxygenParser(
        parsers=parsers, project_path=src_dir, log=log)

    actual_api = parser.parse_api(doxygen_path=xml_dir)

    mismatch_path = testdirectory.mkdir('mismatch')

    recorder = record.Record(
        filename='read_struct.json',
        recording_path='test/data/parser_recordings',
        mismatch_path=mismatch_path.path())

    recorder.record(data=actual_api)


def test_read_function(testdirectory):

    src_dir, xml_dir = generate_coffee_xml(testdirectory)
    log = mock.Mock()

    parsers = {
        'parse_class': wurfdocs.doxygen_parser.parse_class_or_struct,
        'parse_function': wurfdocs.doxygen_parser.parse_function,
    }

    parser = wurfdocs.doxygen_parser.DoxygenParser(
        parsers=parsers, project_path=src_dir, log=log)

    api = parser.parse_api(doxygen_path=xml_dir)

    assert "project::coffee::machine::set_number_cups(uint32_t)" in api
    assert "project::coffee::machine::set_number_cups(std::string)" in api
    assert "project::coffee::machine::number_cups()const" in api
    assert "project::coffee::machine::set(constheat&,int)const" in api
    assert "project::coffee::machine::help_brew()" in api

    # Lets check the api of our set function
    actual_api = api['project::coffee::machine::set(constheat&,int)const']

    mismatch_path = testdirectory.mkdir('mismatch')

    recorder = record.Record(
        filename='read_function.json',
        recording_path='test/data/parser_recordings',
        mismatch_path=mismatch_path.path())

    recorder.record(data=actual_api)
