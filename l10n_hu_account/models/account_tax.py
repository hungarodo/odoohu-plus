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
    l10n_hu_technical_name = fields.Char(
        copy=False,
        string="HU Technical Name",
    )
    l10n_hu_vat_amount_mismatch_case = fields.Selection(
        help="VAT amount mismatch case according to NAV (Hungarian Tax Authority) regulations",
        selection=[
            ('refundable_vat', "REFUNDABLE - VAT must be refunded by the recipient of the invoice"),
            ('nonrefundable_vat', "NONREFUNDABLE - VAT does not need to be refunded by the recipient of the invoice"),
            ('unknown', "UNKNOWN - Pre-3.0 invoice"),
        ],
        string="HU VAT Mismatch Case",
    )
    l10n_hu_vat_exemption_case = fields.Selection(
        help="VAT exemption case according to NAV (Hungarian Tax Authority) regulations",
        selection=[
            ('aam', "AAM - Personal tax exemption"),
            ('tam', "TAM - Tax-exempt activity"),
            ('kbaet', "KBAET - Intra-Community"),
            ('kbauk', "KBAUK - Intra-Community New Transport"),
            ('eam', "EAM - Extra-Community"),
            ('nam', "NAM - Other International"),
            ('unknown', "UNKNOWN - Pre-3.0 invoice"),
        ],
        string="HU VAT Exemption Case",
    )
    l10n_hu_vat_out_of_scope_case = fields.Selection(
        help="VAT out-of-scope case according to NAV (Hungarian Tax Authority) regulations",
        selection=[
            ('atk', "ATK - Outside the scope of VAT"),
            ('eufad37', "EUFAD37 - VAT§37 Intra-Community Reverse Charge"),
            ('eufade', "EUFADE - Non-VAT§37 Intra-Community Reverse Charge"),
            ('eue', "EUE - Intra-Community non-reverse charge"),
            ('ho', "HO - Transaction in a third country"),
            ('unknown', "UNKNOWN - Pre-3.0 invoice"),
        ],
        string="HU VAT Out of Scope Case",
    )
    l10n_hu_vat_reason = fields.Char(
        copy=False,
        help="Reason for VAT exemption and out of scope cases",
        string="HU VAT Reason",
        translate="True",
    )
    l10n_hu_vat_type = fields.Selection(
        copy=False,
        default='out_of_scope',
        help="NAV (Hungarian Tax Authority) VAT type",
        selection=[
            ('percentage', "Percentage"),
            ('exemption', "Exemption"),
            ('out_of_scope', "Out Of Scope"),
            ('domestic_reverse_charge', "Domestic Reverse Charge"),
            ('margin_scheme_vat', "Margin Scheme VAT"),
            ('margin_scheme_no_vat', "Margin Scheme No VAT"),
        ],
        string="HU VAT Type",
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
