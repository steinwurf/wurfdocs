import mock
import os

import wurfdocs
import wurfdocs.doxygen_generator
import wurfdocs.run


def test_doxygen_generator(testdirectory):

    output_dir = testdirectory.mkdir('output')
    coffee_dir = testdirectory.copy_dir('test/data/cpp_coffee')

    runner = mock.Mock()

    generator = wurfdocs.doxygen_generator.DoxygenGenerator(
        runner=wurfdocs.run,
        recursive=True,
        source_path=coffee_dir.path(),
        output_path=output_dir.path())

    xml_output = generator.generate()

    assert output_dir.contains_file('Doxyfile')

    index_xml = os.path.join(xml_output, 'index.xml')
    assert os.path.isfile(index_xml)
