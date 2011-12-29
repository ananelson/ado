from ado.model import Model
import ado.commands

def get_conn():
    conn = Model.setup_db()
    Model.setup_tables(conn, ado.commands.CLASSES)
    return conn
