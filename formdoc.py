import sys
from os.path import basename

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from sphinx.util.compat import Directive
from docutils import nodes, statemachine

class FormDirective(Directive):
    """Execute the specified python code and insert the output into the document"""
    has_content = False
    required_arguments = 2

    def run(self):
        oldStdout, sys.stdout = sys.stdout, StringIO()

        tab_width = self.options.get('tab-width', self.state.document.settings.tab_width)
        source = self.state_machine.input_lines.source(self.lineno - self.state_machine.input_offset - 1)
        code = [
            "from %s.forms import %s as form"% (self.arguments[0], self.arguments[1],),
            "print ''",
            "form_param_doc(form)", 
            "print ''",
            "form_err_doc(form)"
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
    app.add_directive('form', FormDirective)


def form_param_doc(form):
    from tabulate import tabulate
    output = []
    for field in form.base_fields.keys():
        output.insert(-1, (
                    field,
                    'True' if form.base_fields[field].required else 'False',
                    unicode(form.base_fields[field].__dict__.get('max_length', 'N/A')),
                    unicode(form.base_fields[field].__dict__.get('min_value', 'N/A')),
                    unicode(form.base_fields[field].__dict__.get('max_value', 'N/A')),
                    unicode(form.base_fields[field].help_text)
            ))
    headers = [
        'Field ID', 'Required', 
        'Max Length', 'Min Value', 'Max Value', 
        'Description']
    print tabulate(output, headers=headers, tablefmt="grid")

def form_err_doc(form):
    from pprint import pprint
    if hasattr(form, 'err_set'):
        print 'Additional Possible Errors::'
        print ''
        for x in form.err_set.values():
            print "- %s" % x