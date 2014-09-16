import sys
import traceback
from os.path import basename

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from sphinx.util.compat import Directive
from docutils import nodes, statemachine


class PyExecDirective(Directive):
    """
    Execute the specified python code and insert the output into the document
    """
    has_content = True

    def run(self):
        # Number of spaces to indent on output
        tab_width = self.options.get('tab-width')
        code = self.content
        return self.exec_to_state_machine(code, tab_width)

    def exec_to_state_machine(self, code, tab_width=None):
        oldStdout, sys.stdout = sys.stdout, StringIO()

        if tab_width is None:
            # use default if not given as an option
            tab_width = self.state.document.settings.tab_width

        # get the path to this rST source file
        #   for inserting directly to state_machine
        source = self.state_machine.input_lines.source(
            self.lineno - self.state_machine.input_offset - 1)
        try:
            exec('\n'.join(code))

            # convert the multi-line string from stdout
            #   into a list of single-line strings
            lines = statemachine.string2lines(
                sys.stdout.getvalue(),
                tab_width, convert_whitespace=True)

            # insert the list of strings at the source
            #   of the original directive call
            self.state_machine.insert_input(lines, source)

            return []
        except Exception:
            document = self.state.document
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
                ),
                document.reporter.error(
                    "problem executing python code\n"
                    "-- traceback included in document"
                )
            ]
        finally:
            sys.stdout = oldStdout


def setup(app):
    app.add_directive('pyexec', PyExecDirective)
