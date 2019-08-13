# Fakebook.  Guitar Scraper

fakebook is a web scraper that saves guitar tablature from URLs.  The app makes using formatted guitar tablature
convenient and accesssible.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. Deployment requires a few extra configuration details.

## Prerequisites

You will need to have at least Python 3.6+ and a virtual environment manager such as virtualenv to run the server

## Installing
### Server

After you clone the repo create and activate a virtual environment.

```
  $ source env/bin/activate
```
Then install all the dependencies in your virtual environment:
```
  $ pip install -r requirements.txt
```

## Client

Make sure you have the latest version of node.js, then:
```
  $ cd client/
  $ npm install
  $ npm start
```


## Deployment

The app is configured to deploy to Heroku and use a free-tier Postgres database.
Database credentials can be set in ~/config.py or use the default environment variable 'DATABASE_URL'

## Built With

* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - HTML Parser
* [Flask](https://palletsprojects.com/p/flask/) - Python WSGI web application framework
* [React.js](https://ko.reactjs.org/) - Used for the front-end

