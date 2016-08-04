from flask import Flask, request, render_template, jsonify, request
from busstops import Schedule
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', output=defaultOutput)


@app.route('/_get_location')
def get_location():
    print "message received"
    lat = request.args.get('lat', 0, type=str)
    lon = request.args.get('lon', 0, type=str)
    print "Ajax Received"
    output = schedule.output(lat,lon,n_stops=3,n_times=4)
    return render_template('user.html', output=output)



if __name__ == "__main__":
    schedule = Schedule()

    defaultOutput = [{' ':' ','lines':[(' ',' ',' '),
    (' ','Loading',' '),
    (' ',' ',' ')]}]

    app.run(debug=False)
