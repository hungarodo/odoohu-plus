# -*- coding: utf-8 -*-
# author: Online ERP

from __future__ import annotations
import datetime
from typing import TYPE_CHECKING
from odoo import Command
from odoo.addons.l10n_hu_edi.tests.common import L10nHuEdiTestCommon

if TYPE_CHECKING:
    from odoo.addons.account.models.account_journal import AccountJournal
    from odoo.addons.account.models.account_move import AccountMove
    from odoo.addons.base.models.res_currency import Currency
    from odoo.addons.base.models.res_partner import Partner
    from odoo.addons.l10n_hu_plus.models.tag import L10nHuPlusTag


class L10nHuPlusTestCommon(L10nHuEdiTestCommon):
    """Common test base for l10n_hu_plus module.

    Extends the l10n_hu_edi test common with HU+-specific test data:
    - HU+ enabled journal
    - Document type tags (invoice_normal, invoice_storno, invoice_modification)
    - Partner with full Hungarian address and fiscal position
    - Cash rounding for HUF
    """

    @classmethod
    @L10nHuEdiTestCommon.setup_country("hu")
    def setUpClass(cls) -> None:
        """Set up HU+ test data."""
        super().setUpClass()
        cls.env.user.groups_id += cls.env.ref("l10n_hu_plus.manager_group")
        cls.today = datetime.date.today()
        cls.yesterday = cls.today - datetime.timedelta(days=1)
        # enable HU+ on the sale journal
        cls.journal_sale: AccountJournal = cls.company_data["default_journal_sale"]
        cls.journal_sale.write({
            "l10n_hu_plus_enabled": True,
            "l10n_hu_banner_enabled": True,
            "l10n_hu_edi_sending": "manual",
            "l10n_hu_delivery_date_default": "today",
            "l10n_hu_nav_payment_method": "TRANSFER",
            "l10n_hu_cron_batch": 10,
        })
        cls.journal_purchase: AccountJournal = cls.company_data["default_journal_purchase"]
        cls.journal_purchase.write({
            "l10n_hu_plus_enabled": True,
            "l10n_hu_delivery_date_default": "none",
        })
        # document type tags
        company = cls.company_data["company"]
        cls.document_type_normal: L10nHuPlusTag = cls.env["l10n.hu.plus.tag"].create({
            "code": "INVOICE-NORMAL",
            "company": company.id,
            "locked": True,
            "name": "Invoice",
            "priority": 1,
            "tag_type": "document_type",
            "technical_name": "invoice_normal",
        })
        cls.document_type_storno: L10nHuPlusTag = cls.env["l10n.hu.plus.tag"].create({
            "code": "INVOICE-STORNO",
            "company": company.id,
            "locked": True,
            "name": "Storno Invoice",
            "priority": 4,
            "tag_type": "document_type",
            "technical_name": "invoice_storno",
        })
        cls.document_type_modification: L10nHuPlusTag = cls.env["l10n.hu.plus.tag"].create({
            "code": "INVOICE-MODIFICATION",
            "company": company.id,
            "locked": True,
            "name": "Modification Invoice",
            "priority": 3,
            "tag_type": "document_type",
            "technical_name": "invoice_modification",
        })
        # fiscal positions with HU-specific fields
        cls.fiscal_position_domestic = cls.env["account.fiscal.position"].create({
            "name": "Domestic Organization",
            "company_id": company.id,
            "l10n_hu_incorporation": "organization",
            "l10n_hu_trade_position": "domestic",
            "l10n_hu_vat_status": "domestic",
        })
        cls.fiscal_position_domestic_cash = cls.env["account.fiscal.position"].create({
            "name": "Domestic Cash Accounting",
            "company_id": company.id,
            "l10n_hu_incorporation": "organization",
            "l10n_hu_tax_regime": "ca",
            "l10n_hu_trade_position": "domestic",
            "l10n_hu_vat_status": "domestic",
        })
        cls.fiscal_position_eu = cls.env["account.fiscal.position"].create({
            "name": "EU Organization",
            "company_id": company.id,
            "l10n_hu_incorporation": "organization",
            "l10n_hu_trade_position": "eu",
            "l10n_hu_vat_status": "other",
        })
        cls.fiscal_position_private = cls.env["account.fiscal.position"].create({
            "name": "Domestic Private Person",
            "company_id": company.id,
            "l10n_hu_incorporation": "taxable_person",
            "l10n_hu_trade_position": "domestic",
            "l10n_hu_vat_status": "private_person",
        })
        # partner with full HU address
        cls.partner_hu = cls.env["res.partner"].create({
            "name": "Teszt Kft.",
            "is_company": True,
            "street": "Kossuth Lajos utca 1.",
            "city": "Budapest",
            "zip": "1055",
            "country_id": cls.env.ref("base.hu").id,
            "vat": "12345678-2-42",
            "invoice_sending_method": "manual",
            "invoice_edi_format": False,
            "property_account_position_id": cls.fiscal_position_domestic.id,
            "property_account_receivable_id": cls.company_data["default_account_receivable"].id,
            "property_account_payable_id": cls.company_data["default_account_payable"].id,
            "company_id": False,
        })
        # partner without full address (for error testing)
        cls.partner_hu_incomplete = cls.env["res.partner"].create({
            "name": "Hiányos Partner",
            "is_company": True,
            "country_id": cls.env.ref("base.hu").id,
            "invoice_sending_method": "manual",
            "invoice_edi_format": False,
            "property_account_receivable_id": cls.company_data["default_account_receivable"].id,
            "property_account_payable_id": cls.company_data["default_account_payable"].id,
            "company_id": False,
        })
        # cash rounding for HUF
        cls.cash_rounding_huf = cls.env["account.cash.rounding"].create({
            "name": "HUF Rounding",
            "rounding": 1.0,
            "strategy": "biggest_tax",
            "rounding_method": "HALF-UP",
        })
        # payment term with NAV method and rounding
        cls.payment_term_transfer = cls.env["account.payment.term"].create({
            "name": "30 Days Transfer",
            "l10n_hu_nav_method": "TRANSFER",
            "l10n_hu_rounding_method": cls.cash_rounding_huf.id,
            "line_ids": [
                Command.create({"value": "percent", "value_amount": 100.0, "nb_days": 30}),
            ],
        })
        # currency references
        cls.currency_eur = cls.env.ref("base.EUR")
        cls.currency_huf = cls.env.ref("base.HUF")

    @classmethod
    def _create_hu_invoice(
        cls,
        move_type: str = "out_invoice",
        partner: Partner | None = None,
        currency: Currency | None = None,
        amount: float = 100000.0,
        delivery_date: datetime.date | None = None,
        document_type: L10nHuPlusTag | None = None,
    ) -> AccountMove:
        """Create a Hungarian invoice with HU+ specific data.

        :param str move_type: the move type (out_invoice, in_invoice, out_refund, in_refund)
        :param Partner partner: the partner record, defaults to partner_hu
        :param Currency currency: the currency record, defaults to HUF
        :param float amount: the line unit price
        :param datetime.date delivery_date: the delivery date, defaults to today
        :param L10nHuPlusTag document_type: the document type tag, defaults to document_type_normal
        :return: the created account.move record
        """
        if partner is None:
            partner = cls.partner_hu
        if currency is None:
            currency = cls.currency_huf
        if delivery_date is None:
            delivery_date = cls.today
        if document_type is None:
            document_type = cls.document_type_normal
        journal = (cls.journal_sale if move_type in cls.env["account.move"].get_sale_types() else cls.journal_purchase)
        values = {
            "move_type": move_type,
            "journal_id": journal.id,
            "currency_id": currency.id,  # type: ignore[union-attr]
            "partner_id": partner.id,  # type: ignore[union-attr]
            "invoice_date": cls.today,
            "delivery_date": delivery_date,
            "l10n_hu_document_type": document_type.id if document_type else False,
            "invoice_line_ids": [
                Command.create({
                    "product_id": cls.product_a.id,
                    "price_unit": amount,
                    "quantity": 1,
                    "tax_ids": [Command.set(cls.tax_vat.ids)],  # type: ignore[union-attr]
                }),
            ],
        }
        return cls.env["account.move"].create(values)
