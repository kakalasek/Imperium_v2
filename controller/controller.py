# This file is the main entrypoint of this app. It contains all the routes #

# Imports #
from flask import Flask, render_template, url_for, redirect, request
from forms import ScanForm
from models import db, Scan
from flask_config import ApplicationConfig
from config import read_config
import requests

# Configuration #
app = Flask(__name__)
app.config.from_object(ApplicationConfig)
db.init_app(app)

config_data = read_config()

# Global variables #
scans = [] 
endpoints = {
    'scanner': config_data['scanner_endpoint']
}

def get_scans():
    for scan in Scan.query.all():
        scans.append({
            'name': scan.name,
            'targer': scan.target,
            'scan_json': scan.scan_json
        })

# Routes #

# Home route ## So far unused
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

# The scanner route
@app.route("/scanner", methods=['GET', 'POST'])
def scanner():

    test = requests.get(f"{endpoints['scanner']}/@test")

    # Loading the forms
    scanform = ScanForm()

    if test.status_code == 200:
        endpoint_set = True


        # Returns for POST requests
        if request.method == 'POST' and scanform.validate():    # Scan has been initiated
            data[0] = requests.get(f"{endpoints[0]}/@scan?range={scanform.ip.data}&options={scanform.scan_type.data}").json()["nmaprun"]
            return redirect(url_for("scanner"))
    
    else:
        endpoint_set = False

    # Default template return for GET requests
    return render_template('scanner.html', scanform=scanform, endpoint_set=endpoint_set)

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

    return render_template('host.html', data=host_data, without_mac=without_mac)



## THE REST
## WORK IN PROGRESS

"""
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
    return render_template('diagnostics.html', form=form, endpoint_set=endpoints[1])

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
    return render_template('password_cracker.html', form=form, endpoint_set=endpoints[2])

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
    return render_template('social_engineering.html', form=form, endpoint_set=endpoints[3])
"""

if __name__ == '__main__':
    app.run(debug=True)