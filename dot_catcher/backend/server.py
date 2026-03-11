from flask import Flask, request
from flask_socketio import SocketIO, emit
from kafka import KafkaConsumer, KafkaProducer
import json
import threading
import time
import os

# Get Kafka bootstrap servers from environment variable
KAFKA_BOOTSTRAP_SERVERS = os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

app = Flask(__name__)
# Enable CORS and allow all origins for WebSocket
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Kafka consumers
dots_consumer = None
actions_consumer = None

# Kafka producer for actions
actions_producer = None

# Game state
game_state = {
    'score': 0,
    'misses': 0,
    'game_over': False,
    'target_score': 10,  # Win condition: reach 10 points
    'max_misses': 5      # Lose condition: 5 misses
}

def consume_dots():
    """Consume dot appearance events from Kafka and broadcast to clients"""
    global dots_consumer
    
    print("DEBUG: Starting dots consumer...")
    dots_consumer = KafkaConsumer(
        'dots',
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    
    print("DEBUG: Dots consumer initialized, waiting for messages...")
    for message in dots_consumer:
        event = message.value
        print(f"DEBUG: Received dot event from Kafka: {event}")
        # Broadcast to all connected clients using socketio.emit (thread-safe)
        print(f"DEBUG: Broadcasting dot_appeared to WebSocket clients: {event}")
        socketio.emit('dot_appeared', event)
        print(f"DEBUG: Broadcast complete for dot at {event.get('position')}")

def consume_actions():
    """Consume user action events from Kafka and update game state"""
    global actions_consumer, game_state
    
    print("DEBUG: Starting actions consumer...")
    actions_consumer = KafkaConsumer(
        'actions',
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    
    print("DEBUG: Actions consumer initialized, waiting for messages...")
    for message in actions_consumer:
        event = message.value
        print(f"DEBUG: Received action event from Kafka: {event}")
        
        if event['event_type'] == 'dot_caught':
            game_state['score'] += 1
            print(f"DEBUG: Score updated to {game_state['score']}")
        elif event['event_type'] == 'dot_missed':
            game_state['misses'] += 1
            print(f"DEBUG: Misses updated to {game_state['misses']}")
            
        # Check win/lose conditions
        check_game_status()
        
        # Send updated game state to clients
        print(f"DEBUG: Broadcasting game_state_update: {game_state}")
        socketio.emit('game_state_update', game_state)

def check_game_status():
    """Check if the game should end based on win/lose conditions"""
    global game_state
    
    # Win condition: reach target score
    if game_state['score'] >= game_state['target_score']:
        game_state['game_over'] = True
        game_state['win'] = True
        socketio.emit('game_over', {'result': 'win', 'message': f'Congratulations! You won with {game_state["score"]} points!'})
    
    # Lose condition: too many misses
    elif game_state['misses'] >= game_state['max_misses']:
        game_state['game_over'] = True
        game_state['win'] = False
        socketio.emit('game_over', {'result': 'lose', 'message': f'Game Over! You missed too many dots. Score: {game_state["score"]}'})
    
    # If game is over, send final state
    if game_state['game_over']:
        socketio.emit('game_state_update', game_state)

@app.route('/')
def index():
    return "Dot Catcher Backend Server"

@socketio.on('connect')
def handle_connect():
    print('Client connected - SID: {}'.format(request.sid if hasattr(request, 'sid') else 'unknown'))
    # Send current game state to newly connected client
    emit('game_state_update', game_state)
    print(f'Game state sent to client: {game_state}')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('catch_dot')
def handle_catch_dot(data):
    """Handle when a user catches a dot"""
    print(f"User caught dot at position: {data}")
    
    # Send action to Kafka
    if actions_producer:
        event = {
            "event_type": data['event_type'],
            "position": data['position'],
            "timestamp": data['timestamp']
        }
        actions_producer.send('actions', value=event)
        actions_producer.flush()

@socketio.on('reset_game')
def handle_reset_game():
    """Reset the game to initial state"""
    global game_state
    game_state = {
        'score': 0,
        'misses': 0,
        'game_over': False,
        'target_score': 10,
        'max_misses': 5
    }
    # Notify all clients that game has been reset
    socketio.emit('game_reset', game_state)
    socketio.emit('game_state_update', game_state)

if __name__ == '__main__':
    # Initialize Kafka producer with retry logic
    max_retries = 30
    retry_delay = 2
    actions_producer = None
    
    for attempt in range(max_retries):
        try:
            print(f"Attempting to connect to Kafka (attempt {attempt + 1}/{max_retries})...")
            actions_producer = KafkaProducer(
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            print("Successfully connected to Kafka!")
            break
        except Exception as e:
            print(f"Failed to connect to Kafka: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached. Exiting.")
                exit(1)
    
    # Start Kafka consumers in separate threads
    dots_thread = threading.Thread(target=consume_dots, daemon=True)
    actions_thread = threading.Thread(target=consume_actions, daemon=True)
    
    dots_thread.start()
    actions_thread.start()
    
    # Start Flask server
    socketio.run(app, host='0.0.0.0', port=5001, debug=True, use_reloader=False, allow_unsafe_werkzeug=True)
