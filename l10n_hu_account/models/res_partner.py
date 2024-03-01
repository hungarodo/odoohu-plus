# -*- coding: utf-8 -*-
# 1 : imports of python lib
import re

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 : imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuAccountResPartner(models.Model):
    # Private attributes
    _inherit = 'res.partner'

    # Default methods

    # Field declarations
    l10n_hu_incorporation = fields.Selection(
        index=True,
        related='property_account_position_id.l10n_hu_incorporation',
        store=True,
        string="HU Taxpayer Type",
    )
    l10n_hu_trade_position = fields.Selection(
        index=True,
        related='property_account_position_id.l10n_hu_trade_position',
        store=True,
        string="HU Trade Position",
    )
    l10n_hu_vat_status = fields.Selection(
        index=True,
        related='property_account_position_id.l10n_hu_vat_status',
        store=True,
        string="HU VAT Status",
    )
    l10n_hu_vat_status_required = fields.Boolean(
        compute='_compute_l10n_hu_vat_status_required',
        string="HU VAT Status Required"
    )

    # Compute and search fields, in the same order of field declarations

    # Constraints and onchanges

    # CRUD methods (and name_get, name_search, ...) overrides

    # Action methods

    # Business methods
    # # SUPER OVERRIDES
    @api.model
    def _commercial_fields(self):
        """ Super override """
        # Execute super
        result = super(L10nHuAccountResPartner, self)._commercial_fields()

        # Append fields
        result.append('l10n_hu_incorporation')
        result.append('l10n_hu_vat_status')

        # return
        return result

    # # HU
    @api.model
    def l10n_hu_get_is_vat_status_required(self):
        """ Determine if HU VAT Status setting is required

        May be overridden by super

        :return: boolean
        """
        # Initialize variables
        result = False

        # Check active company
        active_company_required = self.env.company.l10n_hu_partner_vat_status_required

        # Check partner company setting
        if self.company_id:
            partner_company_required = self.company_id.l10n_hu_partner_vat_status_required
        else:
            partner_company_required = False

        # NOTE: do not require if parent_id is set (which is the commercial partner probably)
        if not self.parent_id and (active_company_required or partner_company_required):
            result = True

        # Return result
        return result
