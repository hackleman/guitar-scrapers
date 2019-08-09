import os
import requests
import json
import re

from flask import Flask, render_template, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from parseurl import tab_from_url

app = Flask(__name__)
CORS(app)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *

@app.route('/', methods = ['GET', 'POST'])
def index():
    # CREATE new Tab from artist, title, url
    if request.method == 'POST':
        try:
            url = request.args.get('url')
            r = requests.get(url)
        except:
            return jsonify({'error': 'Invalid URL'})
        
        if r:
            tab = tab_from_url(r)

            try:
                # check if the tab already exists
                if bool(db.session.query(Tab.url).filter_by(url=url).first()):
                    return jsonify({'error': 'item already exists in DB'})

                newTab = Tab(
                    artist = request.args.get('artist'),
                    title = request.args.get('title'),
                    url = url,
                    lines = tab
                )
                db.session.add(newTab)
                db.session.commit()
            except:
                return jsonify({'error': 'Unable to POST to DB'})

            return jsonify({'tab': tab, 'msg': 'TAB CREATED'})

        return jsonify({'error': 'timeout'})

    # Get all Tabs from DB
    if request.method == 'GET':

        try:
            data = []
            tabs = db.session.query(Tab).all()
            for tab in tabs:
                item = {}
                item['artist'] = tab.artist
                item['url'] = tab.url
                item['title'] = tab.title
                data.append(item)
            return jsonify({'data': data})

        except:
            return jsonify({'error': 'DB find failure'})


@app.route('/artist/', methods = ['GET'])
def findByArtist():
    artist = request.args.get('artist')
    if artist is None:
        return jsonify({"error": "No artist specified"})

    try:
        data = []
        tabs = db.session.query(Tab).filter_by(artist=artist).all()
        for tab in tabs:
            item = {}
            item['artist'] = tab.artist
            item['url'] = tab.url
            item['title'] = tab.title
            data.append(item)
        return jsonify({'data': data})

    except:
        return jsonify({'error': 'DB find failure'})


@app.route('/title/', methods = ['GET'])
def findByTitle():
    title = request.args.get('title')
    if title is None:
        return jsonify({"error": "No title specified"})

    try:
        data = []
        tabs = db.session.query(Tab).filter_by(title=title).all()
        for tab in tabs:
            item = {}
            item['artist'] = tab.artist
            item['url'] = tab.url
            item['title'] = tab.title
            data.append(item)
        return jsonify({'data': data})

    except:
        return jsonify({'error': 'DB find failure'})

@app.route('/url/', methods = ['GET', 'DELETE'])
def findByURL():
    if request.method == 'GET':
        url = request.args.get('url')
        if url is None:
            return jsonify({"error": "No url specified"})
        try:
            tabs = db.session.query(Tab).filter_by(url=url).first()
            return jsonify(tabs.lines)
        except:
            return jsonify({'error': 'DB find failure'})

    if request.method == 'DELETE':
        try:
            url = request.args.get('url')
            if url is None:
                return jsonify({'msg': 'invalid URL'})

            item = db.session.query(Tab).filter_by(url=url).first()
            if item is None:
                return jsonify({'msg': 'URL NOT FOUND'})
            
            db.session.delete(item)
            db.session.commit()
            return jsonify({'msg': 'Item DELETED'})

        except:
            return jsonify({'msg': 'DELETE FAILED'})

        return jsonify({'msg': 'DELETE URL'})


@app.route('/test/', methods = ['GET', 'DELETE'])
def test():

    return jsonify({ 'msg': 'test working'})

        
    


if __name__ == '__main__':
    app.run()
