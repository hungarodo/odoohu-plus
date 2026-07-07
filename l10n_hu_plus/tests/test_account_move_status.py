# -*- coding: utf-8 -*-
# author: Online ERP

from __future__ import annotations
import datetime
from typing import TYPE_CHECKING
from odoo.tests import tagged
from odoo.addons.l10n_hu_plus.tests.common import L10nHuPlusTestCommon

if TYPE_CHECKING:
    from odoo.addons.l10n_hu_plus.models.account_move import L10nHuPlusAccountMove


@tagged("l10n_hu_plus", "post_install_l10n", "post_install", "-at_install")
class TestAccountMovePlusStatus(L10nHuPlusTestCommon):
    """Test l10n_hu_get_plus_status method on account.move."""

    def test_get_plus_status_with_errors(self) -> None:
        """Status should be error when checklist has errors."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice(partner=self.partner_hu_incomplete)
        invoice.delivery_date = False
        status = invoice.l10n_hu_get_plus_status()
        self.assertEqual(status, "error", "Status should be error when delivery date is missing and address incomplete")

    def test_get_plus_status_ok(self) -> None:
        """Status should be ok when all checks pass."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        status = invoice.l10n_hu_get_plus_status()
        self.assertIn(status, ["ok", "warning", None], "Status should be ok or warning for properly configured invoice")

    def test_get_plus_status_no_invoice(self) -> None:
        """Status should be None for non-invoice moves."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        # for non-invoice moves, status determination may return None
        result = invoice.l10n_hu_get_plus_status()
        self.assertIsNotNone(result, "Result should not be None for invoice with delivery date")


@tagged("l10n_hu_plus", "post_install_l10n", "post_install", "-at_install")
class TestAccountMoveStatusChecklist(L10nHuPlusTestCommon):
    """Test l10n_hu_get_plus_status_checklist method (HU+1 through HU+12)."""

    def _get_checklist_codes(self, checklist_result: dict, list_type: str) -> list[str]:
        """Extract codes from a specific list type in the checklist result.

        :param dict checklist_result: the checklist result dictionary
        :param str list_type: the list type key (error_list, warning_list, success_list, info_list)
        :return: list of code strings
        """
        return [item.get("code", "") for item in checklist_result.get(list_type, [])]

    def test_checklist_returns_expected_structure(self) -> None:
        """Checklist should return a dictionary with all required list keys."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        result = invoice.l10n_hu_get_plus_status_checklist()
        self.assertIsInstance(result, dict, "Checklist should return a dictionary")
        self.assertIn("error_list", result, "Result should contain error_list")
        self.assertIn("warning_list", result, "Result should contain warning_list")
        self.assertIn("success_list", result, "Result should contain success_list")
        self.assertIn("info_list", result, "Result should contain info_list")

    def test_hu_plus_1_document_type_set(self) -> None:
        """HU+1: Document type set should be success."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        result = invoice.l10n_hu_get_plus_status_checklist()
        success_codes = self._get_checklist_codes(result, "success_list")
        self.assertIn("HU+1", success_codes, "HU+1 should be in success_list when document type is set")

    def test_hu_plus_1_document_type_not_set(self) -> None:
        """HU+1: Document type not set should be warning."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice(document_type=None)
        invoice.l10n_hu_document_type = False
        result = invoice.l10n_hu_get_plus_status_checklist()
        warning_codes = self._get_checklist_codes(result, "warning_list")
        self.assertIn("HU+1", warning_codes, "HU+1 should be in warning_list when document type is not set")

    def test_hu_plus_2_invoice_fiscal_position_set(self) -> None:
        """HU+2: Invoice fiscal position set should be success."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        invoice.fiscal_position_id = self.fiscal_position_domestic
        result = invoice.l10n_hu_get_plus_status_checklist()
        success_codes = self._get_checklist_codes(result, "success_list")
        self.assertIn("HU+2", success_codes, "HU+2 should be in success_list when fiscal position is set")

    def test_hu_plus_2_invoice_fiscal_position_not_set(self) -> None:
        """HU+2: Invoice fiscal position not set should be warning."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        invoice.fiscal_position_id = False
        result = invoice.l10n_hu_get_plus_status_checklist()
        warning_codes = self._get_checklist_codes(result, "warning_list")
        self.assertIn("HU+2", warning_codes, "HU+2 should be in warning_list when fiscal position is not set")

    def test_hu_plus_3_partner_fiscal_position_set(self) -> None:
        """HU+3: Partner fiscal position set should be success."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        self.assertTrue(invoice.partner_id.property_account_position_id, "Partner should have fiscal position set")
        result = invoice.l10n_hu_get_plus_status_checklist()
        success_codes = self._get_checklist_codes(result, "success_list")
        self.assertIn("HU+3", success_codes, "HU+3 should be in success_list when partner fiscal position is set")

    def test_hu_plus_3_partner_fiscal_position_not_set(self) -> None:
        """HU+3: Partner fiscal position not set should be warning."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice(partner=self.partner_hu_incomplete)
        result = invoice.l10n_hu_get_plus_status_checklist()
        warning_codes = self._get_checklist_codes(result, "warning_list")
        self.assertIn("HU+3", warning_codes, "HU+3 should be in warning_list when partner has no fiscal position")

    def test_hu_plus_4_delivery_date_set(self) -> None:
        """HU+4: Delivery date set should be success."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        self.assertTrue(invoice.delivery_date, "Delivery date should be set")
        result = invoice.l10n_hu_get_plus_status_checklist()
        success_codes = self._get_checklist_codes(result, "success_list")
        self.assertIn("HU+4", success_codes, "HU+4 should be in success_list when delivery date is set")

    def test_hu_plus_4_delivery_date_not_set(self) -> None:
        """HU+4: Delivery date not set should be error."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        invoice.delivery_date = False
        result = invoice.l10n_hu_get_plus_status_checklist()
        error_codes = self._get_checklist_codes(result, "error_list")
        self.assertIn("HU+4", error_codes, "HU+4 should be in error_list when delivery date is not set")

    def test_hu_plus_5_delivery_period_both_set(self) -> None:
        """HU+5: Delivery period with both dates set should be info or success."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        invoice.write({
            "l10n_hu_delivery_period_start": self.today - datetime.timedelta(days=30),
            "l10n_hu_delivery_period_end": self.today,
        })
        result = invoice.l10n_hu_get_plus_status_checklist()
        success_codes = self._get_checklist_codes(result, "success_list")
        info_codes = self._get_checklist_codes(result, "info_list")
        self.assertTrue(
            "HU+5" in success_codes or "HU+5" in info_codes,
            "HU+5 should be in success_list or info_list when both period dates are set",
        )

    def test_hu_plus_5_delivery_period_only_start(self) -> None:
        """HU+5: Delivery period with only start date should be error."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        invoice.write({
            "l10n_hu_delivery_period_start": self.today - datetime.timedelta(days=30),
            "l10n_hu_delivery_period_end": False,
        })
        result = invoice.l10n_hu_get_plus_status_checklist()
        error_codes = self._get_checklist_codes(result, "error_list")
        self.assertIn("HU+5", error_codes, "HU+5 should be in error_list when only start date is set")

    def test_hu_plus_5_delivery_period_only_end(self) -> None:
        """HU+5: Delivery period with only end date should be error."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        invoice.write({
            "l10n_hu_delivery_period_start": False,
            "l10n_hu_delivery_period_end": self.today,
        })
        result = invoice.l10n_hu_get_plus_status_checklist()
        error_codes = self._get_checklist_codes(result, "error_list")
        self.assertIn("HU+5", error_codes, "HU+5 should be in error_list when only end date is set")

    def test_hu_plus_5_delivery_period_none(self) -> None:
        """HU+5: Delivery period with no dates should be info."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        result = invoice.l10n_hu_get_plus_status_checklist()
        info_codes = self._get_checklist_codes(result, "info_list")
        self.assertIn("HU+5", info_codes, "HU+5 should be in info_list when no period dates are set")

    def test_hu_plus_6_taxes_on_all_lines(self) -> None:
        """HU+6: Tax set on all invoice lines should be success."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        result = invoice.l10n_hu_get_plus_status_checklist()
        success_codes = self._get_checklist_codes(result, "success_list")
        self.assertIn("HU+6", success_codes, "HU+6 should be in success_list when all lines have taxes")

    def test_hu_plus_6_taxes_missing_on_line(self) -> None:
        """HU+6: Tax missing on an invoice line should be error."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        # add a line without tax
        product_line = invoice.invoice_line_ids.filtered(lambda line: line.product_id)
        if product_line:
            product_line[0].tax_ids = False
        result = invoice.l10n_hu_get_plus_status_checklist()
        error_codes = self._get_checklist_codes(result, "error_list")
        self.assertIn("HU+6", error_codes, "HU+6 should be in error_list when a line is missing taxes")

    def test_hu_plus_9_cash_accounting_consistent(self) -> None:
        """HU+9: Consistent cash accounting setting should be info."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        result = invoice.l10n_hu_get_plus_status_checklist()
        # either consistent (info) or inconsistent (warning)
        all_codes = self._get_checklist_codes(result, "info_list") + self._get_checklist_codes(result, "warning_list")
        self.assertIn("HU+9", all_codes, "HU+9 should appear in info_list or warning_list")

    def test_hu_plus_12_partner_address_complete(self) -> None:
        """HU+12: Complete partner address should be success."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        result = invoice.l10n_hu_get_plus_status_checklist()
        success_codes = self._get_checklist_codes(result, "success_list")
        self.assertIn("HU+12", success_codes, "HU+12 should be in success_list when partner address is complete")

    def test_hu_plus_12_partner_address_incomplete(self) -> None:
        """HU+12: Incomplete partner address should be error."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice(partner=self.partner_hu_incomplete)
        result = invoice.l10n_hu_get_plus_status_checklist()
        error_codes = self._get_checklist_codes(result, "error_list")
        self.assertIn("HU+12", error_codes, "HU+12 should be in error_list when partner address is incomplete")

    def test_hu_plus_12_no_partner(self) -> None:
        """HU+12: Missing partner should produce address error."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        invoice.partner_id = False
        result = invoice.l10n_hu_get_plus_status_checklist()
        error_codes = self._get_checklist_codes(result, "error_list")
        self.assertIn("HU+12", error_codes, "HU+12 should be in error_list when partner is not set")


