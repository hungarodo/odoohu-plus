# -*- coding: utf-8 -*-
# 1 : imports of python lib
import json
import re

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 : imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuPlusWizard(models.TransientModel):
    # Private attributes
    _name = 'l10n.hu.plus.wizard'
    _description = "HU+ Wizard"

    # Default methods
    @api.model
    def _get_default_account_move(self):
        account_move_ids = []
        if self._context.get('active_model') and self._context['active_model'] == 'account.move':
            account_move_ids = self._context.get('active_ids', [])
        return [(4, x, 0) for x in account_move_ids]

    @api.model
    def _get_default_active_model(self):
        model_id = False
        if self._context.get('active_model'):
            model_name = self._context.get('active_model')
            model = self.env['ir.model'].sudo().search([
                ('model', '=', model_name)
            ], limit=1)
            if model:
                model_id = model.id
        return model_id

    @api.model
    def _get_default_partner(self):
        partner_ids = []
        if self._context.get('active_model') and self._context['active_model'] == 'res.partner':
            partner_ids = self._context.get('active_ids', [])
        return [(4, x, 0) for x in partner_ids]

    # Field declarations
    # # COMMON
    action_type = fields.Selection(
        selection=[
            ('api', "API"),
            ('configuration', "Configuration"),
            ('currency_exchange', "Currency Exchange"),
            ('product', "Product"),
        ],
        string="Action Type",
    )
    action_type_visible = fields.Boolean(
        default=False,
        string="Action Type Visible",
    )
    active_model = fields.Many2one(
        comodel_name='ir.model',
        default=_get_default_active_model,
        string="Active Model",
    )
    active_model_id = fields.Integer(
        related='active_model.id',
        string="Active Model ID",
    )
    active_model_name = fields.Char(
        related='active_model.model',
        string="Active Model Name",
    )
    company = fields.Many2one(
        comodel_name='res.company',
        default=lambda self: self.env.company.id,
        index=True,
        readonly=True,
        string="Company",
    )
    company_currency = fields.Many2one(
        related='company.currency_id',
        string="Company Currency",
    )
    company_currency_code = fields.Char(
        related='company.currency_id.name',
        string="Company Currency Code",
    )
    # # ACCOUNT MOVE
    account_move = fields.Many2many(
        comodel_name='account.move',
        column1='wizard',
        column2='account_move',
        default=_get_default_account_move,
        relation='l10n_hu_plus_wizard_account_move_rel',
        string="Account Move",
    )
    account_move_action = fields.Selection(
        selection=[
            ('list', "List"),
        ],
        string="Account Move Action",
    )
    account_move_action_editable = fields.Boolean(
        default=True,
        string="Account Move Action Editable",
    )
    account_move_count = fields.Integer(
        compute='_compute_account_move_count',
        string="Account Move Count",
    )
    account_move_visible = fields.Boolean(
        default=False,
        string="Account Move Visible",
    )
    # # API
    api_action = fields.Selection(
        selection=[
            ('check_registration', "Check registration"),
            ('create_registration', "Create registration"),
            ('delete_registration', "Delete registration"),
            ('download_objects', "Download objects"),
        ],
        string="API Action",
    )
    api_action_editable = fields.Boolean(
        default=True,
        string="API Action Editable",
    )
    api_data = fields.Text(
        related='company.l10n_hu_plus_api_data',
        string="API Data",
    )
    api_details = fields.Text(
        readonly=True,
        string="API Details",
    )
    api_key = fields.Char(
        string="API Key",
    )
    api_license_code = fields.Char(
        string="API License Code",
    )
    api_url = fields.Char(
        string="API URL",
    )
    # # CURRENCY EXCHANGE
    company_currency_rate = fields.Many2one(
        comodel_name='res.currency.rate',
        string="Company Currency Rate",
    )
    company_currency_rate_amount = fields.Float(
        related='company_currency_rate.company_rate',
        string="Company Currency Rate Amount",
    )
    company_currency_rate_date = fields.Date(
        related='company_currency_rate.name',
        string="Company Currency Rate Date",
    )
    company_currency_rate_inverse_amount = fields.Float(
        related='company_currency_rate.inverse_company_rate',
        string="Company Currency Rate Inverse Amount",
    )
    company_currency_rate_inverse_visible = fields.Boolean(
        default=True,
        string="Company Currency Rate Inverse Invisible",
    )
    exchange_action = fields.Selection(
        selection=[
            ('from_company_currency', "From company currency"),
            ('to_company_currency', "To company currency"),
            ('custom_currency', "Custom currency"),
        ],
        string="Exchange Method",
    )
    exchange_action_editable = fields.Boolean(
        default=True,
        string="Exchange Action Editable",
    )
    exchange_amount_from = fields.Float(
        string="Exchange Amount From",
    )
    exchange_amount_to = fields.Float(
        string="Exchange Amount To",
    )
    exchange_currency_from = fields.Many2one(
        comodel_name='res.currency',
        string="Exchange Currency From",
    )
    exchange_currency_to = fields.Many2one(
        comodel_name='res.currency',
        string="Exchange Currency To",
    )
    exchange_rate = fields.Float(
        string="Exchange Rate",
    )
    exchange_visible = fields.Boolean(
        default=True,
        string="Exchange Invisible",
    )
    # # PARTNER
    partner = fields.Many2many(
        comodel_name='res.partner',
        column1='wizard',
        column2='partner',
        default=_get_default_partner,
        relation='l10n_hu_plus_wizard_partner_rel',
        string="Partner",
    )
    partner_action = fields.Selection(
        default='list',
        selection=[
            ('list', "List partners"),
        ],
        string="Partner Action",
    )
    partner_action_editable = fields.Boolean(
        default=True,
        string="Partner Action Editable",
    )
    partner_action_summary = fields.Text(
        readonly=True,
        string="Partner Action Summary",
    )
    partner_visible = fields.Boolean(
        default=False,
        string="Partner Visible",
    )

    # Compute and search fields, in the same order of field declarations
    def _compute_account_move_count(self):
        for record in self:
            record.account_move_count = len(record.account_move)

    # Constraints and onchanges
    @api.onchange('api_action')
    def onchange_api_action(self):
        if self.api_action is not None and self.company:
            api_data = self.company.l10n_hu_plus_get_api_data()
            api_details = _("API Key") + ": " + str(api_data.get('api_key', None))
            api_details += "\n" + _("License active") + ": " + str(api_data.get('license_active', None))
            api_details += "\n" + _("License code") + ": " + str(api_data.get('license_code', None))
            api_details += "\n" + _("License owner") + ": " + str(api_data.get('license_owner', None))
            api_details += "\n" + _("License type") + ": " + str(api_data.get('license_type', None))
            api_details += "\n" + _("License valid") + ": " + str(api_data.get('license_valid', None))
            api_details += "\n" + _("License expiry") + ": " + str(api_data.get('license_valid_to', None))
            self.api_details = api_details
            self.api_key = api_data.get('api_key', "free")
            self.api_license_code = api_data.get('license_code', "free")
            self.api_url = api_data.get('api_url', "")
        else:
            pass

    @api.onchange('partner')
    def onchange_partner(self):
        self.partner_action_summary = self.get_partner_summary()

    @api.onchange('exchange_amount_from', 'exchange_amount_to')
    def onchange_currency_exchange(self):
        if self.exchange_action == 'custom_currency':
            if self.exchange_amount_to != 0:
                self.exchange_rate = self.exchange_amount_from / self.exchange_amount_to

    # CRUD methods (and display_name, name_search, ...) overrides

    # Action methods
    def action_execute(self):
        # Ensure one
        self.ensure_one()

        # Process actions
        # # ACCOUNT MOVE
        if self.action_type == 'account_move' and self.account_move:
            # Manage result
            manage_result = self.manage_account_move()

            if manage_result.get('account_move_ids') and len(manage_result['account_move_ids']) == 1:
                result = {
                    'name': _("Account Move"),
                    'res_id': manage_result['account_move_ids'][0],
                    'res_model': 'account.move',
                    'target': 'current',
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form,tree',
                }
                return result
            elif manage_result.get('account_move_ids'):
                result = {
                    'name': _("Account Moves"),
                    'domain': [('id', 'in', manage_result['account_move_ids'])],
                    'res_model': 'account.move',
                    'target': 'current',
                    'type': 'ir.actions.act_window',
                    'view_mode': 'tree,form',
                }
                return result
            else:
                raise exceptions.UserError("account move action error!")
        # # API
        elif self.action_type == 'api':
            # Update company API data
            api_data = self.company.l10n_hu_get_api_data()
            if self.api_key:
                api_data.update({
                    'api_key': self.api_key,
                })
            if self.api_url:
                api_data.update({
                    'api_url': self.api_url,
                })
            if self.api_license_code:
                api_data.update({
                    'license_code': self.api_license_code,
                })
            self.company.write({
                'l10n_hu_api_data': json.dumps(api_data, default=str)
            })

            # Manage result
            manage_result = self.manage_api()

            # Wizard result
            if self.api_action in ['check_registration', 'create_registration', 'delete_registration']:
                result = {
                    'name': _("Company"),
                    'res_id': self.company.id,
                    'res_model': 'res.company',
                    'target': 'current',
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form,tree',
                }
                return result
            elif manage_result.get('object_ids') and len(manage_result['object_ids']) == 1:
                result = {
                    'name': _("HU+ Object"),
                    'res_id': manage_result['object_ids'][0],
                    'res_model': 'l10n.hu.plus.object',
                    'target': 'current',
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form,tree',
                }
                return result
            elif manage_result.get('object_ids'):
                result = {
                    'name': _("HU+ Objects"),
                    'domain': [('id', 'in', manage_result['object_ids'])],
                    'res_model': 'l10n.hu.plus.object',
                    'target': 'current',
                    'type': 'ir.actions.act_window',
                    'view_mode': 'tree,form',
                }
                return result
            elif manage_result.get('log_ids') and len(manage_result['log_ids']) == 1:
                result = {
                    'name': _("HU+ Log"),
                    'res_id': manage_result['log_ids'][0],
                    'res_model': 'l10n.hu.plus.log',
                    'target': 'current',
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form,tree',
                }
                return result
            elif manage_result.get('log_ids'):
                result = {
                    'name': _("HU+ Logs"),
                    'domain': [('id', 'in', manage_result['log_ids'])],
                    'res_model': 'l10n.hu.plus.log',
                    'target': 'current',
                    'type': 'ir.actions.act_window',
                    'view_mode': 'tree,form',
                }
                return result
            else:
                raise exceptions.UserError("api action error!")
        # # PARTNER
        elif self.action_type == 'partner':
            # # # list
            if self.action_partner == 'list':
                # Check input
                if not self.partner:
                    raise exceptions.UserError(_("No partner selected!"))

                # Manage result
                manage_result = self.manage_partner()

                # Wizard result
                if manage_result.get('partner_ids'):
                    result = {
                        'name': _("Partner"),
                        'domain': [('id', 'in', manage_result['partner_ids'])],
                        'res_model': 'res.partner',
                        'target': 'current',
                        'type': 'ir.actions.act_window',
                        'view_mode': 'tree,form',
                    }
                    return result
                else:
                    raise exceptions.UserError("partner_delete error!")
            # # # else
            else:
                raise exceptions.UserError("invalid partner action!")
        # # else
        else:
            pass

        # Return result
        return

    # Business methods
    # # HELPER
    @api.model
    def get_partner_summary(self):
        """ Get summary for the selected partners

        :return: string
        """
        # Initialize variables
        result = ""

        # Process scenarios
        if self.action_type == 'partner' \
                and self.partner:
            # Partner count
            partner_count = len(self.partner)
            result += _("Selected") + ": " + str(partner_count)

            # Partner details
            no_company_partners = []

            for partner in self.partner:
                if not partner.company_id:
                    no_company_partners.append(partner)

            # Summary
            result += "\n" + _("No Company") + ": " + str(len(no_company_partners))
        else:
            pass

        # Return result
        return result

    # # MANAGE
    @api.model
    def manage_account_move(self):
        """ Manage account move actions

        NOTE:
        - We may iterate because account move field is m2m to support mass management

        :return: dictionary
        """
        # Initialize variables
        account_moves = []
        account_move_ids = []
        account_move_ids_ignored = []
        account_move_ids_managed = []
        result = {}

        # Process scenarios
        if self.action_type == 'account_move':
            if self.account_move_action == 'list':
                operation_result = {}
            else:
                pass
        else:
            pass

        # Update result
        result.update({
            'account_moves': account_moves,
            'account_move_ids': account_move_ids,
            'account_move_ids_ignored': account_move_ids_ignored,
            'account_move_ids_managed': account_move_ids_managed,
        })

        # Return result
        # raise exceptions.UserError(str(result))
        return result

    @api.model
    def manage_api(self):
        """ Manage API actions

        :return: dictionary
        """
        # Initialize variables
        api_result = {}
        debug_list = []
        error_list = []
        info_list = []
        log_ids = []
        object_ids = []
        result = {}
        warning_list = []

        # Process scenarios
        if self.action_type == 'api':
            debug_list.append("processing api action_type")
            if self.api_action == 'check_registration':
                debug_list.append("processing check_registration api_action")
                api_values = {
                    'request_type': 'get_registration',
                }
                api_result = self.company.l10n_hu_plus_api_registration_request(api_values)
            # # Create registration
            elif self.api_action == 'create_registration':
                debug_list.append("processing create_registration api_action")
                api_values = {
                    'request_type': 'post_registration',
                }
                api_result = self.company.l10n_hu_plus_api_registration_request(api_values)
            # # Delete registration
            elif self.api_action == 'delete_registration':
                debug_list.append("processing delete_registration api_action")
                api_values = {
                    'request_type': 'delete_registration',
                }
                api_result = self.company.l10n_hu_plus_api_registration_request(api_values)
            # # Get objects
            elif self.api_action == 'download_objects':
                debug_list.append("processing download_objects api_action")
                api_values = {
                    'request_type': 'get_object',
                }
                object_class = self.env['l10n.hu.plus.object']
                api_result = object_class.api_object_request(api_values)
            else:
                error_list.append("invalid api_action")
        else:
            error_list.append("invalid action_type")

        # Append to lists
        if api_result.get('l10n_hu_plus_log'):
            log_ids.append(api_result['l10n_hu_plus_log'].id)
        if api_result.get('l10n_hu_plus_object'):
            object_ids.append(api_result['l10n_hu_plus_object'].id)

        # Update result
        result.update({
            'api_result': api_result,
            'debug_list': debug_list,
            'error_list': error_list,
            'info_list': info_list,
            'log_ids': log_ids,
            'object_ids': object_ids,
            'warning_list': warning_list,
        })

        # Return result
        # raise exceptions.UserError(str(result))
        return result

    @api.model
    def manage_partner(self):
        """ Manage partner actions

        We iterate because partner field is m2m to support mass management

        :return: dictionary
        """
        # Initialize variables
        messages = []
        message_ids = []
        message_results = []
        partners = []
        partner_ids = []
        partner_ids_ignored = []
        partner_ids_managed = []
        result = {}

        # Iterate partners
        for partner in self.partner:
            # Process scenarios
            # # DELETE
            if self.action_type == 'partner' \
                    and self.action_partner == 'delete':
                operation_result = partner.l10n_hu_plus_manage_partner({'operation': 'delete'})
            # # DOWNLOAD
            elif self.action_type == 'partner' \
                    and self.action_partner == 'download':
                operation_result = partner.l10n_hu_plus_manage_partner({'operation': 'download'})
            # # UPLOAD
            elif self.action_type == 'partner' \
                    and self.action_partner == 'upload':
                operation_result = partner.l10n_hu_plus_manage_partner({'operation': 'upload'})
            # # PULL DATA
            elif self.action_type == 'partner' \
                    and self.action_partner == 'pull':
                operation_result = partner.l10n_hu_plus_manage_partner({'operation': 'pull'})
            # # PUSH DATA
            elif self.action_type == 'partner' \
                    and self.action_partner == 'push':
                operation_result = partner.l10n_hu_plus_manage_partner({'operation': 'push'})
            else:
                operation_result = {}

            # Append to lists
            partners.append(partner)
            partner_ids.append(partner.id)
            message_results += operation_result.get('message_results', [])
            messages += operation_result.get('message_results',[])
            message_ids += operation_result.get('message_ids', [])
            partner_ids += operation_result.get('partner_ids', [])
            partner_ids_ignored += operation_result.get('partner_ids_ignored', [])
            partner_ids_managed += operation_result.get('partner_ids_managed', [])

        # Update result
        result.update({
            'messages': messages,
            'message_ids': message_ids,
            'message_results': message_results,
            'partners': partners,
            'partner_ids': partner_ids,
            'partner_ids_ignored': partner_ids_ignored,
            'partner_ids_managed': partner_ids_managed,
        })

        # Return result
        # raise exceptions.UserError(str(result))
        return result
