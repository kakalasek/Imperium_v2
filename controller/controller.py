# This file is the main entrypoint of this app. It contains all the routes #

# Imports #
from flask import Flask, render_template, url_for, redirect, request
from forms import ApiForm, ScanForm
from flask_sqlalchemy import SQLAlchemy
import requests

# Configuration #
app = Flask(__name__)
app.config['SECRET_KEY'] = "73eeac3fa1a0ce48f381ca1e6d71f077"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)

# Global variables #
endpoints = [False, False, False, False] # Field with all currently set endpoints
data = [{}, {}, {}, {}] # Field for data manipulation

# Routes #

# Home route ## So far unused
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')

# The scanner route
@app.route("/scanner", methods=['GET', 'POST'])
def scanner():

    # Loading the forms
    form = ApiForm()
    scanform = ScanForm()

    # Returns for POST requests
    if request.method == 'POST' and scanform.validate():    # Scan has been initiated
        data[0] = requests.get(f"{endpoints[0]}/@scan?range={scanform.ip.data}&options={scanform.scan_type.data}").json()["nmaprun"]
        return redirect(url_for("scanner"))

    if request.method == 'POST' and form.validate():    # Endpoint has been set
        try:
            if requests.get(f"{form.endpoint.data}/@test").json()["state"] == "Scanner":
                endpoints[0] = form.endpoint.data
            return redirect(url_for("scanner"))
        except: # If wrong endpoint or endpoint in the wrong format has been set
            return redirect(url_for("scanner"))
    
    # Default template return for GET requests
    return render_template('scanner.html', title='Scanner', form=form, scanform=scanform, endpoint_set=endpoints[0], data=data[0])

# The scan route
@app.route("/scanner/scan")
def scan():
    return render_template('scan.html')

# The host route
@app.route("/scanner/host")
def host():
    without_mac = True

    if isinstance(data[0]["host"], dict):
        if "@addr" in data[0]["host"]["address"]:
            host_data = data[0]["host"]
        else:
            host_data = data[0]["host"]
            without_mac = False
    else:
        for host in data[0]["host"]:
            if "@addr" in host["address"]:
                if host["address"]["@addr"] == request.args.get('host_ip'):
                    host_data = host
                    break
            else:
                if host["address"][0]["@addr"] == request.args.get('host_ip'):
                    host_data = host
                    without_mac = False
                    break

    return render_template('host.html', title=f'Host:{request.args.get('host_ip')}', data=host_data, without_mac=without_mac)



## THE REST
## WORK IN PROGRESS

@app.route("/diagnostics", methods=['GET', 'POST'])
def diagnostics():
    form = ApiForm()
    if request.method == 'POST' and form.validate():
        try:
            if requests.get(form.endpoint.data).json()["state"] == "Diagnostics":
                endpoints[1] = True
            return redirect(url_for("diagnostics"))
        except:
            return redirect(url_for("diagnostics"))
    return render_template('diagnostics.html', title='Diagnostics', form=form, endpoint_set=endpoints[1])

@app.route("/password_cracker", methods=['GET', 'POST'])
def password_cracker():
    form = ApiForm()
    if request.method == 'POST' and form.validate():
        try:
            if requests.get(form.endpoint.data).json()["state"] == "Password_cracker":
                endpoints[2] = True
            return redirect(url_for("password_cracker"))
        except:
            return redirect(url_for("password_cracker"))
    return render_template('password_cracker.html', title='Password Cracker', form=form, endpoint_set=endpoints[2])

@app.route("/social_engineering", methods=['GET', 'POST'])
def social_engineering():
    form = ApiForm()
    if request.method == 'POST' and form.validate():
        try:
            if requests.get(form.endpoint.data).json()["state"] == "Social_engineering":
                endpoints[3] = True 
            return redirect(url_for("social_engineering"))
        except:
            return redirect(url_for("social_engineering"))
    return render_template('social_engineering.html', title='Social Engineering', form=form, endpoint_set=endpoints[3])

if __name__ == '__main__':
    app.run(debug=True)