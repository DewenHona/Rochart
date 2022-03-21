import json
import logging
import random
from re import S
import sys
import time
from datetime import datetime
from typing import Iterator
import pandas as pd
import json
import csv

from flask import Flask, Response, render_template, request, stream_with_context, jsonify

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

application = Flask(__name__)
random.seed()

@application.route("/")
 
def index() -> str:
    return render_template("index.html")

def generate_random_data() -> Iterator[str]:

    if request.headers.getlist("X-Forwarded-For"):
        client_ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        client_ip = request.remote_addr or ""

    try:
        df = pd.read_csv('eeg_data.csv')  

        x1 = df["0"].tolist()
        x2 = df["1"].tolist()
        x3 = df["2"].tolist()
        x4 = df["3"].tolist()
        x5 = df["4"].tolist()
        
      
        logger.info("Client %s connected", client_ip)
        i=0
        while True:
            json_data = json.dumps(
                {
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "value1": x1[i],
                    "value2": x2[i],
                    "value3": x3[i],
                    "value4": x4[i],
                    "value5": x5[i],
                
                }
            )
            yield f"data:{json_data}\n\n"
            i+=1
            time.sleep(0.5)
    except GeneratorExit:
        logger.info("Client %s disconnected", client_ip)

@application.route("/chart-data")
def chart_data() -> Response:
  
    response = Response(stream_with_context(generate_random_data()), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response

if __name__ == "__main__":
   
    application.run(host="0.0.0.0", threaded=True)
    