"""Pemindai ekspresi dan kelelahan mata (kamera real-time & unggah gambar) untuk RuangRasa."""
from __future__ import annotations

import streamlit.components.v1 as components


def render_realtime_yolo_scanner(clinical_prob: float | None = None) -> None:
    """Merender pemindai kamera real-time dan unggah foto dengan gaya minimal selaras tema Teduh."""
    _ = clinical_prob

    html_code = """
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8" />
<style>
  :root {
    --ink: #0F172A;
    --muted: #64748B;
    --line: #E2E8F0;
    --surface: #F8FAFC;
    --teal: #0F766E;
    --red: #B42318;
  }
  * {
    box-sizing: border-box;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  }
  body {
    margin: 0;
    padding: 0;
    background: transparent;
    color: var(--ink);
  }
  .bar {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    margin-bottom: 10px;
  }
  .controls {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 8px;
  }
  button, .btn-upload {
    height: 36px;
    padding: 0 14px;
    border-radius: 8px;
    border: 1px solid var(--line);
    background: #FFFFFF;
    color: var(--ink);
    font-size: 13.5px;
    font-weight: 500;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    transition: background 0.15s ease, transform 0.1s ease;
    user-select: none;
  }
  button:hover, .btn-upload:hover {
    background: var(--surface);
  }
  button:active, .btn-upload:active {
    transform: translateY(1px);
  }
  button.primary {
    background: var(--teal);
    border-color: var(--teal);
    color: #FFFFFF;
  }
  button.primary:hover {
    background: #0D655E;
  }
  .check {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
    color: var(--muted);
    cursor: pointer;
    user-select: none;
    margin-left: 4px;
  }
  .check input {
    accent-color: var(--teal);
    margin: 0;
  }
  .status {
    font-size: 12.5px;
    color: var(--muted);
  }
  .frame {
    position: relative;
    width: 100%;
    aspect-ratio: 16 / 10;
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 12px;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  video {
    display: none;
  }
  canvas {
    width: 100%;
    height: 100%;
    object-fit: contain;
    background: #0F172A;
    display: none;
  }
  .empty {
    text-align: center;
    padding: 24px;
    max-width: 400px;
  }
  .empty-title {
    font-size: 14.5px;
    font-weight: 600;
    color: var(--ink);
    margin-bottom: 4px;
  }
  .empty-sub {
    font-size: 13px;
    color: var(--muted);
    line-height: 1.5;
  }
  .metrics {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    margin-top: 12px;
  }
  @media (max-width: 640px) {
    .metrics {
      grid-template-columns: repeat(2, 1fr);
    }
  }
  .metric {
    border: 1px solid var(--line);
    border-radius: 10px;
    padding: 11px 14px;
    background: #FFFFFF;
  }
  .metric-label {
    font-size: 12.5px;
    color: var(--muted);
    margin-bottom: 4px;
  }
  .metric-value {
    font-size: 22px;
    font-weight: 600;
    color: var(--ink);
    letter-spacing: -0.02em;
  }
  .metric-note {
    font-size: 11.5px;
    color: var(--muted);
    margin-top: 3px;
  }
</style>
</head>
<body>
  <div class="bar">
    <div class="controls">
      <button id="btnStart" class="primary" onclick="startCamera()">Mulai kamera</button>
      <button id="btnStop" onclick="stopCamera()" style="display:none;">Hentikan</button>
      <label class="btn-upload">
        Unggah gambar
        <input type="file" id="fileInput" accept="image/*" style="display:none;" onchange="handleImageUpload(event)" />
      </label>
      <button id="btnSnap" onclick="downloadSnapshot()" style="display:none;">Unduh hasil</button>
      <label class="check">
        <input type="checkbox" id="chkSubBoxes" checked onchange="redrawStaticIfNeeded()" /> Area mata & mulut
      </label>
      <label class="check">
        <input type="checkbox" id="chkLandmarks" onchange="redrawStaticIfNeeded()" /> Titik wajah
      </label>
    </div>
    <div id="statusText" class="status">Siap digunakan</div>
  </div>

  <div class="frame">
    <video id="webcam" autoplay playsinline muted></video>
    <canvas id="overlay" width="720" height="450"></canvas>
    <div id="placeholder" class="empty">
      <div class="empty-title">Pilih sumber gambar</div>
      <div class="empty-sub">Klik Mulai kamera untuk pemindaian langsung, atau pilih Unggah gambar untuk menganalisis foto wajah (JPG/PNG).</div>
    </div>
  </div>

  <div class="metrics">
    <div class="metric">
      <div class="metric-label">Kelelahan mata</div>
      <div class="metric-value" id="valFatigue">–</div>
      <div class="metric-note" id="subFatigue">Rasio bukaan mata (EAR)</div>
    </div>
    <div class="metric">
      <div class="metric-label">Afek datar</div>
      <div class="metric-value" id="valFlat">–</div>
      <div class="metric-note">Proporsi ekspresi netral</div>
    </div>
    <div class="metric">
      <div class="metric-label">Ekspresi sedih</div>
      <div class="metric-value" id="valSad">–</div>
      <div class="metric-note">Deteksi mikro-ekspresi</div>
    </div>
    <div class="metric">
      <div class="metric-label">Sinyal visual</div>
      <div class="metric-value" id="valFusion">–</div>
      <div class="metric-note">Rata-rata indikator visual</div>
    </div>
  </div>

<script src="https://cdn.jsdelivr.net/npm/@vladmandic/face-api@1.7.12/dist/face-api.js"></script>
<script>
  const MODEL_URL = "https://cdn.jsdelivr.net/npm/@vladmandic/face-api@1.7.12/model/";

  let stream = null;
  let running = false;
  let modelsLoaded = false;
  let modelsLoadingPromise = null;
  let lastFrameTime = performance.now();
  let fpsSmooth = 24;

  let sFatigue = 20;
  let sFlat = 40;
  let sSad = 10;
  let sVisual = 24;
  let latestDetection = null;
  let busyDetecting = false;

  // Untuk mode gambar statis yang diunggah
  let uploadedImage = null;
  let staticDetection = null;

  const video = document.getElementById("webcam");
  const canvas = document.getElementById("overlay");
  const ctx = canvas.getContext("2d");
  const statusText = document.getElementById("statusText");
  const placeholder = document.getElementById("placeholder");

  async function loadFaceModels() {
    if (modelsLoaded) return true;
    if (modelsLoadingPromise) return modelsLoadingPromise;
    if (typeof faceapi === "undefined") return false;
    modelsLoadingPromise = (async () => {
      try {
        statusText.textContent = "Memuat model deteksi...";
        await Promise.all([
          faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL),
          faceapi.nets.faceLandmark68TinyNet.loadFromUri(MODEL_URL),
          faceapi.nets.faceExpressionNet.loadFromUri(MODEL_URL)
        ]);
        modelsLoaded = true;
        return true;
      } catch (e) {
        modelsLoaded = false;
        return false;
      }
    })();
    return modelsLoadingPromise;
  }

  function dist(p1, p2) {
    return Math.hypot(p1.x - p2.x, p1.y - p2.y);
  }

  function calcEAR(eye) {
    const v1 = dist(eye[1], eye[5]);
    const v2 = dist(eye[2], eye[4]);
    const h = dist(eye[0], eye[3]);
    return h > 0 ? (v1 + v2) / (2.0 * h) : 0.28;
  }

  async function startCamera() {
    try {
      uploadedImage = null;
      staticDetection = null;
      statusText.textContent = "Meminta izin kamera...";
      stream = await navigator.mediaDevices.getUserMedia({
        video: { width: { ideal: 720 }, height: { ideal: 450 }, facingMode: "user" },
        audio: false
      });
      video.srcObject = stream;
      await video.play();

      canvas.width = video.videoWidth || 720;
      canvas.height = video.videoHeight || 450;
      canvas.style.objectFit = "cover";

      placeholder.style.display = "none";
      canvas.style.display = "block";
      document.getElementById("btnStart").style.display = "none";
      document.getElementById("btnStop").style.display = "inline-block";
      document.getElementById("btnSnap").style.display = "inline-block";

      running = true;
      loadFaceModels();
      requestAnimationFrame(loop);
    } catch (err) {
      statusText.textContent = "Akses kamera ditolak";
    }
  }

  function stopCamera() {
    running = false;
    if (stream) {
      stream.getTracks().forEach(t => t.stop());
      stream = null;
    }
    if (!uploadedImage) {
      canvas.style.display = "none";
      placeholder.style.display = "block";
      document.getElementById("btnSnap").style.display = "none";
      statusText.textContent = "Kamera nonaktif";
    }
    document.getElementById("btnStart").style.display = "inline-block";
    document.getElementById("btnStop").style.display = "none";
  }

  async function handleImageUpload(event) {
    const file = event.target.files && event.target.files[0];
    if (!file) return;

    // Hentikan kamera live bila sedang aktif
    if (running) {
      running = false;
      if (stream) {
        stream.getTracks().forEach(t => t.stop());
        stream = null;
      }
      document.getElementById("btnStart").style.display = "inline-block";
      document.getElementById("btnStop").style.display = "none";
    }

    const img = new Image();
    img.onload = async () => {
      uploadedImage = img;
      // Sesuaikan ukuran kanvas dengan proporsi foto asli (maks lebar 960px agar tajam)
      const maxDim = 960;
      let cw = img.naturalWidth || img.width;
      let ch = img.naturalHeight || img.height;
      if (cw > maxDim || ch > maxDim) {
        const scale = maxDim / Math.max(cw, ch);
        cw = Math.round(cw * scale);
        ch = Math.round(ch * scale);
      }
      canvas.width = cw;
      canvas.height = ch;
      canvas.style.objectFit = "contain";

      placeholder.style.display = "none";
      canvas.style.display = "block";
      document.getElementById("btnSnap").style.display = "inline-block";

      ctx.drawImage(img, 0, 0, cw, ch);
      statusText.textContent = "Menganalisis foto...";

      await loadFaceModels();
      if (modelsLoaded) {
        try {
          const opts = new faceapi.TinyFaceDetectorOptions({ inputSize: 416, scoreThreshold: 0.25 });
          staticDetection = await faceapi
            .detectSingleFace(canvas, opts)
            .withFaceLandmarks(true)
            .withFaceExpressions();
        } catch (e) {
          staticDetection = null;
        }
      }
      renderStaticAnalysis();
      event.target.value = "";
    };
    img.src = URL.createObjectURL(file);
  }

  function redrawStaticIfNeeded() {
    if (!running && uploadedImage) {
      renderStaticAnalysis();
    }
  }

  function renderStaticAnalysis() {
    if (!uploadedImage) return;
    const w = canvas.width;
    const h = canvas.height;
    ctx.clearRect(0, 0, w, h);
    ctx.drawImage(uploadedImage, 0, 0, w, h);

    if (staticDetection && staticDetection.detection) {
      applyDetectionOverlay(staticDetection, false, false);
      statusText.textContent = "Foto selesai dianalisis · Wajah terdeteksi";
    } else {
      // Fallback kotak wajah tengah apabila foto terlalu kecil/miring untuk TinyFaceDetector
      const fw = Math.round(w * 0.42);
      const fh = Math.round(h * 0.56);
      const fx = Math.round((w - fw) / 2);
      const fy = Math.round((h - fh) / 2);
      drawBox(fx, fy, fw, fh, "Wajah tidak terdeteksi jelas", "#64748B", true);
      statusText.textContent = "Wajah tidak terdeteksi jelas (gunakan foto wajah menghadap depan)";
    }
  }

  function downloadSnapshot() {
    const link = document.createElement("a");
    link.download = "ruangrasa_hasil_deteksi.png";
    link.href = canvas.toDataURL("image/png");
    link.click();
  }

  function drawBox(x, y, w, h, label, color, isMain = true) {
    ctx.save();
    ctx.strokeStyle = color;
    ctx.lineWidth = isMain ? 2 : 1.25;
    ctx.strokeRect(x, y, w, h);

    if (label) {
      ctx.font = isMain
        ? "600 12px -apple-system, BlinkMacSystemFont, sans-serif"
        : "500 10.5px -apple-system, BlinkMacSystemFont, sans-serif";
      const padX = isMain ? 8 : 5;
      const th = isMain ? 20 : 16;
      const tw = ctx.measureText(label).width + padX * 2;
      const ty = Math.max(0, y - th);

      ctx.fillStyle = color;
      ctx.fillRect(x - 1, ty, tw, th);
      ctx.fillStyle = "#FFFFFF";
      ctx.fillText(label, x + padX - 1, ty + (isMain ? 14 : 11));
    }
    ctx.restore();
  }

  function boundingBoxFromPoints(pts, pad = 6) {
    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    for (const p of pts) {
      if (p.x < minX) minX = p.x;
      if (p.y < minY) minY = p.y;
      if (p.x > maxX) maxX = p.x;
      if (p.y > maxY) maxY = p.y;
    }
    return {
      x: minX - pad,
      y: minY - pad,
      w: (maxX - minX) + pad * 2,
      h: (maxY - minY) + pad * 2
    };
  }

  function applyDetectionOverlay(detObj, mirrorX, smooth) {
    const w = canvas.width;
    const box = detObj.detection.box;
    const score = detObj.detection.score || 0.95;
    const mx = mirrorX ? (w - (box.x + box.width)) : box.x;
    const my = box.y;
    const mw = box.width;
    const mh = box.height;

    const expr = detObj.expressions || {};
    const pNeutral = expr.neutral || 0.5;
    const pHappy = expr.happy || 0.0;
    const pSad = (expr.sad || 0) + (expr.fearful || 0) * 0.7 + (expr.angry || 0) * 0.5;

    const showSub = document.getElementById("chkSubBoxes").checked;
    const showLm = document.getElementById("chkLandmarks").checked;

    let ear = 0.28;
    if (detObj.landmarks) {
      const rawPts = detObj.landmarks.positions.map(p => ({
        x: mirrorX ? (w - p.x) : p.x,
        y: p.y
      }));
      const leftEye = rawPts.slice(36, 42);
      const rightEye = rawPts.slice(42, 48);
      const mouth = rawPts.slice(48, 68);
      ear = (calcEAR(leftEye) + calcEAR(rightEye)) / 2.0;

      if (showSub) {
        const eb1 = boundingBoxFromPoints(leftEye, 5);
        const eb2 = boundingBoxFromPoints(rightEye, 5);
        const mb = boundingBoxFromPoints(mouth, 5);
        drawBox(eb1.x, eb1.y, eb1.w, eb1.h, "Mata", "#0F766E", false);
        drawBox(eb2.x, eb2.y, eb2.w, eb2.h, "Mata", "#0F766E", false);
        drawBox(mb.x, mb.y, mb.w, mb.h, pHappy > 0.35 ? "Senyum" : "Netral", "#334155", false);
      }

      if (showLm) {
        ctx.fillStyle = "#0F766E";
        for (const pt of rawPts) {
          ctx.beginPath();
          ctx.arc(pt.x, pt.y, 1.8, 0, Math.PI * 2);
          ctx.fill();
        }
      }
    }

    const rawFatigue = Math.max(5, Math.min(98, ((0.31 - ear) / 0.13) * 100));
    const rawFlat = Math.max(5, Math.min(98, (pNeutral * (1 - pHappy * 0.8)) * 100));
    const rawSad = Math.max(2, Math.min(98, pSad * 135));
    const rawVisual = 0.42 * rawFatigue + 0.33 * rawSad + 0.25 * rawFlat;

    if (smooth) {
      sFatigue = sFatigue * 0.82 + rawFatigue * 0.18;
      sFlat = sFlat * 0.82 + rawFlat * 0.18;
      sSad = sSad * 0.82 + rawSad * 0.18;
      sVisual = sVisual * 0.82 + rawVisual * 0.18;
    } else {
      sFatigue = rawFatigue;
      sFlat = rawFlat;
      sSad = rawSad;
      sVisual = rawVisual;
    }

    let affectTag = "Ekspresif";
    if (sSad >= 42) affectTag = "Sedih / tegang";
    else if (sFlat >= 55) affectTag = "Afek datar";

    const boxColor = sVisual >= 52 ? "#B42318" : "#0F766E";
    drawBox(
      mx, my, mw, mh,
      `Wajah ${(score * 100).toFixed(0)}% · ${affectTag}`,
      boxColor,
      true
    );
    updateMetrics(ear);
  }

  async function runNeuralDetection() {
    if (!modelsLoaded || busyDetecting || video.readyState < 2) return;
    busyDetecting = true;
    try {
      const opts = new faceapi.TinyFaceDetectorOptions({ inputSize: 224, scoreThreshold: 0.35 });
      const det = await faceapi
        .detectSingleFace(video, opts)
        .withFaceLandmarks(true)
        .withFaceExpressions();
      latestDetection = det || null;
    } catch (e) {
      latestDetection = null;
    } finally {
      busyDetecting = false;
    }
  }

  function updateMetrics(ear) {
    const f = Math.round(sFatigue);
    const fl = Math.round(sFlat);
    const sd = Math.round(sSad);
    const vs = Math.round(sVisual);

    document.getElementById("valFatigue").textContent = f + "%";
    document.getElementById("subFatigue").textContent = `EAR ${ear.toFixed(2)} · ${f >= 55 ? "Mata tampak lelah" : "Terbuka normal"}`;
    document.getElementById("valFlat").textContent = fl + "%";
    document.getElementById("valSad").textContent = sd + "%";

    const fusionEl = document.getElementById("valFusion");
    fusionEl.textContent = vs + "%";
    fusionEl.style.color = vs >= 52 ? "#B42318" : "#0F172A";
  }

  function loop(now) {
    if (!running) return;
    const dt = Math.max(1, now - lastFrameTime);
    lastFrameTime = now;
    fpsSmooth = fpsSmooth * 0.9 + (1000 / dt) * 0.1;

    const w = canvas.width;
    const h = canvas.height;

    ctx.save();
    ctx.translate(w, 0);
    ctx.scale(-1, 1);
    ctx.drawImage(video, 0, 0, w, h);
    ctx.restore();

    runNeuralDetection();

    statusText.textContent = `Aktif · ${Math.round(fpsSmooth)} fps`;

    if (latestDetection && latestDetection.detection) {
      applyDetectionOverlay(latestDetection, true, true);
    }

    requestAnimationFrame(loop);
  }
</script>
</body>
</html>
    """
    components.html(html_code, height=565, scrolling=False)
