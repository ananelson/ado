Installation
============

{% from "dexy.jinja" import code, codes with context %}

.. contents:: Contents
    :local:

Installing Ado
--------------

To install the latest release version of ado, just use pip:

{{ codes("install.sh|idio", "pip install") }}

To get the most recent up-to-date version of ado and be able to have the source code handy, install from source:

{{ codes("install.sh|idio", "source install") }}

After successfully installing ado, you should be able to run a simple command:

{{ codes("examples.sh|idio|shint|pyg", "version") }}

To see all the available ado commands, run the `help` command:

{{ codes("examples.sh|idio|shint|pyg", "help") }}

Source
------

{{ code( s.baserootname() + ".rst|pyg") }}
