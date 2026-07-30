# 需求文档 — smart-home-presales-tool

> **版本:** V1.0  
> **日期:** 2026-07-30  
> **状态:** 初稿  

---

## 1. 项目概述

### 1.1 项目背景

智能家居行业在海外市场需求持续增长，售前团队在与客户沟通时，需要快速根据客户需求生成个性化的产品方案和报价建议。当前缺乏一套轻量级的辅助工具来提升售前效率。

### 1.2 项目目标

构建一个基于 **Python + Streamlit** 的海外售前辅助 MVP 工具，帮助售前人员：

- 快速录入客户需求（市场、项目类型、诉求、预算）
- 自动推荐匹配的产品组合
- 自动生成英文方案简述
- 导出为 Markdown 格式的方案简报

### 1.3 项目名称

- **项目名:** `smart-home-presales-tool`
- **技术栈:** Python 3 + Streamlit

---

## 2. 用户角色

| 角色 | 说明 |
|------|------|
| 售前工程师 | 核心用户，使用本工具生成客户方案 |
| 销售经理 | 可查看/导出方案进行汇报 |

---

## 3. 功能需求

### 3.1 核心功能模块

#### F1 — 侧边栏需求表单（左侧）

| 字段 | 类型 | 选项 | 说明 |
|------|------|------|------|
| Target Market | 下拉框 | North America / Europe / Southeast Asia / Middle East | 目标市场 |
| Project Type | 下拉框 | New Apartment / Renovation / Villa Customization / Rental Apartment | 项目类型 |
| Customer Need | 下拉框 | Security Monitoring / Energy Management / Smart Lighting / Whole-Home Voice Control | 客户核心诉求 |
| Budget Range | 下拉框 | Low / Medium / High | 预算范围 |

**行为：** 用户选择任意字段后，右侧主区域实时更新推荐结果。

#### F2 — 推荐产品组合（右侧主区域）

- 根据左侧表单条件，匹配并展示 **3 个虚拟产品**
- 每个产品包含：
  - **产品名称**（英文）
  - **一句话描述**（英文）
- 匹配逻辑基于内置规则引擎（市场 × 项目类型 × 诉求 × 预算）

#### F3 — 自动生成英文方案简述

- 基于用户所选条件和推荐产品，自动生成一段 **英文方案简述**
- 内容涵盖：项目背景、推荐方案概要、预期价值
- 语气专业、简洁

#### F4 — 导出 Markdown 简报

- 点击按钮将当前方案导出为 `.md` 文件
- 导出内容包含：
  - 客户需求摘要
  - 推荐产品列表
  - 方案简述
  - 时间戳

### 3.2 内置产品数据

| 品类 | 产品示例 |
|------|----------|
| Smart Lock | Smart Lock Pro / TouchKey Plus |
| Sensor | Motion Sensor / Door/Window Sensor / Temp & Humidity Sensor |
| Camera | Security Cam 4K / Doorbell Cam / PTZ Camera |
| Smart Lighting | Smart Bulb CW / Light Strip RGB / Ceiling Light |
| Smart Socket | Smart Plug Mini / Power Strip Wi-Fi |

---

## 4. 非功能需求

| 类别 | 要求 |
|------|------|
| 界面语言 | 全英文 |
| 界面风格 | 简洁、专业、响应式 |
| 响应速度 | 筛选条件变更后 1s 内完成推荐刷新 |
| 部署方式 | 支持 `streamlit run` 本地启动 |
| 可维护性 | 产品数据与推荐逻辑分离，易于扩展 |

---

## 5. 技术选型

| 层级 | 技术 | 说明 |
|------|------|------|
| 前端/UI | Streamlit | 快速构建交互式 Web 应用 |
| 后端逻辑 | Python 3 | 推荐引擎、方案生成 |
| 数据存储 | Python 字典 / JSON 文件 | MVP 阶段内嵌数据，无需数据库 |
| 导出 | Markdown | 标准 `.md` 格式导出 |
| 包管理 | pip / requirements.txt | 依赖管理 |

---

## 6. 界面布局（线框图描述）

```
+--------------------------------------------------+
|  smart-home-presales-tool                         |
+--------------------------------------------------+
| 左栏 (Sidebar)         |  右栏 (Main Area)        |
|                         |                          |
| Target Market [▼]      |  📦 Recommended Products  |
| Project Type   [▼]     |                          |
| Customer Need  [▼]     |  1. Product A — desc     |
| Budget Range   [▼]     |  2. Product B — desc     |
|                         |  3. Product C — desc     |
|                         |                          |
|                         |  📝 Solution Brief       |
|                         |  [Generated text...]     |
|                         |                          |
|                         |  [📥 Export Markdown]    |
+--------------------------------------------------+
```

---

## 7. 约束与假设

- **假设：** 用户已安装 Python 3.10+ 环境
- **约束：** MVP 阶段使用虚拟产品数据，不接入真实 SKU 数据
- **约束：** 推荐逻辑为基于规则的简单匹配，不涉及机器学习
- **约束：** 无需用户认证/登录系统

---

## 8. 验收标准

1. 侧边栏四个筛选条件均可正常选择和联动
2. 切换筛选条件后，右侧推荐产品随之更新
3. 点击导出按钮，下载包含当前方案的 `.md` 文件
4. 界面为全英文，无明显排版问题
5. 在本地 terminal 中执行 `streamlit run app.py` 可正常启动
