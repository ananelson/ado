from ado.model import Model
from ado.project import Project
from ado.recipe import Recipe

class Portfolio(Model):
    FIELDS = {
        "alias" : "text",
        "archived_at" : "timestamp",
        "created_at" : "timestamp",
        "description" : "text",
        "name" : "text"
    }

    def projects(self, conn=None):
        if not conn:
            conn = self.conn
        sql = "select * from %s where portfolio_id = ? and archived_at IS NULL" % Project.table_name()
        return [Project.load(conn, row) for row in conn.execute(sql, [self.id])]

    def recipes(self, conn=None):
        if not conn:
            conn = self.conn
        sql = "select * from %s where portfolio_id = ?" % Recipe.table_name()
        return [Recipe.load(conn, row) for row in conn.execute(sql, [self.id])]

    def display_line(self):
        return "Portfolio %02d) %s: %s" % (self.id, self.name, self.description)

    def show(self):
        show_text = []
        show_text.append("Portfolio %s: %s" % (self.id, self.name))
        if self.description:
            show_text.append(self.description)
        return "\n".join(show_text)
