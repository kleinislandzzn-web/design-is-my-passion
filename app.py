import streamlit as st
import streamlit.components.v1 as components

# 1. 设置页面配置
st.set_page_config(
    page_title="Graphic Design Passion Generator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. 隐藏 Streamlit 默认的菜单和页脚，让APP看起来更沉浸
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
/* 去除默认的内边距，让画布尽量铺满 */
.block-container {
    padding-top: 0rem;
    padding-bottom: 0rem;
    padding-left: 0rem;
    padding-right: 0rem;
}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 3. 你的核心 HTML/JS 代码 (我把之前的代码压缩在这里了)
# 注意：我调整了高度 height: 100vh 以适应全屏
html_code = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: #f0f2f5;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh; 
            font-family: sans-serif;
            overflow: hidden;
        }
        .phone-frame {
            width: 100%;
            max-width: 400px; /* 限制最大宽度，在大屏上也不至于太宽 */
            height: 85vh;     /* 使用视口高度 */
            background: black;
            border-radius: 30px;
            padding: 12px; 
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
            position: relative;
            box-sizing: border-box;
        }
        #screen-container {
            width: 100%;
            height: 100%;
            background-color: #ffffff;
            background-size: cover;
            background-position: center;
            border-radius: 20px;
            position: relative;
            overflow: hidden;
        }
        .floater {
            position: absolute;
            white-space: nowrap;
            user-select: none;
            cursor: crosshair;
            font-weight: 900;
            line-height: 1;
            z-index: 10;
            mix-blend-mode: multiply;
            transition: opacity 0.2s;
        }
        .floater:hover { opacity: 0.7; }
        #control-panel {
            position: absolute;
            bottom: 10px;
            left: 50%;
            transform: translateX(-50%);
            width: 95%;
            background: rgba(255, 255, 255, 0.9);
            border: 2px solid blue;
            padding: 8px;
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
            box-shadow: 0px -5px 15px rgba(0,0,0,0.1);
            z-index: 999;
            border-radius: 15px;
            box-sizing: border-box;
        }
        .input-group { display: flex; gap: 5px; width: 100%; margin-bottom: 5px;}
        input[type="text"] { flex: 1; padding: 8px; border: 2px solid #ccc; border-radius: 5px; }
        .btn { padding: 8px 10px; font-size: 12px; font-weight: bold; border: 2px solid black; cursor: pointer; border-radius: 5px; text-align: center; flex: 1; }
        #spawnBtn { background: linear-gradient(45deg, #ff0000, #ffcc00); color: blue; }
        #screenshotBtn { background: linear-gradient(45deg, #00f260, #0575e6); color: white; }
        .file-upload-btn { background: #ddd; color: black; position: relative; overflow: hidden; display: flex; align-items: center; justify-content: center; }
        .file-upload-btn input[type="file"] { position: absolute; font-size: 100px; opacity: 0; right: 0; top: 0; cursor: pointer; }
        .hide-for-screenshot { display: none !important; }
    </style>
</head>
<body>
    <div class="phone-frame">
        <div id="screen-container"></div>
        <div id="control-panel">
            <div class="input-group">
                <input type="text" id="textInput" placeholder="输入文字..." value="My Passion">
                <button id="spawnBtn" class="btn" onclick="spawnText()">生成</button>
            </div>
            <div class="input-group">
                <label class="btn file-upload-btn">
                    换背景
                    <input type="file" id="bgUpload" accept="image/*">
                </label>
                <button id="screenshotBtn" class="btn" onclick="takeScreenshot()">📸 保存图片</button>
            </div>
        </div>
    </div>
    <script>
        const screenContainer = document.getElementById('screen-container');
        let floaters = [];
        const fontFamilies = ['"Comic Sans MS", cursive', '"Impact", fantasy', '"Times New Roman", serif', '"Arial Black", sans-serif', '"Courier New", monospace', '"Brush Script MT", cursive', '"Papyrus", fantasy'];
        function randomColor() { const h = Math.floor(Math.random() * 360); return `hsl(${h}, 100%, 50%)`; }
        
        class Floater {
            constructor(text) {
                this.isAlive = true;
                this.element = document.createElement('div');
                this.element.className = 'floater';
                this.element.innerText = text;
                this.element.style.fontFamily = fontFamilies[Math.floor(Math.random() * fontFamilies.length)];
                this.element.style.fontSize = (Math.floor(Math.random() * 40) + 20) + 'px';
                this.element.style.color = randomColor();
                this.element.style.webkitTextStroke = Math.floor(Math.random() * 3) + 'px ' + randomColor();
                const scaleX = 0.6 + Math.random() * 1.2;
                const scaleY = 0.6 + Math.random() * 1.2;
                this.element.style.transform = `rotate(${Math.floor(Math.random() * 360)}deg) scale(${scaleX}, ${scaleY})`;
                if (Math.random() > 0.5) this.element.style.textShadow = `3px 3px 0px ${randomColor()}`;
                
                this.element.addEventListener('click', (e) => { e.stopPropagation(); this.destroy(); });
                screenContainer.appendChild(this.element);
                
                const screenW = screenContainer.offsetWidth;
                const screenH = screenContainer.offsetHeight;
                this.x = Math.random() * (screenW - 50);
                this.y = Math.random() * (screenH / 2);
                this.vx = (Math.random() - 0.5) * 6;
                this.vy = (Math.random() - 0.5) * 6;
            }
            destroy() { this.isAlive = false; this.element.remove(); }
            update() {
                if (!this.isAlive) return;
                this.x += this.vx; this.y += this.vy;
                const rect = this.element.getBoundingClientRect();
                const screenRect = screenContainer.getBoundingClientRect();
                if (rect.left <= screenRect.left || rect.right >= screenRect.right) { this.vx *= -1; this.element.style.color = randomColor(); }
                if (rect.top <= screenRect.top || rect.bottom >= screenRect.bottom) { this.vy *= -1; this.element.style.color = randomColor(); }
                this.element.style.left = this.x + 'px'; this.element.style.top = this.y + 'px';
            }
        }
        function spawnText() {
            const input = document.getElementById('textInput');
            const text = input.value.trim() || "Passion";
            floaters.push(new Floater(text));
            floaters = floaters.filter(f => f.isAlive);
        }
        document.getElementById('bgUpload').addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(event) { screenContainer.style.backgroundImage = `url(${event.target.result})`; };
                reader.readAsDataURL(file);
            }
        });
        function takeScreenshot() {
            const controlPanel = document.getElementById('control-panel');
            controlPanel.classList.add('hide-for-screenshot');
            html2canvas(screenContainer, { scale: 2, backgroundColor: null }).then(canvas => {
                const link = document.createElement('a');
                link.download = 'meme.png';
                link.href = canvas.toDataURL('image/png');
                link.click();
                controlPanel.classList.remove('hide-for-screenshot');
            });
        }
        function loop() { floaters.forEach(f => f.update()); requestAnimationFrame(loop); }
        window.onload = () => {
            ["Graphic", "Design", "is my", "Passion"].forEach((txt, i) => setTimeout(() => new Floater(txt), i * 300));
            loop();
        };
        document.getElementById('textInput').addEventListener('keypress', (e) => e.key === 'Enter' && spawnText());
    </script>
</body>
</html>
"""

# 4. 渲染 HTML
# height=850 保证在大多数屏幕上能看到完整的手机框
components.html(html_code, height=850, scrolling=False)