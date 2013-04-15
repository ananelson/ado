from ado.metric import Metric
from ado.metric_data import MetricData
from ado.model import Model
from ado.note import Note
from ado.portfolio import Portfolio
from ado.project import Project
from ado.recipe import Recipe
from ado.step import Step
from ado.step import DoingRecipe
from ado.step import DoingStep
from ado.survey import Survey
from ado.survey_data import SurveyData
from ado.task import Task
from ado.timer import Timer
from ado.version import ADO_VERSION
from datetime import datetime
from modargs import args
import os
import re
import shutil
import sys
import sqlite3

from ado.commands.list import list_command
from ado.commands.list import search_command
from ado.commands.recipe import recipe_command
from ado.commands.recipe import do_command
from ado.commands.status import ok_command
from ado.commands.status import due_command
from ado.commands.survey import survey_command
from ado.commands.survey import metric_command

# Anything in settings can be overridden by defining a corresponding
# environment variable. e.g. defining setting('ado-dir') in the environment will override
# the 'ado-dir' entry in settings dict.
settings = {
        'ado-db-file' : 'ado.sqlite3',
        'ado-dir' : os.path.expanduser("~/.ado"),
        'default-command' : 'projects',
        'enforce-worktypes' : True,
        'enforce-context' : False,
        'worktypes' : ['adhoc', 'billable', 'capital', 'maintenance']
        }

# Timer class ?
classes = {
        'n' : Note,
        't' : Task,
        'p' : Project,
        'f' : Portfolio,
        'r' : Recipe,
        's' : Step,
        'm' : Metric,
        'md' : MetricData,
        'v' : Survey,
        'vd' : SurveyData,
        'dr' : DoingRecipe,
        'ds' : DoingStep
        }

def clean(raw):
    return "".join(i for i in raw if ord(i) < 128)

def clean_input(prompt):
    return clean(raw_input(prompt))

def const_key(key):
    """
    Replaces ado-dir with setting('ado-dir'), used for converting settings dict entries to
    environment variable style.
    """
    return key.replace("-", "_").upper()

def setting(key):
    """
    Fetches the value of a setting by first looking in system environment, then
    falling back to default specified in 'settings'.
    """
    return os.environ.get(const_key(key), settings[key])

# constants
MOD = sys.modules[__name__]
PROG = 'ado'

# database
db_filepath = os.path.join(setting('ado-dir'), setting('ado-db-file'))

def conn():
    return Model.setup_db(db_filepath)

# python modargs
def run():
    args.parse_and_run_command(sys.argv[1:], MOD, default_command=setting('default-command'))

def help_command(on=False):
    """
    Prints this help.
    """
    args.help_command(PROG, MOD, setting('default-command'), on)

def help_text(on=False):
    return args.help_text(PROG, MOD, setting('default-command'), on)

def available_commands():
    return args.available_commands(MOD)

def abbrev(ab):
    """
    Returns the class corresponding to the abbreviation. Prints an error
    message and exits if not valid.
    """
    if not ab in classes:
        valid_abbrevs = ", ".join("%s (for %s)" % (k, v.__name__) for k, v in classes.items())
        sys.stderr.write("You passed '%s', should be one of %s.\n" % (ab, valid_abbrevs))
        sys.exit(1)
    return classes[ab]

# commands
def version_command():
    """
    Prints the version of ado which is running.
    """
    print "Ado %s" % ADO_VERSION

# old commands
def blotter_command():
    """
    Starts a timer. Records everything written to STDIN. Stops timer when
    ctrl+d is typed. Creates a task with last line of blotter as name, rest of
    blotter as description.
    """
    c = conn()
    created_at = datetime.now()
    description = ''
    print "Type ctrl+d to save task (might need to type it twice). ctrl+c to cancel."
    print "Started at %s" % created_at
    try:
        while True:
            line = sys.stdin.readline()
            if len(line) > 1:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                description += "%s:: %s" % (timestamp, line)
            elif len(line) == 1:
                description += line
            else:
                break

        name = raw_input("name of task: ")
        context = raw_input("context for task (defaults to @computer): ")
        if not context:
            context = "@computer"
        worktype = raw_input("type of work (defaults to 'adhoc'): ")

        description = description.strip()
        completed_at = datetime.now()
        task = Task.create(
            c,
            name=name,
            context=context,
            worktype=worktype,
            description=description,
            created_at = created_at,
            completed_at = completed_at
        )
        Timer.create(
                c,
                task_id = task.id,
                started_at = created_at,
                finished_at = completed_at,
                description = task.description
                )
        print task.id
    except KeyboardInterrupt:
        print "cancelled"

