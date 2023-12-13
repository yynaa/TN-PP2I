from flask import Flask, render_template, request
import folium
import sys
from datetime import datetime

from backend.db.functions import *

app = Flask(__name__)

app.static_folder=app.root_path + app.static_url_path

@app.route('/')
def root():
    return '<h1>ULTRA MEGA SUPER WHEELCHAIR MAN SIMULATOR 2019</h1>'

@app.route('/map')
def mapLoader():
    """
    Loads the map page
    """
    return render_template("map.html")

############################################################################
# LOGIN PART

@app.route('/login', methods = ['GET', 'POST'])
def login():
    infos = request.form
    login = infos.get("login")
    mdp = infos.get("mdp")

    if request.method == 'GET':
        return render_template("welcome/index.html", is_logged=False, log_issue="")

    is_logged = check_password("backend/db/database.db", login=login, given_password=mdp)

    if is_logged[0]:
        return render_template("welcome/index.html", is_logged = is_logged[0], log_issue="")
    else:
        return render_template("welcome/index.html", is_logged = is_logged[0], log_issue=is_logged[1])

@app.route('/register', methods=['GET', 'POST'])
def register():
    infos = request.form
    mail = infos.get("mail")
    name = infos.get("name")
    mdp = infos.get("mdp")

    if request.method == 'GET':
        return render_template("welcome/register.html", is_created = False, reg_issue = "")

    is_created = create_User("backend/db/database.db", login = name, email = mail, password=mdp, display_name="", year = datetime.now().year, month = datetime.now().month, day = datetime.now().day)

    if is_created[0]:
        return render_template("welcome/register.html", is_created = is_created[0], reg_issue = "")
    else:
        return render_template("welcome/register.html", is_created = is_created[0], reg_issue = is_created[1])
    

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    infos = request.form
    login = infos.get("login")
    mdp = infos.get("mdp")

    if request.method == 'GET':
        return render_template("welcome/forgot_mail.html", is_reseting=False, password_issue="")

    is_reseting = update_password("backend/db/database.db", login=login, newPassword=mdp)

    if is_reseting[0]:
        return render_template("welcome/forgot_mail.html", is_reseting=is_reseting[0], password_issue="")
    else:
        return render_template("welcome/forgot_mail.html", is_reseting=is_reseting[0], password_issue=is_reseting[1])
    
############################
#API

@app.route('/api/buildings')
def apiBuildings():
    """
    Returns the list of buildings
    """
    return fetch_Data("backend/db/dummy.db", "Buildings")

@app.route('/api/b/<int:id>')
def apiBuilding(id):
    """
    Returns the building with the given id
    """
    return fetch_Data_buildings("backend/db/dummy.db", id)

#########################################################################

def runFlask():
    """
    Runs the flask server
    """
    app.run(host='localhost', port=8080, debug=True)
    