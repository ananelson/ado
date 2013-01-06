from ado.model import Model
from ado.metric import Metric
from ado.metric_data import MetricData
from datetime import datetime

def test_metric():
    conn = Model.setup_db()
    Metric.create_table(conn)
    metric = Metric.create(conn,
            created_at = datetime.now(),
            name = "mood",
            description = "On a scale of 1 to 10, 10 being best, rate your mood."
            )
    assert metric.id > 0

    MetricData.create_table(conn)

    p1 = MetricData.create(conn,
            created_at = datetime.now(),
            value = 7,
            metric_id = metric.id
            )
    assert p1.id > 0

    p2 = MetricData.create(conn,
            created_at = datetime.now(),
            value = 8,
            metric_id = metric.id
            )
    assert p2.id > 0

    latest = metric.latest(conn)
    assert latest.value == 8
    assert latest.id == p2.id

    datetimes, values = metric.ts(conn)

    assert values == [7, 8]
