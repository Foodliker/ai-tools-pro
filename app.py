"""
AI Tools Pro - AI智能创作平台
Streamlit Cloud 部署主入口
"""

import streamlit as st

st.set_page_config(
    page_title="AI Tools Pro - AI智能创作平台",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    div[data-testid="stToolbar"] { display: none !important; }
    .block-container { padding-top: 2rem !important; }
    body, html { margin: 0 !important; padding: 0 !important; }
    .stApp { background: #f7f8fc !important; min-height: 100vh; }

    .hero {
        text-align: center;
        padding: 3rem 0 2rem;
    }
    .hero h1 {
        font-size: 3rem; font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text; margin-bottom: 0.5rem;
    }
    .hero p {
        color: #888; font-size: 1.1rem; letter-spacing: 1px;
    }

    .tool-card {
        background: #ffffff;
        border: 1px solid #e8e8ef;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        transition: transform 0.2s, box-shadow 0.2s;
        cursor: pointer;
    }
    .tool-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(102,126,234,0.15);
    }
    .tool-card .icon { font-size: 3rem; margin-bottom: 1rem; }
    .tool-card h3 {
        font-size: 1.4rem; font-weight: 700; color: #1a1a2e;
        margin-bottom: 0.5rem;
    }
    .tool-card p { color: #666; font-size: 0.9rem; line-height: 1.6; }
    .tool-card .tag {
        display: inline-block;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white; font-size: 0.75rem; font-weight: 600;
        padding: 0.3rem 0.8rem; border-radius: 20px; margin-top: 1rem;
    }

    .feature-row {
        display: flex; gap: 2rem; margin-top: 2rem; flex-wrap: wrap;
    }
    .feature-item {
        flex: 1; min-width: 200px;
        background: #ffffff; border: 1px solid #e8e8ef;
        border-radius: 12px; padding: 1.5rem; text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    .feature-item .num {
        font-size: 1.5rem; font-weight: 800;
        background: linear-gradient(135deg, #667eea, #f093fb);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .feature-item .desc { color: #999; font-size: 0.8rem; margin-top: 0.3rem; }
</style>
""", unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="hero">
    <h1>AI Tools Pro</h1>
    <p>AI-POWERED CONTENT CREATION PLATFORM</p>
</div>
""", unsafe_allow_html=True)

# Stats
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="feature-item"><div class="num">6</div><div class="desc">文案类型模板</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="feature-item"><div class="num">8</div><div class="desc">PPT配色主题</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="feature-item"><div class="num">3s</div><div class="desc">秒级生成</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="feature-item"><div class="num">100%</div><div class="desc">AI原创内容</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Tool cards
st.markdown("### 选择工具开始创作")
st.markdown("<br>", unsafe_allow_html=True)

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("""
    <div class="tool-card">
        <div class="icon">✍️</div>
        <h3>AI 文案生成器</h3>
        <p>小红书种草文、工作周报、电商描述、短视频脚本、邮件、文章大纲<br>一键生成专业级文案</p>
        <span class="tag">6种文案类型</span>
    </div>
    """, unsafe_allow_html=True)
    if st.button("打开文案生成器", use_container_width=True):
        st.switch_page("pages/copywriting_tool.py")

with col_right:
    st.markdown("""
    <div class="tool-card">
        <div class="icon">📊</div>
        <h3>AI PPT 生成器</h3>
        <p>输入主题即可自动生成专业PPT<br>8种精美配色，支持15页内容</p>
        <span class="tag">一键生成.pptx</span>
    </div>
    """, unsafe_allow_html=True)
    if st.button("打开PPT生成器", use_container_width=True):
        st.switch_page("pages/ppt_generator.py")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;color:#bbb;font-size:0.75rem;padding:1rem 0;">
AI Tools Pro v2.0 | Powered by DeepSeek AI | Built with Streamlit
</div>
""", unsafe_allow_html=True)
