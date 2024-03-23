# -*- coding: utf-8 -*-
# 1 : imports of python lib
import datetime
import json
import re

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 : imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuAccountWizard(models.TransientModel):
    # Private attributes
    _inherit = 'l10n.hu.wizard'

    # Default methods

    @api.model
    def _get_default_account_move(self):
        account_move_ids = []
        if self._context.get('active_model') and self._context['active_model'] == 'account.move':
            account_move_ids = self._context.get('active_ids', [])
        return [(4, x, 0) for x in account_move_ids]

    # Field declarations
    account_move = fields.Many2many(
        comodel_name='account.move',
        column1='wizard',
        column2='account_move',
        default=_get_default_account_move,
        relation='l10n_hu_wizard_account_move_rel',
        string="Account Move",
    )
    account_move_action = fields.Selection(
        selection=[
            ('list', "List"),
        ],
        string="Account Move Action",
    )
    account_move_action_editable = fields.Boolean(
        default=True,
        string="Account Move Action Editable",
    )
    account_move_count = fields.Integer(
        compute='_compute_account_move_count',
        string="Account Move Count",
    )
    account_move_visible = fields.Boolean(
        default=False,
        string="Account Move Visible",
    )

    # Compute and search fields, in the same order of field declarations
    def _compute_account_move_count(self):
        for record in self:
            record.account_move_count = len(record.account_move)

    # Constraints and onchanges

    # CRUD methods (and name_get, name_search, ...) overrides

    # Action methods
    def action_execute(self):
        """ Super override of original method in l10n_hu_base app """
        # Execute super
        result = super(L10nHuAccountWizard, self).action_execute()

        # ACCOUNT MOVE
        if self.action_type == 'currency_exchange' and self.account_move:
            # Write
            if len(self.account_move) == 1:
                self.account_move[0].write({
                    'l10n_hu_document_rate': self.exchange_rate
                })

                # Assemble result
                result = {
                    'type': 'ir.actions.act_window_close'
                }

                # Return result
                return result
        # else
        else:
            pass

        # Return result
        return result

    # Business methods
    @api.model
    def manage_account_move(self):
        """ Manage account move actions

        NOTE:
        - We may iterate because account move field is m2m to support mass management

        :return: dictionary
        """
        # Initialize variables
        account_moves = []
        account_move_ids = []
        account_move_ids_ignored = []
        account_move_ids_managed = []
        result = {}

        # Process scenarios
        if self.action_type == 'account_move':
            if self.account_move_action == 'compute_document_rate':
                operation_result = partner.l10n_hu_manage_partner({'operation': 'delete'})
            else:
                pass
        else:
            pass

        # Update result
        result.update({
            'account_moves': account_moves,
            'account_move_ids': account_move_ids,
            'account_move_ids_ignored': account_move_ids_ignored,
            'account_move_ids_managed': account_move_ids_managed,
        })

        # Return result
        # raise exceptions.UserError(str(result))
        return result
