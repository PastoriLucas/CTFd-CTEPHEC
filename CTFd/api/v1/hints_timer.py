from datetime import datetime, timedelta
from typing import List

from flask import request
from flask_restx import Namespace, Resource

from CTFd.api.v1.helpers.request import validate_args
from CTFd.api.v1.helpers.schemas import sqlalchemy_to_pydantic
from CTFd.api.v1.schemas import APIDetailedSuccessResponse, APIListSuccessResponse
from CTFd.constants import RawEnum
from CTFd.models import HintsTimer, Hints, HintUnlocks, Unlocks, db
from CTFd.schemas.hints_timer import HintTimerSchema
from CTFd.utils.decorators import admins_only, authed_only, during_ctf_time_only
from CTFd.utils.helpers.models import build_model_filters
from CTFd.utils.user import get_current_user, is_admin, is_observer

hintsTimer_namespace = Namespace("hintsTimer", description="Endpoint to retrieve HintsTimer")

HintTimerModel = sqlalchemy_to_pydantic(HintsTimer)

class HintTimerDetailedSuccessResponse(APIDetailedSuccessResponse):
    data: HintTimerModel


class HintTimerListSuccessResponse(APIListSuccessResponse):
    data: List[HintTimerModel]


hintsTimer_namespace.schema_model(
    "HintTimerDetailedSuccessResponse", HintTimerDetailedSuccessResponse.apidoc()
)

hintsTimer_namespace.schema_model(
    "HintTimerListSuccessResponse", HintTimerListSuccessResponse.apidoc()
)


@hintsTimer_namespace.route("")
class HintTimerList(Resource):
    @hintsTimer_namespace.doc(
        description="Endpoint to list HintTimer objects in bulk",
        responses={
            200: ("Success", "HintTimerListSuccessResponse"),
            400: (
                "An error occured processing the provided or stored data",
                "APISimpleErrorResponse",
            ),
        },
    )
    @validate_args(
        {
            "team_id": (int, None),
            "hint_id": (int, None),
            "end_time": (int, None),
        },
        location="query",
    )
    def get(self, query_args):
        q = query_args.pop("q", None)
        field = str(query_args.pop("field", None))
        filters = build_model_filters(model=HintsTimer, query=q, field=field)

        hintsTimer = HintsTimer.query.filter_by(**query_args).filter(*filters).all()
        response = HintTimerSchema(many=True, view="locked").dump(hintsTimer)

        if response.errors:
            return {"success": False, "errors": response.errors}, 400

        return {"success": True, "data": response.data}

    @hintsTimer_namespace.doc(
        description="Endpoint to create a HintTimer object",
        responses={
            200: ("Success", "HintTimerDetailedSuccessResponse"),
            400: (
                "An error occured processing the provided or stored data",
                "APISimpleErrorResponse",
            ),
        },
    )
    def post(self): 
        req = request.get_json()
        
        challenge = req["challenge_id"]
        team = req["team_id"]
        user = get_current_user()
        
        hint = Hints.query.filter_by(challenge_id=challenge).all()

        
        end_time = []
        hint_id = []
        
        for s in range(len(hint)):
               
            sameHintsTimerHint = HintsTimer.query.filter_by(hint_id = hint[s].id).first()
            sameHintsTimerTeam = HintsTimer.query.filter_by(team_id=team).all()
            alreadyUnlocked = Unlocks.query.filter_by(target = hint[s].id , team_id=team).first()
        
            if(sameHintsTimerHint):
                actual_time = datetime.now()
                end_date = sameHintsTimerHint.end_time.strftime('%Y-%m-%d %H:%M:%S')
                if(actual_time.strftime('%Y-%m-%d %H:%M:%S') > end_date ):
                    unlock = Unlocks(user_id = user.id, team_id = team, target= hint[s].id , date = end_date, type = "hints" ) 
                    db.session.add(unlock)
                    db.session.commit()
                        
                    db.session.delete(sameHintsTimerHint)
                    db.session.commit()
                    
            else:   
                if (alreadyUnlocked):
                    return {"success": True, "data": hint_id, "answer" : "This Hint is already asked !"}
                else :
                    if(len(sameHintsTimerTeam) < 3):  
                        
                        end_time.insert( s, datetime.now() + timedelta(seconds=hint[s].time))
                        end_time[s] = end_time[s].strftime('%Y-%m-%d %H:%M:%S')
                        hint_id.insert(s,hint[s].id ) 
                        
                        hint_timer = HintsTimer(team_id = team, hint_id = hint[s].id , end_time = end_time[s])
                        
                        db.session.add(hint_timer)
                        db.session.commit()
                        return {"success": True, "data": hint_id, "answer" : "Hint asked !"}
                    else : 
                        return {"success": True, "data": hint_id, "answer" : "You cannot ask for more than 3 hints at time !"}
            
        



