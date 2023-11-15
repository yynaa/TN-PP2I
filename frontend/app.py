from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def root():
    return '<h1>ULTRA MEGA SUPER WHEELCHAIR MAN SIMULATOR 2019</h1>'

@app.route('/map')
def mapLoader():
    """
    Loads the map page
    """
    return render_template('map.html')

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)