from kafka import KafkaProducer
import json, random, time
from datetime import datetime

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

GRID_SIZE = 5  # 5x5 grid

def generate_dot():
    x = random.randint(0, GRID_SIZE - 1)
    y = random.randint(0, GRID_SIZE - 1)

    event = {
        "event_type": "dot_appeared",
        "position": [x, y],
        "timestamp": datetime.now().isoformat()
    }

    producer.send("dots", value=event)
    print("Dot created:", event)

if __name__ == "__main__":
    try:
        while True:
            generate_dot()
            time.sleep(random.uniform(0.5, 2.0))   # random interval
    except KeyboardInterrupt:
        print("Stopping dot generator...")
        producer.close()