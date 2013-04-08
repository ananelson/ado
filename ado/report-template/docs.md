## Docs

<p><a href="#docs">&uarr;</a></p>

[TOC]

### Portfolios, Projects and Tasks (Quickstart)

<p><a href="#docs">&uarr;</a></p>

Define portfolios which are the broad categories that your TODOs fall into (i.e. categories like 'work', 'personal' or 'sales', 'writing code').

{{ d['examples.sh|idio|shint|pyg']['portfolios'] }}

You can see your portfolios by:

{{ d['examples.sh|idio|shint|pyg']['list-portfolios'] }}

You can see detail on a single portfolio by:

{{ d['examples.sh|idio|shint|pyg']['show-portfolio'] }}

When you create a project, you should specify the portfolio it belongs to:

{{ d['examples.sh|idio|shint|pyg']['projects'] }}

You can see your projects by:

{{ d['examples.sh|idio|shint|pyg']['list-projects'] }}

You can see detail on a single project by:

{{ d['examples.sh|idio|shint|pyg']['show-project'] }}

Projects are holders for multiple tasks (as in GTD). Now we define individual tasks which are discrete do-able TODOs:

{{ d['examples.sh|idio|shint|pyg']['tasks'] }}

You can list your tasks by:

{{ d['examples.sh|idio|shint|pyg']['list-tasks'] }}

DUE_DATE was defined by:

{{ d['examples.sh|idio|shint|pyg']['calc-due-date'] }}

You can see detail on a single task by:

{{ d['examples.sh|idio|shint|pyg']['show-task'] }}

### Commands

Here are docs for all commands in ado.

{% for command in f.commands() %}
#### {{ command.capitalize() }} Command

<p><a href="#docs">&uarr;</a></p>

<pre>
{{ f.ado_help(command) }}
</pre>
{% endfor %}
