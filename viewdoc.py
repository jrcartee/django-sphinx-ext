import sys
from os.path import basename

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from sphinx.util.compat import Directive
from docutils import nodes, statemachine
from docutils.parsers.rst.directives import unchanged

class ViewDirective(Directive):
    """Execute the specified python code and insert the output into the document"""
    has_content = False
    required_arguments = 1


    option_spec = dict(extra=unchanged)

    def run(self):
        oldStdout, sys.stdout = sys.stdout, StringIO()

        tab_width = self.options.get('tab-width', self.state.document.settings.tab_width)
        source = self.state_machine.input_lines.source(self.lineno - self.state_machine.input_offset - 1)

        extra = self.options.get('extra', '{}')
        code = [
            "from django.core.urlresolvers import reverse",
            "print '::'",
            "print",
            "print reverse(%s, kwargs=%s)" % (self.arguments[0], extra)
        ]
        try:
            exec('\n'.join(code))
            text = sys.stdout.getvalue()
            lines = statemachine.string2lines(text, tab_width, convert_whitespace=True)
            self.state_machine.insert_input(lines, source)
            return []
        except Exception:
            return [nodes.error(None, nodes.paragraph(text = "Unable to execute python code at %s:%d:" % (basename(source), self.lineno)), nodes.paragraph(text = str(sys.exc_info()[1])))]
        finally:
            sys.stdout = oldStdout

def setup(app):
    app.add_directive('endpoint', ViewDirective)

