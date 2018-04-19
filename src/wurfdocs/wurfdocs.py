import os

import docutils.nodes
import docutils.parsers
import docutils.parsers.rst
import docutils.parsers.rst.directives
import docutils.statemachine

import sphinx
import sphinx.util
import sphinx.util.logging
import sphinx.util.nodes

import pyquery
import json

from . import doxygen_generator
from . import doxygen_parser
from . import run
from . import template_render
from . import wurfdocs_error

VERSION = '1.0.0'


class WurfDocsDirective(docutils.parsers.rst.Directive):

    # The WurfDocsDirective requires a single path argument, which is allowed to
    # contain whitepace. This is to allow for long paths which may span
    # multiple lines. The path argument should name a valid template.
    #
    # Same approach as for the image directive:
    # http://docutils.sourceforge.net/docs/howto/rst-directives.html#id10
    required_arguments = 1
    final_argument_whitespace = True

    # A selector may be specified. Some templates may require it. @todo
    # document how to handle situations where:
    # 1. A selector is not needed but passed
    # 2. A selector is needed but not passed
    option_spec = {
        # unchanged: Returns the text argument, unchanged. Returns an empty
        # string ("") if no argument is found.
        'selector': docutils.parsers.rst.directives.unchanged
    }

    def run(self):
        """ Called by Sphinx.

        Process the directive.

        Documentation on creating directives are available here:
        http://docutils.sourceforge.net/docs/howto/rst-directives.html

        :return: List of Docutils/Sphinx nodes that will be inserted into the
                 document where the directive was encountered.
        """

        # The path function returns the path argument unwrapped (with newlines
        # removed). Raises ValueError if no argument is found.
        template_path = docutils.parsers.rst.directives.path(self.arguments[0])

        env = self.state.document.settings.env
        app = env.app
        api = app.wurfdocs_api
        selector = self.options["selector"]

        if selector not in api:
            raise wurfdocs_error.WurfdocsError(
                'Selector "{}" not in API possible values are {}'.format(
                    selector, api.keys()))

        template = template_render.TemplateRender(user_path=None)

        data = template.render(
            selector=self.options['selector'], api=app.wurfdocs_api,
            filename=template_path)

        output_path = os.path.join(app.doctreedir, 'wurfdocs')

        with open(os.path.join(output_path, 'tem.rst'), 'w') as w:
            w.write(data)

        return self.insert_rst(data)

    def insert_rst(self, rst):
        """ Replaces the content of the directive with the rst generated
            content.

        Documentation on how to do this is available here:
        http://www.sphinx-doc.org/en/stable/extdev/markupapi.html
        """
        rst = rst.split('\n')
        view = docutils.statemachine.ViewList(initlist=rst, source="wurfdocs")

        node = docutils.nodes.paragraph()
        sphinx.util.nodes.nested_parse_with_titles(
            state=self.state, content=view, node=node)

        return node.children


def main():

    print("hello wurfdocs")


def generate_doxygen(app):

    source_path = os.path.join(app.srcdir,
                               app.config.wurfdocs['source_path'])

    output_path = os.path.join(app.doctreedir, 'wurfdocs')

    if not os.path.exists(output_path):
        os.makedirs(name=output_path)

    logger = sphinx.util.logging.getLogger('wurfdocs')
    logger.info('wurfdocs source_path={} output_path={}'.format(
        source_path, output_path))

    generator = doxygen_generator.DoxygenGenerator(
        runner=run,
        recursive=True,
        source_path=source_path,
        output_path=output_path)

    output = generator.generate()

    logger.info('wurfdocs doxygen XML {}'.format(output))

    parser = doxygen_parser.DoxygenParser(project_path=source_path, log=logger)

    app.wurfdocs_api = parser.parse_api(doxygen_path=output)

    with open(os.path.join(output_path, 'wurfdocs_api.json'), 'w') as f:
        json.dump(app.wurfdocs_api, f)


def setup(app):
    """ Entry point for the extension. Sphinx will call this function when the
        module is added to the "extensions" list in Sphinx's conf.py file.

        :param app: The application object, which is an instance of Sphinx.
    """

    # Create a logger
    logger = sphinx.util.logging.getLogger('wurfdocs')
    logger.info('Initializing wurfdocs extension')

    # Add the wurfdocs configuration value
    app.add_config_value(name='wurfdocs', default=None, rebuild=True)

    # Add the new directive - added to the document by writing:
    #
    #    ..wurfdocs::
    #
    app.add_directive(name='wurfdocs', obj=WurfDocsDirective)

    # Generate the XML
    app.connect(event="builder-inited", callback=generate_doxygen)

    # We use the doctreedir as build directory. The default for this
    # is inside _build/.doctree folder
    build_dir = os.path.join(app.doctreedir, 'wurfdocs')

    # Run Doxygen on the source code

    return {'version': VERSION}
