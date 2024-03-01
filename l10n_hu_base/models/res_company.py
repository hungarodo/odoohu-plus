# -*- coding: utf-8 -*-
# 1 : imports of python lib

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 : imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuBaseResCompany(models.Model):
    # Private attributes
    _inherit = 'res.company'

    # Default methods

    # Field declarations
    l10n_hu_api_enabled = fields.Boolean(
        default=False,
        string="HU API Enabled",
    )
    l10n_hu_api_key = fields.Char(
        default=False,
        string="HU API Key",
    )
    l10n_hu_api_url = fields.Char(
        default=False,
        string="HU API URL",
    )

    # Compute and search fields, in the same order of fields declaration

    # Constraints and onchanges

    # CRUD methods (and name_get, name_search, ...) overrides

    # Action methods

    # Business methods
