from ado.model import Model
from ado.note import Note
from ado.project import Project
from datetime import datetime
import sqlite3

class Task(Model):
    FIELDS = {
        "archived_at" : "timestamp",
        "completed_at" : "timestamp",
        "context" : "text",
        "created_at" : "timestamp",
        "description" : "text",
        "due_at" : "timestamp",
        "name" : "text",
        "project_id" : "integer",
        "worktype" : "text"
    }

    SEARCH_FIELDS = ["name", "description", "context"]

    @classmethod
    def inbox(klass, conn):
        """
        Return all notes still in the 'inbox'
        """
        sql = "select * from %s where project_id IS NULL and archived_at IS NULL" % klass.table_name()
        return [klass.load(conn, row) for row in conn.execute(sql)]

    def assign(self, conn, project):
        """
        Assigns this task to the project passed.
        """
        Task.update(conn, self.id, {'project_id' : project.id})

    def project(self, conn):
        return Project.get(conn, self.project_id)

    def project_name(self, conn):
        if self.project_id:
            return self.project(conn).name
        else:
            return "no project"

    def display_line(self):
        if self.due_at:
            due_at = " (due in %0d days)" % self.days_until_due()
        else:
            due_at = ""
        return "Task %04d. %-30s %-20s (%d days old)%s" % (self.id, self.name, self.context, self.elapsed_days(), due_at)

    def show(self):
        date_fmt = "%A %d %B %Y"
        show_text = []
        show_text.append(self.name + " " + self.context)
        show_text.append("Created %s" % self.created_at.strftime(date_fmt))
        if self.due_at:
            show_text.append("Due %s" % self.due_at.strftime(date_fmt))
        if self.description:
            show_text.append(self.description)

        notes = self.notes()
        if len(notes) > 0:
            show_text.append("Notes for task:")
        for note in notes:
            show_text.append(note.display_line())

        return "\n".join(show_text)

    def notes(self, conn=None):
        if not conn:
            conn = self.conn

        sql = "select * from %s where linked_to_type = 'Task' and linked_to_id = %s" % (Note.table_name(), self.id)
        return [Note.load(conn, row) for row in conn.execute(sql)]
