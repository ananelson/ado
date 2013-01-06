from ado.model import Model
from ado.survey import Survey
from ado.survey_data import SurveyData
from datetime import datetime

def test_survey():
    conn = Model.setup_db()
    Survey.create_table(conn)
    survey = Survey.create(conn,
            created_at = datetime.now(),
            name = "how do you feel",
            description = "How do you feel?")

    assert survey.id > 0

    SurveyData.create_table(conn)
    a1 = SurveyData.create(conn,
            survey_id = survey.id,
            value = "I feel fine."
            )

    assert a1.id > 0

    latest = survey.latest()
    assert latest.id == a1.id
    assert latest.value == "I feel fine."
