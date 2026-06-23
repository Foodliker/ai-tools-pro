"""
历史记录页面 - 查看和管理生成历史
"""

import streamlit as st
import json
import sys
import os
import tempfile
import re
from datetime import datetime

# 添加父目录到路径以导入 db_utils
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import db_utils

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="历史记录 - AI Tools Pro",
    page_icon="📋",
)

# ==================== 自定义CSS ====================
st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    div[data-testid="stToolbar"] { display: none !important; }
    .block-container { padding-top: 1.5rem !important; }
    body, html { margin: 0 !important; padding: 0 !important; }
    .stApp { background: #f7f8fc !important; min-height: 100vh; }

    .main-header h1 {
        font-size: 2.8rem; font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text; margin-bottom: 0.3rem;
    }
    .main-header .subtitle {
        color: #999; font-size: 1rem; letter-spacing: 2px;
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

    .record-card {
        background: #ffffff;
        border: 1px solid #e8e8ef;
        border-radius: 14px; padding: 1.5rem; margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        transition: box-shadow 0.2s;
    }
    .record-card:hover {
        box-shadow: 0 4px 16px rgba(102,126,234,0.1);
    }
    .record-card .rec-title {
        color: #1a1a2e; font-size: 1.1rem; font-weight: 600;
        margin-bottom: 0.3rem;
    }
    .record-card .rec-meta {
        color: #999; font-size: 0.8rem;
        margin-bottom: 0.5rem;
    }
    .record-card .rec-type {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 500;
    }
    .type-copy {
        background: #ede9fe; color: #7c3aed;
    }
    .type-ppt {
        background: #dbeafe; color: #1d4ed8;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important; border: none !important; border-radius: 12px !important;
        font-size: 1.1rem !important; font-weight: 700 !important;
        padding: 0.8rem 2rem !important;
        box-shadow: 0 4px 15px rgba(102,126,234,0.3) !important;
    }

    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .stDeployButton { visibility: hidden; }

    .stExpander {
        background: #ffffff !important;
        border: 1px solid #e8e8ef !important;
        border-radius: 10px !important;
    }

    /* ===== 移动端适配 ===== */
    @media (max-width: 768px) {
        .block-container { padding: 1rem 0.8rem !important; }
        .main-header h1 { font-size: 2rem !important; }
        .main-header .subtitle { font-size: 0.8rem; letter-spacing: 1px; }
        .stat-card .number { font-size: 1.4rem; }
        .stat-card .label { font-size: 0.65rem; }
        .stat-card { padding: 0.6rem; }
    }
</style>
""", unsafe_allow_html=True)

# ==================== 返回按钮 ====================
nav_col1, _ = st.columns([1, 5])
with nav_col1:
    if st.button("← 返回首页", key="back_home_hist"):
        st.switch_page("app.py")

# ==================== 头部 ====================
st.markdown("""
<div class="main-header">
    <h1>History</h1>
    <div class="subtitle">GENERATION HISTORY & DOWNLOADS</div>
</div>
""", unsafe_allow_html=True)

# ==================== 统计 ====================
stats = db_utils.get_stats()
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="stat-card"><div class="number">{stats["total"]}</div><div class="label">总生成次数</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="stat-card"><div class="number">{stats["copywriting"]}</div><div class="label">文案生成</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="stat-card"><div class="number">{stats["ppt"]}</div><div class="label">PPT生成</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==================== 筛选 ====================
filter_col1, filter_col2 = st.columns([1, 3])
with filter_col1:
    filter_type = st.selectbox(
        "筛选类型",
        ["全部", "文案", "PPT"],
        label_visibility="collapsed",
        format_func=lambda x: {"全部": "📋 全部记录", "文案": "✍️ 文案", "PPT": "📊 PPT"}[x]
    )

type_map = {"全部": None, "文案": "copywriting", "PPT": "ppt"}
records = db_utils.get_records(tool_type=type_map[filter_type])

if not records:
    st.markdown("""
    <div style="text-align:center;padding:4rem 0;color:#999;">
        <div style="font-size:3rem;margin-bottom:1rem;">📭</div>
        <div style="font-size:1.1rem;">暂无生成记录</div>
        <div style="font-size:0.9rem;margin-top:0.5rem;">使用工具生成文案或PPT后，记录会自动保存在这里</div>
    </div>
    """, unsafe_allow_html=True)
else:
    for record in records:
        rec_id = record["id"]
        tool_type = record["tool_type"]
        title = record["title"]
        content = record["content"]
        created_at = record["created_at"]
        extra_data = record.get("extra_data")

        # 类型标签
        if tool_type == "copywriting":
            type_class = "type-copy"
            type_label = "✍️ 文案"
            icon = "✍️"
        else:
            type_class = "type-ppt"
            type_label = "📊 PPT"
            icon = "📊"

        # 格式化时间
        try:
            dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            time_str = dt.strftime("%Y-%m-%d %H:%M")
        except (ValueError, AttributeError):
            time_str = created_at

        with st.expander(f"{icon}  {title}  —  {time_str}"):
            if tool_type == "copywriting":
                # 文案记录：显示内容 + 下载
                st.markdown(content)
                st.divider()
                dl_col1, dl_col2, _ = st.columns([1, 1, 3])
                with dl_col1:
                    st.download_button(
                        "📥 TXT",
                        data=content,
                        file_name=f"{title}.txt",
                        mime="text/plain",
                        key=f"dl_txt_{rec_id}",
                        use_container_width=True
                    )
                with dl_col2:
                    st.download_button(
                        "📥 Markdown",
                        data=f"# {title}\n\n{content}",
                        file_name=f"{title}.md",
                        mime="text/markdown",
                        key=f"dl_md_{rec_id}",
                        use_container_width=True
                    )
            else:
                # PPT记录：尝试重新生成PPT文件下载
                try:
                    ppt_data = json.loads(content)
                    # 显示内容预览
                    st.markdown(f"### {ppt_data.get('title', '')}")
                    if ppt_data.get("subtitle"):
                        st.caption(ppt_data["subtitle"])

                    for i, slide in enumerate(ppt_data.get("slides", [])):
                        st.markdown(f"**第 {i+1} 页：{slide.get('title', '')}**")
                        for point in slide.get("points", []):
                            if isinstance(point, dict):
                                picon = point.get("icon", "📌")
                                ptext = point.get("text", str(point))
                                st.markdown(f"- {picon} {ptext}")
                            else:
                                st.markdown(f"- 📌 {point}")
                        st.markdown("")

                    st.divider()

                    # 重新生成pptx文件供下载
                    extra = json.loads(extra_data) if extra_data else {}
                    theme_name = extra.get("theme", "商务蓝")

                    # 导入PPT生成函数
                    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "pages"))

                    from ppt_generator import generate_pptx, COLOR_THEMES

                    theme = COLOR_THEMES.get(theme_name, COLOR_THEMES["商务蓝"])
                    tmp_dir = tempfile.mkdtemp()
                    safe_title = re.sub(r'[\\/:*?"<>|]', '_', ppt_data.get("title", "presentation"))[:30]
                    pptx_path = os.path.join(tmp_dir, f"{safe_title}.pptx")
                    generate_pptx(ppt_data, theme, pptx_path)

                    with open(pptx_path, "rb") as f:
                        st.download_button(
                            "📥 下载 PPT 文件 (.pptx)",
                            data=f.read(),
                            file_name=f"{safe_title}.pptx",
                            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                            key=f"dl_pptx_{rec_id}",
                            type="primary",
                            use_container_width=True
                        )
                except Exception as e:
                    st.warning(f"无法重建PPT文件：{e}")
                    st.code(content[:500])

# 底部
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;color:#bbb;font-size:0.75rem;padding:1rem 0;">
AI Tools Pro v3.0 | History Manager
</div>
""", unsafe_allow_html=True)
