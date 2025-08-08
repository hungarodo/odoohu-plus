# -*- coding: utf-8 -*-
# 1 : imports of python lib
import base64
import datetime

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered
from odoo.tools import formatLang

# 3 : imports from odoo modules
from odoo.addons.l10n_hu_edi.models.l10n_hu_edi_connection import format_bool, L10nHuEdiConnection, L10nHuEdiConnectionError

# 4 : variable declarations


# Class
class L10nHuPlusAccountMove(models.Model):
    # Private attributes
    _inherit = 'account.move'

    # Default methods

    # Field declarations
    ## CASH ACCOUNTING
    l10n_hu_cash_accounting = fields.Boolean(
        compute='_compute_l10n_hu_cash_accounting',
        copy=False,
        default=False,
        index=True,
        readonly=False,
        store=True,
        string="HU Cash Accounting",
        tracking=True,
    )
    ## CURRENCY
    l10n_hu_company_currency_name = fields.Char(
        related='company_currency_id.name',
        string="HU Company Currency Name",
    )
    l10n_hu_currency_date = fields.Date(
        compute='_compute_l10n_hu_currency',
        string="HU Currency Date",
    )
    l10n_hu_currency_name = fields.Char(
        related='currency_id.name',
        string="HU Currency Name",
    )
    l10n_hu_currency_rate = fields.Float(
        compute='_compute_l10n_hu_currency',
        string="HU Currency Rate",
    )
    l10n_hu_document_rate = fields.Float(
        copy=False,
        default=0,
        string="HU Document Rate",
    )
    l10n_hu_document_rate_difference = fields.Float(
        compute='_compute_l10n_hu_document_rate_difference',
        string="HU Document Rate Difference",
    )
    l10n_hu_huf_rate = fields.Float(
        copy=False,
        default=0,
        string="HU HUF Rate",
    )
    ## DELIVERY PERIOD
    l10n_hu_delivery_period_end = fields.Date(
        copy=False,
        string="HU Delivery Period End",
        tracking=True,
    )
    l10n_hu_delivery_period_legal = fields.Text(
        compute='_compute_l10n_hu_delivery_period_text',
        string="HU Invoice Delivery Period Legal",
    )
    l10n_hu_delivery_period_start = fields.Date(
        copy=False,
        string="HU Delivery Period Start",
        tracking=True,
    )
    l10n_hu_delivery_period_summary = fields.Text(
        compute='_compute_l10n_hu_delivery_period_text',
        string="HU Delivery Period Summary",
    )
    ## DOCUMENT TYPE
    l10n_hu_document_type = fields.Many2one(
        comodel_name='l10n.hu.plus.tag',
        domain=[('tag_type', '=', 'document_type')],
        index=True,
        string="HU Document Type",
        tracking=True,
    )
    ## HU+
    l10n_hu_plus_notes = fields.Char(
        copy=False,
        index=True,
        string="HU+ Notes",
    )
    l10n_hu_plus_status = fields.Selection(
        copy=False,
        selection=[
            ('error', "Error"),
            ('info', "Information"),
            ('ok', "Ok"),
            ('other', "Other"),
            ('warning', "Warning"),
        ],
        string="HU+ Status",
    )
    l10n_hu_plus_tag = fields.Many2many(
        column1='account_move',
        column2='tag',
        comodel_name='l10n.hu.plus.tag',
        domain=[('tag_type', 'in', ['account_move', 'general'])],
        index=True,
        relation='l10n_hu_plus_tag_account_move_rel',
        string="HU+ Tag",
    )
    ## JOURNAL
    l10n_hu_banner_enabled = fields.Boolean(
        related='journal_id.l10n_hu_banner_enabled',
        string="HU Banner",
    )
    l10n_hu_journal_type = fields.Selection(
        related='journal_id.type',
        string="HU Journal Type",
    )
    l10n_hu_plus_enabled = fields.Boolean(
        related='journal_id.l10n_hu_plus_enabled',
        string="HU+ Enabled",
    )
    ## ORIGINAL
    l10n_hu_original_invoice_number = fields.Char(
        copy=False,
        string="HU Original Invoice Number",
        tracking=True,
    )
    ## PARTNER
    l10n_hu_company_partner = fields.Many2one(
        related='company_id.partner_id',
        string="HU Company Partner",
    )
    l10n_hu_fiscal_representative = fields.Many2one(
        comodel_name='res.partner',
        index=True,
        string="HU Fiscal Representative",
    )
    l10n_hu_fiscal_representative_bank_account = fields.Many2one(
        comodel_name='res.partner.bank',
        index=True,
        string="HU Fiscal Representative Bank Account",
    )
    l10n_hu_partner_country = fields.Many2one(
        comodel_name='res.country',
        related='partner_id.country_id',
        index=True,
        store=True,
        string="HU Partner Country",
    )
    l10n_hu_trade_position = fields.Selection(
        related='fiscal_position_id.l10n_hu_trade_position',
        index=True,
        store=True,
        string="HU Trade Position",
    )
    ## PROFORMA
    l10n_hu_proforma_date = fields.Date(
        copy=False,
        help="Date when the proforma is sent out, automatically updated, also editable manually",
        string="Proforma Date",
        tracking=True,
    )
    l10n_hu_proforma_name = fields.Char(
        copy=False,
        help="Name of the proforma, automatically generated when sending, also editable manually",
        string="HU Proforma Name",
        tracking=True,
    )
    l10n_hu_proforma_sequence = fields.Many2one(
        related='journal_id.l10n_hu_proforma_sequence',
        string="HU Proforma Sequence",
    )
    ## VAT
    l10n_hu_vat_date = fields.Date(
        copy=False,
        index=True,
        string="HU VAT Date",
        tracking=True,
    )

    # Compute and search fields, in the same order of field declarations
    ## SUPER
    @api.depends('country_code', 'move_type')
    def _compute_show_delivery_date(self):
        # EXTENDS 'account'
        super()._compute_show_delivery_date()
        for move in self:
            if move.country_code == 'HU':
                move.show_delivery_date = True

    ## HU+
    @api.depends('partner_id')
    def _compute_l10n_hu_cash_accounting(self):
        for record in self:
            record.l10n_hu_cash_accounting = record.l10n_hu_get_cash_accounting()

    def _compute_l10n_hu_currency(self):
        for record in self:
            if record.delivery_date:
                if record.invoice_date and record.delivery_date > record.invoice_date:
                    currency_date = record.invoice_date
                elif record.delivery_date > fields.Date.today():
                    currency_date = fields.Date.today()
                else:
                    currency_date = record.delivery_date
                last_rate = self.env['res.currency.rate'].search([
                    ('company_id', '=', record.company_id.id),
                    ('currency_id', '=', record.currency_id.id),
                    ('name', '<=', record.delivery_date)
                ], limit=1)
            else:
                currency_date = record.date
                last_rate = self.env['res.currency.rate'].search([
                    ('company_id', '=', record.company_id.id),
                    ('currency_id', '=', record.currency_id.id),
                    ('name', '<=', record.date)
                ], limit=1)
            if last_rate:
                record.l10n_hu_currency_date = currency_date
                record.l10n_hu_currency_rate = last_rate.inverse_company_rate
            else:
                record.l10n_hu_currency_date = currency_date
                record.l10n_hu_currency_rate = 1.0
                record.l10n_hu_document_rate = 1.0

    def _compute_l10n_hu_delivery_period_text(self):
        for record in self:
            period_legal = ""
            period_summary = ""
            if record.move_type in ['out_invoice', 'out_refund'] \
                    and record.l10n_hu_delivery_period_start \
                    and record.l10n_hu_delivery_period_end:
                # Get period info
                delivery_period_result = record.l10n_hu_get_delivery_period_data({})
                if delivery_period_result.get('period_legal'):
                    period_legal = delivery_period_result['period_legal']
                if delivery_period_result.get('period_summary'):
                    period_summary = delivery_period_result['period_summary']
            record.l10n_hu_delivery_period_legal = period_legal
            record.l10n_hu_delivery_period_summary = period_summary

    def _compute_l10n_hu_document_rate_difference(self):
        for record in self:
            difference = record.l10n_hu_currency_rate - record.l10n_hu_document_rate
            record.l10n_hu_document_rate_difference = difference

    # Constraints and onchanges
    @api.onchange('l10n_hu_delivery_period_end', 'l10n_hu_delivery_period_start')
    def onchange_l10n_hu_delivery_period(self):
        if self.l10n_hu_delivery_period_end and self.l10n_hu_delivery_period_start:
            if self.l10n_hu_delivery_period_end < self.l10n_hu_delivery_period_start:
                raise exceptions.ValidationError(_("Period end date must be after period start date!"))
            else:
                pass
        else:
            pass

    # CRUD methods (and display_name, name_search, ...) overrides

    # Action methods
    def action_l10n_hu_plus_documentation(self):
        """ HU+ documentation """
        # Make sure there is one record in self
        self.ensure_one()

        # Return
        return self.company_id.action_l10n_hu_plus_documentation()

    def action_l10n_hu_send_proforma(self):
        """Open a window to compose an email using mail template loaded by default"""
        # Ensure one
        self.ensure_one()

        # Prepare proforma_name
        if not self.l10n_hu_proforma_name and self.journal_id and self.journal_id.l10n_hu_proforma_sequence:
            self.l10n_hu_proforma_name = self.journal_id.l10n_hu_proforma_sequence.next_by_id()
        elif not self.l10n_hu_proforma_name:
            self.l10n_hu_proforma_name = self.env["ir.sequence"].next_by_code("l10n.hu.account.move.proforma")
        else:
            pass

        # proforma_self
        proforma_self = self.with_context(l10n_hu_use_proforma=True, proforma=True)

        # Get mail template
        if self.journal_id and self.journal_id.l10n_hu_proforma_mail_template:
            template_id = self.journal_id.l10n_hu_proforma_mail_template.id
        else:
            try:
                template_id = self.env.ref('l10n_hu_plus.account_move_proforma_mail_template').id
            except ValueError:
                template_id = False

        # Get composer
        try:
            compose_form_id = self.env['ir.model.data']._xmlid_lookup('mail.email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False

        # Set template
        template = template_id and self.env['mail.template'].browse(template_id)

        # Set final language
        if template and template.lang:
            language_dict = template._render_template(template.lang, 'account.move', proforma_self.ids)
            # raise exceptions.UserError("language_dict" + str(language_dict))
            language = language_dict[self.id]
        else:
            language = self.env.context.get('lang')
        # raise exceptions.UserError("language" + str(language))

        # subtype_id
        subtype_id = self.env.ref('l10n_hu_plus.proforma_send_mail_message_subtype').id

        # Set mail_context
        mail_context = {
            'default_composition_mode': 'comment',
            'default_model': 'account.move',
            'default_res_ids': proforma_self.ids,
            'default_subtype_id': subtype_id,
            'default_template_id': template_id,
            'default_use_template': bool(template_id),
            'force_email': True,
            'l10n_hu_use_proforma': True,
            # 'model_description': self.with_context(lang=language).move_type,
            'model_description': _("Proforma"),
            'proforma': True,
        }

        # Return
        return {
            'context': mail_context,
            'res_model': 'mail.compose.message',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'view_mode': 'form',
        }

    def action_l10n_hu_update_fields(self):
        """ Update HU+ relevant fields """
        # Ensure one record in self
        self.ensure_one()

        # Check
        if self.state != 'draft':
            raise exceptions.UserError(_("Action only allowed for draft invoices!"))

        # Get values
        values_result = self.l10n_hu_get_field_values({})
        if len(values_result.get('error_list')) == 0 and len(values_result.get('field_values')) > 0:
            return self.write(values_result['field_values'])
        elif len(values_result.get('field_values')) == 0:
            return
        else:
            raise exceptions.UserError(str(values_result['error_list']))

    def action_l10n_hu_view_original_invoice(self):
        """ View original invoice """
        # Make sure there is one record in self
        self.ensure_one()

        # Search
        if self.l10n_hu_original_invoice_number:
            if self.move_type in ['in_invoice', 'in_refund']:
                original_invoice = self.env['account.move'].search([
                    ('company_id', '=', self.company_id.id),
                    ('move_type', 'in', ['in_invoice', 'in_refund']),
                    ('ref', 'ilike', self.l10n_hu_original_invoice_number)
                ], limit=1)
            elif self.move_type in ['out_invoice', 'out_refund']:
                original_invoice = self.env['account.move'].search([
                    ('company_id', '=', self.company_id.id),
                    ('move_type', 'in', ['out_invoice', 'out_refund']),
                    ('name', 'ilike', self.l10n_hu_original_invoice_number)
                ], limit=1)
            else:
                original_invoice = None

        # Return
        if original_invoice:
            result = {
                'name': _("HU+ Wizard"),
                'res_id': original_invoice.id,
                'res_model': 'account.move',
                'target': 'current',
                'type': 'ir.actions.act_window',
                'view_mode': 'form,tree',
            }
            return result
        else:
            return

    def action_l10n_hu_view_currency_rate(self):
        """ View currency rates """
        # Make sure there is one record in self
        self.ensure_one()

        # Check
        if self.currency_id and self.currency_id == self.company_id.currency_id:
            raise exceptions.UserError(_("Invoice currency is same as company currency!"))

        # currency_ids
        currency_ids = [self.currency_id.id]
        if self.company_id.currency_id.name != 'HUF':
            currency_ids.append(self.env.ref('base.HUF').id)

        # Return
        result = {
            'name': _("Currency Rates"),
            'context': {'search_default_name': self.delivery_date, 'search_default_currency_id_filter_group_by': 1, 'default_currency_id': self.currency_id.id},
            'domain': [('currency_id', 'in', currency_ids)],
            'res_model': 'res.currency.rate',
            'target': 'current',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
        }
        return result

    def action_l10n_hu_wizard_accounting(self):
        """ Open the HU+ wizard to update accounting fields """
        # Make sure there is one record in self
        self.ensure_one()

        # Check
        if self.state != 'draft':
            raise exceptions.UserError(_("Action only allowed for draft invoices!"))

        # Assemble context
        context = {
            'default_action_type': 'account_move',
            'default_action_type_visible': False,
            'default_account_move_action': 'update_fields',
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

    def action_l10n_hu_wizard_check_status(self):
        """ Open the HU+ wizard to check status for HU+ """
        # Make sure there is one record in self
        self.ensure_one()

        # Get overview
        status_overview = self.l10n_hu_get_plus_status_overview()

        # Assemble context
        context = {
            'default_action_execute_visible': False,
            'default_action_type': 'account_move',
            'default_action_type_visible': False,
            'default_account_move_action': 'check_status',
            'default_account_move_action_visible': False,
            'default_account_move_plus_overview': status_overview,
            'default_account_move_plus_status': self.l10n_hu_plus_status,
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

    def action_l10n_hu_wizard_currency_exchange(self):
        """ Open the HU+ wizard to calculate the document rate """
        # Make sure there is one record in self
        self.ensure_one()

        # Prepare variables
        exchange_amount_from = self.amount_total
        if self.l10n_hu_document_rate != 0.0:
            exchange_rate = self.l10n_hu_document_rate
        else:
            exchange_rate = self.l10n_hu_currency_rate
        if exchange_rate != 0.0:
            exchange_amount_to = exchange_amount_from * exchange_rate
        else:
            exchange_amount_to = 0.0

        # Assemble context
        context = {
            'default_action_type': 'currency_exchange',
            'default_action_type_visible': False,
            'default_exchange_action': 'custom_currency',
            'default_exchange_amount_from': exchange_amount_from,
            'default_exchange_amount_to': exchange_amount_to,
            'default_exchange_currency_from': self.currency_id.id,
            'default_exchange_currency_to': self.company_id.currency_id.id,
            'default_exchange_rate': exchange_rate,
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
    ## REPLACE
    ## NOTES: unfortunately SUPER is not viable, so this complete method replace is necessary
    ##       the issue was in invert_dict(), currency_obj should be the invoice currency, not the company currency
    ##       there is a fix for 18.0 https://github.com/odoo/odoo/commit/62620e705d8c0a5da1e863733b8baa4f5a489b52
    ##       this fix does not work on 17.0
    def _l10n_hu_get_invoice_totals_for_report(self):
        """ In Hungary, tax amounts should appear negative on credit notes.
            We therefore apply a post-processing to the tax totals to make them negative. """

        def invert_dict(dictionary, keys_to_invert):
            """ Replace the values of keys_to_invert by their negative. """
            dictionary.update({
                key: -value
                for key, value in dictionary.items() if key in keys_to_invert
            })
            keys_to_reformat = {f'formatted_{x}': x for x in keys_to_invert}
            dictionary.update({
                key: formatLang(self.env, dictionary[keys_to_reformat[key]], currency_obj=self.currency_id)
                for key, value in dictionary.items() if key in keys_to_reformat
            })

        self.ensure_one()

        tax_totals = self.tax_totals
        if not isinstance(tax_totals, dict):
            return tax_totals

        tax_totals['display_tax_base'] = True

        if 'refund' in self.move_type:
            invert_dict(tax_totals, ['amount_total', 'amount_untaxed', 'rounding_amount', 'amount_total_rounded'])

            for subtotal in tax_totals['subtotals']:
                invert_dict(subtotal, ['amount'])

            for tax_list in tax_totals['groups_by_subtotal'].values():
                for tax in tax_list:
                    keys_to_invert = ['tax_group_amount', 'tax_group_base_amount',
                                      'tax_group_amount_company_currency', 'tax_group_base_amount_company_currency']
                    invert_dict(tax, keys_to_invert)

        currency_huf = self.env.ref('base.HUF')
        currency_rate = self._l10n_hu_get_currency_rate()

        tax_totals['total_vat_amount_in_huf'] = sum(
            -line.balance if self.company_id.currency_id == currency_huf else currency_huf.round(
                -line.amount_currency * currency_rate)
            for line in self.line_ids.filtered(lambda l: l.tax_line_id.l10n_hu_tax_type)
        )

        tax_totals['formatted_total_vat_amount_in_huf'] = formatLang(
            self.env, tax_totals['total_vat_amount_in_huf'], currency_obj=currency_huf
        )

        return tax_totals

    ## REPLACE
    ## NOTES: unfortunately SUPER is not viable, so this complete method replace is necessary to support STORNO
    def _l10n_hu_edi_upload_single_batch(self, connection):
        try:
            token_result = connection.do_token_exchange(self.company_id.sudo()._l10n_hu_edi_get_credentials_dict())
        except L10nHuEdiConnectionError as e:
            return self.write({
                'l10n_hu_edi_state': 'rejected',
                'l10n_hu_edi_transaction_code': False,
                'l10n_hu_edi_messages': {
                    'error_title': _('Could not authenticate with NAV. Check your credentials and try again.'),
                    'errors': e.errors,
                    'blocking_level': 'error',
                },
            })

        for i, invoice in enumerate(self, start=1):
            invoice.l10n_hu_edi_batch_upload_index = i

        ## L10NHU_PLUS BEGIN
        operation = 'CREATE' if invoice._l10n_hu_get_chain_base() == invoice else 'MODIFY'
        if invoice.l10n_hu_document_type and invoice.l10n_hu_document_type.technical_name == 'invoice_storno':
            operation = 'STORNO'
        ## L10NHU_PLUS END

        invoice_operations = [
            {
                'index': invoice.l10n_hu_edi_batch_upload_index,
                'operation': operation,  # NOTES: moved to variable
                'invoice_data': base64.b64decode(invoice.l10n_hu_edi_attachment),
            }
            for invoice in self
        ]

        self.write({'l10n_hu_edi_send_time': fields.Datetime.now()})

        try:
            transaction_code = connection.do_manage_invoice(
                self.company_id.sudo()._l10n_hu_edi_get_credentials_dict(),
                token_result['token'],
                invoice_operations,
            )
        except L10nHuEdiConnectionError as e:
            if e.code == 'timeout':
                return self.write({
                    'l10n_hu_edi_state': 'send_timeout',
                    'l10n_hu_edi_transaction_code': False,
                    'l10n_hu_edi_messages': {
                        'error_title': _(
                            'Invoice submission timed out. Please wait at least 6 minutes, then update the status.'),
                        'errors': e.errors,
                        'blocking_level': 'warning',
                    },
                })
            return self.write({
                'l10n_hu_edi_state': 'rejected',
                'l10n_hu_edi_transaction_code': False,
                'l10n_hu_invoice_chain_index': 0,
                'l10n_hu_edi_messages': {
                    'error_title': _('Invoice submission failed.'),
                    'errors': e.errors,
                    'blocking_level': 'error',
                },
            })

        self.write({
            'l10n_hu_edi_state': 'sent',
            'l10n_hu_edi_transaction_code': transaction_code,
            'l10n_hu_edi_messages': {
                'error_title': _('Invoice submitted, waiting for response.'),
                'errors': [],
            }
        })

    ## SUPER
    def _get_report_base_filename(self) -> str:
        """ Get the filename for proforma"""
        if self.state == 'draft' and self.l10n_hu_proforma_name:
            return str(self.company_id.vat) + "_" + str(self.l10n_hu_proforma_name).replace('/', '_')
        else:
            return super()._get_report_base_filename()

    def _l10n_hu_edi_get_invoice_values(self):
        """ Super for original method in l10n_hu_edi app

        NOTES:
        - super result is a dictionary containing invoice_values
        - we update the dictionary with some values
        - for xml rendering see file: data/template_invoice_xml.data

        """
        # Execute super
        result = super(L10nHuPlusAccountMove, self)._l10n_hu_edi_get_invoice_values()

        # accounting_delivery_date
        if self.l10n_hu_delivery_period_start and self.l10n_hu_delivery_period_end:
            accounting_delivery_date = self.l10n_hu_delivery_period_end
        elif self.delivery_date:
            accounting_delivery_date = self.delivery_date
        elif self.date:
            accounting_delivery_date = self.date
        else:
            accounting_delivery_date = None

        # periodical_settlement
        if self.l10n_hu_delivery_period_start and self.l10n_hu_delivery_period_end:
            periodical_settlement = True
        else:
            periodical_settlement = False

        # Update result
        result.update({
            'invoiceAccountingDeliveryDate': accounting_delivery_date,
            'invoiceDeliveryPeriodEnd': self.l10n_hu_delivery_period_end,
            'invoiceDeliveryPeriodStart': self.l10n_hu_delivery_period_start,
            'periodicalSettlement': periodical_settlement
        })

        # Customer tax number
        ## NOTES: temporary workaround until Odoo S.A. fix, see https://github.com/hungarodo/odoohu-plus/issues/31
        customer = result.get('customer', None)
        if customer \
                and customer.is_company \
                and customer.vat \
                and customer.country_code != 'HU' \
                and self.fiscal_position_id \
                and self.fiscal_position_id.l10n_hu_vat_status == 'domestic':
            result.update({
                'customer_vat_data': {
                    'tax_number': customer.l10n_hu_group_vat or customer.vat,
                    'group_member_tax_number': customer.l10n_hu_group_vat and customer.vat,
                },
                'customerVatStatus': 'DOMESTIC'
            })

        # Return result
        return result

    def _l10n_hu_edi_get_valid_actions(self):
        """ Super for original method in l10n_hu_edi app

        NOTES:
        - super result is a list containing possible HU EDI actions
        - we empty the list in case EDI is disabled on the journal
        """
        # Execute super
        result = super(L10nHuPlusAccountMove, self)._l10n_hu_edi_get_valid_actions()

        # No action when EDI is disabled on the journal (eg: externally issued invoices, OSS)
        if self.country_code == 'HU' and self.is_sale_document() and self.state == 'posted' \
                and self.journal_id and self.journal_id.l10n_hu_edi_send_disabled:
            result = []
        return result

    ## HU+
    @api.model
    def l10n_hu_get_cash_accounting(self):
        """ Use cash accounting for this invoice or not

        :return: boolean
        """
        # Initialize variables
        result = False

        # Set result
        if self.is_invoice(True) and self.state == 'draft':
            if self.move_type in ['in_invoice', 'in_refund'] \
                    and self.partner_id \
                    and self.partner_id.property_account_position_id \
                    and self.partner_id.property_account_position_id.l10n_hu_trade_position == 'domestic' \
                    and self.partner_id.property_account_position_id.l10n_hu_tax_regime == 'ca':
                result = True
            elif self.move_type in ['out_invoice', 'out_refund'] \
                    and self.partner_id \
                    and self.partner_id.property_account_position_id \
                    and self.partner_id.property_account_position_id.l10n_hu_trade_position == 'domestic' \
                    and self.company_id.l10n_hu_tax_regime == 'ca':
                result = True
            else:
                pass
        else:
            pass

        # Return result
        return result

    @api.model
    def l10n_hu_get_delivery_date_default(self, values):
        """ Get delivery date default

        :param values: dictionary

        :return date or False
        """
        # Initialize variables
        journal = values.get('journal', None)
        if not journal and not self.journal_id:
            return False
        elif not journal and self.journal_id:
            journal = self.journal_id
        else:
            pass

        # Get journal setting
        journal_setting = journal.l10n_hu_delivery_date_default

        # Process options
        if journal_setting == 'none':
            result = False
        elif journal_setting == 'today':
            result = fields.Date.today()
        elif journal_setting == 'first_day_of_this_month':
            # Get today
            today = datetime.date.today()

            # Replace day to first day of this month
            result = today.replace(day=1)
        elif journal_setting == 'last_day_of_this_month':
            # Get today
            today = datetime.date.today()

            # Get close to the end of this month and add 4 days to 'roll it over'
            next_month = today.replace(day=28) + datetime.timedelta(days=4)

            # Set the day to 1 gives us the start of next month
            first_day_of_next_month = next_month.replace(day=1)

            # Remove one day to get last day of this month
            result = first_day_of_next_month - datetime.timedelta(days=1)
        elif journal_setting == 'last_day_of_last_month':
            # Get today
            today = datetime.date.today()

            # Replace day to first day of this month
            first_day_of_this_month = today.replace(day=1)

            # Remove one day to get last day of last month
            result = first_day_of_this_month - datetime.timedelta(days=1)
        elif journal_setting == 'first_day_of_next_month':
            # Get today
            today = datetime.date.today()

            # Get close to the end of this month and add 4 days to 'roll it over'
            next_month = today.replace(day=28) + datetime.timedelta(days=4)

            # Set the day to 1 gives us the first day of next month
            result = next_month.replace(day=1)
        else:
            result = False

        # Return result
        return result

    @api.model
    def l10n_hu_get_delivery_period_data(self, values):
        """ Get delivery period data

        NOTES:
        - This method computes special hungarian rules
        - Specification: 2007. CXXVII. 58.§ (1)
        - NJT: https://njt.hu/jogszabaly/2007-127-00-00

        :param values: dictionary

        :return: dictionary
        """
        # raise exceptions.UserError("l10n_hu_get_delivery_period_data BEGIN" + str(values))

        # Initialize variables
        debug_list = []
        error_list = []
        info_list = []
        period_legal = ""
        period_summary = ""
        result = {}
        warning_list = []

        # Set journal
        if values.get('journal_id'):
            journal = self.env['account.journal'].sudo().browse(values['journal_id'])
        elif values.get('journal'):
            journal = values['journal']
        elif len(self) == 1 and self.id and self.journal_id:
            journal = self.journal_id
        else:
            journal = None
            error_list.append("journal not set")

        # Is hungarian company
        if journal and journal.company_id.partner_id.country_id.code == 'HU':
            is_hungarian_company = True
        else:
            is_hungarian_company = False

        # Is invoice journal
        if journal and journal.type in ['purchase', 'sale']:
            is_invoice_journal = True
        else:
            is_invoice_journal = False

        # Period start and end
        if values.get('period_start'):
            period_start = values['period_start']
            if isinstance(period_start, datetime.date):
                pass
            elif isinstance(period_start, str):
                try:
                    date_string = period_start
                    date_format = "%Y-%m-%d"
                    period_start = datetime.datetime.strptime(date_string, date_format).date()
                except:
                    period_start = False
            else:
                period_start = False
        elif self.l10n_hu_delivery_period_start:
            period_start = self.l10n_hu_delivery_period_start
        else:
            period_start = None

        if values.get('period_end'):
            period_end = values['period_end']
            if isinstance(period_end, datetime.date):
                pass
            elif isinstance(period_end, str):
                try:
                    date_string = period_end
                    date_format = "%Y-%m-%d"
                    period_end = datetime.datetime.strptime(date_string, date_format).date()
                except:
                    period_end = False
            else:
                period_end = False
        elif self.l10n_hu_delivery_period_end:
            period_end = self.l10n_hu_delivery_period_end
        else:
            period_end = False

        # is_periodic_settlement
        if is_invoice_journal and period_start and period_end:
            is_periodic_settlement = True
        else:
            is_periodic_settlement = False

        # Default delivery date
        delivery_date_default = self.l10n_hu_get_delivery_date_default({})

        # Set today
        date_today = fields.Date.today()

        # Set invoice date
        if values.get('invoice_date'):
            invoice_date = values['invoice_date']
            if isinstance(invoice_date, datetime.date):
                pass
            elif isinstance(invoice_date, str):
                try:
                    date_string = invoice_date
                    date_format = "%Y-%m-%d"
                    invoice_date = datetime.datetime.strptime(date_string, date_format).date()
                except:
                    invoice_date = None
            else:
                invoice_date = False
        elif self.invoice_date:
            invoice_date = self.invoice_date
        elif self.state == 'draft':
            invoice_date = date_today
        else:
            invoice_date = False

        # Set invoice due date
        if values.get('invoice_date_due'):
            invoice_date_due = values['invoice_date_due']
            if isinstance(invoice_date_due, datetime.date):
                pass
            elif isinstance(invoice_date_due, str):
                try:
                    date_string = invoice_date_due
                    date_format = "%Y-%m-%d"
                    invoice_date_due = datetime.datetime.strptime(date_string, date_format).date()
                except:
                    invoice_date_due = False
            else:
                invoice_date_due = False
        elif self.invoice_payment_term_id:
            # NOTES: using a payment term needs a recompute, see _compute_invoice_date_due()
            context_today = fields.Date.context_today(self)
            invoice_date_due = self.needed_terms and max(
                (k['date_maturity'] for k in self.needed_terms.keys() if k),
                default=False,
            ) or self.invoice_date_due or context_today
        elif self.invoice_date_due:
            invoice_date_due = self.invoice_date_due
        else:
            invoice_date_due = False

        # Set last day of delivery period month
        if period_end:
            # Get close to the end of the month and add 4 days to 'roll it over'
            period_next_month = period_end.replace(day=28) + datetime.timedelta(days=4)

            # Set the day to 1 gives us the start of next month
            period_first_day_of_next_month = period_next_month.replace(day=1)

            # Remove one day to get last day of this month
            period_month_last_day = period_first_day_of_next_month - datetime.timedelta(days=1)
        else:
            period_month_last_day = False

        # Set 60 days from period_end
        if period_end:
            period_end_plus_60 = period_end + datetime.timedelta(days=60)
        else:
            period_end_plus_60 = False

        # NAV SCENARIOS
        # 0) DEFAULT
        if delivery_date_default:
            scenario = '0_default'
            delivery_date = delivery_date_default
        else:
            scenario = '0_no_default'
            delivery_date = False

        # 1) PERIOD END
        # Rule: period_end is set
        # Value: delivery_period_end
        if period_end:
            scenario = '1_period_end'
            delivery_date = period_end

        # 2) INVOICE DATE
        # Rule: BOTH invoice_date_due AND invoice_date are BEFORE period_end
        # Value: invoice_date
        if invoice_date and invoice_date_due and period_end  \
                and invoice_date_due < period_end \
                and invoice_date < period_end:
            scenario = '1a_invoice_date'
            delivery_date = invoice_date

        # 3) INVOICE DATE DUE (MAX 60)
        # Rule: invoice_date_due is AFTER period_end
        # Value: invoice_date_due (BUT max 60 days from period_end)
        if invoice_date_due and period_end \
                and invoice_date_due > period_end:
            if invoice_date_due <= period_end_plus_60:
                scenario = '1b_invoice_date_due'
                delivery_date = invoice_date_due
            else:
                scenario = '1b_invoice_date_due_max_60'
                delivery_date = period_end_plus_60

        # Period text
        if is_hungarian_company and is_periodic_settlement:
            # period_summary
            period_summary += _("Delivery period") + ": "
            period_summary += str(period_start) + " - " + str(period_end)

            # period_legal
            period_legal = "2007. CXXVII. 58.§"
            if scenario == '1a_invoice_date':
                period_legal += " (1) a)"
            elif scenario == '1b_invoice_date_due':
                period_legal += " (1) b)"
            elif scenario == '1b_invoice_date_due_max_60':
                period_legal += " (1) b) 60+ " + _("day")
            else:
                pass

        # Update result
        result.update({
            'debug_list': debug_list,
            'delivery_date': delivery_date,
            'error_list': error_list,
            'info_list': info_list,
            'invoice_date': invoice_date,
            'invoice_date_due': invoice_date_due,
            'is_periodic_settlement': is_periodic_settlement,
            'period_end': period_end,
            'period_end_plus_60': period_end_plus_60,
            'period_legal': period_legal,
            'period_month_last_day': period_month_last_day,
            'period_start': period_start,
            'period_summary': period_summary,
            'scenario': scenario,
            'warning_list': warning_list,
        })

        # Return result
        # raise exceptions.UserError("l10n_hu_get_delivery_period_data" + "\n" + str(result))
        return result

    @api.model
    def l10n_hu_get_field_values(self, values):
        """ Get field values for HU accounting

        NOTES:
        - This method takes care of special hungarian fields

        :param values: dictionary

        :return: dictionary
        """
        # raise exceptions.UserError("l10n_hu_get_field_values BEGIN" + str(values))

        # Initialize variables
        debug_list = []
        error_list = []
        field_values = {}
        info_list = []
        result = {}
        warning_list = []

        # HU+ enabled
        if self.journal_id and self.journal_id.l10n_hu_plus_enabled:
            debug_list.append("HU+ enabled journal check passed")
        else:
            error_list.append("HU+ enabled journal check failed")

        # Check move type
        if len(self) == 1 and self.id and self.move_type in ['in_invoice', 'in_refund', 'out_invoice', 'out_refund']:
            debug_list.append("move type check passed")
        else:
            error_list.append("invalid account move type")

        # Check state
        if self.state == 'draft':
            debug_list.append("state check passed")
        else:
            error_list.append("invalid state, only draft is allowed")

        # currency_huf
        currency_huf = self.env.ref('base.HUF')

        # Get last_accounting_rate
        ## Company ccy != invoice ccy
        if self.delivery_date and self.currency_id != self.company_currency_id:
            last_accounting_rate = self.env['res.currency.rate'].search([
                ('company_id', '=', self.company_id.id),
                ('currency_id', '=', self.currency_id.id),
                ('name', '<=', self.delivery_date)
            ], limit=1)
            if last_accounting_rate:
                debug_list.append("last_accounting_rate found")
            else:
                error_list.append("last_accounting_rate not found")
        else:
            last_accounting_rate = None
            debug_list.append("last_accounting_rate skipped")

        # Get last_huf_rate
        ## Company HUF AND invoice HUF
        if self.company_currency_id.name == 'HUF' and self.currency_id.name == 'HUF':
            last_huf_rate = None
        ## Company HUF and invoice NOT HUF
        elif self.delivery_date and self.company_currency_id.name == 'HUF' and self.currency_id.name != 'HUF':
            last_huf_rate = self.env['res.currency.rate'].search([
                ('company_id', '=', self.company_id.id),
                ('currency_id', '=', self.currency_id.id),
                ('name', '<=', self.delivery_date)
            ], limit=1)
            if last_huf_rate:
                debug_list.append("last_huf_rate found")
            else:
                error_list.append("last_huf_rate not found for company HUF and invoice NOT HUF")
        ## Company NOT HUF
        elif self.delivery_date and self.company_currency_id.name != 'HUF':
            last_huf_rate = self.env['res.currency.rate'].search([
                ('company_id', '=', self.company_id.id),
                ('currency_id', '=', currency_huf.id),
                ('name', '<=', self.delivery_date)
            ], limit=1)
            if last_huf_rate:
                debug_list.append("last_huf_rate found for company NOT HUF")
            else:
                error_list.append("last_huf_rate not found")
        else:
            last_huf_rate = None
            debug_list.append("last_huf_rate else scenario, probably date not set")

        # Process field values
        if len(error_list) == 0:
            # date
            if values.get('date') and self.state == 'draft':
                field_values.update({'date': values['date']})
                debug_list.append("date set from values: " + str(values['date']))
            else:
                pass

            # delivery_period, delivery_date
            if values.get('delivery_period_start'):
                delivery_period_start = values['delivery_period_start']
            elif self.l10n_hu_delivery_period_start:
                delivery_period_start = self.l10n_hu_delivery_period_start
            else:
                delivery_period_start = None
            if values.get('delivery_period_end'):
                delivery_period_end = values['delivery_period_end']
            elif self.l10n_hu_delivery_period_end:
                delivery_period_end = self.l10n_hu_delivery_period_end
            else:
                delivery_period_end = None

            ## automation only for outgoing invoices
            if delivery_period_start and delivery_period_end and self.move_type in ['out_invoice', 'out_refund']:
                delivery_period_result = self.l10n_hu_get_delivery_period_data({
                    'period_end': delivery_period_end,
                    'period_start': delivery_period_start,
                })
                delivery_date = delivery_period_result.get('delivery_date', None)
            ## manual for any invoice
            elif values.get('delivery_date'):
                delivery_date = values['delivery_date']
                debug_list.append("delivery_date set from values: " + str(values['delivery_date']))
            else:
                delivery_date = self.delivery_date
            field_values.update({'delivery_date': delivery_date})
            field_values.update({'l10n_hu_delivery_period_end': delivery_period_end})
            field_values.update({'l10n_hu_delivery_period_start': delivery_period_start})

            # invoice_origin
            if values.get('invoice_origin') and len(values['invoice_origin']) > 0:
                field_values.update({'invoice_origin': values['invoice_origin']})
                debug_list.append("invoice_origin set from values: " + str(values['invoice_origin']))
            else:
                pass

            # l10n_hu_cash_accounting
            if values.get('l10n_hu_cash_accounting') is not None:
                field_values.update({'l10n_hu_cash_accounting': values['l10n_hu_cash_accounting']})
                debug_list.append("l10n_hu_cash_accounting set from values: " + str(values['l10n_hu_cash_accounting']))
            else:
                pass

            # l10n_hu_document_rate
            if values.get('l10n_hu_document_rate') and self.move_type in ['in_invoice', 'in_refund']:
                field_values.update({'l10n_hu_document_rate': values['l10n_hu_document_rate']})
                debug_list.append("l10n_hu_document_rate set from values: " + str(values['l10n_hu_document_rate']))
            elif self.currency_id == self.company_currency_id and self.l10n_hu_document_rate != 1.0:
                field_values.update({'l10n_hu_document_rate': 1.0})
                debug_list.append("l10n_hu_document_rate set to 1.0")
            elif self.l10n_hu_document_rate in [0, 1] and last_accounting_rate:
                l10n_hu_document_rate = last_accounting_rate.inverse_company_rate
                field_values.update({'l10n_hu_document_rate': l10n_hu_document_rate})
                debug_list.append("l10n_hu_document_rate set from last accounting rate: " + str(l10n_hu_document_rate))
            else:
                debug_list.append("l10n_hu_document_rate passed")

            # l10n_hu_document_type
            if values.get('l10n_hu_document_type'):
                field_values.update({'l10n_hu_document_type': values['l10n_hu_document_type'].id})
            elif not self.l10n_hu_document_type:
                l10n_hu_document_type = self.journal_id.l10n_hu_get_default_document_type()
                if l10n_hu_document_type:
                    field_values.update({'l10n_hu_document_type': l10n_hu_document_type.id})
                else:
                    pass
            else:
                pass

            # l10n_hu_huf_rate
            if self.company_currency_id.name != 'HUF' and values.get('l10n_hu_huf_rate'):
                field_values.update({'l10n_hu_huf_rate': values['l10n_hu_huf_rate']})
                debug_list.append("l10n_hu_huf_rate set from values: " + str(values['l10n_hu_huf_rate']))
            elif last_huf_rate:
                l10n_hu_last_huf_rate = last_huf_rate.company_rate
                field_values.update({'l10n_hu_huf_rate': l10n_hu_last_huf_rate})
                debug_list.append("l10n_hu_huf_rate set last_huf_rate: " + str(l10n_hu_last_huf_rate))
            else:
                field_values.update({'l10n_hu_huf_rate': 1.0})

            # l10n_hu_payment_mode
            if values.get('l10n_hu_payment_mode'):
                field_values.update({'l10n_hu_payment_mode': values['l10n_hu_payment_mode']})
                debug_list.append("l10n_hu_payment_mode set from values: " + str(values['l10n_hu_payment_mode']))
            elif not self.l10n_hu_payment_mode \
                    and self.invoice_payment_term_id \
                    and self.invoice_payment_term_id.l10n_hu_nav_method:
                l10n_hu_payment_mode_2 = self.invoice_payment_term_id.l10n_hu_nav_method
                field_values.update({'l10n_hu_payment_mode': l10n_hu_payment_mode_2})
                debug_list.append("l10n_hu_payment_mode set from payment term: " + str(l10n_hu_payment_mode_2))
            elif not self.l10n_hu_payment_mode and self.journal_id.l10n_hu_nav_payment_method:
                l10n_hu_payment_mode_3 = self.journal_id.l10n_hu_nav_payment_method
                field_values.update({'l10n_hu_payment_mode': l10n_hu_payment_mode_3})
                debug_list.append("l10n_hu_payment_mode set from journal: " + str(l10n_hu_payment_mode_3))
            else:
                pass

            # l10n_hu_vat_date
            if values.get('l10n_hu_vat_date') is not None:
                field_values.update({'l10n_hu_vat_date': values['l10n_hu_vat_date']})
                debug_list.append("l10n_hu_vat_date set from values: " + str(values['l10n_hu_vat_date']))
            else:
                pass
        else:
            debug_list.append("processing skipped due to previous errors")

        # Update result
        result.update({
            'debug_list': debug_list,
            'error_list': error_list,
            'field_values': field_values,
            'info_list': info_list,
            'warning_list': warning_list,
        })

        # Return result
        # raise exceptions.UserError("l10n_hu_get_field_values END" + str(result))
        return result

    @api.model
    def l10n_hu_get_plus_status_checklist(self):
        """ Get HU+ status checklist

        NOTES:
        - we run here a lot of status checks
        - Odoo _l10n_hu_edi_check_invoices() method is not included as it returns only errors when posting

        :return: dictionary
        """
        # Initialize variables
        debug_list = []
        error_list = []
        info_list = []
        result = {}
        success_list = []
        warning_list = []

        # Odoo errors (actually, no need to include, it returns only errors for invoice issue)
        """
        l10n_hu_edi_error_dict = self._l10n_hu_edi_check_invoices()
        for check, values in l10n_hu_edi_error_dict.items():
            l10n_hu_edi_error = {
                'action_text': values.get('action_text', ""),
                'code': check,
                'description': values.get('message', ""),
                'records': values.get('records', None),
                'result': 'error'
            }
            error_list.append(l10n_hu_edi_error)
        """

        # HU+1: document type
        if self.l10n_hu_document_type:
            success_list.append({
                'action_text': None,
                'code': 'HU+1',
                'description': _("Document type set") + ": " + str(self.l10n_hu_document_type.display_name),
                'records': self.l10n_hu_document_type,
                'result': 'ok',
            })
        else:
            warning_list.append({
                'action_text': None,
                'code': 'HU+1',
                'description': _("Document type not set"),
                'records': None,
                'result': 'warning',
            })

        # HU+2: account move fiscal position
        if self.fiscal_position_id:
            success_list.append({
                'action_text': None,
                'code': 'HU+2',
                'description': _("Invoice fiscal position set") + ": " + str(self.fiscal_position_id.display_name),
                'records': self.filtered(lambda am: am.fiscal_position_id),
                'result': 'ok',
            })
        else:
            warning_list.append({
                'action_text': None,
                'code': 'HU+2',
                'description': _("Invoice fiscal position not set"),
                'records': self.filtered(lambda am: not am.fiscal_position_id),
                'result': 'warning',
            })

        # HU+3: partner fiscal position
        if self.partner_id.property_account_position_id:
            success_list.append({
                'action_text': None,
                'code': 'HU+3',
                'description': _("Partner fiscal position set") + ": " + self.partner_id.property_account_position_id.display_name,
                'records': self.partner_id.commercial_partner_id.filtered(lambda p: p.property_account_position_id),
                'result': 'ok',
            })
        else:
            warning_list.append({
                'action_text': None,
                'code': 'HU+3',
                'description': _("Partner fiscal position not set"),
                'records': self.partner_id.commercial_partner_id.filtered(lambda p: not p.property_account_position_id),
                'result': 'warning',
            })

        # HU+4: delivery date
        if self.delivery_date:
            success_list.append({
                'action_text': None,
                'code': 'HU+4',
                'description': _("Delivery date set") + ": " + str(self.delivery_date),
                'records': self,
                'result': 'ok',
            })
        else:
            error_list.append({
                'action_text': None,
                'code': 'HU+4',
                'description': _("Delivery date not set"),
                'records': self,
                'result': 'error',
            })

        # HU+5: delivery period
        hu_5_description = str(self.l10n_hu_delivery_period_start)
        hu_5_description += " - "
        hu_5_description += str(self.l10n_hu_delivery_period_end)
        if self.l10n_hu_delivery_period_start and self.l10n_hu_delivery_period_end:
            ## for outgoing invoices
            if self.move_type in ['out_invoice', 'out_refund']:
                hu_5_description += " (" + self.l10n_hu_delivery_period_legal + ")"
            success_list.append({
                'action_text': None,
                'code': 'HU+5',
                'description': _("Delivery period set") + ": " + hu_5_description,
                'records': self,
                'result': 'info',
            })
        elif self.l10n_hu_delivery_period_start and not self.l10n_hu_delivery_period_end:
            error_list.append({
                'action_text': None,
                'code': 'HU+5',
                'description': _("Delivery period not set") + ": " + hu_5_description,
                'records': self,
                'result': 'error',
            })
        elif not self.l10n_hu_delivery_period_start and self.l10n_hu_delivery_period_end:
            error_list.append({
                'action_text': None,
                'code': 'HU+5',
                'description': _("Delivery period not set") + ": " + hu_5_description,
                'records': self,
                'result': 'error',
            })
        else:
            info_list.append({
                'action_text': None,
                'code': 'HU+5',
                'description': _("Delivery period not set"),
                'records': self,
                'result': 'info',
            })

        # Update result
        result.update({
            'debug_list': debug_list,
            'error_list': error_list,
            'info_list': info_list,
            'success_list': success_list,
            'warning_list': warning_list,
        })

        # Return result
        return result

    @api.model
    def l10n_hu_get_plus_status_overview(self):
        """ Get HU+ status overview as an HTML table

        NOTES:
        - we return status check results
        - we also return an overview html table assembled by a different method

        """
        # Initialize variables
        result = ""

        # Run status check
        checklist_result = self.l10n_hu_get_plus_status_checklist()
        error_list = checklist_result.get('error_list', [])
        info_list = checklist_result.get('info_list', [])
        success_list = checklist_result.get('success_list', [])
        warning_list = checklist_result.get('warning_list', [])

        # Counts
        error_count = len(error_list)
        info_count = len(info_list)
        success_count = len(success_list)
        warning_count = len(warning_list)
        total_count = error_count + info_count + success_count + warning_count
        if total_count > 0:
            error_rate = error_count / total_count
            info_rate = info_count / total_count
            success_rate = success_count / total_count
            warning_rate = warning_count / total_count
            bad_count = error_count + (warning_count * 0.5)
            health_rate = int(round(((total_count - bad_count) / total_count * 100), 0))
        else:
            error_rate = 0
            info_rate = 0
            success_rate = 0
            warning_rate = 0
            health_rate = 0

        # Assemble table
        ### TITLE
        result += '<h2 class="text-center mt-4">'
        result += str(self.display_name)
        result += '</h2>'
        ### SUBTITLE
        result += '<div class="fw-bold text-center mb-2">'
        result += _("HU+ check result")
        result += " " + str(fields.Datetime.now())
        result += " " + str(health_rate) + "%"
        result += '</div>'
        ### STATS
        result += '<div class="row p-1 mt-2 mb-2">'  # div row BEGIN
        result += '<div class="col-3 text-center text-uppercase text-danger">'
        result += '<span class="fa fa-exclamation-circle text-danger pe-1"/>'
        result += '<span class="fw-bold">' + _("Error") + ": " + str(error_count) + '</span>'
        # result += '<span class="fst-italic text-muted">' + str(error_rate) + '</span>'
        result += '</div>'
        result += '<div class="col-3 text-center text-uppercase text-warning">'
        result += '<span class="fa fa-exclamation-triangle text-warning pe-1"/>'
        result += '<span class="fw-bold">' + _("Warning") + ": " + str(warning_count) + '</span>'
        # result += '<span class="fst-italic ps-1 text-muted">' + str(warning_rate) + '</span>'
        result += '</div>'
        result += '<div class="col-3 text-center text-uppercase text-success">'
        result += '<span class="fa fa-check text-success pe-1"/>'
        result += '<span class="fw-bold">' + _("Success") + ": " + str(success_count) + '</span>'
        # result += '<span class="fst-italic ps-1 text-muted">' + str(success_rate) + '</span>'
        result += '</div>'
        result += '<div class="col-3 text-center text-uppercase text-info">'
        result += '<span class="fa fa-info-circle text-info pe-1"/>'
        result += '<span class="fw-bold">' + _("Information") + ": " + str(info_count) + '</span>'
        # result += '<span class="fst-italic ps-1 text-muted">' + str(info_rate) + '</span>'
        result += '</div>'
        result += '</div>'  # div row END
        ## TABLE BEGIN
        result += '<table class="table table-bordered table-sm" style="width:100%;">'
        ## THEAD BEGIN
        result += '<thead>'
        ### TH COLUMN NAMES
        result += '<tr>'
        result += '<th class="text-center" style="width:10%;">'
        result += _("Result")  # Result (eg: error, info, ok, other, warning)
        result += '</th>'
        result += '<th class="text-center" style="width:10%;">'
        result += _("Code")  # Code
        result += '</th>'
        result += '<th class="text-center" style="width:80%;">'
        result += _("Description")  # Description
        result += '</th>'
        result += '</tr>'
        ## THEAD END
        result += '</thead>'
        ## TBODY BEGIN
        result += '<tbody>'
        ### 1) errors
        for error_item in error_list:
            result += '<tr>'
            result += '<td class="text-center">'
            result += '<span class="fa fa-exclamation-circle text-danger me-2"/>'
            result += '</td>'
            result += '<td>'
            result += error_item.get('code', "-")
            result += '</td>'
            result += '<td>'
            result += error_item.get('description', "-")
            result += '</td>'
            result += '<tr>'
        ### 2) warnings
        for warning_item in warning_list:
            result += '<tr>'
            result += '<td class="text-center">'
            result += '<span class="fa fa-exclamation-triangle text-warning me-2"/>'
            result += '</td>'
            result += '<td>'
            result += warning_item.get('code', "-")
            result += '</td>'
            result += '<td>'
            result += warning_item.get('description', "-")
            result += '</td>'
            result += '<tr>'
        ### 3) success
        for success_item in success_list:
            result += '<tr>'
            result += '<td class="text-center">'
            result += '<span class="fa fa-check text-success me-2"/>'
            result += '</td>'
            result += '<td>'
            result += success_item.get('code', "-")
            result += '</td>'
            result += '<td>'
            result += success_item.get('description', "-")
            result += '</td>'
            result += '<tr>'
        ### 4) info
        for info_item in info_list:
            result += '<tr>'
            result += '<td class="text-center">'
            result += '<span class="fa fa-info-circle text-info me-2"/>'
            result += '</td>'
            result += '<td>'
            result += info_item.get('code', "-")
            result += '</td>'
            result += '<td>'
            result += info_item.get('description', "-")
            result += '</td>'
            result += '<tr>'
        ## TBODY END
        result += '</tbody>'
        ## TABLE END
        result += '</table>'

        # Return result
        return result

    @api.model
    def l10n_hu_get_storno_allowed(self):
        """ Determine if storno is allowed for an account move

        NOTES:
        - in certain cases (eg: issued to wrong partner) storno must be used instead of modification
        - we collect points, if all collected, storno is allowed

        :return: boolean
        """
        # Initialize variables
        points = 0

        # document type available
        storno_document_type = self.env['l10n.hu.plus.tag'].search([
            ('company', '=', self.company_id.id),
            ('tag_type', '=', 'document_type'),
            ('technical_name', '=', 'invoice_storno'),
        ], limit=1)
        if storno_document_type:
            points += 1

        # posted out_invoice
        if self.move_type == 'out_invoice' and self.state == 'posted':
            points += 1

        # nav configured for the company
        if self.company_id.l10n_hu_edi_server_mode:
            points += 1

        # Determine points
        if points == 3:
            return True
        else:
            return False
