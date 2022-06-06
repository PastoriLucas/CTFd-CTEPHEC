from webbrowser import get
from flask import Blueprint, abort, redirect, render_template, request, url_for
from sqlalchemy import false, true

from CTFd.cache import clear_team_session, clear_user_session
from CTFd.exceptions import TeamTokenExpiredException, TeamTokenInvalidException
from CTFd.models import Challenges, Solves, TeamFieldEntries, TeamFields, Teams, Users, db
from CTFd.utils import config, get_config, validators
from CTFd.utils.crypto import verify_password
from CTFd.utils.decorators import authed_only, ratelimit, registered_only
from CTFd.utils.decorators.modes import require_team_mode
from CTFd.utils.decorators.visibility import (
    check_account_visibility,
    check_score_visibility,
)
from CTFd.utils.helpers import get_errors, get_infos
from CTFd.utils.humanize.words import pluralize
from CTFd.utils.user import get_current_user, get_current_user_attrs

teams = Blueprint("teams", __name__)


@teams.route("/teams")
@check_account_visibility
@require_team_mode
def listing():
    q = request.args.get("q")
    field = request.args.get("field", "name")
    filters = []

    if field not in ("name", "affiliation", "website"):
        field = "name"

    if q:
        filters.append(getattr(Teams, field).like("%{}%".format(q)))

    teams = (
        Teams.query.filter_by(hidden=False, banned=False)
        .filter(*filters)
        .order_by(Teams.id.asc())
        .paginate(per_page=50)
    )

    args = dict(request.args)
    args.pop("page", 1)

    return render_template(
        "teams/teams.html",
        teams=teams,
        prev_page=url_for(request.endpoint, page=teams.prev_num, **args),
        next_page=url_for(request.endpoint, page=teams.next_num, **args),
        q=q,
        field=field,
    )


@teams.route("/teams/invite", methods=["GET", "POST"])
@registered_only
@require_team_mode
def invite():
    infos = get_infos()
    errors = get_errors()
    code = request.args.get("code")

    if code is None:
        abort(404)

    user = get_current_user_attrs()
    if user.team_id:
        errors.append("You are already in a team. You cannot join another.")

    try:
        team = Teams.load_invite_code(code)
    except TeamTokenExpiredException:
        abort(403, description="This invite URL has expired")
    except TeamTokenInvalidException:
        abort(403, description="This invite URL is invalid")

    team_size_limit = get_config("team_size", default=0)

    if request.method == "GET":
        if team_size_limit:
            infos.append(
                "Teams are limited to {limit} member{plural}".format(
                    limit=team_size_limit, plural=pluralize(number=team_size_limit)
                )
            )

        return render_template(
            "teams/invite.html", team=team, infos=infos, errors=errors
        )

    if request.method == "POST":
        if errors:
            return (
                render_template(
                    "teams/invite.html", team=team, infos=infos, errors=errors
                ),
                403,
            )

        if team_size_limit and len(team.members) >= team_size_limit:
            errors.append(
                "{name} has already reached the team size limit of {limit}".format(
                    name=team.name, limit=team_size_limit
                )
            )
            return (
                render_template(
                    "teams/invite.html", team=team, infos=infos, errors=errors
                ),
                403,
            )

        user = get_current_user()
        user.team_id = team.id
        db.session.commit()

        clear_user_session(user_id=user.id)
        clear_team_session(team_id=team.id)

        return redirect(url_for("challenges.listing"))


