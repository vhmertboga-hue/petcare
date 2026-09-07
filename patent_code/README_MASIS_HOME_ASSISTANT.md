# Masis Home E-Commerce Assistant

Bu proje, Trendyol benzeri bir e-ticaret akışında ürünleri analiz etmek için kullanılacak temel bir asistanı içerir.

## Özellikler
- Ürün başına kar marjı hesaplama
- Hedef marjı sağlayacak önerilen fiyat hesaplama
- Excel raporu export etme
- CSV/JSON ürün listesi ile çalışma

## Kullanım

### Örnek çalıştırma
```bash
python masis_home_ecommerce_assistant.py --input products.json --output masis_home_assistant.xlsx --target-margin 35
```

### JSON formatı
```json
{
  "products": [
    {
      "name": "Ürün adı",
      "price": 1499,
      "supplier_price": 620,
      "shipping_cost": 60,
      "commission_pct": 0.10,
      "ad_cost": 40,
      "packaging_cost": 20
    }
  ]
}
```
