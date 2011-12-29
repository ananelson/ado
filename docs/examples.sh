### @export "set-ado-dir"
export ADO_DIR=`pwd`
export ADO_DB_FILE=dexy--example.sqlite

### @export "setup"
ado setup

### @export "sqlite-dump"
sqlite3 -line $ADO_DIR/$ADO_DB_FILE ".dump"

### @export "create-note"
ado note -note "This is the text of a note."
echo "This is another note." | ado note

### @export "list-notes"
ado notes

### @export "show-note"
ado show -n 1

### @export "delete-note"
ado delete -n 1

### @export "list-notes-again"
ado notes

### @export "archive-note"
ado archive -n 2

### @export "list-notes-yet-again"
ado notes

### @export "create-task"
ado task -name "This is a task" -context "@home" -due "2012-02-02"
ado task -name "This is another task" -context "@car" -description "This is a more detailed description of this task."

### @export "list-tasks"
ado tasks
ado tasks -by context
ado tasks -by due_at

### @export "show-task"
ado show -t 1

### @export "complete-task"
ado complete -t 1

### @export "create-project"
ado project -name "This is a project."

### @export "projects"
ado projects

### @export "create-note-in-project"
ado note -note "This is a note in a project" -p 1

### @export "show-project"
ado show -p 1

### @export "create-task-for-note"
ado task -name "task with a note" -context "@anywhere"
ado assign -n 3 -t 3
ado show -t 3

### @export "update-note"
ado update -n 3 -note "This is a note in a task."
ado show -t 3

### @export "inbox"
ado inbox
