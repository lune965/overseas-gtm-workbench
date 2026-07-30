# 开发计划 — smart-home-presales-tool

> **版本:** V1.0  
> **日期:** 2026-07-30  
> **预计工期:** 4 天  

---

## 1. 总体策略

采用 **MVP 优先** 策略，分 4 个阶段迭代交付：

| 阶段 | 名称 | 工期 | 产出 |
|------|------|------|------|
| 1 | 项目初始化与环境搭建 | 0.5 天 | 可运行的项目骨架 |
| 2 | 核心逻辑开发 | 2 天 | 推荐引擎 + 方案生成 |
| 3 | UI 界面与交互集成 | 1 天 | 完整可交互应用 |
| 4 | 测试与交付 | 0.5 天 | 验收通过，可部署 |

---

## 2. 阶段详情

### 阶段 1 — 项目初始化与环境搭建（0.5 天）

| 任务 ID | 任务描述 | 预计工时 | 依赖 |
|---------|----------|----------|------|
| 1.1 | 创建项目目录结构 | 0.5h | - |
| 1.2 | 初始化 Git 仓库 | 0.5h | 1.1 |
| 1.3 | 创建 `requirements.txt`（streamlit, pyyaml, datetime） | 0.5h | - |
| 1.4 | 创建项目 README.md | 1h | - |
| 1.5 | 创建 `.gitignore` | 0.5h | - |

**目录结构设计:**

```
smart-home-presales-tool/
├── app.py                    # 主入口
├── requirements.txt          # 依赖管理
├── README.md                 # 项目说明
├── .gitignore
├── data/
│   └── products.json         # 内置产品数据
├── engine/
│   ├── __init__.py
│   ├── matcher.py            # 推荐匹配引擎
│   └── generator.py          # 方案简述生成器
└── docs/
    ├── requirements.md       # 需求文档
    └── development-plan.md   # 开发计划
```

---

### 阶段 2 — 核心逻辑开发（2 天）

#### 2.1 产品数据层（0.5 天） — `data/products.json`

| 任务 ID | 任务描述 | 预计工时 |
|---------|----------|----------|
| 2.1.1 | 定义产品数据结构（品类、名称、描述、适用市场/项目/预算标签） | 1h |
| 2.1.2 | 录入初始产品数据（10~15 个虚拟产品） | 2h |
| 2.1.3 | 编写产品数据加载模块 | 1h |

**产品数据字段设计:**

```json
{
  "id": "lock-001",
  "category": "smart_lock",
  "name": "SecureEntry Pro",
  "description": "Biometric smart lock with WiFi and remote access control.",
  "tags": {
    "markets": ["north_america", "europe"],
    "project_types": ["new_apartment", "villa"],
    "needs": ["security"],
    "budgets": ["medium", "high"]
  }
}
```

#### 2.2 推荐匹配引擎（1 天） — `engine/matcher.py`

| 任务 ID | 任务描述 | 预计工时 |
|---------|----------|----------|
| 2.2.1 | 实现标签匹配算法（基于用户选择条件筛选产品） | 2h |
| 2.2.2 | 实现评分排序逻辑（匹配度打分，Top-N 选取） | 2h |
| 2.2.3 | 添加兜底策略（条件无匹配时的备用推荐） | 1h |
| 2.2.4 | 单元测试（边界条件、多组合测试） | 1h |

**匹配逻辑:**

1. 根据用户选择的 4 个条件筛选产品（精确匹配 tags）
2. 按匹配标签数量降序排列
3. 选取 Top 3，不足 3 个时从全量产品中补充兜底
4. 返回含(产品, 匹配分数)的结果列表

#### 2.3 方案简述生成器（0.5 天） — `engine/generator.py`

| 任务 ID | 任务描述 | 预计工时 |
|----------|----------|----------|
| 2.3.1 | 基于模板生成英文方案简述 | 1.5h |
| 2.3.2 | 实现 Markdown 导出功能 | 1h |
| 2.3.3 | 单元测试 | 0.5h |

