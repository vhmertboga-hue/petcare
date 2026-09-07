import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any, Dict, List

import requests
from bs4 import BeautifulSoup


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


def filter_products(products: List[Dict[str, Any]], min_price: int = 800, max_price: int = 2000, min_margin_pct: int = 35) -> List[Dict[str, Any]]:
    candidates = []
    for product in products:
        price = float(product.get("price", 0) or 0)
        margin_pct = calculate_margin_pct(product)
        if min_price <= price <= max_price and margin_pct >= min_margin_pct:
            product_copy = dict(product)
            product_copy["margin_pct"] = round(margin_pct, 2)
            candidates.append(product_copy)
    return sorted(candidates, key=lambda item: item["margin_pct"], reverse=True)


def save_candidates(candidates: List[Dict[str, Any]], output_path: str = "candidates.json") -> None:
    with open(output_path, "w", encoding="utf-8") as handle:
        json.dump(candidates, handle, ensure_ascii=False, indent=2)


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


def fetch_page_text(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, timeout=20, headers=headers)
        response.raise_for_status()
        return response.text
    except Exception:
        proxy_url = f"https://r.jina.ai/http://{url}"
        response = requests.get(proxy_url, timeout=20, headers=headers)
        response.raise_for_status()
        return response.text


def scrape_products_from_url(url: str) -> List[Dict[str, Any]]:
    html_text = fetch_page_text(url)
    if "<html" in html_text.lower() or "<!doctype" in html_text.lower():
        soup = BeautifulSoup(html_text, "html.parser")
        text = soup.get_text(" ", strip=True)
    else:
        text = html_text

    matches = []
    for item in re.findall(r"([A-Za-z0-9çÇğĞıİöÖşŞüÜ\- ]{3,})\s*([0-9]+(?:[.,][0-9]{1,2})?)\s*TL", text):
        name = item[0].strip()
        price = float(item[1].replace(",", "."))
        if name.lower() in {"kargo", "taksit", "fiyat"}:
            continue
        matches.append({"name": name, "price": price})

    if not matches:
        raise ValueError("URL'den ürün bilgisi çıkarılamadı")

    products = []
    for item in matches:
        products.append(
            {
                "name": item["name"],
                "price": item["price"],
                "supplier_price": max(300, int(item["price"] * 0.45)),
                "shipping_cost": 40,
                "commission_pct": 0.10,
                "ad_cost": 30,
                "packaging_cost": 15,
            }
        )
    return products


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fiyatı 800-2000 TL arası ve marjı yüksek olan ürünleri filtreler")
    parser.add_argument("--input", default=None, help="Ürün listesini içeren JSON veya CSV dosyası")
    parser.add_argument("--url", default=None, help="Ürün listesi içeren bir web sayfası URL'si")
    parser.add_argument("--output", default="candidates.json", help="Seçili ürünleri yazdıracak çıktı dosyası")
    parser.add_argument("--min-price", type=int, default=800, help="Minimum fiyat")
    parser.add_argument("--max-price", type=int, default=2000, help="Maksimum fiyat")
    parser.add_argument("--min-margin", type=int, default=35, help="Minimum kar marjı yüzdesi")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    sample_products = [
        {
            "name": "Kablosuz kulaklık",
            "price": 1499,
            "supplier_price": 620,
            "shipping_cost": 60,
            "commission_pct": 0.10,
            "ad_cost": 40,
            "packaging_cost": 20,
        },
        {
            "name": "Akıllı saat",
            "price": 1799,
            "supplier_price": 780,
            "shipping_cost": 70,
            "commission_pct": 0.10,
            "ad_cost": 45,
            "packaging_cost": 25,
        },
        {
            "name": "Mikrofon",
            "price": 650,
            "supplier_price": 280,
            "shipping_cost": 35,
            "commission_pct": 0.10,
            "ad_cost": 20,
            "packaging_cost": 15,
        },
        {
            "name": "Laptop stand",
            "price": 999,
            "supplier_price": 380,
            "shipping_cost": 35,
            "commission_pct": 0.10,
            "ad_cost": 30,
            "packaging_cost": 15,
        },
        {
            "name": "USB-C hub",
            "price": 1199,
            "supplier_price": 470,
            "shipping_cost": 45,
            "commission_pct": 0.10,
            "ad_cost": 35,
            "packaging_cost": 20,
        },
    ]

    if args.input:
        products = load_products(args.input)
    elif args.url:
        products = scrape_products_from_url(args.url)
    else:
        products = sample_products

    candidates = filter_products(products, min_price=args.min_price, max_price=args.max_price, min_margin_pct=args.min_margin)
    save_candidates(candidates, args.output)
    print(f"Bulunan aday ürün sayısı: {len(candidates)}")
    for candidate in candidates:
        print(f"{candidate['name']}: fiyat={candidate['price']} TL, kar marjı={candidate['margin_pct']}%")


if __name__ == "__main__":
    main()
