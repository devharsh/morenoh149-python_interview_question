from flask import Flask, escape, request, render_template
import urllib.request, urllib.parse, urllib.error
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/read')
def read_favorites():
    """Read out favorited movies."""
    filename = os.path.join('data.json')
    with open(filename) as data_file:
        data = json.load(data_file)
        return data

@app.route('/write')
def write_favorites():
    """if query params are passed, write movie to json file."""
    return render_template('favorites.html')

@app.route('/search', methods=['POST'])
def search():
    """if POST, query movie api for data and return results."""
    try:
        query = request.form['title']
        print(query)
        query = query.replace(' ', '+')
        print(query)
        #http://www.omdbapi.com/?t=star+wars&apikey=342a0c0a
        url = 'http://www.omdbapi.com/?t=' + query + '&apikey=342a0c0a'
        print('Retrieving the data of ' + query + ' now... ')
        uh = urllib.request.urlopen(url)
        data = uh.read()
        json_data=json.loads(data)
        
        if json_data['Response']=='True':
            return json_data
        else:
            return 'Error encountered: '
    
    except urllib.error.URLError as e:
        print('ERROR: {e.reason}')

@app.route('/movie/<movie_oid>')
def movie_detail():
    """if fetch data from movie database by oid and display info."""
    qs_name = request.args.get('name', '')
    qs_oid = request.args.get('oid', '')
    return f'Hello, {escape(name)}!'

@app.errorhandler(404)
def page_not_found_error(error):
    """Render a personalized template for 404 status code.
        Flask look for templates on 'templates' directory.
    """
    return render_template('not_found.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
