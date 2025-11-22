import streamlit as st
import streamlit.components.v1 as components

# 1. 页面基础设置
st.set_page_config(
    page_title="Passion Meme Maker",
    page_icon="🎨",
    layout="wide", # 使用宽屏模式，然后我们在 CSS 里居中
    initial_sidebar_state="collapsed"
)

# 2. 隐藏 Streamlit 自带的元素，让界面更干净
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
            max-width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

# 3. 核心 HTML/JS 代码
html_code = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <style>
        /* === 全局布局 === */
        body {
            margin: 0;
            padding: 20px;
            background-color: #f4f4f9; /* 网页背景浅灰，突出画布 */
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 90vh;
        }

        /* === 核心画布 (4:3 比例) === */
        #meme-canvas {
            position: relative;
            width: 100%;
            max-width: 800px; /* 限制最大宽度 */
            aspect-ratio: 4 / 3; /* 强制 4:3 比例 */
            background-color: #ffffff;
            background-size: cover;
            background-position: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15); /* 漂亮的阴影 */
            border: 2px solid #333;
            overflow: hidden; /* 防止文字飘出去 */
            margin-bottom: 20px;
            user-select: none;
        }

        /* === 漂浮文字 === */
        .floater {
            position: absolute;
            white-space: nowrap;
            cursor: grab;
            font-weight: 900;
            line-height: 1;
            z-index: 10;
            mix-blend-mode: multiply;
            /* 应用慢速变色动画 */
            animation: slowHueChange 10s infinite linear alternate;
        }

        .floater:active {
            cursor: grabbing;
            opacity: 0.6;
        }

        /* 定义慢速变色动画 */
        @keyframes slowHueChange {
            0% { filter: hue-rotate(0deg); }
            100% { filter: hue-rotate(60deg); } 
        }

        /* === 底部控制区 === */
        #controls {
            width: 100%;
            max-width: 800px;
            display: grid;
            grid-template-columns: 3fr 1fr 1fr 1fr; /* 布局：输入框占大头，按钮占小头 */
            gap: 10px;
            padding: 15px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            box-sizing: border-box;
        }

        /* 输入框样式 */
        input[type="text"] {
            padding: 12px;
            font-size: 16px;
            border: 2px solid #ddd;
            border-radius: 8px;
            outline: none;
            transition: border-color 0.3s;
        }
        input[type="text"]:focus {
            border-color: #6c5ce7;
        }

        /* 按钮通用样式 */
        .btn {
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            font-size: 14px;
            transition: transform 0.1s, opacity 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            position: relative;
            overflow: hidden;
            text-align: center;
            padding: 0 10px;
        }
        .btn:active { transform: scale(0.95); }
        .btn:hover { opacity: 0.9; }

        /* 各个按钮的颜色 */
        #btn-add { background-color: #6c5ce7; }
        #btn-bg { background-color: #00b894; }
        #btn-export { background-color: #fd79a8; }

        /* 文件上传的隐形 Input */
        #file-input {
            position: absolute;
            opacity: 0;
            width: 100%;
            height: 100%;
            cursor: pointer;
            left: 0;
            top: 0;
        }
        
        /* 截图时的辅助类 */
        .hide-ui { display: none !important; }

    </style>
