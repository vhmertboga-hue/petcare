import os
import tempfile
import unittest
from unittest.mock import patch

from openpyxl import load_workbook

from masis_home_ecommerce_assistant import analyze_products, export_report_to_excel, main


class MasisHomeEcommerceAssistantTests(unittest.TestCase):
    def test_analyze_products_calculates_margin_and_suggested_price(self):
        products = [
            {
                "name": "Ahşap masa lambası",
                "price": 1499,
                "supplier_price": 620,
                "shipping_cost": 60,
                "commission_pct": 0.10,
                "ad_cost": 40,
                "packaging_cost": 20,
            }
        ]

        results = analyze_products(products, target_margin_pct=35, min_price=800, max_price=2000)

        self.assertEqual(len(results), 1)
        self.assertAlmostEqual(results[0]["margin_pct"], 40.63, places=2)
        self.assertAlmostEqual(results[0]["suggested_price"], 1345.45, places=2)

    def test_export_report_to_excel_writes_workbook(self):
        products = [
            {
                "name": "Beyaz dekor vazo",
                "price": 999,
                "supplier_price": 380,
                "shipping_cost": 35,
                "commission_pct": 0.10,
                "ad_cost": 30,
                "packaging_cost": 15,
            }
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "assistant.xlsx")
            export_report_to_excel(analyze_products(products), file_path)

            workbook = load_workbook(file_path)
            sheet = workbook.active
            self.assertEqual(sheet.title, "Masis Home Assistant")
            self.assertEqual(sheet["A2"].value, "Beyaz dekor vazo")
            self.assertEqual(sheet["B2"].value, 999)

    def test_main_falls_back_to_sample_products_when_input_file_is_missing(self):
        with patch("masis_home_ecommerce_assistant.load_products", side_effect=FileNotFoundError("Dosya bulunamadı")), \
             patch("masis_home_ecommerce_assistant.export_report_to_excel") as mock_export, \
             patch("sys.argv", ["assistant.py", "--input", "missing.json"]):
            main()

        self.assertTrue(mock_export.called)


if __name__ == "__main__":
    unittest.main()
