# -*- coding: utf-8 -*-
# 1 : imports of python lib

# 2 : imports of odoo
from odoo import api, fields, models  # alphabetically ordered

# 3 : imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuInvoiceXmlExport(models.Model):
    # Private attributes
    _name = 'l10n.hu.invoice.xml.export'
    _description = "HU Invoice XML Export"
    _inherit = ['mail.thread']
    _order = 'id desc'

    # Default methods

    # Field declarations
    company = fields.Many2one(
        comodel_name='res.company',
        default=lambda self: self.env.company.id,
        index=True,
        required=True,
        string="Company",
    )
    date_start = fields.Date(
        string="Start Date",
    )
    date_end = fields.Date(
        string="End Date",
    )
    export_date = fields.Date(
        default=fields.Date.today(),
        required=True,
        string="Export Date",
    )
    export_invoice_count = fields.Integer(
        help="Count of invoices included in the export",
        index=True,
        string="Invoice Count",
    )
    filter_by = fields.Selection(
        default='invoice_date',
        required=True,
        selection=[
            ('invoice_date', "Invoice Date"),
            ('delivery_date', "Delivery Date"),
            ('invoice_number', "Invoice Number")
        ],
        string="Filter",
    )
    invoice_number_end = fields.Many2one(
        comodel_name='l10n.hu.invoice',
        string="Invoice Number End",
    )
    invoice_number_start = fields.Many2one(
        comodel_name='l10n.hu.invoice',
        string="Invoice Number Start",
    )
    invoice_type = fields.Selection(
        default='out_invoice',
        selection=[
            ('out_invoice', "Customer Invoice"),
            ('in_invoice', "Vendor Bill")
        ],
        string="Invoice Type",
    )
    journal = fields.Many2many(
        comodel_name='account.journal',
        column1='export',
        column2='journal',
        relation='l10n_hu_invoice_xml_export_journal_rel',
        string="Journal",
    )
    order_by = fields.Selection(
        default='date',
        required=True,
        selection=[
            ('date', "Invoice Date"),
            ('invoice_number', "Invoice Number")
        ],
        string="Order By",
    )
    status = fields.Selection(
        default='new',
        selection=[
            ('new', "New"),
            ('export_done', "Export Done"),
            ('export_empty', "Export Empty")
        ],
        string="Status"
    )
    xml_data = fields.Binary(
        readonly=True,
        string="XML",
    )
    xml_file_name = fields.Char(
        readonly=True,
        string="XML file name"
    )

    # Compute and search fields, in the same order of field declarations

    # Constraints and onchanges

    # CRUD methods (and name_get, name_search, ...) overrides
    def name_get(self):
        # Initialize variables
        result = []

        # Iterate through self
        for record in self:
            # Set name
            name = "NAVINVEXP-" + str(record.id)

            # Append to list
            result.append((record.id, name))

        # Return result
        return result

    # Action methods

    # Business methods
