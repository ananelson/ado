from ado.model import Model
from ado.note import Note
from ado.project import Project
from ado.task import Task
from datetime import datetime
from modargs import args
import os
import re
import shutil
import sys

ADO_DB_FILE = "ado.sqlite3"
ADO_DIR = os.path.expanduser("~/.ado")
CLASSES = [Project, Task, Note]
DEFAULT_COMMAND = 'listp'
MOD = sys.modules[__name__]
PROG = 'ado'

def available_commands():
    return args.available_commands(MOD)

def help_command(on=False):
    """
    Prints this help.
    """
    args.help_command(PROG, MOD, DEFAULT_COMMAND, on)

def help_text(on=False):
    return args.help_text(PROG, MOD, DEFAULT_COMMAND, on)

def run():
    args.parse_and_run_command(sys.argv[1:], MOD, default_command=DEFAULT_COMMAND)

def db_filepath():
    if os.environ.has_key('ADO_DIR'):
        ado_dir = os.environ['ADO_DIR']
    else:
        ado_dir = ADO_DIR

    if os.environ.has_key("ADO_DB_FILE"):
        ado_db_file = os.environ['ADO_DB_FILE']
    else:
        ado_db_file = ADO_DB_FILE

    return os.path.join(ado_dir, ado_db_file)

def conn():
    return Model.setup_db(db_filepath())

def note_command(note="", p=-1, t=-1):
    """
    Create a new note.
    """
    c = conn()

    if len(note) == 0:
        note = sys.stdin.read().strip()
    if len(note) == 0:
        raise Exception("You didn't pass any content for your note!")

    n = Note.create(
        c,
        note=note,
        created_at = datetime.now()
    )
    print "Created note", n.id
    if p > 0:
        project = Project.get(c, p)
        n.assign(c, project)
        print "Assigned to project %s" % p
    elif t > 0:
        task = Task.get(c, t)
        n.assign(c, task)
        print "Assigned to task %s" % t

def search_command(search=None):
    """
    Lists all items which meet the search criteria.
    """
    c = conn()

    # Search for notes.
    notes = Note.search(c, search)
    for note in notes:
        print note.display_line()

    # Search for projects.
    projects = Project.search(c, search)
    for project in projects:
        print project.display_line()

    # Search for tasks.
    tasks = Task.search(c, search)
    for task in tasks:
        print task.display_line()

def inbox_command():
    """
    Lists all notes and tasks that are still in the 'inbox', i.e. not assigned to projects, tasks or other elements.
    """
    c = conn()
    notes = Note.inbox(c)
    for note in notes:
        print note.display_line()
    if len(notes) == 0:
        print "No notes in the inbox!"

    tasks = Task.inbox(c)
    for task in tasks:
        print task.display_line()
    if len(tasks) == 0:
        print "No tasks in the inbox!"

def notes_command():
    """
    Lists all notes.
    """
    notes = Note.all(conn())
    for note in notes:
        print note.display_line()
    if len(notes) == 0:
        print "No notes found."

def update_command(t=-1,p=-1,n=-1, **kwargs):
    """
    Update a project, task or note with the supplied kwargs.
    """
    c = conn()
    if t > 0:
        Task.update(c, t, kwargs)
    elif n > 0:
        Note.update(c, n, kwargs)
    elif p > 0:
        Project.update(c, p, kwargs)
    else:
        raise Exception("Must specify one of t (task), n (note) or p (project).")

def show_command(t=-1,n=-1,p=-1):
    """
    Print detailed information for a project, task or note.
    """
    c = conn()
    if t > 0:
        task = Task.get(c, t)
        print task.show()
    elif n > 0:
        note = Note.get(c, n)
        print note.show()
    elif p > 0:
        project = Project.get(c, p)
        print project.show()
    else:
        raise Exception("Must specify one of t (task), n (note) or p (project).")

def project_command(name=None, description=""):
    """
    Create a new project.
    """
    project = Project.create(
        conn(),
        name=name,
        description=description,
        created_at = datetime.now()
    )
    print "Created project", project.id

