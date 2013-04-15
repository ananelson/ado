import ado.model
import ado.recipe

class Step(ado.model.Model):
    FIELDS = {
        "archived_at" : "timestamp",
        "created_at" : "timestamp",
        "description" : "text",
        "recipe_id" : "integer"
    }
    SEARCH_FIELDS = ["name", "description"]

class DoingRecipe(ado.model.Model):
    """
    Class to encapsulate the data from doing a recipe.
    """
    FIELDS = {
        "archived_at" : "timestamp",
        "started_at" : "timestamp",
        "completed_at" : "timestamp",
        "recipe_id" : "integer",
        }

    def display_line(self):
        args = (self.__class__.__name__, self.id, self.recipe().name, self.started_at.strftime("%d %b %Y %H:%M"))
        return "%s %4d) %s [%s]" % args

    def steps(self, conn=None):
        if not conn:
            conn = self.conn

        sql = "select * from %s where doing_recipe_id = %s"
        rows = conn.execute(sql % (DoingStep.table_name(), self.id))
        return [DoingStep.load(conn, row) for row in rows]

    def recipe(self, conn=None):
        if not conn:
            conn = self.conn

        sql = "select * from %s where id = %s"
        rows = conn.execute(sql % (ado.recipe.Recipe.table_name(), self.recipe_id))
        for row in rows:
            recipe_id = row
        return ado.recipe.Recipe.load(conn, recipe_id)

class DoingStep(ado.model.Model):
    FIELDS = {
        "archived_at" : "timestamp",
        "started_at" : "timestamp",
        "completed_at" : "timestamp",
        "step_id" : "integer",
        "step_description" : "text",
        "doing_recipe_id" : "integer",
        "description" : "text",
        }
