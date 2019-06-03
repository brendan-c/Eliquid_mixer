from app_setup import app
from flask import abort, request, jsonify
# from bson.json_util import dumps
from json import dumps
from models import User
import datalayer as dl
import sys
import flask_praetorian

guard = flask_praetorian.Praetorian()
guard.init_app(app, User)


def consoleprint(message):
    print(message, file=sys.stderr)


@app.route('/', methods=['GET'])
def root():
    return dumps('Server active')


@app.route('/recipes', methods=['GET'])
def recipes():
    recipes = dl.list_recipes()
    consoleprint(recipes)
    return dumps(recipes)

@app.route('/my_recipes', methods=['GET'])
@flask_praetorian.auth_required
def my_recipes():
    consoleprint('my recipes')
    user = flask_praetorian.current_user()
    # # implement this method
    recipes = dl.list_user_recipes(user)
    consoleprint(recipes)
    return dumps(recipes)
    # return dumps('Hello')

@app.route('/recipes/name/<string:name>', methods=['GET', 'POST'])
@flask_praetorian.auth_required
def recipe_by_name(name):
    consoleprint('AHH')
    if request.method == 'POST':
        consoleprint('save recipe request')
        consoleprint(request.get_json())
        recipe = request.get_json()
        user = flask_praetorian.current_user()
        consoleprint(user.id)
        dl.insert_recipe(recipe, user)
        return("OK")

    if request.method == 'GET':
        recipe = dl.recipe_by_name(name)
        if recipe:
            recipe_dict = dl.dictify_recipe(recipe)
            return dumps(recipe_dict)
        else:
            abort(404)


@app.route('/recipes/id/<int:recipe_id>')
def recipe_by_id(recipe_id):
    consoleprint(recipe_id)
    recipe = dl.recipe_by_id(recipe_id)
    if recipe:
        recipe_dict = dl.dictify_recipe(recipe)
        return dumps(recipe_dict)
    else:
        abort(404)


# ------------AUTHENTICATION-----------------
# tested and works
@app.route('/users/create_user', methods=['POST'])
def create_user():
    """
    Creates a user
    """
    consoleprint('CREATE USER')
    req = request.get_json(force=True)
    consoleprint(req)
    username = req.get('username', None)
    password = req.get('password', None)
    encrypted_password = guard.encrypt_password(password)
    try:
        user = dl.create_user(username, encrypted_password)
        ret = {'access_token': guard.encode_jwt_token(user)}
        return (jsonify(ret), 200)
    except:
        ret = {'error': 'AuthenticationError',
                'message': 'User already exists',
                'status_code': 409}
        return (jsonify(ret), 409)


# ------------AUTHENTICATION EXAMPLES-----------------

# Set up some routes for the example


@app.route('/users/login', methods=['POST'])
def login():
    """
    Logs a user in by parsing a POST request containing user credentials and
    issuing a JWT token.

    .. example::
       $ curl http://localhost:5000/login -X POST \
         -d '{"username":"Walter","password":"calmerthanyouare"}'
    """
    req = request.get_json(force=True)
    username = req.get('username', None)
    password = req.get('password', None)

    user = guard.authenticate(username, password)
    consoleprint(user)
    ret = {'access_token': guard.encode_jwt_token(user)}
    return (jsonify(ret), 200)


@app.route('/protected')
@flask_praetorian.auth_required
def protected():
    """
    A protected endpoint. The auth_required decorator will require a header
    containing a valid JWT

    .. example::
       $ curl http://localhost:5000/protected -X GET \
         -H "Authorization: Bearer <your_token>"
    """
    return jsonify(message='protected endpoint (allowed user {})'.format(
        flask_praetorian.current_user().username,
    ))


@app.route('/protected_admin_required')
@flask_praetorian.roles_required('admin')
def protected_admin_required():
    """
    A protected endpoint that requires a role. The roles_required decorator
    will require that the supplied JWT includes the required roles

    .. example::
       $ curl http://localhost:5000/protected_admin_required -X GET \
          -H "Authorization: Bearer <your_token>"
    """
    return jsonify(
        message='protected_admin_required endpoint (allowed user {})'.format(
            flask_praetorian.current_user().username,
        )
    )


@app.route('/protected_operator_accepted')
@flask_praetorian.roles_accepted('operator', 'admin')
def protected_operator_accepted():
    """
    A protected endpoint that accepts any of the listed roles. The
    roles_accepted decorator will require that the supplied JWT includes at
    least one of th accepted roles

    .. example::
       $ curl http://localhost/protected_operator_accepted -X GET \
         -H "Authorization: Bearer <your_token>"
    """
    return jsonify(
        message='protected_operator_accepted endpoint (allowed usr {})'.format(
            flask_praetorian.current_user().username,
        )
    )


app.run()
