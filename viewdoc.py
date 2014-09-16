# Sphinx/Docutils
from docutils.parsers.rst.directives import unchanged
# Internal
from pyexec import PyExecDirective


class ViewDirective(PyExecDirective):

    has_content = False
    required_arguments = 1

    option_spec = dict(extra=unchanged, method=unchanged)

    def run(self):
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

        return self.exec_to_state_machine(code)


def setup(app):
    app.add_directive('endpoint', ViewDirective)
