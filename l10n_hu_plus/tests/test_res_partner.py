# -*- coding: utf-8 -*-
# author: Online ERP

from __future__ import annotations
from typing import TYPE_CHECKING
from odoo import exceptions
from odoo.tests import tagged
from odoo.addons.l10n_hu_plus.tests.common import L10nHuPlusTestCommon

if TYPE_CHECKING:
    from odoo.addons.l10n_hu_plus.models.res_partner import L10nHuPlusResPartner


@tagged("l10n_hu_plus", "post_install_l10n", "post_install", "-at_install")
class TestResPartnerVatStatus(L10nHuPlusTestCommon):
    """Test l10n_hu_plus_get_vat_status method on res.partner."""

    def test_vat_status_with_fiscal_position(self) -> None:
        """Partner with fiscal position should derive VAT status from it."""
        partner: L10nHuPlusResPartner = self.partner_hu
        result = partner.l10n_hu_plus_get_vat_status()
        self.assertIsInstance(result, dict, "VAT status should return a dictionary")
        self.assertEqual(
            result.get("l10n_hu_incorporation"),
            "organization",
            "Incorporation should be organization from domestic fiscal position",
        )
        self.assertEqual(
            result.get("l10n_hu_trade_position"),
            "domestic",
            "Trade position should be domestic from domestic fiscal position",
        )
        self.assertEqual(
            result.get("l10n_hu_vat_status"),
            "domestic",
            "VAT status should be domestic from domestic fiscal position",
        )

    def test_vat_status_without_fiscal_position(self) -> None:
        """Partner without fiscal position should produce an error."""
        partner: L10nHuPlusResPartner = self.partner_hu_incomplete
        result = partner.l10n_hu_plus_get_vat_status()
        self.assertIsInstance(result, dict, "VAT status should return a dictionary")
        error_list = result.get("error_list", [])
        self.assertTrue(len(error_list) > 0, "Missing fiscal position should produce an error")

    def test_vat_status_eu_fiscal_position(self) -> None:
        """Partner with EU fiscal position should get EU-related values."""
        self.partner_hu.property_account_position_id = self.fiscal_position_eu
        result = self.partner_hu.l10n_hu_plus_get_vat_status()
        self.assertEqual(result.get("l10n_hu_trade_position"), "eu", "Trade position should be eu from EU fiscal position")
        self.assertEqual(result.get("l10n_hu_vat_status"), "other", "VAT status should be other from EU fiscal position")
        # restore
        self.partner_hu.property_account_position_id = self.fiscal_position_domestic

    def test_vat_status_cash_accounting_fiscal_position(self) -> None:
        """Partner with cash accounting fiscal position should get ca tax regime."""
        self.partner_hu.property_account_position_id = self.fiscal_position_domestic_cash
        result = self.partner_hu.l10n_hu_plus_get_vat_status()
        self.assertEqual(result.get("l10n_hu_tax_regime"), "ca", "Tax regime should be ca (cash accounting)")
        # restore
        self.partner_hu.property_account_position_id = self.fiscal_position_domestic

    def test_vat_status_private_person(self) -> None:
        """Partner with private person fiscal position should get private_person VAT status."""
        self.partner_hu.property_account_position_id = self.fiscal_position_private
        result = self.partner_hu.l10n_hu_plus_get_vat_status()
        self.assertEqual(
            result.get("l10n_hu_vat_status"),
            "private_person",
            "VAT status should be private_person from private fiscal position",
        )
        self.assertEqual(
            result.get("l10n_hu_incorporation"),
            "taxable_person",
            "Incorporation should be taxable_person from private fiscal position",
        )
        # restore
        self.partner_hu.property_account_position_id = self.fiscal_position_domestic

    def test_vat_status_child_partner(self) -> None:
        """Child partner should reference commercial partner info."""
        child_partner: L10nHuPlusResPartner = self.env["res.partner"].create({
            "name": "Contact at Teszt Kft.",
            "parent_id": self.partner_hu.id,
            "type": "contact",
            "company_id": False,
        })
        result = child_partner.l10n_hu_plus_get_vat_status()
        self.assertIsInstance(result, dict, "VAT status for child partner should return a dictionary")
        info_list = result.get("info_list", [])
        self.assertTrue(len(info_list) > 0, "Child partner should have info about commercial partner")

    def test_action_set_vat_status_writes_values(self) -> None:
        """action_l10n_hu_plus_set_vat_status should write VAT status fields to partner."""
        partner: L10nHuPlusResPartner = self.partner_hu
        partner.action_l10n_hu_plus_set_vat_status()
        self.assertEqual(partner.l10n_hu_incorporation, "organization", "Incorporation should be written to partner")
        self.assertEqual(partner.l10n_hu_trade_position, "domestic", "Trade position should be written to partner")
        self.assertEqual(partner.l10n_hu_vat_status, "domestic", "VAT status should be written to partner")

    def test_action_set_vat_status_raises_on_error(self) -> None:
        """action_l10n_hu_plus_set_vat_status should raise when there are errors."""
        partner: L10nHuPlusResPartner = self.partner_hu_incomplete
        with self.assertRaises(exceptions.UserError):
            partner.action_l10n_hu_plus_set_vat_status()


