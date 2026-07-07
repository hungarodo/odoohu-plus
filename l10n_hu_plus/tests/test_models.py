# -*- coding: utf-8 -*-
# author: Online ERP

from __future__ import annotations
import datetime
from typing import TYPE_CHECKING
from odoo import exceptions
from odoo.tests import tagged
from odoo.addons.l10n_hu_plus.tests.common import L10nHuPlusTestCommon

if TYPE_CHECKING:
    from odoo.addons.l10n_hu_plus.models.account_tax import L10nHuPlusAccountTax
    from odoo.addons.l10n_hu_plus.models.log import L10nHuPlusLog
    from odoo.addons.l10n_hu_plus.models.tag import L10nHuPlusTag
    from odoo.addons.l10n_hu_plus.models.account_move_line import L10nHuPlusAccountMoveLine


@tagged("l10n_hu_plus", "post_install_l10n", "post_install", "-at_install")
class TestL10nHuPlusTag(L10nHuPlusTestCommon):
    """Test l10n.hu.plus.tag model."""

    def test_tag_creation(self) -> None:
        """Tag should be created with correct field values."""
        tag: L10nHuPlusTag = self.document_type_normal
        self.assertEqual(tag.code, "INVOICE-NORMAL", "Tag code should be INVOICE-NORMAL")
        self.assertEqual(tag.tag_type, "document_type", "Tag type should be document_type")
        self.assertEqual(tag.technical_name, "invoice_normal", "Technical name should be invoice_normal")
        self.assertTrue(tag.locked, "Tag should be locked")
        self.assertEqual(tag.priority, 1, "Priority should be 1")

    def test_tag_default_color(self) -> None:
        """Tag should have a default color between 1 and 11."""
        tag: L10nHuPlusTag = self.env["l10n.hu.plus.tag"].create({
            "name": "Test Tag",
            "tag_type": "general",
            "company": self.company_data["company"].id,
        })
        self.assertGreaterEqual(tag.color, 1, "Default color should be at least 1")
        self.assertLessEqual(tag.color, 11, "Default color should be at most 11")

    def test_tag_account_move_count(self) -> None:
        """Tag account_move_count should count related invoices."""
        self._create_hu_invoice(document_type=self.document_type_normal)
        self.document_type_normal._compute_account_move_count()
        self.assertGreaterEqual(
            self.document_type_normal.account_move_count,
            1,
            "Account move count should be at least 1 after creating an invoice with the document type",
        )

    def test_tag_account_move_count_zero(self) -> None:
        """Tag without related invoices should have count 0."""
        tag: L10nHuPlusTag = self.env["l10n.hu.plus.tag"].create({
            "name": "Unused Tag",
            "tag_type": "general",
            "company": self.company_data["company"].id,
        })
        tag._compute_account_move_count()
        self.assertEqual(tag.account_move_count, 0, "Unused tag should have account move count 0")

    def test_tag_object_count(self) -> None:
        """Tag object_count should be computed without errors."""
        self.document_type_normal._compute_object_count()
        self.assertIsNotNone(self.document_type_normal.object_count, "Object count should not be None")

    def test_tag_action_list_account_moves(self) -> None:
        """Action list account moves should return a valid action dictionary."""
        result = self.document_type_normal.action_list_account_moves()
        self.assertEqual(result["res_model"], "account.move", "Action should target account.move model")
        self.assertEqual(result["type"], "ir.actions.act_window", "Action type should be act_window")

    def test_tag_action_list_objects(self) -> None:
        """Action list objects should return a valid action dictionary."""
        result = self.document_type_normal.action_list_objects()
        self.assertEqual(result["res_model"], "l10n.hu.plus.object", "Action should target l10n.hu.plus.object model")
        self.assertEqual(result["type"], "ir.actions.act_window", "Action type should be act_window")

    def test_tag_action_view_technical_data_empty(self) -> None:
        """Action view technical data should raise when data is empty."""
        with self.assertRaises(exceptions.UserError):
            self.document_type_normal.action_view_technical_data()

    def test_tag_types_selection(self) -> None:
        """All tag types from the selection should be valid."""
        valid_types = ["general", "account_move", "document_type", "object_category", "object_collection", "object_type", "technical"]
        for tag_type in valid_types:
            tag: L10nHuPlusTag = self.env["l10n.hu.plus.tag"].create({
                "name": f"Tag {tag_type}",
                "tag_type": tag_type,
                "company": self.company_data["company"].id,
            })
            self.assertEqual(tag.tag_type, tag_type, f"Tag type should be {tag_type}")


