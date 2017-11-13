from flask import Flask, render_template, request, make_response, g
from kafka import KafkaProducer
from confluent_kafka import Producer
import os
import socket
# import random
# import json

option_a      = os.getenv('OPTION_A', "Cats")
option_b      = os.getenv('OPTION_B', "Dogs")
KAFKA_TOPIC_1 = os.getenv('KAFKA_TOPIC_1', "incorrect_kafka_topic")
KAFKA_TOPIC_2 = os.getenv('KAFKA_TOPIC_2', "incorrect_kafka_topic")  
KAFKA_SERVER  = os.getenv('KAFKA_SERVER')
hostname = socket.gethostname()
print("hostname is " + hostname)

#add logic to exit gracefully if Kafka Server is unavailable
# producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER, 
#                 key_serializer=str.encode,
#                 value_serializer=lambda v: json.dumps(v).encode('utf-8'))
p = Producer({'bootstrap.servers': KAFKA_SERVER})

app = Flask(__name__)

# def get_redis():
#     if not hasattr(g, 'redis'):
#         g.redis = Redis(host="redis", db=0, socket_timeout=5)
#     return g.redis

def acked(err, msg):
    if err is not None:
        print("failed to deliver message: {0}: {1}"
            .format(msg.value(), err.str()))
    else:
        print("Message produced: {0}".format(msg.value()))

@app.route("/", methods=['POST','GET'])
def hello():
    # voter_id = request.cookies.get('voter_id')
    # if not voter_id:
    #     voter_id = hex(random.getrandbits(64))[2:-1]

    vote = None

    if request.method == 'POST':
        # redis = get_redis()
        vote = request.form['vote']

        try:
            for val in xrange(1, 1000):
            p.produce(KAFKA_TOPIC_2, 'myvalue #{0}'
                        .format(val), callback=acked)
        p.poll(0.5)
        except KeyboardInterrupt:
            pass
        p.flush(30)

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
