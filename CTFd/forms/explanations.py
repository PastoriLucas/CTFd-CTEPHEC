from wtforms import MultipleFileField, SelectField, StringField
from wtforms.validators import InputRequired

from CTFd.forms import BaseForm
from CTFd.forms.fields import SubmitField


class ExplanationSearchForm(BaseForm):
    field = SelectField(
        "Search Field",
        choices=[
            ("id", "ID"),
            ("user_id", "User"),
            ("challenge_id", "Challenge"),
        ],
        default="id",
        validators=[InputRequired()],
    )
    q = StringField("Parameter", validators=[InputRequired()])
    submit = SubmitField("Search")


class ExplanationFilesUploadForm(BaseForm):
    file = MultipleFileField(
        "Upload Files",
        description="Attach multiple files using Control+Click or Cmd+Click.",
        validators=[InputRequired()],
    )
    submit = SubmitField("Upload")
