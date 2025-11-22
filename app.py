import streamlit as st
import streamlit.components.v1 as components

# 1. 页面配置
st.set_page_config(
    page_title="Retro Passion Maker",
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
            margin: 0;
            padding: 20px;
            /* 统一的深紫色复古背景 */
            background-color: #2d1b4e; 
            background-image: radial-gradient(#4a2c7a 1px, transparent 1px);
            background-size: 20px 20px;
            font-family: 'Courier New', Courier, monospace; /* 复古等宽字体 */
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 95vh;
            box-sizing: border-box;
        }

        /* === 2. 80年代电视机外框 === */
        .tv-set {
            background-color: #2a2a2a;
            padding: 20px 20px 40px 20px; /* 底部留宽一点给Logo或散热孔 */
            border-radius: 30px;
            box-shadow: 
                inset 0 0 10px #000, /* 内阴影 */
                0 0 0 5px #111,      /* 边框线 */
                0 20px 50px rgba(0,0,0,0.6); /* 电视机投下的阴影 */
            border-bottom: 10px solid #1a1a1a; /* 底部厚度感 */
            margin-bottom: 30px;
            position: relative;
        }
        
        /* 电视机品牌 Logo (纯装饰) */
        .tv-logo {
            position: absolute;
            bottom: 12px;
            left: 50%;
            transform: translateX(-50%);
            color: #666;
            font-weight: bold;
            font-size: 12px;
            letter-spacing: 2px;
            text-shadow: -1px -1px 0 #000;
        }

        /* === 3. 屏幕/画布 (4:3) === */
        #meme-canvas {
            position: relative;
            width: 700px; /* 基础宽度 */
            max-width: 90vw;
            aspect-ratio: 4 / 3;
            background-color: #ffffff; /* 默认背景 */
            border-radius: 40px / 10px; /* 模拟CRT屏幕的微弧度 */
            box-shadow: inset 0 0 20px rgba(0,0,0,0.5); /* 屏幕内陷感 */
            overflow: hidden;
            border: 2px solid #000;
            transition: background 0.3s;
        }

        /* === 4. 漂浮文字 === */
        .floater {
            position: absolute;
            white-space: nowrap;
            cursor: grab;
            font-weight: 900;
            line-height: 1;
            z-index: 10;
            /* 混合模式让颜色叠加更有趣 */
            mix-blend-mode: hard-light; 
            /* 慢速变色动画 */
            animation: slowFloat 10s infinite linear alternate;
        }
        
        @keyframes slowFloat {
            0% { filter: hue-rotate(0deg); }
            100% { filter: hue-rotate(90deg); }
        }

        /* === 5. 复古控制台 (Win95 风格) === */
        #controls {
            background-color: #c0c0c0; /* 经典Win95灰 */
            border-top: 2px solid #fff;
            border-left: 2px solid #fff;
            border-right: 2px solid #404040;
            border-bottom: 2px solid #404040;
            padding: 15px;
            width: 700px;
            max-width: 90vw;
            display: flex;
            flex-direction: column;
            gap: 15px;
            box-shadow: 5px 5px 0 rgba(0,0,0,0.3);
        }

        .control-row {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            justify-content: space-between;
        }

        /* 复古输入框 */
        input[type="text"] {
            flex: 2;
            background: #fff;
            border-top: 2px solid #404040;
            border-left: 2px solid #404040;
            border-right: 2px solid #fff;
            border-bottom: 2px solid #fff;
            padding: 8px;
            font-family: 'Courier New', monospace;
            font-weight: bold;
            outline: none;
            font-size: 16px;
        }

        /* 复古按钮 */
        .retro-btn {
            background: #c0c0c0;
            border-top: 2px solid #fff;
            border-left: 2px solid #fff;
            border-right: 2px solid #404040;
            border-bottom: 2px solid #404040;
            padding: 8px 15px;
            cursor: pointer;
            font-weight: bold;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            color: black;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            overflow: hidden;
        }

        .retro-btn:active {
            border-top: 2px solid #404040;
            border-left: 2px solid #404040;
            border-right: 2px solid #fff;
            border-bottom: 2px solid #fff;
            transform: translate(1px, 1px); /* 按压位移 */
        }
        
        /* 小标题 */
        .panel-label {
            font-size: 12px;
            margin-bottom: 5px;
            color: #333;
            text-transform: uppercase;
        }

        /* 隐藏的文件上传 */
        #file-input { position: absolute; opacity: 0; width: 100%; height: 100%; cursor: pointer; top:0; left:0;}

    </style>
