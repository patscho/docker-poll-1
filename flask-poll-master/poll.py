from flask import Flask, render_template, request, redirect, make_response
from flask_bootstrap import Bootstrap

import datetime

app = Flask(__name__, static_url_path='/static')
Bootstrap(app)

poll_data = {
    'subject': 'Incident Prevention',
    'question': 'How many stars would you rate Incident Prevention?',
    'fields': ['1', '2', '3', '4', '5']
}

filename = 'data.txt'


@app.route('/')
def root():
    return render_template('poll.html', data=poll_data)


def getcookie():
    name = request.cookies.get('quest4dave')
    if name:
        return True
    else:
        return False


@app.route('/poll')
def poll():

    vote = request.args.get('field')
    if not getcookie():
        out = open(filename, 'a')
        out.write(vote + '\n')
        out.close()
        resp = make_response(redirect('/thankyou'))
        resp.set_cookie('quest4dave', "banaan", expires=datetime.datetime.now()
                        + datetime.timedelta(days=30))
        return resp
    else:
        return redirect("/youalreadyvoted")


@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html', data=poll_data)


@app.route('/youalreadyvoted')
def alreadyvoted():
    return render_template('alreadyvoted.html', data=poll_data)


@app.route('/results')
def show_results():
    votes = {}
    for f in poll_data['fields']:
        votes[f] = 0

    f = open(filename, 'r')
    for line in f:
        List = line.rstrip("\n")
        List2 = List.split(",")
        vote = List2.pop()
        votes[vote] += 1
    total_score = 0
    number_of_votes = 0
    for score, times in votes.items():
        total_score += int(score) * int(times)
        number_of_votes += int(times)
    average = round((total_score / number_of_votes), 2)

    return render_template('new_results.html', data=poll_data, votes=votes,
                           average=average, number_of_votes=number_of_votes)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
