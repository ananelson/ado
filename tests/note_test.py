from ado.project import Project
from tests.utils import get_conn
from ado.note import Note
import datetime

def test_create_note():
    conn = get_conn()
    note = Note.create(conn, note="This is a new note.", created_at = datetime.datetime.now())
    assert note.id == 1
    assert note.elapsed_seconds() < 0.01

    project = Project.create(
                conn,
                name = "My Project With Notes",
                created_at = datetime.datetime.now()
            )

    note2 = Note.create(
                conn,
                note="This is a note assigned to a project.",
                linked_to_type="Project",
                linked_to_id=project.id,
                created_at=datetime.datetime.now()
            )

    assert note2.id == 2

    inbox_notes = [n.id for n in Note.inbox(conn)]
    assert note.id in inbox_notes
    assert not note2.id in inbox_notes

    note.assign(conn, project)

    inbox_notes = [n.id for n in Note.inbox(conn)]
    assert not note.id in inbox_notes
    assert not note2.id in inbox_notes

    note = note.reload(conn)
    assert note.project(conn).id == project.id
    assert note2.project(conn).id == project.id
