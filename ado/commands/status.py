from ado.commands.survey import take_survey
from ado.metric import Metric
from ado.recipe import Recipe
from ado.survey import Survey
import ado.commands
import sys

def ok_command(debug=False):
    c = ado.commands.conn()
    surveys_due = bool(Survey.all_due(c))
    metrics_due = bool(Metric.all_due(c))
    recipes_due = bool(Recipe.all_due(c))

    if debug:
        print "Are surveys due?", surveys_due
        print "Are metrics due?", metrics_due
        print "Are recipes due?", recipes_due

    ok = (not surveys_due) and (not metrics_due) and (not recipes_due)
    if ok:
        if debug:
            print "nothing is due"
        sys.exit(0)
    else:
        print "something is due"
        sys.exit(1)

def due_command():
    c = ado.commands.conn()
    for survey in Survey.all_due(c):
        take_survey(survey.id)
