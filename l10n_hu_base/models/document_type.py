# -*- coding: utf-8 -*-
# 1 : imports of python lib

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 : imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuAccountBaseDocumentType(models.Model):
    # Private attributes
    _name = 'l10n.hu.document.type'
    _description = "Hungary Document Type"
    _inherit = ['image.mixin', 'mail.activity.mixin', 'mail.thread']

    # Default methods

    # Field declarations
    active = fields.Boolean(
        default=True,
        index=True,
        string="Active",
        tracking=2,
    )
    code = fields.Char(
        copy=False,
        index=True,
        string="Code",
        tracking=True,
    )
    company = fields.Many2one(
        comodel_name='res.company',
        default=lambda self: self.env.company.id,
        index=True,
        readonly=True,
        required=True,
        string="Company",
    )
    description = fields.Text(
        string="Description",
    )
    name = fields.Char(
        index=True,
        required=True,
        string="Name",
        translate=True,
        tracking=1,
    )
    priority = fields.Integer(
        default=10,
        index=True,
        string="Priority",
    )
    technical_name = fields.Char(
        index=True,
        string="Technical Name",
    )

    # Compute and search fields, in the same order of field declarations

    # Constraints and onchanges

    # CRUD methods (and name_get, name_search, ...) overrides

    # Action methods

    # Business methods
