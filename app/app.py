from flask import Flask, request, jsonify
from flask_restful import Resource
from confluent_kafka import Producer
import json

p = Producer({"bootstrap.servers": "localhost:9092"})
# create_app wraps the other functions to set up the project


def create_app(config=None, testing=False, cli=True):
    """
    Application factory, used to create application
    """
    app = Flask(__name__, static_folder=None)
    app.port = 5050

    @app.route("/tag/<uuid>/<tag>", methods=["POST"])
    def data(uuid, tag):
        print(">>>>>>>>.", uuid, tag, type(tag))
        p.produce(
            topic="content_curator_twitter",
            key=uuid,
            value=json.dumps({"preference": tag}),
        )
        p.flush()
        print("PUBLISH")
        return "True"

    return app
