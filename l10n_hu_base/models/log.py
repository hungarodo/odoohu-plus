# -*- coding: utf-8 -*-
# 1 : imports of python lib
import base64  # base64 encoding
import datetime
import hashlib  # passwords
import hmac
import json
import logging
import lxml  # xml processing
import requests  # http requests

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 : imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuBaseLog(models.Model):
    # Private attributes
    _name = 'l10n.hu.log'
    _description = "HU Log"
    _order = 'timestamp desc, id desc'

    # Default methods

    # Field declarations
    active = fields.Boolean(
        default=True,
        string="Active",
    )
    app = fields.Many2one(
        comodel_name='ir.module.module',
        index=True,
        readonly=True,
        string="App",
    )
    company = fields.Many2one(
        comodel_name='res.company',
        default=lambda self: self.env.company.id,
        readonly=True,
        required=True,
        string="Company",
    )
    description = fields.Text(
        help="Additional information",
        readonly=True,
        string="Description",
    )
    direction = fields.Selection(
        copy=False,
        selection=[
            ('incoming', "Incoming"),
            ('internal', "Internal"),
            ('outgoing', "Outgoing"),
        ],
        string="Direction",
    )
    level = fields.Selection(
        selection=[
            ('info', "INFO"),
            ('warning', "WARNING"),
            ('error', "ERROR"),
            ('debug', "DEBUG"),
        ],
        string="Level",
    )
    l10n_hu_object = fields.Many2many(
        comodel_name='l10n.hu.object',
        column1='log',
        column2='object',
        copy=False,
        readonly=True,
        relation='l10n_hu_log_object_rel',
        string="Object",
    )
    l10n_hu_object_count = fields.Integer(
        compute='_compute_l10n_hu_object_count',
        string="Object Count",
    )
    log_type = fields.Char(
        readonly=True,
        string="Log Type",
    )
    model = fields.Many2one(
        comodel_name='ir.model',
        index=True,
        readonly=True,
        string="Model",
    )
    name = fields.Char(
        readonly=True,
        string="Name",
    )
    source_model_name = fields.Char(
        copy=False,
        index=True,
        string="Source Model Name",
    )
    source_record_id = fields.Integer(
        copy=False,
        index=True,
        string="Source Record ID",
    )
    source_record_display_name = fields.Char(
        compute='_compute_source_record_info',
        string="Source Record Display Name",
    )
    status = fields.Selection(
        copy=False,
        default='new',
        readonly=True,
        selection=[
            ('new', "New"),
            ('processing', "Processing"),
            ('error', "Error"),
            ('done', "Done"),
        ],
        string="Status",
    )
    technical_data = fields.Text(
        copy=False,
        string="Technical Data",
    )
    technical_name = fields.Char(
        copy=False,
        index=True,
        string="Technical Name",
    )
    timestamp = fields.Datetime(
        copy=False,
        string="Processing Timestamp",
    )
    user_id = fields.Integer(
        readonly=True,
        string="User ID",
    )

    # Compute and search fields, in the same order of field declarations
    def _compute_l10n_hu_object_count(self):
        for record in self:
            record.l10n_hu_object_count = len(record.l10n_hu_object)

    @api.depends('source_model_name', 'source_record_id')
    def _compute_source_record_info(self):
        for record in self:
            # Initialize variables
            display_name = False

            # Get values
            if record.source_model_name and record.source_record_id:
                try:
                    source_record = self.env[record.source_model_name].sudo().search([
                        ('id', '=', record.source_record_id)
                    ])
                    if source_record:
                        display_name = source_record.display_name
                except:
                    pass

            # Set field
            record.source_record_display_name = display_name

    # Constraints and onchanges

    # CRUD methods (and name_get, name_search, ...) overrides
    def name_get(self):
        # Initialize variables
        result = []

        # Iterate through self
        for record in self:
            # Set name
            name = "HU-LOG-" + str(record.id)

            # Append to list
            result.append((record.id, name))

        # Return result
        return result

    # Action methods
    def action_delete(self):
        # Ensure one
        self.ensure_one()

        # Delete
        self.unlink()

        # Assemble result
        result = {
            'name': _("HU Logs"),
            'res_model': 'l10n.hu.log',
            'target': 'main',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
        }

        # Return result
        return result

    def action_list_objects(self):
        # Ensure one
        self.ensure_one()

        # Set l10n_hu_object_ids
        l10n_hu_object_ids = []
        for l10n_hu_object in self.l10n_hu_object:
            l10n_hu_object_ids.append(l10n_hu_object.id)

        # Assemble result
        result = {
            'name': _("HU Objects"),
            'domain': [('id', 'in', l10n_hu_object_ids)],
            'res_model': 'l10n.hu.object',
            'target': 'current',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
        }

        # Return result
        return result

    def action_view_source_record(self):
        # Ensure one
        self.ensure_one()

        if self.source_model_name and self.source_record_id:
            # Assemble result
            result = {
                'res_id': self.source_record_id,
                'res_model': self.source_model_name,
                'target': 'current',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
            }

            # Return result
            return result
        else:
            raise exceptions.UserError(_("Source record model name or source record id is empty!"))

    # Business methods
    @api.model
    def api_request_response(self, values):
        """ Make a request to API and process the response

        NOTE:
        - simple python request implementation to manage API

        :param values: dictionary

        :return: dictionary
        """
        # raise exceptions.UserError("api_request_response BEGIN" + str(values))

        # Initialize variables
        debug_list = []
        error_list = []
        info_list = []
        processing_result = {}
        response_json = {}
        result = {}
        warning_list = []

        # api_key
        if values.get('api_key'):
            api_key = values['api_key']
            debug_list.append("api_key found in values")
        else:
            api_key = None
            error_list.append("api_key not found in values")
        # raise exceptions.UserError("api_request_response api_key" + str(api_key))

        # log
        if values.get('log'):
            log = values['log']
            debug_list.append("log set from values")
        elif len(self) == 1 and self.id:
            log = self
            debug_list.append("log set from self")
        else:
            log = None
            error_list.append("log not set")

        # request_data
        if values.get('request_data'):
            # request_data = {'params': values['request_data']}
            request_data = json.dumps(values['request_data'], default=str)
        else:
            request_data = False
            error_list.append("request_data not found in values")

        # request_method
        if values.get('request_method'):
            request_method = values['request_method']
            debug_list.append("request_method found in values: " + str(request_method))
        else:
            request_method = False
            error_list.append("request_method not found in values")

        # request_type
        if values.get('request_type'):
            request_type = values['request_type']
        else:
            request_type = False
            error_list.append("request_type not found in values")

        # request_url
        if values.get('request_url'):
            request_url = values['request_url']
            debug_list.append("request_url found in values: " + str(request_url))
        else:
            request_url = False
            error_list.append("request_url not found in values")

        # Request-Response
        # request_headers
        request_headers = {
                "accept": "application/json",
                "Content-Type": "application/json",
                "X-Api-Key": api_key,
        }

        # debug_exception
        debug_exception = "\n" + str(request_url)
        debug_exception += "\n" + str(request_headers)
        debug_exception += "\n" + str(request_data)
        debug_exception += "\n" + str(request_method)
        debug_exception += "\n" + str(request_type)
        # raise exceptions.UserError("api_request_response debug_exception" + debug_exception)

        # Make request and process response
        if len(error_list) == 0:
            # Make request
            if request_method == 'DELETE':
                response = requests.delete(request_url, headers=request_headers, data=request_data)
            elif request_method == 'GET':
                response = requests.get(request_url, headers=request_headers, data=request_data)
            elif request_method == 'POST':
                response = requests.post(request_url, headers=request_headers, data=request_data)
            else:
                response = None
            # raise exceptions.UserError(str(response.json()))
            # raise exceptions.UserError(str(response.text))
            try:
                response_json = response.json()
            except:
                warning_list.append("response not json")

            if response_json.get('result') and response_json['result'].get('payload'):
                payload = response_json['result']['payload']
            else:
                payload = {}

            # Process response
            # response_status_code
            if response and response.status_code in [200, 201, 204]:
                response_status_code_type = 'success'
                if request_type in ['delete_registration', 'get_registration', 'post_registration']:
                    response_values = {
                        'log': log,
                        'payload': payload,
                        'request_type': request_type,
                    }
                    processing_result = log.company.l10n_hu_api_registration_response(response_values)
            elif response and response.status_code in [400, 401, 402, 403, 404, 422]:
                response_status_code_type = 'error'
            elif response and response.status_code in [500]:
                response_status_code_type = 'server_error'
            else:
                response_status_code_type = 'unknown'
        else:
            # Processing result
            processing_result = {
                'response_success': False,
                'response_type': 'error',
                'status': 'error',
            }
            debug_list.append("request sending skipped due to previous errors")

        # technical_data
        technical_data = {
            'processing_result': processing_result,
            'request_info': {
                'request_data': request_data,
                'request_headers': request_headers,
                'request_path': request_url,
            },
            'response_info': {
                'response_json': response_json,
                'response_success': processing_result.get('response_success', False),
                'response_type': processing_result.get('response_type', False),
            },
        }
        log.sudo().write({
            'technical_data': json.dumps(technical_data, default=str),
        })

        # Update result
        result.update({
            'debug_list': debug_list,
            'error_list': error_list,
            'info_list': info_list,
            'log': log,
            'processing_result': processing_result,
            'warning_list': warning_list,
        })

        # Return result
        # raise exceptions.UserError("api_request_response END" + str(result))
        return result