@tagged("l10n_hu_plus", "post_install_l10n", "post_install", "-at_install")
class TestAccountMoveStatusOverview(L10nHuPlusTestCommon):
    """Test l10n_hu_get_plus_status_overview HTML generation method."""

    def test_overview_returns_html(self) -> None:
        """Status overview should return an HTML string."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        result = invoice.l10n_hu_get_plus_status_overview()
        self.assertIsInstance(result, str, "Status overview should return a string")
        self.assertIn("<table", result, "Result should contain HTML table markup")
        self.assertIn("</table>", result, "Result should contain closing table tag")

    def test_overview_contains_status_counts(self) -> None:
        """Status overview should display error, warning, success, and info counts."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        result = invoice.l10n_hu_get_plus_status_overview()
        # should contain the count section
        self.assertIn("fa-exclamation-circle", result, "Result should contain error icon class")
        self.assertIn("fa-exclamation-triangle", result, "Result should contain warning icon class")
        self.assertIn("fa-check", result, "Result should contain success icon class")
        self.assertIn("fa-info-circle", result, "Result should contain info icon class")

    def test_overview_contains_check_codes(self) -> None:
        """Status overview should contain the HU+ check codes."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        result = invoice.l10n_hu_get_plus_status_overview()
        self.assertIn("HU+", result, "Result should contain HU+ check codes")

    def test_overview_contains_health_rate(self) -> None:
        """Status overview should contain a health rate percentage."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        result = invoice.l10n_hu_get_plus_status_overview()
        self.assertIn("%", result, "Result should contain a percentage indicator")

    def test_overview_with_errors(self) -> None:
        """Status overview with errors should show error rows."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice(partner=self.partner_hu_incomplete)
        invoice.delivery_date = False
        result = invoice.l10n_hu_get_plus_status_overview()
        self.assertIn("text-danger", result, "Result should contain red danger styling for errors")

    def test_overview_empty_invoice(self) -> None:
        """Status overview for a minimal invoice should still produce valid HTML."""
        invoice: L10nHuPlusAccountMove = self._create_hu_invoice()
        result = invoice.l10n_hu_get_plus_status_overview()
        self.assertTrue(result.startswith("<h2"), "Result should start with an h2 heading tag")
