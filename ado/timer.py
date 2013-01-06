from ado.model import Model
from datetime import datetime

class Timer(Model):
    FIELDS = {
        "task_id" : "integer",
        "started_at" : "timestamp",
        "finished_at" : "timestamp",
        "description" : "text"
    }

    SEARCH_FIELDS = ["description"]

    def task(self, conn):
        return Task.get(conn, self.task_id)

    def elapsed(self):
        """
        how long this timing has been running
        """
        if self.finished_at:
            return self.finished_at - self.started_at
        else:
            return datetime.now() - self.started_at

    @classmethod
    def active_timers(klass, conn):
        sql = "select * from %s where started_at IS NOT NULL and finished_at IS NULL" % klass.table_name()
        return [klass.load(conn, row) for row in conn.execute(sql)]

    @classmethod
    def stop(klass, conn, timer_id):
        klass.update(conn, timer_id, { "finished_at" : datetime.now() })
