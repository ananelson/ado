from ado.model import Model
from ado.task import Task

class Recipe(Model):
    FIELDS = {
        "archived_at" : "timestamp",
        "based_on" : "integer", # ID of recipe this recipe evolved from, if any
        "context" : "text",
        "description" : "text",
        "frequency" : "integer", # how often this recipe should be done, measured in days
        "name" : "text",
        "portfolio_id" : "integer",
        "recipe" : "text" # The actual instructions for how to perform this recipe.
        }

    def tasks(self, conn=None):
        if not conn:
            conn = self.conn

        sql = "select * from %s where recipe_id = %s" % (Task.table_name(), self.id)
        return [Task.load(conn, row) for row in conn.execute(sql)]

    def last_completed_task(self, conn=None):
        if not conn:
            conn = self.conn
        sql = "select * from %s where recipe_id = %s ORDER BY completed_at DESC LIMIT 1" % (Task.table_name(), self.id)
        last_completed_tasks = [Task.load(conn, row) for row in conn.execute(sql)]
        if len(last_completed_tasks) == 1:
            return last_completed_tasks[0]

    def last_completed_at(self):
        task = self.last_completed_task()
        if task:
            return task.completed_at

    def display_line(self):
        lc = self.last_completed_at()
        if lc:
            lc = lc.strftime("%a %b %d %Y")
        return "Recipe %04d) %-40s %-15s %s" % (self.id, self.name, self.context, lc)
