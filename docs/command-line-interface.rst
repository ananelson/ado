Command Line Interface
======================

{% from "dexy.jinja" import code, codes with context %}

.. contents:: Contents
    :local:

Commands
--------

Here are docs for all commands in ado.

{% for command in f.commands() %}

{{ command.capitalize() }} Command
{{ "." * (len(command.capitalize()) + 8) }}

Help::

    {{ f.ado_help(command) | indent(4) }}

{% endfor %}

Source
------

{{ code( s.baserootname() + ".rst|pyg") }}
