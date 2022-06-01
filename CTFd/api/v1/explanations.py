import datetime
from typing import List

from flask import request, session

from flask import abort, render_template, request, url_for
from flask_restx import Namespace, Resource
from sqlalchemy import func as sa_func
from sqlalchemy.sql import and_, false, true

from CTFd.api.v1.helpers.request import validate_args
from CTFd.api.v1.helpers.schemas import sqlalchemy_to_pydantic
from CTFd.api.v1.schemas import APIDetailedSuccessResponse, APIListSuccessResponse
from CTFd.cache import clear_standings
from CTFd.constants import RawEnum
from CTFd.models import Explanations
from CTFd.models import db
from CTFd.plugins.challenges import CHALLENGE_CLASSES, get_chal_class
from CTFd.schemas.explanations import ExplanationSchema
from CTFd.utils import config, get_config
from CTFd.utils import user as current_user
from CTFd.utils.config.visibility import (
    accounts_visible,
    challenges_visible,
    scores_visible,
)
from CTFd.utils.dates import ctf_ended, ctf_paused, ctftime, isoformat, unix_time_to_utc
from CTFd.utils.decorators import (
    admins_only,
    during_ctf_time_only,
    require_verified_emails,
)
from CTFd.utils.decorators.visibility import (
    check_challenge_visibility,
    check_score_visibility,
)
from CTFd.utils.helpers.models import build_model_filters
from CTFd.utils.logging import log
from CTFd.utils.modes import generate_account_url, get_model
from CTFd.utils.security.signing import serialize
from CTFd.utils.user import (
    authed,
    get_current_team,
    get_current_team_attrs,
    get_current_user,
    get_current_user_attrs,
    is_admin,
)

explanations_namespace = Namespace(
    "explanations", description="Endpoint to retrieve Explanations"
)
ExplanationModel = sqlalchemy_to_pydantic(Explanations)
TransientExplanationModel = sqlalchemy_to_pydantic(Explanations, exclude=["id"])

class ExplanationDetailedSuccessResponse(APIDetailedSuccessResponse):
    data: ExplanationModel


class ExplanationListSuccessResponse(APIListSuccessResponse):
    data: List[ExplanationModel]


explanations_namespace.schema_model(
    "ExplanationDetailedSuccessResponse", ExplanationDetailedSuccessResponse.apidoc()
)

explanations_namespace.schema_model(
    "ExplanationListSuccessResponse", ExplanationListSuccessResponse.apidoc()
)

@explanations_namespace.route("")
class Explanation(Resource):
    @during_ctf_time_only
    @require_verified_emails
    @explanations_namespace.doc(
        description="Endpoint to get a every explanations / feedback",
        responses={
            200: ("Success", "ExplanationDetailedSuccessResponse"),
            400: (
                "An error occured processing the provided or stored data",
                "APISimpleErrorResponse",
            ),
        },
    )
    def get(self, query_args):
        q = query_args.pop("q", None)
        field = str(query_args.pop("field", None))
        ExplanationModel = Explanations
        filters = build_model_filters(model=ExplanationModel, query=q, field=field)

        explanations = (
            ExplanationModel.query.filter_by(**query_args)
            .filter(*filters)
            .order_by(ExplanationModel.id.desc())
            .paginate(max_per_page=100)
        )
        schema = ExplanationSchema(many=True)
        response = schema.dump(explanations.items)

        if response.errors:
            return {"success": False, "errors": response.errors}, 400

        return {
            "meta": {
                "pagination": {
                    "page": explanations.page,
                    "next": explanations.next_num,
                    "prev": explanations.prev_num,
                    "pages": explanations.pages,
                    "per_page": explanations.per_page,
                    "total": explanations.total,
                }
            },
            "success": True,
            "data": response.data,
        }
    def post(self):
        req = request.get_json()
        schema = ExplanationSchema()
        response = schema.load(req, session=db.session)

        if response.errors:
            return {"success": False, "errors": response.errors}, 400

        db.session.add(response.data)
        db.session.commit()

        response = schema.dump(response.data)
        db.session.close()

        return {"success": True, "data": response.data}




@explanations_namespace.route("/<explanation_id>")
class Explanation(Resource):
    @during_ctf_time_only
    @require_verified_emails
    @explanations_namespace.doc(
        description="Endpoint to get a specific Explanation object",
        responses={
            200: ("Success", "ExplanationDetailedSuccessResponse"),
            400: (
                "An error occured processing the provided or stored data",
                "APISimpleErrorResponse",
            ),
        },
    )
    def get(self, explanation_id):
        expl = Explanations.query.filter(Explanations.id == explanation_id).first_or_404()
 
        #response = expl_class.read(explanation=expl)
        response = expl
        
        db.session.close()
        return {"success": True, "data": response}
    
    @explanations_namespace.doc(
        description="Endpoint to create a specific Explanation object",
        responses={
            200: ("Success", "ExplanationDetailedSuccessResponse"),
            400: (
                "An error occured processing the provided or stored data",
                "APISimpleErrorResponse",
            ),
        },
    )
        
    @admins_only
    @explanations_namespace.doc(
        description="Endpoint to edit a specific Explanation object",
        responses={
            200: ("Success", "ExplanationDetailedSuccessResponse"),
            400: (
                "An error occured processing the provided or stored data",
                "APISimpleErrorResponse",
            ),
        },
    )
    def patch(self, explanation_id):
        data = request.get_json()

        # Load data through schema for validation but not for insertion
        schema = ExplanationSchema()
        response = schema.load(data)
        if response.errors:
            return {"success": False, "errors": response.errors}, 400

        explanation = Explanations.query.filter_by(id=explanation_id).first_or_404()
        response = explanation
        return {"success": True, "data": response}

    @admins_only
    @explanations_namespace.doc(
        description="Endpoint to delete a specific Explanation object",
        responses={200: ("Success", "APISimpleSuccessResponse")},
    )
    def delete(self, explanation_id):
        explanation = Explanations.query.filter_by(id=explanation_id).first_or_404()
        chal_class = get_chal_class(explanation.type)
        chal_class.delete(explanation)

        return {"success": True}
    
