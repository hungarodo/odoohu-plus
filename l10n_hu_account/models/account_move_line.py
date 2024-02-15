# -*- coding: utf-8 -*-
# 1 : imports of python lib

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 : imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuAccountInvoiceAccountMoveLine(models.Model):
    # Private attributes
    _inherit = 'account.move.line'

    # Default methods

    # Field declarations
    l10n_hu_is_price_refund = fields.Boolean(
        compute='_compute_l10n_hu_is_price_refund',
        string="Price Refund",
    )
    l10n_hu_vat_date = fields.Date(
        string="VAT Date",
    )
    l10n_hu_vat_reason = fields.Char(
        string="HU Tax Reason",
        translate="True",
    )
    l10n_hu_original_account_move = fields.Many2one(
        related='move_id.l10n_hu_original_account_move',
        string="Original Move",
    )
    l10n_hu_original_account_move_line = fields.Many2one(
        comodel_name='account.move.line',
        index=True,
        string="Original Move Line",
    )
    
    # Compute and search fields, in the same order of field declarations
    def _compute_l10n_hu_is_price_refund(self):
        for record in self:
            is_price_refund = False
            """ NOTE: rewrite to new analytic plan
            refund_price_tag = record.move_id.journal_id.l10n_hu_invoice_refund_price_tag
            if refund_price_tag and record.analytic_tag_ids:
                for tag in record.analytic_tag_ids:
                    if tag == refund_price_tag:
                        is_price_refund = True
                        break
                    else:
                        pass
            """
            record.l10n_hu_is_price_refund = is_price_refund

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
