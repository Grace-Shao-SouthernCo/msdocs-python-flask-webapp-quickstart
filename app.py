import os
import json
from flask_cors import CORS


from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for, jsonify)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

from fetch_articles import get_article_links
from summarize_articles import summarize_article

@app.route('/')
def index():
    return render_template('index.html')
    articles = get_articles()
    return render_template('articleCard.html', articles=articles)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
#    name = request.form.get('name')

#    if name:
    #print('Request for hello page received with name=%s' % name)
#    else:
#        print('Request for hello page received with no name or blank name -- redirecting')
#        return redirect(url_for('index'))
    return 'Hello, World!'

@app.route('/api/articles', methods=['GET'])
def get_articles():
    try:
        query = "what is new with generative ai this week"
        num_articles = 5
        article_links = get_article_links(query, num_articles)
        print(article_links)
        return jsonify(article_links)
    except Exception as e:
        print(e)
        return jsonify({"error": "An error occurred while fetching articles"}), 500
    
@app.route('/api/summarize', methods=['GET'])
def get_summary():
    try:
        url = request.args.get('url', default = "", type = str)
        summary = summarize_article(url)
        return jsonify(summary)
    except Exception as e:
        print(e)
        return jsonify({"error": "An error occurred while summarizing the article"}), 500

if __name__ == '__main__':
    app.run()
