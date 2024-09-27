# -*- coding: utf-8 -*-
# 1 : imports of python lib

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered


# 3 : imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuPlusAccountTag(models.Model):
    # Private attributes
    _inherit = 'account.account.tag'

    # Default methods

    # Field declarations
    l10n_hu_country_code = fields.Char(
        related='country_id.code',
        index=True,
        store=True,
        string="HU Country Code",
    )
    l10n_hu_evat_description = fields.Text(
        index=True,
        string="HU eVAT Description",
    )
    l10n_hu_evat_readable_code = fields.Char(
        index=True,
        string="HU eVAT Readable Code",
    )
    l10n_hu_evat_standard_code = fields.Char(
        index=True,
        string="HU eVAT Standard Code",
    )
    l10n_hu_plus_api_enabled = fields.Boolean(
        default=False,
        string="HU+ API Enabled",
    )
    l10n_hu_plus_technical_name = fields.Char(
        index=True,
        string="HU+ Technical Name",
    )

    # Compute and search fields, in the same order of field declarations

    # Constraints and onchanges

    # CRUD methods (and display_name, name_search, ...) overrides

    # Action methods

    # Business methods
