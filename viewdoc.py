import sys
import traceback
from os.path import basename

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from sphinx.util.compat import Directive
from docutils import nodes, statemachine
from docutils.parsers.rst.directives import unchanged


class ViewDirective(Directive):

    has_content = False
    required_arguments = 1

    option_spec = dict(extra=unchanged, method=unchanged)

    def run(self):
        oldStdout, sys.stdout = sys.stdout, StringIO()

        tab_width = self.options.get(
            'tab-width', self.state.document.settings.tab_width)
        source = self.state_machine.input_lines.source(
            self.lineno - self.state_machine.input_offset - 1)

        extra = self.options.get('extra', '{}')
        method = self.options.get('method')
        code = [
            "from django.core.urlresolvers import reverse",
            "print '::'",
            "print",
            "print reverse(%s, kwargs=%s)" % (self.arguments[0], extra)
        ]
        if method:
            method_line = "print '**%s**::'" % method
            code[1] = method_line
        try:
            exec('\n'.join(code))
            text = sys.stdout.getvalue()
            lines = statemachine.string2lines(
                text, tab_width, convert_whitespace=True)
            self.state_machine.insert_input(lines, source)
            return []
        except Exception:
            error_src = (
                "Unable to execute python code at %s:%d:" % (
                    basename(source), self.lineno)
            )
            trace = '\n'.join(traceback.format_exception(*sys.exc_info()))
            return [
                nodes.error(
                    None,
                    nodes.paragraph(text=error_src),
                    nodes.literal_block(text=trace)
                )
            ]
        finally:
            sys.stdout = oldStdout


def setup(app):
    app.add_directive('endpoint', ViewDirective)
