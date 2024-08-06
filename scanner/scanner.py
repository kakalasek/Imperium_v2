from flask import Flask, request
from models import db, Scan
import subprocess
import json
import xmltodict

app = Flask(__name__)
app.config['SECRET_KEY'] = "73eeac3fa1a0ce48f381ca1e6d71f077"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/pipa/Personal/Projects/Imperium/v2/controller/instance/db.sqlite3'
db.init_app(app)


def createJson():
    xml_content = subprocess.getoutput(f"sudo nmap -oX - {request.args.get('options')} {request.args.get('range')}")
    data_dict = xmltodict.parse(xml_content)
    json_data = json.dumps(data_dict, indent=4, sort_keys=True)
    with open("json_output.json", "w") as output:
        output.write(json_data)
    return json_data

@app.route("/@test")
def test():
    return {'state': "Scanner"}

@app.route("/@scan")
def scan():
    json_output = createJson()
    scan_name = ''

    match request.args.get('options'):
        case '-sS':
            scan_name = 'SYN Scan'
        case '-sV':
            scan_name = 'Version Scan'
        case '-O':
            scan_name = 'System Scan'
        case '-sF':
            scan_name = 'Fin Scan'
        case '-sU':
            scan_name = 'UDP Scan'
        case '-sT':
            scan_name = 'Connect Scan'
        case _:
            scan_name = 'Scan'
            
    new_scan = Scan(name=scan_name, target=request.args.get('range'), scan_json=json_output)
    db.session.add(new_scan)
    db.session.commit()

    return 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=3001)
