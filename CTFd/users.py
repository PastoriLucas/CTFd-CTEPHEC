from flask import Blueprint, render_template, request, url_for
from sqlalchemy import false, null, true
from CTFd.admin import challenges

from CTFd.models import Challenges, Solves, Users, Teams
from CTFd.utils import config
from CTFd.utils.decorators import authed_only
from CTFd.utils.decorators.visibility import (
    check_account_visibility,
    check_score_visibility,
)
from CTFd.utils.helpers import get_errors, get_infos
from CTFd.utils.user import get_current_user

users = Blueprint("users", __name__)


@users.route("/users")
@check_account_visibility
def listing():
    q = request.args.get("q")
    field = request.args.get("field", "name")
    if field not in ("name", "affiliation", "website"):
        field = "name"

    filters = []
    if q:
        filters.append(getattr(Users, field).like("%{}%".format(q)))

    users = (
        Users.query.filter_by(banned=False, hidden=False)
        .filter(*filters)
        .order_by(Users.id.asc())
        .paginate(per_page=50)
    )

    args = dict(request.args)
    args.pop("page", 1)

    return render_template(
        "users/users.html",
        users=users,
        prev_page=url_for(request.endpoint, page=users.prev_num, **args),
        next_page=url_for(request.endpoint, page=users.next_num, **args),
        q=q,
        field=field,
    )


@users.route("/profile")
@users.route("/user")
@authed_only
def private():
    
    user = get_current_user()
    firstblood = []
    categoryBreakdown = []
    categoryFirstblood = []
    all_category_of_this_user = []
    chall_of_this_solve = []
    solve_per_user = []
    team = Teams.query.filter_by(id=user.team_id).first()
    if (team is not None):
        
        ## watch out for firstblood and categoryBreakdown and categoryFirstblood
        solves = user.solves
        for solve in solves :
            first = True                                               ## allow to watch if we are the first user to succes
            all_solves_of_a_challenge = Solves.query.filter_by(challenge_id=solve.challenge_id).all() ##get every solves for this challenge
            chall_of_this_solve = Challenges.query.filter_by(id=solve.challenge_id).first_or_404() ##get the chal for this solve
            if(len(all_category_of_this_user) != 0 ):                  ## verify if the array is null
                new = True                                             ## allow to put a new category for this user
                for i in all_category_of_this_user:                    ## go throught the array which contains every category for this user
                    if(i["name"] == chall_of_this_solve.category):     ## if the category already exist in this array 
                        i["count"] += 1                                ## add 1 in the count
                        new = False                                     ## prevent it to be new and add again
                        if(solve.date > i["time"]):
                            i["time"] = solve.date
                if(new):
                    all_category_of_this_user.append({"name" : chall_of_this_solve.category, "count" : 1, "time": solve.date}) ## put a new category for this user
                    
            else :
                all_category_of_this_user.append({"name" : chall_of_this_solve.category, "count" : 1, "time": solve.date}) ## put a new category for this user

            for solve_of_a_challenge in all_solves_of_a_challenge:                         ## verify if we are the first to solve it
                if(solve.date > solve_of_a_challenge.date):
                    first = False
                if(len(solve_per_user) != 0):
                    new = True
                    for i in solve_per_user:                                                                            ## go throught the array which contains every category for this user
                        if(i["name"] == chall_of_this_solve.category and i["user_id"] == solve_of_a_challenge.user_id):     ## if the category already exist in this array 
                            i["count"] += 1                                                                              ## add 1 in the count
                            new = False                                                                                 ## prevent it to be new and add again
                            if(solve_of_a_challenge.date > i["time"] and solve_of_a_challenge.user_id == i['user_id']):
                                i["time"] = solve_of_a_challenge.date
                    if(new):
                        solve_per_user.append({"user_id" :solve_of_a_challenge.user_id ,"name" : chall_of_this_solve.category, "count" : 1, "time": solve_of_a_challenge.date}) ## put a new category for this user
                    
                else :
                    solve_per_user.append({"user_id" :solve_of_a_challenge.user_id ,"name" : chall_of_this_solve.category, "count" : 1, "time": solve_of_a_challenge.date}) ## put a new category for this user
                    
            
            if(first):                                          ## if we are first, add in firstblood
                firstblood.append(chall_of_this_solve.name)
                solve.firstblood = true
                
        for category in all_category_of_this_user:
            firstCategory = True
            every_chal_with_this_category = Challenges.query.filter_by(category = category["name"]).all() ##get every chal of the same category
            if(len(every_chal_with_this_category) == category["count"]):
                categoryBreakdown.append(category["name"])
                for each_user_solve in solve_per_user:
                    if (len(every_chal_with_this_category) == each_user_solve["count"] and category["time"] > each_user_solve["time"] and category['name'] == each_user_solve["name"]):
                        firstCategory = False
                if(firstCategory):
                    categoryFirstblood.append(category["name"])
    
        modifier = team.modifier
        
    else :
        modifier = 100
        
    infos = get_infos()
    errors = get_errors()
    if config.is_scoreboard_frozen():
        infos.append("Scoreboard has been frozen")

    return render_template(
        "users/private.html",
        user=user,
        account=user.account,
        infos=infos,
        team=team,
        errors=errors,
        categoryBreakdown=categoryBreakdown,
        categoryFirstblood=categoryFirstblood,
        firstblood =firstblood,
        modifier=modifier
    )


