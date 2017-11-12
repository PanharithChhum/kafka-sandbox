from flask import Flask, render_template, request, make_response, g
from kafka import KafkaProducer
# from redis import Redis
import os
import socket
# import random
# import json

option_a      = os.getenv('OPTION_A', "Cats")
option_b      = os.getenv('OPTION_B', "Dogs")
KAFKA_TOPIC_1 = os.getenv('KAFKA_TOPIC_1', "incorrect_kafka_topic") 
KAFKA_SERVER  = os.getenv('KAFKA_SERVER')
hostname = socket.gethostname()
print("hostname is " + hostname)

#add logic to exit gracefully if Kafka Server is unavailable
producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER, key_serializer=str.encode)


app = Flask(__name__)

# def get_redis():
#     if not hasattr(g, 'redis'):
#         g.redis = Redis(host="redis", db=0, socket_timeout=5)
#     return g.redis

@app.route("/", methods=['POST','GET'])
def hello():
    # voter_id = request.cookies.get('voter_id')
    # if not voter_id:
    #     voter_id = hex(random.getrandbits(64))[2:-1]

    vote = None

    if request.method == 'POST':
        # redis = get_redis()
        vote = request.form['vote']
        producer.send(KAFKA_TOPIC_1, key="pan", value="chhum")
        # data = json.dumps({'voter_id': voter_id, 'vote': vote})
        # redis.rpush('votes', data)

    resp = make_response(render_template(
        'index.html',
        option_a=option_a,
        option_b=option_b,
        hostname=hostname,
        vote=vote,
    ))
    # resp.set_cookie('voter_id', voter_id)
    return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
