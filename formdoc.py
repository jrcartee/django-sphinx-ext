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

from django.forms import fields
from django.forms.models import ModelChoiceField, ModelMultipleChoiceField


class FormDirective(Directive):
    has_content = False
    required_arguments = 2
    option_spec = dict(
        exclude=unchanged,
        error_dict=unchanged,
        prep_kwargs=unchanged,
        kwargs=unchanged
    )

    def run(self):
        oldStdout, sys.stdout = sys.stdout, StringIO()

        # get the path to this rST source file
        source = self.state_machine.input_lines.source(
            self.lineno - self.state_machine.input_offset - 1)
        # Number of spaces to indent on output
        tab_width = self.options.get(
            'tab-width', self.state.document.settings.tab_width)
        # fields excluded from the table
        exclude = self.options.get('exclude', [])
        # name of dict storing extra errors for the form
        err_dict = self.options.get('error_dict', 'err_set')
        # stuff required to initialize an instance of the form
        prep_code = self.options.get('prep_kwargs', "")
        form_kwargs = self.options.get('kwargs', {})

        code = [
            "from %s import %s as form" % (
                self.arguments[0], self.arguments[1],),
            "%s" % prep_code,
            "form = form(**%s)" % form_kwargs,
            "print ",
            "form_documenter(form, %s)" % (exclude),
            "print ",
            "form_err_doc(form, '%s')" % err_dict
        ]
        try:
            exec('\n'.join(code))
            # convert the multi-line string into a
            #   a list of single-line strings
            lines = statemachine.string2lines(
                sys.stdout.getvalue(),
                tab_width, convert_whitespace=True)
            # insert the list of strings at the source
            #   of the original directive call
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
    app.add_directive('form', FormDirective)


def form_documenter(form, exclude):
    from tabulate import tabulate
    rows = []
    for field_id in form.fields.iterkeys():
        if field_id not in exclude:
            field = form.fields[field_id]
            field = field_documenter(field)

            rows.append([
                field_id, field['required'],
                field['min'], field['max'],
                field['choices'], field['help']
            ])
    headers = [
        'Field ID', 'Required',
        'Min', 'Max',
        'choices', 'Help Text'
    ]
    print tabulate(rows, headers=headers, tablefmt="grid")
    print
    print (
        "*\*\*Min/Max refers to length for string fields, "
        "and value for number fields*"
    )
    print
    print (
        "*\*\*Choices refer either to:* \n"
        "   - *a choice set if ChoiceField or derivative*\n"
        "   - *field used to select from a queryset if a ModelChoiceField*"
    )


def field_documenter(field):
    data = {
        'required': "",
        'min': "",
        'max': "",
        'choices': "",
        'help_text': ""
    }

    data['required'] = unicode(field.required)
    data['help'] = unicode(field.help_text)

    field_type = type(field)
    if field_type in [
        fields.ChoiceField, fields.TypedChoiceField,
        fields.MultipleChoiceField, fields.TypedMultipleChoiceField
    ]:
        data['choices'] = str([choice[0] for choice in field.choices])
    elif field_type in [ModelChoiceField, ModelMultipleChoiceField]:
        data['choices'] = field.to_field_name if field.to_field_name else 'pk'
    elif field_type in [
        fields.IntegerField, fields.FloatField, fields.DecimalField
    ]:
        data['min'] = str(field.min_value or "")
        data['max'] = str(field.max_value or "")
    elif field_type in [fields.CharField, fields.RegexField, fields.URLField]:
        data['min'] = str(field.min_length or "")
        data['max'] = str(field.max_length or "")
    return data


def form_err_doc(form, err_dict_name):
    if hasattr(form, err_dict_name):
        print 'Additional Possible Errors::'
        print ''
        err_dict = getattr(form, err_dict_name)
        for x in err_dict.itervalues():
            print "- %s" % x
