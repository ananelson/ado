from ado.model import Model
from ado.metric import Metric
from ado.commands import db_filepath

conn = Model.setup_db(db_filepath())

with open("metric-data.txt", "w") as f:
    f.write("datetime\tmetric\tvalue\n")
    for metric in Metric.all(conn):
        datetimes, values = metric.ts(conn)
        for i, dt in enumerate(datetimes):
            timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
            f.write("%s\t%s\t%s\n" % (timestamp, metric.name, values[i]))