</head>
<body>

    <div class="tv-set">
        <div id="meme-canvas">
            </div>
        <div class="tv-logo">SONY TRINITRON</div>
    </div>

    <div id="controls">
        <div>
            <div class="panel-label">Text Generator</div>
            <div class="control-row">
                <input type="text" id="text-input" placeholder="TYPE HERE..." value="GRAPHIC DESIGN IS MY PASSION">
                <button class="retro-btn" onclick="spawnSentence()">ADD TEXT</button>
            </div>
        </div>

        <div>
            <div class="panel-label">Background System</div>
            <div class="control-row">
                <button class="retro-btn" onclick="setBg('white')">⬜ Pure White</button>
                <button class="retro-btn" onclick="setBg('rainbow')">🌈 Rainbow</button>
                <button class="retro-btn" onclick="setBg('win98')" style="background:#008080; color:white;">💻 Win98</button>
                <button class="retro-btn">
                    📂 Upload Img
                    <input type="file" id="file-input" accept="image/*">
                </button>
            </div>
        </div>

        <div style="margin-top:5px;">
            <button class="retro-btn" style="width: 100%; font-size: 16px;" onclick="exportMeme()">
                💾 SAVE TO DISK (EXPORT MEME)
            </button>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('meme-canvas');
        const textInput = document.getElementById('text-input');
        let floaters = [];

        // 丑陋字体库
        const fontFamilies = ['"Comic Sans MS"', 'Impact', '"Times New Roman"', 'Arial Black', 'Papyrus', 'Courier New', 'Verdana'];

        // 生成随机颜色
        function randomColor() {
            return `hsl(${Math.floor(Math.random() * 360)}, 100%, 50%)`;
        }

        class Floater {
            constructor(text) {
                this.element = document.createElement('div');
                this.element.className = 'floater';
                this.element.innerText = text;
                
                // 1. 随机字体
                this.element.style.fontFamily = fontFamilies[Math.floor(Math.random() * fontFamilies.length)];
                
                // 2. 随机大小
                const size = Math.floor(Math.random() * 40) + 20;
                this.element.style.fontSize = `${size}px`;
                
                // === 3. 颜色与描边 (修改点：随机决定是否有描边) ===
                const mainColor = randomColor();
                this.element.style.color = mainColor;

                // 50% 的概率添加描边
                if (Math.random() > 0.5) {
                    const strokeColor = randomColor();
                    // 随机描边宽度 1px - 3px
                    const strokeW = Math.floor(Math.random() * 3) + 1; 
                    this.element.style.webkitTextStroke = `${strokeW}px ${strokeColor}`;
                } else {
                    this.element.style.webkitTextStroke = 'none';
                }
                
                // 4. 变形
                const rotate = Math.floor(Math.random() * 60) - 30;
                const scaleX = 0.5 + Math.random(); 
                this.element.style.transform = `rotate(${rotate}deg) scaleX(${scaleX})`;

                // 5. 点击删除
                this.element.addEventListener('click', (e) => {
                    e.stopPropagation();
                    this.element.remove();
                });

                canvas.appendChild(this.element);

                // 6. 位置与速度 (慢速)
                this.x = Math.random() * (canvas.clientWidth - 50);
                this.y = Math.random() * (canvas.clientHeight - 50);
                this.vx = (Math.random() - 0.5) * 1.5; // 速度慢一点
                this.vy = (Math.random() - 0.5) * 1.5;
            }

            update() {
                this.x += this.vx;
                this.y += this.vy;

                // 简单的边界碰撞
                if (this.x <= 0 || this.x >= canvas.clientWidth - this.element.offsetWidth) this.vx *= -1;
                if (this.y <= 0 || this.y >= canvas.clientHeight - this.element.offsetHeight) this.vy *= -1;

                this.element.style.left = `${this.x}px`;
                this.element.style.top = `${this.y}px`;
            }
        }

        function spawnSentence() {
            const text = textInput.value.trim();
            if(!text) return;
            // 拆分单词
            const words = text.split(' ').filter(w => w.length > 0);
            words.forEach(w => floaters.push(new Floater(w)));
            textInput.value = ''; // 清空
        }

        // 背景切换逻辑
        function setBg(type) {
            canvas.style.backgroundImage = 'none'; // 先清除图片
            if (type === 'white') {
                canvas.style.background = '#ffffff';
            } else if (type === 'rainbow') {
                canvas.style.background = 'linear-gradient(45deg, red, orange, yellow, green, blue, indigo, violet)';
            } else if (type === 'win98') {
                // 经典的 Win98 蓝绿色
                canvas.style.background = '#008080'; 
            }
        }

        // 图片上传
        document.getElementById('file-input').addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (evt) => {
                    canvas.style.background = `url(${evt.target.result}) center/cover no-repeat`;
                };
                reader.readAsDataURL(file);
            }
        });

        // 导出
        function exportMeme() {
            // 截屏时需要去除电视框的圆角和阴影，只截取内容
            const originalRadius = canvas.style.borderRadius;
            const originalShadow = canvas.style.boxShadow;
            const originalBorder = canvas.style.border;
            
            // 临时去除样式以便得到干净的矩形图片
            canvas.style.borderRadius = '0';
            canvas.style.boxShadow = 'none';
            canvas.style.border = 'none';

            html2canvas(canvas, { scale: 2 }).then(blob => {
                const link = document.createElement('a');
                link.download = 'retro-passion.png';
                link.href = blob.toDataURL('image/png');
                link.click();

                // 恢复样式
                canvas.style.borderRadius = originalRadius;
                canvas.style.boxShadow = originalShadow;
                canvas.style.border = originalBorder;
            });
        }

        function animate() {
            floaters.forEach(f => f.update());
            requestAnimationFrame(animate);
        }
        
        // 启动
        window.onload = () => {
            setTimeout(spawnSentence, 500);
            animate();
        };
        
        // 回车支持
        textInput.addEventListener('keypress', (e) => e.key === 'Enter' && spawnSentence());

    </script>
</body>
</html>
"""

components.html(html_code, height=1000, scrolling=True)