**方案简述模板示例:**

```
# Smart Home Solution Brief

**Customer Profile:**  
- Market: {market}  
- Project Type: {project_type}  
- Core Need: {need}  
- Budget: {budget}

**Recommended Solution:**  
We recommend a comprehensive smart home solution tailored for {market} {project_type} projects focused on {need}. 

{product_paragraphs}

**Expected Value:**  
This solution delivers enhanced {need_value}, optimized energy efficiency, and seamless user experience within a {budget} budget range.
```

---

### 阶段 3 — UI 界面与交互集成（1 天）

#### 3.1 主应用开发（0.5 天） — `app.py`

| 任务 ID | 任务描述 | 预计工时 |
|----------|----------|----------|
| 3.1.1 | 配置 Streamlit 页面（标题、布局、样式） | 1h |
| 3.1.2 | 实现侧边栏表单（4 个下拉选择框） | 1h |
| 3.1.3 | 实现右侧主区域布局（产品卡片、方案区、导出按钮） | 2h |

#### 3.2 UI 细节打磨（0.5 天）

| 任务 ID | 任务描述 | 预计工时 |
|----------|----------|----------|
| 3.2.1 | 英文界面文案统一检查 | 0.5h |
| 3.2.2 | 响应式布局适配 | 0.5h |
| 3.2.3 | 添加产品卡片样式（emoji 图标、分隔线） | 0.5h |
| 3.2.4 | 导出按钮交互（文件名、下载提示） | 0.5h |

---

### 阶段 4 — 测试与交付（0.5 天）

| 任务 ID | 任务描述 | 预计工时 |
|----------|----------|----------|
| 4.1 | 端到端功能测试（所有筛选组合） | 1.5h |
| 4.2 | 异常情况测试（空数据、边界值） | 0.5h |
| 4.3 | 导出功能验证 | 0.5h |
| 4.4 | README 完善 + 启动说明 | 0.5h |

---

## 3. 依赖清单

| 包名 | 版本 | 用途 |
|------|------|------|
| streamlit | >=1.28 | Web 应用框架 |
| pyyaml | >=6.0 | YAML/Markdown 处理（可选） |

安装命令:

```bash
pip install streamlit pyyaml
```

---

## 4. 里程碑（Milestones）

| 里程碑 | 时间 | 检查点 |
|--------|------|--------|
| M1: 项目骨架 | Day 1 上午 | `streamlit run app.py` 能启动空白页面 |
| M2: 引擎完成 | Day 2 下午 | 单元测试通过，推荐逻辑正确 |
| M3: UI 集成 | Day 3 下午 | 表单与推荐联动，可交互 |
| M4: MVP 交付 | Day 4 下午 | 全功能验收通过 |

---

## 5. 风险与应对

| 风险 | 概率 | 影响 | 应对策略 |
|------|------|------|----------|
| Streamlit 版本兼容问题 | 低 | 中 | 锁定版本号，使用虚拟环境 |
| 推荐逻辑过于简单 | 中 | 中 | 预留扩展接口，后续可升级为权重评分系统 |
| 中文编码问题 | 低 | 低 | 全英文界面，UTF-8 统一编码 |
| 导出文件路径不存在 | 低 | 中 | 使用 `tempfile` 或 `io.BytesIO` 处理 |

---

## 6. 后续规划（MVP 之后）

| 功能 | 优先级 | 说明 |
|------|--------|------|
| 真实产品数据库 | P1 | 接入实际 SKU 数据 |
| PDF 导出 | P2 | 增加 PDF 格式报告导出 |
| 多语言支持 | P2 | 增加更多语言界面 |
| 方案历史记录 | P3 | 保存和管理历史方案 |
| 客户管理 | P3 | 关联客户信息和方案 |
