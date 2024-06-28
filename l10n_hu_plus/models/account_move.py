# -*- coding: utf-8 -*-
# 1 : imports of python lib

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 : imports from odoo modules
from odoo.tools.safe_eval import safe_eval

# 4 : variable declarations


# Class
class L10nHuPlusAccountMove(models.Model):
    # Private attributes
    _inherit = 'account.move'

    # Default methods
    
    # Field declarations
    # # CURRENCY
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
    l10n_hu_rate_difference = fields.Float(
        compute='_compute_l10n_hu_rate_difference',
        string="Rate Difference",
    )
    # # DOCUMENT TYPE
    l10n_hu_plus_document_type = fields.Many2one(
        comodel_name='l10n.hu.plus.object',
        domain=[('type_technical_name', '=', 'document_type')],
        index=True,
        string="Document Type",
    )
    l10n_hu_plus_document_type_code = fields.Char(
        related='l10n_hu_plus_document_type.code',
        string="Document Type Code",
    )
    # # JOURNAL
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

    # CRUD methods (and display_name, name_search, ...) overrides

    # Action methods
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
            'name': _("HU+ Wizard"),
            'context': context,
            'res_model': 'l10n.hu.plus.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
        }

        # Return result
        return result

    # Business methods
