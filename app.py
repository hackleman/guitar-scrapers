import os
import requests
import json
import re
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *

@app.route('/', methods = ['GET', 'POST'])
def index():

    if request.method == 'POST':
        try:
            url = request.args.get('url')
            r = requests.get(url)
        except:
            error = {'error': 'Invalid URL'}
            response = jsonify(error)
            response.headers.set("Content-Type", "application/json")
            return response
        
        if r:
            html = r.content

            # Parse url and find pre tag with tabs
            soup = BeautifulSoup(html, "html.parser")
            tabs_html_content = soup.find_all('pre')
            formatted = ''.join(map(str, tabs_html_content[1].contents))

            # Parse each line into object
            lines = []

            for line in formatted.split('\n'):
                if '<span' in line:
                    continue

                else:
                    lines.append(line[:-2])

            # Construct tab
            tab = {}
            tab['lines'] = lines
            response = jsonify(tab)
            try:
                result = Result(
                    url = url,
                    result_all = tab
                )
                db.session.add(result)
                db.session.commit()
            except:
                response = jsonify({'error': 'Unable to add items to DB'})
                response.headers.set("Content-Type", "application/json")
                return response

            response.headers.set("Content-Type", "application/json")
            return response

        response = jsonify({'error': 'timeout'})
        response.headers.set("Content-Type", "application/json")
        return response

    if request.method == 'GET':
        try:
            url = request.args.get('url')
            try:
                tab = Result.query.filter_by(url = url).first()
                return jsonify(tab.result_all)
            except:
                return jsonify({'error': 'DB find failure'})
        except:
            return jsonify({'error': 'Invalid URL'})

        return jsonify({ 'msg': 'route working'})

if __name__ == '__main__':
    app.run()
