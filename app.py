import streamlit as st
import streamlit.components.v1 as components
import base64
import os

# === 1. Python 后端：图片处理 ===
def get_image_base64(file_path):
    """读取本地图片并转为Base64，如果文件不存在返回None"""
    if os.path.exists(file_path):
        try:
            with open(file_path, "rb") as f:
                data = f.read()
                encoded = base64.b64encode(data).decode()
                return f"data:image/jpeg;base64,{encoded}"
        except Exception: # 修复了这里的语法错误 (加了空格)
            return None
    return None

# 读取本地 bliss.jpeg
local_bliss = get_image_base64("bliss.jpeg")

# 备用链接 (Web Archive 链接，防止 Base64 太长截断代码)
fallback_url = "https://web.archive.org/web/20230206142820if_/https://upload.wikimedia.org/wikipedia/en/d/d2/Bliss_%28Windows_XP%29.png"

# 最终使用的图片地址 (优先本地，其次网络)
final_bliss_url = local_bliss if local_bliss else fallback_url

# === 2. 页面配置 ===
st.set_page_config(
    page_title="What is design?",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 隐藏默认 UI
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {padding: 0 !important;}
    </style>
""", unsafe_allow_html=True)

# === 3. 核心代码 ===
html_code = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <style>
        body {{
            margin: 0; padding: 20px; background-color: #2d1b4e;
            background-image: radial-gradient(#4a2c7a 1px, transparent 1px);
            background-size: 20px 20px; font-family: 'Courier New', Courier, monospace;
            display: flex; flex-direction: column; align-items: center; min-height: 95vh; box-sizing: border-box;
        }}

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
            /* 像素化滤镜 */
            filter: contrast(110%) brightness(105%);
            image-rendering: pixelated;
        }}
        /* 噪点层 */
        #meme-canvas::after {{
            content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background-image: url("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAQAAAAECAYAAACp8Z5+AAAAIklEQVQIW2NkQAKrVq36zwjjgzhhYWGMYAEYB8RmROaABADeOQ8CXl/xfgAAAABJRU5ErkJggg==");
            opacity: 0.1; pointer-events: none; z-index: 5; mix-blend-mode: overlay; background-size: 4px 4px;
        }}

        /* === 漂浮文字 (关键修复) === */
        .floater {{
            position: absolute; 
            white-space: nowrap; 
            cursor: grab; 
            font-weight: 900; 
            
            /* 修复裁切: 增加内边距和行高 */
            padding: 25px; 
            line-height: 1.2;
            
            /* 修复背景不显示: 强制块级显示 */
            display: inline-block;
            
            /* 修复渲染丢失: 强制 GPU 层 */
            will-change: transform, left, top;
            z-index: 10; opacity: 1; 
            
            /* 保持像素感 */
            -webkit-font-smoothing: none;
            
            transition: font-size 0.3s, color 0.3s, text-shadow 0.3s, background 0.3s;
        }}

        /* 控制面板样式 */
        #controls {{
            background-color: #c0c0c0; border: 2px solid #fff; border-right-color: #404040; border-bottom-color: #404040;
            padding: 15px; width: 700px; max-width: 90vw; display: flex; flex-direction: column; gap: 15px; box-shadow: 5px 5px 0 rgba(0,0,0,0.3);
        }}
        .control-row {{ display: flex; gap: 10px; flex-wrap: wrap; justify-content: space-between; align-items: center;}}
        input[type="text"] {{ flex: 2; background: #fff; border: 2px solid #404040; border-right-color: #fff; border-bottom-color: #fff; padding: 8px; font-family: 'Courier New', monospace; font-weight: bold; outline: none; font-size: 18px; }}
        .retro-btn {{ background: #c0c0c0; border: 2px solid #fff; border-right-color: #404040; border-bottom-color: #404040; padding: 8px 15px; cursor: pointer; font-weight: bold; font-family: 'Courier New', monospace; font-size: 12px; color: black; display: flex; align-items: center; justify-content: center; position: relative; overflow: hidden; flex:1; white-space: nowrap; height: 36px; box-sizing: border-box; }}
        .retro-btn:active {{ border: 2px solid #404040; border-right-color: #fff; border-bottom-color: #fff; transform: translate(1px, 1px); }}
        .retro-btn.danger {{ color: red; }}
        .retro-btn.action {{ color: blue; }}
        .panel-label {{ font-size: 12px; margin-bottom: 5px; color: #333; text-transform: uppercase; }}
        #file-input {{ position: absolute; opacity: 0; width: 100%; height: 100%; cursor: pointer; top:0; left:0;}}
        .footer-text {{ margin-top: 20px; font-family: 'Courier New', Courier, monospace; color: rgba(255, 255, 255, 0.6); font-size: 14px; font-weight: bold; text-shadow: 2px 2px 0 #000; letter-spacing: 1px; text-align: center; }}
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
                <button class="retro-btn" style="flex:0.5;" onclick="spawnSentence()">ADD TEXT</button>
                <button class="retro-btn action" style="flex:0.5;" onclick="restyleAll()">🔀 RE-STYLE</button>
                <button class="retro-btn danger" style="flex:0.3;" onclick="clearCanvas()">🗑️</button>
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
            constructor(text) {{
                this.element = document.createElement('div');
                this.element.className = 'floater';
                this.element.innerText = text;
                
                this.applyRandomStyle();
                this.element.addEventListener('click', (e) => {{ e.stopPropagation(); this.element.remove(); }});
                canvas.appendChild(this.element);

                // === 防重叠逻辑 ===
                const safeMargin = 60; 
                const maxAttempts = 100;
                let bestX = 0, bestY = 0;
                let overlap = true;

                for(let i=0; i<maxAttempts; i++) {{
                    const elW = this.element.offsetWidth || 100;
                    const elH = this.element.offsetHeight || 50;
                    const maxX = canvas.clientWidth - elW - safeMargin;
                    const maxY = canvas.clientHeight - elH - safeMargin;
                    
                    const rx = safeMargin + Math.random() * Math.max(0, maxX);
                    const ry = safeMargin + Math.random() * Math.max(0, maxY);
                    
                    let isClean = true;
                    const myRect = {{ l: rx, r: rx+elW, t: ry, b: ry+elH }};
                    
                    for(const f of floaters) {{
                        if(!f.element) continue;
                        const otherRect = {{
                            l: f.x,
                            r: f.x + f.element.offsetWidth,
                            t: f.y,
                            b: f.y + f.element.offsetHeight
                        }};
                        if (!(myRect.r < otherRect.l || myRect.l > otherRect.r || myRect.b < otherRect.t || myRect.t > otherRect.b)) {{
                            isClean = false;
                            break; 
                        }}
                    }}
                    if(isClean) {{
                        bestX = rx; bestY = ry;
                        overlap = false;
                        break;
                    }}
                    bestX = rx; bestY = ry;
                }}

                this.x = bestX;
                this.y = bestY;
                this.vx = (Math.random() - 0.5) * 2;
                this.vy = (Math.random() - 0.5) * 2;
            }}

            applyRandomStyle() {{
                this.element.style.fontFamily = fontFamilies[Math.floor(Math.random() * fontFamilies.length)];
                const size = Math.floor(Math.random() * 120) + 30;
                this.element.style.fontSize = `${{size}}px`;

                this.element.style.color = "";
                this.element.style.webkitTextStroke = "";
                this.element.style.textShadow = "";
                this.element.style.backgroundImage = "";
                this.element.style.backgroundColor = "transparent";
                this.element.style.webkitBackgroundClip = "";
                this.element.style.webkitTextFillColor = "";
                this.element.style.fontStyle = "normal";
                this.element.style.transform = ""; 

                const styleType = Math.floor(Math.random() * 6); 
                const color1 = randomColor();
                const color2 = randomColor();
                let transformCSS = "";

                if (styleType === 0) {{
                    // Style 0: 叠叠乐
                    this.element.style.color = "#fff";
                    this.element.style.webkitTextStroke = "2px black";
                    this.element.style.textShadow = `4px 4px 0 ${{color1}}, 8px 8px 0 ${{color2}}`;
                    this.element.style.fontWeight = "900";
                }} 
                else if (styleType === 1) {{
                     // Style 1: 3D Retro
                    this.element.style.color = color1;
                    this.element.style.textShadow = `2px 2px 0 #000, 4px 4px 0 #000, 6px 6px 0 ${{color2}}`;
                    transformCSS += " skew(-10deg)";
                }} 
                else if (styleType === 2) {{
                    // Style 2: 大描边
                    this.element.style.color = color1;
                    this.element.style.webkitTextStroke = `4px black`; 
                    this.element.style.paintOrder = "stroke fill"; 
                }} 
                else if (styleType === 3) {{
                    // Style 3: 故障风
                    this.element.style.color = "#00ff00"; 
                    this.element.style.textShadow = `-3px 0 red, 3px 0 blue`;
                    this.element.style.fontFamily = '"Courier New", monospace';
                }} 
                else if (styleType === 4) {{
                     // Style 4: 变形
                     this.element.style.color = color1;
                     const scaleX = 0.6 + Math.random() * 1.2; 
                     const scaleY = 0.6 + Math.random() * 0.8; 
                     const skew = Math.random() * 40 - 20;     
                     transformCSS += ` scale(${{scaleX}}, ${{scaleY}}) skew(${{skew}}deg)`;
                     if (Math.random()>0.5) this.element.style.webkitTextStroke = "1px black";
                }}
                else {{
                    // Style 5: 极限拉伸
                    this.element.style.color = color1;
                    let scaleX, scaleY;
                    if (Math.random() > 0.5) {{
                        scaleX = 1.5 + Math.random() * 1.5; 
                        scaleY = 0.6 + Math.random() * 0.2; 
                    }} else {{
                        scaleX = 0.4 + Math.random() * 0.3; 
                        scaleY = 1.5 + Math.random() * 1.5; 
                    }}
                    transformCSS += ` scale(${{scaleX.toFixed(2)}}, ${{scaleY.toFixed(2)}})`;
                    if (Math.random() > 0.5) this.element.style.webkitTextStroke = "1px black";
                }}

                if (!transformCSS.includes("rotate")) {{
                     const rotate = Math.floor(Math.random() * 60) - 30;
                     transformCSS += ` rotate(${{rotate}}deg)`;
                }}
                this.element.style.transform = transformCSS;
            }}
            
            update() {{
                const w = this.element.offsetWidth;
                const h = this.element.offsetHeight;
                const maxW = canvas.clientWidth;
                const maxH = canvas.clientHeight;
                
                // 边界检测
                const safe = 30; 
                this.x += this.vx; 
                this.y += this.vy;

                if (this.x <= safe) {{ this.vx = Math.abs(this.vx); this.x = safe; }} 
                else if (this.x + w >= maxW - safe) {{ this.vx = -Math.abs(this.vx); this.x = maxW - w - safe; }}

                if (this.y <= safe) {{ this.vy = Math.abs(this.vy); this.y = safe; }} 
                else if (this.y + h >= maxH - safe) {{ this.vy = -Math.abs(this.vy); this.y = maxH - h - safe; }}

                // 简单的物理碰撞检测 (反弹)
                for (const other of floaters) {{
                    if (other === this) continue;
                    
                    const dx = this.x - other.x;
                    const dy = this.y - other.y;
                    const dist = Math.sqrt(dx*dx + dy*dy);
                    
                    // 简单判定：如果距离小于两者宽度之和的一半 (近似圆)
                    const minDist = (w + other.element.offsetWidth) * 0.4; // 0.4 是个宽松系数
                    
                    if (dist < minDist) {{
                        // 交换速度
                        let tempVx = this.vx;
                        let tempVy = this.vy;
                        this.vx = other.vx;
                        this.vy = other.vy;
                        other.vx = tempVx;
                        other.vy = tempVy;
                        
                        // 稍微推开防止粘连
                        const angle = Math.atan2(dy, dx);
                        const push = 2;
                        this.x += Math.cos(angle) * push;
                        this.y += Math.sin(angle) * push;
                    }}
                }}

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
