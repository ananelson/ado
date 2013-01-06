import ado.model
import ado.project

class Note(ado.model.Model):
    """
    Notes are stand-alone objects, or they can be assigned to projects or
    tasks, or they can be converted into projects or tasks. Notes can be used
    to store additional information relating to projects or tasks, or they can
    be used as temporary placeholders for information that needs to be filed
    elsewhere later.
    """

    SEARCH_FIELDS = ["note"]

    FIELDS = {
        "archived_at" : "timestamp",
        "created_at" : "timestamp",
        "linked_to_id" : "integer", # For objects that are linked to an instance of a class (e.g. a project or a task), gives the id of linked instance
        "linked_to_type" : "text", # For objects that are linked to an instance of a class (e.g. a project or task), gives the class of linked instance
        "note" : "text"
    }

    @classmethod
    def inbox(klass, conn):
        """
        Return all notes still in the 'inbox'
        """
        sql = "select * from %s where linked_to_id IS NULL and archived_at IS NULL" % klass.table_name()
        return [klass.load(conn, row) for row in conn.execute(sql)]

    def assign(self, conn, element):
        """
        Assigns this note to the element passed.
        """
        args = {'linked_to_type' : element.__class__.__name__, 'linked_to_id' : element.id}
        Note.update(conn, self.id, args)

    def project(self, conn):
        """
        If linked to a project, retrieves the project.
        """
        if self.linked_to_type == "Project":
            return ado.project.Project.get(conn, self.linked_to_id)
        else:
            raise Exception("Not linked to a project")

    def show(self):
        return self.note

    def display_line(self):
        if len(self.note) > 30:
            note = self.note[0:27] + "..."
        else:
            note = self.note
        return "Note %04d. %-30s (%d days old)" % (self.id, note, self.elapsed_days())

