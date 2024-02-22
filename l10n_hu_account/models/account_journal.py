# -*- coding: utf-8 -*-
# 1 : imports of python lib

# 2 :  imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 :  imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuAccountJournal(models.Model):
    # Private attributes
    _inherit = 'account.journal'

    # Default methods

    # Field declarations
    l10n_hu_currency_rate_inverse = fields.Boolean(
        default=False,
        string="HU Currency Rate Inverse",
    )
    l10n_hu_document_type = fields.Many2many(
        column1='journal',
        column2='document_type',
        comodel_name='l10n.hu.document.type',
        index=True,
        relation='l10n_hu_account_journal_document_type_rel',
        string="HU Document Type",
    )
    l10n_hu_eu_oss_enabled = fields.Boolean(
        copy=False,
        default=False,
        string="HU EU OSS Enabled",
    )
    l10n_hu_proforma_advance_journal = fields.Many2one(
        comodel_name='account.journal',
        index=True,
        string="HU Proforma Advance Journal",
    )
    l10n_hu_show_print_pdf = fields.Boolean(
        copy=False,
        default=False,
        string="HU Show Print PDF",
    )
    l10n_hu_technical_type = fields.Selection(
        copy=False,
        selection=[
            ('invoice', "Invoice"),
            ('proforma', "Proforma"),
        ],
        index=True,
        string="HU Technical Type",
    )
    
    # Compute and search fields, in the same order of field declarations

    # Constraints and onchanges

    # CRUD methods (and name_get, name_search, ...) overrides

    # Action methods

    # Business methods
