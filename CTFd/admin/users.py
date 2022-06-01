from flask import render_template, request, url_for
from sqlalchemy import false, true
from sqlalchemy.sql import not_

from CTFd.admin import admin
from CTFd.models import Challenges, Solves, Tracking, Users
from CTFd.utils import get_config
from CTFd.utils.decorators import admins_only
from CTFd.utils.modes import TEAMS_MODE
from CTFd.utils.user import get_current_user


@admin.route("/admin/users")
@admins_only
def users_listing():
    q = request.args.get("q")
    field = request.args.get("field")
    page = abs(request.args.get("page", 1, type=int))
    filters = []
    users = []
    
    current_user = get_current_user()

    if q:
        # The field exists as an exposed column
        if Users.__mapper__.has_property(field):
            filters.append(getattr(Users, field).like("%{}%".format(q)))

    if q and field == "ip":
        users = (
            Users.query.join(Tracking, Users.id == Tracking.user_id)
            .filter(Tracking.ip.like("%{}%".format(q)))
            .order_by(Users.id.asc())
            .paginate(page=page, per_page=50)
        )
    else:
        users = (
            Users.query.filter(*filters)
            .order_by(Users.id.asc())
            .paginate(page=page, per_page=50)
        )

    args = dict(request.args)
    args.pop("page", 1)

    return render_template(
        "admin/users/users.html",
        users=users,
        current_user_type = current_user.type,
        prev_page=url_for(request.endpoint, page=users.prev_num, **args),
        next_page=url_for(request.endpoint, page=users.next_num, **args),
        q=q,
        field=field,
    )


@admin.route("/admin/users/new")
@admins_only
def users_new():
    return render_template("admin/users/new.html")


@admin.route("/admin/users/<int:user_id>")
@admins_only
def users_detail(user_id):
    # Get user object
    user = Users.query.filter_by(id=user_id).first_or_404()
    
    current_user = get_current_user()

    # Get the user's solves
    solves = user.get_solves(admin=True)

    # Get challenges that the user is missing
    if get_config("user_mode") == TEAMS_MODE:
        if user.team:
            all_solves = user.team.get_solves(admin=True)
        else:
            all_solves = user.get_solves(admin=True)
    else:
        all_solves = user.get_solves(admin=True)

    solve_ids = [s.challenge_id for s in all_solves]
    missing = Challenges.query.filter(not_(Challenges.id.in_(solve_ids))).all()

    # Get IP addresses that the User has used
    addrs = (
        Tracking.query.filter_by(user_id=user_id).order_by(Tracking.date.desc()).all()
    )

    # Get Fails
    fails = user.get_fails(admin=True)

    # Get Awards
    awards = user.get_awards(admin=True)

    # Check if the user has an account (team or user)
    # so that we don't throw an error if they dont
    if user.account:
        score = user.account.get_score(admin=True)
        place = user.account.get_place(admin=True)
    else:
        score = None
        place = None
        
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
                
    return render_template(
        "admin/users/user.html",
        solves=solves,
        current_user_type = current_user.type,
        user=user,
        firstblood=firstblood,
        categoryFirstblood=categoryFirstblood,
        categoryBreakdown=categoryBreakdown,
        addrs=addrs,
        score=score,
        missing=missing,
        place=place,
        fails=fails,
        awards=awards,
    )
