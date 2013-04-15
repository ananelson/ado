Getting Started
===============

{% from "dexy.jinja" import code, codes with context %}

.. contents:: Contents
    :local:

Ado is a simple command-line todo system. Ado lets you create notes, projects
and tasks, and organize them into portfolios corresponding to the different
areas of responsibility in your life. Ado also lets you track the time you
spend on tasks so you can better understand your commitments and manage your
time better. Because ado uses Dexy as its reporting engine, you can create
powerful reports (or use the defaults) to really understand and plan how you
spend your productive time.

Ado uses a sqlite file to store data. By default, this sqlite file is named `{{
d['/packages.txt|pydoc']['ado.commands.ADO_DB_FILE:value'] }}` and is stored in
a `.ado` directory in the user's home directory, e.g.  `{{
d['/packages.txt|pydoc']['ado.commands.ADO_DIR:value'] }}`

You can override either of these locations by setting environment constants:

{{ codes('examples.sh|idio|shint|pyg', 'set-ado-dir') }}

The setup command creates the `ADO_DIR` directory (if necessary)
and creates the tables in the database:

{{ codes('examples.sh|idio|shint|pyg', 'setup') }}

You can check that this has worked by using the `sqlite3` command directly:
{{ codes('examples.sh|idio|shint|pyg', 'sqlite-dump') }}

The `ado dump` command lets you dump your data to SQL format, this is useful as
a plain text backup or to help you migrate if the database scheme changes.

{{ codes('examples.sh|idio|shint|pyg', 'reset-db') }}

To manage your todo items, you can create notes, tasks and projects.

Notes
-----

A note can stand alone, or it can be assigned to a task or a project. Create
notes by using the `note` command.

{{ codes('examples.sh|idio|shint|pyg', 'create-note') }}

Each note is assigned an ID number, which is printed to STDOUT when the note is
created. You can list notes with the `notes` command.

{{ codes('examples.sh|idio|shint|pyg', 'list-notes') }}

This displays the note id, the first 30 characters of the note, and how old the
note is (in days). You can use the `show` command to show the full text of
a note:

{{ codes('examples.sh|idio|shint|pyg', 'show-note') }}

Notes can be deleted using the \verb|delete| command, which removes them from the database:

{{ codes('examples.sh|idio|shint|pyg', 'delete-note') }}

{{ codes('examples.sh|idio|shint|pyg', 'list-notes-again') }}

You can also use the \verb|archive| command which keeps the content in the
database, but removes it from lists and reports.

{{ codes('examples.sh|idio|shint|pyg', 'archive-note') }}

{{ codes('examples.sh|idio|shint|pyg', 'list-notes-yet-again') }}

Tasks
-----

Tasks have a name and a context, and an optional description.

Create a task:

{{ codes('examples.sh|idio|shint|pyg', 'create-task') }}

And to list all tasks:

{{ codes('examples.sh|idio|shint|pyg', 'list-tasks') }}

To show detail on a specific task:

{{ codes('examples.sh|idio|shint|pyg', 'show-task') }}

When you have finished a task, you can mark it as complete:

{{ codes('examples.sh|idio|shint|pyg', 'complete-task') }}

Projects
--------

To create a new project:

{{ codes('examples.sh|idio|shint|pyg', 'create-project') }}

To list all projects:

{{ codes('examples.sh|idio|shint|pyg', 'projects') }}

Notes with Projects and Tasks
-----------------------------

Notes can be assigned to projects or tasks, either when they are created, or
afterwards.

You can pass a project or task id when creating a new note, use `-p` to
pass a project id and `-t` to pass a task id, the new note will be
assigned to the project or task in question.

{{ codes('examples.sh|idio|shint|pyg', 'create-note-in-project') }}

When you show the project, you see that the note is linked to it:

{{ codes('examples.sh|idio|shint|pyg', 'show-project') }}

You can also use the \verb|assign| command to assign a note to a project or task:

{{ codes('examples.sh|idio|shint|pyg', 'create-task-for-note') }}

Let's change the note's content to reflect the fact that it is now a part of a
task rather than a project, using the `update` command:

{{ codes('examples.sh|idio|shint|pyg', 'update-note') }}

You can use the update command to change any attribute of a note, project or task.

Workflow
--------

This section talks about how these elements work together for a GTD-style workflow.

The `inbox` command lists all tasks that aren't assigned to a project, and
all notes that aren't assigned to a project or a task:

{{ codes('examples.sh|idio|shint|pyg' ,'inbox') }}

To process this 'inbox', the `assign` command is used to assign notes to
tasks and projects, or tasks to projects. Use the `complete` command to
mark tasks and projects as complete.

So, you can create a note or a task any time so that it's in your system, and
later you can assign it to a project, or create a task for the note to be
attached to.

Tasks have contexts, which traditionally start with the `@` symbol. You
can pass the `-by` option with 'context' to the `tasks` command to
sort your tasks by context.

The tasks, notes and projects commands also take a 'search' option which lets
you find objects that have the search string. The `search` command lets
you search across notes, tasks and projects.

Source
------

{{ code( s.baserootname() + ".rst|pyg") }}
