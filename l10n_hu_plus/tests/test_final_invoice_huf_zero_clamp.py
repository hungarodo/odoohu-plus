# -*- coding: utf-8 -*-
# author: Online ERP
from __future__ import annotations

from unittest.mock import PropertyMock, patch

from odoo import Command
from odoo.tests.common import tagged
from odoo.addons.l10n_hu_edi.tests.common import L10nHuEdiTestCommon

from freezegun import freeze_time


@tagged("post_install", "-at_install")
class TestFinalInvoiceHufZeroClamp(L10nHuEdiTestCommon):
    """Zero-clamp and document/NAV HUF totals for foreign-currency final invoices."""

    @classmethod
    def setUpClass(cls) -> None:
        with freeze_time("2024-02-01"):
            super().setUpClass()
            cls.currency_eur = cls.env.ref("base.EUR")
            cls.eur_journal = cls.env["account.journal"].create({
                "name": "EUR Sales Test",
                "type": "sale",
                "code": "EUST",
                "currency_id": cls.currency_eur.id,
            })

    def test_zero_clamp_threshold(self):
        move_model = self.env["account.move"]
        self.assertEqual(move_model._l10n_hu_zero_clamp_huf_amount(0.0), 0.0)
        self.assertEqual(move_model._l10n_hu_zero_clamp_huf_amount(0.01), 0.0)
        self.assertEqual(move_model._l10n_hu_zero_clamp_huf_amount(0.09), 0.0)
        self.assertEqual(move_model._l10n_hu_zero_clamp_huf_amount(-0.02), 0.0)
        self.assertEqual(move_model._l10n_hu_zero_clamp_huf_amount(0.10), 0.10)
        self.assertEqual(move_model._l10n_hu_zero_clamp_huf_amount(-0.15), -0.15)

    def test_company_currency_tax_totals_use_document_rate(self):
        invoice = self.env["account.move"].create({
            "move_type": "out_invoice",
            "partner_id": self.partner_company.id,
            "journal_id": self.eur_journal.id,
            "currency_id": self.currency_eur.id,
            "invoice_date": self.today,
            "delivery_date": self.today,
            "invoice_line_ids": [Command.create({
                "product_id": self.product_a.id,
                "quantity": 1,
                "price_unit": 100.0,
                "tax_ids": [Command.set(self.tax_vat.ids)],
            })],
        })
        document_rate = invoice._l10n_hu_get_document_huf_rate()
        tax_totals = invoice._l10n_hu_get_company_currency_tax_totals_for_report()
        currency_huf = self.env.ref("base.HUF")

        self.assertAlmostEqual(
            tax_totals["base_amount"],
            currency_huf.round(invoice.amount_untaxed * document_rate),
        )
        self.assertAlmostEqual(
            tax_totals["total_amount"],
            currency_huf.round(invoice.amount_total * document_rate),
        )

    def test_zero_eur_final_invoice_report_huf_totals_are_zero(self):
        """Simulate PO261530-style EUR 0 invoice with 0.01 HUF accounting residual."""
        invoice = self.env["account.move"].create({
            "move_type": "out_invoice",
            "partner_id": self.partner_company.id,
            "journal_id": self.eur_journal.id,
            "currency_id": self.currency_eur.id,
            "invoice_date": self.today,
            "delivery_date": self.today,
            "invoice_line_ids": [Command.create({
                "product_id": self.product_a.id,
                "quantity": 1,
                "price_unit": 100.0,
                "tax_ids": [Command.set(self.tax_vat.ids)],
            })],
        })
        simulated_tax_totals = {
            "currency_id": self.currency_eur.id,
            "company_currency_id": self.env.ref("base.HUF").id,
            "display_in_company_currency": True,
            "same_tax_base": True,
            "base_amount_currency": 0.0,
            "tax_amount_currency": 0.0,
            "total_amount_currency": 0.0,
            "base_amount": 0.01,
            "tax_amount": 0.0,
            "total_amount": 0.01,
            "subtotals": [{
                "name": "Untaxed Amount",
                "base_amount_currency": 0.0,
                "tax_amount_currency": 0.0,
                "base_amount": 0.01,
                "tax_amount": 0.0,
                "tax_groups": [{
                    "group_name": "27% VAT",
                    "base_amount_currency": 0.0,
                    "tax_amount_currency": 0.0,
                    "base_amount": 0.01,
                    "tax_amount": 0.0,
                    "display_base_amount_currency": 0.0,
                    "display_base_amount": 0.01,
                }],
            }],
        }
        with patch.object(
            type(invoice),
            "tax_totals",
            new_callable=PropertyMock,
            return_value=simulated_tax_totals,
        ):
            report_totals = invoice._l10n_hu_get_company_currency_tax_totals_for_report()
            self.assertEqual(report_totals["total_amount"], 0.0)
            self.assertEqual(report_totals["base_amount"], 0.0)
            self.assertEqual(report_totals["subtotals"][0]["base_amount"], 0.0)

    def test_document_data_ignores_technical_huf_residual(self):
        invoice = self.env["account.move"].new({
            "move_type": "out_invoice",
            "company_id": self.company_data["company"],
            "currency_id": self.currency_eur,
            "invoice_currency_rate": 0.0028593486403797213,
            "amount_untaxed": 0.0,
            "amount_tax": 0.0,
            "amount_total": 0.0,
            "amount_untaxed_signed": 0.01,
            "amount_tax_signed": 0.0,
            "amount_total_signed": 0.01,
        })
        document_data = invoice.l10n_hu_plus_get_document_data({})
        self.assertFalse(document_data["huf_amount_diff"])
        self.assertEqual(document_data["l10n_hu_document_gross_huf"], 0.0)