</head>
<body>

    <div id="meme-canvas">
        </div>

    <div id="controls">
        <input type="text" id="text-input" placeholder="输入一句话 (如: Graphic Design is my passion)" value="Graphic Design is my passion">
        
        <button id="btn-add" class="btn" onclick="spawnSentence()">生成文字</button>
        
        <button id="btn-bg" class="btn">
            换背景
            <input type="file" id="file-input" accept="image/*">
        </button>
        
        <button id="btn-export" class="btn" onclick="exportMeme()">
            导出
        </button>
    </div>

    <script>
        const canvas = document.getElementById('meme-canvas');
        const textInput = document.getElementById('text-input');
        let floaters = [];

        // 经典的“丑”字体库
        const fontFamilies = [
            '"Comic Sans MS", cursive', 
            '"Impact", fantasy', 
            '"Times New Roman", serif', 
            '"Arial Black", sans-serif', 
            '"Brush Script MT", cursive', 
            '"Papyrus", fantasy',
            '"Courier New", monospace'
        ];

        // 随机颜色 (高饱和度)
        function randomColor() {
            const h = Math.floor(Math.random() * 360);
            return `hsl(${h}, 100%, 45%)`;
        }

        // 文字对象类
        class Floater {
            constructor(text) {
                this.element = document.createElement('div');
                this.element.className = 'floater';
                this.element.innerText = text;
                
                // === 样式随机化 ===
                this.element.style.fontFamily = fontFamilies[Math.floor(Math.random() * fontFamilies.length)];
                
                // 随机大小 (根据画布宽度自适应一点)
                const baseSize = canvas.clientWidth / 20; 
                const size = Math.floor(Math.random() * baseSize) + (baseSize * 0.8); 
                this.element.style.fontSize = `${size}px`;
                
                // 颜色设置 (静态初始颜色，通过 CSS 动画微调)
                const mainColor = randomColor();
                const strokeColor = randomColor();
                this.element.style.color = mainColor;
                this.element.style.webkitTextStroke = `1px ${strokeColor}`;
                
                // 随机变形
                const rotate = Math.floor(Math.random() * 60) - 30; // -30度到30度
                const scaleX = 0.8 + Math.random() * 0.5;
                this.element.style.transform = `rotate(${rotate}deg) scaleX(${scaleX})`;

                // 点击删除
                this.element.addEventListener('click', (e) => {
                    e.stopPropagation();
                    this.element.remove();
                    floaters = floaters.filter(f => f !== this);
                });

                canvas.appendChild(this.element);

                // === 物理属性 (慢速) ===
                // 初始位置随机
                this.x = Math.random() * (canvas.clientWidth - 100);
                this.y = Math.random() * (canvas.clientHeight - 50);
                
                // 速度变慢 (0.5 ~ 1.5 的速度)
                this.vx = (Math.random() - 0.5) * 2; 
                this.vy = (Math.random() - 0.5) * 2;
            }

            update() {
                this.x += this.vx;
                this.y += this.vy;

                const rect = this.element.getBoundingClientRect();
                const canvasRect = canvas.getBoundingClientRect();

                // 简化的碰撞检测 (基于 relative 坐标模拟)
                // 注意：这里为了性能和简单，我们做简单的边界反弹
                // 获取元素宽高（近似）
                const w = this.element.offsetWidth;
                const h = this.element.offsetHeight;

                // 左右碰撞
                if (this.x <= 0 || this.x + w >= canvas.clientWidth) {
                    this.vx *= -1;
                    // 修正位置防止粘在墙上
                    if (this.x <= 0) this.x = 0;
                    if (this.x + w >= canvas.clientWidth) this.x = canvas.clientWidth - w;
                }
                
                // 上下碰撞
                if (this.y <= 0 || this.y + h >= canvas.clientHeight) {
                    this.vy *= -1;
                    if (this.y <= 0) this.y = 0;
                    if (this.y + h >= canvas.clientHeight) this.y = canvas.clientHeight - h;
                }

                this.element.style.left = `${this.x}px`;
                this.element.style.top = `${this.y}px`;
            }
        }

        // === 核心逻辑：拆解句子并生成 ===
        function spawnSentence() {
            const sentence = textInput.value.trim();
            if (!sentence) return;

            // 按空格拆分，过滤空字符串
            const words = sentence.split(' ').filter(w => w.length > 0);
            
            words.forEach(word => {
                floaters.push(new Floater(word));
            });
            
            // 清空输入框以便下次输入
            textInput.value = ''; 
        }

        // 动画循环
        function animate() {
            floaters.forEach(f => f.update());
            requestAnimationFrame(animate);
        }
        animate();

        // === 换背景 ===
        document.getElementById('file-input').addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (evt) => {
                    canvas.style.backgroundImage = `url(${evt.target.result})`;
                };
                reader.readAsDataURL(file);
            }
        });

        // === 导出图片 ===
        function exportMeme() {
            // 临时隐藏边框阴影，让图片更干净 (可选)
            const originalShadow = canvas.style.boxShadow;
            canvas.style.boxShadow = 'none';
            canvas.style.border = 'none';

            html2canvas(canvas, {
                scale: 2, // 高清导出
                backgroundColor: null // 保持背景图或颜色
            }).then(blob => {
                const link = document.createElement('a');
                link.download = 'my_passion_design.png';
                link.href = blob.toDataURL('image/png');
                link.click();

                // 恢复样式
                canvas.style.boxShadow = originalShadow;
                canvas.style.border = '2px solid #333';
            });
        }

        // 回车触发生成
        textInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') spawnSentence();
        });
        
        // 初始生成一句
        window.onload = () => {
             // 延时一点点确保字体加载
             setTimeout(spawnSentence, 100);
        };

    </script>
</body>
</html>
"""

# 4. 渲染组件
# height 设置大一点，容纳画布和控制栏
components.html(html_code, height=900, scrolling=True)
