# import os
# from parse import parseurl
# from flask import Flask, request, jsonify, abort

# app = Flask(__name__)


# @app.route('/')
# def hello():
#     return "Hello World!"

# @app.route('/test')
# def test():
#     # url2 = 'https://www.guitartabs.cc/tabs/j/john_mayer/free_fallin_tab_ver_3.html'

#     url = request.args.get('url')

#     if not url:
#         print('invalid url')
#         abort(400)
    
#     tab_dict = parseurl(url)
#     response = jsonify(tab_dict)
#     response.headers.set("Content-Type", "application/json")

#     return jsonify(tab_dict)

# if __name__ == '__main__':
#     app.run()
