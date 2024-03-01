# -*- coding: utf-8 -*-
# 1 : imports of python lib
import re

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 : imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuBaseResPartner(models.Model):
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
    l10n_hu_enabled = fields.Boolean(
        compute='_compute_l10n_hu_enabled',
        string="HU Enabled",
    )
    l10n_hu_financial_representative = fields.Many2one(
        comodel_name='res.partner',
        string="Financial Representative",
    )
    l10n_hu_personal_tax_exempt = fields.Boolean(
        default=False,
        string="Personal Tax Exempt",
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
    l10n_hu_vat = fields.Char(
        help="Hungarian tax number",
        string="HU VAT",
    )
    l10n_hu_tax_unit = fields.Many2one(
        comodel_name='res.partner',
        string="HU Tax Unit",
    )
    l10n_hu_tax_unit_vat = fields.Char(
        related='l10n_hu_tax_unit.vat',
        store=True,
        string="HU Tax Unit VAT",
    )
    l10n_hu_tax_unit_vat_hu = fields.Char(
        related='l10n_hu_tax_unit.l10n_hu_vat',
        store=True,
        string="HU Tax Unit VAT HU",
    )
    l10n_hu_vat_reverse_charge = fields.Boolean(
        default=False,
        string="VAT Reverse Charge",
    )
    l10n_hu_vpid = fields.Char(
        string="VPID",
    )

    # Compute and search fields, in the same order of field declarations
    def _compute_l10n_hu_vat_status_required(self):
        for record in self:
            record.l10n_hu_vat_status_required = record.l10n_hu_get_is_vat_status_required()

    @api.depends('country_id', 'commercial_partner_id', 'parent_id')
    def _compute_l10n_hu_enabled(self):
        for record in self:
            record.l10n_hu_enabled = record.l10n_hu_get_is_l10n_hu_enabled()

    # Constraints and onchanges
    @api.onchange('is_company')
    def onchange_l10n_hu_is_company(self):
        vat_status_required = self.l10n_hu_get_is_vat_status_required()
        if not self.is_company and vat_status_required:
            self.l10n_hu_vat_status = 'private_person'
        else:
            self.l10n_hu_vat_status = False

    @api.onchange('company_id', 'name')
    def onchange_l10n_hu_vat_status_required(self):
        self.l10n_hu_vat_status_required = self.l10n_hu_get_is_vat_status_required()

    @api.onchange('l10n_hu_vat')
    def onchange_l10n_hu_vat(self):
        if self.l10n_hu_vat and not self.l10n_hu_get_is_valid_l10n_hu_vat():
            text = _("Invalid hungarian VAT format!")
            text += "\n" + _("Only numbers are allowed in this format: ") + "XXXXXXXX-Y-ZZ"

            raise exceptions.ValidationError(text)
        else:
            pass

    @api.onchange('l10n_hu_vat_status')
    def onchange_l10n_hu_vat_status(self):
        is_l10n_hu = self.l10n_hu_get_is_l10n_hu_enabled()
        if is_l10n_hu and self.l10n_hu_vat_status == 'private_person':
            self.l10n_hu_incorporation = False
            self.l10n_hu_vat = False
            self.vat = False
        elif is_l10n_hu and self.l10n_hu_vat_status == 'other':
            self.l10n_hu_incorporation = False
            self.l10n_hu_vat = False
        else:
            pass

    @api.onchange('parent_id')
    def onchange_l10n_hu_parent_id(self):
        self.l10n_hu_incorporation = False
        self.l10n_hu_self_employed_name = False
        self.l10n_hu_self_employed_number = False
        self.l10n_hu_vat = False
        self.l10n_hu_vat_status = False

    # CRUD methods (and name_get, name_search, ...) overrides

    # Action methods

    # Business methods
    # # SUPER OVERRIDES
    @api.model
    def _commercial_fields(self):
        """ Super override """
        # Execute super
        result = super(L10nHuBaseResPartner, self)._commercial_fields()

        # Append fields
        result.append('l10n_hu_self_employed_name')
        result.append('l10n_hu_self_employed_number')
        result.append('l10n_hu_vat')

        # return
        return result

    # # HU
    @api.model
    def l10n_hu_get_is_l10n_hu_enabled(self):
        """ Determine if partner is L10NHU

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
    def l10n_hu_get_is_valid_l10n_hu_crn(self, l10n_hu_crn=None):
        """ Validate hungarian company registration number format """
        if l10n_hu_crn and isinstance(l10n_hu_crn, str):
            pass
        elif not l10n_hu_crn and self.l10n_hu_crn:
            l10n_hu_crn = self.l10n_hu_crn
        else:
            return False

        if l10n_hu_crn:
            pattern = re.compile("(0[1-9]|1[0-9]|20)-(0[1-9]|1[0-9]|2[0-3])-[0-9]{6}")
            match = pattern.match(l10n_hu_crn)

            if match and match.start() == 0 and match.end() == 12 and len(l10n_hu_crn) == 12:
                return True
            else:
                return False
        else:
            return False

    @api.model
    def l10n_hu_get_is_valid_l10n_hu_vat(self, l10n_hu_vat=None):
        """ Checks if the VAT number complies with hungarian regulations

        Sample: xxxxxxxx-y-zz
        - 1st-8th character (unique code, same as the EU community code): [0-9]{8} integers 0-9
        - 10th character (NAV status code): [1-5]{1} integer 1-5
        - 12th-13th character (NAV branch code): [0-9]{2} integers 0-9
        """

        # Validate hungarian company registration number format
        if l10n_hu_vat and isinstance(l10n_hu_vat, str):
            pass
        elif not l10n_hu_vat and self.l10n_hu_vat:
            l10n_hu_vat = self.l10n_hu_vat
        else:
            return False

        if l10n_hu_vat:
            # pattern = re.compile("[0-9]{8}-[1-5]-(0[235689]|1[12345679]|2[0235689]|3[1245679]|4[01234])")
            pattern = re.compile("[0-9]{8}-[1-5]-[0-9]{2}")
            match = pattern.match(l10n_hu_vat)
            if match and match.start() == 0 and match.end() == 13 and len(l10n_hu_vat) == 13:
                return True
            else:
                return False
        else:
            return False
