import ado.model

class MetricData(ado.model.Model):
    FIELDS = {
        "metric_id" : "integer",
        "created_at" : "timestamp",
        "value" : "float"
        }

    def display_line(self):
        args = (self.__class__.__name__, self.id, self.metric().name, self.value)
        return "%s %4d) %s [%s]" % args

    def metric(self, conn=None):
        if not conn:
            conn = self.conn

        sql = "select * from %s where id = %s"
        rows = conn.execute(sql % (ado.metric.Metric.table_name(), self.metric_id))
        row = rows.fetchone()
        if row:
            return ado.metric.Metric.load(conn, row)
