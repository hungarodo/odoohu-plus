# -*- coding: utf-8 -*-
# 1 : imports of python lib

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 : imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuPlusAccountCashRounding(models.Model):
    # Private attributes
    _inherit = 'account.cash.rounding'

    # Default methods

    # Field declarations
    l10n_hu_payment_term = fields.One2many(
        comodel_name='account.payment.term',
        inverse_name='l10n_hu_rounding_method',
        string="HU Payment Term",
    )

    # Compute and search fields, in the same order of field declarations

    # Constraints and onchanges

    # CRUD methods (and name_get, name_search, ...) overrides

    # Action methods

    # Business methods