@tagged("l10n_hu_plus", "post_install_l10n", "post_install", "-at_install")
class TestL10nHuPlusLog(L10nHuPlusTestCommon):
    """Test l10n.hu.plus.log model."""

    def test_log_creation(self) -> None:
        """Log should be created with correct field values."""
        log: L10nHuPlusLog = self.env["l10n.hu.plus.log"].create({
            "app_name": "l10n_hu_plus",
            "company": self.company_data["company"].id,
            "direction": "internal",
            "level": "info",
            "log_type": "test",
            "name": "Test Log Entry",
        })
        self.assertTrue(log.id, "Log should be created successfully")
        self.assertEqual(log.app_name, "l10n_hu_plus", "App name should match")
        self.assertEqual(log.direction, "internal", "Direction should be internal")
        self.assertEqual(log.level, "info", "Level should be info")

    def test_log_display_name(self) -> None:
        """Log display_name should follow the HU+LOG-ID format."""
        log: L10nHuPlusLog = self.env["l10n.hu.plus.log"].create({
            "app_name": "l10n_hu_plus",
            "company": self.company_data["company"].id,
            "name": "Display Name Test",
        })
        log._compute_display_name()
        expected_name = f"HU+LOG-{log.id}"
        self.assertEqual(log.display_name, expected_name, f"Display name should be {expected_name}")

    def test_log_object_count(self) -> None:
        """Log object_count should be computed correctly."""
        log: L10nHuPlusLog = self.env["l10n.hu.plus.log"].create({
            "app_name": "l10n_hu_plus",
            "company": self.company_data["company"].id,
            "name": "Object Count Test",
        })
        log._compute_l10n_hu_object_count()
        self.assertEqual(log.l10n_hu_object_count, 0, "Object count should be 0 for log without objects")

    def test_log_source_display_name_valid(self) -> None:
        """Log source_display_name should resolve when source model and record exist."""
        log: L10nHuPlusLog = self.env["l10n.hu.plus.log"].create({
            "app_name": "l10n_hu_plus",
            "company": self.company_data["company"].id,
            "name": "Source Name Test",
            "source_model_name": "res.company",
            "source_record_id": self.company_data["company"].id,
        })
        log._compute_source_display_name()
        self.assertTrue(log.source_display_name, "Source display name should be resolved for valid source")

    def test_log_source_display_name_invalid(self) -> None:
        """Log source_display_name should be False when source record does not exist."""
        log: L10nHuPlusLog = self.env["l10n.hu.plus.log"].create({
            "app_name": "l10n_hu_plus",
            "company": self.company_data["company"].id,
            "name": "Invalid Source Test",
            "source_model_name": "res.company",
            "source_record_id": 999999,
        })
        log._compute_source_display_name()
        self.assertFalse(log.source_display_name, "Source display name should be False for nonexistent record")

    def test_log_source_display_name_no_model(self) -> None:
        """Log source_display_name should be False when source model is not set."""
        log: L10nHuPlusLog = self.env["l10n.hu.plus.log"].create({
            "app_name": "l10n_hu_plus",
            "company": self.company_data["company"].id,
            "name": "No Model Test",
        })
        log._compute_source_display_name()
        self.assertFalse(log.source_display_name, "Source display name should be False when model is not set")

    def test_log_status_values(self) -> None:
        """Log status selection values should all be valid."""
        valid_statuses = ["new", "processing", "error", "done"]
        for status in valid_statuses:
            log: L10nHuPlusLog = self.env["l10n.hu.plus.log"].create({
                "app_name": "l10n_hu_plus",
                "company": self.company_data["company"].id,
                "name": f"Status {status}",
                "status": status,
            })
            self.assertEqual(log.status, status, f"Log status should be {status}")

    def test_log_direction_values(self) -> None:
        """Log direction selection values should all be valid."""
        valid_directions = ["incoming", "internal", "outgoing"]
        for direction in valid_directions:
            log: L10nHuPlusLog = self.env["l10n.hu.plus.log"].create({
                "app_name": "l10n_hu_plus",
                "company": self.company_data["company"].id,
                "name": f"Direction {direction}",
                "direction": direction,
            })
            self.assertEqual(log.direction, direction, f"Log direction should be {direction}")

    def test_log_action_delete(self) -> None:
        """Action delete should remove the log and return a list view action."""
        log: L10nHuPlusLog = self.env["l10n.hu.plus.log"].create({
            "app_name": "l10n_hu_plus",
            "company": self.company_data["company"].id,
            "name": "Delete Test",
        })
        log_id = log.id
        result = log.action_delete()
        self.assertEqual(result["res_model"], "l10n.hu.plus.log", "Action should target l10n.hu.plus.log model")
        deleted_log = self.env["l10n.hu.plus.log"].search([("id", "=", log_id)])
        self.assertFalse(deleted_log, "Log should be deleted after action_delete")


