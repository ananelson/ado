Dexy Integration
================

{% from "dexy.jinja" import hl, code, codes with context %}

{% macro hl_pydoc(key) -%}
{{ hl(d['/packages.txt|pydoc'][key], 'python') }}
{% endmacro -%}

{% macro raw_pydoc(key) -%}
{{ d['/packages.txt|pydoc'][key] | indent(4, True) }}
{% endmacro -%}

.. contents:: Contents
    :local:


Ado Jinja Plugin
----------------

The Ado Jinja plugin makes information about ado objects available to a dexy jinja template.

{{ hl_pydoc("ado.dexy_plugins.AdoFilter:source") }}

Reports Template
----------------

When ado is installed, it adds a new template to dexy:

{{ codes("examples.sh|idio|shint|pyg", "dexy templates") }}

The template can be used with the `dexy gen` command to create a new project
directory which will let you generate the standard reports, and easily modify
them.

Source
------

{{ code( s.baserootname() + ".rst|pyg") }}

