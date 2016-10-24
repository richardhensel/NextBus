#from werkzeug.contrib.fixers import ProxyFix

from flask import Flask, request, render_template, jsonify, request, redirect, url_for
from BusSql import Schedule

app = Flask(__name__)

schedule = Schedule('StaticGtfs.db')

output = [{' ':'s ','lines':[(' ',' ',' '),
(' ','Loading',' '),
(' ','d ',' ')]}]

updatedLocation = 0

@app.route('/')
def index():
    global updatedLocation

    if updatedLocation == 0: # Just Refreshed page.
        return render_template('user.html', output=output, runscript=1)
    else: # Redirected from _get_location.
        updatedLocation = 0
        return render_template('user.html', output=output, runscript=0)

@app.route('/_get_location')
def get_location():
    global output
    global updatedLocation

    lat = request.args.get('lat', 0, type=str)
    lon = request.args.get('lon', 0, type=str)

    output = schedule.output(float(lat),float(lon),n_stops=3,n_times=4)
    updatedLocation = 1

    return jsonify(redirect=url_for('index'))

# WSGI server config. 
#app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
