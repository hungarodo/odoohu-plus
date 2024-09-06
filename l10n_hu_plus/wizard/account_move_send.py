# -*- coding: utf-8 -*-
# 1 : imports of python lib

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models, tools  # alphabetically ordered

# 3 : imports from odoo modules

# 4 : initialize variables


# Class
class L10nHuPlusAccountMoveSend(models.TransientModel):
    # Private attributes
    _inherit = 'account.move.send'

    # Default methods

    # Field declarations

    # Compute and search fields, in the same order of fields declaration

    # Constraints and onchanges

    # CRUD methods (and display_name, name_search, ...) overrides

    # Action methods

    # Business methods
    # # SUPER
    @api.depends('checkbox_send_mail')
    def _compute_send_mail_extra_fields(self):
        """ Super override of original method in account app"""
        super()._compute_send_mail_extra_fields()
        for wizard in self:
            wizard.send_mail_readonly = False
        return
