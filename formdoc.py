import sys
from os.path import basename

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from sphinx.util.compat import Directive
from docutils import nodes, statemachine
from docutils.parsers.rst.directives import unchanged

from django.forms import CharField


class FormDirective(Directive):
    """Execute the specified python code and insert the output into the document"""
    has_content = False
    required_arguments = 2
    option_spec = dict(exclude=unchanged)

    def run(self):
        oldStdout, sys.stdout = sys.stdout, StringIO()

        tab_width = self.options.get('tab-width', self.state.document.settings.tab_width)
        source = self.state_machine.input_lines.source(self.lineno - self.state_machine.input_offset - 1)
        exclude = self.options.get('exclude', [])
        code = [
            "from %s.forms import %s as form"% (self.arguments[0], self.arguments[1],),
            "print ",
            "form_param_doc(form, %s)" % exclude, 
            "print ",
            "form_err_doc(form)"
        ]
        try:
            exec('\n'.join(code))
            text = sys.stdout.getvalue()
            lines = statemachine.string2lines(text, tab_width, convert_whitespace=True)
            self.state_machine.insert_input(lines, source)
            return []
        except Exception:
            return [
                nodes.error(None, 
                nodes.paragraph(
                    text="Unable to execute python code at %s:%d:" % (basename(source), self.lineno)), 
                nodes.paragraph(
                    text=str(sys.exc_info()[1])))]
        finally:
            sys.stdout = oldStdout

def setup(app):
    app.add_directive('form', FormDirective)


def form_param_doc(form, exclude):
    from tabulate import tabulate
    output = []
    for field_id in form.base_fields.keys():
        if field_id not in exclude:
            field = form.base_fields[field_id]
            
            if hasattr(field, 'min_value') or hasattr(field, 'max_value'):
                description = "integer"

                min_value = field.min_value
                min_value = str(min_value) if type(min_value) is int else 'n'

                max_value = field.max_value
                max_value = str(max_value) if type(max_value) is int else 'n'

                bounds = 'min(%s) / max(%s)' % (min_value, max_value)

            elif hasattr(field, 'min_length') or hasattr(field, 'max_length'):
                description = "string"

                min_length = field.min_length
                min_length = str(min_length) if type(min_length) is int else 'n'

                max_length = field.max_length
                max_length = str(max_length) if type(max_length) is int else 'n'
                
                bounds = 'min(%s) / max(%s)' % (min_length, max_length)

            else:
                description = '(other)'
                bounds = 'n/a'
                
            required = 'True' if field.required else 'False'
            help_text = field.help_text

            output.insert(-1, (
                field_id, description, required, bounds, help_text
            ))
    headers = ['Field ID', 'Type', 'Required', 'Value/Length Bounds', 'Description']
    print tabulate(output, headers=headers, tablefmt="grid")

def form_err_doc(form):
    from pprint import pprint
    if hasattr(form, 'err_set'):
        print 'Additional Possible Errors::'
        print ''
        for x in form.err_set.values():
            print "- %s" % x