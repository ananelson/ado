import ado.model
from ado.survey_data import SurveyData

class Survey(ado.model.Model):
    FIELDS = {
        "archived_at" : "timestamp",
        "created_at" : "timestamp",
        "description" : "text",
        "name" : "text"
        }

    SEARCH_FIELDS = ["name", "description"]

    def latest(self, conn=None):
        """
        Returns most recent SurveyData point available.
        """
        if not conn:
            conn = self.conn

        sql = "select * from %s where survey_id = %s ORDER BY created_at DESC LIMIT 1"
        rows = conn.execute(sql % (SurveyData.table_name(), self.id))
        return SurveyData.load(conn, rows.fetchone())

    def data(self, conn=None):
        """
        Returns iterator of all data points.
        """
        sql = "select * from %s where survey_id = %s ORDER BY created_at"

        rows = conn.execute(sql % (SurveyData.table_name(), self.id))
        for row in rows:
            yield row
