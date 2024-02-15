# -*- coding: utf-8 -*-
# 1 : imports of python lib

# 2 :  imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 :  imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuInvoiceAccountJournal(models.Model):
    # Private attributes
    _inherit = 'account.journal'

    # Default methods

    # Field declarations
    l10n_hu_invoice_delivery_date_default = fields.Selection(
        copy=False,
        default='none',
        selection=[
            ('none', "None"),
            ('today', "Today"),
            ('first_day_of_this_month', "First day of this month"),
            ('last_day_of_this_month', "Last day of this month"),
            ('last_day_of_last_month', "Last day of last month"),
            ('first_day_of_next_month', "First day of next month"),
        ],
        string="HU Invoice Delivery Date Default",
    )
    l10n_hu_invoice_delivery_date_limit = fields.Integer(
        copy=False,
        default=8,
        string="HU Invoice Delivery Date Limit",
    )
    l10n_hu_invoice_document_line_label = fields.Selection(
        copy=False,
        default='line_name',
        selection=[
            ('line_name', "Line Name"),
            ('product_display_name', "Product Display Name"),
            ('product_name', "Product Name"),
        ],
        string="HU Invoice Document Line Label",
    )
    l10n_hu_invoice_document_template = fields.Many2one(
        comodel_name='ir.ui.view',
        copy=False,
        domain=[('type', '=', 'qweb'), ('inherit_id', '=', False), ('key', 'ilike', 'report_invoice_document')],
        string="HU Invoice Document Template",
    )
    l10n_hu_invoice_enabled = fields.Boolean(
        default=False,
        string="HU Invoice Enabled",
    )
    l10n_hu_invoice_refund_price_default = fields.Boolean(
        copy=False,
        default=False,
        string="HU Invoice Refund Price Default",
    )
    l10n_hu_invoice_rounding_enabled = fields.Boolean(
        default=False,
        string="HU Invoice Rounding Enabled",
    )
    
    # Compute and search fields, in the same order of field declarations

    # Constraints and onchanges

    # CRUD methods (and name_get, name_search, ...) overrides

    # Action methods

    # Business methods
