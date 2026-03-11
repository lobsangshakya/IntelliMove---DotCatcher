from kafka import KafkaProducer
import json, random, time, os
from datetime import datetime

# Get Kafka bootstrap servers from environment variable
KAFKA_BOOTSTRAP_SERVERS = os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

def create_producer_with_retry():
    """Create Kafka producer with retry logic"""
    max_retries = 30
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            print(f"Attempting to connect to Kafka (attempt {attempt + 1}/{max_retries})...")
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode()
            )
            print("Successfully connected to Kafka!")
            return producer
        except Exception as e:
            print(f"Failed to connect to Kafka: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached. Exiting.")
                exit(1)

producer = create_producer_with_retry()

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
        print("Starting continuous dot generation...")
        while True:
            # Randomly choose number of dots to generate (5-7)
            num_dots = random.randint(5, 7)
            print(f"Generating batch of {num_dots} dots")
            
            for i in range(num_dots):
                generate_dot()
                
                # Add delay between dots
                time.sleep(random.uniform(0.5, 2.0))
            
            print("Batch completed, waiting before next batch...")
            time.sleep(2.0)  # Wait 2 seconds between batches
        
    except KeyboardInterrupt:
        print("Dot generation interrupted by user")
    finally:
        producer.close()
        print("Kafka producer closed")