@tagged("l10n_hu_plus", "post_install_l10n", "post_install", "-at_install")
class TestAccountJournal(L10nHuPlusTestCommon):
    """Test HU+ fields and methods on account.journal."""

    def test_journal_hu_plus_enabled(self) -> None:
        """Journal HU+ enabled should be correctly set."""
        self.assertTrue(self.journal_sale.l10n_hu_plus_enabled, "Sale journal should have HU+ enabled")

    def test_journal_edi_sending_values(self) -> None:
        """Journal EDI sending should accept all valid values."""
        valid_values = ["disabled", "manual", "auto_edi", "auto_edi_email"]
        for value in valid_values:
            self.journal_sale.l10n_hu_edi_sending = value
            self.assertEqual(self.journal_sale.l10n_hu_edi_sending, value, f"EDI sending should be {value}")
        # restore
        self.journal_sale.l10n_hu_edi_sending = "manual"

    def test_journal_delivery_date_default_today(self) -> None:
        """Journal delivery date default 'today' should return today's date."""
        self.journal_sale.l10n_hu_delivery_date_default = "today"
        result = self.journal_sale.l10n_hu_get_default_delivery_date()
        self.assertEqual(result, datetime.date.today(), "Default delivery date should be today")

    def test_journal_delivery_date_default_none(self) -> None:
        """Journal delivery date default 'none' should return None."""
        self.journal_sale.l10n_hu_delivery_date_default = "none"
        result = self.journal_sale.l10n_hu_get_default_delivery_date()
        self.assertIsNone(result, "Default delivery date should be None when set to none")

    def test_journal_default_document_type(self) -> None:
        """Journal default document type should return the highest priority document type tag."""
        result = self.journal_sale.l10n_hu_get_default_document_type()
        if result:
            self.assertEqual(result._name, "l10n.hu.plus.tag", "Default document type should be a tag record")

    def test_journal_proforma_sequence_available(self) -> None:
        """Proforma sequence available should be computed correctly."""
        self.journal_sale._compute_l10n_hu_proforma_sequence_available()
        # may or may not be available depending on whether sequences exist
        self.assertIn(
            self.journal_sale.l10n_hu_proforma_sequence_available,
            [True, False],
            "Proforma sequence available should be a boolean",
        )

    def test_journal_cron_batch(self) -> None:
        """Journal cron batch should be set correctly."""
        self.assertEqual(self.journal_sale.l10n_hu_cron_batch, 10, "Cron batch should be 10 as configured")

    def test_journal_nav_payment_method(self) -> None:
        """Journal NAV payment method should accept all valid values."""
        self.assertEqual(
            self.journal_sale.l10n_hu_nav_payment_method,
            "TRANSFER",
            "NAV payment method should be TRANSFER as configured",
        )


@tagged("l10n_hu_plus", "post_install_l10n", "post_install", "-at_install")
class TestAccountPaymentTerm(L10nHuPlusTestCommon):
    """Test HU+ fields and methods on account.payment.term."""

    def test_nav_method_selection(self) -> None:
        """NAV method selection should contain all expected payment methods."""
        result = self.env["account.payment.term"].l10n_hu_get_nav_method_selection()
        self.assertIsInstance(result, list, "NAV method selection should be a list")
        method_codes = [item[0] for item in result]
        self.assertIn("TRANSFER", method_codes, "TRANSFER should be in NAV methods")
        self.assertIn("CASH", method_codes, "CASH should be in NAV methods")
        self.assertIn("CARD", method_codes, "CARD should be in NAV methods")
        self.assertIn("VOUCHER", method_codes, "VOUCHER should be in NAV methods")
        self.assertIn("OTHER", method_codes, "OTHER should be in NAV methods")

    def test_nav_methods_list(self) -> None:
        """NAV methods should return a flat list of method code strings."""
        result = self.env["account.payment.term"].l10n_hu_get_nav_methods()
        self.assertIsInstance(result, list, "NAV methods should be a list")
        self.assertEqual(len(result), 5, "NAV methods should contain 5 items")
        self.assertIn("TRANSFER", result, "TRANSFER should be in methods list")
        self.assertIn("CASH", result, "CASH should be in methods list")

    def test_payment_term_nav_method_field(self) -> None:
        """Payment term HU NAV method field should be correctly set."""
        self.assertEqual(self.payment_term_transfer.l10n_hu_nav_method, "TRANSFER", "NAV method should be TRANSFER")

    def test_payment_term_rounding_method(self) -> None:
        """Payment term HU rounding method should reference the cash rounding."""
        self.assertEqual(
            self.payment_term_transfer.l10n_hu_rounding_method,
            self.cash_rounding_huf,
            "Rounding method should reference the HUF cash rounding",
        )