@teams.route("/teams/join", methods=["GET", "POST"])
@authed_only
@require_team_mode
@ratelimit(method="POST", limit=10, interval=5)
def join():
    infos = get_infos()
    errors = get_errors()

    user = get_current_user_attrs()
    if user.team_id:
        errors.append("You are already in a team. You cannot join another.")

    if request.method == "GET":
        team_size_limit = get_config("team_size", default=0)
        if team_size_limit:
            plural = "" if team_size_limit == 1 else "s"
            infos.append(
                "Teams are limited to {limit} member{plural}".format(
                    limit=team_size_limit, plural=plural
                )
            )
        return render_template("teams/join_team.html", infos=infos, errors=errors)

    if request.method == "POST":
        teamname = request.form.get("name")
        passphrase = request.form.get("password", "").strip()

        team = Teams.query.filter_by(name=teamname).first()

        if errors:
            return (
                render_template("teams/join_team.html", infos=infos, errors=errors),
                403,
            )

        if team and verify_password(passphrase, team.password):
            team_size_limit = get_config("team_size", default=0)
            if team_size_limit and len(team.members) >= team_size_limit:
                errors.append(
                    "{name} has already reached the team size limit of {limit}".format(
                        name=team.name, limit=team_size_limit
                    )
                )
                return render_template(
                    "teams/join_team.html", infos=infos, errors=errors
                )

            user = get_current_user()
            user.team_id = team.id
            modifier = 0
            for member in team.members:
                if(member.year == 1):
                    modifier += int(get_config("first_year_modifier"))
                if(member.year == 2):
                    modifier += int(get_config("second_year_modifier"))
                if(member.year == 3):
                    modifier += int(get_config("third_year_modifier"))
                if(member.year == 4):
                    modifier += int(get_config("old_student_modifier"))
                print(modifier)
                
            if(user.year == 1):
                modifier += int(get_config("first_year_modifier"))
            if(user.year == 2):
                modifier += int(get_config("second_year_modifier"))
            if(user.year == 3):
                modifier += int(get_config("third_year_modifier"))
            if(user.year == 4):
                modifier += int(get_config("old_student_modifier"))
                       
                    
            modifier = modifier/ (len(team.members)  +1)            
            team.modifier = modifier
            
            db.session.commit()

            if len(team.members) == 1:
                team.captain_id = user.id
                db.session.commit()

            clear_user_session(user_id=user.id)
            clear_team_session(team_id=team.id)

            return redirect(url_for("challenges.listing"))
        else:
            errors.append("That information is incorrect")
            return render_template("teams/join_team.html", infos=infos, errors=errors)


@teams.route("/teams/new", methods=["GET", "POST"])
@authed_only
@require_team_mode
def new():
    infos = get_infos()
    errors = get_errors()

    if bool(get_config("team_creation", default=True)) is False:
        abort(
            403,
            description="Team creation is currently disabled. Please join an existing team.",
        )

    num_teams_limit = int(get_config("num_teams", default=0))
    num_teams = Teams.query.filter_by(banned=False, hidden=False).count()
    if num_teams_limit and num_teams >= num_teams_limit:
        abort(
            403,
            description=f"Reached the maximum number of teams ({num_teams_limit}). Please join an existing team.",
        )

    user = get_current_user_attrs()
    if user.team_id:
        errors.append("You are already in a team. You cannot join another.")

    if request.method == "GET":
        team_size_limit = get_config("team_size", default=0)
        if team_size_limit:
            plural = "" if team_size_limit == 1 else "s"
            infos.append(
                "Teams are limited to {limit} member{plural}".format(
                    limit=team_size_limit, plural=plural
                )
            )
        return render_template("teams/new_team.html", infos=infos, errors=errors)

    elif request.method == "POST":
        teamname = request.form.get("name", "").strip()
        passphrase = request.form.get("password", "").strip()

        website = request.form.get("website")
        affiliation = request.form.get("affiliation")

        user = get_current_user()
    
        existing_team = Teams.query.filter_by(name=teamname).first()
        if existing_team:
            errors.append("That team name is already taken")
        if not teamname:
            errors.append("That team name is invalid")

        # Process additional user fields
        fields = {}
        for field in TeamFields.query.all():
            fields[field.id] = field

        entries = {}
        for field_id, field in fields.items():
            value = request.form.get(f"fields[{field_id}]", "").strip()
            if field.required is True and (value is None or value == ""):
                errors.append("Please provide all required fields")
                break

            # Handle special casing of existing profile fields
            if field.name.lower() == "affiliation":
                affiliation = value
                break
            elif field.name.lower() == "website":
                website = value
                break

            if field.field_type == "boolean":
                entries[field_id] = bool(value)
            else:
                entries[field_id] = value

        if website:
            valid_website = validators.validate_url(website)
        else:
            valid_website = True

        if affiliation:
            valid_affiliation = len(affiliation) < 128
        else:
            valid_affiliation = True

        if valid_website is False:
            errors.append("Websites must be a proper URL starting with http or https")
        if valid_affiliation is False:
            errors.append("Please provide a shorter affiliation")

        if errors:
            return render_template("teams/new_team.html", errors=errors), 403

        team = Teams(name=teamname, password=passphrase, captain_id=user.id)

       
        modifier = 0
        print(get_config("first_year_modifier"))
    
        if(user.year == 1):
            modifier += int(get_config("first_year_modifier"))
        if(user.year == 2):
            modifier += int(get_config("second_year_modifier"))
        if(user.year == 3):
            modifier += int(get_config("third_year_modifier"))
        if(user.year == 4):
            modifier += int(get_config("old_student_modifier"))
                       
    
        team.modifier = modifier
            
        if website:
            team.website = website
        if affiliation:
            team.affiliation = affiliation

        db.session.add(team)
        db.session.commit()

        for field_id, value in entries.items():
            entry = TeamFieldEntries(field_id=field_id, value=value, team_id=team.id)
            db.session.add(entry)
        db.session.commit()

        user.team_id = team.id
        db.session.commit()

        clear_user_session(user_id=user.id)
        clear_team_session(team_id=team.id)

        return redirect(url_for("challenges.listing"))


