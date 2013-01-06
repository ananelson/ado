import ado.model

class SurveyData(ado.model.Model):
    FIELDS = {
        "survey_id" : "integer",
        "created_at" : "timestamp",
        "value" : "text"
        }
