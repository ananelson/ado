import ado.model
from ado.survey_data import SurveyData
import datetime

class Survey(ado.model.Model):
    FIELDS = {
        "archived_at" : "timestamp",
        "created_at" : "timestamp",
        "frequency" : "text",
        "description" : "text",
        "name" : "text"
        }

    SEARCH_FIELDS = ["name", "description"]

    def frequency_delta(self):
        """
        Returns a timedelta object for the specified frequency.
        """
        if "m" in self.frequency:
            minutes = int(self.frequency.replace("m", ""))
            return datetime.timedelta(minutes=minutes)
        elif "h" in self.frequency:
            hours = int(self.frequency.replace("h", ""))
            return datetime.timedelta(hours=hours)
        elif "d" in self.frequency:
            days = int(self.frequency.replace("d", ""))
            return datetime.timedelta(days=days)
        else:
            try:
                days = int(self.frequency)
                return datetime.timedelta(days=days)
            except ValueError:
                raise Exception("Invalid frequency '%s'" % self.frequency)

    def is_due(self, conn=None):
        if not conn:
            conn = self.conn

        if self.frequency < 0:
            # No frequency specified, so it cannot be due.
            return False

        latest = self.latest()

        if latest:
            return (datetime.datetime.now() - latest.created_at) > self.frequency_delta()
        else:
            # This survey has never been taken, so it is due now.
            return True

    def latest(self, conn=None):
        """
        Returns most recent SurveyData point available.
        """
        if not conn:
            conn = self.conn

        sql = "select * from %s where survey_id = %s ORDER BY created_at DESC LIMIT 1"
        rows = conn.execute(sql % (SurveyData.table_name(), self.id))
        row = rows.fetchone()
        if row:
            return SurveyData.load(conn, row)

    def data(self, conn=None):
        """
        Returns iterator of all data points.
        """
        sql = "select * from %s where survey_id = %s ORDER BY created_at"

        rows = conn.execute(sql % (SurveyData.table_name(), self.id))
        for row in rows:
            yield row
