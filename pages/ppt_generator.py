"""
AI PPT 生成器 Pro - 商业化级AI演示文稿生成平台
运行方式: streamlit run ppt_generator.py
"""

import streamlit as st
import json
import re
import os
import tempfile
from openai import OpenAI
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="SlideAI Pro - AI PPT生成器",
    page_icon="📊",
)

# ==================== 自定义CSS ====================
st.markdown("""
<style>
    /* ===== 消除顶部留白 ===== */
    header[data-testid="stHeader"] { display: none !important; }
    div[data-testid="stToolbar"] { display: none !important; }
    .block-container { padding-top: 1.5rem !important; }
    body, html { margin: 0 !important; padding: 0 !important; }

    /* ===== 全局背景 - 浅色 ===== */
    .stApp {
        background: #f7f8fc !important;
        min-height: 100vh;
    }

    /* ===== 侧边栏 ===== */
    section[data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid #e8e8ef;
    }
    section[data-testid="stSidebar"] h2 { color: #1a1a2e; }

    /* ===== 主标题 ===== */
    .main-header h1 {
        font-size: 2.8rem; font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text; margin-bottom: 0.3rem;
    }
    .main-header .subtitle {
        color: #999; font-size: 1rem; letter-spacing: 2px;
    }

    /* ===== 按钮 ===== */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important; border: none !important; border-radius: 12px !important;
        font-size: 1.1rem !important; font-weight: 700 !important;
        padding: 0.8rem 2rem !important;
        box-shadow: 0 4px 15px rgba(102,126,234,0.3) !important;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(102,126,234,0.5) !important;
    }
    .stDownloadButton > button {
        background: #ffffff !important;
        border: 1px solid #ddd !important;
        color: #333 !important; border-radius: 10px !important;
        font-weight: 600 !important;
    }
    .stDownloadButton > button:hover {
        background: #f0f0f5 !important;
        border-color: #667eea !important;
    }

    /* ===== 结果展示 ===== */
    .result-box {
        background: #ffffff;
        border: 1px solid #e8e8ef;
        border-radius: 16px; padding: 2rem; margin: 1rem 0;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    }
    .stat-card {
        background: #ffffff;
        border: 1px solid #e8e8ef;
        border-radius: 12px; padding: 1rem; text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    .stat-card .number {
        font-size: 1.8rem; font-weight: 800;
        background: linear-gradient(135deg, #667eea, #f093fb);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .stat-card .label { color: #999; font-size: 0.75rem; margin-top: 0.3rem; }

    /* ===== 隐藏默认元素 ===== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    .stExpander {
        background: #ffffff !important;
        border: 1px solid #e8e8ef !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================== 配色方案 ====================
COLOR_THEMES = {
    "商务蓝": {
        "primary": RGBColor(0x1A, 0x56, 0xDB),
        "secondary": RGBColor(0x3B, 0x82, 0xF6),
        "bg": RGBColor(0xF0, 0xF4, 0xFF),
        "text": RGBColor(0x1E, 0x29, 0x3B),
        "subtext": RGBColor(0x64, 0x74, 0x8B),
    },
    "科技紫": {
        "primary": RGBColor(0x7C, 0x3A, 0xED),
        "secondary": RGBColor(0xA7, 0x8B, 0xFA),
        "bg": RGBColor(0xF5, 0xF3, 0xFF),
        "text": RGBColor(0x1E, 0x1B, 0x4B),
        "subtext": RGBColor(0x6B, 0x72, 0x80),
    },
    "活力橙": {
        "primary": RGBColor(0xEA, 0x58, 0x0C),
        "secondary": RGBColor(0xFB, 0x92, 0x3C),
        "bg": RGBColor(0xFF, 0xF7, 0xED),
        "text": RGBColor(0x43, 0x14, 0x07),
        "subtext": RGBColor(0x78, 0x71, 0x6C),
    },
    "自然绿": {
        "primary": RGBColor(0x05, 0x96, 0x69),
        "secondary": RGBColor(0x34, 0xD3, 0x99),
        "bg": RGBColor(0xEC, 0xFD, 0xF5),
        "text": RGBColor(0x06, 0x4E, 0x3B),
        "subtext": RGBColor(0x6B, 0x72, 0x80),
    },
    "简约黑": {
        "primary": RGBColor(0x1F, 0x29, 0x37),
        "secondary": RGBColor(0x6B, 0x72, 0x80),
        "bg": RGBColor(0xF9, 0xFA, 0xFB),
        "text": RGBColor(0x11, 0x18, 0x27),
        "subtext": RGBColor(0x9C, 0xA3, 0xAF),
    },
    "玫瑰红": {
        "primary": RGBColor(0xBE, 0x18, 0x5D),
        "secondary": RGBColor(0xF4, 0x72, 0xB6),
        "bg": RGBColor(0xFD, 0xF2, 0xF8),
        "text": RGBColor(0x50, 0x07, 0x24),
        "subtext": RGBColor(0x6B, 0x72, 0x80),
    },
    "深海蓝": {
        "primary": RGBColor(0x0E, 0x74, 0x90),
        "secondary": RGBColor(0x22, 0xD3, 0xEE),
        "bg": RGBColor(0xEC, 0xFE, 0xFF),
        "text": RGBColor(0x08, 0x33, 0x44),
        "subtext": RGBColor(0x6B, 0x72, 0x80),
    },
    "暗夜金": {
        "primary": RGBColor(0xB8, 0x86, 0x0B),
        "secondary": RGBColor(0xDA, 0xA5, 0x20),
        "bg": RGBColor(0x1A, 0x1A, 0x2E),
        "text": RGBColor(0xFF, 0xD7, 0x00),
        "subtext": RGBColor(0xB0, 0xB0, 0xB0),
    },
}

# ==================== PPT 生成函数 ====================

def set_slide_bg(slide, color):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_textbox(slide, left, top, width, height, text, font_size=18,
                bold=False, color=RGBColor(0, 0, 0), alignment=PP_ALIGN.LEFT):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.alignment = alignment
    return txBox


def create_title_slide(prs, title, subtitle, theme):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, theme["primary"])
    add_textbox(slide, Inches(1), Inches(2.2), Inches(8), Inches(1.5),
                title, font_size=36, bold=True,
                color=RGBColor(0xFF, 0xFF, 0xFF), alignment=PP_ALIGN.CENTER)
    if subtitle:
        add_textbox(slide, Inches(1), Inches(3.8), Inches(8), Inches(1),
                    subtitle, font_size=18,
                    color=RGBColor(0xE0, 0xE0, 0xE0), alignment=PP_ALIGN.CENTER)
    shape = slide.shapes.add_shape(1, Inches(3), Inches(5.2), Inches(4), Pt(3))
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    shape.line.fill.background()


def create_content_slide(prs, slide_data, slide_num, total_slides, theme):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, theme["bg"])
    bar = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(10), Inches(0.08))
    bar.fill.solid()
    bar.fill.fore_color.rgb = theme["primary"]
    bar.line.fill.background()
    title = slide_data.get("title", "")
    add_textbox(slide, Inches(0.8), Inches(0.4), Inches(8.4), Inches(0.8),
                title, font_size=28, bold=True, color=theme["primary"])
    subtitle = slide_data.get("subtitle", "")
    y_start = Inches(1.5)
    if subtitle:
        add_textbox(slide, Inches(0.8), Inches(1.2), Inches(8.4), Inches(0.5),
                    subtitle, font_size=16, color=theme["subtext"])
        y_start = Inches(1.8)
    points = slide_data.get("points", [])
    for i, point in enumerate(points):
        point_text = point.get("text", str(point)) if isinstance(point, dict) else str(point)
        add_textbox(slide, Inches(0.8), y_start + Inches(i * 0.7),
                    Inches(0.4), Inches(0.5),
                    f"{i + 1}", font_size=16, bold=True,
                    color=theme["primary"], alignment=PP_ALIGN.CENTER)
        add_textbox(slide, Inches(1.3), y_start + Inches(i * 0.7),
                    Inches(7.9), Inches(0.6),
                    point_text, font_size=16, color=theme["text"])
    add_textbox(slide, Inches(8.8), Inches(7.0), Inches(1), Inches(0.4),
                f"{slide_num}/{total_slides}", font_size=10,
                color=theme["subtext"], alignment=PP_ALIGN.RIGHT)


def create_end_slide(prs, theme):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, theme["primary"])
    add_textbox(slide, Inches(1), Inches(2.5), Inches(8), Inches(1.5),
                "感谢观看", font_size=40, bold=True,
                color=RGBColor(0xFF, 0xFF, 0xFF), alignment=PP_ALIGN.CENTER)
    add_textbox(slide, Inches(1), Inches(4.0), Inches(8), Inches(0.8),
                "THANK YOU", font_size=18,
                color=RGBColor(0xCC, 0xCC, 0xCC), alignment=PP_ALIGN.CENTER)


def parse_ai_json(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    patterns = [r'```json\s*\n(.*?)\n\s*```', r'```\s*\n(.*?)\n\s*```']
    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1).strip())
            except json.JSONDecodeError:
                continue
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            pass
    return None


def generate_pptx(ppt_data, theme, output_path):
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)
    slides = ppt_data.get("slides", [])
    total = len(slides)
    create_title_slide(prs, ppt_data.get("title", ""), ppt_data.get("subtitle", ""), theme)
    for i, slide_data in enumerate(slides):
        create_content_slide(prs, slide_data, i + 1, total, theme)
    create_end_slide(prs, theme)
    prs.save(output_path)
    return output_path


# ==================== API 配置（服务端密钥） ====================
api_key = st.secrets.get("api_key", "")
api_base = st.secrets.get("api_base", "https://api.deepseek.com/v1")
model_name = st.secrets.get("model_name", "deepseek-chat")

# ==================== 主界面 ====================
st.markdown("""
<div class="main-header">
    <h1>SlideAI Pro</h1>
    <div class="subtitle">AI-POWERED PRESENTATION GENERATOR</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="stat-card"><div class="number">8</div><div class="label">配色主题</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="stat-card"><div class="number">15</div><div class="label">最大页数</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="stat-card"><div class="number">10s</div><div class="label">平均生成</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="stat-card"><div class="number">.pptx</div><div class="label">标准格式</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col_left, col_right = st.columns([2, 1])

with col_left:
    topic = st.text_input("PPT 主题", placeholder="例：人工智能发展趋势、2024年度工作总结、新产品发布方案")
    subtitle = st.text_input("副标题（可选）", placeholder="例：面向管理层的战略汇报")
    num_slides = st.slider("幻灯片数量（不含封面封底）", min_value=3, max_value=15, value=6)
    detail = st.text_area("补充说明（可选）", height=100,
                          placeholder="可以补充：目标受众、需要涵盖的要点、希望突出的内容等")

with col_right:
    st.markdown('<div style="color:#555;font-size:0.9rem;margin-bottom:0.5rem;"> 配色方案</div>', unsafe_allow_html=True)
    theme_name = st.selectbox("选择风格", list(COLOR_THEMES.keys()), label_visibility="collapsed")
    theme = COLOR_THEMES[theme_name]

    st.markdown("**预览：**")
    preview_html = '<div style="display:flex;gap:4px;margin-top:4px;">'
    for label, color in [("主色", theme["primary"]), ("辅色", theme["secondary"]),
                         ("背景", theme["bg"]), ("文字", theme["text"])]:
        hex_c = f"{color[0]:02x}{color[1]:02x}{color[2]:02x}"
        preview_html += f'<div style="width:40px;height:40px;background:#{hex_c};border-radius:6px;border:1px solid #ddd;" title="{label}"></div>'
    preview_html += '</div>'
    st.markdown(preview_html, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f'<div style="color:#999;font-size:0.85rem;">**模型：** {model_name} | **预计：** {num_slides + 2} 页</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 生成按钮
if st.button("✨ 一键生成 PPT", type="primary", use_container_width=True):
    if not api_key:
        st.error("⚠️ 系统未配置 API Key，请联系管理员")
    elif not topic.strip():
        st.warning("⚠️ 请输入PPT主题")
    else:
        with st.spinner("🤖 AI 正在构思PPT内容..."):
            try:
                client = OpenAI(api_key=api_key, base_url=api_base)

                system_prompt = """你是一位专业的PPT内容策划师。请根据用户提供的主题生成PPT内容。

你必须严格返回以下格式的JSON（不要包含任何其他文字，不要用markdown代码块包裹）：

{
  "title": "演示文稿主标题",
  "subtitle": "副标题或一句话描述",
  "slides": [
    {
      "title": "章节标题",
      "subtitle": "章节副标题（可选，可为空字符串）",
      "points": ["要点1：具体说明", "要点2：具体说明", "要点3：具体说明"]
    }
  ]
}

要求：
1. 每页3-5个要点，每个要点一句话概括（20字以内）
2. 内容逻辑清晰，层层递进
3. 标题简洁有力（10字以内）
4. 要点要有实质内容，不要空话套话
5. 只返回JSON，不要任何额外说明文字"""

                user_prompt = f"""请为以下主题生成PPT内容：

主题：{topic}
副标题：{subtitle if subtitle else '无'}
幻灯片数量：{num_slides}页
补充说明：{detail if detail else '无'}

请直接返回JSON。"""

                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=3000
                )

                raw_content = response.choices[0].message.content
                ppt_data = parse_ai_json(raw_content)

                if ppt_data is None:
                    st.error("❌ AI 返回的内容无法解析为JSON，请重试")
                    with st.expander("查看AI原始回复（调试用）"):
                        st.code(raw_content)
                else:
                    tmp_dir = tempfile.mkdtemp()
                    safe_topic = re.sub(r'[\\/:*?"<>|]', '_', topic)[:30]
                    output_path = os.path.join(tmp_dir, f"{safe_topic}.pptx")
                    generate_pptx(ppt_data, theme, output_path)

                    st.session_state["ppt_data"] = ppt_data
                    st.session_state["ppt_path"] = output_path
                    st.success("✅ PPT 生成成功！")

            except Exception as e:
                st.error(f"生成失败: {e}")

# 结果展示
if "ppt_data" in st.session_state:
    ppt_data = st.session_state["ppt_data"]
    ppt_path = st.session_state["ppt_path"]

    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.subheader("📋 内容预览")
    st.markdown(f"### {ppt_data.get('title', '')}")
    if ppt_data.get("subtitle"):
        st.caption(ppt_data["subtitle"])

    for i, slide in enumerate(ppt_data.get("slides", [])):
        with st.expander(f"第 {i + 1} 页：{slide.get('title', '')}"):
            if slide.get("subtitle"):
                st.markdown(f"*{slide['subtitle']}*")
            for j, point in enumerate(slide.get("points", [])):
                if isinstance(point, dict):
                    point = point.get("text", str(point))
                st.markdown(f"{j + 1}. {point}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    with open(ppt_path, "rb") as f:
        st.download_button(
            "📥 下载 PPT 文件 (.pptx)",
            data=f.read(),
            file_name=f"{re.sub(r'[\\/:*?\"<>|]', '_', ppt_data.get('title', 'presentation'))}.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            type="primary",
            use_container_width=True
        )

# 底部
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;color:#bbb;font-size:0.75rem;padding:1rem 0;">
SlideAI Pro v2.0 | Powered by AI | Built with Streamlit + python-pptx
</div>
""", unsafe_allow_html=True)
