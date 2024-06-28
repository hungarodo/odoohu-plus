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
    l10n_hu_category = fields.Selection(
        selection=[
            ('vat', "VAT"),
        ],
        string="HU Category",
    )
    l10n_hu_plus_api_enabled = fields.Boolean(
        default=False,
        string="HU+ API",
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
    l10n_hu_vat_percentage = fields.Float(
        copy=False,
        digits=(5, 4),
        help="NAV (Hungarian Tax Authority) VAT rate",
        string="HU VAT Percentage",
    )

    # Compute and search fields, in the same order of field declarations

    # Constraints and onchanges

    # CRUD methods (and name_get, name_search, ...) overrides

    # Action methods
    def action_l10n_hu_update_configuration(self):
        """ Update l10n_hu configuration for the tax """
        # Get vat_configuration_data
        vat_configuration_result = self.l10n_hu_get_vat_configuration()
        vat_configuration = vat_configuration_result.get('vat_configuration')

        for record in self:
            write_values = {}

            for item in vat_configuration:
                account_tax = item.get('account_tax', False)
                technical_name = item.get('technical_name', False)
                # technical_name
                if account_tax and account_tax == record and not record.technical_name:
                    write_values.update({
                        'l10n_hu_technical_name': technical_name,
                    })
                    break
                else:
                    pass

        # Return
        return

    # Business methods
    @api.model
    def l10n_hu_get_vat_configuration(self):
        """ Get hungarian VAT configuration """
        # Initialize variables
        debug_list = []
        error_list = []
        info_list = []
        result = {}
        vat_configuration = []
        warning_list = []

        # SALES taxes
        # # Sales 27% (net)
        try:
            l10n_hu_1_f27 = self.env.ref('account.1_F27')
        except (KeyError, ValueError):
            l10n_hu_1_f27 = False
        vat_configuration.append({
            'account_tax': l10n_hu_1_f27,
            'amount': 27.0000,
            'l10n_hu_technical_name': 'l10n_hu_1_f27',
            'l10n_hu_vat_amount_mismatch_case': False,
            'l10n_hu_vat_exemption_case': False,
            'l10n_hu_vat_out_of_scope_case': False,
            'l10n_hu_vat_reason': False,
            'l10n_hu_vat_type': 'percentage',
            'price_include': False,
            'type_tax_type': 'sale',
        })

        # Sales 18% (net)
        try:
            l10n_hu_1_f18 = self.env.ref('account.1_F18')
        except (KeyError, ValueError):
            l10n_hu_1_f18 = False
        vat_configuration.append({
            'account_tax': l10n_hu_1_f18,
            'amount': 18.0000,
            'l10n_hu_technical_name': 'l10n_hu_1_f18',
            'l10n_hu_vat_amount_mismatch_case': False,
            'l10n_hu_vat_exemption_case': False,
            'l10n_hu_vat_out_of_scope_case': False,
            'l10n_hu_vat_reason': False,
            'l10n_hu_vat_type': 'percentage',
            'price_include': False,
            'type_tax_type': 'sale',
        })

        # Sales 5% (net)
        try:
            l10n_hu_1_f5 = self.env.ref('account.1_F5')
        except (KeyError, ValueError):
            l10n_hu_1_f5 = False
        vat_configuration.append({
            'account_tax': l10n_hu_1_f5,
            'amount': 5.0000,
            'l10n_hu_technical_name': 'l10n_hu_1_f5',
            'l10n_hu_vat_amount_mismatch_case': False,
            'l10n_hu_vat_exemption_case': False,
            'l10n_hu_vat_out_of_scope_case': False,
            'l10n_hu_vat_reason': False,
            'l10n_hu_vat_type': 'percentage',
            'price_include': False,
            'type_tax_type': 'sale',
        })

        # Sales Subject 0% AAM
        try:
            l10n_hu_1_fa = self.env.ref('account.1_FA')
        except (KeyError, ValueError):
            l10n_hu_1_fa = False
        vat_configuration.append({
            'account_tax': l10n_hu_1_fa,
            'amount': 0.0000,
            'l10n_hu_technical_name': 'l10n_hu_1_fa',
            'l10n_hu_vat_amount_mismatch_case': False,
            'l10n_hu_vat_exemption_case': 'aam',
            'l10n_hu_vat_out_of_scope_case': False,
            'l10n_hu_vat_reason': "AAM",
            'l10n_hu_vat_type': 'exemption',
            'price_include': False,
            'type_tax_type': 'sale',
        })

        # PURCHASE
        # # Purchase 27% (net)
        try:
            l10n_hu_1_v27 = self.env.ref('account.1_V27')
        except (KeyError, ValueError):
            l10n_hu_1_v27 = False
        vat_configuration.append({
            'account_tax': l10n_hu_1_v27,
            'amount': 27.0000,
            'l10n_hu_technical_name': 'l10n_hu_1_v27',
            'l10n_hu_vat_amount_mismatch_case': False,
            'l10n_hu_vat_exemption_case': False,
            'l10n_hu_vat_out_of_scope_case': False,
            'l10n_hu_vat_reason': False,
            'l10n_hu_vat_type': 'percentage',
            'price_include': False,
            'type_tax_type': 'purchase',
        })

        # # Purchase 18% (net)
        try:
            l10n_hu_1_v18 = self.env.ref('account.1_V18')
        except (KeyError, ValueError):
            l10n_hu_1_v18 = False
        vat_configuration.append({
            'account_tax': l10n_hu_1_v18,
            'amount': 18.0000,
            'l10n_hu_technical_name': 'l10n_hu_1_v18',
            'l10n_hu_vat_amount_mismatch_case': False,
            'l10n_hu_vat_exemption_case': False,
            'l10n_hu_vat_out_of_scope_case': False,
            'l10n_hu_vat_reason': False,
            'l10n_hu_vat_type': 'percentage',
            'price_include': False,
            'type_tax_type': 'purchase',
        })

        # # Purchase 5% (net)
        try:
            l10n_hu_1_v5 = self.env.ref('account.1_V5')
        except (KeyError, ValueError):
            l10n_hu_1_v5 = False
        vat_configuration.append({
            'account_tax': l10n_hu_1_v5,
            'amount': 5.0000,
            'l10n_hu_technical_name': 'l10n_hu_1_v5',
            'l10n_hu_vat_amount_mismatch_case': False,
            'l10n_hu_vat_exemption_case': False,
            'l10n_hu_vat_out_of_scope_case': False,
            'l10n_hu_vat_reason': False,
            'l10n_hu_vat_type': 'percentage',
            'price_include': False,
            'type_tax_type': 'purchase',
        })

        # # Purchase 0% Subject AAM
        try:
            l10n_hu_1_va = self.env.ref('account.1_VA')
        except (KeyError, ValueError):
            l10n_hu_1_va = False
        vat_configuration.append({
            'account_tax': l10n_hu_1_va,
            'amount': 0.0000,
            'l10n_hu_technical_name': 'l10n_hu_1_va',
            'l10n_hu_vat_amount_mismatch_case': False,
            'l10n_hu_vat_exemption_case': 'aam',
            'l10n_hu_vat_out_of_scope_case': False,
            'l10n_hu_vat_reason': "AAM",
            'l10n_hu_vat_type': 'exemption',
            'price_include': False,
            'type_tax_type': 'purchase',
        })

        try:
            l10n_hu_1_ft = self.env.ref('account.1_FT')
        except (KeyError, ValueError):
            l10n_hu_1_ft = False

        try:
            l10n_hu_1_vt = self.env.ref('account.1_VT')
        except (KeyError, ValueError):
            l10n_hu_1_vt = False

        try:
            l10n_hu_1_ff = self.env.ref('account.1_FF')
        except (KeyError, ValueError):
            l10n_hu_1_ff = False

        try:
            l10n_hu_1_vf = self.env.ref('account.1_VF')
        except (KeyError, ValueError):
            l10n_hu_1_vf = False

        try:
            l10n_hu_1_feu = self.env.ref('account.1_FEU')
        except (KeyError, ValueError):
            l10n_hu_1_feu = False

        try:
            l10n_hu_1_veu = self.env.ref('account.1_VEU')
        except (KeyError, ValueError):
            l10n_hu_1_veu = False

        try:
            l10n_hu_1_feuo = self.env.ref('account.1_FEUO')
        except (KeyError, ValueError):
            l10n_hu_1_feuo = False

        try:
            l10n_hu_1_veuo = self.env.ref('account.1_VEUO')
        except (KeyError, ValueError):
            l10n_hu_1_veuo = False

        try:
            l10n_hu_1_vaht = self.env.ref('account.1_VAHT')
        except (KeyError, ValueError):
            l10n_hu_1_vaht = False

        # Update result
        result.update({
            'debug_list': debug_list,
            'error_list': error_list,
            'info_list': info_list,
            'vat_configuration': vat_configuration,
            'warning_list': warning_list,
        })

        # Return result
        return result
