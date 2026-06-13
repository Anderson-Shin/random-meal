#!/usr/bin/env python3
"""Shared mapping helpers for local OpenRice candidate transformation."""

from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any


BUDGET_MAP = {
    "budget": "$",
    "affordable": "$$",
    "mid": "$$",
    "upper_mid": "$$$",
    "premium": "$$$$",
    "luxury": "$$$$",
    "unknown": "$$",
}

ZH_HANS_REPLACEMENTS = {
    "環": "环", "鰂": "鲗", "魚": "鱼", "涌": "涌", "觀": "观", "灣": "湾",
    "國": "国", "菜": "菜", "壽": "寿", "麵": "面", "點": "点", "鍋": "锅",
    "廳": "厅", "車": "车", "雲": "云", "餅": "饼", "漢": "汉", "韓": "韩",
    "臺": "台", "萬": "万", "與": "与", "專": "专", "門": "门", "店": "店",
    "樓": "楼", "號": "号", "舖": "铺", "廣": "广", "場": "场", "華": "华",
    "龍": "龙", "島": "岛", "樂": "乐", "蝦": "虾", "湯": "汤", "處": "处",
}


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"{path}: invalid JSON: {error.msg}") from error


def load_district_map(path: Path) -> list[dict[str, Any]]:
    data = load_json(path)
    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        raise ValueError("district map must be a JSON array of objects")
    return data


def load_category_map(path: Path) -> dict[str, dict[str, Any]]:
    data = load_json(path)
    if not isinstance(data, dict) or not all(isinstance(item, dict) for item in data.values()):
        raise ValueError("category map must be a JSON object of mapping objects")
    return data


def dedupe_list(values: list[Any]) -> list[Any]:
    result: list[Any] = []
    seen: set[str] = set()
    for value in values:
        if value in (None, ""):
            continue
        key = json.dumps(value, ensure_ascii=False, sort_keys=True)
        if key not in seen:
            seen.add(key)
            result.append(value)
    return result


def to_zh_hans(text: str) -> str:
    return "".join(ZH_HANS_REPLACEMENTS.get(character, character) for character in text)


def map_district(source_district: Any, district_map: list[dict[str, Any]]) -> dict[str, str]:
    source = source_district.strip() if isinstance(source_district, str) else ""
    source_key = source.casefold()
    for mapping in district_map:
        labels = mapping.get("sourceLabels", [])
        if any(isinstance(label, str) and label.casefold() == source_key for label in labels):
            return {
                "area": str(mapping.get("area") or source),
                "district": str(mapping.get("district") or source),
                "area_zhHant": str(mapping.get("area_zhHant") or source),
                "area_zhHans": str(mapping.get("area_zhHans") or to_zh_hans(source)),
            }
    return {
        "area": source,
        "district": source,
        "area_zhHant": source,
        "area_zhHans": to_zh_hans(source),
    }


def map_categories(categories: Any, category_map: dict[str, dict[str, Any]]) -> dict[str, Any]:
    source_categories = [
        item.strip() for item in categories if isinstance(item, str) and item.strip()
    ] if isinstance(categories, list) else []
    casefold_map: dict[str, dict[str, Any]] = {}
    for key, value in category_map.items():
        casefold_map[key.casefold()] = value
        casefold_map[to_zh_hans(key).casefold()] = value
    matches = [casefold_map[item.casefold()] for item in source_categories if item.casefold() in casefold_map]
    first = matches[0] if matches else {}

    def combined(field: str) -> list[Any]:
        return dedupe_list([
            value
            for match in matches
            for value in (match.get(field) if isinstance(match.get(field), list) else [])
        ])

    speeds = [match.get("speed") for match in matches if isinstance(match.get("speed"), str)]
    speed = "quick" if "quick" in speeds else "relaxed" if "relaxed" in speeds else "normal"
    return {
        "cuisine": first.get("cuisine", "Other"),
        "cuisine_en": first.get("cuisine_en", "Other"),
        "cuisine_zhHant": first.get("cuisine_zhHant", "其他"),
        "cuisine_zhHans": first.get("cuisine_zhHans", "其他"),
        "sourceCategories": dedupe_list(source_categories),
        "tags": combined("tags"),
        "tags_en": combined("tags_en"),
        "tags_zhHant": combined("tags_zhHant"),
        "tags_zhHans": combined("tags_zhHans"),
        "mealTypes": combined("mealTypes"),
        "situations": combined("situations"),
        "speed": speed,
    }


def map_price(price_range_id: Any, price_band: Any, price_map: dict[str, str]) -> dict[str, str]:
    mapped_band = price_map.get(str(price_range_id), "")
    band = mapped_band or (price_band.strip() if isinstance(price_band, str) else "") or "unknown"
    return {"priceBand": band, "budget": BUDGET_MAP.get(band, "$$")}


def build_multilingual_names(candidate: dict[str, Any]) -> dict[str, str]:
    name = candidate.get("name", "")
    name = name.strip() if isinstance(name, str) else ""
    other = candidate.get("name_other_lang")
    alternatives: list[str] = []
    if isinstance(other, str) and other.strip():
        alternatives.append(other.strip())
    elif isinstance(other, dict):
        alternatives.extend(
            value.strip() for value in other.values() if isinstance(value, str) and value.strip()
        )
    elif isinstance(other, list):
        alternatives.extend(value.strip() for value in other if isinstance(value, str) and value.strip())

    all_names = [name] + alternatives
    chinese_names = [value for value in all_names if re.search(r"[\u3400-\u9fff]", value)]
    english_names = [value for value in all_names if re.search(r"[A-Za-z]", value) and not re.search(r"[\u3400-\u9fff]", value)]
    zh_hant = chinese_names[0] if chinese_names else name
    return {
        "name_en": english_names[0] if english_names else "",
        "name_zhHant": zh_hant,
        "name_zhHans": to_zh_hans(zh_hant),
    }
