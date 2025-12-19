from kafka import KafkaConsumer
import json
import threading
import time

# Game state
game_state = {
    'score': 0,
    'misses': 0,
    'total_dots': 0,
    'start_time': time.time(),
    'game_duration': 0
}

def consume_dots():
    """Consume dot appearance events from Kafka"""
    consumer = KafkaConsumer(
        'dots',
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    
    print("Dot consumer started...")
    for message in consumer:
        event = message.value
        print(f"Dot appeared: {event}")
        game_state['total_dots'] += 1
        game_state['game_duration'] = time.time() - game_state['start_time']
        print_game_state()

def consume_actions():
    """Consume user action events from Kafka"""
    consumer = KafkaConsumer(
        'actions',
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    
    print("Action consumer started...")
    for message in consumer:
        event = message.value
        print(f"Action received: {event}")
        
        if event['event_type'] == 'dot_caught':
            game_state['score'] += 1
        elif event['event_type'] == 'dot_missed':
            game_state['misses'] += 1
            
        game_state['game_duration'] = time.time() - game_state['start_time']
        print_game_state()

def print_game_state():
    """Print current game state"""
    print("\n=== GAME STATE ===")
    print(f"Score: {game_state['score']}")
    print(f"Misses: {game_state['misses']}")
    print(f"Total Dots: {game_state['total_dots']}")
    print(f"Game Duration: {game_state['game_duration']:.2f} seconds")
    if game_state['total_dots'] > 0:
        accuracy = (game_state['score'] / game_state['total_dots']) * 100
        print(f"Accuracy: {accuracy:.2f}%")
    print("==================\n")

if __name__ == '__main__':
    print("Game Tracker started...")
    
    # Start Kafka consumers in separate threads
    dots_thread = threading.Thread(target=consume_dots, daemon=True)
    actions_thread = threading.Thread(target=consume_actions, daemon=True)
    
    dots_thread.start()
    actions_thread.start()
    
    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Game Tracker stopped.")