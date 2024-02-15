# -*- coding: utf-8 -*-
# 1 : imports of python lib

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 : imports from odoo modules
from odoo.tools.safe_eval import safe_eval

# 4 : variable declarations


# Class
class L10nHuInvoiceAccountMove(models.Model):
    # Private attributes
    _inherit = 'account.move'

    # Default methods

    # Field declarations
    l10n_hu_journal_invoice_enabled = fields.Boolean(
        related='journal_id.l10n_hu_invoice_enabled',
        string="HU Invoice Journal",
    )
    l10n_hu_invoice = fields.Many2one(
        comodel_name='l10n.hu.invoice',
        copy=False,
        string="HU Invoice",
    )
    l10n_hu_invoice_status = fields.Selection(
        related='l10n_hu_invoice.invoice_status',
        string="HU Invoice Status",
    )

    # Compute and search fields, in the same order of field declarations

    # Constraints and onchanges

    # CRUD methods (and name_get, name_search, ...) overrides

    # Action methods

    # Business methods
    # # SUPER OVERRIDES
    def _get_report_base_filename(self):
        """ Super override of original Odoo method to support cancelled invoices in customer portal"""
        # Ensure one record in self
        self.ensure_one()

        # Execute super
        result = super(L10nHuInvoiceAccountMove, self)._get_report_base_filename()

        # Manage cancelled invoices
        if self.move_type == 'out_invoice' and self.state == 'cancel':
            return self.move_type == 'out_invoice' and self.state == 'cancel' and (self.name)
        elif self.move_type == 'out_refund' and self.state == 'cancel':
            return self.move_type == 'out_refund' and self.state == 'cancel' and (self.name)
        elif self.move_type == 'in_invoice' and self.state == 'cancel':
            return self.move_type == 'in_invoice' and self.state == 'cancel' and (self.name)
        elif self.move_type == 'in_refund' and self.state == 'cancel':
            return self.move_type == 'in_refund' and self.state == 'cancel' and (self.name)
        else:
            return result