@teams.route("/team")
@authed_only
@require_team_mode
def private():
    infos = get_infos()
    errors = get_errors()

    user = get_current_user()
    if not user.team_id:
        return render_template("teams/team_enrollment.html")

    team_id = user.team_id

    team = Teams.query.filter_by(id=team_id).first_or_404()
    solves = team.get_solves()
    print(solves)
    awards = team.get_awards()
    team_users = Users.query.filter_by(team_id=team.id).all()

    place = team.place
    score = team.score
    
    firstblood = []
    categoryBreakdown = []
    categoryFirstblood = []
    all_category_of_this_team = []
    chall_of_this_solve = []
    solve_per_team = []
    
    ## watch out for firstblood and categoryBreakdown and categoryFirstblood
    for solve in solves :
        first = True                                               ## allow to watch if we are the first team to succes
        all_solves_of_a_challenge = Solves.query.filter_by(challenge_id=solve.challenge_id).all() ##get every solves for this challenge
        chall_of_this_solve = Challenges.query.filter_by(id=solve.challenge_id).first_or_404() ##get the chal for this solve
        if(len(all_category_of_this_team) != 0 ):                  ## verify if the array is null
            new = True                                             ## allow to put a new category for this team
            for i in all_category_of_this_team:                    ## go throught the array which contains every category for this team
                if(i["name"] == chall_of_this_solve.category):     ## if the category already exist in this array 
                    i["count"] += 1                                ## add 1 in the count
                    new = False                                     ## prevent it to be new and add again
                    if(solve.date > i["time"]):
                        i["time"] = solve.date
            if(new):
                all_category_of_this_team.append({"name" : chall_of_this_solve.category, "count" : 1, "time": solve.date}) ## put a new category for this team
                
        else :
            all_category_of_this_team.append({"name" : chall_of_this_solve.category, "count" : 1, "time": solve.date}) ## put a new category for this team

        for solve_of_a_challenge in all_solves_of_a_challenge:                         ## verify if we are the first to solve it
            if(solve.date > solve_of_a_challenge.date):
                first = False
            if(len(solve_per_team) != 0):
                new = True
                for i in solve_per_team:                                                                            ## go throught the array which contains every category for this team
                    if(i["name"] == chall_of_this_solve.category and i["team_id"] == solve_of_a_challenge.team_id):     ## if the category already exist in this array 
                        i["count"] += 1                                                                              ## add 1 in the count
                        new = False                                                                                 ## prevent it to be new and add again
                        if(solve_of_a_challenge.date > i["time"] and solve_of_a_challenge.team_id == i['team_id']):
                            i["time"] = solve_of_a_challenge.date
                if(new):
                    solve_per_team.append({"team_id" :solve_of_a_challenge.team_id ,"name" : chall_of_this_solve.category, "count" : 1, "time": solve_of_a_challenge.date}) ## put a new category for this team
                
            else :
                solve_per_team.append({"team_id" :solve_of_a_challenge.team_id ,"name" : chall_of_this_solve.category, "count" : 1, "time": solve_of_a_challenge.date}) ## put a new category for this team
                
        
        if(first):                                          ## if we are first, add in firstblood
            firstblood.append(chall_of_this_solve.name)
            solve.firstblood = true
            
    for category in all_category_of_this_team:
        firstCategory = True
        every_chal_with_this_category = Challenges.query.filter_by(category = category["name"]).all() ##get every chal of the same category
        if(len(every_chal_with_this_category) == category["count"]):
            categoryBreakdown.append(category["name"])
            for each_team_solve in solve_per_team:
                if (len(every_chal_with_this_category) == each_team_solve["count"] and category["time"] > each_team_solve["time"] and category['name'] == each_team_solve["name"]):
                    firstCategory = False
            if(firstCategory):
                categoryFirstblood.append(category["name"])

    if config.is_scoreboard_frozen():
        infos.append("Scoreboard has been frozen")
    

    return render_template(
        "teams/private.html",
        solves=solves,
        awards=awards,
        user=user,
        firstblood=firstblood,
        categoryBreakdown=categoryBreakdown,
        categoryFirstblood=categoryFirstblood,
        team=team,
        score=score,
        place=place,
        score_frozen=config.is_scoreboard_frozen(),
        infos=infos,
        errors=errors,
    )


