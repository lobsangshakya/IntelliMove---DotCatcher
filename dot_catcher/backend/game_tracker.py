from kafka import KafkaConsumer
import json, threading, time

# Game state
game_state = {
    "score": 0,
    "misses": 0,
    "total_dots": 0,
    "start_time": time.time()
}

def create_consumer(topic):
    return KafkaConsumer(
        topic,
        bootstrap_servers="localhost:9092",
        value_deserializer=lambda m: json.loads(m.decode())
    )

def update_duration():
    return time.time() - game_state["start_time"]

def print_game_state():
    total = game_state["total_dots"]
    duration = update_duration()
    accuracy = (game_state["score"] / total * 100) if total else 0

    print(f"""
=== GAME STATE ===
Score: {game_state['score']}
Misses: {game_state['misses']}
Total Dots: {total}
Game Duration: {duration:.2f}s
Accuracy: {accuracy:.2f}%
==================
""")

def consume_dots():
    print("Dot consumer started...")
    for msg in create_consumer("dots"):
        print(f"Dot appeared: {msg.value}")
        game_state["total_dots"] += 1
        print_game_state()

def consume_actions():
    print("Action consumer started...")
    for msg in create_consumer("actions"):
        event = msg.value
        print(f"Action received: {event}")

        if event["event_type"] == "dot_caught":
            game_state["score"] += 1
        elif event["event_type"] == "dot_missed":
            game_state["misses"] += 1

        print_game_state()

if __name__ == "__main__":
    print("Game Tracker started...")

    threading.Thread(target=consume_dots, daemon=True).start()
    threading.Thread(target=consume_actions, daemon=True).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Game Tracker stopped.")