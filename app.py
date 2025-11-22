import streamlit as st
import streamlit.components.v1 as components

# 1. 页面配置
st.set_page_config(
    page_title="Retro Passion Maker Ultimate",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. 隐藏 Streamlit 原生元素
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {padding: 0 !important;}
    </style>
""", unsafe_allow_html=True)

# 3. 核心代码
html_code = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <style>
        /* === 1. 网站整体背景 (复古暗色) === */
        body {
            margin: 0; padding: 20px; background-color: #2d1b4e;
            background-image: radial-gradient(#4a2c7a 1px, transparent 1px);
            background-size: 20px 20px; font-family: 'Courier New', Courier, monospace;
            display: flex; flex-direction: column; align-items: center; min-height: 95vh; box-sizing: border-box;
        }

        /* === 2. 80年代电视机外框 === */
        .tv-set {
            background-color: #2a2a2a; padding: 20px 20px 40px 20px; border-radius: 30px;
            box-shadow: inset 0 0 10px #000, 0 0 0 5px #111, 0 20px 50px rgba(0,0,0,0.6);
            border-bottom: 10px solid #1a1a1a; margin-bottom: 30px; position: relative;
        }
        .tv-logo {
            position: absolute; bottom: 12px; left: 50%; transform: translateX(-50%);
            color: #666; font-weight: bold; font-size: 12px; letter-spacing: 2px; text-shadow: -1px -1px 0 #000;
        }

        /* === 3. 屏幕/画布 (4:3) === */
        #meme-canvas {
            position: relative; width: 700px; max-width: 90vw; aspect-ratio: 4 / 3;
            background-color: #ffffff; border-radius: 40px / 10px;
            box-shadow: inset 0 0 20px rgba(0,0,0,0.5); overflow: hidden;
            border: 2px solid #000; transition: background 0.3s;
        }
        /* 复古噪点纹理层 */
        #meme-canvas::after {
            content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background-image: url("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAMAAAAp4XiDAAAAUVBMVEWFhYWDg4N3d3dtbW17e3t1dXV0dHR4eHh2dnZ6enp8fHx5eXl9fX1xcXF/f39wcHBzc3Nvb29TU1NEREQtLS0lJSUgICAfHx8QEBAAAAAA/wAkAAAAPnRSTlMAAQIDBAUGBwgJCgsMDQ4PEBITFBUWFxgZGhscHR4fICEiIyQmJygpKissLS4vMDEyMzQ1Njc4OTo7PD0+P0Zom6gAAAEZSURBVEjHhZKHctwwDANFaaTYRZvb/v9fN0hA4g1cOa3tK9c4FkWRokRKCgE/hJ1I8d/Zt2r58wWza3eF4H92v2m+gU+R8X+w5874D2z9F0j8C53jX+h3/IWH+Bdu+S9c418YFv+FufkXlvErbPErXN9+hU9/hX3/Fa7XW2Q1r9HXeI2u1it0/b5Ctl9B1+9/IXsE7P25QnZfIftv0M1+hWz+C9k/obcI2T2Bt98gO39B71+QnZeo9r9A7xW62+9R+xX2vEDvF+jdY7XfINsH9H4F7X6B7P8F7X+D7L4h92s0998gO19R+/+g2z/o9gH9+4LevoD+O+j/B/R+h/2+Qp7vUPN3qNl+Q+3W8x37B6jdfL9jV1G+X1H8A4x9d6nQ8oafAAAAAElFTkSuQmCC");
            opacity: 0.2; pointer-events: none; z-index: 5; mix-blend-mode: overlay;
        }

        /* === 4. 漂浮文字 === */
        .floater {
            position: absolute; white-space: nowrap; cursor: grab; font-weight: 900; line-height: 1;
            z-index: 10; opacity: 1;
        }
        /* 纯色文字的慢速变色动画 */
        .floater.solid-text { animation: slowHue 10s infinite linear alternate; }
        @keyframes slowHue {
            0% { filter: hue-rotate(0deg); }
            100% { filter: hue-rotate(90deg); }
        }
        /* 彩虹文字不需要变色动画，因为本身就是渐变 */
        .floater.rainbow-text { }

        /* === 5. 复古控制台 === */
        #controls {
            background-color: #c0c0c0; border: 2px solid #fff; border-right-color: #404040; border-bottom-color: #404040;
            padding: 15px; width: 700px; max-width: 90vw; display: flex; flex-direction: column; gap: 15px; box-shadow: 5px 5px 0 rgba(0,0,0,0.3);
        }
        .control-row { display: flex; gap: 10px; flex-wrap: wrap; justify-content: space-between; }
        input[type="text"] { flex: 2; background: #fff; border: 2px solid #404040; border-right-color: #fff; border-bottom-color: #fff; padding: 8px; font-family: 'Courier New', monospace; font-weight: bold; outline: none; font-size: 18px; }
        .retro-btn { background: #c0c0c0; border: 2px solid #fff; border-right-color: #404040; border-bottom-color: #404040; padding: 8px 15px; cursor: pointer; font-weight: bold; font-family: 'Courier New', monospace; font-size: 12px; color: black; display: flex; align-items: center; justify-content: center; position: relative; overflow: hidden; flex:1; white-space: nowrap;}
        .retro-btn:active { border: 2px solid #404040; border-right-color: #fff; border-bottom-color: #fff; transform: translate(1px, 1px); }
        .panel-label { font-size: 12px; margin-bottom: 5px; color: #333; text-transform: uppercase; }
        #file-input { position: absolute; opacity: 0; width: 100%; height: 100%; cursor: pointer; top:0; left:0;}

    </style>
</head>
<body>

    <div class="tv-set">
        <div id="meme-canvas"></div>
        <div class="tv-logo">SONY TRINITRON</div>
    </div>

    <div id="controls">
        <div>
            <div class="panel-label">Text Generator (智能分词/多重风格)</div>
            <div class="control-row">
                <input type="text" id="text-input" placeholder="输入文字..." value="Passion 设计!!!">
                <button class="retro-btn" style="flex:0.5;" onclick="spawnSentence()">ADD TEXT</button>
            </div>
        </div>
        <div>
            <div class="panel-label">Background System</div>
            <div class="control-row">
                <button class="retro-btn" onclick="setBg('white')">⬜ White</button>
                <button class="retro-btn" onclick="setRandomRainbowBg()">🌈 Rainbow</button>
                <button class="retro-btn" onclick="setBg('win98')" style="background:#008080; color:white;">💻 Win98</button>
                <button class="retro-btn" onclick="setBg('win98-bliss')" style="background: linear-gradient(to bottom, #62c2fc, #ffffff); color:black;">🏞️ Bliss</button>
                <button class="retro-btn">📂 Upload <input type="file" id="file-input" accept="image/*"></button>
            </div>
        </div>
        <div style="margin-top:5px;">
            <button class="retro-btn" style="width: 100%; font-size: 16px;" onclick="exportMeme()">💾 SAVE TO DISK (EXPORT MEME)</button>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('meme-canvas');
        const textInput = document.getElementById('text-input');
        let floaters = [];
        const fontFamilies = ['"Comic Sans MS"', 'Impact', '"Times New Roman"', 'Arial Black', 'Papyrus', 'Courier New', 'Verdana', '"Brush Script MT"'];
        // Windows XP Bliss 壁纸的 URL (这里使用一个公共地址)
        const blissBgUrl = "https://upload.wikimedia.org/wikipedia/en/d/d2/Bliss_%28Windows_XP%29.png";

        function randomColor() { return `hsl(${Math.floor(Math.random() * 360)}, 100%, 50%)`; }

        // === 升级版：智能分词逻辑 ===
        function segmentText(text) {
            text = text.trim();
            if (!text) return [];
            // 如果包含空格，直接按空格拆分 (适用于句子)
            if (text.includes(' ')) {
                return text.split(' ').filter(w => w.length > 0);
            } else {
                // 如果没有空格
                // 检测是否为纯英文字符/数字/符号 (简单正则)
                const isEnglishWord = /^[A-Za-z0-9\!\@\#\$\%\^\&\*\(\)\-\_\=\+\[\]\{\}\;\:\'\"\,\.\<\>\/\?\|]+$/.test(text);
                if (isEnglishWord) {
                    // 如果是纯英文单词，不拆分，直接返回
                    return [text];
                } else {
                    // 如果是中文或混合，则进行随机碎片化拆分
                    const chunks = [];
                    let i = 0;
                    while (i < text.length) {
                        let remaining = text.length - i;
                        let chunkLen = Math.floor(Math.random() * Math.min(remaining, 3)) + 1;
                        chunks.push(text.substr(i, chunkLen));
                        i += chunkLen;
                    }
                    return chunks;
                }
            }
        }

        class Floater {
            constructor(text) {
                this.element = document.createElement('div');
                this.element.className = 'floater';
                this.element.innerText = text;
                this.element.style.fontFamily = fontFamilies[Math.floor(Math.random() * fontFamilies.length)];
                
                // 随机大小 (40px - 100px)
                const size = Math.floor(Math.random() * 60) + 40;
                this.element.style.fontSize = `${size}px`;
                
                // === 核心升级：随机风格生成 ===
                // 30% 的概率生成彩虹渐变字
                const isRainbow = Math.random() < 0.3;

                if (isRainbow) {
                    this.element.classList.add('rainbow-text');
                    const angle = Math.floor(Math.random() * 360);
                    // 设置彩虹渐变背景并裁切到文字
                    this.element.style.backgroundImage = `linear-gradient(${angle}deg, red, orange, yellow, green, blue, indigo, violet)`;
                    this.element.style.webkitBackgroundClip = 'text';
                    this.element.style.webkitTextFillColor = 'transparent';
                    // 彩虹字通常不加描边，保持干净
                    this.element.style.webkitTextStroke = 'none';
                } else {
                    // 纯色文字风格
                    this.element.classList.add('solid-text');
                    const mainColor = randomColor();
                    this.element.style.color = mainColor;
                    // 50% 概率描边
                    if (Math.random() > 0.5) {
                        const strokeW = Math.floor(Math.random() * 4) + 2;
                        this.element.style.webkitTextStroke = `${strokeW}px ${randomColor()}`;
                    } else {
                        this.element.style.webkitTextStroke = 'none';
                    }
                    // 新增：50% 概率添加随机投影 (仅对纯色字)
                    if (Math.random() > 0.5) {
                        const shadowColor = randomColor();
                        const offsetX = Math.floor(Math.random() * 6) - 3; // -3到3
                        const offsetY = Math.floor(Math.random() * 6) - 3;
                        this.element.style.textShadow = `${offsetX}px ${offsetY}px 0px ${shadowColor}`;
                    }
                }
                
                // === 新增：随机变形扭曲 (Skew) ===
                const rotate = Math.floor(Math.random() * 60) - 30; // 旋转
                const scaleX = 0.6 + Math.random() * 0.8; // 拉伸
                const skewX = Math.floor(Math.random() * 30) - 15; // X轴扭曲 -15到15度
                const skewY = Math.floor(Math.random() * 30) - 15; // Y轴扭曲
                
                // 应用复合变换
                this.element.style.transform = `rotate(${rotate}deg) scaleX(${scaleX}) skew(${skewX}deg, ${skewY}deg)`;

                this.element.addEventListener('click', (e) => { e.stopPropagation(); this.element.remove(); });
                canvas.appendChild(this.element);

                // 物理属性
                this.x = Math.random() * (canvas.clientWidth - 100);
                this.y = Math.random() * (canvas.clientHeight - 100);
                this.vx = (Math.random() - 0.5) * 1.5;
                this.vy = (Math.random() - 0.5) * 1.5;
            }
            update() {
                this.x += this.vx; this.y += this.vy;
                if (this.x <= 0 || this.x >= canvas.clientWidth - this.element.offsetWidth) this.vx *= -1;
                if (this.y <= 0 || this.y >= canvas.clientHeight - this.element.offsetHeight) this.vy *= -1;
                this.element.style.left = `${this.x}px`; this.element.style.top = `${this.y}px`;
            }
        }

        function spawnSentence() {
            const text = textInput.value;
            const words = segmentText(text);
            words.forEach(w => floaters.push(new Floater(w)));
            textInput.value = '';
        }

        function setRandomRainbowBg() {
            const angle = Math.floor(Math.random() * 360);
            let colors = [];
            const numColors = Math.floor(Math.random() * 4) + 3; 
            for(let i=0; i<numColors; i++) colors.push(randomColor());
            canvas.style.background = `linear-gradient(${angle}deg, ${colors.join(', ')})`;
        }

        function setBg(type) {
            if (type === 'white') canvas.style.background = '#ffffff';
            else if (type === 'win98') canvas.style.background = '#008080';
            // 新增：设置 Bliss 壁纸
            else if (type === 'win98-bliss') canvas.style.background = `url(${blissBgUrl}) center/cover no-repeat`;
        }

        document.getElementById('file-input').addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (evt) => canvas.style.background = `url(${evt.target.result}) center/cover no-repeat`;
                reader.readAsDataURL(file);
            }
        });

        function exportMeme() {
            const originalRadius = canvas.style.borderRadius;
            const originalShadow = canvas.style.boxShadow;
            const originalBorder = canvas.style.border;
            canvas.style.borderRadius = '0'; canvas.style.boxShadow = 'none'; canvas.style.border = 'none';
            html2canvas(canvas, { scale: 2 }).then(blob => {
                const link = document.createElement('a'); link.download = 'retro-passion-ultimate.png'; link.href = blob.toDataURL('image/png'); link.click();
                canvas.style.borderRadius = originalRadius; canvas.style.boxShadow = originalShadow; canvas.style.border = originalBorder;
            });
        }

        function animate() { floaters.forEach(f => f.update()); requestAnimationFrame(animate); }
        window.onload = () => { setTimeout(spawnSentence, 500); animate(); };
        textInput.addEventListener('keypress', (e) => e.key === 'Enter' && spawnSentence());

    </script>
</body>
</html>
"""

components.html(html_code, height=1000, scrolling=True)
