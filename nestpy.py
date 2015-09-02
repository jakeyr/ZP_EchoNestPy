import os
import nestpy_app
import nestpy_lib as nest
import echopy_app
import echopy_doc
import echopy_nest as myApp
import nestpy_app
import nestpy_settings as settings

import requests

from flask import Flask, render_template, Response, send_from_directory, request, current_app, redirect, jsonify, json

app = Flask(__name__)

@app.route("/")
def main():
	return "Web Interface for NestPy"

@app.route("/auth/<path:path>",methods = ['GET'])
def auth(path):

	auth_uri = nest.nestAuth(path)
	return redirect(auth_uri)

@app.route("/oauth2",methods = ['GET'])
def authcode():
	user = request.args.get('state')
	code = request.args.get('code')

	if nest.nestToken(user,code):

		print nest.nestData.getUser(user).getToken()

	return redirect("/")

@app.route("/users")
def listUsers():
	return str(nest.nestData.nestUsers.keys())

@app.route("/structures/<path:path>")
def listStructures(path):
	nest.getStructures(path)
	nest.getThermostats(path)
	return redirect("/")

@app.route("/set/<path:user>/<path:temp>")
def setTemp(user,temp):
	nest.setTemperatureTargetAll(user,temp)
	return redirect("/")

@app.route("/mode/<path:user>/<path:mode>")
def setMode(user,mode):
	nest.setModeAll(user,mode)
	return redirect("/")

@app.route("/alexa/")
def alexa_main():
	return echopy_doc.main_page

@app.route("/alexa/EchoPyAPI",methods = ['GET','POST'])
def apicalls():
	if request.method == 'POST':
		data = request.get_json()
		print(data)
		sessionId = myApp.data_handler(data)
		return sessionId + "\n"

@app.route("/alexa/auth/<path:path>",methods = ['GET'])
def alexa_auth(path):

	auth_uri = nest.nestAuth(path)
	return redirect(auth_uri)

@app.route("/alexa/oauth2",methods = ['GET'])
def alexa_authcode():
	user = request.args.get('state')
	code = request.args.get('code')

	if nest.nestToken(user,code):

		print nest.nestData.getUser(user).getToken()

	return redirect("/alexa")

if __name__ == '__main__':
  port = int(os.environ.get('PORT',5000))
  app.run(host='0.0.0.0', port=port)
