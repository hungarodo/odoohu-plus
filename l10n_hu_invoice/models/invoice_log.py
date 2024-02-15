# -*- coding: utf-8 -*-
# 1 : imports of python lib
import json

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 : imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuInvoiceInvoiceLog(models.Model):
    # Private attributes
    _name = 'l10n.hu.invoice.log'
    _description = "HU Invoice Log"
    _order = 'timestamp desc, id desc'

    # Default methods

    # Field declarations
    account_move = fields.Many2one(
        related='invoice.account_move',
        store=True,
        string="Account Move",
    )
    company = fields.Many2one(
        related='invoice.company',
        store=True,
        string="Company",
    )
    description = fields.Text(
        copy=False,
        readonly=True,
        string="Description",
    )
    invoice_number = fields.Char(
        copy=False,
        readonly=True,
        string="Invoice Number",
    )
    linked_user = fields.Many2one(
        comodel_name='res.users',
        copy=False,
        readonly=True,
        string="Linked User",
    )
    details_error = fields.Text(
        copy=False,
        readonly=True,
        string="Details Error",
    )
    details_info = fields.Text(
        copy=False,
        readonly=True,
        string="Details Info",
    )
    details_success = fields.Text(
        copy=False,
        readonly=True,
        string="Details Success",
    )
    details_warning = fields.Text(
        copy=False,
        readonly=True,
        string="Details Warning",
    )
    invoice = fields.Many2one(
        comodel_name='l10n.hu.invoice',
        copy=False,
        ondelete='cascade',
        readonly=True,
        string="Invoice",
    )
    invoice_data = fields.Text(
        copy=False,
        readonly=True,
        string="Invoice Data",
    )
    related_invoice_number = fields.Char(
        copy=False,
        readonly=True,
        string="Related Invoice Number",
    )
    related_invoice = fields.Many2one(
        comodel_name='l10n.hu.invoice',
        copy=False,
        readonly=True,
        string="Related Invoice",
    )
    source = fields.Char(
        copy=False,
        readonly=True,
        string="Source",
    )
    technical_data = fields.Text(
        copy=False,
        readonly=True,
        string="Technical Data",
    )
    technical_name = fields.Char(
        copy=False,
        readonly=True,
        string="Technical Name",
    )
    technical_status = fields.Char(
        copy=False,
        readonly=True,
        string="Technical Status",
    )
    technical_timestamp = fields.Datetime(
        copy=False,
        default=fields.Datetime.now(),
        readonly=True,
        string="Technical Timestamp",
    )
    timestamp = fields.Datetime(
        copy=False,
        default=fields.Datetime.now(),
        readonly=True,
        string="Timestamp",
    )

    # Compute and search fields, in the same order of field declarations

    # Constraints and onchanges

    # CRUD methods (and name_get, name_search, ...) overrides
    def name_get(self):
        # Initialize variables
        result = []

        # Iterate through self
        for record in self:
            # NOTE: INVLOG = Invoice Log
            name = "INVLOG-" + str(record.id)
            if record.invoice:
                name += " " + record.invoice.invoice_number
            if record.timestamp:
                name += " " + str(record.timestamp)

            # Append to list
            result.append((record.id, name))

        # Return
        return result

    # Action methods

    # Business methods
    @api.model
    def create_log(self, values):
        """ Create invoice log

        :param values: dictionary

        :return: dictionary
        """
        # raise exceptions.UserError("create_log BEGIN" + str(values))

        # Initialize variables
        debug_list = []
        error_list = []
        info_list = []
        mail_message = False
        result = {}
        warning_list = []

        # invoice
        if values.get('invoice'):
            invoice = values['invoice']
            debug_list.append("invoice found in values: " + str(invoice))
        else:
            invoice = False
            error_list.append("invoice not found in values")

        # create_values
        create_values_result = self.get_create_values(values)
        create_values = create_values_result.get('create_values', {})
        if len(create_values) == 0:
            error_list.append("create_values len is 0")

        # DO create
        if len(error_list) == 0:
            invoice_log = self.env['l10n.hu.invoice.log'].create(create_values)
        else:
            invoice_log = False
            debug_list.append("log create skipped due to previous errors")

        # Update result
        result.update({
            'debug_list': debug_list,
            'error_list': error_list,
            'info_list': info_list,
            'invoice': invoice,
            'invoice_log': invoice_log,
            'warning_list': warning_list,
        })
        if len(error_list) == 0:
            result.update({
                'result_type': 'success',
            })
        else:
            result.update({
                'result_type': 'error',
            })

        # Return result
        # raise exceptions.UserError("create_log END" + str(result))
        return result

    @api.model
    def get_create_values(self, values):
        """ Create NAV invoice log

        :param values: dictionary

        :return: dictionary
        """
        # raise exceptions.UserError("get_create_values BEGIN" + str(values))

        # Initialize variables
        create_values = values
        debug_list = []
        error_list = []
        info_list = []
        result = {}
        warning_list = []

        # sanitize keys
        try:
            model_id = self.env.ref('l10n_hu_account_invoice.model_l10n_hu_invoice_log').id
            model_fields = self.env['ir.model.fields'].sudo().search([
                ('model_id', '=', model_id)
            ])
            model_field_list = []
            for model_field in model_fields:
                model_field_list.append(model_field.name)
        except:
            model_field_list = []
        for key in list(create_values):
            if key not in model_field_list:
                create_values.pop(key)

        # invoice
        if values.get('invoice'):
            invoice = values['invoice']
            create_values.update({
                'invoice': invoice.id
            })
            debug_list.append("invoice found in values: " + str(invoice))
        else:
            invoice = False
            create_values.update({
                'invoice': False
            })
            error_list.append("invoice not found in values")

        # invoice_number
        if not create_values.get('invoice_number') \
                and invoice \
                and invoice.invoice_number:
            create_values.update({
                'invoice_number': invoice.invoice_number
            })

        # linked_user
        if not create_values.get('linked_user') and self.env.uid:
            create_values.update({
                'linked_user': self.env.uid
            })

        # invoice_data
        if values.get('log_invoice_data') and invoice:
            read_result = invoice.sudo().read()[0]
            create_values.update({
                'invoice_data': json.dumps(read_result, default=str)
            })

        # related_invoice
        if values.get('related_invoice'):
            related_invoice = values['related_invoice']
            create_values.update({
                'related_invoice': related_invoice.id
            })
            debug_list.append("related_invoice found in values: " + str(related_invoice))
        else:
            create_values.update({
                'related_invoice': False
            })
            debug_list.append("related_invoice not found in values")

        # related_invoice_number
        if not create_values.get('related_invoice_number') \
                and create_values.get('related_invoice') \
                and create_values['related_invoice'].invoice_number:
            create_values.update({
                'related_invoice_number': create_values['related_invoice'].invoice_number
            })

        # timestamp
        if not values.get('timestamp'):
            create_values.update({
                'timestamp': fields.Datetime.now()
            })

        # Update result
        result.update({
            'create_values': create_values,
            'debug_list': debug_list,
            'error_list': error_list,
            'info_list': info_list,
            'warning_list': warning_list,
        })

        # Return result
        # raise exceptions.UserError("get_create_values END" + str(result))
        return result
