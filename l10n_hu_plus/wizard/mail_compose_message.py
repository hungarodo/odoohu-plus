# -*- coding: utf-8 -*-
# 1 : imports of python lib
from ast import literal_eval

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 : imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuPlusMailComposeMessage(models.TransientModel):
    # Private attributes
    _inherit = 'mail.compose.message'

    # Default methods

    # Field declarations

    # Compute and search fields, in the same order of field declarations

    # Constraints and onchanges

    # CRUD methods (and display_name, name_search, ...) overrides

    # Action methods
    def _action_send_mail(self, auto_commit=False):
        result = super(L10nHuPlusMailComposeMessage, self)._action_send_mail(auto_commit=auto_commit)
        if self.model == 'account.move' and self.env.context.get('l10n_hu_use_proforma', False):
            account_moves = self.env['account.move'].browse(literal_eval(self.res_ids))
            for account_move in account_moves:
                account_move.write({'l10n_hu_proforma_date': fields.Date.today()})
        return result

    # Business methods
