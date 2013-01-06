import ado.model

class MetricData(ado.model.Model):
    FIELDS = {
        "metric_id" : "integer",
        "created_at" : "timestamp",
        "value" : "float"
        }