def projects_command():
    """
    List all projects.
    """
    projects = Project.all(conn())
    for project in projects:
        print project.display_line()
    if len(projects) == 0:
        print "No projects found."

def task_command(name=None, context=None, p=-1, description="", due=-1):
    """
    Create a new task.
    """
    if due > 0:
        if re.match("[0-9]{4}-[0-9]{2}-[0-9]{2}", due):
            f = "%Y-%m-%d"
            due_at = datetime.strptime(due, f)
        else:
            raise Exception("I don't know how to parse dates like %s" % due)
    else:
        due_at = None

    task = Task.create(
        conn(),
        due_at=due_at,
        name=name,
        context=context,
        description=description,
        created_at = datetime.now()
    )
    print "Created task", task.id
    if p > 0:
        project = Project.get(c, p)
        task.assign(project)
        print "Assigned to project %s" % p

def tasks_command(by="id", search=-1):
    """
    List all tasks.
    """
    c = conn()
    if search > 0:
        tasks = Task.search(c, search, by)
    else:
        tasks = Task.all(c, by)

    for task in tasks:
        print task.display_line()
    if len(tasks) == 0:
        print "No tasks found."

def assign_command(n=-1, p=-1, t=-1):
    """
    Assign a note to a project or task, or a task to a project.
    """
    c = conn()
    if n > 0:
        # We are assigning a note to a project or task.
        if p > 0:
            element = Project.get(c, p)
        elif t > 0:
            element = Task.get(c, t)
        else:
            raise Exception("You must specify either a project id or a task id.")
        note = Note.get(c, n)
        note.assign(c, element)
    elif t > 0:
        task = Task.get(c, t)
        # We are assigning a task to a project.
        if p > 0:
            project = Project.get(c, p)
            task.assign(c, project)
        else:
            raise Exception("You must specify a project id to assign the task to.")
    else:
        raise Exception("You didn't specify anything to assign!")

def setup_command():
    """
    Run this command to initialize all database tables. Can be run multiple times safely.
    """
    if not os.path.exists(ADO_DIR):
        print "Creating directory", ADO_DIR
        os.mkdir(ADO_DIR)

    c = conn()
    Model.setup_tables(c, CLASSES)

def reset_command():
    """
    Deletes user dir and recreates database tables. DESTROYS ALL YOUR DATA!
    """
    shutil.rmtree(ADO_DIR)
    setup_command()

def completion_command():
    """
    Prints a bash script that can be saved to generate bash autocompletion for ado commands.
    """
    args.completion_command(PROG, MOD)

def dump_command():
    """
    Dumps your data to console in sqlite format (data only, not structure, so you can preserve data while resetting your db schema).
    """
    c = conn()
    for klass in CLASSES:
        sql = klass.insert_instance_sql()
        rows = c.execute(sql)
        for row in rows:
            print row[0]

def load_command(filename=None):
    """
    Loads a data file previously created by saving the output of 'dump'.
    """
    c = conn()
    with open(filename, "r") as f:
        for line in f.readlines():
            c.execute(line)
        c.commit()

def delete_command(n=-1,p=-1,t=-1):
    """
    Delete the note, project or task specified.
    """
    c = conn()
    if n > 0:
        Note.delete(c, n)
    elif p > 0:
        Project.delete(c, p)
    elif t > 0:
        Task.delete(c, t)
    else:
        raise Exception()

def archive_command(n=-1,p=-1,t=-1):
    """
    Archive the note, project or task specified.
    """
    c = conn()
    if n > 0:
        Note.archive(c, n)
    elif p > 0:
        Project.archive(c, p)
    elif t > 0:
        Task.archive(c, t)
    else:
        raise Exception()

def complete_command(p=-1,t=-1):
    """
    Mark the project or task as completed.
    """
    c = conn()
    if p > 0:
        project = Project.get(c, p)
        project.complete(c)
        print "Project %s marked as complete!" % p
    elif t > 0:
        task = Task.get(c, t)
        task.complete(c)
        print "Task %s marked as complete!" % t
    else:
        raise Exception()
