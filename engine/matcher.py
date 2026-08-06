"""
matcher.py — Consumer Electronics Product Recommendation Engine

Matches user inputs (market, use_scenario, use_case, budget) to products
using tag-based scoring. Returns top-N matches with fallback logic.
"""

import json
import os


DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "products.json")


def load_products() -> list[dict]:
    """Load product catalog from JSON data file."""
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# ── Tag normalisation (Chinese UI labels → internal tags) ──────────────────

_MARKET_MAP = {
    "北美": "north_america",
    "欧洲": "europe",
    "东南亚": "southeast_asia",
    "中东": "middle_east",
}

_SCENARIO_MAP = {
    "户外运动": "outdoor_sports",
    "商务办公": "business_office",
    "日常通勤": "daily_commute",
    "游戏娱乐": "gaming_entertainment",
    "旅行出差": "travel",
}

_USECASE_MAP = {
    "音质表现": "audio_quality",
    "续航能力": "battery_life",
    "快充技术": "fast_charging",
    "便携设计": "portable_design",
    "智能互联": "smart_connectivity",
    "运动健身": "sports_fitness",
    "商务兼容": "business_compatibility",
}

_BUDGET_MAP = {
    "入门": "low",
    "中端": "medium",
    "高端": "high",
}

# 中文品类标签 → 产品数据里的英文 category 键
_CATEGORY_MAP = {
    "TWS 耳机": "TWS Earbuds",
    "智能手表": "Smart Watch",
    "充电宝": "Power Bank",
    "蓝牙音箱": "Bluetooth Speaker",
    "GaN 充电器": "GaN Charger",
    "线缆与配件": "Cables & Accessories",
    "运动手环": "Fitness Tracker",
    "平板配件": "Tablet Accessories",
}

_ALL_CATEGORIES = "全部品类"


def _resolve_category(category: str) -> str | None:
    """Map a UI category label to its English catalog key; None = 不筛选."""
    if not category or category.strip() == _ALL_CATEGORIES:
        return None
    return _CATEGORY_MAP.get(category.strip(), category.strip())


def _tag(label: str, mapping: dict) -> str:
    """Map a UI label to its internal tag; return slug on fallback."""
    return mapping.get(label.strip(), label.strip().lower().replace(" ", "_"))


# ── Matching logic ─────────────────────────────────────────────────────────


def match_products(
    market: str,
    use_scenario: str,
    use_case: str,
    budget: str,
    category: str | None = None,
    top_n: int = 3,
) -> list[dict]:
    """
    Return the top-N products whose tags intersect most with user selections.

    Strategy
    --------
    1. (可选) 按品类过滤产品池。
    2. Build a user-tag set from the four UI selections.
    3. Score every product by intersection size (max 4).
    4. Return highest-scored products (top N).
    5. If fewer than top_n match, append unused products (prefer same use_case).
       当指定了品类时,只在所选品类内补齐,不跨品类。
    """
    products = load_products()
    cat_en = _resolve_category(category)
    if cat_en:
        products = [p for p in products if p.get("category") == cat_en]
        if not products:  # 所选品类暂无产品时回退全量,避免空结果
            products = load_products()

    user_tags = {
        _tag(market, _MARKET_MAP),
        _tag(use_scenario, _SCENARIO_MAP),
        _tag(use_case, _USECASE_MAP),
        _tag(budget, _BUDGET_MAP),
    }

    scored = []
    for p in products:
        flat = _flatten_tags(p)
        score = len(user_tags & flat)
        if score > 0:
            scored.append((score, p))

    # Descending score, stable by id
    scored.sort(key=lambda x: (-x[0], x[1]["id"]))
    matched = [p for _, p in scored[:top_n]]
    used_ids = {p["id"] for p in matched}

    if cat_en:
        # 品类筛选 — 只在所选品类内补齐
        if len(matched) < top_n:
            for p in products:
                if len(matched) >= top_n:
                    break
                if p["id"] in used_ids:
                    continue
                matched.append(p)
                used_ids.add(p["id"])
    else:
        # Fallback — fill remaining slots with same-use_case products
        if len(matched) < top_n:
            use_case_tag = _tag(use_case, _USECASE_MAP)
            for p in products:
                if len(matched) >= top_n:
                    break
                if p["id"] in used_ids:
                    continue
                if use_case_tag in _flatten_tags(p):
                    matched.append(p)
                    used_ids.add(p["id"])

        # Last-resort — anything left
        if len(matched) < top_n:
            for p in products:
                if len(matched) >= top_n:
                    break
                if p["id"] not in used_ids:
                    matched.append(p)
                    used_ids.add(p["id"])

    return matched[:top_n]


def _flatten_tags(product: dict) -> set[str]:
    """Collect all tag values from a product into a single set of strings."""
    flat: set[str] = set()
    for val in product.get("tags", {}).values():
        if isinstance(val, list):
            flat.update(val)
        else:
            flat.add(val)
    return flat
