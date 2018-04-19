import os
import mock

import wurfdocs
import wurfdocs.doxygen_generator
import wurfdocs.doxygen_parser
import wurfdocs.template_render

import record


def generate_coffee_api(testdirectory):
    """ Test helper - generate the XML. """

    output_dir = testdirectory.mkdir('xml_output')
    coffee_dir = testdirectory.copy_dir('test/data/cpp_coffee')
    src_dir = coffee_dir.join('src')

    generator = wurfdocs.doxygen_generator.DoxygenGenerator(
        runner=wurfdocs.run,
        recursive=True,
        source_path=src_dir.path(),
        output_path=output_dir.path())

    xml_dir = generator.generate()

    log = mock.Mock()

    reader = wurfdocs.doxygen_parser.DoxygenParser(
        project_path=src_dir.path(), log=log)

    return reader.parse_api(doxygen_path=xml_dir)


def test_template_finder_builtin(testdirectory):

    template = wurfdocs.template_render.TemplateRender(user_path=None)

    api = generate_coffee_api(testdirectory=testdirectory)

    data = template.render(selector="project::coffee::machine", api=api,
                           filename='class_synopsis.rst')

    mismatch_path = testdirectory.mkdir('mismatch')

    recorder = record.Record(
        filename='builtin_class_synopsis.rst',
        recording_path='test/data/template_recordings',
        mismatch_path=mismatch_path.path())

    recorder.record(data=data)


def test_template_finder_user(testdirectory):

    api = generate_coffee_api(testdirectory=testdirectory)

    user_path = testdirectory.copy_file(
        'test/data/custom_templates/class_synopsis.rst')

    template = wurfdocs.template_render.TemplateRender(
        user_path=testdirectory.path())

    data = template.render(selector=None, api=api,
                           filename='class_synopsis.rst')

    expect = r"""custom coffee"""

    assert expect == data


def test_template_render_namespace(testdirectory):

    template = wurfdocs.template_render.TemplateRender(user_path=None)

    api = {
        "test::ok": {
            "briefdescription": "",
            "name": "ok",
            "location": {"file": "ok"}
        }
    }

    data = template.render(selector='test::ok', api=api,
                           filename='namespace_synopsis.rst')

    mismatch_path = testdirectory.mkdir('mismatch')

    recorder = record.Record(
        filename='builtin_namespace_synopsis.rst',
        recording_path='test/data/template_recordings',
        mismatch_path=mismatch_path.path())

    recorder.record(data=data)
