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

@app.route('/welcome', methods=['GET'])
def welcome():
    return render_template('welcome/welcome.html', is_logged=session.get('is_logged'))

@app.route("/profile", methods=['GET', 'POST'])
def profile():
    is_co = session['is_logged']

    if is_co:
        decoded = jwt.decode(session['token'], app.config['SECRET_KEY'], algorithms='HS256')
        datas = fetch_Data_user("backend/db/database.db", decoded['login'])
        
        if request.method == 'GET':
            return render_template('welcome/profile.html', is_logged=is_co, login=datas['login'], mail=datas['email'], password=datas['password'], creation_date=datas['creation_date'], username=datas['display_name'], modif = "", mail_good = "", mail_issue = "", login_good = "", login_issue = "", user_good = "", user_issue = "")
        else:
            form = request.form

            if 'mail' in form:
                new_mail = form.get('mail')
                switch = update_mail('backend/db/database.db', datas['login'], new_mail)

                if switch[0]:
                    decoded['email'] = new_mail
                    datas = fetch_Data_user("backend/db/database.db", decoded['login'])
                    session['token'] = jwt.encode(decoded, app.config['SECRET_KEY'])

                    return render_template('welcome/profile.html', is_logged=is_co, login=datas['login'], mail=datas['email'], password=datas['password'], creation_date=datas['creation_date'], username=datas['display_name'], modif = "", mail_good = switch[0], mail_issue = "", login_good = "", login_issue = "", user_good = "", user_issue = "")
                else:
                    return render_template('welcome/profile.html', is_logged=is_co, login=datas['login'], mail=datas['email'], password=datas['password'], creation_date=datas['creation_date'], username=datas['display_name'], modif = "", mail_good = switch[0], mail_issue = switch[1], login_good = "", login_issue = "", user_good = "", user_issue = "")
            
            if 'login' in form:
                new_login = form.get('login')
                switch = update_login('backend/db/database.db', datas['login'], new_login)

                if switch[0]:
                    decoded['login'] = new_login
                    datas = fetch_Data_user("backend/db/database.db", decoded['login'])
                    session['token'] = jwt.encode(decoded, app.config['SECRET_KEY'])

                    return render_template('welcome/profile.html', is_logged=is_co, login=datas['login'], mail=datas['email'], password=datas['password'], creation_date=datas['creation_date'], username=datas['display_name'], modif = "", mail_good = "", mail_issue = "", login_good = switch[0], login_issue = "", user_good = "", user_issue = "")
                else:
                    return render_template('welcome/profile.html', is_logged=is_co, login=datas['login'], mail=datas['email'], password=datas['password'], creation_date=datas['creation_date'], username=datas['display_name'], modif = "", mail_good = "", mail_issue = "", login_good = switch[0], login_issue = switch[1], user_good = "", user_issue = "")
            
            if 'user' in form:
                new_user = form.get('user')
                switch = update_display_name('backend/db/database.db', datas['login'], new_user)

                if switch[0]:
                    decoded['display_name'] = new_user
                    datas = fetch_Data_user("backend/db/database.db", decoded['login'])
                    session['token'] = jwt.encode(decoded, app.config['SECRET_KEY'])

                    return render_template('welcome/profile.html', is_logged=is_co, login=datas['login'], mail=datas['email'], password=datas['password'], creation_date=datas['creation_date'], username=datas['display_name'], modif = "", mail_good = "", mail_issue = "", login_good = "", login_issue = "", user_good = switch[0], user_issue = "")
                else:
                    return render_template('welcome/profile.html', is_logged=is_co, login=datas['login'], mail=datas['email'], password=datas['password'], creation_date=datas['creation_date'], username=datas['display_name'], modif = "", mail_good = "", mail_issue = "", login_good = "", login_issue = "", user_good = switch[0], user_issue = switch[1])
            


                

    else:
        return render_template('welcome/profile.html', is_logged=is_co, login="", mail="", password="", creation_date="", username="", modif = "")

@app.route("/profile/<string:modif>", methods=['GET'])
def profile_with_modif(modif: str):
    is_co = session['is_logged']

    if is_co:
        decoded = jwt.decode(session['token'], app.config['SECRET_KEY'], algorithms='HS256')
        datas = fetch_Data_user("backend/db/database.db", decoded['login'])

        return render_template('welcome/profile.html', is_logged=is_co, login=datas['login'], mail=datas['email'], password=datas['password'], creation_date=datas['creation_date'], username=datas['display_name'], modif = modif)
    else:
        return render_template('welcome/profile.html', is_logged=is_co, login="", mail="", password="", creation_date="", username="", modif = modif)

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
    if session['is_logged']:
        if request.method == 'GET':
            return render_template("welcome/forgot_mail.html", is_reseting=False, password_issue="")
        else:
            infos = request.form
            decoded = jwt.decode(session['token'], app.config['SECRET_KEY'], algorithms='HS256')
            login = decoded['login']
            mdp = generate_password_hash(infos.get("mdp"))

            is_reseting = update_password("backend/db/database.db", login=login, newPassword=mdp)

            if is_reseting[0]:
                decoded['password'] = mdp
                session['token'] = jwt.encode(decoded, app.config['SECRET_KEY'])

                return render_template("welcome/forgot_mail.html", is_reseting=is_reseting[0], password_issue="")
            else:
                return render_template("welcome/forgot_mail.html", is_reseting=is_reseting[0], password_issue=is_reseting[1])
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

@app.route('/disconnect', methods=['GET'])
def disconnect():
    session['is_logged'] = False
    session.pop('token', None)

    return redirect(url_for('welcome'))


#########################################################################

def runFlask():
    """
    Runs the flask server
    """
    app.run(host='localhost', port=8080, debug=True)
    