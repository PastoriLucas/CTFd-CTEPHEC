from flask import abort, render_template, request, url_for

from CTFd.admin import admin
from CTFd.models import Challenges, Explanations, Users
from CTFd.plugins.explanations import EXPLANATION_CLASSES, get_exp_class
from CTFd.utils.decorators import admins_only


@admin.route("/admin/explanations")
@admins_only
def explanation_listing():
    q = request.args.get("q")
    field = request.args.get("field")
    filters = []
    
    users = []
    challenges = []

    if q:
        # The field exists as an exposed column
        if Explanations.__mapper__.has_property(field):
            filters.append(getattr(Explanations, field).like("%{}%".format(q)))

    query = Explanations.query.filter(*filters).order_by(Explanations.id.asc())
    explanations = query.all()
    explanations_brief_content = []
    
    for i in range(len(explanations)):
        actualUser = Users.query.filter_by(id=explanations[i].user_id).first_or_404()
        actualChallenge = Challenges.query.filter_by(id=explanations[i].challenge_id).first_or_404()
        users.insert(i, actualUser)
        challenges.insert(i,actualChallenge)
        
    for j in range(len(explanations)):
        content = explanations[j].content
        length = len(content)
        brief = ""
        if (length < 25):
            for i in range(length):
                brief += content[i]
        if (length > 25):
            for i in range(25):
                brief += content[i]
        explanations_brief_content.insert(j, brief)
        
    print(explanations_brief_content)
            
    total = query.count()

    return render_template(
        "admin/explanations/explanations.html",
        users = users,
        challenges = challenges,
        explanations=explanations,
        content = explanations_brief_content,
        total=total,
        q=q,
        field=field,
    )


@admin.route("/admin/explanations/<int:explanation_id>")
@admins_only
def explanation_detail(explanation_id):
    
    explanation = Explanations.query.filter_by(id=explanation_id).first_or_404()
    
    user = Users.query.filter_by(id=explanation.user_id).first_or_404()
    challenge = Challenges.query.filter_by(id=explanation.challenge_id).first_or_404()

 
    return render_template(
        "admin/explanations/explanation.html",

        explanation=explanation,
        user = user.name,
        challenge = challenge.name,
    )


@admin.route("/admin/explanations/new")
@admins_only
def explanation_new():
    types = EXPLANATION_CLASSES.keys()
    return render_template("admin/explanations/new.html", types=types)
