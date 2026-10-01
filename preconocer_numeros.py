

import logging
from threading import Lock

import cv2
import numpy as np
from flask import Flask, Response, jsonify, render_template_string
from tensorflow.keras.models import load_model

model = load_model("modelo_mnist.h5")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
        raise SystemExit("No se pudo abrir la cámara")

app = Flask(__name__)
camera_lock = Lock()
latest_number = None

PAGE = """<!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Reconocedor de dígitos</title>
    <style>
        :root {
            color-scheme: light;
            --ink: #172924;
            --muted: #64746c;
            --paper: #f0f3ed;
            --line: #d5ddd5;
            --green: #174d40;
            --lime: #c6e36a;
            --white: #fff;
        }
        * { box-sizing: border-box; }
        body {
            margin: 0;
            background: var(--paper);
            color: var(--ink);
            font-family: Verdana, sans-serif;
        }
        header {
            height: 64px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 clamp(20px, 5vw, 72px);
            border-bottom: 1px solid var(--line);
            background: rgba(255, 255, 255, .72);
        }
        .brand { display: flex; align-items: center; gap: 11px; font-size: 13px; font-weight: 700; }
        .mark { width: 12px; height: 12px; background: var(--green); border-radius: 2px 7px 2px 7px; }
        .live { display: flex; align-items: center; gap: 8px; color: var(--muted); font-size: 11px; text-transform: uppercase; }
        .dot { width: 8px; height: 8px; border-radius: 50%; background: #70a738; box-shadow: 0 0 0 3px #70a73822; }
        main { max-width: 1180px; margin: 0 auto; padding: 46px 24px 56px; }
        .eyebrow { margin: 0 0 10px; color: #4d7566; font-size: 11px; font-weight: 700; text-transform: uppercase; }
        h1 { margin: 0; font: 400 34px/1.15 Georgia, serif; }
        .layout { display: grid; grid-template-columns: minmax(0, 1.65fr) minmax(230px, .72fr); gap: 22px; margin-top: 28px; }
        .camera { min-width: 0; }
        .camera-head { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 10px; }
        .label { margin: 0; font-size: 12px; font-weight: 700; }
        .subtle { color: var(--muted); font-size: 11px; }
        .feed { overflow: hidden; aspect-ratio: 4 / 3; background: #14211e; border: 1px solid #294238; border-radius: 4px; }
        .feed img { display: block; width: 100%; height: 100%; object-fit: contain; }
        .readout { display: flex; min-height: 100%; flex-direction: column; justify-content: space-between; padding: 22px; background: var(--green); color: var(--white); border-radius: 4px; }
        .readout .label { color: #d0e0d7; }
        .digit { display: grid; min-height: 200px; place-items: center; margin: 24px 0; border: 1px solid #ffffff2a; border-radius: 3px; background: #ffffff09; color: var(--lime); font: 400 112px/1 Georgia, serif; }
        .readout-foot { display: flex; justify-content: space-between; align-items: center; color: #d0e0d7; font-size: 11px; }
        .chip { padding: 6px 9px; border: 1px solid #ffffff35; border-radius: 2px; color: #fff; }
        @media (max-width: 720px) {
            main { padding-top: 32px; }
            h1 { font-size: 29px; }
            .layout { grid-template-columns: 1fr; }
            .readout { min-height: 220px; }
            .digit { min-height: 140px; margin: 16px 0; font-size: 88px; }
        }
    </style>
</head>
<body>
    <header>
        <div class="brand"><span class="mark"></span><span>LAB / MNIST</span></div>
        <div class="live"><span class="dot"></span><span id="status">En vivo</span></div>
    </header>
    <main>
        <p class="eyebrow">Visión por computadora</p>
        <h1>Reconocedor de dígitos</h1>
        <section class="layout">
            <div class="camera">
                <div class="camera-head">
                    <p class="label">Cámara</p>
                    <span class="subtle">Área de lectura: centro</span>
                </div>
                <div class="feed"><img src="/video_feed" alt="Video en vivo de la cámara"></div>
            </div>
            <aside class="readout">
                <p class="label">Número reconocido</p>
                <output class="digit" id="number" aria-live="polite">–</output>
                <div class="readout-foot"><span>Clasificación MNIST</span><span class="chip">0–9</span></div>
            </aside>
        </section>
    </main>
    <script>
        const numberDisplay = document.getElementById('number');
        const statusDisplay = document.getElementById('status');
        async function refreshNumber() {
            try {
                const response = await fetch('/api/number', { cache: 'no-store' });
                const result = await response.json();
                numberDisplay.textContent = result.number ?? '–';
                statusDisplay.textContent = 'En vivo';
            } catch {
                statusDisplay.textContent = 'Sin conexión';
            }
        }
        refreshNumber();
        setInterval(refreshNumber, 350);
    </script>
</body>
</html>"""


def generate_frames():
        global latest_number

        while True:
                with camera_lock:
                        ret, frame = cap.read()
                if not ret:
                        break

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                x1, y1, x2, y2 = 200, 100, 400, 300
                roi = gray[y1:y2, x1:x2]
                image = cv2.resize(roi, (28, 28)) / 255.0
                image = image.reshape(1, 28, 28, 1)

                prediction = model.predict(image, verbose=0)
                latest_number = int(np.argmax(prediction))

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                success, encoded_frame = cv2.imencode(".jpg", frame)
                if not success:
                        continue

                yield (b"--frame\r\n"
                             b"Content-Type: image/jpeg\r\n\r\n" + encoded_frame.tobytes() + b"\r\n")


@app.get("/")
def index():
        return render_template_string(PAGE)


@app.get("/video_feed")
def video_feed():
        return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.get("/api/number")
def api_number():
        return jsonify(number=latest_number)


if __name__ == "__main__":
        logging.getLogger("werkzeug").setLevel(logging.ERROR)
        print("Abre http://127.0.0.1:5000 en tu navegador")
        try:
                app.run(host="127.0.0.1", port=5000, debug=False, threaded=True, use_reloader=False)
        finally:
                cap.release()

