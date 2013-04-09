from ado.commands import available_commands
from ado.commands import conn
from ado.commands import help_text
from ado.note import Note
from ado.recipe import Recipe
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
        """
        Returns help text for the specified command, same as calling "ado help
        -on <on>" on the command line.
        """
        return help_text(on)

    def commands(self):
        """
        Returns a list of all available commands, can be used to iterate over
        help for each command.
        """
        return available_commands()

    def recipes(self):
        return Recipe.all(conn())

    def inbox_notes(self):
        return Note.inbox(conn())

class ReportTemplate(dexy.template.Template):
    """
    Report of ado items.
    """
    aliases = ['adoreport']
