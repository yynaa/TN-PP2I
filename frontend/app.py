from flask import Flask, render_template, request, session,redirect, url_for
import folium
import sys
from datetime import datetime, timedelta
import jwt
from werkzeug.security import generate_password_hash

from backend.db.functions import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'af6f328e28ed48fb89ee914c1acd9b4c'
app.permanent_session_lifetime = timedelta(weeks=1)

@app.route('/')
def root():
    return '<h1>ULTRA MEGA SUPER WHEELCHAIR MAN SIMULATOR 2019</h1>'

@app.route('/map')
def mapLoader():
    """
    Loads the map page
    """
    m = folium.Map(location=[48.689, 6.2], zoom_start=13)

    for building in fetch_Data("backend/db/database.db", "Buildings"):
        folium.Marker(
            location=[building["GPS_lat"], building["GPS_long"]],
            popup=building["building_name"],
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)

    return m.get_root().render()

    for building in fetch_Data("backend/db/database.db", "Buildings"):
        folium.Marker(
            location=[building["GPS_lat"], building["GPS_long"]],
            popup=building["building_name"],
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)

    return m.get_root().render()

def getMapData():
    """
    Returns the map data
    """
    # this is test data
    return []

############################################################################
# LOGIN PART

@app.route('/welcome')
def welcome():
    return render_template('welcome/welcome.html')

def check_connexion():
    if session.get('is_logged'):
        return redirect('/welcome')


@app.route('/login', methods = ['GET', 'POST'])
def login():
    red = check_connexion()
    if red:
        return red

    if request.method == 'GET':
        return render_template("welcome/index.html", is_logged=False, log_issue="")

    infos = request.form
    login = infos.get("login")
    mdp = infos.get("mdp")

    is_logged = check_password("backend/db/database.db", login=login, given_password=mdp)

    if is_logged[0]:
        session.permanent = True

        session['is_logged'] = True
        datas = fetch_Data_user('backend/db/database.db', login)
        token = jwt.encode({
            'login': datas['login'],
            'email': datas['email'],
            'display_name': datas['display_name']
        }, app.config['SECRET_KEY'])
        session['token'] = token

        return render_template("welcome/index.html", is_logged = is_logged[0], log_issue="")
    else:
        return render_template("welcome/index.html", is_logged = is_logged[0], log_issue=is_logged[1])

@app.route('/register', methods=['GET', 'POST'])
def register():
    red = check_connexion()
    if red:
        return red

    if request.method == 'GET':
        return render_template("welcome/register.html", is_created = False, reg_issue = "")

    infos = request.form
    mail = infos.get("mail")
    name = infos.get("name")
    mdp = generate_password_hash(infos.get("mdp"))

    y = datetime.now().year
    m = datetime.now().month
    d = datetime.now().day

    is_created = create_User("backend/db/database.db", login = name, email = mail, password=mdp, display_name="", year = y, month = m, day = d)

    if is_created[0]:
        session.permanent = True

        session['is_logged'] = True
        token = jwt.encode({
            'login': name,
            'email': mail,
            'display_name': ""
        }, app.config['SECRET_KEY'])
        session['token'] = token

        return render_template("welcome/register.html", is_created = is_created[0], reg_issue = "")
    else:
        return render_template("welcome/register.html", is_created = is_created[0], reg_issue = is_created[1])
    

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    red = check_connexion()
    if red:
        return red

    if request.method == 'GET':
        return render_template("welcome/forgot_mail.html", is_reseting=False, password_issue="")

    infos = request.form
    login = infos.get("login")
    mdp = generate_password_hash(infos.get("mdp"))

    is_reseting = update_password("backend/db/database.db", login=login, newPassword=mdp)

    if is_reseting[0]:
        return render_template("welcome/forgot_mail.html", is_reseting=is_reseting[0], password_issue="")
    else:
        return render_template("welcome/forgot_mail.html", is_reseting=is_reseting[0], password_issue=is_reseting[1])

@app.route('/disconnect', methods=['GET'])
def disconnect():
    session.pop('is_logged', None)
    session.pop('token', None)

    return redirect(url_for('welcome'))


#########################################################################

#if __name__ == '__main__':
    