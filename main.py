from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
import requests

app = Flask(__name__)
CORS(app)

@app.route("/")
def mainPage():
    return send_file('templates/index.html')

@app.route("/polyhon", methods=["GET"])
def getPrice():
    company_Name = request.args.get("name")

    API_key = "1xVEQnsDZnGlm0ZOJzGa_5QayQGPJupA"

    endDay = datetime.now().strftime("%Y-%m-%d") #Today's Date
    startDay = (date.today() + relativedelta(months=-6)).strftime("%Y-%m-%d")

    polygon_URL = "https://api.polygon.io/v2/aggs/ticker/"

    request_URL = polygon_URL + company_Name + "/range/1/day/" + startDay + "/" + endDay + "?adjusted=true&sort=asc&apiKey=" + API_key

    response = requests.get(request_URL)

    if response.status_code == 200:
        abstract_json = [response.json()]

        data = abstract_json[0]["results"]

        priceList = []
        volumeList = []

        for item in data:
            priceList.append([item['t'], item['c']])
            volumeList.append([item['t'], item['v']])

        returnFile = jsonify({"priceList" : priceList, "volumeList" : volumeList, "sticker" : company_Name, "time": endDay})
    else:
        returnFile = jsonify({"error": "No data can be searched."})

    return returnFile

    




@app.route("/search", methods=["GET"])
def getname():
    getArgs = request.args.to_dict()
    company_Name = getArgs["name"]
    requestType = getArgs["type"]


    if requestType == "abstract":
        ## Determine the URL for company abstract
        finnfub_origin = "https://finnhub.io/api/v1/stock/profile2?symbol="
        API_key = "cn05sghr01qkcvkfq110cn05sghr01qkcvkfq11g"
        request_URL = finnfub_origin + company_Name + "&token=" + API_key

        # Make a request to the specified URL
        response = requests.get(request_URL)

        if response.status_code == 200:
            jsonFile = response.json()
            if len(jsonFile) == 0:
                return jsonify({})
        else:
            return jsonify({})
    
    if requestType == "price":
        ## Determine the URL for stock price
        finnfub_origin = "https://finnhub.io/api/v1/quote?symbol="
        API_key = "cn05sghr01qkcvkfq110cn05sghr01qkcvkfq11g"
        request_URL = finnfub_origin + company_Name + "&token=" + API_key

        # Make a request to the specified URL
        response = requests.get(request_URL)

        if response.status_code == 200:
            jsonFile = [response.json()]
        else:
            jsonFile = jsonify({"error": "No data can be searched."})


        ## Determine the URL for recommendation
        finnfub_origin = "https://finnhub.io/api/v1/stock/recommendation?symbol="
        API_key = "cn05sghr01qkcvkfq110cn05sghr01qkcvkfq11g"
        request_URL = finnfub_origin + company_Name + "&token=" + API_key

        # Make a request to the specified URL
        response = requests.get(request_URL)

        if response.status_code == 200:
            jsonFile2 = [response.json()]
        else:
            jsonFile = jsonify({"error": "No data can be searched."})

        jsonFile = jsonFile + jsonFile2

    if requestType == "news":
        ## News
        finnfub_origin = "https://finnhub.io/api/v1/company-news?symbol="
        API_key = "cn05sghr01qkcvkfq110cn05sghr01qkcvkfq11g"
        today = datetime.now().strftime("%Y-%m-%d")
        t30days_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        request_URL = finnfub_origin + company_Name + "&from="+t30days_ago+"&to="+today+"&token=" + API_key

        # Make a request to the specified URL
        response = requests.get(request_URL)

        if response.status_code == 200:
            jsonFile = response.json()
        else:
            jsonFile = jsonify({"error": "No data can be searched."})

    returnFile = jsonify(jsonFile)

    return returnFile

if __name__ == "__main__":
    app.run(debug=True)