@tagged("l10n_hu_plus", "post_install_l10n", "post_install", "-at_install")
class TestResPartnerVisibility(L10nHuPlusTestCommon):
    """Test l10n_hu_plus_get_visible method on res.partner."""

    def test_visible_hu_country(self) -> None:
        """Partner with HU country should have HU+ visible."""
        result = self.partner_hu.l10n_hu_plus_get_visible()
        self.assertTrue(result, "HU+ should be visible for Hungarian partner")

    def test_visible_non_hu_country(self) -> None:
        """Partner with non-HU country should not have HU+ visible (unless company is HU)."""
        partner_de: L10nHuPlusResPartner = self.env["res.partner"].create({
            "name": "German Company GmbH",
            "is_company": True,
            "country_id": self.env.ref("base.de").id,
            "company_id": self.company_data["company"].id,
        })
        result = partner_de.l10n_hu_plus_get_visible()
        # since the company is HU, it should still be visible
        self.assertTrue(result, "HU+ should be visible when company is Hungarian")

    def test_visible_parent_hu_country(self) -> None:
        """Child partner with HU parent should have HU+ visible."""
        child_partner: L10nHuPlusResPartner = self.env["res.partner"].create({
            "name": "Contact Person",
            "parent_id": self.partner_hu.id,
            "type": "contact",
        })
        result = child_partner.l10n_hu_plus_get_visible()
        self.assertTrue(result, "HU+ should be visible for child of Hungarian partner")

    def test_visible_no_company(self) -> None:
        """Partner with no company_id should have HU+ visible."""
        partner_no_company: L10nHuPlusResPartner = self.env["res.partner"].create({
            "name": "No Company Partner",
            "is_company": True,
            "company_id": False,
        })
        result = partner_no_company.l10n_hu_plus_get_visible()
        self.assertTrue(result, "HU+ should be visible when partner has no company")

    def test_compute_l10n_hu_plus_visible(self) -> None:
        """Computed l10n_hu_plus_visible field should match get_visible result."""
        self.partner_hu._compute_l10n_hu_plus_visible()
        self.assertTrue(self.partner_hu.l10n_hu_plus_visible, "Computed visible should be True for HU partner")


