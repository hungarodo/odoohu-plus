# -*- coding: utf-8 -*-
# author: Online ERP
from __future__ import annotations

from unittest.mock import patch

from odoo.tests.common import tagged
from odoo.addons.l10n_hu_edi.tests.common import L10nHuEdiTestCommon

from freezegun import freeze_time


@tagged("post_install", "-at_install")
class TestNavInvoiceSummaryConsistency(L10nHuEdiTestCommon):
    """Test suite for NAV invoice summary rounding fix.

    Tests cover:
    - Invoice summary totals are consistent with per-VAT-rate breakdown
    - Fix prevents INCORRECT_SUMMARY_CALCULATION NAV warnings
    """

    @classmethod
    def setUpClass(cls) -> None:
        """Set up test fixtures: posted invoices with amounts that trigger rounding."""
        with freeze_time("2024-02-01"):
            super().setUpClass()

    # -------------------------------------------------------------------------
    # HELPERS
    # -------------------------------------------------------------------------

    def _assert_nav_summary_consistency(self, invoice_values: dict) -> None:
        """Assert that NAV summary totals are internally consistent with per-VAT-rate values.

        :param dict invoice_values: result of _l10n_hu_edi_get_invoice_values()
        """
        tax_summary = invoice_values["tax_summary"]
        sum_net = sum(tv["vatRateNetAmount"] for tv in tax_summary)
        sum_net_huf = sum(tv["vatRateNetAmountHUF"] for tv in tax_summary)
        sum_vat = sum(tv["vatRateVatAmount"] for tv in tax_summary)
        sum_vat_huf = sum(tv["vatRateVatAmountHUF"] for tv in tax_summary)
        self.assertEqual(
            invoice_values["invoiceNetAmount"], sum_net,
            "invoiceNetAmount must equal sum of vatRateNetAmount values"
        )
        self.assertEqual(
            invoice_values["invoiceNetAmountHUF"], sum_net_huf,
            "invoiceNetAmountHUF must equal sum of vatRateNetAmountHUF values"
        )
        expected_gross = invoice_values["invoice"].currency_id.round(sum_net + sum_vat)
        expected_gross_huf = self.env.ref("base.HUF").round(sum_net_huf + sum_vat_huf)
        self.assertEqual(
            invoice_values["invoiceGrossAmount"], expected_gross,
            "invoiceGrossAmount must equal net + vat"
        )
        self.assertEqual(
            invoice_values["invoiceGrossAmountHUF"], expected_gross_huf,
            "invoiceGrossAmountHUF must equal netHUF + vatHUF"
        )

    # -------------------------------------------------------------------------
    # TEST: SUMMARY CONSISTENCY WITH SIMULATED ROUNDING MISMATCH
    # -------------------------------------------------------------------------

    def test_summary_consistent_when_amount_total_differs_from_line_sum(self) -> None:
        """Verify invoice summary stays consistent even when amount_total diverges from per-line sum."""
        with freeze_time("2024-02-01"):
            invoice = self.create_invoice_simple()
            invoice.action_post()
            # simulate the real-world rounding mismatch: amount_total deviates by 1 HUF
            real_total = invoice.amount_total_in_currency_signed
            real_total_signed = invoice.amount_total_signed
            with patch.object(
                type(invoice), "amount_total_in_currency_signed",
                new_callable=lambda: property(lambda self: real_total + 1)
            ), patch.object(
                type(invoice), "amount_total_signed",
                new_callable=lambda: property(lambda self: real_total_signed + 1)
            ):
                result = invoice._l10n_hu_edi_get_invoice_values()
            self._assert_nav_summary_consistency(result)

    def test_summary_consistent_multi_line_eur_invoice(self) -> None:
        """Verify invoice summary consistency for multi-line EUR invoice with rate conversion."""
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
                        "price_unit": 17.13,
                        "quantity": 3,
                        "tax_ids": [(6, 0, self.tax_vat.ids)],
                    }),
                    (0, 0, {
                        "product_id": self.product_b.id,
                        "price_unit": 23.47,
                        "quantity": 7,
                        "tax_ids": [(6, 0, self.tax_vat.ids)],
                    }),
                    (0, 0, {
                        "product_id": self.product_service.id,
                        "price_unit": 9.99,
                        "quantity": 11,
                        "tax_ids": [(6, 0, self.tax_vat.ids)],
                    }),
                ],
            })
            invoice.action_post()
            real_total = invoice.amount_total_in_currency_signed
            real_total_signed = invoice.amount_total_signed
            with patch.object(
                type(invoice), "amount_total_in_currency_signed",
                new_callable=lambda: property(lambda self: real_total + 0.01)
            ), patch.object(
                type(invoice), "amount_total_signed",
                new_callable=lambda: property(lambda self: real_total_signed + 1)
            ):
                result = invoice._l10n_hu_edi_get_invoice_values()
            self._assert_nav_summary_consistency(result)

    def test_summary_consistent_without_mock(self) -> None:
        """Verify invoice summary consistency holds for a normal posted invoice (no mock)."""
        with freeze_time("2024-02-01"):
            invoice = self.create_invoice_simple()
            invoice.action_post()
            result = invoice._l10n_hu_edi_get_invoice_values()
            self._assert_nav_summary_consistency(result)
