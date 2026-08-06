"""
海外GTM工作台 — 消费电子出海售前辅助工具
===============================================

Streamlit MVP，帮助售前工程师为消费电子品牌出海
生成产品推荐、市场进入策略和社媒内容。

运行:  streamlit run app.py
"""

import sys
sys.dont_write_bytecode = True  # prevent stale .pyc conflicts

import streamlit as st

from engine.matcher import match_products
from engine.generator import generate_solution_brief, export_to_bytesio, suggest_filename

# ═══════════════════════════════════════════════════════════════════════════
# 页面配置
# ═══════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="海外GTM工作台 — 消费电子出海",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════════════════
# 自定义 CSS（Spotify 风格浅色主题）
# ═══════════════════════════════════════════════════════════════════════════

st.markdown("""<style>
  /* ── 全局 ── */
  #root, .stApp { background: #f5f5f0; }
  .main > div { padding-top: 1.2rem; }

  /* ── 侧边栏 ── */
  section[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e8e8e3;
  }
  section[data-testid="stSidebar"] label {
    color: #6b6b6b !important;
    font-weight: 600;
    font-size: 0.8rem;
    letter-spacing: 0.3px;
  }
  section[data-testid="stSidebar"] .stSelectbox > div > div {
    background: #f5f5f0;
    border: 1px solid #d9d9d4;
    border-radius: 6px;
    color: #1a1a1a;
  }
  section[data-testid="stSidebar"] .stSelectbox > div > div:hover {
    border-color: #1DB954;
  }
  section[data-testid="stSidebar"] hr { border-color: #e8e8e3; margin: 1rem 0; }
  section[data-testid="stSidebar"] .stCaption { color: #a0a09a; font-size: 0.75rem; }
  .sidebar-header {
    font-size: 1.1rem; font-weight: 700; color: #1a1a1a;
    margin-bottom: 0.3rem; letter-spacing: -0.2px;
  }
  .sidebar-sub {
    color: #a0a09a; font-size: 0.8rem; margin-bottom: 1rem;
  }

  /* ── 标题 ── */
  .app-title {
    font-size: 1.8rem; font-weight: 700; color: #1a1a1a;
    letter-spacing: -0.5px; margin-bottom: 0.2rem;
  }
  .app-subtitle {
    color: #8c8c86; font-size: 0.9rem;
    margin-top: -0.3rem; margin-bottom: 1.2rem;
  }

  /* ── 板块标题 ── */
  .section-title {
    font-size: 1.15rem; font-weight: 700; color: #1a1a1a;
    margin-bottom: 1rem; letter-spacing: -0.2px;
    display: flex; align-items: center; gap: 0.4rem;
  }

  /* ── 卡片 ── */
  .card {
    background: #ffffff; border-radius: 10px;
    padding: 1.3rem 1.5rem; margin-bottom: 1rem;
    border: 1px solid #e8e8e3;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    transition: all 0.2s ease;
  }
  .card:hover {
    border-color: #d0d0cb; box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  }
  .card-label {
    font-size: 0.8rem; font-weight: 600; color: #8c8c86;
    text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.6rem;
  }
  .card-body { color: #333330; line-height: 1.65; font-size: 0.92rem; }
  .card-body strong { color: #1a1a1a; }
  .card-body ul { padding-left: 1.2rem; margin: 0.3rem 0 0; }
  .card-body li { margin-bottom: 0.3rem; color: #333330; line-height: 1.5; }

  /* ── 产品卡片 ── */
  .product-card {
    background: #ffffff; border-radius: 10px;
    padding: 1.2rem 1.5rem; margin-bottom: 0.75rem;
    border: 1px solid #e8e8e3;
    border-left: 3px solid #1DB954;
    min-height: 95px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    transition: all 0.2s ease;
  }
  .product-card:hover {
    border-color: #1DB954;
    box-shadow: 0 2px 10px rgba(29,185,84,0.1);
    transform: translateX(3px);
  }
  .product-name {
    font-size: 1.05rem; font-weight: 700; color: #1a1a1a;
    display: flex; align-items: center; gap: 0.5rem;
  }
  .product-category {
    display: inline-block; font-size: 0.65rem; font-weight: 700;
    background: #1DB954; color: #ffffff;
    padding: 0.15rem 0.55rem; border-radius: 20px;
    letter-spacing: 0.5px; text-transform: uppercase;
  }
  .product-desc { color: #6b6b6b; margin-top: 0.35rem; line-height: 1.5; font-size: 0.88rem; }

  /* ── 方案简报框 ── */
  .brief-box {
    background: #ffffff; border-radius: 10px;
    padding: 1.5rem; border: 1px solid #e8e8e3;
    line-height: 1.7; font-size: 0.9rem; color: #333330;
    max-height: 460px; overflow-y: auto;
  }
  .brief-box h1 { font-size: 1.2rem; color: #1a1a1a; margin-bottom: 0.5rem; }
  .brief-box h2 { font-size: 1rem; color: #1a1a1a; margin-top: 1rem; }
  .brief-box strong { color: #1a1a1a; }
  .brief-box em { color: #6b6b6b; }
  .brief-box table { width: 100%; border-collapse: collapse; margin: 0.5rem 0; }
  .brief-box th { text-align: left; color: #6b6b6b; font-weight: 600; font-size: 0.8rem; border-bottom: 1px solid #e8e8e3; padding: 0.3rem 0.5rem; }
  .brief-box td { color: #333330; border-bottom: 1px solid #e8e8e3; padding: 0.3rem 0.5rem; font-size: 0.85rem; }
  .brief-box hr { border-color: #e8e8e3; margin: 0.8rem 0; }
  .brief-box::-webkit-scrollbar { width: 6px; }
  .brief-box::-webkit-scrollbar-track { background: #f5f5f0; }
  .brief-box::-webkit-scrollbar-thumb { background: #d0d0cb; border-radius: 3px; }

  /* ── Tab ── */
  .stTabs [data-baseweb="tab-list"] {
    gap: 0; background: #ffffff; border-radius: 10px;
    padding: 4px; border: 1px solid #e8e8e3;
    margin-bottom: 1.2rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  }
  .stTabs [data-baseweb="tab"] {
    border-radius: 8px; padding: 0.5rem 1.2rem;
    font-weight: 500; font-size: 0.85rem; color: #8c8c86;
    border: none; transition: all 0.2s;
  }
  .stTabs [data-baseweb="tab"]:hover { color: #1a1a1a; background: #f5f5f0; }
  .stTabs [aria-selected="true"] { background: #1DB954 !important; color: #ffffff !important; }
  .stTabs [data-baseweb="tab-highlight"] { display: none; }
  .stTabs [data-baseweb="tab-panel"] { outline: none; }

  /* ── 按钮 ── */
  .stDownloadButton button, .stButton button {
    background: #1DB954 !important; color: #ffffff !important;
    font-weight: 700 !important; border: none !important;
    border-radius: 24px !important; padding: 0.45rem 1.5rem !important;
    font-size: 0.85rem !important; transition: all 0.2s ease !important;
    letter-spacing: 0.3px;
  }
  .stDownloadButton button:hover, .stButton button:hover {
    background: #1ed760 !important; transform: scale(1.02);
    box-shadow: 0 2px 12px rgba(29,185,84,0.3);
  }

  /* ── 下拉框 ── */
  .stSelectbox > div > div {
    background: #f5f5f0; border: 1px solid #d9d9d4;
    border-radius: 6px; color: #1a1a1a;
  }
  .stSelectbox > div > div:hover { border-color: #1DB954; }

  /* ── 文本框 ── */
  .stTextArea textarea {
    background: #ffffff; border: 1px solid #d9d9d4;
    border-radius: 8px; color: #1a1a1a; font-size: 0.88rem;
  }
  .stTextArea textarea:focus { border-color: #1DB954; box-shadow: 0 0 0 3px rgba(29,185,84,0.08); }

  /* ── 复选框 ── */
  .stCheckbox label { color: #333330 !important; font-size: 0.88rem; }
  .stCheckbox [role="checkbox"] { accent-color: #1DB954; }

  /* ── 进度条 ── */
  .stProgress > div > div > div { background: linear-gradient(90deg, #1DB954, #1ed760) !important; }
  .stProgress > div > div { background: #e8e8e3 !important; }

  /* ── 提示框 ── */
  .stAlert { background: #ffffff !important; border: 1px solid #e8e8e3 !important; border-radius: 8px !important; }

  /* ── 网格 ── */
  .card-grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 0.5rem; }
  @media (max-width: 768px) { .card-grid-2 { grid-template-columns: 1fr; } }

  /* ── 标签 Chips ── */
  .metric-chip {
    display: inline-block; background: #e8e8e3; color: #333330;
    padding: 0.25rem 0.8rem; border-radius: 20px;
    font-size: 0.82rem; font-weight: 500; margin: 0.15rem 0.3rem 0.15rem 0;
  }

  footer { display: none; }
  .app-footer {
    text-align: center; color: #c0c0ba; font-size: 0.75rem;
    padding: 1.5rem 0 0.5rem 0;
    border-top: 1px solid #e8e8e3; margin-top: 2rem;
  }
</style>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# 侧边栏 — 筛选条件
# ═══════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown('<div class="sidebar-header">📋 客户画像</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">设置筛选条件 — 所有 Tab 将实时更新</div>', unsafe_allow_html=True)

    market = st.selectbox(
        "目标市场",
        options=["北美", "欧洲", "东南亚", "中东"],
        index=0,
    )
    use_scenario = st.selectbox(
        "使用场景",
        options=["户外运动", "商务办公", "日常通勤",
                 "游戏娱乐", "旅行出差"],
        index=0,
    )
    use_case = st.selectbox(
        "核心诉求",
        options=["音质表现", "续航能力", "快充技术",
                 "便携设计", "智能互联",
                 "运动健身", "商务兼容"],
        index=0,
    )
    budget = st.selectbox(
        "预算范围",
        options=["入门", "中端", "高端"],
        index=1,
    )

    st.markdown("---")
    product_category = st.selectbox(
        "产品品类",
        options=["全部品类", "TWS 耳机", "智能手表", "充电宝",
                 "蓝牙音箱", "GaN 充电器",
                 "线缆与配件", "运动手环",
                 "平板配件"],
        index=0,
        help="联动所有 Tab：方案匹配（仅推荐该品类）、市场策略（渠道/定价）、社媒营销（帖文角度）。",
    )
    st.markdown("---")
    st.caption("调整上方筛选条件 — 所有内容将实时刷新。")


# ═══════════════════════════════════════════════════════════════════════════
# 顶部标题
# ═══════════════════════════════════════════════════════════════════════════

st.markdown(
    '<div class="app-title">⚡ 海外GTM工作台 — 消费电子出海</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="app-subtitle">'
    "产品匹配 · 市场进入策略 · 社媒营销"
    "</div>",
    unsafe_allow_html=True,
)


# ═══════════════════════════════════════════════════════════════════════════
# Tab 2 & 3 共享数据函数
# ═══════════════════════════════════════════════════════════════════════════

def _market_strategy(market: str, cat: str) -> dict:
    """返回市场概况、渠道、定价和本地化数据。"""
    chars = {
        "北美": (
            "北美消费电子市场是全球最大的市场，购买力强劲，品牌忠诚度高。"
            "Amazon 和 Best Buy 是核心线上渠道；CES 引领行业趋势。"
            "FCC/UL 认证和售后服务是准入基础。"
        ),
        "欧洲": (
            "欧洲市场注重环保合规（CE、RoHS、WEEE）和消费者权益保护。"
            "各国偏好不同：德国看重品质，法国注重设计，北欧领先可持续理念。"
            "GDPR 合规和多语言支持是标配。"
        ),
        "东南亚": (
            "东南亚是消费电子增长最快的区域，年轻人口主导、移动优先。"
            "Shopee 和 Lazada 主导电商，性价比产品走量，但泰国和马来西亚的中高端市场正在扩大。"
        ),
        "中东": (
            "中东市场偏高端，阿联酋和沙特为核心。消费者是早期采用者，偏好国际品牌和精美设计。"
            "Noon 和 Amazon AE 主导线上，高端零售在线下仍具影响力。"
        ),
    }

    channels = {
        ("北美", "TWS 耳机"): "线上 65%（Amazon、品牌官网）/ 线下 35%（Best Buy、Walmart、Target）",
        ("北美", "智能手表"): "线上 55% / 线下 45%（Best Buy、运动用品店、运营商门店）",
        ("北美", "充电宝"): "线上 75%（Amazon、品牌官网）/ 线下 25%（Best Buy、电子零售商）",
        ("北美", "蓝牙音箱"): "线上 60% / 线下 40%（Best Buy、Target、家居用品店）",
        ("北美", "GaN 充电器"): "线上 70%（Amazon、品牌官网）/ 线下 30%（Best Buy、电子零售商）",
        ("北美", "线缆与配件"): "线上 80%（Amazon、品牌官网）/ 线下 20%（Best Buy、便利店）",
        ("北美", "运动手环"): "线上 60% / 线下 40%（Best Buy、运动用品店、运营商门店）",
        ("北美", "平板配件"): "线上 65% / 线下 35%（Best Buy、Apple Store、办公用品店）",
        ("欧洲", "TWS 耳机"): "线上 60%（Amazon DE/FR/UK、品牌官网）/ 线下 40%（MediaMarkt、FNAC、Saturn）",
        ("欧洲", "智能手表"): "线上 50% / 线下 50%（MediaMarkt、运营商门店、手表专卖店）",
        ("欧洲", "充电宝"): "线上 65% / 线下 35%（MediaMarkt、电子卖场、超市）",
        ("欧洲", "蓝牙音箱"): "线上 55% / 线下 45%（MediaMarkt、Saturn、家居用品店）",
        ("欧洲", "GaN 充电器"): "线上 60% / 线下 40%（MediaMarkt、FNAC、电子卖场）",
        ("欧洲", "线缆与配件"): "线上 70% / 线下 30%（MediaMarkt、超市、便利店）",
        ("欧洲", "运动手环"): "线上 55% / 线下 45%（MediaMarkt、运动用品店、运营商）",
        ("欧洲", "平板配件"): "线上 60% / 线下 40%（MediaMarkt、FNAC、办公用品店）",
        ("东南亚", "TWS 耳机"): "线上 75%（Shopee、Lazada、TikTok Shop）/ 线下 25%（手机店、电子卖场）",
        ("东南亚", "智能手表"): "线上 65% / 线下 35%（运营商门店、手表店、百货商场）",
        ("东南亚", "充电宝"): "线上 80% / 线下 20%（手机配件店、便利店、电子卖场）",
        ("东南亚", "蓝牙音箱"): "线上 70% / 线下 30%（电子卖场、家居店、夜市）",
        ("东南亚", "GaN 充电器"): "线上 75% / 线下 25%（电子卖场、手机配件店）",
        ("东南亚", "线缆与配件"): "线上 85% / 线下 15%（手机配件店、便利店、夜市）",
        ("东南亚", "运动手环"): "线上 70% / 线下 30%（运动用品店、运营商门店、商场）",
        ("东南亚", "平板配件"): "线上 70% / 线下 30%（电子卖场、办公用品店、商场）",
        ("中东", "TWS 耳机"): "线上 55%（Amazon AE、Noon）/ 线下 45%（电子卖场、手机店、高端百货）",
        ("中东", "智能手表"): "线上 45% / 线下 55%（高端百货、手表专卖店、运营商）",
        ("中东", "充电宝"): "线上 60% / 线下 40%（电子卖场、手机配件店、机场店）",
        ("中东", "蓝牙音箱"): "线上 50% / 线下 50%（高端百货、电子卖场、家居店）",
        ("中东", "GaN 充电器"): "线上 55% / 线下 45%（电子卖场、手机店、高端零售）",
        ("中东", "线缆与配件"): "线上 65% / 线下 35%（电子卖场、手机配件店、便利店）",
        ("中东", "运动手环"): "线上 50% / 线下 50%（运动用品店、运营商、商场）",
        ("中东", "平板配件"): "线上 50% / 线下 50%（高端百货、电子卖场、办公用品店）",
    }

    pricing = {
        ("北美", "TWS 耳机"): "中高端 — ANC、音质和品牌溢价重要；舒适区 $80-$150",
        ("北美", "智能手表"): "高端 — Apple / Garmin 主导；$200-$500 区间",
        ("北美", "充电宝"): "中端 — 性价比导向，65W+ 快充可差异化；$30-$60",
        ("北美", "蓝牙音箱"): "中高端 — 音质和品牌驱动；$50-$200 跨度大",
        ("北美", "GaN 充电器"): "中端 — 参数驱动，高功率多口畅销；$30-$80",
        ("北美", "线缆与配件"): "中低端 — 价格敏感，品牌和耐用性溢价；$10-$30",
        ("北美", "运动手环"): "中端 — Fitbit 主导，健康功能为核心；$80-$150",
        ("北美", "平板配件"): "中端 — 品牌兼容性和做工质量；$30-$80",
        ("欧洲", "TWS 耳机"): "中高端 — 音质和环保包装；€70-€130（德国可更高）",
        ("欧洲", "智能手表"): "高端 — 品牌和设计驱动；€200-€450",
        ("欧洲", "充电宝"): "中端 — 安全和环保认证；€25-€50",
        ("欧洲", "蓝牙音箱"): "中高端 — 设计美学和能效等级；€50-€180",
        ("欧洲", "GaN 充电器"): "中端 — CE 强制性要求，多口快充；€25-€70",
        ("欧洲", "线缆与配件"): "中低端 — 环保材料可差异化；€8-€25",
        ("欧洲", "运动手环"): "中端 — 健康和隐私关注度高；€70-€130",
        ("欧洲", "平板配件"): "中端 — 可持续材料与设计；€25-€70",
        ("东南亚", "TWS 耳机"): "中低端 — 价格敏感；$20-$60 舒适区",
        ("东南亚", "智能手表"): "中端 — 性价比优先；$50-$150",
        ("东南亚", "充电宝"): "中低端 — 容量和价格决定；$10-$30",
        ("东南亚", "蓝牙音箱"): "中低端 — 便携性和音量；$15-$50",
        ("东南亚", "GaN 充电器"): "中端 — 快充认知度高；$15-$40",
        ("东南亚", "线缆与配件"): "低端 — 极度价格敏感；$3-$10",
        ("东南亚", "运动手环"): "中低端 — 基础功能为主；$30-$80",
        ("东南亚", "平板配件"): "中端 — 品质和价格并重；$15-$45",
        ("中东", "TWS 耳机"): "高端 — 国际旗舰；$100-$200",
        ("中东", "智能手表"): "高端 — 奢华和品牌声望；$300-$700",
        ("中东", "充电宝"): "中高端 — 优质品牌和快充；$30-$80",
        ("中东", "蓝牙音箱"): "高端 — 音质和设计；$80-$250",
        ("中东", "GaN 充电器"): "中高端 — 追求最新技术；$30-$90",
        ("中东", "线缆与配件"): "中端 — 偏好品牌产品；$10-$30",
        ("中东", "运动手环"): "中高端 — 健康意识强；$100-$200",
        ("中东", "平板配件"): "中高端 — 优质配件；$30-$80",
    }

    l10n = {
        "北美": [
            "FCC / UL 认证必备",
            "英语 + 加拿大法语产品页面和说明书",
            "美西 + 美东双仓备货（Amazon FBA）",
            "30 天无理由退换 + 1 年保修是消费者预期",
        ],
        "欧洲": [
            "CE、RoHS、WEEE、REACH 强制性要求；需指定欧盟授权代表",
            "英/法/德 包装和说明书；GDPR 隐私声明",
            "230V / Type C&F 标准；英国需独立 SKU（Type G）",
            "建议荷兰或德国设立欧洲中心仓",
        ],
        "东南亚": [
            "各国认证要求：Postel（印尼）、NBTC（泰国）、MIC（越南）",
            "与 Shopee Mall / LazMall 合作，直播带货是关键渠道",
            "热带气候要求耐热设计和安全认证",
            "强烈建议提供印尼语/泰语/越南语支持",
        ],
        "中东": [
            "ESMA（阿联酋）/ SASO-SABER（沙特）认证；伊拉克和科威特有单独规定",
            "阿拉伯语包装和说明书；尊重伊斯兰文化规范",
            "高温环境要求可靠的热设计",
            "本地经销商合作（GCC）对 B2B 至关重要",
        ],
    }

    # 渠道/定价数据按「市场 × 品类（中文标签）」索引
    # 注意：channels / pricing 字典的品类键为中文（如 "TWS 耳机"），
    # 不能转换为英文后再查找，否则永远命中不到、回退到通用兜底文案。
    key = (market, cat)

    # 「全部品类」→ 展示综合通用策略,并引导选择具体品类
    if cat == "全部品类":
        return {
            "characteristic": chars.get(market, ""),
            "channel": "线上 55% / 线下 45% — 综合各品类的通用配比。选择具体品类可查看差异化渠道策略。",
            "pricing": "中端 — 通用定位。选择具体品类可查看针对性定价建议。",
            "localisation": l10n.get(market, ["建议进行本地市场调研以确认要求。"]),
        }

    return {
        "characteristic": chars.get(market, ""),
        "channel": channels.get(key, "线上 50% / 线下 50% — 按品类优化。"),
        "pricing": pricing.get(key, "中端 — 该市场的标准定位。"),
        "localisation": l10n.get(market, ["建议进行本地市场调研以确认要求。"]),
    }


def _social_content(stage: str, market: str, category: str = "全部品类") -> dict:
    """返回阶段信息和社媒帖文草稿(内容方向与帖文按品类定制)。"""
    # 品类 → 英文卖点短语(用于英文帖文)
    category_blurbs = {
        "TWS 耳机": "studio-grade sound with adaptive ANC and all-day battery in a featherlight design",
        "智能手表": "advanced health tracking on a crystal-clear AMOLED display with 14-day battery",
        "充电宝": "high-capacity 65W fast charging that powers your laptop and phone anywhere",
        "蓝牙音箱": "360° waterproof sound engineered to power every adventure",
        "GaN 充电器": "ultra-compact GaN fast charging that powers multiple devices at once",
        "线缆与配件": "premium braided cables with 100W PD fast charging built to last",
        "运动手环": "24/7 heart-rate & SpO2 tracking in a featherlight band with 10-day battery",
        "平板配件": "backlit keys, precision trackpad, and all-day productivity for your tablet",
    }
    # 品类 → 英文品类名(用于留存期帖文)
    category_en = {
        "TWS 耳机": "TWS earbuds",
        "智能手表": "smartwatch",
        "充电宝": "power bank",
        "蓝牙音箱": "Bluetooth speaker",
        "GaN 充电器": "GaN charger",
        "线缆与配件": "cables & accessories",
        "运动手环": "fitness tracker",
        "平板配件": "tablet accessories",
    }
    # 品类特化内容方向(追加到该阶段内容列表)
    extra_content = {
        "预热期": "{category} 卖点悬念海报（{blurb}）",
        "发布期": "{category} 卖点实测对比（{blurb}）",
        "留存期": "{category} 隐藏功能与使用技巧（{blurb}）",
    }

    is_specific = category in category_blurbs
    blurb = category_blurbs.get(
        category, "consumer tech engineered to make everyday life easier"
    )
    cat_en = category_en.get(category, "device")

    stages = {
        "预热期": {
            "goal": "在正式发布前制造期待，积累粉丝并营造热度",
            "platforms": ["YouTube", "Instagram", "TikTok"],
            "content": [
                "产品渲染图和设计视频预告",
                "悬念式对比帖（\"挑战者即将登场……\"）",
                "KOL 提前体验和开箱预览",
                "工厂/QC 幕后花絮",
                "核心卖点参数海报",
            ],
            "frequency": "每周 3-5 条，覆盖 2-3 个平台",
        },
        "发布期": {
            "goal": "最大化发布曝光，驱动首波转化，建立口碑",
            "platforms": ["TikTok", "Instagram", "YouTube", "Facebook"],
            "content": [
                "开箱与测评视频（KOL + KOC 矩阵）",
                "同级竞品横向对比",
                "极限耐用测试（跌落/防水/续航）",
                "限时早鸟价和发布促销",
                "直播带货 + 实时问答",
                "付费社媒广告 + 再营销",
            ],
            "frequency": "每天 1-2 条 + 持续投放；前两周是关键期",
        },
        "留存期": {
            "goal": "提升用户粘性和复购率，激励 UGC 和社群活跃",
            "platforms": ["Instagram", "Email", "Facebook Groups"],
            "content": [
                "真实用户 UGC 活动和晒单展示",
                "使用技巧和隐藏功能教程",
                "固件/软件更新亮点",
                "老客折扣和以旧换新",
                "季度配件推荐",
            ],
            "frequency": "每周 2-3 条 + 双周邮件简报",
        },
    }

    hashtags = {
        "北美": "#ConsumerTech #TechGadgets #Unboxing #TechReview",
        "欧洲": "#ConsumerElectronics #TechLife #Innovation #GadgetLover",
        "东南亚": "#TechPH #TechID #DigitalLife #GadgetIndonesia",
        "中东": "#TechUAE #GadgetReview #SmartTech #MiddleEastTech",
    }

    info = stages.get(stage, stages["预热期"])

    # 追加品类特化内容方向(复制,避免污染共享的 stages 字典)
    if is_specific and extra_content.get(stage):
        info = dict(info)
        info["content"] = list(info["content"]) + [
            extra_content[stage].format(category=category, blurb=blurb)
        ]

    tag = hashtags.get(market, "#ConsumerTech")

    if stage == "预热期":
        draft = (
            f"⚡ Something big is coming to {market}.\n\n"
            f"We've been in the lab engineering {blurb} — and it's going to change "
            f"the way you experience everyday tech. Lighter. Faster. Smarter.\n\n"
            f"This isn't just another gadget — it's the one we'd use ourselves.\n\n"
            f"📬 Be the first to know: [sign-up link]\n\n"
            f"{tag}"
        )
    elif stage == "发布期":
        draft = (
            f"🚀 It's here. Meet your new daily driver in {market}.\n\n"
            f"After months of R&D and real-world testing, we're proud to launch "
            f"our latest consumer electronics innovation — engineered for those "
            f"who demand more from their tech.\n\n"
            f"✨ What makes it different:\n"
            f"⚡ {blurb[:1].upper()}{blurb[1:]}\n"
            f"🎯 Designed for real-life use\n"
            f"💰 Premium feel, honest price\n\n"
            f"🎉 Launch week special: 15% off first 200 orders.\n\n"
            f"👉 Get yours: [link]\n\n"
            f"{tag}"
        )
    else:
        draft = (
            f"🌟 You've been part of our journey in {market} — thank you!\n\n"
            f"Pro tip for your {cat_en}: get the most out of your device "
            f"with these simple hacks:\n"
            f"🔋 Optimise battery settings for all-day power\n"
            f"🔄 Keep firmware updated for the latest features\n"
            f"🎒 Use the right accessories for every scenario\n\n"
            f"Tag us in your setup for a chance to be featured! 📸\n\n"
            f"Got questions? We're here to help.\n\n"
            f"{tag}"
        )

    return {"info": info, "draft": draft}


# ═══════════════════════════════════════════════════════════════════════════
# Tab 导航
# ═══════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3 = st.tabs(["📋 产品匹配", "📈 市场策略", "📱 社媒营销"])

# ── Tab 1：产品匹配 ──────────────────────────────────────────────────────

with tab1:
    products = match_products(
        market=market,
        use_scenario=use_scenario,
        use_case=use_case,
        budget=budget,
        category=product_category,
        top_n=3,
    )

    solution_brief = generate_solution_brief(
        market=market,
        use_scenario=use_scenario,
        use_case=use_case,
        budget=budget,
        products=products,
    )

    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown('<div class="section-title">📦 推荐产品</div>', unsafe_allow_html=True)

        if not products:
            st.info("未找到匹配产品，请调整筛选条件。")
        else:
            EMOJI = {
                "TWS Earbuds": "🎧", "Smart Watch": "⌚", "Power Bank": "🔋",
                "Bluetooth Speaker": "🔊", "GaN Charger": "⚡",
                "Cables & Accessories": "🔌", "Fitness Tracker": "🏃",
                "Tablet Accessories": "📱",
            }
            for p in products:
                emoji = EMOJI.get(p["category"], "🛠️")
                st.markdown(
                    f'<div class="product-card">'
                    f'<div class="product-name">{emoji} {p["name"]}'
                    f'<span class="product-category">{p["category"]}</span></div>'
                    f'<div class="product-desc">{p["description"]}</div>'
                    f"</div>",
                    unsafe_allow_html=True,
                )

    with col_right:
        st.markdown('<div class="section-title">📝 方案简报</div>', unsafe_allow_html=True)

        with st.container():
            st.markdown(
                f'<div class="brief-box">{solution_brief}</div>',
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        md_bytes = export_to_bytesio(solution_brief)
        fname = suggest_filename(market, use_scenario)
        st.download_button(
            label="📥 导出方案简报（Markdown）",
            data=md_bytes,
            file_name=fname,
            mime="text/markdown",
            use_container_width=True,
        )

# ── Tab 2：市场策略 ───────────────────────────────────────────────────────

with tab2:
    st.markdown('<div class="section-title">🌍 市场进入策略</div>', unsafe_allow_html=True)

    strategy = _market_strategy(market, product_category)

    # 第 1 行 — 市场概况（通栏）
    st.markdown(
        f'<div class="card">'
        f'<div class="card-label">📊 市场概况</div>'
        f'<div class="card-body">{strategy["characteristic"]}</div>'
        f"</div>",
        unsafe_allow_html=True,
    )

    # 第 2 行 — 渠道 + 定价（2 列）
    st.markdown(
        f'<div class="card-grid-2">'
        f'<div class="card">'
        f'<div class="card-label">📡 渠道策略</div>'
        f'<div class="card-body"><strong>推荐配比：</strong> {strategy["channel"]}</div>'
        f"</div>"
        f'<div class="card">'
        f'<div class="card-label">💰 定价建议</div>'
        f'<div class="card-body">{strategy["pricing"]}</div>'
        f"</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # 第 3 行 — 本地化注意事项
    notes_html = "".join(f"<li>{n}</li>" for n in strategy["localisation"])
    st.markdown(
        f'<div class="card">'
        f'<div class="card-label">🌐 本地化清单</div>'
        f'<div class="card-body"><ul>{notes_html}</ul></div>'
        f"</div>",
        unsafe_allow_html=True,
    )

    st.caption(
        f"基于 **{market}** × **{product_category}**。修改侧边栏筛选条件即可更新。"
    )

# ── Tab 3：社媒营销 ──────────────────────────────────────────────────────

with tab3:
    st.markdown('<div class="section-title">📱 社媒营销工作台</div>', unsafe_allow_html=True)

    stage = st.selectbox(
        "营销阶段",
        options=["预热期", "发布期", "留存期"],
        index=0,
        label_visibility="collapsed",
    )

    stage_labels = {"预热期": "预热期", "发布期": "发布期", "留存期": "留存期"}
    st.markdown(
        f'<div style="display:flex;gap:0.5rem;align-items:center;margin-bottom:1rem;">'
        f'<span class="metric-chip" style="background:#1DB954;color:#fff;font-weight:700;">{stage_labels[stage]}</span>'
        f'<span style="color:#8c8c86;font-size:0.85rem;">{market}</span>'
        f"</div>",
        unsafe_allow_html=True,
    )

    sm = _social_content(stage, market, product_category)
    info = sm["info"]

    # 第 1 行 — 目标 + 平台
    platforms_html = " · ".join(f"<strong>{p}</strong>" for p in info["platforms"])
    st.markdown(
        f'<div class="card-grid-2">'
        f'<div class="card">'
        f'<div class="card-label">🎯 阶段目标</div>'
        f'<div class="card-body">{info["goal"]}</div>'
        f"</div>"
        f'<div class="card">'
        f'<div class="card-label">📱 推荐平台</div>'
        f'<div class="card-body">{platforms_html}</div>'
        f"</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # 第 2 行 — 内容方向 + 频率
    bullets = "".join(f"<li>{item}</li>" for item in info["content"])
    st.markdown(
        f'<div class="card-grid-2">'
        f'<div class="card">'
        f'<div class="card-label">📝 内容方向建议</div>'
        f'<div class="card-body"><ul>{bullets}</ul></div>'
        f"</div>"
        f'<div class="card">'
        f'<div class="card-label">📅 发布频率</div>'
        f'<div class="card-body">{info["frequency"]}</div>'
        f"</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # 帖文草稿
    st.markdown(
        '<div class="section-title" style="margin-top:0.5rem;">✍️ 英文帖文草稿</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="color:#727272;font-size:0.8rem;margin-top:-0.5rem;margin-bottom:0.5rem;">'
        "可编辑 — 发布前可根据需要调整。</p>",
        unsafe_allow_html=True,
    )
    st.text_area("帖文内容", value=sm["draft"], height=220, label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)

    # 发布前清单
    st.markdown('<div class="section-title">✅ 发布前检查清单</div>', unsafe_allow_html=True)
    c1 = st.checkbox("各社媒账号已设置并完成品牌化", value=False)
    c2 = st.checkbox("至少 3 篇帖文已准备好排期", value=False)
    c3 = st.checkbox("广告预算已批准并分配", value=False)
    c4 = st.checkbox("数据分析 / Pixel 工具已部署", value=False)
    c5 = st.checkbox("客服预案已就绪", value=False)
    done = sum([c1, c2, c3, c4, c5])

    st.progress(done / 5, text=f"准备进度：{done}/5")

    if done == 5:
        st.success("✅ 全部就绪 — 可以发布了！")
    elif done >= 3:
        st.info(f"⚡ {done}/5 已完成 — 继续完成剩余项即可发布。")
    else:
        st.warning(f"📋 发布前请至少完成 3 项（目前 {done}/5）。")


# ═══════════════════════════════════════════════════════════════════════════
# 底部
# ═══════════════════════════════════════════════════════════════════════════

st.markdown(
    '<div class="app-footer">'
    "海外GTM工作台 · MVP v1.1 · Powered by Streamlit"
    "</div>",
    unsafe_allow_html=True,
)
