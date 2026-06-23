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
    /* ===== 基础重置 ===== */
    header[data-testid="stHeader"] { display: none !important; }
    div[data-testid="stToolbar"] { display: none !important; }
    .block-container { padding-top: 1rem !important; padding-bottom: 0 !important; }
    body, html { margin: 0 !important; padding: 0 !important; }
    .stApp { background: #f7f8fc !important; min-height: 100vh; }

    /* ===== 全屏Hero区域 ===== */
    .hero-section {
        text-align: center;
        padding: 5rem 0 3rem;
        position: relative;
    }
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0; left: 50%;
        transform: translateX(-50%);
        width: 600px; height: 600px;
        background: radial-gradient(circle, rgba(102,126,234,0.08) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
        z-index: 0;
    }
    .hero-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea20, #764ba220);
        color: #667eea;
        font-size: 0.85rem;
        font-weight: 600;
        padding: 0.4rem 1.2rem;
        border-radius: 20px;
        border: 1px solid #667eea30;
        margin-bottom: 1.5rem;
        letter-spacing: 1px;
        position: relative;
        z-index: 1;
    }
    .hero-section h1 {
        font-size: 3.8rem;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 40%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.8rem;
        line-height: 1.1;
        position: relative;
        z-index: 1;
    }
    .hero-section .tagline {
        color: #555;
        font-size: 1.25rem;
        font-weight: 400;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 1;
    }
    .hero-section .sub-tagline {
        color: #999;
        font-size: 0.95rem;
        position: relative;
        z-index: 1;
    }

    /* ===== 统计条 ===== */
    .stats-bar {
        display: flex;
        justify-content: center;
        gap: 3rem;
        padding: 2rem 0;
        margin: 1rem 0 2rem;
    }
    .stat-item {
        text-align: center;
    }
    .stat-item .num {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .stat-item .label {
        color: #888;
        font-size: 0.8rem;
        margin-top: 0.2rem;
        letter-spacing: 0.5px;
    }

    /* ===== 工具卡片区 ===== */
    .tools-container {
        display: flex;
        justify-content: center;
        gap: 2.5rem;
        padding: 1rem 2rem;
        flex-wrap: wrap;
    }
    .tool-card {
        background: #ffffff;
        border: 1px solid #e8e8ef;
        border-radius: 20px;
        padding: 2.5rem 2rem;
        width: 340px;
        min-height: 340px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.04);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .tool-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
    }
    .tool-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 40px rgba(102,126,234,0.18);
        border-color: #667eea40;
    }
    .tool-card .icon {
        font-size: 3.5rem;
        margin-bottom: 1.2rem;
    }
    .tool-card h3 {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1a1a2e;
        margin-bottom: 0.8rem;
    }
    .tool-card .desc {
        color: #666;
        font-size: 0.9rem;
        line-height: 1.7;
        margin-bottom: 1.2rem;
    }
    .tool-card .features {
        display: flex;
        flex-wrap: wrap;
        gap: 0.4rem;
        justify-content: center;
        margin-bottom: 0.5rem;
    }
    .tool-card .feat-tag {
        display: inline-block;
        background: #f0f1ff;
        color: #667eea;
        font-size: 0.75rem;
        font-weight: 500;
        padding: 0.25rem 0.6rem;
        border-radius: 6px;
    }

    /* ===== 底部特性 ===== */
    .features-section {
        display: flex;
        justify-content: center;
        gap: 2rem;
        padding: 3rem 2rem 2rem;
        flex-wrap: wrap;
    }
    .feat-card {
        text-align: center;
        width: 180px;
    }
    .feat-card .feat-icon {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .feat-card .feat-title {
        color: #333;
        font-weight: 600;
        font-size: 0.9rem;
        margin-bottom: 0.3rem;
    }
    .feat-card .feat-desc {
        color: #999;
        font-size: 0.78rem;
        line-height: 1.4;
    }

    /* ===== 隐藏默认元素 ===== */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .stDeployButton { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ==================== Hero 区域 ====================
st.markdown("""
<div class="hero-section">
    <div class="hero-badge">AI-POWERED PLATFORM</div>
    <h1>AI Tools Pro</h1>
    <div class="tagline">智能创作平台 — 文案 & PPT 一键生成</div>
    <div class="sub-tagline">基于先进AI大模型，为你提供专业级内容创作工具</div>
</div>
""", unsafe_allow_html=True)

# ==================== 统计数据 ====================
st.markdown("""
<div class="stats-bar">
    <div class="stat-item">
        <div class="num">6</div>
        <div class="label">文案类型模板</div>
    </div>
    <div class="stat-item">
        <div class="num">8</div>
        <div class="label">PPT配色主题</div>
    </div>
    <div class="stat-item">
        <div class="num">3s</div>
        <div class="label">秒级响应</div>
    </div>
    <div class="stat-item">
        <div class="num">100%</div>
        <div class="label">AI原创内容</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== 工具卡片（居中） ====================
st.markdown("""
<div style="text-align:center;margin-bottom:1.5rem;">
    <span style="color:#555;font-size:1.1rem;font-weight:600;">选择工具开始创作</span>
</div>
""", unsafe_allow_html=True)

# 用空列实现居中: spacer | card1 | card2 | spacer
spacer1, col_left, col_right, spacer2 = st.columns([1, 2.2, 2.2, 1])

with col_left:
    st.markdown("""
    <div class="tool-card">
        <div class="icon">✍️</div>
        <h3>CopyAI Pro</h3>
        <div class="desc">AI 文案生成器</div>
        <div class="desc">小红书种草文、工作周报、电商描述、短视频脚本、邮件、文章大纲，一键生成专业级文案</div>
        <div class="features">
            <span class="feat-tag">小红书</span>
            <span class="feat-tag">周报</span>
            <span class="feat-tag">电商</span>
            <span class="feat-tag">短视频</span>
            <span class="feat-tag">邮件</span>
            <span class="feat-tag">大纲</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("打开文案生成器  →", use_container_width=True, type="primary"):
        st.switch_page("pages/copywriting_tool.py")

with col_right:
    st.markdown("""
    <div class="tool-card">
        <div class="icon">📊</div>
        <h3>SlideAI Pro</h3>
        <div class="desc">AI PPT 生成器</div>
        <div class="desc">输入主题即可自动生成专业演示文稿，8种精美配色主题，支持多种专业布局</div>
        <div class="features">
            <span class="feat-tag">商务蓝</span>
            <span class="feat-tag">科技紫</span>
            <span class="feat-tag">活力橙</span>
            <span class="feat-tag">自然绿</span>
            <span class="feat-tag">简约黑</span>
            <span class="feat-tag">+3</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("打开PPT生成器  →", use_container_width=True, type="primary"):
        st.switch_page("pages/ppt_generator.py")

# ==================== 底部特性 ====================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="features-section">
    <div class="feat-card">
        <div class="feat-icon">🤖</div>
        <div class="feat-title">AI 驱动</div>
        <div class="feat-desc">基于先进大语言模型<br>理解语境精准生成</div>
    </div>
    <div class="feat-card">
        <div class="feat-icon">⚡</div>
        <div class="feat-title">极速生成</div>
        <div class="feat-desc">秒级响应<br>流式输出实时呈现</div>
    </div>
    <div class="feat-card">
        <div class="feat-icon">📂</div>
        <div class="feat-title">历史管理</div>
        <div class="feat-desc">自动保存生成记录<br>随时查看下载</div>
    </div>
    <div class="feat-card">
        <div class="feat-icon">🎨</div>
        <div class="feat-title">专业模板</div>
        <div class="feat-desc">多种风格主题<br>满足不同场景</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== 底部导航 ====================
st.markdown("<br>", unsafe_allow_html=True)
nav1, nav2, nav3 = st.columns([1, 1, 1])
with nav2:
    if st.button("📋 查看历史生成记录", use_container_width=True):
        st.switch_page("pages/history.py")

# Footer
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;color:#bbb;font-size:0.75rem;padding:1rem 0;">
AI Tools Pro v3.0 | Powered by DeepSeek AI | Built with Streamlit
</div>
""", unsafe_allow_html=True)