@hintsTimer_namespace.route("/<hintTimer_id>")
class HintTimer(Resource):
    @during_ctf_time_only
    @authed_only
    @hintsTimer_namespace.doc(
        description="Endpoint to get a specific HintTimer object",
        responses={
            200: ("Success", "HintTimerDetailedSuccessResponse"),
            400: (
                "An error occured processing the provided or stored data",
                "APISimpleErrorResponse",
            ),
        },
    )
    def get(self, hintTimer_id):
        user = get_current_user()
        hintTimer = HintsTimer.query.filter_by(id=hintTimer_id).first_or_404()

        view = "unlocked"
        if hintTimer.cost:
            view = "locked"
            unlocked = HintUnlocks.query.filter_by(
                account_id=user.account_id, target=hintTimer.id
            ).first()
            if unlocked:
                view = "unlocked"

        if is_admin() or is_observer():
            if request.args.get("preview", False):
                view = "admin"

        response = HintTimerSchema(view=view).dump(hintTimer)

        if response.errors:
            return {"success": False, "errors": response.errors}, 400

        return {"success": True, "data": response.data}

    @admins_only
    @hintsTimer_namespace.doc(
        description="Endpoint to edit a specific HintTimer object",
        responses={
            200: ("Success", "HintDetailedSuccessResponse"),
            400: (
                "An error occured processing the provided or stored data",
                "APISimpleErrorResponse",
            ),
        },
    )
    def patch(self, hint_id):
        hintTimer = HintsTimer.query.filter_by(id=hint_id).first_or_404()
        req = request.get_json()

        schema = HintTimerSchema(view="admin")
        response = schema.load(req, instance=hintTimer, partial=True, session=db.session)

        if response.errors:
            return {"success": False, "errors": response.errors}, 400

        db.session.add(response.data)
        db.session.commit()

        response = schema.dump(response.data)

        return {"success": True, "data": response.data}

    @admins_only
    @hintsTimer_namespace.doc(
        description="Endpoint to delete a specific Tag object",
        responses={200: ("Success", "APISimpleSuccessResponse")},
    )
    def delete(self, hintTimer_id):
        hintTimer = HintsTimer.query.filter_by(id=hintTimer_id).first_or_404()
        db.session.delete(hintTimer)
        db.session.commit()
        db.session.close()

        return {"success": True}
    
@hintsTimer_namespace.route("/watch_hintsTimer")
class HintTimer(Resource):
    @during_ctf_time_only
    @authed_only
    @hintsTimer_namespace.doc(
        description="Endpoint to verify if a hints_timer is ended",
        responses={
            200: ("Success", "HintTimerDetailedSuccessResponse"),
            400: (
                "An error occured processing the provided or stored data",
                "APISimpleErrorResponse",
            ),
        },
    )
    def post(self):

        req = request.get_json()
         
        team = req["team_id"]
        user = get_current_user()
        challenge = req["challenge_id"]
        
        hint = Hints.query.filter_by(challenge_id=challenge).all()
        for s in range(len(hint)):
               
            sameHintsTimerHint = HintsTimer.query.filter_by(hint_id = hint[s].id).first()
            
            if(sameHintsTimerHint):
                actual_time = datetime.now()
                end_date = sameHintsTimerHint.end_time.strftime('%Y-%m-%d %H:%M:%S')
                if(actual_time.strftime('%Y-%m-%d %H:%M:%S') > end_date ):
                    unlock = Unlocks(user_id = user.id, team_id = team, target= hint[s].id , date = end_date, type = "hints" ) 
                    db.session.add(unlock)
                    db.session.commit()
                        
                    db.session.delete(sameHintsTimerHint)
                    db.session.commit()
                    return {"success": True, "data": sameHintsTimerHint.id,}