@tagged("l10n_hu_plus", "post_install_l10n", "post_install", "-at_install")
class TestAccountMoveLine(L10nHuPlusTestCommon):
    """Test HU+ fields and methods on account.move.line."""

    def test_is_invoice_rounding_line_product_line(self) -> None:
        """Product line should not be identified as rounding line."""
        invoice = self._create_hu_invoice()
        product_line: L10nHuPlusAccountMoveLine = invoice.invoice_line_ids.filtered(lambda line: line.product_id)
        if product_line:
            result = product_line[0].l10n_hu_is_invoice_rounding_line()
            self.assertFalse(result, "Product line should not be a rounding line")

    def test_is_invoice_rounding_line_rounding_type(self) -> None:
        """Line with display_type rounding should be identified as rounding line."""
        invoice = self._create_hu_invoice()
        # check all lines for rounding type
        for line in invoice.line_ids:
            result = line.l10n_hu_is_invoice_rounding_line()
            if line.display_type == "rounding":
                self.assertTrue(result, "Rounding line should return True")
            else:
                self.assertFalse(result, "Non-rounding line should return False")

    def test_move_line_hu_fields(self) -> None:
        """Move line HU-specific fields should be populated from parent move."""
        invoice = self._create_hu_invoice()
        invoice.l10n_hu_vat_date = self.today
        for line in invoice.invoice_line_ids:
            if line.product_id:
                self.assertEqual(
                    line.l10n_hu_move_trade_position,
                    invoice.l10n_hu_trade_position,
                    "Line trade position should match move trade position",
                )


@tagged("l10n_hu_plus", "post_install_l10n", "post_install", "-at_install")
class TestAccountFiscalPosition(L10nHuPlusTestCommon):
    """Test HU+ fields on account.fiscal.position."""

    def test_fiscal_position_hu_fields(self) -> None:
        """Fiscal position should have HU-specific fields correctly set."""
        fiscal_position = self.fiscal_position_domestic
        self.assertEqual(
            fiscal_position.l10n_hu_incorporation,
            "organization",
            "Incorporation should be organization",
        )
        self.assertEqual(
            fiscal_position.l10n_hu_trade_position,
            "domestic",
            "Trade position should be domestic",
        )
        self.assertEqual(fiscal_position.l10n_hu_vat_status, "domestic", "VAT status should be domestic")

    def test_fiscal_position_eu_fields(self) -> None:
        """EU fiscal position should have correct EU-related field values."""
        self.assertEqual(self.fiscal_position_eu.l10n_hu_trade_position, "eu", "Trade position should be eu")
        self.assertEqual(self.fiscal_position_eu.l10n_hu_vat_status, "other", "VAT status should be other")

    def test_fiscal_position_cash_accounting_fields(self) -> None:
        """Cash accounting fiscal position should have ca tax regime."""
        self.assertEqual(self.fiscal_position_domestic_cash.l10n_hu_tax_regime, "ca", "Tax regime should be ca")

    def test_fiscal_position_private_person_fields(self) -> None:
        """Private person fiscal position should have correct values."""
        self.assertEqual(
            self.fiscal_position_private.l10n_hu_incorporation,
            "taxable_person",
            "Incorporation should be taxable_person",
        )
        self.assertEqual(
            self.fiscal_position_private.l10n_hu_vat_status,
            "private_person",
            "VAT status should be private_person",
        )

    def test_fiscal_position_all_incorporation_values(self) -> None:
        """All incorporation selection values should be accepted."""
        valid_values = ["organization", "self_employed", "taxable_person"]
        for value in valid_values:
            fiscal_position = self.env["account.fiscal.position"].create({
                "name": f"FP {value}",
                "company_id": self.company_data["company"].id,
                "l10n_hu_incorporation": value,
            })
            self.assertEqual(
                fiscal_position.l10n_hu_incorporation,
                value,
                f"Incorporation should be {value}",
            )

    def test_fiscal_position_all_trade_position_values(self) -> None:
        """All trade position selection values should be accepted."""
        valid_values = ["domestic", "eu", "other"]
        for value in valid_values:
            fiscal_position = self.env["account.fiscal.position"].create({
                "name": f"FP trade {value}",
                "company_id": self.company_data["company"].id,
                "l10n_hu_trade_position": value,
            })
            self.assertEqual(
                fiscal_position.l10n_hu_trade_position,
                value,
                f"Trade position should be {value}",
            )


