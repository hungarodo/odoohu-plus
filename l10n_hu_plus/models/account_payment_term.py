# -*- coding: utf-8 -*-
# 1 : imports of python lib

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 : imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuPlusPaymentTerm(models.Model):
    # Private attributes
    _inherit = 'account.payment.term'

    # Default methods
    @api.model
    def _get_l10n_hu_nav_method_selection(self):
        return self.l10n_hu_get_nav_method_selection()

    # Field declarations
    l10n_hu_nav_method = fields.Selection(
        selection=_get_l10n_hu_nav_method_selection,
        copy=False,
        string="HU NAV Method",
    )

    # Compute and search fields, in the same order of field declarations

    # Constraints and onchanges

    # CRUD methods (and name_get, name_search, ...) overrides

    # Action methods

    # Business methods
    @api.model
    def l10n_hu_get_nav_method_selection(self):
        """ Get a selection field compatible list of NAV payment methods

        :return: list
        """
        # Assemble result
        result = [
            ('transfer', "Transfer"),
            ('cash', "Cash"),
            ('card', "Card"),
            ('voucher', "Voucher"),
            ('other', "Other"),
        ]

        # Return result
        return result

    @api.model
    def l10n_hu_get_nav_methods(self):
        """ Get list of NAV methods

        NOTE:
        - we call selection and assemble list

        :return: list
        """
        # Initialize variables
        result = []

        # Get selection
        selection_list = self.l10n_hu_get_nav_method_selection()

        # Assemble result
        for selection in selection_list:
            result.append(selection[0])

        # Return result
        return result
