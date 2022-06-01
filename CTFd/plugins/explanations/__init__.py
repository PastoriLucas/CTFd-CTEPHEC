from flask import Blueprint ,request,render_template

from CTFd.models import (
    Explanations,
    db,
)
from CTFd.plugins import register_plugin_assets_directory
from CTFd.utils.user import get_ip


class BaseExplanation(object):
    id = None
    content = None
    templates = {}
    scripts = {}
    explanation_model = Explanations

    @classmethod
    def create(cls, request):
        """
        This method is used to process the explanation creation request.

        :param request:
        :return:
        """
        data = request.form or request.get_json()

        explanation = cls.explanation_model(**data)

        db.session.add(explanation)
        db.session.commit()

        return explanation

    @classmethod
    def read(cls, explanation):
        """
        This method is in used to access the data of a explanation in a format processable by the front end.

        :param explanation:
        :return: explanation object, data dictionary to be returned to the user
        """
        data = {
            "id": explanation.id,
            "content": explanation.content,
            "user_id": explanation.user_id,
            "explanation_id": explanation.explanation_id,
            "type_data": {
                "id": cls.id,
            },
        }
        return data

    @classmethod
    def update(cls, explanation, request):
        """
        This method is used to update the information associated with a explanation. This should be kept strictly to the
        explanation table and any child tables.

        :param explanation:
        :param request:
        :return:
        """
        data = request.form or request.get_json()
        for attr, value in data.items():
            setattr(explanation, attr, value)

        db.session.commit()
        return explanation

    @classmethod
    def delete(cls, explanation):
        """
        This method is used to delete the resources used by a explanation.

        :param explanation:
        :return:
        """
        Explanations.query.filter_by(id=explanation.id).delete()
        cls.explanation_model.query.filter_by(id=explanation.id).delete()
        db.session.commit()


class CTFdStandardExplanation(BaseExplanation):
    id = "standard"  # Unique identifier used to register explanations
    name = "standard"  # Name of a explanation type
    templates = {  # Templates used for each aspect of explanation editing & viewing
        "create": "/plugins/explanations/assets/create.html",
        "update": "/plugins/explanations/assets/update.html",
        "view": "/plugins/explanations/assets/view.html",
    }
    scripts = {  # Scripts that are loaded when a template is loaded
        "create": "/plugins/explanations/assets/create.js",
        "update": "/plugins/explanations/assets/update.js",
        "view": "/plugins/explanations/assets/view.js",
    }
    # Route at which files are accessible. This must be registered using register_plugin_assets_directory()
    route = "/plugins/explanation/assets/"
    # Blueprint used to access the static_folder directory.
    blueprint = Blueprint(
        "standard", __name__, template_folder="templates", static_folder="assets"
    )
    explanation_model = Explanations
    

def get_exp_class(class_id):
    """
    Utility function used to get the corresponding class from a class ID.

    :param class_id: String representing the class ID
    :return: Succes class
    """
    cls = EXPLANATION_CLASSES.get(class_id)
    if cls is None:
        raise KeyError
    return cls


"""
Global dictionary used to hold all the explanation Type classes used by CTFd. Insert into this dictionary to register
your explanation Type.
"""
EXPLANATION_CLASSES = {"standard": CTFdStandardExplanation}


def load(app):
    app.db.create_all()
    register_plugin_assets_directory(app, base_path="/plugins/explanations/assets/")
    ##@app.route('/admin/explanations', methods=['GET'])
    ##def view_exp():
    ##    return render_template('explanations.html')