# -*- coding: utf-8 -*-
# 1 : imports of python lib

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 : imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuAccountFiscalPosition(models.Model):
    # Private attributes
    _inherit = 'account.fiscal.position'

    # Default methods

    # Field declarations
    l10n_hu_api_enabled = fields.Boolean(
        default=False,
        string="HU API Enabled",
    )
    l10n_hu_incorporation = fields.Selection(
        index=True,
        selection=[
            ('organization', "Organization"),
            ('self_employed', "Self Employed"),
            ('taxable_person', "Taxable Person"),
        ],
        string="HU Taxpayer Type",
    )
    l10n_hu_technical_name = fields.Char(
        copy=False,
        string="HU Technical Name",
    )
    l10n_hu_trade_position = fields.Selection(
        index=True,
        selection=[
            ('domestic', "Domestic"),
            ('eu', "EU"),
            ('other', "Other"),
        ],
        string="HU Trade Position",
    )
    l10n_hu_vat_status = fields.Selection(
        index=True,
        selection=[
            ('domestic', "Domestic"),
            ('private_person', "Private Person"),
            ('other', "Other"),
        ],
        string="HU VAT Status",
    )

    # Compute and search fields, in the same order of field declarations

    # Constraints and onchanges

    # CRUD methods (and name_get, name_search, ...) overrides

    # Action methods

    # Business methods

