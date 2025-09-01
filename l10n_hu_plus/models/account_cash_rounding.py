# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountCashRounding(models.Model):
    _inherit = "account.cash.rounding"

    l10n_hu_payment_term = fields.One2many(
        comodel_name="account.payment.term",
        inverse_name="l10n_hu_rounding_method",
        string="Payment Terms",
        help="Payment terms that use this cash rounding.",
    )
