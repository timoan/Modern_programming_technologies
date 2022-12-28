#!/usr/bin/env python3

import json

#getting tasks from .json file
with open("data.json", "r") as data:
	tasks = json.load(data)
print("Starting data:")
print(tasks)

from flask import Flask, flash, redirect, render_template, request, session, abort, Response

app = Flask(__name__)

#main page
@app.route("/")
def index():
	return "<h1>It's server for determining whether a number is prime.</h1>"

#page with task infotmation table
@app.route("/table/")
def show_table():
	return render_template('table.html',taskslist=tasks)

#page for getting task
@app.route('/gettask/', methods=['GET'])
def get_task():
	answer = None
	for t in range(len(tasks)):
		if (tasks[t]["status"] == "TODO") and (tasks[t]["result"] == None):
			answer = tasks[t]
			tasks[t]["status"] = "DOING"
			break
	json_response=json.dumps(answer)
	response=Response(json_response,content_type='application/json; charset=utf-8')
	response.headers.add('content-length',len(json_response))
	response.status_code=200
	return response

#page for sending results
@app.route('/sendanswer/', methods = ['POST'])
def send_answer():
	req_data = request.json
	print(req_data)
	for t in range(len(tasks)):
		if tasks[t]["taskID"] == req_data["taskID"]:
			tasks[t]["status"] = "DONE"
			tasks[t]["time"] = req_data["time"]
			tasks[t]["result"] = req_data["result"]
	answer = { "results": 1 }
	json_response=json.dumps(answer)
	response=Response(json_response,content_type='application/json; charset=utf-8')
	response.headers.add('content-length',len(json_response))
	response.status_code=200
	with open("data.json", "w") as data:
		json.dump(tasks,data)
	print(tasks)
	return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)





