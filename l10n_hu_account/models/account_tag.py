# -*- coding: utf-8 -*-
# 1 : imports of python lib

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered


# 3 : imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuAccountAccountTag(models.Model):
    # Private attributes
    _inherit = 'account.account.tag'

    # Default methods

    # Field declarations
    l10n_hu_country_code = fields.Char(
        related='country_id.code',
        index=True,
        store=True,
        string="Country Code",
    )

    # Compute and search fields, in the same order of field declarations

    # Constraints and onchanges

    # CRUD methods (and name_get, name_search, ...) overrides

    # Action methods

    # Business methods
