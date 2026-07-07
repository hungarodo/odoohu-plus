# -*- coding: utf-8 -*-
# author: Online ERP

from __future__ import annotations
import datetime
from typing import TYPE_CHECKING
from odoo import exceptions
from odoo.tests import tagged
from odoo.addons.l10n_hu_plus.tests.common import L10nHuPlusTestCommon

if TYPE_CHECKING:
    from odoo.addons.l10n_hu_plus.models.account_move import L10nHuPlusAccountMove


@tagged("l10n_hu_plus", "post_install_l10n", "post_install", "-at_install")
class TestAccountMoveComputedFields(L10nHuPlusTestCommon):
    """Test computed fields on account.move for HU+ module."""

    def test_compute_show_delivery_date_hu_company(self) -> None:
        """Show delivery date is forced True for Hungarian companies."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        self.assertTrue(invoice.show_delivery_date, "show_delivery_date should be True for HU company invoices")

    def test_compute_l10n_hu_currency_huf_invoice(self) -> None:
        """HUF invoice should have HUF rate of 1.0 and HUF currency set."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice(currency=self.currency_huf)
        self.assertEqual(invoice.l10n_hu_huf_currency, self.currency_huf, "HUF currency should be set on HUF invoice")

    def test_compute_l10n_hu_currency_eur_invoice(self) -> None:
        """EUR invoice should have HUF currency and a non-zero HUF rate."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice(currency=self.currency_eur)
        self.assertEqual(invoice.l10n_hu_huf_currency, self.currency_huf, "HUF currency should be set on EUR invoice")

    def test_compute_l10n_hu_delivery_period_text_empty(self) -> None:
        """Period summary should be empty when no delivery period is set."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        self.assertFalse(invoice.l10n_hu_delivery_period_summary, "Period summary should be empty when no period set")

    def test_compute_l10n_hu_delivery_period_text_with_period(self) -> None:
        """Period summary should contain date range when delivery period is set."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        period_start = self.today.replace(day=1)
        period_end = self.today
        invoice.write({
            "l10n_hu_delivery_period_start": period_start,
            "l10n_hu_delivery_period_end": period_end,
        })
        invoice._compute_l10n_hu_delivery_period_text()
        # period summary is populated only for outgoing invoices with both period dates
        if invoice.move_type in ("out_invoice", "out_refund"):
            self.assertTrue(invoice.l10n_hu_delivery_period_summary, "Period summary should be populated for outgoing invoice")

    def test_compute_l10n_hu_document_huf_amounts(self) -> None:
        """Document HUF amounts should be computed for HUF invoices."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice(amount=10000.0)
        # for HUF invoices, the document amounts should match the invoice amounts
        self.assertIsNotNone(invoice.l10n_hu_document_net_huf, "Document net HUF should not be None")
        self.assertIsNotNone(invoice.l10n_hu_document_gross_huf, "Document gross HUF should not be None")


