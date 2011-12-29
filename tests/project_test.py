from ado.project import Project
from tests.utils import get_conn
import datetime

def test_create_project():
    conn = get_conn()
    project = Project.create(conn, name="My New Project", created_at = datetime.datetime.now())
    assert project.id == 1
    assert project.elapsed_seconds() < 0.01

    lookup_project = Project.get(conn, 1)
    assert lookup_project.name == "My New Project"
    assert project.elapsed_seconds() < 0.01
