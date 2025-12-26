from flask import Flask
from flask_socketio import SocketIO, emit
from kafka import KafkaConsumer, KafkaProducer
import json, threading, time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# Kafka producer & consumers
actions_producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Game state
game_state = {'score': 0, 'misses': 0, 'game_over': False, 'target_score': 10, 'max_misses': 5}

def consume_kafka(topic, update_fn):
    consumer = KafkaConsumer(
        topic, bootstrap_servers='localhost:9092',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    for msg in consumer:
        update_fn(msg.value)

def update_game(event):
    global game_state
    if event['event_type'] == 'dot_caught': game_state['score'] += 1
    elif event['event_type'] == 'dot_missed': game_state['misses'] += 1
    check_game_status()
    socketio.emit('game_state_update', game_state)

def check_game_status():
    global game_state
    if game_state['score'] >= game_state['target_score']:
        game_state.update({'game_over': True, 'win': True})
        socketio.emit('game_over', {'result': 'win', 'message': f'You won! Score: {game_state["score"]}'})
    elif game_state['misses'] >= game_state['max_misses']:
        game_state.update({'game_over': True, 'win': False})
        socketio.emit('game_over', {'result': 'lose', 'message': f'Game Over! Score: {game_state["score"]}'})

@app.route('/')
def index(): return "Dot Catcher Backend"

@socketio.on('connect')
def handle_connect(): emit('game_state_update', game_state)

@socketio.on('catch_dot')
def handle_catch_dot(data):
    if actions_producer:
        actions_producer.send('actions', value=data)
        actions_producer.flush()

@socketio.on('reset_game')
def handle_reset_game():
    global game_state
    game_state = {'score': 0, 'misses': 0, 'game_over': False, 'target_score': 10, 'max_misses': 5}
    socketio.emit('game_reset', game_state)
    socketio.emit('game_state_update', game_state)

if __name__ == '__main__':
    threading.Thread(target=consume_kafka, args=('dots', lambda e: socketio.emit('dot_appeared', e)), daemon=True).start()
    threading.Thread(target=consume_kafka, args=('actions', update_game), daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=5001, debug=True, use_reloader=False)