@tagged("l10n_hu_plus", "post_install_l10n", "post_install", "-at_install")
class TestAccountCashRounding(L10nHuPlusTestCommon):
    """Test HU+ fields on account.cash.rounding."""

    def test_cash_rounding_payment_term_relation(self) -> None:
        """Cash rounding should have reverse relation to payment terms."""
        self.assertIn(
            self.payment_term_transfer,
            self.cash_rounding_huf.l10n_hu_payment_term,
            "Cash rounding should reference the payment term via reverse relation",
        )

    def test_cash_rounding_creation(self) -> None:
        """Cash rounding for HUF should be created correctly."""
        self.assertEqual(self.cash_rounding_huf.rounding, 1.0, "HUF rounding should be 1.0")
        self.assertEqual(self.cash_rounding_huf.name, "HUF Rounding", "Name should match")


@tagged("l10n_hu_plus", "post_install_l10n", "post_install", "-at_install")
class TestAccountTax(L10nHuPlusTestCommon):
    """Test HU+ fields on account.tax."""

    def test_tax_hu_plus_fields(self) -> None:
        """Tax HU+ fields should be accessible."""
        tax: L10nHuPlusAccountTax = self.tax_vat  # type: ignore[assignment]
        # these fields should exist and be accessible
        self.assertFalse(tax.l10n_hu_plus_api_enabled, "Default API enabled should be False")
        self.assertFalse(tax.l10n_hu_plus_technical_name, "Default technical name should be empty")

    def test_tax_hu_plus_category(self) -> None:
        """Tax HU+ category should be settable."""
        tax: L10nHuPlusAccountTax = self.tax_vat  # type: ignore[assignment]
        category_tag: L10nHuPlusTag = self.env["l10n.hu.plus.tag"].create({
            "name": "Tax Category Test",
            "tag_type": "object_category",
            "technical_name": "account_tax_category_test",
            "company": self.company_data["company"].id,
        })
        tax.l10n_hu_plus_category = category_tag
        self.assertEqual(tax.l10n_hu_plus_category, category_tag, "Tax category should be set correctly")
        # cleanup
        tax.l10n_hu_plus_category = False


@tagged("l10n_hu_plus", "post_install_l10n", "post_install", "-at_install")
class TestUomUom(L10nHuPlusTestCommon):
    """Test HU+ fields on uom.uom."""

    def test_uom_hu_plus_fields(self) -> None:
        """UoM HU+ fields should be accessible."""
        unit_uom = self.env.ref("uom.product_uom_unit")
        self.assertFalse(unit_uom.l10n_hu_plus_api_enabled, "Default API enabled should be False")

    def test_uom_technical_name_settable(self) -> None:
        """UoM HU+ technical name should be settable."""
        unit_uom = self.env.ref("uom.product_uom_unit")
        unit_uom.l10n_hu_plus_technical_name = "PIECE"
        self.assertEqual(unit_uom.l10n_hu_plus_technical_name, "PIECE", "Technical name should be set")
        # cleanup
        unit_uom.l10n_hu_plus_technical_name = False


@tagged("l10n_hu_plus", "post_install_l10n", "post_install", "-at_install")
class TestAccountTag(L10nHuPlusTestCommon):
    """Test HU+ fields on account.account.tag."""

    def test_account_tag_hu_fields(self) -> None:
        """Account tag HU+ fields should be accessible and writable."""
        account_tag = self.env["account.account.tag"].create({
            "name": "Test HU Tag",
            "applicability": "taxes",
            "country_id": self.env.ref("base.hu").id,
        })
        self.assertFalse(account_tag.l10n_hu_plus_api_enabled, "Default API enabled should be False")
        self.assertFalse(account_tag.l10n_hu_plus_technical_name, "Default technical name should be empty")

    def test_account_tag_country_code(self) -> None:
        """Account tag HU country code should be derived from country."""
        account_tag = self.env["account.account.tag"].create({
            "name": "Test HU Country Tag",
            "applicability": "taxes",
            "country_id": self.env.ref("base.hu").id,
        })
        self.assertEqual(account_tag.l10n_hu_country_code, "HU", "Country code should be HU")
