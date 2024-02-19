#!/usr/local/bin/python
# import main Flask class and request object
from flask import Flask, request

# create the Flask app
app = Flask(__name__)

@app.route('/status',methods=['POST'])
def json_example():
    request_data = request.get_json()
    print (request_data)
    print ('\n')
    return str(request_data) + '\n'

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
