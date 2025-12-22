from flask import Flask
from flask_socketio import SocketIO, emit
from kafka import KafkaConsumer, KafkaProducer
import json, threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode()
)

game_state = {
    'score': 0, 'misses': 0,
    'target_score': 10, 'max_misses': 5,
    'game_over': False
}

def consume(topic, handler):
    consumer = KafkaConsumer(
        topic, bootstrap_servers='localhost:9092',
        value_deserializer=lambda m: json.loads(m.decode())
    )
    for msg in consumer:
        handler(msg.value)

def update_game(event):
    if event['event_type'] == 'dot_caught':
        game_state['score'] += 1
    elif event['event_type'] == 'dot_missed':
        game_state['misses'] += 1

    if game_state['score'] >= game_state['target_score']:
        game_state.update(game_over=True, win=True)
        socketio.emit('game_over', {'result': 'win'})
    elif game_state['misses'] >= game_state['max_misses']:
        game_state.update(game_over=True, win=False)
        socketio.emit('game_over', {'result': 'lose'})

    socketio.emit('game_state_update', game_state)

@app.route('/')
def index():
    return "Dot Catcher Backend"

@socketio.on('connect')
def connect():
    emit('game_state_update', game_state)

@socketio.on('catch_dot')
def catch_dot(data):
    producer.send('actions', data)
    producer.flush()

@socketio.on('reset_game')
def reset_game():
    game_state.update(score=0, misses=0, game_over=False)
    socketio.emit('game_state_update', game_state)

if __name__ == '__main__':
    threading.Thread(target=consume, args=('dots', lambda e: socketio.emit('dot_appeared', e)), daemon=True).start()
    threading.Thread(target=consume, args=('actions', update_game), daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=5001, debug=True, use_reloader=False)
