import streamlit as st
import streamlit.components.v1 as components
import base64
import os

# === 1. Python 后端 ===
def get_image_base64(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, "rb") as f:
                data = f.read()
                encoded = base64.b64encode(data).decode()
                return f"data:image/jpeg;base64,{encoded}"
        except Exception:
            return None
    return None

local_bliss = get_image_base64("bliss.jpeg")
fallback_url = "https://web.archive.org/web/20230206142820if_/https://upload.wikimedia.org/wikipedia/en/d/d2/Bliss_%28Windows_XP%29.png"
final_bliss_url = local_bliss if local_bliss else fallback_url

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
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <style>
        /* === 全局重置：防止 padding 撑大宽度导致溢出 === */
        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0; padding: 20px; background-color: #2d1b4e;
            background-image: radial-gradient(#4a2c7a 1px, transparent 1px);
            background-size: 20px 20px; font-family: 'Courier New', Courier, monospace;
            display: flex; flex-direction: column; align-items: center; min-height: 95vh;
        }}

        /* === 电视机外框 === */
        .tv-set {{
            background-color: #2a2a2a; 
            padding: 20px 20px 50px 20px; /* 底部留出更多空间给 Logo */
            border-radius: 30px;
            box-shadow: inset 0 0 10px #000, 0 0 0 5px #111, 0 20px 50px rgba(0,0,0,0.6);
            border-bottom: 10px solid #1a1a1a; 
            margin-bottom: 30px; 
            position: relative;
            width: 100%; 
            max-width: 700px;
        }}
        
        /* 修复 Logo 定位：使用 width:100% + text-align:center 替代 transform，防止手机端跑偏 */
        .tv-logo {{
            position: absolute; 
            bottom: 15px; 
            left: 0; 
            width: 100%;
            text-align: center;
            color: #666; 
            font-weight: bold; 
            font-size: 12px; 
            letter-spacing: 2px; 
            text-shadow: -1px -1px 0 #000;
            pointer-events: none;
        }}

        /* === 画布 === */
        #meme-canvas {{
            position: relative; width: 100%; aspect-ratio: 4 / 3;
            background-color: #ffffff; border-radius: 40px / 10px;
            box-shadow: inset 0 0 20px rgba(0,0,0,0.5); overflow: hidden;
            border: 2px solid #000; 
            filter: contrast(125%) brightness(105%);
            image-rendering: pixelated;
        }}
        #meme-canvas::after {{
            content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background-image: url("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAQAAAAECAYAAACp8Z5+AAAAIklEQVQIW2NkQAKrVq36zwjjgzhhYWGMYAEYB8RmROaABADeOQ8CXl/xfgAAAABJRU5ErkJggg==");
            opacity: 0.25; pointer-events: none; z-index: 5; mix-blend-mode: overlay;
        }}

        /* === 漂浮文字 === */
        .floater {{
            position: absolute; 
            white-space: nowrap; 
            cursor: grab; 
            font-weight: 900; 
            padding: 25px; 
            line-height: 1.2;
            display: inline-block;
            will-change: transform; 
            z-index: 10; 
            opacity: 1; 
            -webkit-backface-visibility: hidden;
            backface-visibility: hidden;
            -webkit-perspective: 1000;
            perspective: 1000;
            -webkit-font-smoothing: none;
            transition: font-size 0.3s, color 0.3s, text-shadow 0.3s, background 0.3s;
        }}

        /* === 控制面板 === */
        #controls {{
            background-color: #c0c0c0; 
            border: 2px solid #fff; 
            border-right-color: #404040; 
            border-bottom-color: #404040;
            padding: 15px; 
            width: 100%; 
            max-width: 700px; 
            display: flex; 
            flex-direction: column; 
            gap: 15px; 
            box-shadow: 5px 5px 0 rgba(0,0,0,0.3);
        }}
        
        /* 桌面端布局：Flex */
        .control-row {{ 
            display: flex; 
            gap: 10px; 
            flex-wrap: wrap; 
            justify-content: space-between; 
            align-items: center;
        }}
        
        input[type="text"] {{ 
            flex: 2; 
            background: #fff; 
            border: 2px solid #404040; 
            border-right-color: #fff; 
            border-bottom-color: #fff; 
            padding: 8px; 
            font-family: 'Courier New', monospace; 
            font-weight: bold; 
            outline: none; 
            font-size: 18px; 
            width: 100%; /* 确保宽度 */
        }}
        
        .retro-btn {{ 
            background: #c0c0c0; 
            border: 2px solid #fff; 
            border-right-color: #404040; 
            border-bottom-color: #404040; 
            padding: 8px 15px; 
            cursor: pointer; 
            font-weight: bold; 
            font-family: 'Courier New', monospace; 
            font-size: 12px; 
            color: black; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            position: relative; 
            overflow: hidden; 
            flex: 1; 
            white-space: nowrap; 
            height: 36px; 
        }}
        .retro-btn:active {{ 
            border: 2px solid #404040; 
            border-right-color: #fff; 
            border-bottom-color: #fff; 
            transform: translate(1px, 1px); 
        }}
        .retro-btn.danger {{ color: red; }}
        .retro-btn.action {{ color: blue; }}
        .panel-label {{ font-size: 12px; margin-bottom: 5px; color: #333; text-transform: uppercase; }}
        #file-input {{ position: absolute; opacity: 0; width: 100%; height: 100%; cursor: pointer; top:0; left:0;}}
        
        .footer-text {{ 
            margin-top: 20px; 
            font-family: 'Courier New', Courier, monospace; 
            color: rgba(255, 255, 255, 0.6); 
            font-size: 14px; 
            font-weight: bold; 
            text-shadow: 2px 2px 0 #000; 
            letter-spacing: 1px; 
            text-align: center; 
            width: 100%;
        }}

        /* === 📱 手机端深度自适应 === */
        @media (max-width: 768px) {{
            body {{ padding: 10px; }}
            
            .tv-set {{ 
                padding: 15px 15px 45px 15px; /* 调整内边距 */
                border-radius: 15px; 
                margin-bottom: 15px; 
            }}
            
            .tv-logo {{
                font-size: 10px; /* 缩小 Logo 字号 */
                bottom: 12px;
            }}
            
            #meme-canvas {{ border-radius: 20px / 5px; }}
            
            #controls {{ padding: 10px; gap: 12px; }}
            
            /* 强制改为 Grid 布局，让按钮对齐更整齐 */
            .control-row {{
                display: grid !important;
                grid-template-columns: 1fr 1fr 1fr; /* 3列 */
                gap: 8px;
            }}
            
            /* 输入框强制占满第一行 */
            #textInput {{
                grid-column: 1 / -1; /* 跨越所有列 */
                margin-bottom: 5px;
                font-size: 16px; /* 防止 iOS 自动放大 */
                width: 100%;
            }}
            
            /* 按钮样式微调 */
            .retro-btn {{
                flex: none !important;
                width: 100% !important; /* 占满格子 */
                font-size: 11px;
                padding: 5px 2px;
                height: 44px; /* 增大点击区域 */
                white-space: normal; /* 允许文字换行 */
                line-height: 1.1;
                text-align: center;
            }}
        }}
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
                <input type="text" id="textInput" placeholder="Type your passion..." value="Design is My Passion !!!">
                <button class="retro-btn" onclick="spawnSentence()">ADD TEXT</button>
                <button class="retro-btn action" onclick="restyleAll()">🔀 RE-STYLE</button>
                <button class="retro-btn danger" onclick="clearCanvas()">🗑️ CLEAR</button>
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

    <div class="footer-text">© 2025 Leki's Arc Inc.</div>

    <script>
        const canvas = document.getElementById('meme-canvas');
        const textInput = document.getElementById('textInput');
        let floaters = [];
        const fontFamilies = ['"Comic Sans MS"', 'Impact', '"Times New Roman"', 'Arial Black', 'Papyrus', 'Courier New', 'Verdana', '"Brush Script MT"'];
        const blissData = "{final_bliss_url}";

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

        let rainbowClickCount = 0;
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
            constructor(text, index, total) {{
                this.element = document.createElement('div');
                this.element.className = 'floater';
                this.element.innerText = text;
                
                this.applyRandomStyle();
                this.element.addEventListener('click', (e) => {{ e.stopPropagation(); this.element.remove(); }});
                canvas.appendChild(this.element);

                const baseWidth = 700; 
                const scale = Math.max(0.4, Math.min(1, canvas.clientWidth / baseWidth));

                const safeMargin = 60 * scale; 
                const availableWidth = canvas.clientWidth - (100 * scale) - safeMargin * 2;
                const availableHeight = canvas.clientHeight - (100 * scale) - safeMargin * 2;
                
                const cols = Math.ceil(Math.sqrt(total));
                const rows = Math.ceil(total / cols);
                const col = index % cols;
                const row = Math.floor(index / cols);
                const cellWidth = availableWidth / cols;
                const cellHeight = availableHeight / rows;
                let baseX = safeMargin + col * cellWidth;
                let baseY = safeMargin + row * cellHeight;
                const jitterX = Math.random() * (cellWidth * 0.6);
                const jitterY = Math.random() * (cellHeight * 0.6);

                this.x = baseX + jitterX;
                this.y = baseY + jitterY;
                this.vx = (Math.random() - 0.5) * 0.5; 
                this.vy = (Math.random() - 0.5) * 0.5;
            }}

            applyRandomStyle() {{
                this.element.style.fontFamily = fontFamilies[Math.floor(Math.random() * fontFamilies.length)];
                
                const baseWidth = 700; 
                const scale = Math.max(0.4, Math.min(1, canvas.clientWidth / baseWidth));
                const baseMin = 30;
                const baseMax = 120;
                const size = Math.floor(Math.random() * (baseMax * scale)) + (baseMin * scale);
                this.element.style.fontSize = `${{size}}px`;
                this.element.style.padding = `${{25 * scale}}px`;

                this.element.style.color = "";
                this.element.style.webkitTextStroke = "";
                this.element.style.textShadow = "";
                this.element.style.backgroundImage = "";
                this.element.style.backgroundColor = "transparent";
                this.element.style.webkitBackgroundClip = "";
                this.element.style.webkitTextFillColor = "";
                this.element.style.fontStyle = "normal";
                this.element.style.border = "none";
                this.element.style.transform = ""; 

                const styleType = Math.floor(Math.random() * 10); 
                const color1 = randomColor();
                const color2 = randomColor();
                const color3 = randomColor();
                let transformCSS = "";

                if (styleType === 0) {{
                    this.element.style.color = "#fff";
                    this.element.style.webkitTextStroke = "2px black";
                    this.element.style.textShadow = `4px 4px 0 ${{color1}}, 8px 8px 0 ${{color2}}`;
                    this.element.style.fontWeight = "900";
                }} 
                else if (styleType === 1) {{
                    const angle = Math.floor(Math.random() * 360);
                    this.element.style.backgroundImage = `linear-gradient(${{angle}}deg, ${{color1}}, ${{color2}}, ${{color3}})`;
                    this.element.style.webkitBackgroundClip = 'text';
                    this.element.style.webkitTextFillColor = 'transparent';
                    transformCSS += ` skew(${{Math.random()*30-15}}deg)`; 
                }} 
                else if (styleType === 2) {{
                    this.element.style.color = color1;
                    this.element.style.webkitTextStroke = `4px black`; 
                    this.element.style.paintOrder = "stroke fill"; 
                }} 
                else if (styleType === 3) {{
                    this.element.style.color = "#00ff00"; 
                    this.element.style.textShadow = `-3px 0 red, 3px 0 blue`;
                    this.element.style.fontFamily = '"Courier New", monospace';
                }} 
                else if (styleType === 4) {{
                     this.element.style.color = color1;
                     const scaleX = 0.6 + Math.random() * 1.2; 
                     const scaleY = 0.6 + Math.random() * 0.8; 
                     const skew = Math.random() * 40 - 20;     
                     transformCSS += ` scale(${{scaleX}}, ${{scaleY}}) skew(${{skew}}deg)`;
                     if (Math.random()>0.5) this.element.style.webkitTextStroke = "1px black";
                }}
                else if (styleType === 5) {{
                    this.element.style.color = color1;
                    let scaleX, scaleY;
                    if (Math.random() > 0.5) {{
                        scaleX = 1.5 + Math.random() * 1.5; scaleY = 0.6 + Math.random() * 0.2; 
                    }} else {{
                        scaleX = 0.4 + Math.random() * 0.3; scaleY = 1.5 + Math.random() * 1.5; 
                    }}
                    transformCSS += ` scale(${{scaleX.toFixed(2)}}, ${{scaleY.toFixed(2)}})`;
                    if (Math.random() > 0.5) this.element.style.webkitTextStroke = "1px black";
                }}
                else if (styleType === 6) {{
                    this.element.style.color = "white";
                    this.element.style.textShadow = `0 0 5px ${{color1}}, 0 0 10px ${{color1}}, 0 0 20px ${{color1}}`;
                }}
                else if (styleType === 7) {{
                    this.element.style.color = "rgba(255,255,255,0.8)";
                    this.element.style.textShadow = `5px 5px 0px ${{color1}}, 10px 10px 0px rgba(0,0,0,0.2)`;
                    this.element.style.fontStyle = "italic";
                }}
                else if (styleType === 8) {{
                    this.element.style.color = "black";
                    this.element.style.backgroundColor = color1;
                    this.element.style.padding = `${{10 * scale}}px ${{20 * scale}}px`; 
                    transformCSS += ` rotate(${{Math.random()*10-5}}deg)`;
                }}
                else {{
                    this.element.style.color = "transparent";
                    this.element.style.webkitTextStroke = `2px ${{color1}}`;
                    this.element.style.filter = `drop-shadow(3px 3px 0px ${{color2}})`;
                }}

                if (!transformCSS.includes("rotate")) {{
                     const rotate = Math.floor(Math.random() * 60) - 30;
                     transformCSS += ` rotate(${{rotate}}deg)`;
                }}
                
                this.element.style.transform = transformCSS + " translateZ(0)";
            }}
            
            update() {{
                const w = this.element.offsetWidth;
                const h = this.element.offsetHeight;
                const maxW = canvas.clientWidth;
                const maxH = canvas.clientHeight;
                const safeBuffer = 30; 

                this.x += this.vx; 
                this.y += this.vy;

                if (this.x <= safeBuffer) {{ this.vx = Math.abs(this.vx); this.x = safeBuffer; }} 
                else if (this.x + w >= maxW - safeBuffer) {{ this.vx = -Math.abs(this.vx); this.x = maxW - w - safeBuffer; }}

                if (this.y <= safeBuffer) {{ this.vy = Math.abs(this.vy); this.y = safeBuffer; }} 
                else if (this.y + h >= maxH - safeBuffer) {{ this.vy = -Math.abs(this.vy); this.y = maxH - h - safeBuffer; }}

                for (const other of floaters) {{
                    if (other === this) continue;
                    const cx1 = this.x + w/2; const cy1 = this.y + h/2;
                    const cx2 = other.x + other.element.offsetWidth/2; const cy2 = other.y + other.element.offsetHeight/2;
                    const dx = cx1 - cx2; const dy = cy1 - cy2;
                    const minDistX = (w + other.element.offsetWidth) / 2;
                    const minDistY = (h + other.element.offsetHeight) / 2;
                    
                    if (Math.abs(dx) < minDistX && Math.abs(dy) < minDistY) {{
                        const overlapX = minDistX - Math.abs(dx);
                        const overlapY = minDistY - Math.abs(dy);
                        if (overlapX < overlapY) {{
                            const force = overlapX * 0.05; const dir = dx > 0 ? 1 : -1;
                            this.x += dir * force; this.vx += dir * 0.05;
                        }} else {{
                            const force = overlapY * 0.05; const dir = dy > 0 ? 1 : -1;
                            this.y += dir * force; this.vy += dir * 0.05;
                        }}
                    }}
                }}

                this.element.style.left = `${{this.x}}px`; 
                this.element.style.top = `${{this.y}}px`;
            }}
        }}

        function spawnSentence() {{
            const text = textInput.value;
            const words = segmentText(text);
            const total = words.length;
            words.forEach((w, i) => floaters.push(new Floater(w, i, total)));
            textInput.value = '';
        }}

        function restyleAll() {{
            floaters.forEach(f => f.applyRandomStyle());
        }}

        function clearCanvas() {{ floaters = []; canvas.innerHTML = ''; }}

        function setHighSatRainbow() {{
            let gradient;
            if (rainbowClickCount === 0) {{
                gradient = highSatGradients[0];
            }} else {{
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
        
        window.onload = () => {{ 
            setBg('bliss');
            setTimeout(spawnSentence, 500); 
            animate(); 
        }};
        
        textInput.addEventListener('keypress', (e) => e.key === 'Enter' && spawnSentence());

    </script>
</body>
</html>
"""

components.html(html_code, height=1000, scrolling=True)
