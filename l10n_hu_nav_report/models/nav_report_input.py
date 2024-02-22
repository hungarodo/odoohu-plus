# -*- coding: utf-8 -*-
# 1 : imports of python lib

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 : imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuNavReportInput(models.Model):
    # Private attributes
    _name = 'l10n.hu.nav.report.input'
    _description = "HU NAV Report Input"
    _order = 'date asc, id desc'

    # Default methods

    # Field declarations
    account_move = fields.Many2one(
        related='account_move_line.move_id',
        store=True,
        string="Account Move",
    )
    account_move_line = fields.Many2one(
        comodel_name='account.move.line',
        readonly=True,
        string="Account Move Line",
    )
    active = fields.Boolean(
        related='report.active',
        store=True,
        string="Active",
    )
    code = fields.Char(
        string="Code",
    )
    company = fields.Many2one(
        comodel_name='res.company',
        index=True,
        related='report.company',
        store=True,
        string="Company",
    )
    company_currency = fields.Many2one(
        comodel_name='res.currency',
        related='company.currency_id',
        readonly=True,
    )
    customer = fields.Many2one(
        comodel_name='res.partner',
        string="Customer",
    )
    date = fields.Date(
        string="Date",
    )
    description = fields.Text(
        string="Description",
    )
    is_locked = fields.Boolean(
        default=False,
        string="Locked",
    )
    name = fields.Char(
        string="Name",
    )
    report = fields.Many2one(
        comodel_name='l10n.hu.nav.report',
        index=True,
        ondelete='cascade',
        required=True,
        string="Report",
    )
    quantity = fields.Float(
        string="Quantity"
    )
    rule = fields.Many2one(
        comodel_name='l10n.hu.nav.report.rule',
        index=True,
        string="Rule",
    )
    status = fields.Selection(
        related='report.status',
        store=True,
        string="Status",
    )
    partner = fields.Many2one(
        comodel_name='res.partner',
        readonly=True,
        string="Partner",
    )
    value_char = fields.Char(
        string="Value Char",
    )
    value_date = fields.Date(
        string="Value Date",
    )
    value_float = fields.Float(
        string="Value Float",
    )
    value_integer = fields.Integer(
        string="Value Integer",
    )

    # Compute and search fields, in the same order of field declarations

    # Constraints and onchanges

    # CRUD methods (and name_get, name_search, ...) overrides

    # Action methods

    # Business methods

