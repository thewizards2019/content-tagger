from flask import Flask, request, jsonify
from flask_restful import Resource
from confluent_kafka import Producer
import json


# create_app wraps the other functions to set up the project

def create_app(config=None, testing=False, cli=True):
    """
    Application factory, used to create application
    """
    app = Flask(__name__, static_folder=None)

    @app.route("/tag/<uuid>/<tag>", methods=['POST'])
    def data(uuid,tag):
        preference = {
                      'uuid': uuid,
                      'perference-tag': tag
                    }
        jsonify(preference)
        writeToKafka.delivery_report(preference)
        return  "j"

    return app
class writeToKafka():

    def delivery_report(data):
        p = Producer({'bootstrap.servers': 'localhost:9091'})
        p.produce('wizards', json.dumps(data))
        # print(json.dumps(data))
        p.flush()