def note_command(
        note="", # the contents of the note
        p=-1, # the project id to link the new note to (optional)
        t=-1 # the task id to link the new note to (optional)
        ):
    """
    Create a new note. If note contents are not specified, will read from
    STDIN.
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


def inbox_command():
    """
    Lists all notes and tasks that are still in the 'inbox', i.e. not assigned to projects, tasks or other elements.
    """
    c = conn()
    notes = Note.inbox(c)
    for note in notes:
        print note.display_line()

    tasks = Task.inbox(c)
    for task in tasks:
        print task.display_line()

def notes_command():
    """
    Lists all notes.
    """
    notes = Note.all(conn())
    for note in notes:
        print note.display_line()
    if len(notes) == 0:
        print "No notes found."

def update_command(t=-1,p=-1,n=-1, r=-1, **kwargs):
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
    elif r > 0:
        Recipe.update(c, r, kwargs)
    else:
        raise Exception("Must specify one of t (task), n (note), p (project) or r (recipe).")

def show_command(
        t=-1, # id of task to show detail on
        n=-1, # id of note to show detail on
        p=-1, # id of project to show detail on
        portfolio=-1 # id of portfolio to show detail on
        ):
    """
    Print detailed information for a project, task, note or portfolio.
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
    elif portfolio > 0:
        portfolio = Portfolio.get(c, portfolio)
        print portfolio.show()
    else:
        raise Exception("Must specify one of t (task), n (note), p (project) or portfolio.")

def project_command(
        name=None, # the name of the project (required)
        description="", # an optional description for this project
        p=-1, # portfolio id for this project (required unless parent project specified)
        parent=-1 # parent project id, if this is a subproject
        ):
    """
    Create a new project.
    """
    c = conn()

    if parent > 0:
        parent_project_id = parent
        parent_project = Project.get(c, parent)
        portfolio_id = parent_project.portfolio_id
    else:
        parent_project_id = None
        if p > 0:
            portfolio_id = p
        else:
            raise Exception("You must provide a portfolo id using the -p parameter if this project doesn't have a parent project.")

    project = Project.create(
        c,
        created_at = datetime.now(),
        description=description,
        parent_project_id=parent_project_id,
        name=name,
        portfolio_id=portfolio_id
    )
    print project.id,

def projects_command():
    """
    List all projects.
    """
    c = conn()
    projects = Project.all_nested_subprojects(c)
    for project in projects:
        print project.display_line()
    if len(projects) == 0:
        print "No projects found. Run 'ado help' if you need help."

def task_command(
        name=None, # The name for this task
        context=None, # The @context in which task can be done
        complete=False, # Whether task is already complete.
        p=-1, # project id this task is part of
        r=-1, # recipe this task corresponds to
        description="", # optional longer description for this task
        due=-1, # due date in YYYY-MM-DD format
        estimate=-1, # estimate of time this will take, in minutes
        waiting=-1, # the id of another task that must be completed first
        worktype="adhoc" # type of work this is
        ):
    """
    Create a new task.
    """
    c = conn()

    if due > 0:
        if re.match("[0-9]{4}-[0-9]{2}-[0-9]{2}", due):
            f = "%Y-%m-%d"
            due_at = datetime.strptime(due, f)
        else:
            raise Exception("I don't know how to parse dates like %s" % due)
    else:
        due_at = None

    if estimate < 0:
        estimate = None

    if setting('enforce-worktypes') and not worktype in setting('worktypes'):
        raise Exception("Acceptable worktypes are %s" % ", ".join(setting('worktypes')))

    if setting('enforce-worktypes') and worktype == "maintenance" and r < 0:
        raise Exception("You must specify a recipe in order to designate a task as 'maintenance'")

    if waiting > 0:
        waiting_for_task = Task.get(c, waiting)
        waiting_for_task_id = waiting_for_task.id
        if p < 0:
            # Get the project id based on the task we are waiting for.
            project_id = waiting_for_task.project_id
        else:
            project_id = p
    else:
        waiting_for_task_id = None
        if p > 0:
            project_id = p
        else:
            print "putting new task into inbox"
            project_id = None

    if complete:
        completed_at = datetime.now()
    else:
        completed_at = None

    task = Task.create(
        c,
        due_at=due_at,
        name=name,
        context=context,
        description=description,
        estimate=estimate,
        project_id=project_id,
        worktype=worktype,
        waiting_for_task_id=waiting_for_task_id,
        created_at = datetime.now(),
        completed_at = completed_at
    )
    print "Created task", task.id

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
    ado_dir = setting('ado-dir')
    if not os.path.exists(ado_dir):
        print "Creating directory", ado_dir
        os.mkdir(ado_dir)

    c = conn()
    Model.setup_tables(c, classes.values())

def reset_command():
    """
    Deletes user dir and recreates database tables. DESTROYS ALL YOUR DATA!
    """
    shutil.rmtree(setting('ado-dir'))
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
    for klass in classes.values():
        sql = klass.insert_instance_sql()
        try:
            rows = c.execute(sql)
            for row in rows:
                print row[0]
        except sqlite3.OperationalError as e:
            print "-- %s %s" % (klass.__name__, str(e))

