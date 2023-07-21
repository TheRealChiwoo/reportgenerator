from flask import Flask, request
from flask import render_template
from flask import request
from flask import jsonify
from flask_cors import CORS
from flask import send_file
from reportgenerator import *

app = Flask(__name__, template_folder='./')

<<<<<<< HEAD
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response
app.after_request(add_cors_headers)

@app.route('/get_report', methods=["POST", "GET"])
def get_report():
    formNumber = request.form["number"]
    number = int(formNumber)
    report_data = dict(get_results(number))
    generatepdf()
    return report_data
=======
@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        contest_id = request.args.get('contest_id')
        id = int(contest_id)
    except ValueError:
        raise Exception("contest_id must be a number")
    report_data = dict(get_results(id))
    top_info = {
        "total_users" : report_data["total_users"],
        "total_teams" : report_data["total_teams"],
        "total_solved" : report_data["total_solved"]
    }
    
    top_teams = report_data["top_teams"]
    top_indiv = report_data["top_indiv"]
    random_users = report_data["random_users"]
    print(top_teams)
>>>>>>> 69e6ec499ffa2d72233f854d09642c2e6eca3435


    return render_template("index.html", top_info=top_info, top_teams = top_teams, top_indiv = top_indiv, random_users = random_users, id=id)
app.run(debug=True,host="0.0.0.0")
