from flask import Flask, request, jsonify
from kafka import KafkaProducer
import json

app = Flask(__name__)

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

@app.route('/catch_dot', methods=['POST'])
def catch_dot():
    data = request.get_json(silent=True) or {}
    if 'position' not in data:
        return jsonify(error="Invalid data"), 400

    try:
        producer.send('actions', {
            "event_type": "dot_caught",
            "position": data['position'],
            "timestamp": data.get('timestamp'),
            "user_id": data.get('user_id', 'anonymous')
        })
        return jsonify(status="success", message="Action recorded")
    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
