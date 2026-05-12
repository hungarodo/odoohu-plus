# -*- coding: utf-8 -*-
# author: Online ERP
from __future__ import annotations

import datetime

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase, tagged


@tagged("-at_install", "post_install")
class TestL10nHuPlusModels(TransactionCase):
    """Deterministic tests for core HU+ model and wizard helpers (Odoo 19)."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.hu_country = cls.env.ref("base.hu")
        cls.us_country = cls.env.ref("base.us")
        cls.hu_parent_partner = cls.env["res.partner"].create({
            "name": "HU Parent Partner",
            "country_id": cls.hu_country.id,
        })

    # -------------------------------------------------------------------------
    # HELPERS
    # -------------------------------------------------------------------------
    def _create_partner(self, name, country, parent=None):
        values = {
            "name": name,
            "country_id": country.id,
        }
        if parent:
            values["parent_id"] = parent.id
        return self.env["res.partner"].create(values)

    def _create_wizard(self, values):
        return self.env["l10n.hu.plus.wizard"].new(values)

    def _get_sale_journal(self):
        journal = self.env["account.journal"].search([
            ("type", "=", "sale"),
            ("company_id", "=", self.env.company.id),
        ], limit=1)
        self.assertTrue(journal)
        return journal

    def _create_fiscal_position(
        self,
        name: str,
        incorporation: str,
        vat_status: str,
        trade_position: str = "domestic",
    ):
        return self.env["account.fiscal.position"].create({
            "name": name,
            "l10n_hu_incorporation": incorporation,
            "l10n_hu_trade_position": trade_position,
            "l10n_hu_vat_status": vat_status,
        })

    # -------------------------------------------------------------------------
    # TEST: ACCOUNT PAYMENT TERM HELPERS
    # -------------------------------------------------------------------------
    def test_nav_method_selection_has_expected_values(self) -> None:
        payment_term_model = self.env["account.payment.term"]
        selection = payment_term_model.l10n_hu_get_nav_method_selection()
        self.assertEqual(
            selection,
            [
                ("TRANSFER", "Transfer"),
                ("CASH", "Cash"),
                ("CARD", "Card"),
                ("VOUCHER", "Voucher"),
                ("OTHER", "Other"),
            ],
        )

    def test_nav_methods_returns_only_selection_codes(self) -> None:
        payment_term_model = self.env["account.payment.term"]
        methods = payment_term_model.l10n_hu_get_nav_methods()
        self.assertEqual(methods, ["TRANSFER", "CASH", "CARD", "VOUCHER", "OTHER"])

    # -------------------------------------------------------------------------
    # TEST: PARTNER HU+ LOGIC
    # -------------------------------------------------------------------------
    def test_partner_visible_for_hungarian_country(self) -> None:
        partner = self._create_partner("HU Customer", self.hu_country)
        self.assertTrue(partner.l10n_hu_plus_get_visible())

    def test_partner_visible_for_child_of_hungarian_parent(self) -> None:
        child_partner = self._create_partner(
            "HU Child Contact",
            self.us_country,
            parent=self.hu_parent_partner,
        )
        self.assertTrue(child_partner.l10n_hu_plus_get_visible())

    def test_partner_visible_matches_company_country_when_company_bound(self) -> None:
        partner = self.env["res.partner"].create({
            "name": "Company-bound US Partner",
            "country_id": self.us_country.id,
            "company_id": self.env.company.id,
        })
        expected_visible = bool(
            self.env.company.country_id and self.env.company.country_id.code == "HU"
        )
        self.assertEqual(partner.l10n_hu_plus_get_visible(), expected_visible)

    def test_crn_validation_accepts_valid_format(self) -> None:
        partner = self.env["res.partner"].create({"name": "CRN Partner"})
        self.assertTrue(partner.l10n_hu_plus_check_crn("01-01-123456"))

    def test_crn_validation_rejects_invalid_format(self) -> None:
        partner = self.env["res.partner"].create({"name": "CRN Partner Invalid"})
        self.assertFalse(partner.l10n_hu_plus_check_crn("1-01-123456"))

    def test_crn_validation_accepts_upper_boundary_codes(self) -> None:
        partner = self.env["res.partner"].create({"name": "CRN Partner Boundary"})
        self.assertTrue(partner.l10n_hu_plus_check_crn("20-23-999999"))

    def test_crn_validation_rejects_invalid_county_code(self) -> None:
        partner = self.env["res.partner"].create({"name": "CRN Partner County Invalid"})
        self.assertFalse(partner.l10n_hu_plus_check_crn("21-01-123456"))

    # -------------------------------------------------------------------------
    # TEST: VAT STATUS COMPLIANCE
    # -------------------------------------------------------------------------
    def test_partner_vat_status_follows_fiscal_position(self) -> None:
        fiscal_position = self._create_fiscal_position(
            name="HU Domestic FP",
            incorporation="organization",
            vat_status="domestic",
        )
        partner = self.env["res.partner"].create({
            "name": "HU VAT Partner",
            "country_id": self.hu_country.id,
            "property_account_position_id": fiscal_position.id,
        })
        result = partner.l10n_hu_plus_get_vat_status()
        self.assertEqual(result["l10n_hu_incorporation"], "organization")
        self.assertEqual(result["l10n_hu_vat_status"], "domestic")
        self.assertEqual(result["error_list"], [])

    def test_partner_vat_status_onchange_sets_fields_from_fiscal_position(self) -> None:
        fiscal_position = self._create_fiscal_position(
            name="HU Other FP",
            incorporation="taxable_person",
            vat_status="other",
            trade_position="other",
        )
        partner = self.env["res.partner"].new({
            "name": "Onchange Partner",
            "country_id": self.hu_country.id,
            "property_account_position_id": fiscal_position.id,
        })
        partner._onchange_l10n_hu_plus_vat_status()
        self.assertEqual(partner.l10n_hu_incorporation, "taxable_person")
        self.assertEqual(partner.l10n_hu_vat_status, "other")

    def test_partner_vat_status_reports_error_without_fiscal_position(self) -> None:
        partner = self.env["res.partner"].create({
            "name": "No Fiscal Position Partner",
            "country_id": self.hu_country.id,
        })
        result = partner.l10n_hu_plus_get_vat_status()
        self.assertTrue(result["error_list"])
        self.assertFalse(result["l10n_hu_incorporation"])
        self.assertFalse(result["l10n_hu_vat_status"])

    # -------------------------------------------------------------------------
    # TEST: HUNGARIAN DELIVERY PERIOD COMPLIANCE (ODOO 19 METHOD NAMES)
    # -------------------------------------------------------------------------
    def test_delivery_period_scenario_1a_uses_invoice_date(self) -> None:
        journal = self._get_sale_journal()
        move = self.env["account.move"].create({
            "move_type": "out_invoice",
            "journal_id": journal.id,
            "partner_id": self.hu_parent_partner.id,
        })
        period_end = datetime.date(2026, 5, 31)
        invoice_date = datetime.date(2026, 5, 20)
        result = move.l10n_hu_plus_get_delivery_data({
            "l10n_hu_delivery_period_start": datetime.date(2026, 5, 1),
            "l10n_hu_delivery_period_end": period_end,
            "invoice_date": invoice_date,
            "invoice_date_due": datetime.date(2026, 5, 25),
        })
        self.assertEqual(result["period_scenario"], "1a_invoice_date")
        self.assertEqual(result["delivery_date"], invoice_date)
        self.assertIn("2007. CXXVII. 58.§", result["period_legal"])
        self.assertIn("(1) a)", result["period_legal"])

    def test_delivery_period_scenario_1b_uses_due_date_within_60_days(self) -> None:
        journal = self._get_sale_journal()
        move = self.env["account.move"].create({
            "move_type": "out_invoice",
            "journal_id": journal.id,
            "partner_id": self.hu_parent_partner.id,
        })
        due_date = datetime.date(2026, 6, 10)
        result = move.l10n_hu_plus_get_delivery_data({
            "l10n_hu_delivery_period_start": datetime.date(2026, 5, 1),
            "l10n_hu_delivery_period_end": datetime.date(2026, 5, 31),
            "invoice_date": datetime.date(2026, 5, 20),
            "invoice_date_due": due_date,
        })
        self.assertEqual(result["period_scenario"], "1b_invoice_date_due")
        self.assertEqual(result["delivery_date"], due_date)
        self.assertIn("(1) b)", result["period_legal"])

    def test_delivery_period_scenario_1b_caps_due_date_at_60_days(self) -> None:
        journal = self._get_sale_journal()
        move = self.env["account.move"].create({
            "move_type": "out_invoice",
            "journal_id": journal.id,
            "partner_id": self.hu_parent_partner.id,
        })
        period_end = datetime.date(2026, 5, 31)
        expected_capped_date = period_end + datetime.timedelta(days=60)
        result = move.l10n_hu_plus_get_delivery_data({
            "l10n_hu_delivery_period_start": datetime.date(2026, 5, 1),
            "l10n_hu_delivery_period_end": period_end,
            "invoice_date": datetime.date(2026, 5, 20),
            "invoice_date_due": datetime.date(2026, 8, 5),
        })
        self.assertEqual(result["period_scenario"], "1b_invoice_date_due_max_60")
        self.assertEqual(result["delivery_date"], expected_capped_date)
        self.assertIn("60+", result["period_legal"])

    # -------------------------------------------------------------------------
    # TEST: ACCOUNT MOVE LINE HELPERS
    # -------------------------------------------------------------------------
    def test_invoice_rounding_line_classifier_true_for_rounding_display_type(self) -> None:
        move_line = self.env["account.move.line"].new({"display_type": "rounding"})
        self.assertTrue(move_line.l10n_hu_is_invoice_rounding_line())

    def test_invoice_rounding_line_classifier_false_for_non_rounding_display_type(self) -> None:
        move_line = self.env["account.move.line"].new({"display_type": "product"})
        self.assertFalse(move_line.l10n_hu_is_invoice_rounding_line())

    # -------------------------------------------------------------------------
    # TEST: WIZARD ONCHANGE LOGIC (ODOO 19)
    # -------------------------------------------------------------------------
    def test_wizard_onchange_delivery_period_raises_when_end_before_start(self) -> None:
        wizard = self._create_wizard({
            "accounting_delivery_period_enabled": True,
            "accounting_delivery_period_start": datetime.date(2026, 5, 11),
            "accounting_delivery_period_end": datetime.date(2026, 5, 10),
        })
        with self.assertRaises(ValidationError):
            wizard.onchange_accounting_delivery_period()

    def test_wizard_onchange_account_move_sets_accounting_date(self) -> None:
        journal = self._get_sale_journal()
        move = self.env["account.move"].create({
            "move_type": "out_invoice",
            "journal_id": journal.id,
            "partner_id": self.hu_parent_partner.id,
        })
        wizard = self._create_wizard({
            "action_type": "account_move",
            "account_move_action": "check_status",
            "account_move": [(6, 0, [move.id])],
        })
        wizard.onchange_account_move()
        self.assertEqual(wizard.accounting_date, move.date)

    def test_wizard_onchange_partner_generates_summary(self) -> None:
        partner_1 = self._create_partner("Summary Partner 1", self.hu_country)
        partner_2 = self._create_partner("Summary Partner 2", self.us_country)
        wizard = self._create_wizard({
            "action_type": "partner",
            "partner": [(6, 0, [partner_1.id, partner_2.id])],
        })
        wizard.onchange_partner()
        self.assertTrue(wizard.partner_action_summary)
        self.assertIn("2", wizard.partner_action_summary)

