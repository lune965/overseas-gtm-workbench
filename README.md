# 🏠 Smart Home Pre-Sales Tool — 智能家居海外售前辅助工具

> **版本:** MVP v1.0  
> **技术栈:** Python 3 + Streamlit  
> **项目定位:** 面向智能家居场景的海外售前支持工具，帮助售前工程师快速生成个性化产品方案与英文方案简报。

---

## 📋 目录

- [项目背景](#-项目背景)
- [功能特性](#-功能特性)
- [快速开始](#-快速开始)
- [使用指南](#-使用指南)
- [推荐引擎原理](#-推荐引擎原理)
- [内置产品目录](#-内置产品目录)
- [项目结构](#-项目结构)
- [开发计划](#-开发计划)
- [技术栈](#-技术栈)
- [常见问题](#-常见问题)

---

## 🎯 项目背景

智能家居行业在海外市场需求持续增长。售前团队在与海外客户沟通时，需要快速根据客户需求匹配产品方案并输出英文提案。目前缺乏一套轻量级的辅助工具来提升售前效率。

**本工具的目标是：**

1. 帮助售前人员快速录入客户需求（目标市场 / 项目类型 / 核心诉求 / 预算）
2. 自动匹配最合适的 3 个产品组合
3. 自动生成专业的英文方案简述（Solution Brief）
4. 支持导出为 Markdown 格式的方案简报

---

## ✨ 功能特性

### 核心功能

| 功能 | 说明 |
|------|------|
| 📋 **客户需求表单** | 侧边栏包含 4 个筛选条件：目标市场、项目类型、核心诉求、预算范围 |
| 📦 **智能产品推荐** | 基于标签评分算法，实时匹配 3 款最适合的产品 |
| 📝 **英文方案生成** | 自动生成专业的英文 Solution Brief，包含客户画像、方案概述、价值主张 |
| 📥 **Markdown 导出** | 一键下载完整的方案简报 `.md` 文件 |

### 筛选条件详情

| 字段 | 选项 |
|------|------|
| **Target Market**（目标市场） | North America · Europe · Southeast Asia · Middle East |
| **Project Type**（项目类型） | New Apartment · Renovation · Villa Customization · Rental Apartment |
| **Customer Core Need**（核心诉求） | Security Monitoring · Energy Management · Smart Lighting · Whole-Home Voice Control |
| **Budget Range**（预算范围） | Low · Medium · High |

> 所有条件均为下拉选择，切换后右侧结果区域**实时更新**，无需点击任何按钮。

---

## 🚀 快速开始

### 环境要求

- Python 3.10 或更高版本
- pip 包管理器

### 安装与启动

```bash
# 1. 进入项目目录
cd smart-home-presales-tool

# 2. 安装依赖
pip install streamlit pyyaml

# 3. 启动应用
streamlit run app.py
```

启动后，浏览器会自动打开 `http://localhost:8501`，你将看到如下界面布局：

```
+--------------------------------------------------+
|  🏠 Smart Home Pre-Sales Tool                     |
+--------------------------------------------------+
| 📋 侧边栏            |  📦 主区域                   |
|                       |                             |
| Target Market  [▼]    |  📦 Recommended Products    |
| Project Type   [▼]    |                             |
| Customer Need  [▼]    |  1. Product A — desc       |
| Budget Range   [▼]    |  2. Product B — desc       |
|                       |  3. Product C — desc       |
|                       |                             |
|                       |  📝 Solution Brief          |
|                       |  [自动生成的英文方案...]    |
|                       |                             |
|                       |  [📥 Export Markdown]       |
+--------------------------------------------------+
```

---

## 🎮 使用指南

### 第一步：填写需求

在左侧侧边栏中依次选择：
1. **Target Market** — 客户所在的目标市场
2. **Project Type** — 项目类型
3. **Customer Core Need** — 客户最核心的诉求
4. **Budget Range** — 预算范围

### 第二步：查看推荐

右侧上方会展示 **3 款推荐产品**，每款产品以卡片形式展示：
- 🔒 产品名称 + 品类标签（如 `Smart Lock`）
- 一行英文描述
- 产品按匹配度从高到低排序

### 第三步：阅读方案

右侧下方展示自动生成的 **英文 Solution Brief**，内容包括：
- **Customer Profile** — 客户需求摘要表
- **Recommended Product Bundle** — 推荐产品列表
- **Solution Overview** — 方案概述（针对不同诉求自动适配）
- **Expected Value** — 预期价值（根据预算级别自动调整语气）

### 第四步：导出简报

点击 **📥 Export Markdown Brief** 按钮，即可下载包含当前方案的 `.md` 文件。

---

## ⚙️ 推荐引擎原理

本工具采用**基于标签的评分匹配算法**：

```
输入: 市场 + 项目类型 + 诉求 + 预算
                ↓
       转换成内部标签 (tags)
                ↓
    遍历所有产品，计算匹配标签数量
                ↓
        按匹配分数降序排列
                ↓
       选取 Top 3 作为推荐结果
                ↓
      (若不足 3 个，用同类产品补充)
```

### 评分示例

例如用户选择：`North America + New Apartment + Security + Medium`

产品 `SecureEntry Pro` 的标签为：
- `markets: ["north_america", "europe"]` ✅ 匹配 1
- `project_types: ["new_apartment", "villa"]` ✅ 匹配 1
- `needs: ["security"]` ✅ 匹配 1
- `budgets: ["medium", "high"]` ✅ 匹配 1

→ 匹配得分 = **4/4**，优先推荐。

### 兜底策略

当某个筛选组合匹配到的产品少于 3 个时，系统会自动：
1. 优先从同一诉求（Need）分类中补充
2. 如果仍不足，从全量产品中补充
3. 确保始终返回 Top 3 推荐

---

## 🧰 内置产品目录

当前内置 **15 个虚拟产品**，覆盖 5 个品类：

### 🔒 Smart Lock（智能门锁）

| 产品名称 | 一句话描述 |
|----------|-----------|
| **SecureEntry Pro** | Biometric smart lock with WiFi and remote access control. |
| **TouchKey Plus** | Affordable keyless entry with fingerprint, PIN and Bluetooth. |
| **GateKeeper Max** | Heavy-duty smart deadbolt with Z-Wave for high-end villas. |

### 📡 Sensor（传感器）

| 产品名称 | 一句话描述 |
|----------|-----------|
| **MotionWatch 360** | PIR motion sensor with pet immunity and 10m detection range. |
| **OpenSense Mini** | Magnetic door/window sensor for alarms and automations. |
| **ClimateSense** | Temp & humidity sensor with HVAC integration for energy saving. |
| **WaterGuard Alarm** | Water leak detector with notifications for rental projects. |

### 📹 Camera（摄像头）

| 产品名称 | 一句话描述 |
|----------|-----------|
| **SecurityCam 4K** | Ultra HD 4K camera with AI motion detection and cloud storage. |
| **Doorbell Cam HD** | 1080p video doorbell with two-way audio and package detection. |
| **PanTilt Zoom Pro** | Motorized PTZ camera with 360° coverage and auto-tracking. |

### 💡 Smart Lighting（智能照明）

| 产品名称 | 一句话描述 |
|----------|-----------|
| **SmartBulb CW** | Tunable white WiFi bulb, dimmable, voice-compatible. |
| **LightStrip RGB** | Addressable RGB strip with music sync and scene presets. |
| **CeilingLite Smart** | Smart ceiling light with CCT tuning and motion activation. |

### 🔌 Smart Socket（智能插座）

| 产品名称 | 一句话描述 |
|----------|-----------|
| **Smart Plug Mini** | Compact WiFi plug with energy monitoring and scheduling. |
| **PowerStrip Wi-Fi** | 4-outlet smart strip with USB-C and surge protection. |

---

## 🗂️ 项目结构

```
smart-home-presales-tool/
│
├── app.py                      # 🔹 主入口 — Streamlit Web 应用
├── requirements.txt            # Python 依赖清单
├── README.md                   # 项目说明文档（本文件）
├── .gitignore                  # Git 忽略规则
│
├── data/
│   └── products.json           # 内置产品目录数据（15个产品）
│
├── engine/                     # 核心业务逻辑
│   ├── __init__.py
│   ├── matcher.py              # 标签匹配推荐引擎
│   └── generator.py            # 方案简述生成器 + Markdown 导出
│
└── docs/
    ├── requirements.md         # 需求文档
    └── development-plan.md     # 开发计划
```

### 核心文件说明

| 文件 | 职责 |
|------|------|
| `app.py` | Streamlit 主入口：页面布局、表单交互、UI 渲染 |
| `engine/matcher.py` | 推荐匹配引擎：产品加载、标签评分、排序选取 |
| `engine/generator.py` | 方案生成器：Solution Brief 模板渲染、Markdown 导出 |
| `data/products.json` | 产品数据：品类、名称、描述、标签 |

---

## 📅 开发计划

项目采用 MVP 优先策略，分 4 个阶段迭代交付：

| 阶段 | 内容 | 工期 |
|------|------|------|
| 1 — 项目初始化 | 目录结构、依赖、README、Git 初始化 | 0.5 天 |
| 2 — 核心逻辑 | 产品数据层、推荐引擎、方案生成器 | 2 天 |
| 3 — UI 集成 | Streamlit 界面、表单交互、导出功能 | 1 天 |
| 4 — 测试交付 | 端到端测试、边界情况、文档完善 | 0.5 天 |

> 完整需求文档见 `docs/requirements.md`，详细开发计划见 `docs/development-plan.md`。

---

## 🛠️ 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 前端/UI | **Streamlit** | 快速构建数据驱动的交互式 Web 应用 |
| 后端逻辑 | **Python 3** | 推荐引擎、方案生成 |
| 数据存储 | **JSON 文件** | MVP 阶段内嵌数据，无需数据库 |
| 导出格式 | **Markdown** | 标准 `.md` 文件导出 |
| 包管理 | **pip** | 依赖管理（见 `requirements.txt`） |

---

## ❓ 常见问题

### Q: 启动后浏览器没有自动打开？

在终端中手动访问：`http://localhost:8501`

### Q: 如何修改端口？

```bash
streamlit run app.py --server.port 8080
```

### Q: 如何停用 Streamlit 的匿名使用统计？

创建 `~/.streamlit/config.toml` 文件，添加：

```toml
[browser]
gatherUsageStats = false
```

### Q: 如何添加更多产品数据？

编辑 `data/products.json`，按照以下格式添加：

```json
{
  "id": "your-product-id",
  "category": "Category Name",
  "name": "Product Name",
  "description": "One-line English description.",
  "tags": {
    "markets": ["north_america"],
    "project_types": ["new_apartment"],
    "needs": ["security"],
    "budgets": ["low", "medium"]
  }
}
```

### Q: 支持哪些 Python 版本？

推荐 Python 3.10+，最低支持 Python 3.8。

---

## 📄 许可证

**内部使用 — MVP 原型**

---

## 🙌 致谢

- 基于 [Streamlit](https://streamlit.io/) 构建
- 所有产品数据为 MVP 虚拟数据，不涉及真实 SKU

---

*如有问题或建议，欢迎提交 Issue 或直接联系开发团队。*
