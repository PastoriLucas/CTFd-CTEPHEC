from CTFd.models import Explanations, ma
from marshmallow import fields
from CTFd.utils import string_types
from CTFd.schemas.challenges import ChallengeSchema
from CTFd.schemas.users import UserSchema

class ExplanationSchema(ma.ModelSchema):
    
    challenge = fields.Nested(ChallengeSchema, only=["id", "name", "category", "value"])
    user = fields.Nested(UserSchema, only=["id", "name"])

    class Meta:
        model = Explanations
        include_fk = True
        dump_only = ("id",)
    
    views = {
        "admin": [
           "id",
            "content",
            "user_id",
            "challenge_id",
        ],
          "user": [
           "id",
            "content",
            "user_id",
            "challenge_id",
        ],
    }

    def __init__(self, view=None, *args, **kwargs):
        if view:
            if isinstance(view, string_types):
                kwargs["only"] = self.views[view]
            elif isinstance(view, list):
                kwargs["only"] = view

        super(ExplanationSchema, self).__init__(*args, **kwargs)