import os
import requests
import json
import re
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from tab import UltimateTab

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

            # Parse url and find pre tag with tablature
            soup = BeautifulSoup(html, "html.parser")
            tabs_html_content = soup.find_all('pre')
            formatted = ''.join(map(str, tabs_html_content[1].contents))

            # Parse each line of the string into object
            lines = []

            for line in formatted.split('\n'):
                if '<span' in line:
                    continue

                else: # Line contains lyrics/string
                    lines.append(line[:-2])

            # Construct tab json object
            
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
        response = jsonify({ 'msg': 'route working'})
        response.headers.set("Content-Type", "application/json")
        return response


if __name__ == '__main__':
    app.run()
