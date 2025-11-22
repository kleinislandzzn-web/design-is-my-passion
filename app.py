import streamlit as st
import streamlit.components.v1 as components
import base64
import os

# === 1. Python 后端 ===
def get_image_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
            encoded = base64.b64encode(data).decode()
            return f"data:image/jpeg;base64,{encoded}"
    return None

local_bliss_url = get_image_base64("bliss.jpeg")
fallback_url = "https://web.archive.org/web/20230206142820if_/https://upload.wikimedia.org/wikipedia/en/d/d2/Bliss_%28Windows_XP%29.png"
final_bliss_url = local_bliss_url if local_bliss_url else fallback_url

# === 2. 页面配置 ===
st.set_page_config(
    page_title="What is design?",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {padding: 0 !important;}
    </style>
""", unsafe_allow_html=True)

# === 3. 核心 HTML/JS 代码（Bliss URL 用占位符 __BLISS_URL__） ===
html_code = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <style>
        body {
            margin: 0; padding: 20px; background-color: #2d1b4e;
            background-image: radial-gradient(#4a2c7a 1px, transparent 1px);
            background-size: 20px 20px; font-family: 'Courier New', Courier, monospace;
            display: flex; flex-direction: column; align-items: center; min-height: 95vh;
        }

        .tv-set {
            background-color: #2a2a2a; padding: 20px 20px 40px 20px; border-radius: 30px;
            box-shadow: inset 0 0 10px #000, 0 0 0 5px #111, 0 20px 50px rgba(0,0,0,0.6);
            border-bottom: 10px solid #1a1a1a; margin-bottom: 30px; position: relative;
        }

        .tv-logo {
            position: absolute; bottom: 12px; left: 50%; transform: translateX(-50%);
            color: #666; font-weight: bold; font-size: 12px; letter-spacing: 2px; text-shadow: -1px -1px 0 #000;
        }

        #meme-canvas {
            position: relative;
            width: 700px; max-width: 90vw; aspect-ratio: 4 / 3;
            background-color: #ffffff; border-radius: 40px / 10px;
            box-shadow: inset 0 0 20px rgba(0,0,0,0.5);
            overflow: hidden; border: 2px solid #000; 
            filter: contrast(125%) brightness(105%);
        }

        #meme-canvas::after {
            content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            opacity: 0.25; pointer-events: none; z-index: 5; mix-blend-mode: overlay;
        }

        .floater {
            position: absolute; 
            white-space: nowrap; cursor: grab; 
            font-weight: 900; padding: 12px 16px;
            z-index: 10; display: inline-block;
            transition: font-size 0.3s, color 0.3s, text-shadow 0.3s;
            will-change: transform, left, top;
        }

        #controls {
            background-color: #c0c0c0; border: 2px solid #fff; border-right-color: #404040; border-bottom-color: #404040;
            padding: 15px; width: 700px; max-width: 90vw; display: flex; flex-direction: column; gap: 15px;
            box-shadow: 5px 5px 0 rgba(0,0,0,0.3);
        }

        .control-row { display: flex; gap: 10px; flex-wrap: wrap; }

        input[type="text"] {
            flex: 2; background: #fff; border: 2px solid #404040;
            padding: 8px; font-family: 'Courier New', monospace; font-weight: bold; font-size: 18px;
        }

        .retro-btn {
            background: #c0c0c0; border: 2px solid #fff; border-right-color: #404040; border-bottom-color: #404040;
            padding: 8px 15px; cursor: pointer; font-weight: bold;
            font-family: 'Courier New', monospace; font-size: 12px;
            display: flex; align-items: center; justify-content: center;
            flex:1; white-space: nowrap; height: 36px;
        }

        @media (max-width: 768px) {
            input[type="text"] { font-size: 14px; padding: 6px; }
            .retro-btn { font-size: 12px; height: auto; white-space: normal; padding: 8px; }
            .floater { -webkit-font-smoothing: antialiased; text-rendering: optimizeLegibility; }
            #meme-canvas::after { opacity: 0; }
        }
    </style>
</head>
<body>

<div class="tv-set">
    <div id="meme-canvas"></div>
    <div class="tv-logo">SONY TRINITRON</div>
</div>

<div id="controls">
    <div class="control-row">
        <input type="text" id="textInput" placeholder="Type your passion..." value="Design is My Passion !!!">
        <button class="retro-btn" onclick="spawnSentence()">ADD TEXT</button>
        <button class="retro-btn" onclick="restyleAll()">🔀 RE-STYLE</button>
        <button class="retro-btn" onclick="clearCanvas()">🗑️</button>
    </div>
    <div class="control-row">
        <button class="retro-btn" onclick="setBg('white')">⬜ White</button>
        <button class="retro-btn" onclick="setHighSatRainbow()">🌈 Rainbow</button>
        <button class="retro-btn" onclick="setBg('win98')" style="background:#008080; color:white;">💻 Win98</button>
        <button class="retro-btn" onclick="setBg('bliss')" style="background: linear-gradient(to bottom, #62c2fc, #ffffff); color:black;">🏞️ Bliss</button>
        <button class="retro-btn">📂 Upload <input type="file" id="file-input" accept="image/*" style="opacity:0; position:absolute; width:100%; height:100%;"></button>
    </div>
    <button class="retro-btn" style="width:100%; font-size:16px;" onclick="exportMeme()">💾 EXPORT</button>
</div>

<script>
const canvas = document.getElementById('meme-canvas');
const textInput = document.getElementById('textInput');
const blissData = "__BLISS_URL__";
const isMobile = window.matchMedia('(max-width: 768px)').matches;
let floaters = [];

const BASE_SPEED = 0.30;
const MIN_SPEED = 0.10;
const MAX_SPEED = 0.45;

function randomColor() { return `hsl(${Math.floor(Math.random() * 360)}, 100%, 50%)`; }

class Floater {
    constructor(text) {
        this.element = document.createElement('div');
        this.element.className = 'floater';
        this.element.innerText = text;

        const safe = 100;
        this.x = safe + Math.random() * (canvas.clientWidth - 2 * safe);
        this.y = safe + Math.random() * (canvas.clientHeight - 2 * safe);

        this.vx = (Math.random() - 0.5) * BASE_SPEED;
        this.vy = (Math.random() - 0.5) * BASE_SPEED;

        this.applyStyle();
        canvas.appendChild(this.element);
        this.ensureInBounds();
    }

    applyStyle() {
        const size = Math.floor(Math.random() * 90) + 40;
        const color = randomColor();

        if (isMobile) {
            this.element.style.color = color;
            this.element.style.fontSize = `${size}px`;
            return;
        }

        const styleType = Math.floor(Math.random() * 8);
        if (styleType === 0) this.element.style.textShadow = "2px 2px 0 #000, 4px 4px 0 #000";
        if (styleType === 1) this.element.style.textShadow = `0 0 4px ${color}`;
        if (styleType === 2) this.element.style.textShadow = `0 0 6px ${color}, 0 0 12px ${color}`;
        if (styleType === 3) this.element.style.webkitTextStroke = "2px black";
        if (styleType === 4) this.element.style.transform = "skew(-10deg)";
        if (styleType === 5) this.element.style.transform = "rotate(8deg)";
        if (styleType === 6) this.element.style.transform = "rotate(-8deg)";
        if (styleType === 7) this.element.style.textShadow = `3px 3px 0 ${color}`;

        this.element.style.fontSize = `${size}px`;
        this.element.style.color = color;
    }

    ensureInBounds() {
        const w = this.element.offsetWidth, h = this.element.offsetHeight;
        const maxX = canvas.clientWidth - w - 10;
        const maxY = canvas.clientHeight - h - 10;
        this.x = Math.max(10, Math.min(this.x, maxX));
        this.y = Math.max(10, Math.min(this.y, maxY));
        this.element.style.left = `${this.x}px`;
        this.element.style.top = `${this.y}px`;
    }

    update() {
        this.x += this.vx; this.y += this.vy;

        const w = this.element.offsetWidth, h = this.element.offsetHeight;
        const maxX = canvas.clientWidth - w - 10;
        const maxY = canvas.clientHeight - h - 10;

        if (this.x <= 10 || this.x >= maxX) this.vx = -this.vx;
        if (this.y <= 10 || this.y >= maxY) this.vy = -this.vy;

        let speed = Math.sqrt(this.vx * this.vx + this.vy * this.vy);
        if (speed < MIN_SPEED) {
            const a = Math.random()*Math.PI*2;
            this.vx = Math.cos(a) * BASE_SPEED;
            this.vy = Math.sin(a) * BASE_SPEED;
        }
        if (speed > MAX_SPEED) {
            this.vx *= 0.98; this.vy *= 0.98;
        }

        this.ensureInBounds();
    }
}

function spawnSentence() {
    const text = textInput.value.trim();
    if (!text) return;
    const arr = text.includes(" ") ? text.split(/\s+/) : text.split('');
    arr.forEach(w => floaters.push(new Floater(w)));
    textInput.value = '';
}

function restyleAll() { floaters.forEach(f => f.applyStyle()); }
function clearCanvas() { floaters = []; canvas.innerHTML = ''; }

function setHighSatRainbow() {
    canvas.style.background = "linear-gradient(120deg, red, yellow, green, cyan, blue, violet)";
}
function setBg(type) {
    if (type === 'white') canvas.style.background = '#fff';
    if (type === 'win98') canvas.style.background = '#008080';
    if (type === 'bliss') canvas.style.background = `url(${blissData}) center/cover no-repeat`;
}

document.getElementById('file-input').addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const r = new FileReader();
    r.onload = (evt) => canvas.style.background = `url(${evt.target.result}) center/cover no-repeat`;
    r.readAsDataURL(file);
});

function exportMeme() {
    html2canvas(canvas, { scale: 2 }).then(c => {
        const a = document.createElement('a');
        a.download = 'passion-meme.png';
        a.href = c.toDataURL('image/png');
        a.click();
    });
}

function animate() { floaters.forEach(f => f.update()); requestAnimationFrame(animate); }
window.onload = () => { setBg('bliss'); animate(); };
textInput.addEventListener('keypress', (e) => e.key === 'Enter' && spawnSentence());
</script>

</body>
</html>
"""

# === 修复关键 BUG：给 Bliss URL 自动加引号 ===
html_code = html_code.replace("__BLISS_URL__", f'"{final_bliss_url}"')

components.html(html_code, height=1000, scrolling=True)
