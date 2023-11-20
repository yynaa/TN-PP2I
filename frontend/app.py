from flask import Flask, render_template, request
import folium
import sys
from datetime import datetime

from backend.db.functions import *

app = Flask(__name__)

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

@app.route('/login', methods = ['GET'])
def login():
    return render_template("welcome/index.html")

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
    return render_template("welcome/forgot_mail.html")

#########################

# THESES HTML PAGES ARE NOT PERMANENT, JUST HERE TO CHECK IF THE DB AND 
# THE FRONT END STRUCTURE ARE WORKING

@app.route('/post_login', methods=['POST'])
def postlog():
    "<p>Cond of connection will be implemented asap</p>"

############################

#########################################################################

#if __name__ == '__main__':
    