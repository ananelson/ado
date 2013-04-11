from ado.model import Model
from ado.portfolio import Portfolio
from ado.task import Task
from ado.commands import db_filepath
import json

conn = Model.setup_db(db_filepath())

def dict_for_task(task):
    return {
            "name" : "[%d] %s" % (task.id, task.name_with_check()),
            "size" : 1,
            "title" : task.description,
            "state" : task.state()
            }

def dict_for_project(project):
    return {
            "name" : "[%d] %s" % (project.id, project.name),
            "title" : project.description,
            "state" : "child"
            }

def dict_for_portfolio(portfolio):
    return {
            "name" : "[%d] %s" % (portfolio.id, portfolio.name),
            "title" : portfolio.description,
            "state" : "child"
            }

inbox = {
        "name" : "inbox",
        "children" : [{
            "name" : "inbox",
            "children" : [dict_for_task(t) for t in Task.inbox(conn)]
            }]
        }

data = {
    "name" : 'ado',
    "children" : [inbox]
    }


for portfolio in Portfolio.all(conn):
    projects = []
    for project in portfolio.projects():
        tasks = [dict_for_task(t) for t in project.tasks()]

        project_info = dict_for_project(project)

        if len(tasks) > 0:
            project_info["children"] = tasks
        else:
            project_info["size"] = 1

        projects.append(project_info)

    portfolio_info = dict_for_portfolio(portfolio)

    if len(projects) > 0:
        portfolio_info["children"] = projects
    else:
        portfolio_info["size"] = 1

    data["children"].append(portfolio_info)

with open("ado.json", "w") as f:
    json.dump(data, f, sort_keys=True, indent=4)