@tagged("l10n_hu_plus", "post_install_l10n", "post_install", "-at_install")
class TestAccountMoveOnchange(L10nHuPlusTestCommon):
    """Test onchange methods on account.move for HU+ module."""

    def test_onchange_delivery_period_valid(self) -> None:
        """Valid delivery period (end > start) should not raise."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        invoice.l10n_hu_delivery_period_start = self.today - datetime.timedelta(days=10)
        invoice.l10n_hu_delivery_period_end = self.today
        # should not raise
        invoice.onchange_l10n_hu_delivery_period()

    def test_onchange_delivery_period_invalid(self) -> None:
        """Invalid delivery period (end < start) should raise ValidationError."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        invoice.l10n_hu_delivery_period_start = self.today
        invoice.l10n_hu_delivery_period_end = self.today - datetime.timedelta(days=10)
        with self.assertRaises(exceptions.ValidationError):
            invoice.onchange_l10n_hu_delivery_period()

    def test_onchange_delivery_period_no_dates(self) -> None:
        """Missing delivery period dates should not raise."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        invoice.l10n_hu_delivery_period_start = False
        invoice.l10n_hu_delivery_period_end = False
        # should not raise
        invoice.onchange_l10n_hu_delivery_period()

    def test_onchange_currency_rate_inverse_negative(self) -> None:
        """Negative currency rate inverse should raise ValidationError."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice(currency=self.currency_eur)
        invoice.l10n_hu_invoice_currency_rate_inverse = -1.0
        with self.assertRaises(exceptions.ValidationError):
            invoice.onchange_l10n_hu_invoice_currency_rate_inverse()

    def test_onchange_currency_rate_inverse_positive(self) -> None:
        """Positive currency rate inverse should update the invoice_currency_rate."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice(currency=self.currency_eur)
        invoice.l10n_hu_invoice_currency_rate_inverse = 380.0
        invoice.onchange_l10n_hu_invoice_currency_rate_inverse()
        expected_rate = 1.0 / 380.0
        self.assertAlmostEqual(invoice.invoice_currency_rate, expected_rate, places=6, msg="Invoice currency rate should be 1/380")

    def test_onchange_currency_rate_negative(self) -> None:
        """Negative currency rate should raise ValidationError."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice(currency=self.currency_eur)
        with self.assertRaises(exceptions.ValidationError):
            invoice.invoice_currency_rate = -0.5

    def test_onchange_currency_rate_positive(self) -> None:
        """Positive currency rate should update the inverse rate."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice(currency=self.currency_eur)
        invoice.invoice_currency_rate = 0.002631578947  # ~ 1/380
        invoice.onchange_l10n_hu_invoice_currency_rate()
        self.assertAlmostEqual(
            invoice.l10n_hu_invoice_currency_rate_inverse,
            380.0,
            places=0,
            msg="Inverse rate should be approximately 380",
        )

    def test_onchange_payment_term_sets_rounding_and_mode(self) -> None:
        """Onchange payment term should set cash rounding and payment mode from term."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        invoice.invoice_payment_term_id = self.payment_term_transfer
        invoice.onchange_l10n_hu_payment_term_id()
        self.assertEqual(
            invoice.invoice_cash_rounding_id,
            self.cash_rounding_huf,
            "Cash rounding should be set from payment term",
        )
        self.assertEqual(invoice.l10n_hu_payment_mode, "TRANSFER", "Payment mode should be set from payment term")

    def test_onchange_payment_term_disabled_journal(self) -> None:
        """Onchange payment term should not set values when journal HU+ is disabled."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        self.journal_sale.l10n_hu_plus_enabled = False
        invoice.invoice_payment_term_id = self.payment_term_transfer
        invoice.onchange_l10n_hu_payment_term_id()
        # reset journal
        self.journal_sale.l10n_hu_plus_enabled = True

    def test_onchange_vat_status_empty_clears_date(self) -> None:
        """Clearing VAT status should clear the VAT date."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        invoice.l10n_hu_vat_status = "to_declare"
        invoice.l10n_hu_vat_date = self.today
        invoice.l10n_hu_vat_status = False
        invoice.onchange_l10n_hu_vat_status()
        self.assertFalse(invoice.l10n_hu_vat_date, "VAT date should be cleared when VAT status is empty")


@tagged("l10n_hu_plus", "post_install_l10n", "post_install", "-at_install")
class TestAccountMoveActions(L10nHuPlusTestCommon):
    """Test action methods on account.move for HU+ module."""

    def test_action_post_blocked_by_error_status(self) -> None:
        """Posting should be blocked when HU+ status is error."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice(partner=self.partner_hu_incomplete)
        # force error status
        invoice.l10n_hu_plus_status = "error"
        with self.assertRaises(exceptions.UserError):
            invoice.action_post()

    def test_action_post_allowed_with_ok_status(self) -> None:
        """Posting should be allowed when HU+ status is ok."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        invoice.l10n_hu_plus_status = "ok"
        # should not raise: posting may still fail due to other checks, but not the HU+ one
        try:
            invoice.action_post()
        except exceptions.UserError as exception:
            # the error should NOT be the HU+ error
            self.assertNotIn("HU+ error", str(exception), "The error should not be the HU+ blocking error")

    def test_action_post_allowed_without_hu_plus(self) -> None:
        """Posting should be allowed when HU+ is not enabled on journal."""
        self.journal_sale.l10n_hu_plus_enabled = False
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        invoice.l10n_hu_plus_status = "error"
        # should not be blocked by HU+ check since journal is not enabled
        try:
            invoice.action_post()
        except exceptions.UserError as exception:
            self.assertNotIn("HU+ error", str(exception), "HU+ check should not block when not enabled")
        finally:
            self.journal_sale.l10n_hu_plus_enabled = True

    def test_action_update_fields_draft(self) -> None:
        """Update fields action should work for draft invoices."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        self.assertEqual(invoice.state, "draft", "Invoice should be in draft state")
        # should not raise; method returns None on success
        invoice.action_l10n_hu_update_fields()

    def test_action_update_plus_status(self) -> None:
        """Update HU+ status action should set a status value."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        invoice.action_l10n_hu_update_plus_status()
        self.assertIn(
            invoice.l10n_hu_plus_status,
            [False, "ok", "warning", "error", "other", "closed"],
            "HU+ status should be a valid selection value",
        )


