from flask import Flask, request
import subprocess
import json
import xmltodict

app = Flask(__name__)
app.config['SECRET_KEY'] = "73eeac3fa1a0ce48f381ca1e6d71f077"

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
    return json_output

if __name__ == '__main__':
    app.run(debug=True, port=3001)
