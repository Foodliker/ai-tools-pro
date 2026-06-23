"""
AI文案生成器 Pro - 商业化级AI文案创作平台
运行方式: streamlit run copywriting_tool.py
"""

import streamlit as st
import json
import re
from openai import OpenAI

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="CopyAI Pro - AI文案生成器",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="collapsed"
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
    section[data-testid="stSidebar"] h2 { color: #1a1a2e; font-size: 1.3rem; }

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

    /* ===== 生成按钮 ===== */
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

    /* ===== 下载按钮 ===== */
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

    /* ===== 结果展示区 ===== */
    .result-box {
        background: #ffffff;
        border: 1px solid #e8e8ef;
        border-radius: 16px; padding: 2rem; margin: 1rem 0;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    }
    .result-box h3 { color: #667eea; font-size: 1.3rem; }

    /* ===== 统计卡片 ===== */
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
</style>
""", unsafe_allow_html=True)

# ==================== 文案类型定义 ====================
COPY_TYPES = {
    "小红书种草文": {
        "icon": "",
        "desc": "适合小红书平台的种草/分享类笔记",
        "fields": ["主题/产品", "关键词（逗号分隔）", "语气风格"],
        "defaults": ["", "亮点,使用感受,推荐人群", "活泼可爱"],
        "prompt_tpl": lambda topic, kw, tone: f"""请帮我写一篇小红书种草文案。
主题/产品：{topic}
关键词：{kw}
语气风格：{tone}

要求：
1. 标题要有吸引力，善用emoji，让人想点进来
2. 正文用轻松活泼的口吻，像闺蜜分享一样自然
3. 包含以下模块：
   - 🔥 开头hook（一句话抓住注意力）
   - 💡 个人使用体验/推荐理由（3-5个要点）
   - ⭐ 总结推荐（一句话种草）
   - #话题标签（5-8个热门标签）
4. 总字数300-500字
5. 适当使用emoji让文案更生动
6. 段落之间用空行分隔，排版清晰"""
    },
    "工作周报": {
        "icon": "📊",
        "desc": "自动生成格式规范的工作周报",
        "fields": ["本周完成的工作（每行一项）", "下周计划（每行一项）", "遇到的问题/需要协调的事项（可选）"],
        "defaults": ["", "", ""],
        "prompt_tpl": lambda work, plan, issues: f"""请根据以下信息生成一份专业的工作周报。

【本周完成的工作】
{work}

【下周计划】
{plan}

{"【遇到的问题/需要协调的事项】\n" + issues if issues else ""}

要求：
1. 格式规范，分为"本周工作总结"、"下周工作计划"、"问题与建议"三个部分
2. 语言专业简洁，适合发给领导
3. 每项工作用序号标注，简明扼要
4. 如果提供了问题，要给出合理的建议或解决方案
5. 开头加上"XX部门 XX周工作周报"的标题格式"""
    },
    "电商产品描述": {
        "icon": "🛒",
        "desc": "适合淘宝/京东/拼多多等平台的商品文案",
        "fields": ["产品名称", "核心卖点（逗号分隔）", "目标人群", "价格区间"],
        "defaults": ["", "材质,功能,设计", "", ""],
        "prompt_tpl": lambda name, sp, target, price: f"""请为以下产品写一份电商产品描述文案。

产品名称：{name}
核心卖点：{sp}
目标人群：{target if target else "通用人群"}
价格区间：{price if price else "中端价位"}

要求：
1. 写一个吸引眼球的产品标题（15字以内）
2. 提炼3-5个核心卖点，每个卖点用一句话展开
3. 描述使用场景（至少3个场景）
4. 写出用户痛点和产品解决方案
5. 结尾加一句促单话术
6. 总字数300-500字
7. 语言要有感染力，让人想买"""
    },
    "短视频脚本": {
        "icon": "🎬",
        "desc": "适合抖音/快手的短视频口播或剧情脚本",
        "fields": ["主题", "视频时长", "风格"],
        "defaults": ["", "60秒", "干货分享"],
        "prompt_tpl": lambda topic, duration, style: f"""请帮我写一个短视频脚本。

主题：{topic}
视频时长：{duration}
风格：{style}

要求：
1. 按时间轴分段，标注每段的画面内容和口播文案
2. 格式：
   [0-3秒] 画面描述 | 口播/字幕内容
   [3-10秒] ...
3. 开头3秒必须有强hook（悬念/冲突/反常识）
4. 中间内容节奏紧凑，信息密度高
5. 结尾有明确的行动号召（关注/点赞/评论）
6. 标注BGM风格建议
7. 适合竖屏拍摄"""
    },
    "邮件文案": {
        "icon": "📧",
        "desc": "各类商务/学术邮件的专业文案",
        "fields": ["邮件目的", "收件人身份", "语气"],
        "defaults": ["", "领导/客户/老师", "正式"],
        "prompt_tpl": lambda purpose, recipient, tone: f"""请帮我写一封邮件。

邮件目的：{purpose}
收件人身份：{recipient if recipient else "通用"}
语气：{tone}

要求：
1. 包含完整的邮件格式（称呼、正文、结尾敬语、署名占位）
2. 语言得体，符合收件人身份
3. 正文简洁明了，重点突出
4. 如果是请求类邮件，要礼貌但不卑微
5. 如果是汇报类邮件，要有条理有数据"""
    },
    "文章大纲": {
        "icon": "📝",
        "desc": "为公众号/知乎/博客等平台生成文章结构",
        "fields": ["文章主题", "目标读者", "文章类型"],
        "defaults": ["", "通用", "干货教程"],
        "prompt_tpl": lambda topic, reader, art_type: f"""请帮我生成一篇文章大纲。

文章主题：{topic}
目标读者：{reader if reader else "通用读者"}
文章类型：{art_type}

要求：
1. 提供3个备选标题（吸引眼球但不标题党）
2. 文章结构清晰，包含：
   - 引言（hook + 文章价值预告）
   - 3-5个主要章节（每章含小标题和要点）
   - 总结（核心观点回顾 + 行动建议）
3. 每个章节标注预估字数
4. 标注哪里适合插入图片/图表/案例
5. 总字数建议1500-3000字的大纲"""
    },
}

# ==================== API 配置（服务端密钥） ====================
api_key = st.secrets.get("api_key", "")
api_base = st.secrets.get("api_base", "https://api.deepseek.com/v1")
model_name = st.secrets.get("model_name", "deepseek-chat")

# ==================== 主界面 ====================

# 头部
st.markdown("""
<div class="main-header">
    <h1>CopyAI Pro</h1>
    <div class="subtitle">AI-POWERED COPYWRITING PLATFORM</div>
</div>
""", unsafe_allow_html=True)

# 统计卡片
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="stat-card"><div class="number">6</div><div class="label">文案类型</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="stat-card"><div class="number"></div><div class="label">生成次数</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="stat-card"><div class="number">3s</div><div class="label">平均生成</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="stat-card"><div class="number">100%</div><div class="label">原创内容</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 文案类型选择 - 用卡片式
st.markdown('<div style="color:#666;font-size:0.9rem;margin-bottom:0.8rem;">选择文案类型</div>', unsafe_allow_html=True)
types_list = list(COPY_TYPES.keys())
selected_type = st.selectbox(
    "选择文案类型",
    types_list,
    label_visibility="collapsed",
    format_func=lambda x: f"{COPY_TYPES[x]['icon']}  {x}"
)

st.markdown("<br>", unsafe_allow_html=True)

# 动态表单
cfg = COPY_TYPES[selected_type]
inputs = []
for i, field in enumerate(cfg["fields"]):
    val = st.text_input(field, value=cfg["defaults"][i],
                        placeholder=f"请输入{field}")
    inputs.append(val)

# 生成按钮
st.markdown("<br>", unsafe_allow_html=True)
if st.button("✨ 一键生成文案", type="primary", use_container_width=True):
    if not api_key:
        st.error("⚠️ 系统未配置 API Key，请联系管理员")
    elif not inputs[0].strip():
        st.warning(f"⚠️ 请填写「{cfg['fields'][0]}」")
    else:
        with st.spinner("AI 正在创作中..."):
            try:
                client = OpenAI(api_key=api_key, base_url=api_base)
                prompt = cfg["prompt_tpl"](*[x.strip() for x in inputs])
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system",
                         "content": "你是一位资深文案策划师，擅长各类商业文案写作。你的文案既有创意又有转化力。请直接输出文案内容，不要加多余的解释。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.8,
                    max_tokens=2000
                )
                result = response.choices[0].message.content

                # 展示结果
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.markdown(f"### {cfg['icon']} 生成结果")
                st.markdown(result)
                st.markdown('</div>', unsafe_allow_html=True)

                # 下载按钮
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        "📥 下载 TXT",
                        data=result,
                        file_name=f"{selected_type}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                with col2:
                    st.download_button(
                        "📥 下载 Markdown",
                        data=f"# {selected_type}\n\n{result}",
                        file_name=f"{selected_type}.md",
                        mime="text/markdown",
                        use_container_width=True
                    )

            except Exception as e:
                st.error(f"生成失败: {e}")

# 底部
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;color:#bbb;font-size:0.75rem;padding:1rem 0;">
CopyAI Pro v2.0 | Powered by AI | Built with Streamlit
</div>
""", unsafe_allow_html=True)