@tagged("l10n_hu_plus", "post_install_l10n", "post_install", "-at_install")
class TestResPartnerCrnValidation(L10nHuPlusTestCommon):
    """Test l10n_hu_plus_check_crn method on res.partner for company registration number validation."""

    def test_valid_crn_format(self) -> None:
        """Valid CRN should return True."""
        result = self.partner_hu.l10n_hu_plus_check_crn("01-09-123456")
        self.assertTrue(result, "Valid CRN format 01-09-123456 should return True")

    def test_valid_crn_format_boundary_low(self) -> None:
        """CRN with lowest valid county code should return True."""
        result = self.partner_hu.l10n_hu_plus_check_crn("01-01-000001")
        self.assertTrue(result, "CRN 01-01-000001 should be valid")

    def test_valid_crn_format_boundary_high(self) -> None:
        """CRN with highest valid county code should return True."""
        result = self.partner_hu.l10n_hu_plus_check_crn("20-23-999999")
        self.assertTrue(result, "CRN 20-23-999999 should be valid")

    def test_invalid_crn_county_code_too_high(self) -> None:
        """CRN with county code > 20 should return False."""
        result = self.partner_hu.l10n_hu_plus_check_crn("21-09-123456")
        self.assertFalse(result, "CRN with county code 21 should be invalid")

    def test_invalid_crn_county_code_zero(self) -> None:
        """CRN with county code 00 should return False."""
        result = self.partner_hu.l10n_hu_plus_check_crn("00-09-123456")
        self.assertFalse(result, "CRN with county code 00 should be invalid")

    def test_invalid_crn_court_code_too_high(self) -> None:
        """CRN with court code > 23 should return False."""
        result = self.partner_hu.l10n_hu_plus_check_crn("01-24-123456")
        self.assertFalse(result, "CRN with court code 24 should be invalid")

    def test_invalid_crn_court_code_zero(self) -> None:
        """CRN with court code 00 should return False."""
        result = self.partner_hu.l10n_hu_plus_check_crn("01-00-123456")
        self.assertFalse(result, "CRN with court code 00 should be invalid")

    def test_invalid_crn_too_short(self) -> None:
        """CRN shorter than 12 chars should return False."""
        result = self.partner_hu.l10n_hu_plus_check_crn("01-09-12345")
        self.assertFalse(result, "CRN shorter than 12 chars should be invalid")

    def test_invalid_crn_too_long(self) -> None:
        """CRN longer than 12 chars should return False."""
        result = self.partner_hu.l10n_hu_plus_check_crn("01-09-1234567")
        self.assertFalse(result, "CRN longer than 12 chars should be invalid")

    def test_invalid_crn_wrong_format(self) -> None:
        """CRN with wrong separator format should return False."""
        result = self.partner_hu.l10n_hu_plus_check_crn("0109-123456")
        self.assertFalse(result, "CRN with wrong format should be invalid")

    def test_invalid_crn_letters(self) -> None:
        """CRN with letters in numeric positions should return False."""
        result = self.partner_hu.l10n_hu_plus_check_crn("01-09-12345A")
        self.assertFalse(result, "CRN with letters should be invalid")

    def test_crn_none_input(self) -> None:
        """CRN None should return False."""
        if not hasattr(self.partner_hu, "l10n_hu_crn"):
            # l10n_hu_crn field not available; method fallback accesses the field
            return
        result = self.partner_hu.l10n_hu_plus_check_crn(None)
        self.assertFalse(result, "CRN None should return False")

    def test_crn_empty_string(self) -> None:
        """CRN empty string should return False."""
        if not hasattr(self.partner_hu, "l10n_hu_crn"):
            # l10n_hu_crn field not available; method fallback accesses the field
            return
        result = self.partner_hu.l10n_hu_plus_check_crn("")
        self.assertFalse(result, "CRN empty string should return False")

    def test_crn_from_partner_field(self) -> None:
        """CRN validation should work using the partner l10n_hu_crn field."""
        # only if the field exists (it may come from l10n_hu_edi)
        if hasattr(self.partner_hu, "l10n_hu_crn"):
            self.partner_hu.l10n_hu_crn = "01-09-123456"  # type: ignore[attr-defined]
            result = self.partner_hu.l10n_hu_plus_check_crn()
            self.assertTrue(result, "CRN from partner field should be valid")


@tagged("l10n_hu_plus", "post_install_l10n", "post_install", "-at_install")
class TestResPartnerOnchange(L10nHuPlusTestCommon):
    """Test onchange methods on res.partner for HU+ module."""

    def test_onchange_vat_status_sets_fields(self) -> None:
        """Onchange for VAT status should set incorporation and vat_status fields."""
        partner: L10nHuPlusResPartner = self.partner_hu
        partner._onchange_l10n_hu_plus_vat_status()
        self.assertEqual(partner.l10n_hu_incorporation, "organization", "Incorporation should be set by onchange")
        self.assertEqual(partner.l10n_hu_vat_status, "domestic", "VAT status should be set by onchange")

    def test_onchange_vat_status_eu_partner(self) -> None:
        """Onchange for EU partner should set EU-related values."""
        self.partner_hu.property_account_position_id = self.fiscal_position_eu
        self.partner_hu._onchange_l10n_hu_plus_vat_status()
        self.assertEqual(self.partner_hu.l10n_hu_vat_status, "other", "VAT status should be other for EU partner")
        # restore
        self.partner_hu.property_account_position_id = self.fiscal_position_domestic
