import streamlit as st
import streamlit.components.v1 as components
import base64
import os

# === 1. Python 后端：读取本地 bliss.jpeg ===
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
html_code = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <style>
        /* === 全局样式 === */
        body {{
            margin: 0; padding: 20px; background-color: #2d1b4e;
            background-image: radial-gradient(#4a2c7a 1px, transparent 1px);
            background-size: 20px 20px; font-family: 'Courier New', Courier, monospace;
            display: flex; flex-direction: column; align-items: center; min-height: 95vh; box-sizing: border-box;
        }}

        /* === 电视机外框 === */
        .tv-set {{
            background-color: #2a2a2a; padding: 20px 20px 40px 20px; border-radius: 30px;
            box-shadow: inset 0 0 10px #000, 0 0 0 5px #111, 0 20px 50px rgba(0,0,0,0.6);
            border-bottom: 10px solid #1a1a1a; margin-bottom: 30px; position: relative;
        }}
        .tv-logo {{
            position: absolute; bottom: 12px; left: 50%; transform: translateX(-50%);
            color: #666; font-weight: bold; font-size: 12px; letter-spacing: 2px; text-shadow: -1px -1px 0 #000;
        }}

        /* === 画布 === */
        #meme-canvas {{
            position: relative; width: 700px; max-width: 90vw; aspect-ratio: 4 / 3;
            background-color: #ffffff; border-radius: 40px / 10px;
            box-shadow: inset 0 0 20px rgba(0,0,0,0.5); overflow: hidden;
            border: 2px solid #000; 
        }}
        #meme-canvas::after {{
            content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background-image: url("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAMAAAAp4XiDAAAAUVBMVEWFhYWDg4N3d3dtbW17e3t1dXV0dHR4eHh2dnZ6enp8fHx5eXl9fX1xcXF/f39wcHBzc3Nvb29TU1NEREQtLS0lJSUgICAfHx8QEBAAAAAA/wAkAAAAPnRSTlMAAQIDBAUGBwgJCgsMDQ4PEBITFBUWFxgZGhscHR4fICEiIyQmJygpKissLS4vMDEyMzQ1Njc4OTo7PD0+P0Zom6gAAAEZSURBVEjHhZKHctwwDANFaaTYRZvb/v9fN0hA4g1cOa3tK9c4FkWRokRKCgE/hJ1I8d/Zt2r58wWza3eF4H92v2m+gU+R8X+w5874D2z9F0j8C53jX+h3/IWH+Bdu+S9c418YFv+FufkXlvErbPErXN9+hU9/hX3/Fa7XW2Q1r9HXeI2u1it0/b5Ctl9B1+9/IXsE7P25QnZfIftv0M1+hWz+C9k/obcI2T2Bt98gO39B71+QnZeo9r9A7xW62+9R+xX2vEDvF+jdY7XfINsH9H4F7X+D7L4h92s0998gO19R+/+g2z/o9gH9+4LevoD+O+j/B/R+h/2+Qp7vUPN3qNl+Q+3W8x37B6jdfL9jV1G+X1H8A4x9d6nQ8oafAAAAAElFTkSuQmCC");
            opacity: 0.2; pointer-events: none; z-index: 5; mix-blend-mode: overlay;
        }}

        /* === 漂浮文字 === */
        .floater {{
            position: absolute; white-space: nowrap; cursor: grab; font-weight: 900; line-height: 1;
            z-index: 10; opacity: 1;
        }}
        /* 增加一个慢速变色动画，只对部分文字生效 */
        @keyframes hueAnim {{
            0% {{ filter: hue-rotate(0deg); }}
            100% {{ filter: hue-rotate(360deg); }}
        }}

        /* === 控制面板 === */
        #controls {{
            background-color: #c0c0c0; border: 2px solid #fff; border-right-color: #404040; border-bottom-color: #404040;
            padding: 15px; width: 700px; max-width: 90vw; display: flex; flex-direction: column; gap: 15px; box-shadow: 5px 5px 0 rgba(0,0,0,0.3);
        }}
        .control-row {{ display: flex; gap: 10px; flex-wrap: wrap; justify-content: space-between; align-items: center;}}
        
        input[type="text"] {{ flex: 2; background: #fff; border: 2px solid #404040; border-right-color: #fff; border-bottom-color: #fff; padding: 8px; font-family: 'Courier New', monospace; font-weight: bold; outline: none; font-size: 18px; }}
        
        .retro-btn {{ background: #c0c0c0; border: 2px solid #fff; border-right-color: #404040; border-bottom-color: #404040; padding: 8px 15px; cursor: pointer; font-weight: bold; font-family: 'Courier New', monospace; font-size: 12px; color: black; display: flex; align-items: center; justify-content: center; position: relative; overflow: hidden; flex:1; white-space: nowrap; height: 36px; box-sizing: border-box; }}
        .retro-btn:active {{ border: 2px solid #404040; border-right-color: #fff; border-bottom-color: #fff; transform: translate(1px, 1px); }}
        .retro-btn.danger {{ color: red; }}
        
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
            <div class="panel-label">Text Generator</div>
            <div class="control-row">
                <input type="text" id="textInput" placeholder="输入文字..." value="Design is my Passion">
                <button class="retro-btn" style="flex:0.6;" onclick="spawnSentence()">ADD TEXT</button>
                <button class="retro-btn danger" style="flex:0.4;" onclick="clearCanvas()">🗑️ CLEAR</button>
            </div>
        </div>
        <div>
            <div class="panel-label">Background System</div>
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

    <script>
        const canvas = document.getElementById('meme-canvas');
        const textInput = document.getElementById('textInput');
        let floaters = [];
        const fontFamilies = ['"Comic Sans MS"', 'Impact', '"Times New Roman"', 'Arial Black', 'Papyrus', 'Courier New', 'Verdana', '"Brush Script MT"'];
        const blissData = "{final_bliss_url}";

        // === 1. 纯高饱和渐变库 (High Saturation ONLY) ===
        // 第一个是经典全彩虹，后续是各种高饱和撞色
        const highSatGradients = [
            "linear-gradient(180deg, #FF0000, #FF7F00, #FFFF00, #00FF00, #0000FF, #4B0082, #9400D3)", // 0: 经典全彩虹 (首发必中)
            "linear-gradient(135deg, #FF0099, #493240)", // 赛博粉黑
            "linear-gradient(90deg, #00F260, #0575E6)",  // 极光绿蓝
            "linear-gradient(to right, #833ab4, #fd1d1d, #fcb045)", // Instagram 风格高饱和
            "linear-gradient(to top, #00c6ff, #0072ff)", // 宝马蓝
            "linear-gradient(45deg, #f12711, #f5af19)", // 火焰红黄
            "linear-gradient(to bottom, #cc2b5e, #753a88)", // 紫红强对比
            "linear-gradient(to right, #000000, #0f9b0f)", // 黑客帝国绿
            "linear-gradient(120deg, #e65c00, #F9D423)", // 橘子汽水
            "linear-gradient(to right, #DA22FF, #9733EE)", // 霓虹紫
            "linear-gradient(to bottom, #FF416C, #FF4B2B)"  // 警示红
        ];

        let rainbowClickCount = 0; // 计数器，用于判断是否第一次点击

        function randomColor() {{ return `hsl(${{Math.floor(Math.random() * 360)}}, 100%, 50%)`; }}

        function segmentText(text) {{
            text = text.trim();
            if (!text) return [];
            if (text.includes(' ')) return text.split(/\s+/).filter(w => w.length > 0);
            if (window.Intl && Intl.Segmenter) {{
                try {{
                    const segmenter = new Intl.Segmenter('zh-CN', {{ granularity: 'word' }});
                    return Array.from(segmenter.segment(text)).map(s => s.segment).filter(s => s.trim().length > 0);
                }} catch (e) {{ return text.split(''); }}
            }} else {{ return text.split(''); }}
        }}

        class Floater {{
            constructor(text) {{
                this.element = document.createElement('div');
                this.element.className = 'floater';
                this.element.innerText = text;
                this.element.style.fontFamily = fontFamilies[Math.floor(Math.random() * fontFamilies.length)];
                
                const size = Math.floor(Math.random() * 60) + 40;
                this.element.style.fontSize = `${{size}}px`;
                
                // === 2. 多样化字体设计 (4种随机风格) ===
                const styleType = Math.floor(Math.random() * 4); 

                if (styleType === 0) {{
                    // Style 0: [实色投影风] 纯色 + 黑色描边 + 黑色硬投影
                    this.element.style.color = randomColor();
                    this.element.style.webkitTextStroke = "2px black";
                    this.element.style.textShadow = "4px 4px 0px black";
                }} 
                else if (styleType === 1) {{
                    // Style 1: [彩虹渐变风] 文字内部渐变 + 无描边
                    const angle = Math.floor(Math.random() * 360);
                    this.element.style.backgroundImage = `linear-gradient(${{angle}}deg, red, orange, yellow, green, blue, violet)`;
                    this.element.style.webkitBackgroundClip = 'text';
                    this.element.style.webkitTextFillColor = 'transparent';
                    // 渐变字一般加点倾斜更好看
                    this.element.style.fontStyle = "italic";
                }} 
                else if (styleType === 2) {{
                    // Style 2: [撞色描边风] 纯色填充 + 粗壮的彩色描边
                    this.element.style.color = randomColor();
                    const strokeColor = randomColor();
                    this.element.style.webkitTextStroke = `3px ${{strokeColor}}`;
                    // 稍微旋转
                    this.element.style.transform = `rotate(${{Math.random()*20-10}}deg)`;
                }} 
                else {{
                    // Style 3: [轻度变形风] 纯色 + 随机拉伸/压扁
                    this.element.style.color = randomColor();
                    // 偶尔加个发光效果
                    this.element.style.textShadow = `0 0 5px ${{randomColor()}}`;
                }}

                // 通用变形逻辑 (叠加在特定风格之上)
                // 只有非Style2(因为Style2已经定义了旋转)才随机旋转
                let baseTransform = this.element.style.transform || "";
                
                // 随机 Skew (倾斜)
                const skewX = Math.floor(Math.random() * 30) - 15;
                // 随机 Scale (拉伸)
                const scaleX = 0.7 + Math.random() * 0.6; // 0.7 ~ 1.3
                
                // 组合变换
                this.element.style.transform = `${{baseTransform}} skew(${{skewX}}deg) scaleX(${{scaleX}})`;

                this.element.addEventListener('click', (e) => {{ e.stopPropagation(); this.element.remove(); }});
                canvas.appendChild(this.element);

                this.x = Math.random() * (canvas.clientWidth - 100);
                this.y = Math.random() * (canvas.clientHeight - 100);
                this.vx = (Math.random() - 0.5) * 1.5;
                this.vy = (Math.random() - 0.5) * 1.5;
            }}
            
            update() {{
                const w = this.element.offsetWidth;
                const h = this.element.offsetHeight;
                const maxW = canvas.clientWidth;
                const maxH = canvas.clientHeight;
                this.x += this.vx; this.y += this.vy;

                if (this.x <= 0) {{ this.vx = Math.abs(this.vx); this.x = 0; }} 
                else if (this.x + w >= maxW) {{ this.vx = -Math.abs(this.vx); this.x = maxW - w; }}

                if (this.y <= 0) {{ this.vy = Math.abs(this.vy); this.y = 0; }} 
                else if (this.y + h >= maxH) {{ this.vy = -Math.abs(this.vy); this.y = maxH - h; }}

                this.element.style.left = `${{this.x}}px`; 
                this.element.style.top = `${{this.y}}px`;
            }}
        }}

        function spawnSentence() {{
            const text = textInput.value;
            const words = segmentText(text);
            words.forEach(w => floaters.push(new Floater(w)));
            textInput.value = '';
        }}

        function clearCanvas() {{ floaters = []; canvas.innerHTML = ''; }}

        // === 3. 高饱和彩虹逻辑 ===
        function setHighSatRainbow() {{
            let gradient;
            if (rainbowClickCount === 0) {{
                // 第一次点击，强制使用索引 0 (全彩虹)
                gradient = highSatGradients[0];
            }} else {{
                // 之后点击，从列表中随机选 (包含全彩虹)
                gradient = highSatGradients[Math.floor(Math.random() * highSatGradients.length)];
            }}
            rainbowClickCount++;
            canvas.style.background = gradient;
            canvas.style.backgroundSize = "cover";
        }}

        function setBg(type) {{
            if (type === 'white') canvas.style.background = '#ffffff';
            else if (type === 'win98') canvas.style.background = '#008080';
            else if (type === 'bliss') {{
                canvas.style.background = `url('${{blissData}}') center/cover no-repeat`;
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
