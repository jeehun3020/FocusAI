# ====== FocusAI camera test (FastAPI + async YOLO) ======
import cv2, base64, json, io, time, asyncio
import numpy as np
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from ultralytics import YOLO
import uvicorn

# ----------------------------------------------------------
# ⚙️ FastAPI 기본 설정
# ----------------------------------------------------------
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# ----------------------------------------------------------
# ⚙️ YOLO 모델 로드 (비동기 추론용)
# ----------------------------------------------------------
print("⏳ Loading YOLO model...")
yolo_model = YOLO("yolov8n.pt")
print("✅ YOLO model loaded successfully")

# ----------------------------------------------------------
# ⚙️ 유틸 함수: base64 → OpenCV 이미지
# ----------------------------------------------------------
def b64_to_cv2image(data_url: str) -> np.ndarray:
    b64 = data_url.split(",")[1] if "," in data_url else data_url
    img = Image.open(io.BytesIO(base64.b64decode(b64))).convert("RGB")
    return np.array(img)[:, :, ::-1]  # RGB → BGR

# ----------------------------------------------------------
# ⚙️ 비동기 YOLO 감지 함수
# ----------------------------------------------------------
async def detect_objects(frame):
    """YOLO 감지를 별도 스레드로 실행 (루프 블로킹 방지)"""
    def _detect():
        results = yolo_model(frame, verbose=False)[0]
        return results

    results = await asyncio.to_thread(_detect)
    phone_detected = any(yolo_model.names[int(box.cls[0])] == "cell phone" for box in results.boxes)
    return phone_detected

# ----------------------------------------------------------
# ⚙️ 메인 WebSocket 엔드포인트
# ----------------------------------------------------------
@app.websocket("/ws")
async def ws_camera(websocket: WebSocket):
    await websocket.accept()
    print("✅ WebSocket connected (async camera mode)")

    try:
        # 첫 연결 시 ready 신호
        hello = await websocket.receive_json()
        if hello.get("type") == "start":
            await websocket.send_json({"type": "ready"})

        while True:
            msg = await websocket.receive_json()
            if msg.get("type") != "frame":
                continue

            # 프레임 변환
            frame = b64_to_cv2image(msg["data"])
            h, w, _ = frame.shape

            # YOLO 감지 (비동기)
            phone_detected = await detect_objects(frame)

            # 화면에 YOLO 감지 결과 표시
            if phone_detected:
                cv2.putText(frame, "📱 PHONE DETECTED", (30, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            # 프레임 인코딩 및 전송
            _, buffer = cv2.imencode(".jpg", frame)
            frame_b64 = base64.b64encode(buffer).decode("utf-8")

            await websocket.send_json({
                "type": "frame",
                "image": frame_b64
            })

    except Exception as e:
        print("❌ Error:", e)
    finally:
        print("🔚 WebSocket closed")

# ----------------------------------------------------------
# ⚙️ 서버 실행
# ----------------------------------------------------------
if __name__ == "__main__":
    print("🚀 Async FocusAI Camera Server running on ws://localhost:8000/ws")
    uvicorn.run(app, host="0.0.0.0", port=8000)