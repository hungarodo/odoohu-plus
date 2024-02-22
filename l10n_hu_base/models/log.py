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
    # # API
    @api.model
    def api_object_request_response(self, values):
        """ Make a request to API and process the response

        NOTE:
        - simple python request implementation to manage API
        - currency we only support GET

        :param values: dictionary

        :return: dictionary
        """
        # raise exceptions.UserError("object_api_request_response BEGIN" + str(values))

        # Initialize variables
        debug_list = []
        error_list = []
        info_list = []
        request_type = ""
        result = {}
        warning_list = []

        # request_data
        if values.get('request_data') and application:
            request_data = values['request_data']
            # debug_list.append("request_data: " + str(request_data))
            # raise exceptions.UserError("get_registration request_data" + str(request_data))
            request_data.update({
                'environment': application.environment_type,
                'operation': request_type,
            })
        else:
            request_data = {}
            error_list.append("request_data not found in values")

        # request_url
        if values.get('request_url'):
            request_url = values['request_url']
            debug_list.append("request_url found in values: " + str(request_url))
        else:
            request_url = False
            error_list.append("request_url not found in values")

        # Create log
        log_values = {
            'application': application_id,
            'direction': 'outgoing',
            'request_method': 'GET',
            'request_type': request_type,
        }
        log = self.env['l10n.hu.log'].sudo().create(log_values)

        # Request-Response
        # request_headers
        request_headers = {
                "accept": "application/json",
                "Content-Type": "application/json",
                "X-Api-Key": api_data['api_key'],
        }

        # request_method
        if message and message.request_method in ['GET', 'POST', 'PUT', 'DELETE']:
            request_method = message.request_method
        else:
            request_method = False
            error_list.append("invalid request_method")

        # request_url
        if values.get('request_url'):
            request_url = values['request_url']
        else:
            request_url = False
            error_list.append("request_url not found in values")

        # request_type
        if values.get('request_type'):
            request_type = values['request_type']
        else:
            request_type = False
            error_list.append("request_type not found in values")

        # request_data
        if values.get('request_data'):
            # request_data = {'params': values['request_data']}
            request_data = json.dumps(values['request_data'], default=str)
        else:
            request_data = False
            error_list.append("request_type not found in values")

        # debug_exception
        debug_exception = "\n" + str(request_url)
        debug_exception += "\n" + str(request_headers)
        debug_exception += "\n" + str(request_data)
        # raise exceptions.UserError("debug_exception" + debug_exception)

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
                pass
            # raise exceptions.UserError(str(response.text))

            # Process response
            # response_status_code
            if response_details.get('response_status_code') in [200, 201, 204]:
                response_status_code_type = 'success'
            elif response_details.get('response_status_code') in [400, 401, 402, 403, 404, 422]:
                response_status_code_type = 'error'
            elif response_details.get('response_status_code') in [500]:
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

        write_info = {
            'message': message,
            'processing_parameters': processing_parameters,
            'processing_result': processing_result,
            'request_info': {
                'request_data': request_data,
                'request_headers': request_headers,
                'request_path': request_url,
            },
            'response_info': {
                'response_json': response_result.get('payload', {}),
                'response_success': processing_result.get('response_success', False),
                'response_type': processing_result.get('response_type', False),
            },
        }

        # Update result
        result.update({
            'debug_list': debug_list,
            'error_list': error_list,
            'info_list': info_list,
            'message': message,
            'processing_result': processing_result,
            'warning_list': warning_list,
        })

        # raise exceptions.UserError("application_get_registration_request END" + str(result))

        # Return result
        return result

    @api.model
    def api_object_response(self, values):
        """ Process application_get_registration response

        :param values: dictionary

        :return: dictionary
        """
        # Oregional log
        self._oregional_log({
            'app': "oregional_api_base",
            'description': str(values),
            'level': "debug",
            'name': "application_get_registration_response BEGIN",
        })
        # raise exceptions.UserError("application_get_registration_response BEGIN" + str(values))

        # Initialize variables
        debug_list = []
        error_list = []
        info_list = []
        processing_log = ""
        processing_result = {}
        result = {}
        warning_list = []

        # Get message
        if values.get('message'):
            message = values['message']
        else:
            message = False

        # Get response_json
        if values.get('response_json'):
            response_json = values['response_json']
        else:
            response_json = {}

        # Process
        if message \
                and message.application \
                and message.request_method == 'GET' \
                and message.request_type == 'application_get_registration' \
                and response_json.get('result'):
            response_json_result = response_json.get('result')
            response_payload = response_json_result.get('payload')

            # Response details processing
            processing_values = {
                'api_message': message,
                'api_payload': response_payload,
            }
            response_processing_result = message.application.api_get_registration_response(processing_values)
            # raise exceptions.UserError("response_processing_result" + str(response_processing_result))
            error_list += response_processing_result['error_list']

            if len(error_list) == 0:
                processing_result.update({
                    'registration_data': response_processing_result.get('registration_data', {}),
                    'result_messages': response_processing_result.get('result_messages', []),
                    'response_success': True,
                    'response_type': 'application_get_registration',
                    'status': 'done',
                })
        else:
            processing_result.update({
                'response_success': False,
                'response_type': 'application_get_registration_error',
                'status': 'error',
            })

        # Update result
        result.update({
            'debug_list': debug_list,
            'error_list': error_list,
            'info_list': info_list,
            'message': message,
            'processing_log': processing_log,
            'processing_result': processing_result,
            'warning_list': warning_list,
        })

        # Oregional log
        self._oregional_log({
            'app': "oregional_api_base",
            'description': str(result),
            'level': "debug",
            'name': "application_get_registration_response END",
        })
        # raise exceptions.UserError('application_get_registration_response END' + str(result))

        # Return result
        return result

    # # HELPER
    @api.model
    def get_request_response_details(self, response):
        """ Get details of a http response

        :param response: a response (python requests.Response object)

        :return: dictionary
        """
        # raise exceptions.UserError(str(result))

        # Initialize variables
        result = {}

        # Now try and set details
        try:
            result.update({
                'response_content': response.content,
            })
        except:
            result.update({
                'response_content': False,
            })

        try:
            result.update({
                'response_headers': response.headers,
            })
        except:
            result.update({
                'response_headers': False,
            })

        try:
            result.update({
                'response_json': response.json(),
            })
        except:
            result.update({
                'response_json': False,
            })

        try:
            result.update({
                'response_ok': response.ok,
            })
        except:
            result.update({
                'response_ok': False,
            })

        try:
            result.update({
                'response_reason': response.reason,
            })
        except:
            result.update({
                'response_reason': False,
            })

        try:
            result.update({
                'response_status_code': response.status_code,
            })
        except:
            result.update({
                'response_status_code': False,
            })

        try:
            result.update({
                'response_text': response.text,
            })
        except:
            result.update({
                'response_text': False,
            })


        # Return result
        # raise exceptions.UserError(str(result))
        return result
