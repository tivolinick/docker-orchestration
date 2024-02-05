#!/usr/bin/python3
# import main Flask class and request object
from flask import Flask, request
import json

# create the Flask app
app = Flask(__name__)

@app.route('/query-example')
def query_example():
    return request.args
    language = request.args.get('language')
    return '''<h1>The language value is: {}</h1>'''.format(language)
    # return 'Query String Example'

@app.route('/json-example',methods=['POST'])
def json_example():
    request_data = request.get_json()
    print (request_data)
    f=open('/tmp/'+ str(request_data['actionOid']),'w')
    f.write(request_data['status'])
    f.close()
    return str(request_data['actionOid']) + ' ' + request_data['status']
    return 'JSON Object Example'

# if __name__ == '__main__':
#     # run app in debug mode on port 5000
#     app.run(debug=True, port=5000)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
