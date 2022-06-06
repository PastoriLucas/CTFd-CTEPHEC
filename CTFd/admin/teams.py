from flask import render_template, request, url_for
from sqlalchemy import false, true
from sqlalchemy.sql import not_

from CTFd.admin import admin
from CTFd.models import Challenges, Solves, Teams, Tracking, db
from CTFd.utils import get_config
from CTFd.utils.decorators import admins_only
from CTFd.utils.user import get_current_user


@admin.route("/admin/teams")
@admins_only
def teams_listing():
    q = request.args.get("q")
    field = request.args.get("field")
    page = abs(request.args.get("page", 1, type=int))
    filters = []

    current_user = get_current_user()
    
    all_teams = Teams.query.all()
    
    if q:
        # The field exists as an exposed column
        if Teams.__mapper__.has_property(field):
            filters.append(getattr(Teams, field).like("%{}%".format(q)))

    teams = (
        Teams.query.filter(*filters)
        .order_by(Teams.id.asc())
        .paginate(page=page, per_page=50)
    )

    
    for team in all_teams:
        if (team.modifier is None):     
           
            team.modifier = 100
            db.session.commit()
                
    args = dict(request.args)
    args.pop("page", 1)

    return render_template(
        "admin/teams/teams.html",
        teams=teams,
        current_user_type = current_user.type,
        prev_page=url_for(request.endpoint, page=teams.prev_num, **args),
        next_page=url_for(request.endpoint, page=teams.next_num, **args),
        q=q,
        field=field,
    )


@admin.route("/admin/teams/new")
@admins_only
def teams_new():
    return render_template("admin/teams/new.html")


@admin.route("/admin/teams/<int:team_id>")
@admins_only
def teams_detail(team_id):
    team = Teams.query.filter_by(id=team_id).first()
    
    current_user = get_current_user()

    # Get members
    members = team.members
    member_ids = [member.id for member in members]

    # Get Solves for all members
    solves = team.get_solves(admin=True)
    fails = team.get_fails(admin=True)
    awards = team.get_awards(admin=True)
    score = team.get_score(admin=True)
    place = team.get_place(admin=True)
    
    
    # Get the score modifier based on total number of years
    
    modifier = 100

    # Get missing Challenges for all members
    # TODO: How do you mark a missing challenge for a team?
    solve_ids = [s.challenge_id for s in solves]
    missing = Challenges.query.filter(not_(Challenges.id.in_(solve_ids))).all()

    # Get addresses for all members
    addrs = (
        Tracking.query.filter(Tracking.user_id.in_(member_ids))
        .order_by(Tracking.date.desc())
        .all()
    )
    
    firstblood = []
    categoryBreakdown = []
    categoryFirstblood = []
    all_category_of_this_team = []
    chall_of_this_solve = []
    solve_per_team = []
    
    if(team is not None) :
    
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
        
        
        modifier = 0
        if(len(team.members)):
            for member in team.members:
                if(member.year == 1):
                    modifier += int(get_config("first_year_modifier"))
                if(member.year == 2):
                    modifier += int(get_config("second_year_modifier"))
                if(member.year == 3):
                    modifier += int(get_config("third_year_modifier"))
                if(member.year == 4):
                    modifier += int(get_config("old_student_modifier"))
                    
            modifier = modifier/ (len(team.members))            
            
            team.modifier = modifier
        else:
            modifier = 100
        db.session.commit()
        
    else:
        modifier = 100 

    return render_template(
        "admin/teams/team.html",
        team=team,
        mdifier = modifier,
        members=members,
        current_user_type = current_user.type,
        score=score,
        place=place,
        solves=solves,
        firstblood=firstblood,
        categoryBreakdown=categoryBreakdown,
        categoryFirstblood=categoryFirstblood,
        fails=fails,
        missing=missing,
        awards=awards,
        addrs=addrs,
        modifier=modifier
    )