@teams.route("/teams/<int:team_id>")
@check_account_visibility
@check_score_visibility
@require_team_mode
def public(team_id):
    infos = get_infos()
    errors = get_errors()
    team = Teams.query.filter_by(id=team_id, banned=False, hidden=False).first_or_404()
    solves = team.get_solves()
    awards = team.get_awards()

    place = team.place
    score = team.score
    
    firstblood = []
    categoryBreakdown = []
    categoryFirstblood = []
    all_category_of_this_team = []
    chall_of_this_solve = []
    solve_per_team = []
    
   ## watch out for firstblood and categoryBreakdown and categoryFirstblood
    for solve in solves :
        first = True                                               ## allow to watch if we are the first team to succes
        all_solves_of_a_challenge = Solves.query.filter_by(challenge_id=solve.challenge_id).all() ##get every solves for this challenge
        chall_of_this_solve = Challenges.query.filter_by(id=solve.challenge_id).first_or_404() ##get the chal for this solve
        if(len(all_category_of_this_team) != 0 ):                  ## verify if the array is null
            new = True                                             ## allow to put a new category for this team
            for i in all_category_of_this_team:                    ## go throught the array which contains every category for this team
                if(i["name"] == chall_of_this_solve.category):     ## if the category already exist in this array 
                    i["count"] += 1                                ## add 1 in the count
                    new = False                                     ## prevent it to be new and add again
                    if(solve.date > i["time"]):
                        i["time"] = solve.date
            if(new):
                all_category_of_this_team.append({"name" : chall_of_this_solve.category, "count" : 1, "time": solve.date}) ## put a new category for this team
                
        else :
            all_category_of_this_team.append({"name" : chall_of_this_solve.category, "count" : 1, "time": solve.date}) ## put a new category for this team

        for solve_of_a_challenge in all_solves_of_a_challenge:                         ## verify if we are the first to solve it
            if(solve.date > solve_of_a_challenge.date):
                first = False
            if(len(solve_per_team) != 0):
                new = True
                for i in solve_per_team:                                                                            ## go throught the array which contains every category for this team
                    if(i["name"] == chall_of_this_solve.category and i["team_id"] == solve_of_a_challenge.team_id):     ## if the category already exist in this array 
                        i["count"] += 1                                                                              ## add 1 in the count
                        new = False                                                                                 ## prevent it to be new and add again
                        if(solve_of_a_challenge.date > i["time"] and solve_of_a_challenge.team_id == i['team_id']):
                            i["time"] = solve_of_a_challenge.date
                if(new):
                    solve_per_team.append({"team_id" :solve_of_a_challenge.team_id ,"name" : chall_of_this_solve.category, "count" : 1, "time": solve_of_a_challenge.date}) ## put a new category for this team
                
            else :
                solve_per_team.append({"team_id" :solve_of_a_challenge.team_id ,"name" : chall_of_this_solve.category, "count" : 1, "time": solve_of_a_challenge.date}) ## put a new category for this team
                
        
        if(first):                                          ## if we are first, add in firstblood
            firstblood.append(chall_of_this_solve.name)
            solve.firstblood = true
            
    for category in all_category_of_this_team:
        firstCategory = True
        every_chal_with_this_category = Challenges.query.filter_by(category = category["name"]).all() ##get every chal of the same category
        if(len(every_chal_with_this_category) == category["count"]):
            categoryBreakdown.append(category["name"])
            for each_team_solve in solve_per_team:
                if (len(every_chal_with_this_category) == each_team_solve["count"] and category["time"] > each_team_solve["time"] and category['name'] == each_team_solve["name"]):
                    firstCategory = False
            if(firstCategory):
                categoryFirstblood.append(category["name"])
            

    if errors:
        return render_template("teams/public.html", team=team, errors=errors)

    if config.is_scoreboard_frozen():
        infos.append("Scoreboard has been frozen")

    return render_template(
        "teams/public.html",
        solves=solves,
        awards=awards,
        team=team,
        score=score,
        firstblood=firstblood,
        categoryBreakdown=categoryBreakdown,
        categoryFirstblood=categoryFirstblood,
        place=place,
        score_frozen=config.is_scoreboard_frozen(),
        infos=infos,
        errors=errors,
    )
