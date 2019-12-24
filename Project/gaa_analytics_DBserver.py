from flask import Flask, render_template, json, request,redirect,session,jsonify, url_for,abort
from Gaa_analyticsDAO import Gaa_analyticsDAO # take the Gaa_analytics DAO/ read in
from flask_cors import CORS
import pandas as pd
from json import JSONEncoder
app = Flask(__name__, static_url_path='', static_folder='.')

#app = Flask(__name__)

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



@app.route('/dashboard')

def dashboard():
        return render_template('dashboard.html')

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

# Create works:
@app.route('/matches', methods=['POST'])
def create():
    
    if not request.json:
        abort(400)
    # other checking 
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

# Update works:
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
	
    if 'competition' in reqJson:
        foundMatch['competition'] = reqJson['competition']

    if 'round' in reqJson:
        foundMatch['round'] = reqJson['round']

    if 'player' in reqJson:
        foundMatch['player'] = reqJson['player']

    if 'player_name' in reqJson:
        foundMatch['player_name'] = reqJson['player_name'] 
   	
	
    values = (foundMatch['game_id'],foundMatch['team_name'],foundMatch['venue'],foundMatch['date'],foundMatch['competition'],foundMatch['round'],foundMatch['player'],foundMatch['player_name'])
    Gaa_analyticsDAO.update(values)
    return jsonify(foundMatch)
        

# Delete works
@app.route('/matches/<int:id>' , methods=['DELETE'])
def delete(id):
    Gaa_analyticsDAO.delete(id)
    return jsonify({"done":True})
	

if __name__ == '__main__' :
    app.run(debug= True)