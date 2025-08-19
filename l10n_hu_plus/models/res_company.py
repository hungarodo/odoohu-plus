# -*- coding: utf-8 -*-
# 1 : imports of python lib
import json

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 : imports from odoo modules
from odoo.service import common as odoo_service_common

# 4 : variable declarations


# Class
class L10nHuBaseResCompany(models.Model):
    # Private attributes
    _inherit = 'res.company'

    # Default methods

    # Field declarations
    ## API
    l10n_hu_plus_api_enabled = fields.Boolean(
        copy=False,
        default=False,
        string="HU+ API Enabled",
    )
    l10n_hu_plus_api_license_valid = fields.Boolean(
        copy=False,
        readonly=True,
        string="HU+ API License Valid",
    )
    l10n_hu_plus_api_registered = fields.Boolean(
        copy=False,
        readonly=True,
        string="HU+ API Registered",
    )
    l10n_hu_plus_api_timestamp = fields.Datetime(
        copy=False,
        default=fields.Datetime.now(),
        readonly=True,
        string="HU+ API Timestamp",
    )
    ## TECHNICAL
    l10n_hu_plus_technical_data = fields.Json(
        copy=False,
        default=False,
        readonly=True,
        string="HU+ Technical Data",
    )

    # Compute and search fields, in the same order of fields declaration

    # Constraints and onchanges

    # CRUD methods (and name_get, name_search, ...) overrides

    # Action methods
    def action_l10n_hu_plus_api_check_registration(self):
        """ Open the wizard for check API registration """
        # Ensure one
        self.ensure_one()

        # Checks
        if not self.l10n_hu_plus_api_enabled:
            raise exceptions.UserError(_("API is not enabled!"))
        if not self.l10n_hu_plus_technical_data:
            raise exceptions.UserError(_("Technical data not available!"))
        try:
            api_data = self.l10n_hu_plus_technical_data.get("hu_plus_api")
        except:
            raise exceptions.UserError(_("API data not available!"))

        # API details
        api_details = _("Registered") + ": " + str(api_data.get('registered'))
        api_details += "\n" + _("License Type") + ": " + str(api_data.get('license_type'))
        api_details += "\n" + _("License Owner") + ": " + str(api_data.get('license_owner'))
        api_details += "\n" + _("License Status") + ": " + str(api_data.get('license_status'))
        api_details += "\n" + _("License Valid") + ": " + str(api_data.get('license_valid'))
        api_details += "\n" + _("Valid To") + ": " + str(api_data.get('license_valid_to'))

        # Assemble context
        context = {
            'default_action_type': 'api',
            'default_api_action': 'check_registration',
            'default_api_action_editable': False,
            'default_api_details': api_details,
            'default_api_key': api_data.get('api_key', "free"),
            'default_api_license_code': api_data.get('license_code', "free"),
            'default_api_url': api_data.get('api_url', None),
        }

        # Assemble result
        result = {
            'name': _("HU+ Wizard"),
            'context': context,
            'res_model': 'l10n.hu.plus.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
        }

        # Return result
        return result

    def action_l10n_hu_plus_api_create_registration(self):
        """ Open the wizard for create API registration """
        # Ensure one
        self.ensure_one()

        # Checks
        if not self.l10n_hu_plus_api_enabled:
            raise exceptions.UserError(_("API is not enabled!"))

        # Data
        try:
            api_data = self.l10n_hu_plus_technical_data.get("hu_plus_api")
        except:
            api_data = {}

        if api_data:
            api_key = api_data.get('api_key', "free")
            api_url = api_data.get('api_url', None)
            license_code = api_data.get('license_code', "free")
        else:
            api_key = "free"
            api_url = "https://odoohu17e.hungarodo.hu/v1/l10n_hu_api/registration"
            license_code = "free"

        # Assemble context
        context = {
            'default_action_type': 'api',
            'default_api_action': 'create_registration',
            'default_api_action_editable': False,
            'default_api_key': api_key,
            'default_api_license_code': license_code,
            'default_api_url': api_url,
        }

        # Assemble result
        result = {
            'name': _("HU+ Wizard"),
            'context': context,
            'res_model': 'l10n.hu.plus.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
        }

        # Return result
        return result

    def action_l10n_hu_plus_api_delete_registration(self):
        """ Open the wizard for delete API registration """
        # Ensure one
        self.ensure_one()

        # Checks
        if not self.l10n_hu_plus_api_enabled:
            raise exceptions.UserError(_("API is not enabled!"))
        try:
            api_data = self.l10n_hu_plus_technical_data.get("hu_plus_api")
        except:
            raise exceptions.UserError(_("API data not available!"))

        # API details
        api_details = _("Registered") + ": " + str(api_data.get('registered'))
        api_details += "\n" + _("License Type") + ": " + str(api_data.get('license_type'))
        api_details += "\n" + _("License Owner") + ": " + str(api_data.get('license_owner'))
        api_details += "\n" + _("License Status") + ": " + str(api_data.get('license_status'))
        api_details += "\n" + _("License Valid") + ": " + str(api_data.get('license_valid'))
        api_details += "\n" + _("Valid To") + ": " + str(api_data.get('license_valid_to'))

        # Assemble context
        context = {
            'default_action_type': 'api',
            'default_api_action': 'delete_registration',
            'default_api_action_editable': False,
            'default_api_details': api_details,
            'default_api_key': api_data.get('api_key', "free"),
            'default_api_license_code': api_data.get('license_code', "free"),
            'default_api_url': api_data.get('api_url', "free"),
        }

        # Assemble result
        result = {
            'name': _("HU Wizard"),
            'context': context,
            'res_model': 'l10n.hu.plus.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
        }

        # Return result
        return result

    def action_l10n_hu_plus_api_get_objects(self):
        """ Open the wizard for GET API objects """
        # Ensure one
        self.ensure_one()

        # Check
        if not self.l10n_hu_plus_api_enabled:
            raise exceptions.UserError(_("HU+ API is not enabled!"))

        # Assemble context
        context = {
            'default_action_type': 'api',
            'default_api_action': 'get_objects',
            'default_api_action_editable': False,
        }

        # Assemble result
        result = {
            'name': _("HU Wizard"),
            'context': context,
            'res_model': 'l10n.hu.plus.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
        }

        # Return result
        return result

    def action_l10n_hu_plus_api_list_logs(self):
        """ List logs """
        # Ensure one
        self.ensure_one()

        # Set l10n_hu_log_ids
        l10n_hu_log_ids = []
        logs = self.env['l10n.hu.plus.log'].sudo().search([('company', '=', self.id)])
        for log in logs:
            l10n_hu_log_ids.append(log.id)

        # Assemble result
        result = {
            'name': _("HU+ Logs"),
            'domain': [('id', 'in', l10n_hu_log_ids)],
            'res_model': 'l10n.hu.plus.log',
            'target': 'current',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
        }

        # Return result
        return result

    def action_l10n_hu_plus_api_reset_registration(self):
        """ Reset registration to default """
        # Ensure one
        self.ensure_one()

        # api_url
        try:
            api_data = self.l10n_hu_plus_technical_data.get("hu_plus_api")
            api_url = api_data.get('api_url', None)
        except:
            api_url = None

        # Reset
        api_data = {
            'api_key': 'free',
            'api_url': api_url,
            'license_code': 'free',
        }
        try:
            technical_data = json.loads(self.l10n_hu_plus_technical_data)
        except:
            technical_data = {}
        technical_data.update({'hu_plus_api': api_data})
        company_values = {
            'l10n_hu_plus_technical_data': json.dumps(technical_data, default=str),
            'l10n_hu_plus_api_license_valid': False,
            'l10n_hu_plus_api_registered': False,
        }
        self.write(company_values)

        # Return
        return

    def action_l10n_hu_plus_apply_configuration(self):
        self.ensure_one()
        context = {
            'default_action_type': 'configuration',
            'default_action_type_visible': True,
        }
        result = {
            'name': _("HU+ Wizard"),
            'context': context,
            'res_model': 'l10n.hu.plus.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
        }
        return result

    def action_l10n_hu_plus_view_documentation(self):
        """ View HU+ documentation """
        # Make sure there is one record in self
        self.ensure_one()

        # Get config_parameters
        try:
            config_param_obj = self.env['ir.config_parameter'].sudo()
            config_parameters_string = config_param_obj.get_param('l10n_hu_plus.settings')
            config_parameters = json.loads(config_parameters_string)
        except:
            config_parameters = {}

        if config_parameters.get('documentation_url'):
            return {
                'target': 'new',
                'type': 'ir.actions.act_url',
                'url': config_parameters['documentation_url'],
            }
        else:
            raise exceptions.UserError(_("Documentation URL is not configured!"))

    def action_l10n_hu_plus_view_technical_data(self):
        # Ensure one record in self
        self.ensure_one()

        # Return
        if self.l10n_hu_plus_technical_data:
            data_display = json.dumps(self.l10n_hu_plus_technical_data, default=str, indent=4)
            context = {
                'default_action_type': 'technical',
                'default_action_execute_visible': False,
                'default_technical_action': 'view_data',
                'default_technical_data_display': data_display,
            }
            result = {
                'name': _("HU+ Wizard"),
                'context': context,
                'res_model': 'l10n.hu.plus.wizard',
                'target': 'new',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
            }
            return result
        else:
            raise exceptions.UserError(_("Technical data is empty!"))

    # Business methods
    ## API
    @api.model
    def l10n_hu_plus_api_registration_request(self, values):
        """ Registration request to HU+ API

        NOTES:
        - we send one message here, manage iterations on the caller side

        :return: dictionary
        """
        # raise exceptions.UserError("l10n_hu_plus_api_registration_request BEGIN" + str(values))

        # Initialize variables
        debug_list = []
        error_list = []
        info_list = []
        result = {}
        warning_list = []

        # company
        if values.get('company'):
            company = values['company']
            debug_list.append("company set from values")
        elif len(self) == 1 and self.id:
            company = self
            debug_list.append("company set from self")
        else:
            company = self.env.company
            debug_list.append("company set from self env")

        # request_type
        if values.get('request_type'):
            request_type = values['request_type']
            debug_list.append("request_type found in values: " + str(request_type))
        else:
            request_type = False
            error_list.append("request_type not found in values")

        # api_data, api_environment
        try:
            technical_data = json.loads(company.l10n_hu_plus_technical_data)
            api_data = technical_data.get('hu_plus_api')
        except:
            api_data = {}
        api_environment_result = company.l10n_hu_plus_get_api_environment()

        # payload
        if len(error_list) == 0:
            payload = {'license_code': api_data.get('license_code')}
            payload.update(api_environment_result.get('api_environment', {}))
        else:
            payload = {}
            debug_list.append("payload skipped due to previous errors")

        # request_data
        request_data = {'payload': payload}

        # request_method
        request_method = None
        if len(error_list) == 0:
            if request_type == 'delete_registration':
                request_method = 'DELETE'
            elif request_type == 'get_registration':
                request_method = 'GET'
            elif request_type == 'post_registration':
                request_method = 'POST'
            else:
                error_list.append("invalid request_type for request_method")
        else:
            debug_list.append("request_method skipped due to previous errors")

        # name
        name = "l10n_hu_plus_api_registration" + " " + str(request_type)

        # Create l10n_hu_log
        ## NOTES: we want to log everything, even failed attempts
        log_values = {
            'app_name': 'l10n_hu_plus',
            'company': company.id,
            'direction': 'outgoing',
            'level': 'info',
            'log_type': request_type,
            'name': name,
            'model_name': 'res.company',
            'technical_data': request_data,
            'technical_name': 'l10n_hu_plus.l10n_hu_plus_api_registration_request',
        }
        log_record = self.env['l10n.hu.plus.log'].create(log_values)

        # Send API message
        if len(error_list) == 0:
            # API values
            api_values = {
                'api_key': api_data.get('api_key'),
                'request_data': request_data,
                'request_method': request_method,
                'request_type': request_type,
                'request_url': api_data.get('api_url'),
            }
            api_result = log_record.api_request_response(api_values)
            # raise exceptions.UserError("api_result" + str(api_result))
            error_list += api_result['error_list']
        else:
            api_result = {}
            debug_list.append("api_result skipped due to previous errors")

        # Log description
        description_json = {
            'error_list': error_list,
            'info_list': info_list,
            'warning_list': warning_list,
        }
        log_record.write({'description': json.dumps(description_json, default=str)})

        # Update result
        result.update({
            'api_data': api_data,
            'api_result': api_result,
            'debug_list': debug_list,
            'error_list': error_list,
            'info_list': info_list,
            'log_record': log_record,
            'warning_list': warning_list,
        })

        # Return result
        # raise exceptions.UserError("l10n_hu_plus_api_registration_request END" + str(result))
        return result

    @api.model
    def l10n_hu_plus_api_registration_response(self, values):
        """ Process response for registration request

        NOTES:
        - common method for DELETE, GET, POST operations

        :return: dictionary
        """
        # raise exceptions.UserError("l10n_hu_plus_api_registration_response BEGIN" + str(values))

        # Initialize variables
        company_values = {}
        debug_list = []
        error_list = []
        info_list = []
        result = {}
        warning_list = []

        # log
        if values.get('log') is not None:
            log = values['log']
            debug_list.append("log id: " + str(log.id))
        else:
            log = None
            error_list.append('could not set log')

        # payload
        if values.get('payload'):
            payload = values['payload']
            debug_list.append('payload found in values')
        else:
            payload = {}
            error_list.append('payload not found in values')

        # result_messages
        if payload.get('result_messages') is not None:
            result_messages = payload['result_messages']
        else:
            result_messages = []
            error_list.append("result_messages not found in payload")

        # registration_data
        if payload.get('registration_data') is not None:
            registration_data = payload['registration_data']
        else:
            registration_data = {}
            error_list.append("registration_data not found in payload")

        # request_type
        if values.get('request_type'):
            request_type = values['request_type']
            debug_list.append("request_type found in values: " + str(request_type))
        elif log and log.request_type:
            request_type = log.request_type
            debug_list.append("request_type set from log: " + str(request_type))
        else:
            request_type = None
            error_list.append("request_type not set")

        # Update log technical_data
        try:
            log_technical_data = log.technical_data
            log_technical_data.update({'response_payload': payload})
            log.sudo().write({'technical_data': log_technical_data})
            debug_list.append("log technical_data update success")
        except:
            error_list.append("log technical_data update exception")

        # Process
        if len(error_list) == 0:
            if request_type in ['get_registration', 'post_registration']:
                try:
                    technical_data = json.loads(log.company.l10n_hu_plus_technical_data)
                except:
                    technical_data = {}
                technical_data.update({'hu_plus_api': registration_data})
                if registration_data.get('api_key'):
                    l10n_hu_plus_api_registered = True
                else:
                    l10n_hu_plus_api_registered = False
                company_values.update({
                    'l10n_hu_plus_api_license_valid': registration_data.get('license_valid', False),
                    'l10n_hu_plus_api_registered': l10n_hu_plus_api_registered,
                    'l10n_hu_plus_technical_data': json.dumps(technical_data, default=str),
                })
                debug_list.append("l10n_hu_plus api_data set to registration_data")
            elif request_type == 'delete_registration':
                try:
                    technical_data = json.loads(log.company.l10n_hu_plus_technical_data)
                    current_api_data = technical_data.get('hu_plus_api')
                except:
                    technical_data = {}
                    current_api_data = {}
                api_data = {
                    'api_key': 'free',
                    'api_url': current_api_data.get('api_url'),
                    'license_code': 'free',
                }
                technical_data.update({'hu_plus_api': api_data})
                company_values.update({
                    'l10n_hu_plus_api_license_valid': False,
                    'l10n_hu_plus_api_registered': False,
                    'l10n_hu_plus_technical_data': json.dumps(technical_data, default=str),
                })
                debug_list.append("l10n_hu_plus api_data set to empty dict")
            else:
                error_list.append("invalid request_type for company_values")
        else:
            error_list.append("company_values skipped due to previous errors")

        # crud
        if len(error_list) == 0:
            log.company.sudo().write(company_values)
            result.update({'result_type': 'success'})
            debug_list.append("company updated")
        else:
            error_list.append("crud skipped due to previous errors")

        # Update result
        result.update({
            'debug_list': debug_list,
            'error_list': error_list,
            'info_list': info_list,
            'result_messages': result_messages,
            'registration_data': registration_data,
            'warning_list': warning_list,
        })

        # Return result
        # raise exceptions.UserError("l10n_hu_plus_api_registration_response END" + str(result))
        return result

    @api.model
    def l10n_hu_plus_apply_configuration(self, values):
        """ Apply HU+ configuration
        @:return: dictionary
        """
        # raise exceptions.UserError("l10n_hu_plus_apply_configuration BEGIN")

        # Initialize variables
        debug_list = []
        error_list = []
        info_list = []
        operations = []
        result = {}
        success_list = []
        warning_list = []

        # company
        if values.get('company'):
            company = values['company']
            company_id = company.id
            info_list.append(_("Company") + ": " + str(company.display_name))
        elif len(self) == 1 and self.id:
            company = self
            company_id = company.id
            info_list.append(_("Company") + ": " + str(company.display_name))
        else:
            company = None
            company_id = None
            error_list.append("could not set company")

        if len(error_list) == 0:
            # 1) DOCUMENT TYPES
            if values.get('document_types'):
                documents_types = []
                ## NORMAL INVOICE
                invoice_normal = self.env['l10n.hu.plus.tag'].search([
                    ('company', '=', company_id),
                    ('tag_type', '=', 'document_type'),
                    ('technical_name', '=', 'invoice_normal'),
                ])
                if not invoice_normal:
                    invoice_normal_values = {
                        'code': "INVOICE-NORMAL",
                        'company': company.id,
                        'locked': True,
                        'name': "invoice_normal",
                        'priority': 1,
                        'tag_type': 'document_type',
                        'technical_name': 'invoice_normal',
                    }
                    invoice_normal = self.env['l10n.hu.plus.tag'].sudo().create(invoice_normal_values)
                    invoice_normal.with_context(lang="en_US").name = "Invoice"
                    invoice_normal.with_context(lang="hu_HU").name = "Számla"
                    operations.append({
                        'model_name': 'l10n.hu.plus.tag',
                        'record_id': invoice_normal.id,
                        'operation': 'create'
                    })
                documents_types.append(invoice_normal)
                ## INVOICE STORNO
                invoice_storno = self.env['l10n.hu.plus.tag'].search([
                    ('company', '=', company_id),
                    ('tag_type', '=', 'document_type'),
                    ('technical_name', '=', 'invoice_storno'),
                ])
                if not invoice_storno:
                    invoice_storno_values = {
                        'code': "INVOICE-STORNO",
                        'company': company.id,
                        'locked': True,
                        'name': "invoice_storno",
                        'priority': 4,
                        'tag_type': 'document_type',
                        'technical_name': 'invoice_storno',
                    }
                    invoice_storno = self.env['l10n.hu.plus.tag'].sudo().create(invoice_storno_values)
                    invoice_storno.with_context(lang="en_US").name = "Storno Invoice"
                    invoice_storno.with_context(lang="hu_HU").name = "Storno számla"
                    operations.append({'model_name': 'l10n.hu.plus.tag', 'record_id': invoice_storno.id, 'operation': 'create'})
                documents_types.append(invoice_normal)
                ## MODIFICATION INVOICE
                invoice_modification = self.env['l10n.hu.plus.tag'].search([
                    ('company', '=', company_id),
                    ('tag_type', '=', 'document_type'),
                    ('technical_name', '=', 'invoice_modification'),
                ])
                if not invoice_modification:
                    invoice_modification_values = {
                        'code': "INVOICE-MODIFICATION",
                        'company': company.id,
                        'locked': True,
                        'name': "invoice_modification",
                        'priority': 3,
                        'tag_type': 'document_type',
                        'technical_name': 'invoice_modification',
                    }
                    invoice_modification = self.env['l10n.hu.plus.tag'].sudo().create(invoice_modification_values)
                    invoice_modification.with_context(lang="en_US").name = "Modification Invoice"
                    invoice_modification.with_context(lang="hu_HU").name = "Módosító számla"
                    operations.append({'model_name': 'l10n.hu.plus.tag', 'record_id': invoice_modification.id, 'operation': 'create'})
                documents_types.append(invoice_normal)
                success_list.append(_("Document types configured"))
            else:
                info_list.append(_("Document type configuration skipped"))
        else:
            debug_list.append("operations skipped due to previous errors")

        # Create log
        log_description = {
            'error_list': error_list,
            'operations': operations,
            'success_list': success_list,
            'warning_list': warning_list,
        }
        log_technical_data = {
            'debug_list': debug_list,
            'error_list': error_list,
            'info_list': info_list,
            'operations': operations,
            'success_list': success_list,
            'warning_list': warning_list,
        }
        log_values = {
            'app_name': 'l10n_hu_plus',
            'company': company.id,
            'description': str(log_description),
            'direction': 'internal',
            'level': 'info',
            'log_type': 'hu_plus_configuration',
            'name': " HU+ configuration company_id: " + str(company_id),
            'source_model_name': 'res.company',
            'source_record_id': company_id,
            'technical_data': json.loads(json.dumps(log_technical_data, default=str)),
            'technical_name': 'l10n_hu_plus.l10n_hu_plus_run_configuration',
        }
        log_record = self.env['l10n.hu.plus.log'].create(log_values)

        # Update result
        result.update({
            'debug_list': debug_list,
            'error_list': error_list,
            'info_list': info_list,
            'log_record': log_record,
            'operations': operations,
            'success_list': success_list,
            'warning_list': warning_list,
        })

        # Return result
        # raise exceptions.UserError("l10n_hu_plus_run_configuration END")
        return result

    @api.model
    def l10n_hu_plus_get_api_environment(self):
        """ Get API environment
        @:return: dictionary
        """
        # raise exceptions.UserError("l10n_hu_plus_get_api_environment BEGIN")

        # Initialize variables
        api_environment = {}
        debug_list = []
        error_list = []
        info_list = []
        result = {}
        warning_list = []

        # config_class
        config_class = self.env['ir.config_parameter'].sudo()

        # ir_module_module_class
        ir_module_module_class = self.env['ir.module.module'].sudo()

        # company
        if len(self) == 1 and self.id:
            company = self
            company_id = company.id
            company_name = company.name
            company_vat = company.vat
        else:
            company = False
            company_id = False
            company_name = False
            company_vat = False
            error_list.append('could not set company')

        # api_enabled
        if company and company.l10n_hu_plus_api_enabled is not None:
            api_enabled = company.l10n_hu_plus_api_enabled
        else:
            api_enabled = False
            error_list.append("could not set api_enabled")

        ## app_version
        try:
            app_module = ir_module_module_class.search([
                ('name', '=', 'l10n_hu_plus'),
                ('state', '=', 'installed'),
            ])
            if app_module:
                app_version = app_module.installed_version
                debug_list.append("app_version set: " + str(app_version))
            else:
                app_version = False
                error_list.append("app_module not found, could not set app_version")
        except:
            app_version = False
            error_list.append('could not set app_version')

        ## database_uuid
        try:
            database_uuid = config_class.get_param('database.uuid')
        except:
            database_uuid = False
            error_list.append("could not set database_uuid")

        ## odoo_edition
        try:
            web_enterprise_module = ir_module_module_class.search([('name', '=', 'web_enterprise')])
            if web_enterprise_module:
                odoo_edition = 'enterprise'
            else:
                odoo_edition = 'community'
        except:
            odoo_edition = False
            error_list.append('could not set odoo_edition')

        ## odoo_release
        try:
            exp_version = odoo_service_common.exp_version()
            odoo_release = exp_version['server_serie']
        except:
            odoo_release = False
            error_list.append('could not set odoo_release')

        # Update application_data
        if len(error_list) == 0:
            api_environment.update({
                'app_version': app_version,
                'api_enabled': api_enabled,
                'company_id': company_id,
                'company_name': company_name,
                'company_vat': company_vat,
                'database_uuid': database_uuid,
                'odoo_edition': odoo_edition,
                'odoo_release': odoo_release,
            })

        # Update result
        result.update({
            'api_environment': api_environment,
            'debug_list': debug_list,
            'error_list': error_list,
            'info_list': info_list,
            'warning_list': warning_list,
        })

        # Return result
        # raise exceptions.UserError("l10n_hu_plus_get_api_environment END")
        return result
