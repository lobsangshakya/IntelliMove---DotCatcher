from flask import Flask, request, jsonify
from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

def create_kafka_producer():
    """Create and return a Kafka producer instance"""
    try:
        return KafkaProducer(
            bootstrap_servers='localhost:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            retries=3
        )
    except KafkaError as e:
        logging.error(f"Kafka connection failed: {e}")
        return None

producer = create_kafka_producer()


@app.route('/catch_dot', methods=['POST'])
def catch_dot():
    """Handle when a user catches a dot"""

    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400

    data = request.get_json()

    # Validate required fields
    if 'position' not in data:
        return jsonify({'error': 'Missing required field: position'}), 400

    event = {
        "event_type": "dot_caught",
        "position": data['position'],
        "timestamp": data.get('timestamp'),
        "user_id": data.get('user_id', 'anonymous')
    }

    if producer is None:
        logging.warning("Kafka producer unavailable")
        return jsonify({'error': 'Event service unavailable'}), 503

    try:
        producer.send('actions', value=event)
        producer.flush()
        logging.info(f"Dot caught event sent: {event}")
        return jsonify({'status': 'success', 'message': 'Action recorded'}), 200

    except KafkaError as e:
        logging.error(f"Kafka error: {e}")
        return jsonify({'error': 'Failed to record action'}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'running'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=False)