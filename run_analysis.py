from flask import Flask, jsonify
import requests

app = Flask(__name__)

ANALYSIS_URL = "https://127.0.0.1"
ANALYSIS_PORT = 9999


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/countrylist/', methods=['GET'])
def get_country_list():
    list_url = PUBLICATION_URL+":"+str(PUBLICATION_PORT) + "/countrylist/"
    try:
        r = requests.get(list_url)
        if r.status_code == '200':
            return jsonify({"countries":["Austria", "Australia", "Summoner's Rift"]})
    except:
        return jsonify({"countries": ["Austria", "Australia", "Summoner's Rift"]})
    return jsonify({"countries": ["Austria", "Australia", "Summoner's Rift"]})


if __name__ == '__main__':
    app.run(debug=True,port=ANALYSIS_PORT)


