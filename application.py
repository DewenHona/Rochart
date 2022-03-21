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
random.seed()  #RNG

@application.route("/")


# def readcsv_data():
#     with open('data.csv', 'r') as f:
#         reader = csv.reader(f, delimiter=';')
#         data_list = list()
#         for row in reader:
#             data_list.append(row)
#     data = [dict(zip(data_list[0],row)) for row in data_list]
#     data.pop(0)
#     s = json.dumps(data)


def index() -> str:
    return render_template("index.html")

def generate_random_data() -> Iterator[str]:

    if request.headers.getlist("X-Forwarded-For"):
        client_ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        client_ip = request.remote_addr or ""

    try:
        logger.info("Client %s connected", client_ip)
        while True:
            json_data = json.dumps(
                {
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "value": random.random() ,
                }
            )
            yield f"data:{json_data}\n\n"
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
