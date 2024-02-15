# -*- coding: utf-8 -*-
# 1 : imports of python lib

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 : imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuInvoiceAccountMoveLine(models.Model):
    # Private attributes
    _inherit = 'account.move.line'

    # Default methods

    # Field declarations

    # Compute and search fields, in the same order of field declarations

    # Constraints and onchanges

    # CRUD methods (and name_get, name_search, ...) overrides

    # Action methods

    # Business methods
    @api.model
    def l10n_hu_is_processable_invoice_line(self):
        """ Determine if an account move line is processable as HU invoice line

        :return: boolean
        """
        # is_rounding_line
        is_rounding_line = self.l10n_hu_is_invoice_rounding_line()

        # rounding_enabled
        if self.move_id and self.move_id.journal_id:
            rounding_enabled = self.move_id.journal_id.l10n_hu_invoice_rounding_enabled
        else:
            rounding_enabled = False

        # Evaluate
        if is_rounding_line and rounding_enabled:
            result = True
        elif self.display_type == 'product':
            result = True
        else:
            result = False

        # Return
        return result

    @api.model
    def l10n_hu_is_processable_invoice_summary(self):
        """ Determine if an account move line is processable as a HU invoice summary

        :return: boolean
        """
        # is_rounding_line
        is_rounding_line = self.l10n_hu_is_invoice_rounding_line()

        # rounding_enabled
        if self.move_id and self.move_id.journal_id:
            rounding_enabled = self.move_id.journal_id.l10n_hu_invoice_rounding_enabled
        else:
            rounding_enabled = False

        # Evaluate
        if is_rounding_line and rounding_enabled:
            result = True
        elif self.display_type == 'product':
            result = True
        elif self.display_type == 'tax':
            result = True
        else:
            result = False

        # Return
        return result
