from flask import Flask, render_template, json, request,redirect,session,jsonify, url_for,abort
from Gaa_analyticsDAO import Gaa_analyticsDAO # take the Gaa_analytics DAO/ read in
from flask_cors import CORS
import decimal
import flask.json
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__, static_url_path='', static_folder='.')
class MyJSONEncoder(flask.json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        return super(MyJSONEncoder, self).default(obj)


app.json_encoder = MyJSONEncoder
#app = Flask(__name__)
# Define the percentile keys that will be used later on (list of strings)
percentile_keys = ["Min", "Mean","Max"]
@app.route('/')
def main():

    return render_template('index.html')
CORS(app)

@app.route('/showSignUp')

def showSignUp():

    return render_template('signup.html')
    
@app.route('/showSignin')

def showSignin():

    if session.get('user'):

        return render_template('userHome.html')

    else:

        return render_template('signin.html')

@app.route('/validateLogin',methods=['POST'])

def validateLogin():

    try:

            return render_template('userHome.html')
    except Exception as e:

        return render_template('error.html',error = str(e))

@app.route('/userHome')

def userHome():
        return render_template('userHome.html')
@app.route("/counties")
def counties():
    # Run a query to find all unique counties and return a list of those counties
    counties =Gaa_analyticsDAO.getAllViz()
    county_list = counties[1].unique()    
    return jsonify(county_list.tolist())

@app.route("/scoresummary/<county>")
def scoresummary(county):
    score_data = Gaa_analyticsDAO.getAllViz()
    # Ensure county column is equal to the chosen county (in the path)
    score_data_grouped = score_data.loc[(score_data[1]== county),:]
    # Calculate min, mean, and max
    min_score = score_data_grouped[21].min()
   
    mean_score = round(score_data_grouped[21].mean(),2)
    max_score = score_data_grouped[21].max()
    summary_scores = [min_score,mean_score,max_score]
    summary_scores_dictionary = dict(zip(percentile_keys,summary_scores))
    # Put the resulting dictionary into JSON format and return it
    return jsonify(summary_scores_dictionary)
    
# Define the route to "/scoreslist/<county>"
@app.route("/scoreslist/<county>")
def scoreslist(county):
    data_4 = Gaa_analyticsDAO.getAllViz()
    # Ensure county column is equal to the chosen county (in the path)
    data_grouped_4 = data_4.loc[(data_4[1] == county),:]
    return jsonify(data_grouped_4.to_dict())


@app.route('/dashboard')

def dashboard():
        plots=[]
        plots.append(make_plot())
        return render_template('dashboard.html', plots=plots)

def make_plot():
    data_4 = Gaa_analyticsDAO.getAllViz()
    x = data_4[1]
    y = data_4[21]
    
    a=plt.hist(x, y)
    #fig, ax =plt.subplots()
    #x.plot.bar()
    return plt.savefig('C:/Users/Diarmuid/Documents/GMIT_DATA_ANALYTICS/Data_Representation/BigProjectDataRepG00364693-master/BigProjectDataRepG00364693/images/team_plot.png')

@app.route('/logout')
def logout():

    session.pop('user',None)

    return redirect('/')

@app.route('/matches')
def getAll():
    results = Gaa_analyticsDAO.getAll()
    return jsonify(results)
    
@app.route('/matches_info')
def match_info():
    return render_template('match_info.html')

    


@app.route('/matches/<int:game_id>')
def findById(game_id):
    #print(game_id)
    foundMatch = Gaa_analyticsDAO.findByID(game_id)
    return jsonify(foundMatch)
    #return render_template('match_info.html')

@app.route('/matches', methods=['POST'])
def create():
    
    if not request.json:
        abort(400)
    match = {
        "game_id": request.json['game_id'],
        "team": request.json['team'],
        "team_name": request.json['team_name'],
        "venue": request.json['venue'],
         "date": request.json['date'],
        "competition": request.json['competition'],
        "round": request.json['round'],
        "player": request.json['player'],
        "player_name": request.json['player_name']
    }
    values =(
        match['game_id'],
        match['team'],
        match['team_name'], 
        match['venue'], 
        match['date'],
        match['competition'],
        match[ 'round'],
        match[ 'player'],
        match['player_name']
        
    )
    Gaa_analyticsDAO.create(values)
    return jsonify(match)

@app.route('/matches/<int:id>', methods=['PUT'])
def update(id):
    foundMatch = Gaa_analyticsDAO.findByID(id)
    if not foundMatch:
        abort(404)
    
    if not request.json:
        abort(400)
    reqJson = request.json

    if 'game_id' in reqJson and type(reqJson['game_id']) is not int:
        abort(400)
		
    if 'team' in reqJson:
	    foundMatch['team'] = reqJson['team']
	
    if 'team_name' in reqJson:
        foundMatch['team_name'] = reqJson['team_name']
	
    if 'venue' in reqJson:
        foundMatch['venue'] = reqJson['venue']
		
    if 'date' in reqJson:
        foundMatch['date'] = reqJson['date']
		
	
    values = (foundMatch['game_id'],foundMatch['team'],foundMatch['team_name'],foundMatch['venue'],foundJob['date'])
    Gaa_analyticsDAO.update(values)
    return jsonify(foundMatch)
        

@app.route('/matches/<int:id>' , methods=['DELETE'])
def delete(id):
    Gaa_analyticsDAO.delete(id)
    return jsonify({"done":True})
	

if __name__ == '__main__' :
    app.run(debug= True)