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
        print("=" * 60)
        print("DOT GENERATOR STARTED")
        print("=" * 60)
        print("Will generate continuous batches of 5-7 dots for demo...")
        print("Each batch has random delays between dots (0.5-2s)")
        print("Batch delay: 3 seconds")
        print("=" * 60)
        
        batch_count = 0
        
        while True:
            batch_count += 1
            # Generate only 5-7 dots per batch for demo purposes
            num_dots = random.randint(5, 7)
            print(f"\n[BATCH {batch_count}] Generating {num_dots} dots...")
            
            for i in range(num_dots):
                generate_dot()
                
                # Add delay between dots (0.5-2 seconds)
                delay = random.uniform(0.5, 2.0)
                time.sleep(delay)
            
            print(f"[BATCH {batch_count}] Complete! Waiting 3 seconds before next batch...")
            time.sleep(3)  # Wait 3 seconds between batches
        
    except KeyboardInterrupt:
        print("\nDot generation interrupted by user")
    finally:
        producer.close()
        print("Kafka producer closed")
