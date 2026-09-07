from __future__ import annotations

import json
import csv
from pathlib import Path
from typing import Any, Dict, List

from openpyxl import Workbook


def calculate_margin_pct(product: Dict[str, Any]) -> float:
    price = float(product.get("price", 0) or 0)
    supplier_price = float(product.get("supplier_price", 0) or 0)
    shipping_cost = float(product.get("shipping_cost", 0) or 0)
    commission_pct = float(product.get("commission_pct", 0) or 0)
    ad_cost = float(product.get("ad_cost", 0) or 0)
    packaging_cost = float(product.get("packaging_cost", 0) or 0)

    if price <= 0:
        return 0.0

    total_cost = supplier_price + shipping_cost + (price * commission_pct) + ad_cost + packaging_cost
    return ((price - total_cost) / price) * 100


def suggest_price(product: Dict[str, Any], target_margin_pct: float) -> float:
    supplier_price = float(product.get("supplier_price", 0) or 0)
    shipping_cost = float(product.get("shipping_cost", 0) or 0)
    commission_pct = float(product.get("commission_pct", 0) or 0)
    ad_cost = float(product.get("ad_cost", 0) or 0)
    packaging_cost = float(product.get("packaging_cost", 0) or 0)

    if target_margin_pct <= 0:
        return float(product.get("price", 0) or 0)

    denominator = 1 - commission_pct - (target_margin_pct / 100)
    if denominator <= 0:
        return float(product.get("price", 0) or 0)

    return (supplier_price + shipping_cost + ad_cost + packaging_cost) / denominator


def analyze_products(
    products: List[Dict[str, Any]],
    target_margin_pct: float = 35,
    min_price: int = 800,
    max_price: int = 2000,
) -> List[Dict[str, Any]]:
    results = []
    for product in products:
        price = float(product.get("price", 0) or 0)
        margin_pct = calculate_margin_pct(product)
        if min_price <= price <= max_price:
            result = dict(product)
            result["margin_pct"] = round(margin_pct, 2)
            result["suggested_price"] = round(suggest_price(product, target_margin_pct), 2)
            results.append(result)
    return sorted(results, key=lambda item: item["margin_pct"], reverse=True)


def load_products(input_path: str) -> List[Dict[str, Any]]:
    path = Path(input_path)
    if path.suffix.lower() == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return [
            {
                "name": row.get("name") or row.get("product") or row.get("ürün") or "",
                "price": float(row.get("price") or row.get("fiyat") or 0),
                "supplier_price": float(row.get("supplier_price") or row.get("maliyet") or 0),
                "shipping_cost": float(row.get("shipping_cost") or row.get("kargo") or 0),
                "commission_pct": float(row.get("commission_pct") or row.get("komisyon") or 0.10),
                "ad_cost": float(row.get("ad_cost") or row.get("reklam") or 0),
                "packaging_cost": float(row.get("packaging_cost") or row.get("paketleme") or 0),
            }
            for row in rows
        ]

    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("products"), list):
        return payload["products"]
    raise ValueError("Input should be a JSON list or a JSON object containing a 'products' list")


def export_report_to_excel(results: List[Dict[str, Any]], output_path: str) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Masis Home Assistant"

    headers = ["name", "price", "supplier_price", "shipping_cost", "commission_pct", "ad_cost", "packaging_cost", "margin_pct", "suggested_price"]
    ws.append(headers)

    for result in results:
        ws.append([
            result.get("name", ""),
            result.get("price", 0),
            result.get("supplier_price", 0),
            result.get("shipping_cost", 0),
            result.get("commission_pct", 0),
            result.get("ad_cost", 0),
            result.get("packaging_cost", 0),
            result.get("margin_pct", 0),
            result.get("suggested_price", 0),
        ])

    wb.save(output_path)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Masis Home E-Commerce Assistant")
    parser.add_argument("--input", default=None, help="Ürün listesini içeren JSON veya CSV dosyası")
    parser.add_argument("--output", default="masis_home_assistant.xlsx", help="Raporun yazılacağı Excel dosyası")
    parser.add_argument("--target-margin", type=float, default=35, help="Hedef kar marjı yüzdesi")
    args = parser.parse_args()

    default_products = [
        {
            "name": "Ahşap masa lambası",
            "price": 1499,
            "supplier_price": 620,
            "shipping_cost": 60,
            "commission_pct": 0.10,
            "ad_cost": 40,
            "packaging_cost": 20,
        },
        {
            "name": "Beyaz dekor vazo",
            "price": 999,
            "supplier_price": 380,
            "shipping_cost": 35,
            "commission_pct": 0.10,
            "ad_cost": 30,
            "packaging_cost": 15,
        },
    ]

    if args.input:
        try:
            products = load_products(args.input)
        except FileNotFoundError:
            print(f"Girdi dosyası bulunamadı: {args.input}. Örnek ürün listesiyle devam ediliyor.")
            products = default_products
        except Exception as exc:
            print(f"Girdi dosyası okunamadı: {exc}. Örnek ürün listesiyle devam ediliyor.")
            products = default_products
    else:
        products = default_products

    results = analyze_products(products, target_margin_pct=args.target_margin)
    export_report_to_excel(results, args.output)
    print(f"Analiz tamamlandı. {len(results)} ürün raporlandı.")


if __name__ == "__main__":
    main()
[
    {
        "name": "Ahşap masa lambası",
        "price": 1499,
        "supplier_price": 620,
        "shipping_cost": 60,
        "commission_pct": 0.10,
        "ad_cost": 40,
        "packaging_cost": 20,
        "margin_pct": 40.63,
        "suggested_price": 1345.45
    },
    {
        "name": "Beyaz dekor vazo",
        "price": 999,
        "supplier_price": 380,
        "shipping_cost": 35,
        "commission_pct": 0.10,
        "ad_cost": 30,

        "packaging_cost": 15,
        "margin_pct": 35.0,
        "suggested_price": 999.0
    }
]