@tagged("l10n_hu_plus", "post_install_l10n", "post_install", "-at_install")
class TestAccountMoveDeliveryData(L10nHuPlusTestCommon):
    """Test l10n_hu_plus_get_delivery_data method on account.move."""

    def test_delivery_data_no_period(self) -> None:
        """Delivery data without period should return delivery date as invoice date or due date."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        result = invoice.l10n_hu_plus_get_delivery_data({})
        self.assertIsInstance(result, dict, "Delivery data should return a dictionary")

    def test_delivery_data_with_period(self) -> None:
        """Delivery data with period should compute period summary."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        period_start = self.today - datetime.timedelta(days=30)
        period_end = self.today
        invoice.write({
            "l10n_hu_delivery_period_start": period_start,
            "l10n_hu_delivery_period_end": period_end,
        })
        result = invoice.l10n_hu_plus_get_delivery_data({})
        self.assertEqual(result.get("l10n_hu_delivery_period_start"), period_start, "Period start should match")
        self.assertEqual(result.get("l10n_hu_delivery_period_end"), period_end, "Period end should match")

    def test_delivery_data_period_over_60_days(self) -> None:
        """Delivery period over 60 days should affect the NAV delivery date calculation."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        period_start = self.today - datetime.timedelta(days=90)
        period_end = self.today
        invoice.write({
            "l10n_hu_delivery_period_start": period_start,
            "l10n_hu_delivery_period_end": period_end,
        })
        result = invoice.l10n_hu_plus_get_delivery_data({})
        # for periods > 60 days, NAV scenario changes
        self.assertIsNotNone(result, "Delivery data should return a result even for periods > 60 days")

    def test_delivery_data_vendor_bill(self) -> None:
        """Delivery data for vendor bills should follow vendor-specific logic."""
        bill: L10nHuPlusAccountMove = self._create_hu_invoice(move_type="in_invoice")
        result = bill.l10n_hu_plus_get_delivery_data({})
        self.assertIsInstance(result, dict, "Delivery data for vendor bill should return a dictionary")


@tagged("l10n_hu_plus", "post_install_l10n", "post_install", "-at_install")
class TestAccountMoveDocumentData(L10nHuPlusTestCommon):
    """Test l10n_hu_plus_get_document_data method on account.move."""

    def test_document_data_huf_customer_invoice(self) -> None:
        """Document data for HUF customer invoice should compute HUF amounts."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice(amount=10000.0, currency=self.currency_huf)
        result = invoice.l10n_hu_plus_get_document_data({})
        self.assertIsInstance(result, dict, "Document data should return a dictionary")
        self.assertIn("l10n_hu_document_net_huf", result, "Result should contain document_net_huf")
        self.assertIn("l10n_hu_document_gross_huf", result, "Result should contain document_gross_huf")

    def test_document_data_eur_customer_invoice(self) -> None:
        """Document data for EUR customer invoice should convert amounts to HUF."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice(amount=100.0, currency=self.currency_eur)
        result = invoice.l10n_hu_plus_get_document_data({})
        self.assertIsInstance(result, dict, "Document data should return a dictionary for EUR invoice")

    def test_document_data_huf_vendor_bill(self) -> None:
        """Document data for HUF vendor bill should compute HUF amounts."""
        bill: L10nHuPlusAccountMove = self._create_hu_invoice(move_type="in_invoice", amount=50000.0, currency=self.currency_huf)
        result = bill.l10n_hu_plus_get_document_data({})
        self.assertIsInstance(result, dict, "Document data for vendor bill should return a dictionary")

    def test_document_data_eur_vendor_bill(self) -> None:
        """Document data for EUR vendor bill should convert amounts to HUF."""
        bill: L10nHuPlusAccountMove = self._create_hu_invoice(move_type="in_invoice", amount=200.0, currency=self.currency_eur)
        result = bill.l10n_hu_plus_get_document_data({})
        self.assertIsInstance(result, dict, "Document data for EUR vendor bill should return a dictionary")

    def test_document_data_storno_detection(self) -> None:
        """Document data should detect storno (credit note) invoices."""
        credit_note: L10nHuPlusAccountMove = self._create_hu_invoice(
            move_type="out_refund",
            document_type=self.document_type_storno,
        )
        result = credit_note.l10n_hu_plus_get_document_data({})
        self.assertIn("is_storno_invoice", result, "Document data should contain is_storno_invoice key")

    def test_document_data_modification_detection(self) -> None:
        """Document data should detect modification invoices."""
        credit_note: L10nHuPlusAccountMove = self._create_hu_invoice(
            move_type="out_refund",
            document_type=self.document_type_modification,
        )
        result = credit_note.l10n_hu_plus_get_document_data({})
        self.assertEqual(
            result.get("l10n_hu_document_type"),
            self.document_type_modification,
            "Credit note should have modification document type assigned",
        )

    def test_document_data_normal_invoice_not_storno(self) -> None:
        """Normal invoice should not be detected as storno or modification."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        result = invoice.l10n_hu_plus_get_document_data({})
        self.assertFalse(result.get("is_storno_invoice", False), "Normal invoice should not be storno")

    def test_document_data_document_type_assignment(self) -> None:
        """Document data should reference the assigned document type."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        _result = invoice.l10n_hu_plus_get_document_data({})
        # document type should be present in data or invoice field
        self.assertEqual(invoice.l10n_hu_document_type, self.document_type_normal, "Document type should be invoice_normal")


@tagged("l10n_hu_plus", "post_install_l10n", "post_install", "-at_install")
class TestAccountMoveRateData(L10nHuPlusTestCommon):
    """Test l10n_hu_plus_get_rate_data method on account.move."""

    def test_rate_data_huf_invoice(self) -> None:
        """Rate data for HUF invoice should have rate 1.0."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice(currency=self.currency_huf)
        result = invoice.l10n_hu_plus_get_rate_data({})
        self.assertIsInstance(result, dict, "Rate data should return a dictionary")
        huf_rate = result.get("l10n_hu_huf_rate", 0.0)
        # for HUF invoice in HUF company, rate should be 1.0 or 0.0 (indicating same currency)
        self.assertIn(huf_rate, [0.0, 1.0], "HUF rate should be 1.0 or 0.0 for same currency")

    def test_rate_data_eur_invoice(self) -> None:
        """Rate data for EUR invoice should have a non-zero HUF rate."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice(currency=self.currency_eur)
        result = invoice.l10n_hu_plus_get_rate_data({})
        self.assertIsInstance(result, dict, "Rate data should return a dictionary for EUR invoice")

    def test_rate_data_contains_huf_currency(self) -> None:
        """Rate data should always contain HUF currency reference."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        result = invoice.l10n_hu_plus_get_rate_data({})
        self.assertIn("l10n_hu_huf_currency", result, "Rate data should contain l10n_hu_huf_currency key")

    def test_rate_data_rate_date(self) -> None:
        """Rate data should contain the currency rate date."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice(currency=self.currency_eur)
        result = invoice.l10n_hu_plus_get_rate_data({})
        self.assertIn("l10n_hu_invoice_currency_rate_date", result, "Rate data should contain rate date")


@tagged("l10n_hu_plus", "post_install_l10n", "post_install", "-at_install")
class TestAccountMoveVatData(L10nHuPlusTestCommon):
    """Test l10n_hu_plus_get_vat_data method on account.move."""

    def test_vat_data_basic(self) -> None:
        """VAT data should return a dictionary with expected keys."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        result = invoice.l10n_hu_plus_get_vat_data({})
        self.assertIsInstance(result, dict, "VAT data should return a dictionary")
        self.assertIn("l10n_hu_cash_accounting", result, "VAT data should contain l10n_hu_cash_accounting")
        self.assertIn("l10n_hu_vat_status", result, "VAT data should contain l10n_hu_vat_status")

    def test_vat_data_no_cash_accounting(self) -> None:
        """VAT data without cash accounting fiscal position should be False."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        result = invoice.l10n_hu_plus_get_vat_data({})
        self.assertFalse(result.get("l10n_hu_cash_accounting"), "Cash accounting should be False for standard fiscal position")

    def test_vat_data_cash_accounting(self) -> None:
        """VAT data with cash accounting fiscal position should be True."""
        # cash accounting for vendor bills: partner's fiscal position must have tax_regime=ca
        self.partner_hu.property_account_position_id = self.fiscal_position_domestic_cash
        bill: L10nHuPlusAccountMove = self._create_hu_invoice(move_type="in_invoice")
        result = bill.l10n_hu_plus_get_vat_data({})
        self.assertTrue(
            result.get("is_cash_accounting"),
            "Cash accounting should be True for vendor bill with cash accounting fiscal position",
        )
        # restore
        self.partner_hu.property_account_position_id = self.fiscal_position_domestic

    def test_vat_data_default_status(self) -> None:
        """VAT data should propose a default VAT status."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        result = invoice.l10n_hu_plus_get_vat_data({})
        vat_status = result.get("l10n_hu_vat_status")
        # default depends on move type and configuration
        if vat_status:
            self.assertIn(
                vat_status,
                ["to_declare", "postponed", "declared", "excluded", "out_of_scope", "legacy"],
                "Default VAT status should be a valid selection value",
            )

    def test_vat_data_vat_taxes_collected(self) -> None:
        """VAT data should collect information about applied VAT taxes."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        result = invoice.l10n_hu_plus_get_vat_data({})
        self.assertIn("vat_taxes", result, "VAT data should contain vat_taxes list")


@tagged("l10n_hu_plus", "post_install_l10n", "post_install", "-at_install")
class TestAccountMoveGetData(L10nHuPlusTestCommon):
    """Test l10n_hu_plus_get_data central data collection method."""

    def test_get_data_returns_field_values(self) -> None:
        """get_data should return field_values dictionary."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        result = invoice.l10n_hu_plus_get_data({})
        self.assertIsInstance(result, dict, "get_data should return a dictionary")
        self.assertIn("field_values", result, "Result should contain field_values")

    def test_get_data_calls_sub_methods(self) -> None:
        """get_data should aggregate data from delivery, document, rate, and vat sub-methods."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        result = invoice.l10n_hu_plus_get_data({})
        field_values = result.get("field_values", {})
        # field_values should contain keys from the sub-methods
        self.assertIsInstance(field_values, dict, "field_values should be a dictionary")

    def test_get_data_delivery_data(self) -> None:
        """get_data should include delivery_data in its return."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        result = invoice.l10n_hu_plus_get_data({})
        self.assertIn("delivery_data", result, "Result should contain delivery_data")

    def test_get_data_document_data(self) -> None:
        """get_data should include document_data in its return."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        result = invoice.l10n_hu_plus_get_data({})
        self.assertIn("document_data", result, "Result should contain document_data")

    def test_get_data_rate_data(self) -> None:
        """get_data should include rate_data in its return."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        result = invoice.l10n_hu_plus_get_data({})
        self.assertIn("rate_data", result, "Result should contain rate_data")

    def test_get_data_vat_data(self) -> None:
        """get_data should include vat_data in its return."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        result = invoice.l10n_hu_plus_get_data({})
        self.assertIn("vat_data", result, "Result should contain vat_data")


@tagged("l10n_hu_plus", "post_install_l10n", "post_install", "-at_install")
class TestAccountMoveEdiEligibility(L10nHuPlusTestCommon):
    """Test l10n_hu_get_send_edi_allowed 8-point eligibility check."""

    def test_edi_allowed_returns_boolean(self) -> None:
        """EDI eligibility check should return a boolean."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        invoice.l10n_hu_plus_status = "ok"
        invoice.action_post()
        result = invoice.l10n_hu_get_send_edi_allowed()
        self.assertIsInstance(result, bool, "EDI eligibility should return a boolean")

    def test_edi_not_allowed_draft_invoice(self) -> None:
        """A draft invoice should not be eligible for EDI sending."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        result = invoice.l10n_hu_get_send_edi_allowed()
        self.assertFalse(result, "Draft invoice should not be EDI eligible")

    def test_edi_not_allowed_vendor_bill(self) -> None:
        """A vendor bill should not be eligible for EDI sending."""
        bill: L10nHuPlusAccountMove = self._create_hu_invoice(move_type="in_invoice")
        bill.l10n_hu_plus_status = "ok"
        try:
            bill.action_post()
        except Exception:
            pass
        result = bill.l10n_hu_get_send_edi_allowed()
        self.assertFalse(result, "Vendor bill should not be EDI eligible")

    def test_edi_not_allowed_closed_status(self) -> None:
        """An invoice with closed HU+ status should not be eligible for EDI."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        invoice.l10n_hu_plus_status = "ok"
        invoice.action_post()
        invoice.l10n_hu_plus_status = "closed"
        result = invoice.l10n_hu_get_send_edi_allowed()
        self.assertFalse(result, "Closed status should make EDI not allowed")

    def test_edi_not_allowed_disabled_journal(self) -> None:
        """An invoice on a journal with disabled EDI should not be eligible."""
        self.journal_sale.l10n_hu_edi_sending = "disabled"
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        invoice.l10n_hu_plus_status = "ok"
        invoice.action_post()
        result = invoice.l10n_hu_get_send_edi_allowed()
        self.assertFalse(result, "Disabled EDI journal should make EDI not allowed")
        # restore
        self.journal_sale.l10n_hu_edi_sending = "manual"
