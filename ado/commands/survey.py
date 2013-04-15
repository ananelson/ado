from ado.survey import Survey
from ado.survey_data import SurveyData
from datetime import datetime
import ado.commands
import sys
from ado.metric import Metric
from ado.metric_data import MetricData

def take_survey(s):
    c = ado.commands.conn()
    if s < 0:
        Survey.printall(c)
        raw_s = ado.commands.clean_input("Choose a survey number: ")
        if raw_s:
            s = int(raw_s)
        else:
            sys.stderr.write("No survey chosen.\n")
            sys.exit(1)

    survey = Survey.get(c, s)
    print "Taking Survey %s) %s" % (survey.id, survey.name)
    print survey.description
    value = ado.commands.clean_input("> ")

    SurveyData.create(
            c,
            survey_id=s,
            value=value,
            created_at = datetime.now()
            )

def create_survey(name, frequency, description):
    c = ado.commands.conn()
    survey = Survey.create(
            c,
            name=name,
            frequency=frequency,
            description=description,
            created_at = datetime.now()
            )
    print survey.id

def survey_command(
        s=-1,
        name=False,
        frequency='1d',
        description=""
        ):
    """
    Define a new survey, or take a survey.
    """
    if not name:
        take_survey(s)
    else:
        create_survey(name, frequency, description)


def record_metric(m, value):
    c = ado.commands.conn()
    if m < 0:
        Metric.printall(c)
        raw_m = ado.commands.clean_input("Choose a metric number: ")
        if raw_m:
            m = int(raw_m)
        else:
            sys.stderr.write("No metric chosen.\n")
            sys.exit(1)

    if value == "None":
        metric = Metric.get(c, m)
        print "Record Metric %s) %s" % (metric.id, metric.name)
        print metric.description
        value = float(ado.commands.clean_input("> "))

    md = MetricData.create(
            c,
            metric_id=m,
            value=value,
            created_at = datetime.now()
            )
    print md.display_line()

def create_metric(name, frequency, description):
    c = ado.commands.conn()
    metric = Metric.create(
            c,
            name=name,
            frequency=frequency,
            description=description,
            created_at = datetime.now()
            )
    print metric.id

def metric_command(
        m=-1,
        name=False,
        frequency='1d',
        description='',
        value="None"
        ):
    """
    Define a new metric, or take a metric.
    """
    if not name:
        record_metric(m, value)
    else:
        create_metric(name, frequency, description)
