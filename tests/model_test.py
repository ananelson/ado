from ado.project import Project
from ado.model import Model

def test_table_name():
    assert Model.table_name() == "Model"
    assert Project.table_name() == "Project"

def test_create_table():
    conn = Model.setup_db()
    Project.create_table(conn)
    sql = "select * from sqlite_master where type='table' and name='Project'"
    assert len(conn.execute(sql).fetchall()) == 1
    row = conn.execute(sql).fetchone()
    assert row['sql'] == Project.create_table_sql()
    conn.execute("select * from Project")

def test_persist_instance():
    conn = Model.setup_db()
    Project.create_table(conn)
    project = Project.create(conn, name="My New Project")
    print project.persist_instance_sql()
    print project.persist(conn)
