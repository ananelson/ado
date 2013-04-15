from ado.survey import Survey
from ado.survey_data import SurveyData
from datetime import datetime
import ado.commands
import sys

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
        frequency=1,
        description=""
        ):
    """
    Define a new survey, or take a survey.
    """
    if not name:
        take_survey(s)
    else:
        create_survey(name, frequency, description)

