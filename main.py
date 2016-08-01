from flask import Flask, request, render_template
from busstops import Schedule
app = Flask(__name__)

output = [{' ':' ','lines':[(' ',' ',' '),
(' ','Loading',' '),
(' ',' ',' ')]}]

# run app first the end

@app.route('/')
def index():
    return render_template('index.html', output=output)

@app.route('/user/<GPS>')
def user(GPS):
    output = schedule.output(*GPS.split(','),n_stops=3,n_times=4)
    return render_template('user.html', output=output)

schedule = Schedule()
#output = schedule.output(-27.4990795,153.0146127,n_stops=1,n_times=3)

if __name__ == "__main__":
    app.run(debug=False)
