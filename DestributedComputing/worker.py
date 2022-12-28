#!/usr/bin/env python3

import requests, json, time, sympy

def factorial(n):
	return 1 if n<2 else factorial(n-1) 

def get_task():
	response=requests.get("http://192.168.25.128:8000/gettask")
	data=json.loads(response.text)
	print("INPUT: ", data)
	return data

def calculate(task):
	startTime = time.time()
	task["result"] = sympy.isprime(2**task["inputdata"]-1)
	task["time"] = time.time()-startTime
	print("OUTPUT", task)
	return task

def send_answer(answer):
	response = requests.post("http://192.168.25.128:8000/sendanswer",json=answer)

task = get_task()
answer = calculate(task)
send_answer(answer)
