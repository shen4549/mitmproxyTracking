from flask import Flask,request
import json
import time
import ast
from queue_subscribe import QueueSuscriber
from helper import Helper
app = Flask(__name__)
message_list=[]

def setMessgae(body):
    global message_list
    print('set msg')
    message_list=body


@app.route('/view')
def view():
    QueueSuscriber(setMessgae)
    print(request.args, len(request.args))
    filters=request.args
    if len(request.args) ==0 :
        return json.dumps(message_list)
    else:
        helper = Helper()
        print(type(filters.items()))
        return json.dumps(helper.filter_items(message_list,filters.items()))

@app.route('/view/matching')
def view_matching():
    QueueSuscriber(setMessgae)
    filters=request.args
    if len(request.args) ==0 or message_list is None:
        return json.dumps(message_list)
    else:
        helper = Helper()
        print(type(filters.items()))
        return json.dumps(helper.filter_items_if_all_filters_match(message_list,filters.items()))

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'
    
if __name__ == "__main__":
    print('Starting server...')
    app.run(debug=True)





