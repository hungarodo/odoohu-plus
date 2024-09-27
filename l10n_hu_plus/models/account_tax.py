# -*- coding: utf-8 -*-
# 1 : imports of python lib

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered


# 3 : imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuAccountTax(models.Model):
    # Private attributes
    _inherit = 'account.tax'

    # Default methods

    # Field declarations
    l10n_hu_plus_api_enabled = fields.Boolean(
        default=False,
        string="HU+ API",
    )
    l10n_hu_plus_category = fields.Many2one(
        comodel_name='l10n.hu.plus.tag',
        domain=[('tag_type', '=', 'object_category'), ('technical_name', 'like', 'account_tax_category')],
        string="HU+ Category",
    )
    l10n_hu_plus_technical_name = fields.Char(
        copy=False,
        string="HU+ Technical Name",
    )
    l10n_hu_vat_declaration = fields.Boolean(
        default=False,
        help="Can be included in VAT declarations",
        string="HU VAT Declaration",
    )

    # Compute and search fields, in the same order of field declarations

    # Constraints and onchanges

    # CRUD methods (and display_name, name_search, ...) overrides

    # Action methods

    # Business methods
