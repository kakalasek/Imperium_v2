from flask import Flask, render_template, url_for, redirect, request
from forms import ApiForm, ScanForm
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = "73eeac3fa1a0ce48f381ca1e6d71f077"

endpoints = [False, False, False, False]
data = [{}, {}, {}, {}]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')

@app.route("/scanner", methods=['GET', 'POST'])
def scanner():
    form = ApiForm()
    scanform = ScanForm()
    if request.method == 'POST' and scanform.validate():
        data[0] = requests.get(f"{endpoints[0]}/@scan?range={scanform.ip.data}&options={scanform.scan_type.data}").json()["nmaprun"]
        return redirect(url_for("scanner"))
    if request.method == 'POST' and form.validate():
        try:
            if requests.get(f"{form.endpoint.data}/@test").json()["state"] == "Scanner":
                endpoints[0] = form.endpoint.data
            return redirect(url_for("scanner"))
        except:
            return redirect(url_for("scanner"))
    return render_template('scanner.html', title='Scanner', form=form, scanform=scanform, endpoint_set=endpoints[0], data=data[0])

@app.route("/scanner/host", methods=['GET'])
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