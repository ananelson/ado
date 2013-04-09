### @export "set-ado-dir"
export ADO_DIR=`pwd`
export ADO_DB_FILE=example.sqlite

### @export "setup"
ado setup

### @export "sqlite-dump"
sqlite3 -line $ADO_DIR/$ADO_DB_FILE ".dump"

### @export "portfolios"
ado portfolio -name "Prince" -description "Duties relating to being the Prince of Aragon."
ado portfolio -name "Fighting" -description "Waging battle."
ado portfolio -name "Matchmaking" -description "Arranging suitable matches for my peeps."
ado portfolio -name "Personal" -description "Personal stuff."

### @export "list-portfolios"
ado portfolios

### @export "show-portfolio"
ado show -portfolio 1

### @export "projects"
ado project -name "Hook up Beatrice and Benedick." -p 3
ado project -name "Buy costume for masquerade ball." -p 4

### @export "list-projects"
ado projects

### @export "show-project"
ado show -p 1

### @export "calc-due-date"
date
DUE_DATE=`date -d "+5 days" +%Y-%m-%d`
echo $DUE_DATE

### @export "tasks"
ado task -name "Talk about Beatrice's thing for Broderick where Broderick can hear." -context "@orchard" -due $DUE_DATE -p 1
ado task -name "Go to costumer's shop." -context "@town" -description "Take a look at what costumes they have and see if there's anything I like." -p 2

### @export "list-tasks"
ado tasks
ado tasks -by context
ado tasks -by due_at

### @export "show-task"
ado show -t 1

### @export "create-note"
ado note -note "do some stuff"
echo "do some more stuff" | ado note

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


### @export "show-task"
ado show -t 1

### @export "complete-task"
ado complete -t 1

### @export "create-note-in-project"
ado note -note "This is a note in a project" -p 1

### @export "show-project"
ado show -p 1

### @export "create-task-for-note"
ado task -name "task with a note" -context "@anywhere" -p 1
ado assign -n 3 -t 3
ado show -t 3

### @export "update-note"
ado update -n 3 -note "This is a note in a task."
ado show -t 3

### @export "inbox"
ado inbox

dexy setup
dexy
