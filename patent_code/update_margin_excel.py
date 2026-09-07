#!/usr/bin/env python3
import argparse
import os
import re
import sys
import time
from datetime import datetime
from typing import Optional, Tuple

import pandas as pd
import requests
from bs4 import BeautifulSoup


def normalize_column_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def find_column(columns, preferred_names, fallback_name: Optional[str] = None) -> Optional[str]:
    normalized_map = {normalize_column_name(col): col for col in columns}
    for preferred in preferred_names:
        if normalize_column_name(preferred) in normalized_map:
            return normalized_map[normalize_column_name(preferred)]
    if fallback_name:
        if normalize_column_name(fallback_name) in normalized_map:
            return normalized_map[normalize_column_name(fallback_name)]
    return None


def fetch_usd_try_rate(rate_override: Optional[float] = None) -> float:
    """Try Demet Döviz first, then fall back to a public API if needed."""
    if rate_override is not None:
        return float(rate_override)

    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get("https://www.demetdoviz.com/", timeout=20, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        text = "\n".join(soup.stripped_strings)
        matches = re.findall(r"([0-9]+(?:[\.,][0-9]+)?)", text)
        if matches:
            # Try to find a plausible rate near USD/TRY references in the page content.
            # The site may not expose a stable numeric field, so this branch is best-effort.
            for idx, token in enumerate(matches):
                if token.count(",") or token.count("."):
                    # Prefer a value that looks like a rate and appears later in the page.
                    if idx + 1 < len(matches):
                        return float(token.replace(",", "."))
    except Exception:
        pass

    try:
        response = requests.get("https://api.frankfurter.app/latest?from=USD&to=TRY", timeout=20, headers=headers)
        response.raise_for_status()
        payload = response.json()
        return float(payload["rates"]["TRY"])
    except Exception as exc:
        raise RuntimeError(f"Kur bilgisi alınamadı: {exc}") from exc


def update_excel(file_path: str, sheet_name: Optional[str], cost_col_name: Optional[str], margin_col_name: Optional[str], price_col_name: Optional[str], rate_col_name: Optional[str], timestamp_col_name: Optional[str], rate_override: Optional[float] = None) -> Tuple[pd.DataFrame, float]:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Excel dosyası bulunamadı: {file_path}")

    excel = pd.ExcelFile(file_path)
    if sheet_name is None:
        sheet_name = excel.sheet_names[0]

    df = pd.read_excel(file_path, sheet_name=sheet_name)
    columns = list(df.columns)

    cost_col = find_column(columns, [cost_col_name] if cost_col_name else [], "Maliyet_USD") if cost_col_name else find_column(columns, ["maliyet_usd", "maliyetusd", "costusd", "usd_maliyet", "maliyet", "cost_usd"], "Maliyet_USD")
    margin_col = find_column(columns, [margin_col_name] if margin_col_name else [], "Kar_Marjı_%") if margin_col_name else find_column(columns, ["kar_marj_yuzdesi", "kar_marjı", "karmarj", "kar_marj", "margin_pct", "marginpercent", "margin"], "Kar_Marjı_%")
    price_col = find_column(columns, [price_col_name] if price_col_name else [], "Satış_Fiyat_TRY") if price_col_name else find_column(columns, ["satis_fiyati_try", "satis_fiyati", "fiyat_try", "satisfiyati", "selling_price_try", "selling_price", "price_try"], "Satış_Fiyat_TRY")
    rate_col = find_column(columns, [rate_col_name] if rate_col_name else [], "Dolar_Kuru") if rate_col_name else find_column(columns, ["dolar_kuru", "usd_try", "usd_kuru", "kur", "exchange_rate", "rate"], "Dolar_Kuru")
    timestamp_col = find_column(columns, [timestamp_col_name] if timestamp_col_name else [], "Son_Güncelleme") if timestamp_col_name else find_column(columns, ["son_guncelleme", "last_updated", "updated_at"], "Son_Güncelleme")

    if cost_col is None or margin_col is None:
        raise ValueError(
            "Gerekli sütunlar bulunamadı. "
            "Excel'de 'Maliyet_USD' ve 'Kar_Marjı_%' sütunları olmalı veya parametreleri belirtmelisiniz."
        )

    if price_col is None:
        price_col = "Satış_Fiyat_TRY"
    if rate_col is None:
        rate_col = "Dolar_Kuru"
    if timestamp_col is None:
        timestamp_col = "Son_Güncelleme"

    rate = fetch_usd_try_rate(rate_override)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    df[cost_col] = pd.to_numeric(df[cost_col], errors="coerce")
    df[margin_col] = pd.to_numeric(df[margin_col], errors="coerce")

    if df[margin_col].abs().max() <= 1.0:
        margin_decimal = df[margin_col]
    else:
        margin_decimal = df[margin_col] / 100.0

    df[price_col] = df[cost_col] * rate / (1 - margin_decimal)
    df[rate_col] = rate
    df[timestamp_col] = now_str

    if os.path.exists(file_path):
        with pd.ExcelWriter(file_path, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    else:
        with pd.ExcelWriter(file_path, engine="openpyxl", mode="w") as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    return df, rate


def main() -> None:
    parser = argparse.ArgumentParser(description="USD kuruna göre ürünlerin satış fiyatını güncelleyen Excel betiği")
    parser.add_argument("--file", required=True, help="Güncellenecek Excel dosyasının yolu")
    parser.add_argument("--sheet", default=None, help="İşlenecek sayfa adı")
    parser.add_argument("--cost-column", default=None, help="USD maliyet sütunu adı")
    parser.add_argument("--margin-column", default=None, help="Kar marjı sütunu adı")
    parser.add_argument("--price-column", default=None, help="Yazılacak satış fiyatı sütunu adı")
    parser.add_argument("--rate-column", default=None, help="Dolar kuru sütunu adı")
    parser.add_argument("--timestamp-column", default=None, help="Güncelleme zamanı sütunu adı")
    parser.add_argument("--rate", type=float, default=None, help="Manuel USD/TRY kuru. İnternet yoksa kullanılır")
    parser.add_argument("--interval-minutes", type=float, default=None, help="Belirtilirse bu aralıkta tekrar çalışır")
    args = parser.parse_args()

    while True:
        try:
            df, rate = update_excel(
                args.file,
                args.sheet,
                args.cost_column,
                args.margin_column,
                args.price_column,
                args.rate_column,
                args.timestamp_column,
                args.rate,
            )
            print(f"Başarılı. {len(df)} satır güncellendi. Dolar kuru: {rate:.4f}")
        except Exception as exc:
            print(f"Hata: {exc}", file=sys.stderr)
            sys.exit(1)

        if args.interval_minutes is None or args.interval_minutes <= 0:
            break

        print(f"{args.interval_minutes} dakika sonra tekrar kontrol edilecek...")
        time.sleep(args.interval_minutes * 60)


if __name__ == "__main__":
    main()
