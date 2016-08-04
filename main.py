from flask import Flask, request, render_template, jsonify, request
from busstops import Schedule
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', output=defaultOutput)

@app.route('/user/<GPS>')
def user(GPS):
    output = schedule.output(*GPS.split(','),n_stops=3,n_times=4)
    return render_template('user.html', output=output)


if __name__ == "__main__":
    schedule = Schedule()

    defaultOutput = [{' ':' ','lines':[(' ',' ',' '),
    (' ','Loading',' '),
    (' ',' ',' ')]}]

    app.run(debug=False)
