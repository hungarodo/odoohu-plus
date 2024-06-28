# -*- coding: utf-8 -*-
# 1 : imports of python lib

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 : imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuPlusAccountMoveLine(models.Model):
    # Private attributes
    _inherit = 'account.move.line'

    # Default methods

    # Field declarations
    l10n_hu_original_account_move = fields.Many2one(
        related='move_id.l10n_hu_original_account_move',
        string="Original Move",
    )
    l10n_hu_original_account_move_line = fields.Many2one(
        comodel_name='account.move.line',
        index=True,
        string="Original Move Line",
    )
    l10n_hu_price_refund = fields.Boolean(
        default=False,
        string="Price Refund",
    )
    l10n_hu_move_trade_position = fields.Selection(
        related='move_id.l10n_hu_trade_position',
        index=True,
        store=True,
        string="Trade Position Date",
    )
    l10n_hu_move_vat_date = fields.Date(
        related='move_id.l10n_hu_vat_date',
        index=True,
        store=True,
        string="VAT Date",
    )
    l10n_hu_vat_reason = fields.Char(
        string="VAT Reason",
        translate="True",
    )
    
    # Compute and search fields, in the same order of field declarations

    # Constraints and onchanges

    # CRUD methods (and name_get, name_search, ...) overrides

    # Action methods

    # Business methods
    @api.model
    def l10n_hu_is_invoice_rounding_line(self):
        """ Determine if an account move line is a HU invoice rounding line

        :return: boolean
        """

        # Check display_type
        if self.display_type == 'rounding':
            is_rounding_line = True
        else:
            is_rounding_line = False

        # Evaluate
        if is_rounding_line:
            result = True
        else:
            result = False

        # Return
        return result
