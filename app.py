from flask import Flask, escape, request, render_template
import urllib.request, urllib.parse, urllib.error
import json
import os.path

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favorites')
def read_favorites():
    with open('data.json', 'r+', encoding='utf-8') as data_file:
        data = json.load(data_file)
        return data

@app.route('/write')
def write_favorites():
    save_in_database(json_data)
    return render_template('favorites.html')

def save_in_database(json_data):
    if os.path.isfile('data.json'):
        with open('data.json') as f:
            data = json.load(f)
        data.update(json_data)
        with open('data.json', 'w+') as f:
            json.dump(data, f)
    else:
        with open('data.json', 'w+') as f:
            json.dump(json_data, f)

@app.route('/search', methods=['POST'])
def search():
    try:
        query = request.form['title']
        query = query.replace(' ', '+')
        url = 'http://www.omdbapi.com/?t=' + query + '&apikey=342a0c0a'
        uh = urllib.request.urlopen(url)
        data = uh.read()
        json_data=json.loads(data)
        
        if json_data['Response']=='True':
            save_in_database(json_data)
            return json_data
        else:
            return 'Error encountered: '
    
    except urllib.error.URLError as e:
        print('ERROR: {e.reason}')

@app.route('/movie/<movie_oid>')
def movie_detail():
    qs_name = request.args.get('name', '')
    qs_oid = request.args.get('oid', '')
    return f'Hello, {escape(name)}!'

@app.errorhandler(404)
def page_not_found_error(error):
    return render_template('not_found.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
