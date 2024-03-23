# -*- coding: utf-8 -*-
# 1 : imports of python lib

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 : imports from odoo modules
from odoo.tools.safe_eval import safe_eval

# 4 : variable declarations


# Class
class L10nHuAccountMove(models.Model):
    # Private attributes
    _inherit = 'account.move'

    # Default methods
    
    # Field declarations
    # # CURRENCY
    l10n_hu_company_currency = fields.Many2one(
        related='company_id.currency_id',
        string="Company Currency",
    )
    l10n_hu_currency_date = fields.Date(
        compute='_compute_l10n_hu_currency',
        string="Currency Date",
    )
    l10n_hu_currency_name = fields.Char(
        related='currency_id.name',
        string="Currency Name",
    )
    l10n_hu_currency_rate = fields.Float(
        compute='_compute_l10n_hu_currency',
        string="Currency Rate",
    )
    l10n_hu_document_rate = fields.Float(
        copy=False,
        string="Document Rate",
    )
    l10n_hu_foreign_currency = fields.Boolean(
        compute='_compute_l10n_hu_foreign_currency',
        string="Foreign Currency",
    )
    l10n_hu_rate_difference = fields.Float(
        compute='_compute_l10n_hu_rate_difference',
        string="Rate Difference",
    )
    # # DOCUMENT TYPE
    l10n_hu_document_type = fields.Many2one(
        comodel_name='l10n.hu.document.type',
        index=True,
        string="Document Type",
    )
    l10n_hu_document_type_code = fields.Char(
        related='l10n_hu_document_type.code',
        string="Document Type Code",
    )
    # # JOURNAL
    l10n_hu_journal_show_print_pdf = fields.Boolean(
        related='journal_id.l10n_hu_show_print_pdf',
        string="Show Print PDF",
    )
    l10n_hu_journal_technical_type = fields.Selection(
        related='journal_id.l10n_hu_technical_type',
        string="Journal Technical Type",
    )
    l10n_hu_journal_type = fields.Selection(
        related='journal_id.type',
        string="Journal Type",
    )
    # # ORIGINAL
    l10n_hu_original_account_move = fields.Many2one(
        comodel_name='account.move',
        copy=False,
        readonly=True,
        string="Original Account Move",
    )
    l10n_hu_original_invoice_number = fields.Char(
        copy=False,
        string="Original Invoice Number",
    )
    # # OSS
    l10n_hu_eu_oss_eligible = fields.Boolean(
        copy=False,
        default=False,
        string="EU OSS Eligible",
    )
    l10n_hu_eu_oss_enabled = fields.Boolean(
        copy=False,
        default=False,
        string="EU OSS Enabled",
    )
    # # PARTNER
    l10n_hu_company_partner = fields.Many2one(
        related='company_id.partner_id',
        string="Company Partner",
    )
    l10n_hu_fiscal_representative = fields.Many2one(
        comodel_name='res.partner',
        index=True,
        string="Fiscal Representative",
    )
    l10n_hu_fiscal_representative_bank_account = fields.Many2one(
        comodel_name='res.partner.bank',
        index=True,
        string="Fiscal Representative Bank Account",
    )
    l10n_hu_partner_country = fields.Many2one(
        comodel_name='res.country',
        related='partner_id.country_id',
        index=True,
        store=True,
        string="Partner Country",
    )
    l10n_hu_trade_position = fields.Selection(
        related='fiscal_position_id.l10n_hu_trade_position',
        index=True,
        store=True,
        string="Trade Position",
    )
    # # PERIOD
    l10n_hu_invoice_delivery_period_end = fields.Date(
        string="Invoice Delivery Period End",
    )
    l10n_hu_invoice_delivery_period_start = fields.Date(
        string="Invoice Delivery Period Start",
    )
    l10n_hu_invoice_delivery_period_summary = fields.Text(
        string="Invoice Delivery Period Summary",
    )
    l10n_hu_invoice_periodical_delivery = fields.Boolean(
        default=False,
        string="Invoice Periodical Delivery",
    )
    # # PAYMENT
    l10n_hu_invoice_payment_method = fields.Many2one(
        comodel_name='account.payment.method',
        index=True,
        string="Invoice Payment Method",
    )
    # # VAT
    l10n_hu_vat_date = fields.Date(
        string="VAT Date",
    )

    # Compute and search fields, in the same order of field declarations
    def _compute_l10n_hu_foreign_currency(self):
        for record in self:
            if record.currency_id and record.currency_id != record.company_id.currency_id:
                record.l10n_hu_foreign_currency = True
            else:
                record.l10n_hu_foreign_currency = False

    def _compute_l10n_hu_currency(self):
        for record in self:
            last_rate = self.env['res.currency.rate'].search([
                ('company_id', '=', record.company_id.id),
                ('currency_id', '=', record.currency_id.id),
                ('name', '<=', record.date)
            ], limit=1)
            if last_rate:
                record.l10n_hu_currency_date = last_rate.name
                record.l10n_hu_currency_rate = last_rate.inverse_company_rate
            else:
                record.l10n_hu_currency_date = record.date
                record.l10n_hu_currency_rate = 1.0

    def _compute_l10n_hu_rate_difference(self):
        for record in self:
            difference = record.l10n_hu_currency_rate - record.l10n_hu_document_rate
            record.l10n_hu_rate_difference = difference

    @api.depends('partner_id')
    def _compute_l10n_hu_vat_position(self):
        for record in self:
            if record.state == 'draft' and record.partner_id:
                vat_position_result = record.l10n_hu_get_vat_position({})
                if vat_position_result.get('error_list', []) == 0:
                    vat_position = vat_position_result.get('vat_position')
                else:
                    vat_position = False
            elif record.state != 'draft' and record.partner_id:
                vat_position = record.l10n_hu_vat_position
            else:
                vat_position = False

            # Set value
            record.l10n_hu_vat_position = vat_position

    # Constraints and onchanges

    # CRUD methods (and name_get, name_search, ...) overrides

    # Action methods
    def action_l10n_hu_update_eu_oss(self):
        # Checks
        for record in self:
            if not record.is_invoice:
                error_text = _("This action isn't available for this document.")
                error_text += " " + str(record.display_name)
                raise exceptions.ValidationError(error_text)

        # Set fields
        for record in self:
            oss_data = record.l10n_hu_get_eu_oss_data({})
            if oss_data.get('update_allowed') \
                    and oss_data['update_allowed'] is not None:
                record.l10n_hu_eu_oss_eligible = oss_data.get('eu_oss_eligible', False)
                record.l10n_hu_eu_oss_enabled = oss_data.get('eu_oss_enabled', False)

        # Return
        return

    def action_l10n_hu_wizard_currency_exchange(self):
        """ Open the L10n HU wizard to calculate the document rate """
        # Make sure there is one record in self
        self.ensure_one()

        # Assemble context
        context = {
            'default_action_type': 'currency_exchange',
            'default_action_type_visible': False,
            'default_account_move': [self.id],
            'default_exchange_action': 'custom_currency',
            'default_exchange_currency_from': self.company_id.currency_id.id,
            'default_exchange_currency_to': self.currency_id.id,
        }

        # Assemble result
        result = {
            'name': _("HU Wizard"),
            'context': context,
            'res_model': 'l10n.hu.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
        }

        # Return result
        return result

    # Business methods
    # # L10NHU METHODS
    @api.model
    def l10n_hu_get_eu_oss_data(self, values):
        """ Get OSS data (eligibility, settings, etc.)

        OSS eligible if:
        - account move is an invoice
        - AND commercial partner is private person (not company)
        - AND commercial partner country is in EU
        - AND company country is in EU
        - AND commercial partner country is not the same as the company country

        OSS enabled can be set:
        - in ANY state: from values
        - in draft state: from values or from journal default setting

        Update allowed:
        - account move is not posted

        :param values: dictionary

        :return: dictionary
        """
        # raise exceptions.UserError(str(values))

        # Initialize variables
        debug_list = []
        error_list = []
        info_list = []
        result = {}
        warning_list = []

        # Set account_move
        if values.get('account_move_id'):
            account_move = self.env['account.move'].sudo().browse(values['account_move_id'])
            debug_list.append("account_move set from id in values: " + str(account_move.id))
        elif values.get('account_move'):
            account_move = values['account_move']
            debug_list.append("account_move set from values: " + str(account_move.id))
        elif len(self) == 1 and self.id:
            account_move = self
            debug_list.append("account_move set from self: " + str(account_move.id))
        else:
            account_move = False
            error_list.append("could not set account_move")

        # account_journal
        if account_move and account_move.journal_id:
            account_journal = account_move.journal_id
        else:
            account_journal = False
            error_list.append("could not set account_journal")

        # EU
        try:
            eu_country_group = self.env.ref('base.europe')
            debug_list.append("eu_country_group set: " + str(eu_country_group.id))
        except:
            eu_country_group = False
            error_list.append("could not set eu_country_group")

        # Is invoice
        if account_move:
            is_invoice = account_move.is_invoice(include_receipts=True)
            debug_list.append("is_invoice set: " + str(is_invoice))
        else:
            is_invoice = False
            error_list.append("could not set is_invoice")

        # commercial_partner
        if account_move and account_move.partner_id:
            commercial_partner = account_move.partner_id.commercial_partner_id
            debug_list.append("commercial_partner set: " + str(commercial_partner.id))
        else:
            commercial_partner = False
            error_list.append("could not set commercial_partner")

        # eu_oss_eligible
        if is_invoice \
                and eu_country_group \
                and account_move.company_id \
                and account_move.company_id.country_id \
                and account_move.company_id.country_id in eu_country_group.country_ids \
                and commercial_partner \
                and not commercial_partner.is_company \
                and commercial_partner.country_id \
                and commercial_partner.country_id in eu_country_group.country_ids \
                and commercial_partner.country_id != account_move.company_id.country_id:
            eu_oss_eligible = True
        else:
            eu_oss_eligible = False
        debug_list.append("eu_oss_eligible set: " + str(eu_oss_eligible))

        # eu_oss_enabled
        if values.get('l10n_hu_eu_oss_enabled'):
            eu_oss_enabled = True
            debug_list.append("eu_oss_enabled set from scenario 1: " + str(eu_oss_eligible))
        elif account_move \
                and account_move.state != 'draft' \
                and is_invoice:
            eu_oss_enabled = account_move.l10n_hu_eu_oss_enabled
            debug_list.append("eu_oss_enabled set from scenario 2: " + str(eu_oss_eligible))
        elif account_move \
                and account_move.state == 'draft' \
                and account_journal \
                and account_journal.l10n_hu_eu_oss_enabled \
                and is_invoice:
            eu_oss_enabled = True
            debug_list.append("eu_oss_enabled set from scenario 3: " + str(eu_oss_eligible))
        else:
            eu_oss_enabled = False
            debug_list.append("eu_oss_enabled set from else: " + str(eu_oss_eligible))

        # update_allowed
        if account_move \
                and account_move.state == 'draft' \
                and commercial_partner \
                and is_invoice:
            update_allowed = True
        else:
            update_allowed = False
        debug_list.append("update_allowed set: " + str(update_allowed))

        # Update result
        result.update({
            'account_move': account_move,
            'commercial_partner': commercial_partner,
            'debug_list': debug_list,
            'error_list': error_list,
            'eu_oss_eligible': eu_oss_eligible,
            'eu_oss_enabled': eu_oss_enabled,
            'info_list': info_list,
            'update_allowed': update_allowed,
            'warning_list': warning_list,
        })

        # Return result
        # raise exceptions.UserError(str(result))
        return result
