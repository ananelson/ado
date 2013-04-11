# Dumps all data into a bash format which you can run to re-load the database.
# IN DEVELOPMENT! DOES NOT WORK YET!

{% for portfolio in f.portfolios() -%}
portfolio_id = `portfolio -name "{{ portfolio.name }}" -description "{{ portfolio.description}}"`
{% for project in portfolio.projects() -%}
project_id = `project -p $portfolio_id -name {{ project.name }}`
{% endfor -%}
{% endfor -%}
