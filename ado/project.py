import ado.model
import ado.task
import ado.note
from datetime import datetime

class Project(ado.model.Model):
    FIELDS = {
        "archived_at" : "timestamp",
        "completed_at" : "timestamp",
        "created_at" : "timestamp",
        "description" : "text",
        "due_at" : "timestamp",
        "name" : "text",
        "parent_project_id" : "integer",
        "portfolio_id" : "integer"
    }

    SEARCH_FIELDS = ["name", "description"]

    @classmethod
    def all_nested_subprojects(klass, conn):
        projects = []

        sql = "select * from %s where parent_project_id IS NULL and archived_at IS NULL" % klass.table_name()

        def append_self_and_children(project):
            projects.append(project)
            sql = "select * from %s where parent_project_id = ? and archived_at IS NULL" % klass.table_name()
            for row in conn.execute(sql, [project.id]):
                child_project = klass.load(conn, row)
                append_self_and_children(child_project)

        for row in conn.execute(sql):
            parent_project = klass.load(conn, row)
            append_self_and_children(parent_project)

        return projects

    def create_subproject(self, name, description=None, conn=None):
        """
        Create a subproject of this project.
        """
        if not conn:
            conn = self.conn

        subproject = Project.create(
                conn,
                created_at = datetime.now(),
                description = description,
                parent_project_id = self.id,
                name=name,
                portfolio_id = self.portfolio_id
                )

        return subproject

    def create_task(self, name, context, description=None, due_at=None, estimate=None, worktype=None, conn=None):
        """
        Create a task for this project.
        """
        if not conn:
            conn = self.conn

        task = ado.task.Task.create(
                conn,
                due_at=due_at,
                name=name,
                context=context,
                description=description,
                estimate=estimate,
                project_id=self.id,
                worktype=worktype,
                created_at = datetime.now()
                )

        return task

    def notes(self, conn=None):
        if not conn:
            conn = self.conn

        sql = "select * from %s where linked_to_type = 'Project' and linked_to_id = %s" % (ado.note.Note.table_name(), self.id)
        return [ado.note.Note.load(conn, row) for row in conn.execute(sql)]

    def open_tasks(self, conn=None):
        if not conn:
            conn = self.conn

        sql = "select * from %s where project_id = %s and archived_at IS NULL and completed_at IS NULL" % (ado.task.Task.table_name(), self.id)
        return [ado.task.Task.load(conn, row) for row in conn.execute(sql)]

    def tasks(self, conn=None):
        if not conn:
            conn = self.conn

        sql = "select * from %s where project_id = %s and archived_at IS NULL" % (ado.task.Task.table_name(), self.id)
        return [ado.task.Task.load(conn, row) for row in conn.execute(sql)]

    def display_line(self):
        if self.due_at:
            due_at = " (due in %0d days)" % self.days_until_due()
        else:
            due_at = ""

        if self.parent_project_id:
            parent_project_description = ", subproject of %s" % self.parent_project_id
        else:
            parent_project_description = ""

        spaces = "  " * self.indent()
        indented_start = spaces + "Project %04d" % self.id

        return "%-20s %-40s (in %s%s)%s" % (indented_start, self.name, self.portfolio().name, parent_project_description, due_at)

    def validate_complete(self, conn):
        return (len(self.open_tasks()) == 0)

    def show(self):
        show_text = []
        show_text.append("Project %s: %s" % (self.id, self.name))
        if self.description:
            show_text.append(self.description)
        show_text.append("Elapsed days %s, Created at %s" % (self.elapsed_days(), self.created_at))
        notes = self.notes()
        if len(notes) > 0:
            show_text.append("Notes for project:")
        for note in notes:
            show_text.append(note.display_line())
        return "\n".join(show_text)

    def portfolio(self, conn=None):
        from ado.portfolio import Portfolio
        if not conn:
            conn = self.conn
        return Portfolio.get(conn, self.portfolio_id)

    def parent_project(self, conn):
        return Project.get(conn, self.parent_project_id)

    def indent(self, conn=None):
        if not conn:
            conn = self.conn
        if not self.parent_project_id:
            return 0
        else:
            return 1 + self.parent_project(conn).indent()

