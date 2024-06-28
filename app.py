from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_TOKEN = '74Z7pz8ZfG3eYpPw1mEqT5gD6ydA2uM39dUV8RhD'
HEADERS = {'api_key': API_TOKEN}

LEAGUES_API = "https://api.sportradar.com/soccer/trial/v4/en/competitions.json?api_key={api_key}"
SEASONS_API = "https://api.sportradar.com/soccer/trial/v4/en/competitions/{league_id}/seasons.json?api_key={api_key}"
LEAGUE_TABLE_API = "https://api.sportradar.com/soccer/trial/v4/en/seasons/{season_id}/standings.json?api_key={api_key}"

@app.route('/')
def home():
    url = LEAGUES_API.format(api_key=API_TOKEN)
    response = requests.get(url, headers=HEADERS)
    leagues = response.json()['competitions'] if response.status_code == 200 else []
    return render_template('home.html', leagues=leagues)

#all leages list in Folder/Sportradar_coverage
# liste hameye lig ha dar PDF dakhel folder hast hatta lige daste 2 iran :)

@app.route('/select_year/<league_id>')
def select_year(league_id):
    url = SEASONS_API.format(league_id=league_id, api_key=API_TOKEN)
    response = requests.get(url, headers=HEADERS)
    data = response.json() if response.status_code == 200 else {}
    seasons = data.get('seasons', [])
    return render_template('select_year.html', league_id=league_id, seasons=seasons)


@app.route('/league_table/<season_id>')
def league_table_view(season_id):
    url = LEAGUE_TABLE_API.format(season_id=season_id, api_key=API_TOKEN)
    response = requests.get(url, headers=HEADERS)
    data = response.json()

    if response.status_code == 200:
        standings = data.get('standings', [])
        if standings and 'groups' in standings[0]:
            table = standings[0]['groups'][0].get('standings', [])
        else:
            table = []
    else:
        table = []

    return render_template('league_table.html', season_id=season_id, table=table)


if __name__ == '__main__':
    app.run(debug=True)

    #this FREE API can only send 200 requests per month per IP
    #dar il project license free API estefade shode va baraye request haye bishtar bayad license gereft
