
import requests
import subprocess
import platform
import json
import random
import os
import io

from datetime import date
from pylatex import Document, Section, Subsection, Tabular
from pylatex import Math, TikZ, Axis, Plot, Figure, Matrix, Alignat
from pylatex.utils import italic
    

# Get the user's "Downloads" folder path
downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
output_path = os.path.join(downloads_folder, "report.pdf")

my_param = 181
def get_results(id):
    global my_param
    my_param = id
    return_data = dict()
    return_data["id_num"] = id
    scoreurl = "https://compete.metactf.com/"+str(id)+"/api/get_scoreboard"
    url = "https://api.metactf.com/reports/get_individuals"

    querystring = {"contest_id":id}

    payload = ""
    headers = {"Authorization": "Bearer d98838046fe0cfd34d40ba2c209dc9be"}

    scores = requests.request("GET", scoreurl, data=payload, headers=headers, params=querystring)
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    print(id)
    teamInfo = json.loads(scores.text)["scores"]
    indivInfo = json.loads(response.text)
    indivLength = len(json.loads(response.text))
    return_data["total_users"] = indivLength
    teamLength = len(json.loads(scores.text)["scores"])
    return_data["total_teams"] = teamLength

    totalSolved = 0
    for i in range(0,teamLength):
        totalSolved += teamInfo[i]["solved"]
    return_data["total_solved"] = totalSolved


    #47 total teams
    return_data["top_teams"] = []
    for i in range(0, 5): 
        return_data["top_teams"].append({"name": teamInfo[i]["name"].replace('_', '\_'), "members": {"username":[],"email":[]}})
        for n in range(0,indivLength):
            if indivInfo[n]["name"] == teamInfo[i]["name"]:
                return_data["top_teams"][i]["members"]["username"].append(indivInfo[n]["alias"].replace('_', '\_'))
                return_data["top_teams"][i]["members"]["email"].append(indivInfo[n]["email"].replace('_', '\_'))


    pos_teams = []
    indivNumbers = []
    for team in teamInfo:
        if team["team_size"] < 2 and team["total"] > 0:
            pos_teams.append(team)
    return_data["top_indiv"] = []
    pos_teams.sort(key=lambda team: team['total'], reverse=True)
    for n in range(0,indivLength):
        for i in range(0,min(len(pos_teams), 5)):
            if indivInfo[n]["name"] == pos_teams[i]["name"] and indivInfo[n]["admin"] != 1:
                return_data["top_indiv"].append((indivInfo[n]["alias"].replace('_', '_')))
                return_data["top_indiv"].append((indivInfo[n]["email"].replace('_', '_')))
                indivNumbers.append(n)                
    for i in indivNumbers:
        del indivInfo[i]    
    # Getting random users
    random_users = random.sample(indivInfo, 10)
    return_data["random_users"] = []

    # Printing random users
    for user in random_users:
        if user["admin"]==1:
            random_users = random.sample(indivInfo, 10)

    for user in random_users:
        return_data["random_users"].append(user["alias"].replace('_', '_'))
        return_data["random_users"].append(user["email"].replace('_', '_'))

    return(return_data)

