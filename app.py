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

# === 3. 核心 HTML/JS 代码 ===
html_code = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <style>
        /* === 全局样式 === */
        body {
            margin: 0; padding: 20px; background-color: #2d1b4e;
            background-image: radial-gradient(#4a2c7a 1px, transparent 1px);
            background-size: 20px 20px; font-family: 'Courier New', Courier, monospace;
            display: flex; flex-direction: column; align-items: center; min-height: 95vh; box-sizing: border-box;
        }

        /* === 电视机外框 === */
        .tv-set {
            background-color: #2a2a2a; padding: 20px 20px 40px 20px; border-radius: 30px;
            box-shadow: inset 0 0 10px #000, 0 0 0 5px #111, 0 20px 50px rgba(0,0,0,0.6);
            border-bottom: 10px solid #1a1a1a; margin-bottom: 30px; position: relative;
        }
        .tv-logo {
            position: absolute; bottom: 12px; left: 50%; transform: translateX(-50%);
            color: #666; font-weight: bold; font-size: 12px; letter-spacing: 2px; text-shadow: -1px -1px 0 #000;
        }

        /* === 画布 === */
        #meme-canvas {
            position: relative; width: 700px; max-width: 90vw; aspect-ratio: 4 / 3;
            background-color: #ffffff; border-radius: 40px / 10px;
            box-shadow: inset 0 0 20px rgba(0,0,0,0.5); overflow: hidden;
            border: 2px solid #000; 
            filter: contrast(125%) brightness(105%);
            image-rendering: pixelated;
        }
        #meme-canvas::after {
            content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background-image: url("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAMAAAAp4XiDAAAAUVBMVEWFhYWDg4N3d3dtbW17e3t1dXV0dHR4eHh2dnZ6enp8fHx5eXl9fX1xcXF/f39wcHBzc3Nvb29TU1NEREQtLS0lJSUgICAfHx8QEBAAAAAA/wAkAAAAPnRSTlMAAQIDBAUGBwgJCgsMDQ4PEBITFBUWFxgZGhscHR4fICEiIyQmJygpKissLS4vMDEyMzQ1Njc4OTo7PD0+P0Zom6gAAAEZSURBVEjHhZKHctwwDANFaaTYRZvb/v9fN0hA4g1cOa3tK9c4FkWRokRKCgE/hJ1I8d/Zt2r58wWza3eF4H92v2m+gU+R8X+w5874D2z9F0j8C53jX+h3/IWH+Bdu+S9c418YFv+FufkXlvErbPErXN9+hU9/hX3/Fa7XW2Q1r9HXeI2u1it0/b5Ctl9B1+9/IXsE7P25QnZfIftv0M1+hWz+C9k/obcI2T2Bt98gO39B71+QnZeo9r9A7xW62+9R+xX2vEDvF+jdY7XfINsH9H4F7X+D7L4h92s0998gO19R+/+g2z/o9gH9+4LevoD+O+j/B/R+h/2+Qp7vUPN3qNl+Q+3W8x37B6jdfL9jV1G+X1H8A4x9d6nQ8oafAAAAAElFTkSuQmCC");
            opacity: 0.25; pointer-events: none; z-index: 5; mix-blend-mode: overlay;
        }

        /* === 漂浮文字 === */
        .floater {
            position: absolute; 
            white-space: nowrap; 
            cursor: grab; 
            font-weight: 900; 
            padding: 20px; 
            line-height: 1.5; 
            z-index: 10; 
            opacity: 1; 
            display: inline-block;
            will-change: transform, left, top;
            -webkit-font-smoothing: none;
            text-rendering: geometricPrecision;
            transition: font-size 0.3s, color 0.3s, text-shadow 0.3s;
        }

        /* === 控制面板 === */
        #controls {
            background-color: #c0c0c0; border: 2px solid #fff; border-right-color: #404040; border-bottom-color: #404040;
            padding: 15px; width: 700px; max-width: 90vw; display: flex; flex-direction: column; gap: 15px; box-shadow: 5px 5px 0 rgba(0,0,0,0.3);
        }
        .control-row { display: flex; gap: 10px; flex-wrap: wrap; justify-content: space-between; align-items: center;}
        input[type="text"] { flex: 2; background: #fff; border: 2px solid #404040; border-right-color: #fff; border-bottom-color: #fff; padding: 8px; font-family: 'Courier New', monospace; font-weight: bold; outline: none; font-size: 18px; }
        .retro-btn { background: #c0c0c0; border: 2px solid #fff; border-right-color: #404040; border-bottom-color: #404040; padding: 8px 15px; cursor: pointer; font-weight: bold; font-family: 'Courier New', monospace; font-size: 12px; color: black; display: flex; align-items: center; justify-content: center; position: relative; overflow: hidden; flex:1; white-space: nowrap; height: 36px; box-sizing: border-box; }
        .retro-btn:active { border: 2px solid #404040; border-right-color: #fff; border-bottom-color: #fff; transform: translate(1px, 1px); }
        .retro-btn.danger { color: red; }
        .retro-btn.action { color: blue; }
        #file-input { position: absolute; opacity: 0; width: 100%; height: 100%; cursor: pointer; top:0; left:0;}

        .footer-text { margin-top: 20px; font-family: 'Courier New', Courier, monospace; color: rgba(255, 255, 255, 0.6); font-size: 14px; font-weight: bold; text-shadow: 2px 2px 0 #000; letter-spacing: 1px; text-align: center; }

        /* === 移动端适配 & 降噪 === */
        @media (max-width: 768px) {
            body {
                padding: 10px;
            }

            .tv-set {
                width: 100%;
                padding: 10px 10px 30px 10px;
            }

            #meme-canvas {
                width: 100%;
                max-width: 100%;
                border-radius: 24px / 8px;
                filter: none; /* 移动端关闭对比/亮度滤镜，减少闪烁 */
            }

            /* 关掉 CRT 噪点遮罩 */
            #meme-canvas::after {
                opacity: 0;
                background-image: none;
                content: "";
            }

            #controls {
                width: 100%;
                max-width: 100%;
                padding: 10px;
                gap: 10px;
            }

            .control-row {
                flex-direction: column;
                align-items: stretch;
                gap: 8px;
            }

            input[type="text"] {
                font-size: 14px;
                padding: 6px 8px;
            }

            .retro-btn {
                font-size: 12px;
                height: auto;
                white-space: normal;
                padding: 8px 10px;
            }

            /* 移动端降低文字特效以防闪屏 */
            .floater {
                -webkit-font-smoothing: antialiased;
                text-rendering: optimizeLegibility;
                will-change: left, top;
            }
        }
    </style>
</head>
<body>

    <div class="tv-set">
        <div id="meme-canvas"></div>
        <div class="tv-logo">SONY TRINITRON</div>
    </div>

    <div id="controls">
        <div>
            <div class="control-row">
                <input type="text" id="textInput" placeholder="Type your passion..." value="Design is My Passion !!!">
                <button class="retro-btn" style="flex:0.5;" onclick="spawnSentence()">ADD TEXT</button>
                <button class="retro-btn action" style="flex:0.5;" onclick="restyleAll()">🔀 RE-STYLE</button>
                <button class="retro-btn danger" style="flex:0.3;" onclick="clearCanvas()">🗑️</button>
            </div>
        </div>
        <div>
            <div class="control-row">
                <button class="retro-btn" onclick="setBg('white')">⬜ White</button>
                <button class="retro-btn" onclick="setHighSatRainbow()">🌈 Rainbow</button>
                <button class="retro-btn" onclick="setBg('win98')" style="background:#008080; color:white;">💻 Win98</button>
                <button class="retro-btn" onclick="setBg('bliss')" style="background: linear-gradient(to bottom, #62c2fc, #ffffff); color:black;">🏞️ Bliss</button>
                <button class="retro-btn">📂 Upload <input type="file" id="file-input" accept="image/*"></button>
            </div>
        </div>
        <div style="margin-top:5px;">
            <button class="retro-btn" style="width: 100%; font-size: 16px;" onclick="exportMeme()">💾 EXPORT MEME</button>
        </div>
    </div>

    <div class="footer-text">© 2025 Leki's Arc Inc.</div>

<script>
    const canvas = document.getElementById('meme-canvas');
    const textInput = document.getElementById('textInput');
    const blissData = "__BLISS__";
    const BASE_SPEED = 0.8;                             // 速度稍快一点
    const isMobile = window.matchMedia('(max-width: 768px)').matches;
    let floaters = [];

    const fontFamilies = ['"Comic Sans MS"', 'Impact', '"Times New Roman"', 'Arial Black', 'Papyrus', 'Courier New', 'Verdana', '"Brush Script MT"'];

    const highSatGradients = [
        "linear-gradient(180deg, #FF0000 0%, #FF7F00 15%, #FFFF00 30%, #00FF00 50%, #0000FF 70%, #4B0082 85%, #9400D3 100%)",
        "linear-gradient(45deg, #FF0000, #FFFF00, #0000FF, #FF0000)",
        "linear-gradient(135deg, #FF00CC 0%, #333399 100%)", 
        "linear-gradient(90deg, #00FF00, #FF00FF, #00FFFF, #FFFF00)",
        "radial-gradient(circle, #FFFF00 0%, #FF0000 100%)",
        "linear-gradient(120deg, #e4ff00 0%, #ff0055 50%, #00ccff 100%)",
        "linear-gradient(to bottom right, #2C3E50, #FD746C)",
        "linear-gradient(to bottom, #00F260, #0575E6)" 
    ];

    function randomColor() {
        return `hsl(${Math.floor(Math.random() * 360)}, 100%, 50%)`;
    }

    class Floater {
        constructor(text) {
            this.element = document.createElement('div');
            this.element.className = 'floater';
            this.element.innerText = text;

            const safeMargin = 100;
            const maxW = canvas.clientWidth || 700;
            const maxH = canvas.clientHeight || 500;

            this.x = safeMargin + Math.random() * Math.max(10, (maxW - 2 * safeMargin));
            this.y = safeMargin + Math.random() * Math.max(10, (maxH - 2 * safeMargin));

            this.vx = (Math.random() - 0.5) * BASE_SPEED;
            this.vy = (Math.random() - 0.5) * BASE_SPEED;

            this.applyRandomStyle();
            this.element.addEventListener('click', (e) => { e.stopPropagation(); this.element.remove(); });
            canvas.appendChild(this.element);

            this.resolveOverlap();  // 生成时做一次排布，尽量不和已有文字重叠
        }

        resolveOverlap() {
            const maxW = canvas.clientWidth || 700;
            const maxH = canvas.clientHeight || 500;
            const safeMargin = 40;
            const maxAttempts = 40;

            if (!maxW || !maxH) return;

            let attempts = 0;

            const getRect = () => {
                const w = this.element.offsetWidth || 0;
                const h = this.element.offsetHeight || 0;
                return { w, h };
            };

            while (attempts < maxAttempts) {
                const { w, h } = getRect();
                let overlap = false;

                for (const other of floaters) {
                    // 忽略已从 DOM 移除的
                    if (!other || !other.element || !other.element.isConnected) continue;

                    const ow = other.element.offsetWidth || 0;
                    const oh = other.element.offsetHeight || 0;

                    if (ow === 0 || oh === 0 || w === 0 || h === 0) continue;

                    const noOverlap =
                        this.x + w < other.x ||
                        this.x > other.x + ow ||
                        this.y + h < other.y ||
                        this.y > other.y + oh;

                    if (!noOverlap) {
                        overlap = true;
                        break;
                    }
                }

                if (!overlap) break;

                // 重抽一个位置继续试
                this.x = safeMargin + Math.random() * Math.max(10, (maxW - 2 * safeMargin));
                this.y = safeMargin + Math.random() * Math.max(10, (maxH - 2 * safeMargin));
                attempts++;
            }

            this.element.style.left = `${this.x}px`;
            this.element.style.top = `${this.y}px`;
        }

        applyRandomStyle() {
            this.element.style.fontFamily = fontFamilies[Math.floor(Math.random() * fontFamilies.length)];
            const size = Math.floor(Math.random() * 120) + 30;
            this.element.style.fontSize = `${size}px`;

            // === Mobile: 简化版，保留彩色但去掉阴影和变形，减少闪烁 ===
            if (isMobile) {
                const color = randomColor();
                this.element.style.cssText = `
                    font-family: ${this.element.style.fontFamily};
                    font-size: ${size}px;
                    position: absolute;
                    white-space: nowrap;
                    cursor: grab;
                    z-index: 10;
                    opacity: 1;
                    display: inline-block;
                    padding: 12px 16px;
                    line-height: 1.4;
                    left: ${this.x}px;
                    top: ${this.y}px;
                    color: ${color};
                    -webkit-font-smoothing: antialiased;
                    text-rendering: optimizeLegibility;
                    will-change: left, top;
                `;
                this.element.style.transform = 'none';
                this.element.style.textShadow = 'none';
                this.element.style.webkitTextStroke = '0';
                return;
            }

            // === Desktop: 保留原来的花里胡哨特效 ===
            this.element.style.cssText = `
                font-family: ${this.element.style.fontFamily};
                font-size: ${size}px;
                position: absolute;
                white-space: nowrap;
                cursor: grab;
                z-index: 10;
                opacity: 1;
                display: inline-block;
                will-change: transform, left, top;
                -webkit-font-smoothing: none;
                text-rendering: geometricPrecision;
                padding: 20px;
                line-height: 1.5;
                transition: font-size 0.3s, color 0.3s, text-shadow 0.3s;
                left: ${this.x}px;
                top: ${this.y}px;
            `;

            const styleType = Math.floor(Math.random() * 6);
            const color1 = randomColor();
            const color2 = randomColor();

            let transformCSS = "";

            if (styleType === 0) {
                this.element.style.color = "#fff";
                this.element.style.webkitTextStroke = "2px black";
                this.element.style.textShadow = `4px 4px 0 ${color1}, 8px 8px 0 ${color2}`;
                this.element.style.fontWeight = "900";
            } 
            else if (styleType === 1) {
                this.element.style.color = color1;
                this.element.style.textShadow = `1px 1px 0 #000, 2px 2px 0 #000, 3px 3px 0 #000, 4px 4px 0 #000, 5px 5px 0 ${color2}`;
                transformCSS += " skew(-10deg)";
            } 
            else if (styleType === 2) {
                this.element.style.color = color1;
                this.element.style.webkitTextStroke = `4px black`; 
                this.element.style.paintOrder = "stroke fill"; 
            } 
            else if (styleType === 3) {
                this.element.style.color = "#00ff00"; 
                this.element.style.textShadow = `-3px 0 red, 3px 0 blue`;
                this.element.style.fontFamily = '"Courier New", monospace';
            } 
            else if (styleType === 4) {
                this.element.style.color = color1;
                const scaleX = 0.6 + Math.random() * 1.2; 
                const scaleY = 0.6 + Math.random() * 0.8; 
                const skew = Math.random() * 40 - 20;     
                transformCSS += ` scale(${scaleX}, ${scaleY}) skew(${skew}deg)`;
                if (Math.random()>0.5) this.element.style.webkitTextStroke = "1px black";
            }
            else {
                this.element.style.color = color1;
                let scaleX, scaleY;
                if (Math.random() > 0.5) {
                    scaleX = 1.5 + Math.random() * 1.5; 
                    scaleY = 0.6 + Math.random() * 0.2; 
                } else {
                    scaleX = 0.4 + Math.random() * 0.3; 
                    scaleY = 1.5 + Math.random() * 1.5; 
                }
                transformCSS += ` scale(${scaleX.toFixed(2)}, ${scaleY.toFixed(2)})`;
                if (Math.random() > 0.5) this.element.style.webkitTextStroke = "1px black";
            }

            if (!transformCSS.includes("rotate")) {
                const rotate = Math.floor(Math.random() * 60) - 30;
                transformCSS += ` rotate(${rotate}deg)`;
            }
                
            this.element.style.transform = transformCSS;
        }
            
        update() {
            const w = this.element.offsetWidth;
            const h = this.element.offsetHeight;
            const maxW = canvas.clientWidth || 700;
            const maxH = canvas.clientHeight || 500;
            const safeBuffer = 50; 

            this.x += this.vx; this.y += this.vy;

            if (this.x <= safeBuffer) { this.vx = Math.abs(this.vx); this.x = safeBuffer; } 
            else if (this.x + w >= maxW - safeBuffer) { this.vx = -Math.abs(this.vx); this.x = maxW - w - safeBuffer; }

            if (this.y <= safeBuffer) { this.vy = Math.abs(this.vy); this.y = safeBuffer; } 
            else if (this.y + h >= maxH - safeBuffer) { this.vy = -Math.abs(this.vy); this.y = maxH - h - safeBuffer; }

            this.element.style.left = `${this.x}px`; 
            this.element.style.top = `${this.y}px`;
        }
    }

    function spawnSentence() {
        const text = textInput.value.trim();
        if (!text) return;
        const words = text.includes(' ') ? text.split(/\\s+/) : text.split('');
        words.forEach(w => floaters.push(new Floater(w)));
        textInput.value = '';
    }

    function restyleAll() { floaters.forEach(f => f.applyRandomStyle()); }
    function clearCanvas() { floaters = []; canvas.innerHTML = ''; }

    let rainbowClickCount = 0;
    function setHighSatRainbow() {
        const gradient = rainbowClickCount === 0 ? highSatGradients[0] : highSatGradients[Math.floor(Math.random() * highSatGradients.length)];
        rainbowClickCount++;
        canvas.style.background = gradient;
        canvas.style.backgroundSize = "cover";
    }

    function setBg(type) {
        if (type === 'white') canvas.style.background = '#ffffff';
        else if (type === 'win98') canvas.style.background = '#008080';
        else if (type === 'bliss') canvas.style.background = `url('${blissData}') center/cover no-repeat`;
    }

    document.getElementById('file-input').addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (evt) => canvas.style.background = `url(${evt.target.result}) center/cover no-repeat`;
            reader.readAsDataURL(file);
        }
        e.target.value = ''; 
    });

    function exportMeme() {
        const originalRadius = canvas.style.borderRadius;
        const originalShadow = canvas.style.boxShadow;
        const originalBorder = canvas.style.border;
        canvas.style.borderRadius = '0'; canvas.style.boxShadow = 'none'; canvas.style.border = 'none';
        html2canvas(canvas, { scale: 2 }).then(capturedCanvas => {
            const link = document.createElement('a'); 
            link.download = 'passion-meme.png'; 
            link.href = capturedCanvas.toDataURL('image/png'); 
            link.click();
            canvas.style.borderRadius = originalRadius; 
            canvas.style.boxShadow = originalShadow; 
            canvas.style.border = originalBorder;
        });
    }

    function animate() { floaters.forEach(f => f.update()); requestAnimationFrame(animate); }

    window.onload = () => { 
        setBg('bliss');
        setTimeout(spawnSentence, 500); 
        animate(); 
    };
    textInput.addEventListener('keypress', (e) => e.key === 'Enter' && spawnSentence());
</script>

</body>
</html>
"""

# 把占位符替换成真实的 Bliss URL
html_code = html_code.replace("__BLISS__", final_bliss_url)

components.html(html_code, height=1000, scrolling=True)
