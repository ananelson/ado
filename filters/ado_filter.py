from ado.commands import conn
from ado.commands import help_text
from ado.commands import available_commands
from ado.project import Project
from dexy.filters.templating_filters import JinjaFilter

class AdoFilter(JinjaFilter):
    """
    A jinja filter with information from ado content.
    """
    ALIASES = ['adojinja']
    DIRTY = True

    def projects(self):
        return Project.all(conn())

    def ado_help(self, on):
        return help_text(on)

    def commands(self):
        return available_commands()
