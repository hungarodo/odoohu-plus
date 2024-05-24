# -*- coding: utf-8 -*-
# 1 : imports of python lib
import datetime
import json
import random
import string
import uuid

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models, tools  # alphabetically ordered

# 3 : imports from odoo modules
from odoo.tools.translate import html_translate

# 4 : variable declarations


# Class
class L10nHuBaseObject(models.Model):
    # Private attributes
    _name = 'l10n.hu.object'
    _description = "Hungary Object"
    _inherit = ['image.mixin', 'mail.activity.mixin', 'mail.thread']
    _order = 'name asc, id desc'

    # Default methods

    # Field declarations
    active = fields.Boolean(
        default=True,
        string="Active",
    )
    api_enabled = fields.Boolean(
        default=False,
        string="API Enabled",
    )
    api_data = fields.Text(
        copy=False,
        readonly=True,
        string="API Data",
    )
    api_timestamp = fields.Datetime(
        copy=False,
        readonly=True,
        string="API Timestamp",
    )
    category_tag = fields.Many2one(
        comodel_name='l10n.hu.tag',
        domain=[('tag_type', '=', 'object_category')],
        index=True,
        string="Category",
    )
    category_technical_name = fields.Char(
        related='category_tag.technical_name',
        string="Category Technical Name",
    )
    code = fields.Char(
        copy=False,
        string="Code",
    )
    collection_tag = fields.Many2one(
        comodel_name='l10n.hu.tag',
        domain=[('tag_type', '=', 'object_collection')],
        index=True,
        store=True,
        string="Collection",
    )
    collection_technical_name = fields.Char(
        related='collection_tag.technical_name',
        string="Collection Technical Name",
    )
    color = fields.Integer(
        string="Color",
    )
    company = fields.Many2one(
        comodel_name='res.company',
        default=lambda self: self.env.company.id,
        index=True,
        readonly=True,
        string="Company",
    )
    description = fields.Text(
        copy=False,
        string="Description",
    )
    external_id = fields.Char(
        copy=False,
        string="External ID",
    )
    html_content = fields.Html(
        copy=False,
        index=True,
        sanitize_attributes=False,
        sanitize_form=False,
        string="HTML Content",
        translate=html_translate,
    )
    html_visible = fields.Boolean(
        default=False,
        string="HTML Visible",
    )
    key = fields.Char(
        copy=False,
        index=True,
        string="Key",
    )
    linked_model_name = fields.Char(
        copy=False,
        index=True,
        string="Linked Model Name",
    )
    linked_record_id = fields.Integer(
        copy=False,
        index=True,
        string="Linked Record ID",
    )
    linked_record_name = fields.Char(
        compute='_compute_linked_record_name',
        string="Linked Record Name",
    )
    locked = fields.Boolean(
        default=False,
        string="Locked",
    )
    name = fields.Char(
        copy=False,
        index=True,
        string="Name",
    )
    priority = fields.Integer(
        copy=False,
        index=True,
        string="Priority",
    )
    reference = fields.Char(
        copy=False,
        readonly=True,
        index=True,
        string="Reference",
    )
    status_tag = fields.Many2one(
        comodel_name='l10n.hu.tag',
        domain=[('tag_type', '=', 'object_status')],
        index=True,
        string="Object Status",
    )
    status_technical_name = fields.Char(
        related='status_tag.technical_name',
        string="Status Technical Name",
    )
    tag = fields.Many2many(
        comodel_name='l10n.hu.tag',
        column1='object',
        column2='tag',
        domain=[('tag_type', 'in', ['general', 'object', 'technical'])],
        index=True,
        relation='l10n_hu_object_tag_rel',
        string="Tag",
    )
    technical_data = fields.Text(
        copy=False,
        string="Technical Data",
    )
    technical_data_type = fields.Char(
        copy=False,
        string="Technical Data Type",
    )
    technical_name = fields.Char(
        copy=False,
        index=True,
        string="Technical Name",
    )
    type_tag = fields.Many2one(
        comodel_name='l10n.hu.tag',
        domain=[('tag_type', '=', 'object_type')],
        index=True,
        string="Object Type",
    )
    type_technical_name = fields.Char(
        related='type_tag.technical_name',
        index=True,
        store=True,
        string="Type Technical Name",
    )
    url = fields.Char(
        copy=False,
        index=True,
        size=1024,
        string="Url",
    )

    # Compute and search fields, in the same order of field declarations
    def _compute_linked_record_name(self):
        for record in self:
            if record.linked_model_name and record.linked_record_id:
                linked_record = self.env[record.linked_model_name].browse(record.linked_record_id).exists()
                if linked_record:
                    record.linked_record_name = linked_record.display_name
                else:
                    record.linked_record_name = None
            else:
                record.linked_record_name = None

    # Constraints and onchanges

    # CRUD methods (and name_get, name_search, ...) overrides
    def name_get(self):
        # Initialize result
        result = []

        # Iterate through self
        for record in self:
            # Set name
            if record.name:
                name = record.name
            else:
                name = record.id

            # Append to list
            result.append((record.id, name))

        # Return
        return result

    # Action methods
    def action_generate_key(self):
        # Ensure one record in self
        self.ensure_one()

        # Get
        if self.object_type \
                and self.object_type.key_regeneration \
                and self.object_type.key_automation == 'uuid4':
            self.key = self.get_uuid4()
        else:
            return

    def action_view_linked_record(self):
        # Ensure one
        self.ensure_one()

        # Check
        if not self.linked_model_name or not self.linked_record_id:
            raise exceptions.UserError(_("Linked model name and record ID are both required!"))

        model = self.env['ir.model'].search([
            ('model', '=', self.linked_model_name)
        ])

        # Result
        result = {
            'name': model.display_name,
            'res_id': self.linked_record_id,
            'res_model': self.linked_model_name,
            'target': 'current',
            'type': 'ir.actions.act_window',
            'view_mode': 'form,tree',
        }

        # Return result
        return result

    # Business methods
    # # API
    @api.model
    def api_object_request(self, values):
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

    # # CRON
    @api.model
    def run_object_api_cron(self):
        """ Meant to be called by scheduled cron

        Run cron for HU object to manage data:
        - get fresh definitions

        :return: nothing, but logs an info entry into l10n.hu.log
        """
        # Initialize variables
        company_ids = []
        company_results = []
        error_list = []
        object_results = []
        result = {}

        # Get companies
        companies = self.env['res.company'].sudo().search([])

        # Get config_parameters
        try:
            config_param_obj = self.env['ir.config_parameter'].sudo()
            config_parameters_string = config_param_obj.get_param('l10n_hu_base.settings')
            config_parameters = json.loads(config_parameters_string)
            debug_list.append("config parameters loaded")
        except:
            config_parameters = {}
            warning_list.append("config parameters exception")

        for company in companies:
            # 1) GET objects
            api_values = {
                'query_last_modified_date': query_last_modified_date,
                'query_page': query_page,
                'query_per_page': query_per_page,
                'request_type': 'get_objects',
            }
            api_result = self.env['l10n.hu.object'].api_request_response(api_values)
            if len(api_result.get('error_list', [])) == 0:
                pass

            # Update result
            company_result = {
                'company_id': company.id,
                'object_count': len(object_results),
                'object_results': object_results
            }

            # Append to list
            company_ids.append(company.id)
            company_results.append(company_result)

        # Update result
        result.update({
            'company_count': len(company_ids),
            'company_ids': company_ids,
            'company_results': company_results,
            'error_list': error_list,
        })

        # HU log
        log_values = {
            'app': "l10n_hu_base",
            'description': str(result),
            'level': "info",
            'name': "run_object_api_cron END",
            'user': self.env.user,
        }
        try:
            self.env['l10n.hu.log'].create(log_values)
        except:
            self.env['l10n.hu.log'].sudo().create(log_values)

        # Return
        return

    # # HELPER
    @api.model
    def generate_random_string(self, values=None):
        """ Generate a random string

        :param values: optional dictionary of parameters, including:
            - length: integer
            - letters: lowercase | uppercase | both | none
            - numbers: boolean
            - prefix: string
            - start_with_letter: boolean
            - suffix: string

        :return string
        """
        # Initialize variables
        result = ""

        # Set letters
        if values and values.get('letters'):
            letters = values['letters']
        elif self.object_type and self.object_type.random_name_letters:
            letters = self.object_type.random_name_letters
        else:
            letters = "both"

        # Set numbers
        if values and values.get('numbers') is not None and values.get('numbers'):
            numbers = True
        elif values and values.get('numbers') is not None and not values.get('numbers'):
            numbers = False
        elif self.object_type and self.object_type.random_name_numbers:
            numbers = True
        elif self.object_type and not self.object_type.random_name_numbers:
            numbers = False
        else:
            numbers = True

        # Set prefix
        if values and values.get('prefix'):
            result += values['prefix']
        elif self.object_type and self.object_type.random_name_prefix:
            result += self.object_type.random_name_prefix
        else:
            pass

        # Set length
        if values and values.get('length'):
            length = values['length']
        elif self.object_type and self.object_type.random_name_length:
            length = self.object_type.random_name_length
        else:
            length = 8

        # Start with letter
        if values and values.get('start_with_letter'):
            if letters == 'both' and numbers:
                result += random.choice(string.ascii_uppercase + string.ascii_lowercase)
            elif letters == 'lowercase' and numbers:
                result += random.choice(string.ascii_lowercase)
            elif letters == 'uppercase' and numbers:
                result += random.choice(string.ascii_uppercase)
            else:
                result += random.choice(string.ascii_uppercase + string.ascii_lowercase)
            length = length - 1
        elif self.object_type and self.object_type.random_name_start_with_letter:
            if letters == 'both' and numbers:
                result += random.choice(string.ascii_uppercase + string.ascii_lowercase)
            elif letters == 'lowercase' and numbers:
                result += random.choice(string.ascii_lowercase)
            elif letters == 'uppercase' and numbers:
                result += random.choice(string.ascii_uppercase)
            else:
                result += random.choice(string.ascii_uppercase + string.ascii_lowercase)
            length = length - 1
        else:
            pass

        # Iterate for random characters
        for i in range(length):
            if letters == 'both' and numbers:
                result += random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase)
            elif letters == 'lowercase' and numbers:
                result += random.choice(string.digits + string.ascii_lowercase)
            elif letters == 'uppercase' and numbers:
                result += random.choice(string.digits + string.ascii_lowercase)
            elif letters == 'none' and numbers:
                result += random.choice(string.digits + string.ascii_lowercase)
            else:
                result += random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase)

        # Set suffix
        if values and values.get('suffix'):
            result += values['suffix']
        elif self.object_type and self.object_type.random_name_suffix:
            result += self.object_type.random_name_suffix
        else:
            pass

        # Return
        return result

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

    @api.model
    def get_tags_by_technical_name(self):
        """ Get tags by technical name

        NOTE:
        - helper method to get available tag ids and objects organized by technical name

        :return dictionary
        """
        # raise exceptions.UserError("get_tags_by_technical_name BEGIN")

        # Initialize variables
        result = {}

        # Collect tags and update result
        tags = self.env['l10n.hu.tag'].sudo().search([
            ('active', 'in', [True, False]),
        ])
        for tag in tags:
            if tag.technical_name:
                record_key = tag.technical_name + "_tag"
                record_id_key = tag.technical_name + "_tag_id"
                result[record_key] = tag
                result[record_id_key] = tag.id

        # Return result
        return result

    @api.model
    def get_uuid4(self):
        """ Get uuid4

        :return string
        """
        # Generate uuid4
        result = uuid.uuid4()

        # Return
        return result
