# Sphinx/Docutils
from docutils.parsers.rst.directives import unchanged
# Django
from django.forms import fields
from django.forms.models import ModelChoiceField, ModelMultipleChoiceField
# Internal
from pyexec import PyExecDirective


class FormDirective(PyExecDirective):
    has_content = False
    required_arguments = 2
    option_spec = dict(
        exclude=unchanged,
        error_dict=unchanged,
        prep_kwargs=unchanged,
        kwargs=unchanged
    )

    def run(self):
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
            "self.form_documenter(form, %s)" % (exclude),
            "print ",
            "self.form_err_documenter(form, '%s')" % err_dict
        ]

        return self.exec_to_state_machine(code)

    def form_documenter(self, form, exclude):
        from tabulate import tabulate
        rows = []
        for field_id in form.fields.iterkeys():
            if field_id not in exclude:
                field = form.fields[field_id]
                field = self.field_documenter(field)

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

    def field_documenter(self, field):
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
        elif field_type in [
            fields.CharField, fields.RegexField, fields.URLField
        ]:
            data['min'] = str(field.min_length or "")
            data['max'] = str(field.max_length or "")
        return data

    def form_err_documenter(self, form, err_dict_name):
        if hasattr(form, err_dict_name):
            print 'Additional Possible Errors::'
            print ''
            err_dict = getattr(form, err_dict_name)
            for x in err_dict.itervalues():
                print "- %s" % x


def setup(app):
    app.add_directive('form', FormDirective)
