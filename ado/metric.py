import ado.model
from ado.metric_data import MetricData

class Metric(ado.model.Model):
    FIELDS = {
        "archived_at" : "timestamp",
        "created_at" : "timestamp",
        "description" : "text",
        "name" : "text"
        }

    SEARCH_FIELDS = ["name", "description"]

    def latest(self, conn=None):
        """
        Returns most recent MetricData point available.
        """
        if not conn:
            conn = self.conn

        sql = "select * from %s where metric_id = %s ORDER BY created_at DESC LIMIT 1"
        rows = conn.execute(sql % (MetricData.table_name(), self.id))
        return MetricData.load(conn, rows.fetchone())

    def ts(self, conn=None):
        """
        Returns time series of all data points.
        """
        sql = "select * from %s where metric_id = %s ORDER BY created_at"

        datetimes = []
        values = []
        rows = conn.execute(sql % (MetricData.table_name(), self.id))
        for row in rows:
            datetimes.append(row['created_at'])
            values.append(row['value'])
        return datetimes, values

