# -*- coding: utf-8 -*-
# 1 : imports of python lib
import re

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 : imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuInvoiceProductFee(models.Model):
    # Private attributes
    _name = 'l10n.hu.invoice.product.fee'
    _description = "HU Invoice Product Fee"
    _order = 'write_date desc, id desc'

    # Default methods

    # Field declarations
    account_move = fields.Many2one(
        related='invoice.account_move',
        store=True,
        string="Account Move",
    )
    account_move_line = fields.Many2one(
        related='invoice_line.account_move_line',
        store=True,
        string="Account Move Line",
    )
    company = fields.Many2one(
        related='invoice.company',
        store=True,
        string="Company",
    )
    company_currency = fields.Many2one(
        comodel_name='res.currency',
        copy=False,
        readonly=True,
        string="Company Currency",
    )
    currency = fields.Many2one(
        comodel_name='res.currency',
        copy=False,
        readonly=True,
        string="Currency",
    )
    currency_huf = fields.Many2one(
        comodel_name='res.currency',
        copy=False,
        readonly=True,
        string="Currency HUF",
    )
    evidence_document_date = fields.Date(
        string="Evidence Document Date",
    )
    evidence_document_number = fields.Char(
        string="Evidence Document Number",
    )
    invoice = fields.Many2one(
        comodel_name='l10n.hu.invoice',
        copy=False,
        ondelete='cascade',
        readonly=True,
        string="Invoice",
    )
    invoice_line = fields.Many2one(
        comodel_name='l10n.hu.invoice.line',
        copy=False,
        readonly=True,
        string="Invoice Line",
    )
    obligated_address_building = fields.Char(
        copy=False,
        readonly=True,
        string="Obligated Address Building",
    )
    obligated_address_country = fields.Many2one(
        comodel_name='res.country',
        copy=False,
        index=True,
        readonly=True,
        string="Obligated Country",
    )
    obligated_address_country_code = fields.Char(
        copy=False,
        readonly=True,
        string="Obligated Address Country Code",
    )
    obligated_address_country_name = fields.Char(
        copy=False,
        readonly=True,
        string="Obligated Address Country Name",
    )
    obligated_address_country_state_code = fields.Char(
        copy=False,
        readonly=True,
        string="Obligated Address Country State Code",
    )
    obligated_address_country_state_name = fields.Char(
        copy=False,
        readonly=True,
        string="Obligated Address Country State Name",
    )
    obligated_address_district = fields.Char(
        copy=False,
        readonly=True,
        string="Obligated Address District",
    )
    obligated_address_door = fields.Char(
        copy=False,
        readonly=True,
        string="Obligated Address Door",
    )
    obligated_address_floor = fields.Char(
        copy=False,
        readonly=True,
        string="Obligated Address Floor",
    )
    obligated_address_house_number = fields.Char(
        copy=False,
        readonly=True,
        string="Obligated Address House Number",
    )
    obligated_address_lot_number = fields.Char(
        copy=False,
        readonly=True,
        string="Obligated Address Lot Number",
    )
    obligated_address_postal_code = fields.Char(
        copy=False,
        readonly=True,
        string="Obligated Address Postal Code",
    )
    obligated_address_public_place_name = fields.Char(
        copy=False,
        readonly=True,
        string="Obligated Address Public Place Name",
    )
    obligated_address_public_place_type = fields.Char(
        copy=False,
        readonly=True,
        string="Obligated Address Public Place Type",
    )
    obligated_address_settlement = fields.Char(
        copy=False,
        readonly=True,
        string="Obligated Address Settlement",
    )
    obligated_address_staircase = fields.Char(
        copy=False,
        readonly=True,
        string="Obligated Address Staircase",
    )
    obligated_address_street = fields.Char(
        copy=False,
        readonly=True,
        string="Obligated Address Street",
    )
    obligated_address_street2 = fields.Char(
        copy=False,
        readonly=True,
        string="Obligated Address Street2",
    )
    obligated_address_type = fields.Char(
        copy=False,
        readonly=True,
        string="Obligated Address Type",
    )
    obligated_name = fields.Char(
        string="Obligated Name",
    )
    obligated_partner = fields.Many2one(
        comodel_name='res.partner',
        copy=False,
        index=True,
        readonly=True,
        string="Obligated Partner",
    )
    obligated_tax_number = fields.Char(
        string="Obligated Tax Number",
    )
    product_fee_amount = fields.Monetary(
        currency_field='currency_huf',
        string="Product Fee Amount",
    )
    product_fee_code = fields.Char(
        string="Product Fee Code",
    )
    product_fee_measuring_unit = fields.Char(
        string="Product Fee Measuring Unit",
    )
    product_fee_quantity = fields.Float(
        string="Product Fee Quantity",
    )
    product_fee_rate = fields.Monetary(
        currency_field='currency_huf',
        string="Product Fee Rate",
    )
    product_fee_uom = fields.Many2one(
        comodel_name='uom.uom',
        index=True,
        string="Product Fee UoM",
    )
    scope = fields.Selection(
        index=True,
        selection=[
            ('line', "Line"),
            ('summary', "Summary"),
        ],
        string="Scope"
    )

    # Compute and search fields, in the same order of field declarations

    # Constraints and onchanges

    # CRUD methods (and name_get, name_search, ...) overrides

    # Action methods

    # Business methods