def generatepdf():
    result_data = dict(get_results(my_param))
    today = date.today().strftime("%m/%d/%y")


    template = """
    \\documentclass{article}
    \\usepackage{multicol}
    \\usepackage{titling}
    \\usepackage{geometry}
    \\usepackage{listofitems}
    \\setlength{\\columnsep}{1cm}

    \\setlength{\\droptitle}{-11em} % Shifts everything up

    \\title{}
    \\author{CTF REPORT}"""

    template += '\n\\date{' + today + '}'
    template += """

    \\geometry{
    a4paper,
    total={170mm,257mm},
    left=20mm,
    top=20mm,
    }

    \\begin{document}
    \\maketitle

    % START OF TOP 5 TEAM RESULTS!!!
    \\begin{multicols}{2}
    [
    % Statistics Section
    \\section*{Statistics:} % The makes the 1 go away!
    """ + str(result_data["total_users"]) + """ users across """ + str(result_data["total_teams"]) + """ teams \\
    """+ str(result_data["total_solved"]) +""" correct submissions.
    \\section*{Top 5 Team Results:}
    ]

    \\subsection*{1st Place:}
    \\subsubsection*{""" + result_data["top_teams"][0]["name"] + """}
    """ + ' \\\\ '.join(result_data["top_teams"][0]['members']) + """
    \\subsection*{2nd Place:}
    \\subsubsection*{""" + result_data["top_teams"][1]["name"] + """}
    """ + ' \\\\ '.join(result_data["top_teams"][1]['members']) + """
    \\subsection*{3rd Place:}
    \\subsubsection*{""" + result_data["top_teams"][2]["name"] + """}
    """ + ' \\\\ '.join(result_data["top_teams"][2]['members']) + """

    \\subsection*{4th Place:}
    \\subsubsection*{""" + result_data["top_teams"][3]["name"] + """}
    """ + ' \\\\ '.join(result_data["top_teams"][3]['members']) + """
    \\subsection*{5th Place:}
    \\subsubsection*{""" + result_data["top_teams"][4]["name"] + """}
    """ + ' \\\\ '.join(result_data["top_teams"][4]['members']) + """\\end{multicols}

    % START OF TOP 5 INDIVIDUALS!!!
    \\begin{multicols}{2}
    [
    \\section*{Top 5 Individuals Results:}
    ]"""

    for i in range(len(result_data["top_indiv"])):
        place = ""
        if i==0:
            place="1st"
        elif i==1:
            place="2nd"
        elif i==2:
            place="3rd"
        else:
            place = str(i + 1) + 'th'
        template += """\\subsection*{""" + str(place) + """ Place:}
        """ + result_data["top_indiv"][0] + " - " + result_data["top_indiv"][1] + """

    \\end{multicols}

    % Custom command to process data and display in columns


    \\section*{10 Random Users for Raffle (Solved at least 1 challenge)}
    \\begin{multicols}{2}
    \\begin{itemize}
        \\item """ + result_data["random_users"][0] + ' - ' + result_data["random_users"][1] + """
        \\item """ + result_data["random_users"][2] + ' - ' + result_data["random_users"][3] + """
        \\item """ + result_data["random_users"][4] + ' - ' + result_data["random_users"][5] + """
        \\item """ + result_data["random_users"][6] + ' - ' + result_data["random_users"][7] + """
        \\item """ + result_data["random_users"][8] + ' - ' + result_data["random_users"][9] + """
        \\item """ + result_data["random_users"][10] + ' - ' + result_data["random_users"][11] + """
        \\item """ + result_data["random_users"][12] + ' - ' + result_data["random_users"][13] + """
        \\item """ + result_data["random_users"][14] + ' - ' + result_data["random_users"][15] + """
        \\item """ + result_data["random_users"][16] + ' - ' + result_data["random_users"][17] + """
        \\item """ + result_data["random_users"][18] + ' - ' + result_data["random_users"][19] + """
    \\end{itemize}
    \\end{multicols}

    \\end{document}"""

    print(template)




    # Save the rendered template as a .tex file
    with open("report.tex", "w") as file:
        file.write(template)


    # Use subprocess to call pdflatex and generate the PDF report
    # create a binary stream object
    pdf_stream = io.BytesIO()
    # run the pdflatex command and redirect the output to the stream
    subprocess.run(["pdflatex", "-output-directory", downloads_folder, "report.tex"], stdout=pdf_stream)
    # move the stream position to the beginning
    pdf_stream.seek(0)
    # return the stream object
    return pdf_stream

    # if platform.system() == "Windows":  # Windows
    #     subprocess.run(["start", "", output_path], shell=True)

    print("Report generated successfully!")