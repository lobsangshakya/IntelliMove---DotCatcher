from kafka import KafkaProducer
import json, random, time
from datetime import datetime

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode()
)

GRID_SIZE = 5

def generate_dot():
    position = [random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)]
    event = {
        "event_type": "dot_appeared",
        "position": position,
        "timestamp": datetime.now().isoformat()
    }
    
    print(f"DEBUG: Generating dot at position {position}")
    producer.send("dots", event)
    producer.flush()
    print(f"DEBUG: Sent dot event to Kafka: {event}")

if __name__ == "__main__":
    try:
        while True:
            generate_dot()
            time.sleep(random.uniform(0.5, 2.0))
    except KeyboardInterrupt:
        producer.close()
