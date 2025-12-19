from flask import Flask, request, jsonify
from kafka import KafkaProducer
import json

app = Flask(__name__)
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode()
)

@app.post('/catch_dot')
def catch_dot():
    d = request.get_json() or {}
    if 'position' not in d:
        return jsonify(error="Invalid data"), 400
    producer.send('actions', {
        "event_type": "dot_caught",
        "position": d['position'],
        "timestamp": d.get('timestamp'),
        "user_id": d.get('user_id', 'anonymous')
    })
    return jsonify(status="success")

app.run(port=5002, debug=True)