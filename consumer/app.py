from flask import Flask, render_template, make_response
from kafka import KafkaConsumer
import os

KAFKA_TOPIC_1 = os.getenv('KAFKA_TOPIC_1', "incorrect_kafka_topic") 
KAFKA_SERVER  = os.getenv('KAFKA_SERVER')

total = 0
consumer = KafkaConsumer(bootstrap_servers=KAFKA_SERVER, value_deserializer=lambda v: json.loads(v).decode('utf-8'))
consumer.subscribe('foo')
for msg in consumer:
    total = total + 1

app = Flask(__name__)

@app.route("/", methods=['GET'])
def hello():

    # total = 0
    # consumer.subscribe(KAFKA_TOPIC_1)
    # for msg in consumer:
    #     total += 1

    # resp = make_response(render_template(
    #     'index.html',
    #     option_a="test1",
    #     option_b="test2",
    #     hostname="blah",
    #     vote="some vote",
    #     total=total
    # ))
    # resp.set_cookie('voter_id', voter_id)
    return "total is " + total


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
