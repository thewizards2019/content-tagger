from flask import Flask
import re
import json
import requests
from confluent_kafka import Consumer
from confluent_kafka import Producer



def create_app(config=None, testing=False, cli=True):
    """
    Application factory, used to create application
    """
    app = Flask(__name__, static_folder=None)
    app.port = 5010


    def classify_content(sentence):
        """
        recieves
        """
        try:
            resp = requests.get(url="http://localhost:5020/preference/{}".format(sentence))
            return {"personal": resp.content.decode("utf8")}
        except Exception as exp:
            return False

    c = Consumer(
        {
            "bootstrap.servers": "localhost:9092",
            "group.id": "content_curator_twitter_group_50",
            "auto.offset.reset": "earliest",
        }
    )

    p = Producer({"bootstrap.servers": "localhost:9092"})

    c.subscribe(["content_curator_twitter"])

    while True:
        msg = c.poll()

        if msg is None:
            continue
        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue

        # print('Received message: {}'.format(msg.value().decode('utf-8')))
        try:
            m = json.loads(msg.value().decode("utf-8"))
            if "content" in m.keys():
                clf = json.dumps(classify_content(m["content"]))
                msg_key = msg.key().decode("utf-8")
                print("classification", clf)
                if msg_key is not None:
                    p.produce(
                        topic="content_curator_twitter",
                        key=msg_key,
                        value=clf,
                    )
                    p.flush()
                    print("ADDED:", {"key": msg_key, "value": clf})
        except Exception as e:
            print("ERROR:", e)

    c.close()

    return app