def load_command(filename=None):
    """
    Loads a data file previously created by saving the output of 'dump'.
    """
    c = conn()
    with open(filename, "r") as f:
        for line in f.readlines():
            c.execute(line)
        c.commit()

def delete_command(
        n=-1, # id of the note to delete
        p=-1, # id of the project to delete
        t=-1 # id of the task to delete
        ):
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

def archive_command(
        n=-1, # id of the note to archive
        p=-1, # id of the project to archive
        t=-1 # id of the task to archive
        ):
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

def complete_command(
        p=-1, # id of the project to mark complete
        t=-1 # id of the task to mark complete
        ):
    """
    Mark the project or task as completed.
    """
    c = conn()
    if p > 0:
        project = Project.get(c, p)
        project.complete(c)
        Project.archive(c, project.id)
        print "Project %s marked as complete!" % p
    elif t > 0:
        task = Task.get(c, t)
        task.complete(c)
        print "Task %s marked as complete!" % t
    else:
        raise Exception()

def start_command(r=None):
    """
    Start a timer for a recipe.
    """
    c = conn()
    recipe = Recipe.get(c, r)
    recipe_id = recipe.id
    print recipe.recipe
    task = Task.create(
            c,
            name="Doing Recipe %s (%s)" % (recipe_id, recipe.name),
            recipe_id=recipe_id,
            context=recipe.context
            )
    time_command(task.id)
    print "Created task %s and started timer" % task.id

def time_command(t=-1, description=""):
    """
    Starts a timer, optionally give a description and specify the task id you are working on.
    """
    c = conn()
    active_timers = Timer.active_timers(c)
    if len(active_timers) > 0:
        # List the existing timer(s) and show elapsed times
        for timer in active_timers:
            if timer.description:
                description = timer.description
            else:
                description = ""

            if timer.task_id:
                task_id = "Task %4d." % timer.task_id
            else:
                task_id = "No task assigned."
            print "Timer %04d.    %s   %s %s" % (timer.id, timer.elapsed_time(), task_id, description)
    else:
        # Create a new timer.
        if t > 0:
            task_id = t
        else:
            task_id = None

        if len(description) == 0:
            description = None

        if not description and not task_id:
            print "No active timers. To create a new timer please specify either a description or a task id."
        else:
            time = Timer.create(
                c,
                task_id=task_id,
                description=description,
                started_at = datetime.now()
            )
            print "Timer %s Started" % time.id

def stop_command(t=-1):
    c = conn()
    if t > 0:
        # stop the particular timer specified
        timers = [ t ]
    else:
        # stop all timers (there's probably just 1)
        timers = Timer.active_timers(c)

    if len(timers) == 0:
        print "No timers running."

    for timer in timers:
        Timer.stop(c, timer.id)
        print "Stopped timer %04d total time %s" % (timer.id, timer.elapsed_time())

def tasktime_command(t=None):
    c = conn()
    task = Task.get(c, t)
    print task.total_time(c)

def portfolio_command(name=None, description=None):
    """
    Creates a new portfolio.
    """
    c = conn()
    portfolio = Portfolio.create(
        c,
        name=name,
        description=description,
        created_at = datetime.now()
    )
    print portfolio.id,

def portfolios_command():
    c = conn()
    portfolios = Portfolio.all(c)

    for portfolio in portfolios:
        print portfolio.display_line()

def ts_command(
        m=-1 # The metric id to print data for.
        ):
    c = conn()
    if m > 0:
        metric = Metric.get(c, m)
        datetimes, values = metric.ts(c)
        for i, value in enumerate(values):
            print "%s: %s" % (datetimes[i], value)

def values_command(
        m=-1, # The metric id to print data for.
        s=-1 # The survey id to print data for.
        ):
    """
    Returns space-separated data for a metric, or longer form data for a survey.
    
    Metric output can be piped to spark. https://github.com/holman/spark
    """
    c = conn()
    if m > 0:
        metric = Metric.get(c, m)
        datetimes, values = metric.ts(c)
        print " ".join("%s" % v for v in values)
    elif s > 0:
        survey = Survey.get(c, s)
        for row in survey.data(c):
            print row['created_at']
            print row['value']
            print ''

def metrics_command(
       l=False # Whether to just list all available metrics.
        ):
    """
    Run through all metrics and gather data from responses.
    """
    c = conn()
    metrics = Metric.all(c)
    if len(metrics) == 0:
        print "No metrics found, define some first with 'ado metric'"
    elif l:
        for metric in metrics:
            print "%s) %s: %s" % (metric.id, metric.name, metric.description)
    else:
        for metric in metrics:
            try:
                print metric.id, ' ',
                if metric.description:
                    value = raw_input(metric.description + "\n")
                else:
                    value = raw_input(metric.name + ": ")

                if len(value) > 0:
                    MetricData.create(
                            c,
                            metric_id = metric.id,
                            value=value,
                            created_at = datetime.now()
                            )
            except KeyboardInterrupt:
                print "quitting"
