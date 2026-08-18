# -*- coding: utf-8 -*-
# author: Online ERP
from __future__ import annotations
from typing import TYPE_CHECKING
from freezegun import freeze_time
from odoo import Command
from odoo.tests.common import tagged
from odoo.addons.l10n_hu_edi.tests.common import L10nHuEdiTestCommon

if TYPE_CHECKING:
    from odoo.addons.base.models.res_currency import Currency
    from odoo.addons.l10n_hu_plus.models.account_move import L10nHuPlusAccountMove


@tagged("l10n_hu_plus", "post_install_l10n", "post_install", "-at_install")
class TestAccountMoveCurrencyCompute(L10nHuEdiTestCommon):
    """Test suite for _compute_l10n_hu_currency on account.move.

    Tests cover:
    - Opening a company-currency invoice does not raise RecursionError
    - Company-currency invoices get document rate 1.0 when no currency rate exists
    - Foreign-currency invoices keep a manually set document rate
    - Foreign-currency invoices take the accounting rate from res.currency.rate
    """

    @classmethod
    def setUpClass(cls, chart_template_ref: str = "hu") -> None:
        """Set up HU invoicing fixtures with a frozen invoice date."""
        with freeze_time("2024-02-01"):
            super().setUpClass(chart_template_ref=chart_template_ref)

    # -------------------------------------------------------------------------
    # HELPERS
    # -------------------------------------------------------------------------

    def _create_invoice(self, currency: Currency | None = None, document_rate: float = 0.0) -> L10nHuPlusAccountMove:
        """Create a customer invoice with one product line.

        :param Currency | None currency: invoice currency, defaults to company currency
        :param float document_rate: stored HU document rate written on the invoice
        :return: the created invoice
        :rtype: L10nHuPlusAccountMove
        """
        if currency is None:
            currency = self.company_data["company"].currency_id
        return self.env["account.move"].create({
            "move_type": "out_invoice",
            "journal_id": self.company_data["default_journal_sale"].id,
            "currency_id": currency.id,
            "partner_id": self.partner_company.id,
            "invoice_date": self.today,
            "delivery_date": self.today,
            "l10n_hu_document_rate": document_rate,
            "invoice_line_ids": [
                Command.create({
                    "product_id": self.product_a.id,
                    "price_unit": 100.0,
                    "quantity": 1,
                    "tax_ids": [Command.set(self.tax_vat.ids)],
                }),
            ],
        })

    # -------------------------------------------------------------------------
    # TEST: _COMPUTE_L10N_HU_CURRENCY
    # -------------------------------------------------------------------------

    def test_compute_l10n_hu_currency_company_currency_does_not_recurse(self) -> None:
        """Verify web_read of HU currency fields on a HUF invoice does not raise RecursionError."""
        invoice = self._create_invoice()
        values_list = invoice.web_read({
            "l10n_hu_currency_rate": {},
            "l10n_hu_currency_date": {},
            "l10n_hu_document_rate": {},
            "l10n_hu_document_rate_difference": {},
            "line_ids": {},
        })
        self.assertEqual(len(values_list), 1)
        self.assertEqual(values_list[0]["l10n_hu_currency_rate"], 1.0)
        self.assertEqual(values_list[0]["l10n_hu_document_rate"], 1.0)

    def test_compute_l10n_hu_currency_sets_document_rate_when_no_last_rate(self) -> None:
        """Verify a company-currency invoice gets document rate 1.0 when no currency rate exists."""
        invoice = self._create_invoice()
        invoice.invalidate_recordset(["l10n_hu_currency_rate", "l10n_hu_currency_date", "l10n_hu_document_rate"])
        self.assertEqual(invoice.l10n_hu_currency_rate, 1.0)
        self.assertEqual(invoice.l10n_hu_document_rate, 1.0)

    def test_compute_l10n_hu_currency_keeps_manual_document_rate(self) -> None:
        """Verify a foreign-currency invoice keeps a manually set document rate."""
        currency_eur = self.env.ref("base.EUR")
        invoice = self._create_invoice(currency=currency_eur)
        invoice.l10n_hu_document_rate = 2.5
        invoice.invalidate_recordset(["l10n_hu_currency_rate", "l10n_hu_currency_date", "l10n_hu_document_rate"])
        self.assertEqual(invoice.l10n_hu_document_rate, 2.5)

    def test_compute_l10n_hu_currency_uses_last_rate_for_foreign_currency(self) -> None:
        """Verify a EUR invoice uses inverse_company_rate from the matching currency rate."""
        currency_eur = self.env.ref("base.EUR")
        invoice = self._create_invoice(currency=currency_eur)
        last_rate = self.env["res.currency.rate"].search([
            ("company_id", "=", invoice.company_id.id),
            ("currency_id", "=", currency_eur.id),
            ("name", "<=", invoice.delivery_date),
        ], limit=1)
        self.assertTrue(last_rate)
        self.assertAlmostEqual(invoice.l10n_hu_currency_rate, last_rate.inverse_company_rate, places=6)
        self.assertAlmostEqual(invoice.l10n_hu_document_rate, last_rate.inverse_company_rate, places=6)