@users.route("/users/<int:user_id>")
@check_account_visibility
@check_score_visibility
def public(user_id):
    infos = get_infos()
    errors = get_errors()
    user = Users.query.filter_by(id=user_id, banned=False, hidden=False).first_or_404()
    team = Teams.query.filter_by(id=user.team_id).first_or_404()
    modifier = team.modifier
    
    firstblood = []
    categoryBreakdown = []
    categoryFirstblood = []
    all_category_of_this_user = []
    chall_of_this_solve = []
    solve_per_user = []
    
    ## watch out for firstblood and categoryBreakdown and categoryFirstblood
    solves = user.solves
    for solve in solves :
        first = True                                               ## allow to watch if we are the first user to succes
        all_solves_of_a_challenge = Solves.query.filter_by(challenge_id=solve.challenge_id).all() ##get every solves for this challenge
        chall_of_this_solve = Challenges.query.filter_by(id=solve.challenge_id).first_or_404() ##get the chal for this solve
        if(len(all_category_of_this_user) != 0 ):                  ## verify if the array is null
            new = True                                             ## allow to put a new category for this user
            for i in all_category_of_this_user:                    ## go throught the array which contains every category for this user
                if(i["name"] == chall_of_this_solve.category):     ## if the category already exist in this array 
                    i["count"] += 1                                ## add 1 in the count
                    new = False                                     ## prevent it to be new and add again
                    if(solve.date > i["time"]):
                        i["time"] = solve.date
            if(new):
                all_category_of_this_user.append({"name" : chall_of_this_solve.category, "count" : 1, "time": solve.date}) ## put a new category for this user
                
        else :
            all_category_of_this_user.append({"name" : chall_of_this_solve.category, "count" : 1, "time": solve.date}) ## put a new category for this user

        for solve_of_a_challenge in all_solves_of_a_challenge:                         ## verify if we are the first to solve it
            if(solve.date > solve_of_a_challenge.date):
                first = False
            if(len(solve_per_user) != 0):
                new = True
                for i in solve_per_user:                                                                            ## go throught the array which contains every category for this user
                    if(i["name"] == chall_of_this_solve.category and i["user_id"] == solve_of_a_challenge.user_id):     ## if the category already exist in this array 
                        i["count"] += 1                                                                              ## add 1 in the count
                        new = False                                                                                 ## prevent it to be new and add again
                        if(solve_of_a_challenge.date > i["time"] and solve_of_a_challenge.user_id == i['user_id']):
                            i["time"] = solve_of_a_challenge.date
                if(new):
                    solve_per_user.append({"user_id" :solve_of_a_challenge.user_id ,"name" : chall_of_this_solve.category, "count" : 1, "time": solve_of_a_challenge.date}) ## put a new category for this user
                
            else :
                solve_per_user.append({"user_id" :solve_of_a_challenge.user_id ,"name" : chall_of_this_solve.category, "count" : 1, "time": solve_of_a_challenge.date}) ## put a new category for this user
                
        
        if(first):                                          ## if we are first, add in firstblood
            firstblood.append(chall_of_this_solve.name)
            solve.firstblood = true
            
    for category in all_category_of_this_user:
        firstCategory = True
        every_chal_with_this_category = Challenges.query.filter_by(category = category["name"]).all() ##get every chal of the same category
        if(len(every_chal_with_this_category) == category["count"]):
            categoryBreakdown.append(category["name"])
            for each_user_solve in solve_per_user:
                if (len(every_chal_with_this_category) == each_user_solve["count"] and category["time"] > each_user_solve["time"] and category['name'] == each_user_solve["name"]):
                    firstCategory = False
            if(firstCategory):
                categoryFirstblood.append(category["name"])

    if config.is_scoreboard_frozen():
        infos.append("Scoreboard has been frozen")

    return render_template(
        "users/public.html", user=user, account=user.account, infos=infos, errors=errors, modifier=modifier,firstblood=firstblood,categoryBreakdown=categoryBreakdown,categoryFirstblood=categoryFirstblood
    )

