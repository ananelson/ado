Reports
=======

{% from "dexy.jinja" import image_ext, code, codes with context %}

.. contents:: Contents
    :local:

Installing Dexy
---------------

If you have Ado installed, you should already have Dexy installed.

To check, run this command:

{{ codes('examples.sh|idio|shint|pyg', 'dexy version') }}

For more information about installing dexy, look at the `dexy installation docs
<http://www.dexy.it/guide/installing-dexy.html>`__.

Generating a Template
---------------------

The best way to get started is to generate a template with reports you can run
straight away, and later customize.

{{ codes('reports-setup.sh|idio|shint|pyg', 'gen') }}

We can run dexy on this repository:

{{ codes('reports-setup.sh|idio|shint|pyg', 'run') }}

The results include HTML and can be viewed as a web server:

{{ codes('reports-setup.sh|idio|shint|pyg', 'start-server') }}

Later we stop the server:

{{ codes('reports-teardown.sh|idio|shint|pyg', 'kill') }}
{{ codes('reports-teardown.sh|idio|shint|pyg', 'check-killed') }}

.. image:: dexy-serve-index.{{ image_ext }}
