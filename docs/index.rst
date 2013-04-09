=============
The Ado Guide
=============

{% from '_pages.jinja' import pages -%}

You can also view this guide as a `single HTML page <the-ado-guide.html>`_ or
`download the PDF <the-ado-guide.pdf>`_.

Contents:

{% for page in pages -%}
* `{{ titleize(page) }} <{{ page }}.html>`_ (`download PDF <{{ page }}.pdf>`__)
{% endfor -%}

{% if False -%}
Formatting
==========

Cheat sheet of formatting levels to keep things consistent (since rst breaks if we don't)

First Level
-----------

This is first level.

Second Level
............

This is the second level.

Third Level
^^^^^^^^^^^

This is the third level.
{% endif -%}
