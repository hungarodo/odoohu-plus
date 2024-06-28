# -*- coding: utf-8 -*-
# 1 : imports of python lib
import re

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 : imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuPlusResPartner(models.Model):
    # Private attributes
    _inherit = 'res.partner'

    # Default methods

    # Field declarations
    l10n_hu_cash_accounting = fields.Boolean(
        default=False,
        string="Cash Accounting",
    )
    l10n_hu_crn = fields.Char(
        help="Hungarian Company Registration Number",
        string="HU CRN",
    )
    l10n_hu_financial_representative = fields.Many2one(
        comodel_name='res.partner',
        string="Financial Representative",
    )
    l10n_hu_personal_tax_exempt = fields.Boolean(
        default=False,
        string="Personal Tax Exempt",
    )
    l10n_hu_plus_visible = fields.Boolean(
        compute='_compute_l10n_hu_plus_visible',
        string="HU+ Visible",
    )
    l10n_hu_self_billing = fields.Boolean(
        default=False,
        string="Self Billing",
    )
    l10n_hu_self_employed_name = fields.Char(
        string="Self-Employed Name",
    )
    l10n_hu_self_employed_number = fields.Char(
        size=10,
        string="Self-Employed Number",
    )
    l10n_hu_small_business = fields.Boolean(
        default=False,
        string="Small Business",
    )
    l10n_hu_vat_reverse_charge = fields.Boolean(
        default=False,
        string="VAT Reverse Charge",
    )
    l10n_hu_vpid = fields.Char(
        string="VPID",
    )

    # Compute and search fields, in the same order of field declarations
    @api.depends('country_id', 'commercial_partner_id', 'parent_id')
    def _compute_l10n_hu_plus_visible(self):
        for record in self:
            record.l10n_hu_plus_visible = record.l10n_hu_plus_get_visible()

    # Constraints and onchanges

    # CRUD methods (and name_get, name_search, ...) overrides

    # Action methods

    # Business methods
    # # HU+
    @api.model
    def l10n_hu_plus_get_visible(self):
        """ Determine if HU+ should be visible

        May be overridden by super

        :return: boolean
        """
        # Initialize variables
        result = False

        if self.country_id and self.country_id.code == 'HU':
            result = True
        elif self.parent_id and self.parent_id.country_id and self.parent_id.country_id.code == 'HU':
            result = True
        else:
            pass

        # Return result
        return result

    @api.model
    def l10n_hu_plus_check_crn(self, crn=None):
        """ Validate hungarian company registration number format """
        if crn and isinstance(crn, str):
            pass
        elif not crn and self.l10n_hu_crn:
            crn = self.l10n_hu_crn
        else:
            return False

        if crn:
            pattern = re.compile("(0[1-9]|1[0-9]|20)-(0[1-9]|1[0-9]|2[0-3])-[0-9]{6}")
            match = pattern.match(crn)

            if match and match.start() == 0 and match.end() == 12 and len(crn) == 12:
                return True
            else:
                return False
        else:
            return False
