Quickstart
==========

{% from "dexy.jinja" import hl, code, codes with context %}

{% macro hl_pydoc(key) -%}
{{ hl(d['/packages.txt|pydoc'][key], 'python') }}
{% endmacro -%}

{% macro raw_pydoc(key) -%}
{{ d['/packages.txt|pydoc'][key] | indent(4, True) }}
{% endmacro -%}

.. contents:: Contents
    :local:


Installing Ado
--------------

To install the latest release version of ado, just use pip:

{{ codes("install.sh|idio", "pip install") }}

To get the most recent up-to-date version of ado and be able to have the source code handy, install from source:

{{ codes("install.sh|idio", "source install") }}

Simple Workflow
---------------

The workflow is done by running command line tools.

Tasks
.....

Here is how to create tasks:

{{ codes("examples.sh|idio|shint|pyg", "create-task") }}

And to list them:

{{ codes("examples.sh|idio|shint|pyg", "list-tasks") }}

Projects
........

Here is how to create projects:

{{ codes("examples.sh|idio|shint|pyg", "create-project") }}

And list them:

{{ codes("examples.sh|idio|shint|pyg", "projects") }}

Ado Help
--------

To list all available commands:

{{ codes("examples.sh|idio|shint|pyg", "help") }}

Source
------

This Document
.............

{{ code( s.baserootname() + ".rst|pyg") }}

_pages.jinja
............

{{ code('_pages.jinja|pyg') }}
