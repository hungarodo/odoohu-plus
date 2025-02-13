# -*- coding: utf-8 -*-
# 1 : imports of python lib

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models, tools  # alphabetically ordered

# 3 : imports from odoo modules

# 4 : initialize variables


# Class
class L10nHuPlusAccountMoveReversal(models.TransientModel):
    # Private attributes
    _inherit = 'account.move.reversal'

    # Default methods

    # Field declarations
    l10n_hu_storno_enabled = fields.Boolean(
        default=False,
        string="HU Storno Enabled",
    )
    l10n_hu_storno_visible = fields.Boolean(
        compute='_compute_l10n_hu_storno_visible',
        string="HU Storno Visible",
    )

    # Compute and search fields, in the same order of field declarations
    @api.depends('move_ids')
    def _compute_l10n_hu_storno_visible(self):
        for record in self:
            # Initialize variables
            checked_account_move_count = 0
            compatible_account_moves = []

            # Iterate account moves
            for account_move in record.move_ids:
                checked_account_move_count += 1
                if account_move.l10n_hu_get_storno_allowed():
                    compatible_account_moves.append(account_move)

            # Set field value
            if len(compatible_account_moves) == checked_account_move_count:
                record.l10n_hu_storno_visible = True
            else:
                record.l10n_hu_storno_visible = False

    # Constraints and onchanges

    # CRUD methods (and display_name, name_search, ...) overrides

    # Action methods

    # Business methods
    ## SUPER
    def reverse_moves(self, is_modify=False):
        action = super().reverse_moves(is_modify=is_modify)
        storno_document_type = self.env['l10n.hu.plus.tag'].search([
            ('company', '=', self.company_id.id),
            ('tag_type', '=', 'document_type'),
            ('technical_name', '=', 'invoice_storno'),
        ], limit=1)
        if self.l10n_hu_storno_enabled and storno_document_type:
            # NOTES: is_modify = storno & create draft
            # In this case self.new_move_ids contains only the drafts, not the storno ones
            # So it is safer to search instead of relying on self.new_move_ids
            new_storno_moves = self.env['account.move'].search([
                ('move_type', '=', 'out_refund'),
                ('reversed_entry_id', 'in', self.move_ids.ids),
            ])
            for new_move in new_storno_moves:
                new_move.write({'l10n_hu_document_type': storno_document_type.id})
                # Run HU+ accounting automations and post it
                try:
                    new_move.action_l10n_hu_quick_accounting()
                    new_move.action_post()
                except:
                    pass
        else:
            pass
        return action
