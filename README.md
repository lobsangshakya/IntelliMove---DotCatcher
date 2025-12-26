diff --git a/README.md b/README.md
index 0000000..1111111 100644
--- a/README.md
+++ b/README.md
@@ -1,6 +1,12 @@
 # Dot Catcher Game

+A real-time interactive game where dots appear on a grid and the user must catch them before they disappear.
+The project demonstrates event-driven architecture using Apache Kafka.
+
+---
+
 A real-time interactive game built with Python, Kafka, and React where players catch randomly appearing dots on a 5x5 grid.

 ## Features
+* 5x5 grid with randomly spawning dots
+* Real-time gameplay updates
+* Kafka-based event streaming
+* Score and miss tracking
+* Win/Lose conditions based on player performance

+## Architecture
+The application follows an event-driven microservices architecture.
+
+* Dot Generator publishes `dot_appeared` events to Kafka
+* Frontend sends `dot_caught` and `dot_missed` events
+* Game Tracker consumes events and updates game state
+* Flask backend relays updates to the React UI via WebSockets
+
 ## Quick Start