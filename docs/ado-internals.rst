Ado Internals
=============

{% from "dexy.jinja" import hl, code, codes with context %}

{% macro hl_pydoc(key) -%}
{{ hl(d['/packages.txt|pydoc'][key], 'python') }}
{% endmacro -%}

{% macro raw_pydoc(key) -%}
{{ d['/packages.txt|pydoc'][key] | indent(4, True) }}
{% endmacro -%}

.. contents:: Contents
    :local:

Commands
--------

Let's start by looking at the source for a simple command line command:

{{ hl_pydoc("ado.commands.projects_command:source") }}

The docstring `{{ raw_pydoc("ado.commands.projects_command:doc") }}` is used as
help for the command in the command line help:

{{ codes("examples.sh|idio|shint|pyg", "help on projects") }}

The `conn` function makes a connection to the database (using the Model class's `setup_db`_ method):

{{ hl_pydoc("ado.commands.conn:source") }}

Then the method retrieves a list of projects and then iterates over them,
calling the `display_line` method for each, or displaying a message that there
are no projects available.

Other commands follow a similar pattern. They make a connection to the
database, then pass this connection to various Model objects and print out the
desired output.

More complex methods will take user arguments and use these to format the output 

Models
------

The Model class has code for interacting with a sqlite database.

setup_db
........

The setup_db method creates a connection to a sqlite database:

{{ hl_pydoc("ado.model.Model.setup_db:source") }}

Source
------

{{ code( s.baserootname() + ".rst|pyg") }}

