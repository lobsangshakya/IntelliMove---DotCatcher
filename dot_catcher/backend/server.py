from flask import Flask
from flask_socketio import SocketIO, emit
from kafka import KafkaConsumer, KafkaProducer
import json
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

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
    
    dots_consumer = KafkaConsumer(
        'dots',
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    
    for message in dots_consumer:
        event = message.value
        print(f"Received dot event: {event}")
        # Broadcast to all connected clients
        socketio.emit('dot_appeared', event)

def consume_actions():
    """Consume user action events from Kafka and update game state"""
    global actions_consumer, game_state
    
    actions_consumer = KafkaConsumer(
        'actions',
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    
    for message in actions_consumer:
        event = message.value
        print(f"Received action event: {event}")
        
        if event['event_type'] == 'dot_caught':
            game_state['score'] += 1
        elif event['event_type'] == 'dot_missed':
            game_state['misses'] += 1
            
        # Check win/lose conditions
        check_game_status()
        
        # Send updated game state to clients
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
    print('Client connected')
    # Send current game state to newly connected client
    emit('game_state_update', game_state)

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
    # Initialize Kafka producer
    actions_producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    
    # Start Kafka consumers in separate threads
    dots_thread = threading.Thread(target=consume_dots, daemon=True)
    actions_thread = threading.Thread(target=consume_actions, daemon=True)
    
    dots_thread.start()
    actions_thread.start()
    
    # Start Flask server
    socketio.run(app, host='0.0.0.0', port=5001, debug=True, use_reloader=False)