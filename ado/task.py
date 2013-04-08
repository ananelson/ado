from ado.model import Model
from ado.timer import Timer
from datetime import datetime
import ado.note
import ado.project
import sqlite3

class Task(Model):
    FIELDS = {
        "archived_at" : "timestamp",
        "completed_at" : "timestamp",
        "context" : "text",
        "created_at" : "timestamp",
        "description" : "text",
        "due_at" : "timestamp",
        "estimate" : "float",
        "name" : "text",
        "project_id" : "integer",
        "recipe_id" : "integer",
        "worktype" : "text",
        "waiting_for_task_id" : "integer"
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

    def project(self, conn=None):
        if not conn:
            conn = self.conn
        return ado.project.Project.get(conn, self.project_id)

    def project_name(self, conn=None):
        if self.project_id:
            return self.project(conn).name
        else:
            return "no project"

    def name_with_check(self):
        """
        Returns name of task with unicode empty ballot box (if not complete)
        """
        if self.completed_at:
            return u"%s \u2611 %s" % (self.name, self.context)
        elif self.waiting_for_task_id:
            return u"%s \u2612 %s" % (self.name, self.context)
        else:
            return u"%s \u2610 %s" % (self.name, self.context)

    def state(self, conn=None):
        if self.completed_at:
            return "complete"
        elif self.waiting_for_task_id:
            return "waiting"
        else:
            return "active"

    def display_line(self):
        if self.due_at:
            due_at = " (due in %0d days)" % self.days_until_due()
        else:
            due_at = ""

        if self.waiting_for_task_id:
            waiting_for = " (needs %s)" % self.waiting_for_task_id
        else:
            waiting_for = ""

        if self.project_id:
            project = "[%s]" % self.project_name()
        else:
            project = ""

        task_id = self.id
        task_name = self.name
        context = self.context
        return "Task %(task_id)04d) %(task_name)-60s %(context)-15s %(project)s %(due_at)s%(waiting_for)s" % locals()

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

        sql = "select * from %s where linked_to_type = 'Task' and linked_to_id = %s" % (ado.note.Note.table_name(), self.id)
        return [ado.note.Note.load(conn, row) for row in conn.execute(sql)]

    def timers(self, conn=None):
        if not conn:
            conn = self.conn

        sql = "select * from %s where task_id = ?" % (Timer.table_name())
        return [Timer.load(conn, row) for row in conn.execute(sql, [self.id])]

    def total_time(self, conn):
        sql = "select * from %s where started_at IS NOT NULL AND finished_at IS NOT NULL and task_id = ?" % Timer.table_name()
        return sum(Timer.load(conn, row).elapsed_seconds() for row in conn.execute(sql, [self.id]))

    def waiting_for_task(self, conn):
        if self.waiting_for_task_id:
            return Task.get(conn, self.waiting_for_task_id)

    def indent(self, conn=None):
        if not conn:
            conn = self.conn
        if not self.waiting_for_task_id:
            return 0
        else:
            return 1 + self.waiting_for_task(conn).indent()

    def due(self):
        if self.due_at:
            return "%s (%s days left)" % (self.due_at.strftime("%Y-%m-%d"), self.days_until_due())
        else:
            return ""
