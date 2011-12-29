from ado.model import Model
from datetime import datetime
import sqlite3

class Project(Model):
    FIELDS = {
        "archived_at" : "timestamp",
        "completed_at" : "timestamp",
        "created_at" : "timestamp",
        "description" : "text",
        "due_at" : "timestamp",
        "name" : "text"
    }

    SEARCH_FIELDS = ["name", "description"]

    def notes(self, conn=None):
        from ado.note import Note
        if not conn:
            conn = self.conn

        sql = "select * from %s where linked_to_type = 'Project' and linked_to_id = %s" % (Note.table_name(), self.id)
        return [Note.load(conn, row) for row in conn.execute(sql)]

    def tasks(self, conn=None):
        from ado.task import Task
        if not conn:
            conn = self.conn

        sql = "select * from %s where project_id = %s" % (Task.table_name(), self.id)
        return [Task.load(conn, row) for row in conn.execute(sql)]

    def display_line(self):
        if self.due_at:
            due_at = " (due in %0d days)" % self.days_until_due()
        else:
            due_at = ""
        return "Project %04d. %-30s (%d days old)%s" % (self.id, self.name, self.elapsed_days(), due_at)

    def validate_complete(self, conn):
        return (len(self.tasks()) == 0)

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
