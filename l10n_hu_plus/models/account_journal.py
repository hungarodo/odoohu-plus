# -*- coding: utf-8 -*-
# 1 : imports of python lib

# 2 :  imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 :  imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuPlusAccountJournal(models.Model):
    # Private attributes
    _inherit = 'account.journal'

    # Default methods

    # Field declarations
    l10n_hu_delivery_date_default = fields.Selection(
        copy=False,
        default='none',
        selection=[
            ('none', "None"),
            ('today', "Today"),
        ],
        string="HU Delivery Date Default",
    )
    l10n_hu_document_type = fields.Many2many(
        column1='journal',
        column2='document_type',
        comodel_name='l10n.hu.plus.object',
        domain=[('type_technical_name', '=', 'document_type')],
        index=True,
        relation='l10n_hu_journal_document_type_rel',
        string="HU Document Type",
    )

    # Compute and search fields, in the same order of field declarations

    # Constraints and onchanges

    # CRUD methods (and display_name, name_search, ...) overrides

    # Action methods

    # Business methods
