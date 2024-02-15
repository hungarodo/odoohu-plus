# -*- coding: utf-8 -*-
# 1 : imports of python lib

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered


# 3 : imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuBaseWizardLine(models.TransientModel):
    # Private attributes
    _name = 'l10n.hu.wizard.line'
    _description = "HU Wizard Line"

    # Default methods

    # Field declarations
    name = fields.Char(
        string="Name",
    )
    wizard = fields.Many2one(
        comodel_name="l10n.hu.wizard",
        copy=False,
        readonly=True,
        string="Wizard",
    )

    # Compute and search fields, in the same order of field declarations

    # Constraints and onchanges

    # CRUD methods (and name_get, name_search, ...) overrides

    # Action methods

    # Business methods
