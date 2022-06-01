from CTFd.models import HintsTimer, ma
from CTFd.utils import string_types


class HintTimerSchema(ma.ModelSchema):
    class Meta:
        model = HintsTimer
        include_fk = True
        dump_only = ("id")

    views = {
        "locked": ["id", "team_id","hint_id", "end_time"],
        "unlocked": [
            "id",
            "team_id",
            "hint_id",
            "end_time",
        ],
        "admin": [
            "id",
            "team_id",
            "hint_id",
            "end_time",
        ],
    }

    def __init__(self, view=None, *args, **kwargs):
        if view:
            if isinstance(view, string_types):
                kwargs["only"] = self.views[view]
            elif isinstance(view, list):
                kwargs["only"] = view

        super(HintTimerSchema, self).__init__(*args, **kwargs)
