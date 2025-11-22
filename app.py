import streamlit as st
import streamlit.components.v1 as components
import base64
import os

# === 1. Python 后端处理：图片转 Base64 ===
# 这一步是为了解决 Bliss 壁纸加载失败的问题。
# 如果你在 GitHub 仓库里放了 "bliss.jpg"，它会优先使用；否则用网络链接。
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return f"data:image/jpeg;base64,{base64.b64encode(img_file.read()).decode()}"
    return None

# 尝试读取本地 bliss.jpg，如果不存在，使用备用网络链接
local_bliss = get_base64_image("bliss.jpg")
fallback_bliss = "https://upload.wikimedia.org/wikipedia/en/d/d2/Bliss_%28Windows_XP%29.png"
# 最终使用的 Bliss 链接 (JS中使用)
bliss_url = local_bliss if local_bliss else fallback_bliss

# === 2. 页面基础设置 ===
st.set_page_config(
    page_title="Passion Meme Ultimate",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 隐藏 Streamlit 原生 UI
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {padding: 0 !important;}
    </style>
""", unsafe_allow_html=True)

# === 3. 前端核心代码 ===
# 注意：我们将 python 变量 bliss_url 注入到了 HTML 中
html_code = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <style>
        /* === 1. 整体背景 (深色复古) === */
        body {{
            margin: 0; padding: 20px; background-color: #2d1b4e;
            background-image: radial-gradient(#4a2c7a 1px, transparent 1px);
            background-size: 20px 20px; font-family: 'Courier New', Courier, monospace;
            display: flex; flex-direction: column; align-items: center; min-height: 95vh; box-sizing: border-box;
        }}

        /* === 2. 电视机外框 === */
        .tv-set {{
            background-color: #2a2a2a; padding: 20px 20px 40px 20px; border-radius: 30px;
            box-shadow: inset 0 0 10px #000, 0 0 0 5px #111, 0 20px 50px rgba(0,0,0,0.6);
            border-bottom: 10px solid #1a1a1a; margin-bottom: 30px; position: relative;
        }}
        .tv-logo {{
            position: absolute; bottom: 12px; left: 50%; transform: translateX(-50%);
            color: #666; font-weight: bold; font-size: 12px; letter-spacing: 2px; text-shadow: -1px -1px 0 #000;
        }}

        /* === 3. 画布 === */
        #meme-canvas {{
            position: relative; width: 700px; max-width: 90vw; aspect-ratio: 4 / 3;
            background-color: #ffffff; border-radius: 40px / 10px;
            box-shadow: inset 0 0 20px rgba(0,0,0,0.5); overflow: hidden;
            border: 2px solid #000; transition: background 0.5s ease;
        }}
        /* 噪点层 */
        #meme-canvas::after {{
            content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background-image: url("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAMAAAAp4XiDAAAAUVBMVEWFhYWDg4N3d3dtbW17e3t1dXV0dHR4eHh2dnZ6enp8fHx5eXl9fX1xcXF/f39wcHBzc3Nvb29TU1NEREQtLS0lJSUgICAfHx8QEBAAAAAA/wAkAAAAPnRSTlMAAQIDBAUGBwgJCgsMDQ4PEBITFBUWFxgZGhscHR4fICEiIyQmJygpKissLS4vMDEyMzQ1Njc4OTo7PD0+P0Zom6gAAAEZSURBVEjHhZKHctwwDANFaaTYRZvb/v9fN0hA4g1cOa3tK9c4FkWRokRKCgE/hJ1I8d/Zt2r58wWza3eF4H92v2m+gU+R8X+w5874D2z9F0j8C53jX+h3/IWH+Bdu+S9c418YFv+FufkXlvErbPErXN9+hU9/hX3/Fa7XW2Q1r9HXeI2u1it0/b5Ctl9B1+9/IXsE7P25QnZfIftv0M1+hWz+C9k/obcI2T2Bt98gO39B71+QnZeo9r9A7xW62+9R+xX2vEDvF+jdY7XfINsH9H4F7X+D7L4h92s0998gO19R+/+g2z/o9gH9+4LevoD+O+j/B/R+h/2+Qp7vUPN3qNl+Q+3W8x37B6jdfL9jV1G+X1H8A4x9d6nQ8oafAAAAAElFTkSuQmCC");
            opacity: 0.2; pointer-events: none; z-index: 5; mix-blend-mode: overlay;
        }}

        /* === 4. 漂浮文字 === */
        .floater {{
            position: absolute; white-space: nowrap; cursor: grab; font-weight: 900; line-height: 1;
            z-index: 10; opacity: 1;
        }}
        /* 纯色字呼吸灯 */
        .floater.solid-text {{ animation: slowHue 10s infinite linear alternate; }}
        @keyframes slowHue {{
            0% {{ filter: hue-rotate(0deg); }}
            100% {{ filter: hue-rotate(30deg); }} /* 降低变色幅度，避免变脏 */
        }}

        /* === 5. 控制面板 === */
        #controls {{
            background-color: #c0c0c0; border: 2px solid #fff; border-right-color: #404040; border-bottom-color: #404040;
            padding: 15px; width: 700px; max-width: 90vw; display: flex; flex-direction: column; gap: 15px; box-shadow: 5px 5px 0 rgba(0,0,0,0.3);
        }}
        .control-row {{ display: flex; gap: 10px; flex-wrap: wrap; justify-content: space-between; }}
        input[type="text"] {{ flex: 2; background: #fff; border: 2px solid #404040; border-right-color: #fff; border-bottom-color: #fff; padding: 8px; font-family: 'Courier New', monospace; font-weight: bold; outline: none; font-size: 18px; }}
        .retro-btn {{ background: #c0c0c0; border: 2px solid #fff; border-right-color: #404040; border-bottom-color: #404040; padding: 8px 15px; cursor: pointer; font-weight: bold; font-family: 'Courier New', monospace; font-size: 12px; color: black; display: flex; align-items: center; justify-content: center; position: relative; overflow: hidden; flex:1; white-space: nowrap;}}
        .retro-btn:active {{ border: 2px solid #404040; border-right-color: #fff; border-bottom-color: #fff; transform: translate(1px, 1px); }}
        .panel-label {{ font-size: 12px; margin-bottom: 5px; color: #333; text-transform: uppercase; }}
        #file-input {{ position: absolute; opacity: 0; width: 100%; height: 100%; cursor: pointer; top:0; left:0;}}

    </style>
</head>
<body>

    <div class="tv-set">
        <div id="meme-canvas"></div>
        <div class="tv-logo">SONY TRINITRON</div>
    </div>

    <div id="controls">
        <div>
            <div class="panel-label">Meme Text Generator</div>
            <div class="control-row">
                <input type="text" id="text-input" placeholder="输入文字..." value="我终于学会了设计!">
                <button class="retro-btn" style="flex:0.5;" onclick="spawnSentence()">ADD TEXT</button>
            </div>
        </div>
        <div>
            <div class="panel-label">Background & Style</div>
            <div class="control-row">
                <button class="retro-btn" onclick="setBg('white')">⬜ White</button>
                <button class="retro-btn" onclick="setAestheticGradient()">🌈 Gradient</button>
                <button class="retro-btn" onclick="setBg('win98')" style="background:#008080; color:white;">💻 Win98</button>
                <button class="retro-btn" onclick="setBg('win98-bliss')" style="background: linear-gradient(to bottom, #62c2fc, #ffffff); color:black;">🏞️ Bliss</button>
                <button class="retro-btn">📂 Upload <input type="file" id="file-input" accept="image/*"></button>
            </div>
        </div>
        <div style="margin-top:5px;">
            <button class="retro-btn" style="width: 100%; font-size: 16px;" onclick="exportMeme()">💾 EXPORT MEME</button>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('meme-canvas');
        const textInput = document.getElementById('text-input');
        let floaters = [];
        const fontFamilies = ['"Comic Sans MS"', 'Impact', '"Times New Roman"', 'Arial Black', 'Papyrus', 'Courier New', 'Verdana', '"Brush Script MT"'];
        
        // 注入 Python 处理好的 Bliss 壁纸链接
        const blissBgUrl = "{bliss_url}";

        function randomColor() {{ return `hsl(${{Math.floor(Math.random() * 360)}}, 100%, 50%)`; }}

        // === 修复：高端审美渐变库 (根据参考图定制) ===
        const aestheticGradients = [
            "linear-gradient(45deg, #ff9a9e 0%, #fad0c4 99%, #fad0c4 100%)", // 暖粉
            "linear-gradient(120deg, #a18cd1 0%, #fbc2eb 100%)", // 梦幻紫
            "linear-gradient(120deg, #84fab0 0%, #8fd3f4 100%)", // 清新蓝绿
            "linear-gradient(135deg, #667eea 0%, #764ba2 100%)", // 深邃蓝紫
            "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)", // 冷淡灰白
            "linear-gradient(to top, #30cfd0 0%, #330867 100%)", // 赛博朋克
            "linear-gradient(to right, #4facfe 0%, #00f2fe 100%)", // 明亮天蓝
            "linear-gradient(to right, #43e97b 0%, #38f9d7 100%)", // 极光绿
            "linear-gradient(to right, #fa709a 0%, #fee140 100%)", // 落日橙红
            "linear-gradient(to top, #a8edea 0%, #fed6e3 100%)", // 糖果色
            "linear-gradient(45deg, #ee9ca7 0%, #ffdde1 100%)",  // 玫瑰金
            "linear-gradient(to right, #b8cbb8 0%, #b8cbb8 0%, #b465da 0%, #cf6cc9 33%, #ee609c 66%, #ee609c 100%)" // 故障风
        ];

        // === 修复：智能语感分词 (Intl.Segmenter) ===
        function segmentText(text) {{
            text = text.trim();
            if (!text) return [];
            
            // 1. 检测是否为纯英文/符号句子
            const isEnglishSentence = /^[A-Za-z0-9\s\W]+$/.test(text);

            if (isEnglishSentence) {{
                // 英文按空格拆
                return text.split(/\s+/).filter(w => w.length > 0);
            }} else {{
                // 2. 中文/混合：使用浏览器原生的高级分词器
                if (window.Intl && Intl.Segmenter) {{
                    const segmenter = new Intl.Segmenter('zh-CN', {{ granularity: 'word' }});
                    const segments = segmenter.segment(text);
                    // 提取分词结果
                    return Array.from(segments).map(s => s.segment).filter(s => s.trim().length > 0);
                }} else {{
                    // 降级方案 (极少用到)
                    return text.split('');
                }}
            }}
        }}

        class Floater {{
            constructor(text) {{
                this.element = document.createElement('div');
                this.element.className = 'floater';
                this.element.innerText = text;
                this.element.style.fontFamily = fontFamilies[Math.floor(Math.random() * fontFamilies.length)];
                
                const size = Math.floor(Math.random() * 60) + 40;
                this.element.style.fontSize = `${{size}}px`;
                
                // 随机风格：彩虹字 or 纯色字
                const isRainbow = Math.random() < 0.3;

                if (isRainbow) {{
                    this.element.classList.add('rainbow-text');
                    // 文字内部的彩虹渐变
                    const angle = Math.floor(Math.random() * 360);
                    this.element.style.backgroundImage = `linear-gradient(${{angle}}deg, red, orange, yellow, green, blue, violet)`;
                    this.element.style.webkitBackgroundClip = 'text';
                    this.element.style.webkitTextFillColor = 'transparent';
                    this.element.style.webkitTextStroke = 'none';
                }} else {{
                    this.element.classList.add('solid-text');
                    const mainColor = randomColor();
                    this.element.style.color = mainColor;
                    
                    // 描边
                    if (Math.random() > 0.5) {{
                        const strokeW = Math.floor(Math.random() * 4) + 2;
                        this.element.style.webkitTextStroke = `${{strokeW}}px ${{randomColor()}}`;
                    }} else {{
                        this.element.style.webkitTextStroke = 'none';
                    }}
                    
                    // 投影
                    if (Math.random() > 0.5) {{
                        const shadowColor = randomColor();
                        const offsetX = Math.floor(Math.random() * 6) - 3;
                        const offsetY = Math.floor(Math.random() * 6) - 3;
                        this.element.style.textShadow = `${{offsetX}}px ${{offsetY}}px 0px ${{shadowColor}}`;
                    }}
                }}
                
                // 变形
                const rotate = Math.floor(Math.random() * 60) - 30;
                const scaleX = 0.8 + Math.random() * 0.5; 
                const skewX = Math.floor(Math.random() * 20) - 10; 
                this.element.style.transform = `rotate(${{rotate}}deg) scaleX(${{scaleX}}) skew(${{skewX}}deg)`;

                this.element.addEventListener('click', (e) => {{ e.stopPropagation(); this.element.remove(); }});
                canvas.appendChild(this.element);

                this.x = Math.random() * (canvas.clientWidth - 100);
                this.y = Math.random() * (canvas.clientHeight - 100);
                this.vx = (Math.random() - 0.5) * 1.5;
                this.vy = (Math.random() - 0.5) * 1.5;
            }}
            update() {{
                this.x += this.vx; this.y += this.vy;
                if (this.x <= 0 || this.x >= canvas.clientWidth - this.element.offsetWidth) this.vx *= -1;
                if (this.y <= 0 || this.y >= canvas.clientHeight - this.element.offsetHeight) this.vy *= -1;
                this.element.style.left = `${{this.x}}px`; this.element.style.top = `${{this.y}}px`;
            }}
        }}

        function spawnSentence() {{
            const text = textInput.value;
            const words = segmentText(text);
            words.forEach(w => floaters.push(new Floater(w)));
            textInput.value = '';
        }}

        // 设定美学渐变背景
        function setAestheticGradient() {{
            const randomGradient = aestheticGradients[Math.floor(Math.random() * aestheticGradients.length)];
            canvas.style.background = randomGradient;
            // 确保背景尺寸铺满
            canvas.style.backgroundSize = "cover";
        }}

        function setBg(type) {{
            if (type === 'white') canvas.style.background = '#ffffff';
            else if (type === 'win98') canvas.style.background = '#008080';
            else if (type === 'win98-bliss') {{
                canvas.style.background = `url('${{blissBgUrl}}') center/cover no-repeat`;
            }}
        }}

        document.getElementById('file-input').addEventListener('change', (e) => {{
            const file = e.target.files[0];
            if (file) {{
                const reader = new FileReader();
                reader.onload = (evt) => canvas.style.background = `url(${{evt.target.result}}) center/cover no-repeat`;
                reader.readAsDataURL(file);
            }}
        }});

        function exportMeme() {{
            const originalRadius = canvas.style.borderRadius;
            const originalShadow = canvas.style.boxShadow;
            const originalBorder = canvas.style.border;
            canvas.style.borderRadius = '0'; canvas.style.boxShadow = 'none'; canvas.style.border = 'none';
            html2canvas(canvas, {{ scale: 2 }}).then(blob => {{
                const link = document.createElement('a'); link.download = 'passion-meme.png'; link.href = blob.toDataURL('image/png'); link.click();
                canvas.style.borderRadius = originalRadius; canvas.style.boxShadow = originalShadow; canvas.style.border = originalBorder;
            }});
        }}

        function animate() {{ floaters.forEach(f => f.update()); requestAnimationFrame(animate); }}
        window.onload = () => {{ setTimeout(spawnSentence, 500); animate(); }};
        textInput.addEventListener('keypress', (e) => e.key === 'Enter' && spawnSentence());

    </script>
</body>
</html>
"""

components.html(html_code, height=1000, scrolling=True)
