from ado.commands import available_commands
from ado.commands import conn
from ado.commands import help_text
from ado.note import Note
from ado.portfolio import Portfolio
from ado.project import Project
from ado.task import Task
import dexy.filters.templating

class AdoFilter(dexy.filters.templating.JinjaFilter):
    """
    A jinja filter with information from ado content.
    """
    aliases = ['adojinja']

    def projects(self):
        return Project.all_nested_subprojects(conn())

    def tasks(self, sort_by=None):
        return Task.all(conn(), sort_by)

    def portfolios(self):
        return Portfolio.all(conn())

    def ado_help(self, on):
        return help_text(on)

    def commands(self):
        return available_commands()

    def inbox_notes(self):
        return Note.inbox(conn())

class ReportTemplate(dexy.template.Template):
    """
    Report of ado items.
    """
    aliases = ['adoreport']
