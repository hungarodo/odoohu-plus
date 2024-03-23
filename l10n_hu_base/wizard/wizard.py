# -*- coding: utf-8 -*-
# 1 : imports of python lib
import re

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 : imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuBaseWizard(models.TransientModel):
    # Private attributes
    _name = 'l10n.hu.wizard'
    _description = "HU Wizard"

    # Default methods
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
    action_partner = fields.Selection(
        selection=[],
        string="DEPRECATED"
    )
    partner = fields.Many2many(
        comodel_name='res.partner',
        column1='wizard',
        column2='partner',
        default=_get_default_partner,
        relation='l10n_hu_wizard_partner_rel',
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

    # Constraints and onchanges
    @api.onchange('partner')
    def onchange_partner(self):
        self.partner_action_summary = self.get_partner_summary()

    @api.onchange('exchange_amount_from', 'exchange_amount_to')
    def onchange_currency_exchange(self):
        if self.exchange_action == 'custom_currency':
            if self.exchange_amount_to != 0:
                self.exchange_rate = self.exchange_amount_from / self.exchange_amount_to

    # CRUD methods (and name_get, name_search, ...) overrides

    # Action methods
    def action_execute(self):
        # Ensure one
        self.ensure_one()

        # Process actions
        # # PARTNER
        if self.action_type == 'partner':
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
                operation_result = partner.l10n_hu_manage_partner({'operation': 'delete'})
            # # DOWNLOAD
            elif self.action_type == 'partner' \
                    and self.action_partner == 'download':
                operation_result = partner.l10n_hu_manage_partner({'operation': 'download'})
            # # UPLOAD
            elif self.action_type == 'partner' \
                    and self.action_partner == 'upload':
                operation_result = partner.l10n_hu_manage_partner({'operation': 'upload'})
            # # PULL DATA
            elif self.action_type == 'partner' \
                    and self.action_partner == 'pull':
                operation_result = partner.l10n_hu_manage_partner({'operation': 'pull'})
            # # PUSH DATA
            elif self.action_type == 'partner' \
                    and self.action_partner == 'push':
                operation_result = partner.l10n_hu_manage_partner({'operation': 'push'})
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
