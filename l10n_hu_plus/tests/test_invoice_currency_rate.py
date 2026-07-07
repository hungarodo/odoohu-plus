# -*- coding: utf-8 -*-
# author: Online ERP
from __future__ import annotations

from odoo.tests.common import tagged
from odoo.addons.l10n_hu_edi.tests.common import L10nHuEdiTestCommon

from freezegun import freeze_time


@tagged("post_install", "-at_install")
class TestInvoiceCurrencyRateDeliveryDate(L10nHuEdiTestCommon):
    """Test suite for invoice_currency_rate recomputation on delivery_date change.

    Tests cover:
    - invoice_currency_rate recomputes when delivery_date changes
    - Correct exchange rate is applied based on delivery_date (Hungarian VAT Act)
    """

    @classmethod
    def setUpClass(cls) -> None:
        """Set up test fixtures: EUR rates on two different dates."""
        with freeze_time("2024-02-01"):
            super().setUpClass()

    # -------------------------------------------------------------------------
    # TEST: INVOICE_CURRENCY_RATE RECOMPUTATION
    # -------------------------------------------------------------------------

    def test_invoice_currency_rate_recomputes_on_delivery_date_change(self) -> None:
        """Verify invoice_currency_rate updates when delivery_date is changed."""
        with freeze_time("2024-02-01"):
            currency_eur = self.env.ref("base.EUR")
            invoice = self.env["account.move"].create({
                "move_type": "out_invoice",
                "journal_id": self.company_data["default_journal_sale"].id,
                "currency_id": currency_eur.id,
                "partner_id": self.partner_company.id,
                "invoice_date": self.today,
                "delivery_date": self.today,
                "invoice_line_ids": [
                    (0, 0, {
                        "product_id": self.product_a.id,
                        "price_unit": 100.0,
                        "quantity": 1,
                        "tax_ids": [(6, 0, self.tax_vat.ids)],
                    }),
                ],
            })
            rate_at_today = invoice.invoice_currency_rate
            # change delivery_date to yesterday (different rate: 377.66 vs 380.77)
            invoice.delivery_date = self.yesterday
            rate_at_yesterday = invoice.invoice_currency_rate
            self.assertNotEqual(
                rate_at_today, rate_at_yesterday,
                "invoice_currency_rate must change when delivery_date changes to a date with a different rate"
            )
            # verify the rate corresponds to yesterday's rate
            expected_rate = self.env["res.currency"]._get_conversion_rate(
                from_currency=invoice.company_currency_id,
                to_currency=currency_eur,
                company=invoice.company_id,
                date=self.yesterday,
            )
            self.assertAlmostEqual(
                rate_at_yesterday, expected_rate, places=6,
                msg="invoice_currency_rate must reflect the rate at delivery_date"
            )

    def test_invoice_currency_rate_uses_delivery_date_over_invoice_date(self) -> None:
        """Verify invoice_currency_rate uses delivery_date rate, not invoice_date rate."""
        with freeze_time("2024-02-01"):
            currency_eur = self.env.ref("base.EUR")
            invoice = self.env["account.move"].create({
                "move_type": "out_invoice",
                "journal_id": self.company_data["default_journal_sale"].id,
                "currency_id": currency_eur.id,
                "partner_id": self.partner_company.id,
                "invoice_date": self.today,
                "delivery_date": self.yesterday,
                "invoice_line_ids": [
                    (0, 0, {
                        "product_id": self.product_a.id,
                        "price_unit": 100.0,
                        "quantity": 1,
                        "tax_ids": [(6, 0, self.tax_vat.ids)],
                    }),
                ],
            })
            # for HU invoices, the rate should be based on delivery_date
            expected_rate = self.env["res.currency"]._get_conversion_rate(
                from_currency=invoice.company_currency_id,
                to_currency=currency_eur,
                company=invoice.company_id,
                date=self.yesterday,
            )
            self.assertAlmostEqual(
                invoice.invoice_currency_rate, expected_rate, places=6,
                msg="invoice_currency_rate must use delivery_date rate for HU invoices"
            )
