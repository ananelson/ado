from ado.task import Task
from tests.utils import get_conn
import datetime

def test_create_task():
    conn = get_conn()
    task = Task.create(conn, name="My New Task", created_at = datetime.datetime.now())
    assert task.id == 1
    assert task.elapsed_seconds() < 0.01

    lookup_task = Task.get(conn, 1)
    assert lookup_task.name == "My New Task"
    assert task.elapsed_seconds() < 0.01
