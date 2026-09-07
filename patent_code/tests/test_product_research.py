import unittest

from product_research import filter_products


class ProductResearchTests(unittest.TestCase):
    def test_filters_products_by_price_range_and_margin(self):
        products = [
            {
                "name": "Ürün A",
                "price": 1200,
                "supplier_price": 520,
                "shipping_cost": 40,
                "commission_pct": 0.10,
                "ad_cost": 20,
                "packaging_cost": 20,
            },
            {
                "name": "Ürün B",
                "price": 700,
                "supplier_price": 300,
                "shipping_cost": 40,
                "commission_pct": 0.10,
                "ad_cost": 20,
                "packaging_cost": 20,
            },
            {
                "name": "Ürün C",
                "price": 1800,
                "supplier_price": 800,
                "shipping_cost": 50,
                "commission_pct": 0.10,
                "ad_cost": 30,
                "packaging_cost": 20,
            },
            {
                "name": "Ürün D",
                "price": 1500,
                "supplier_price": 700,
                "shipping_cost": 50,
                "commission_pct": 0.10,
                "ad_cost": 25,
                "packaging_cost": 20,
            },
        ]

        candidates = filter_products(products, min_price=800, max_price=2000, min_margin_pct=35)

        self.assertEqual([item["name"] for item in candidates], ["Ürün A", "Ürün C", "Ürün D"])


if __name__ == "__main__":
    unittest.main()
