=============
The Ado Guide
=============

{% from "dexy.jinja" import code, codes with context %}

.. contents:: Contents
    :depth: 1

{% from '_pages.jinja' import pages %}
{% for page in pages %}
{% set template = "%s.rst" % page %}
{% include template %}
{% endfor %}

Source
------

{{ code( s.baserootname() + ".rst|pyg") }}
