🧠 FocusAI

AI-powered concentration monitoring system using YOLOv8, MediaPipe, and Deep Learning

⸻

🎯 Overview

FocusAI is a real-time attention analysis system that detects yawning, head turning, phone usage, and absence (away detection) through camera-based behavioral monitoring.
The system combines computer vision and deep learning models to evaluate focus levels during study or work sessions and provides insights for improving productivity.

⸻

⚙️ Features

✅ Real-time camera streaming through FastAPI WebSocket
✅ Yawn detection (CNN-based mouth state classification)
✅ Drowsiness & eye-closure detection (deep learning model)
✅ Head turn & absence detection (MediaPipe FaceMesh landmarks)
✅ Phone detection using YOLOv8 object detection
✅ Mirror-mode (left–right flipped display for natural view)
✅ Easy React + Flask/FastAPI integration for UI & backend

⸻

🧩 System Architecture
Frontend (React)
   │
   ├── WebSocket (image frames)
   │
Backend (FastAPI)
   ├── YOLOv8 (phone detection)
   ├── MediaPipe (head/eye tracking)
   ├── TensorFlow/Keras (yawn, drowsiness)
   │
   └── Real-time JSON response (Focus metrics)

   🚀 Quick Start
1️⃣ Clone Repository
git clone https://github.com/<your-username>/FocusAI.git
cd FocusAI

2️⃣ Backend Setup
cd back
pip install -r requirements.txt
python main.py

3️⃣ Frontend Setup
cd frontend
npm install
npm start

4️⃣ Start Monitoring
	•	Open your browser at http://localhost:3000
	•	Click 🚀 Start
	•	Allow camera access ✅
	•	Observe real-time detection overlays and statistics.

  📊 Output Example
  Metric    Description
😮‍💨 Yawn      Counts yawns detected through mouth landmarks
👀 Head      Detects head turn via facial symmetry offset
📱 Phone     YOLO detects “cell phone” objects
🙈 Away      Time spent with no face detected

🧩 Folder Structure
FocusAI/
│
├── back/
│   ├── main.py              # FastAPI WebSocket server (YOLO + AI)
│   ├── flask_server.py      # Flask launcher (optional)
│   ├── yawn_model.h5        # Keras-based yawn classifier
│   ├── drowsiness_model.h5  # Eye-closure detection model
│
├── frontend/
│   ├── src/
│   │   ├── StudySessionModal.js   # Core React modal for camera + stream
│   │   ├── App.js
│   │   └── components/
│   ├── public/
│   └── package.json
│
└── README.md

🧠 Future Work
	•	Add emotion recognition module
	•	Integrate focus scoring and session analytics
	•	Develop dashboard for long-term trend visualization
	•	Edge-device optimization (ONNX, TensorRT)

  🪪 License

This project is licensed under the MIT License – feel free to use and modify.
