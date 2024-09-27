# -*- coding: utf-8 -*-
# 1 : imports of python lib
import datetime
from typing import Dict, List

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 : imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuPlusAccountMove(models.Model):
    # Private attributes
    _inherit = 'account.move'

    # Default methods
    
    # Field declarations
    # # CASH ACCOUNTING
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
    # # CURRENCY
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
        string="HU Document Rate",
    )
    l10n_hu_rate_difference = fields.Float(
        compute='_compute_l10n_hu_rate_difference',
        string="HU Rate Difference",
    )
    # # DELIVERY PERIOD
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
    # # DOCUMENT TYPE
    l10n_hu_document_type = fields.Many2one(
        comodel_name='l10n.hu.plus.object',
        domain=[('type_technical_name', '=', 'document_type')],
        index=True,
        string="HU Document Type",
        tracking=True,
    )
    # # JOURNAL
    l10n_hu_journal_type = fields.Selection(
        related='journal_id.type',
        string="HU Journal Type",
    )
    # # ORIGINAL
    l10n_hu_original_account_move = fields.Many2one(
        comodel_name='account.move',
        compute='_compute_l10n_hu_original_account_move',
        copy=False,
        index=True,
        readonly=False,
        store=True,
        string="HU Original Account Move",
        tracking=True,
    )
    l10n_hu_original_invoice_number = fields.Char(
        copy=False,
        string="HU Original Invoice Number",
        tracking=True,
    )
    # # PARTNER
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
    # # VAT
    l10n_hu_vat_date = fields.Date(
        copy=False,
        index=True,
        string="HU VAT Date",
        tracking=True,
    )

    # Compute and search fields, in the same order of field declarations
    # # SUPER
    @api.depends('country_code', 'move_type')
    def _compute_show_delivery_date(self):
        # EXTENDS 'account'
        super()._compute_show_delivery_date()
        for move in self:
            if move.country_code == 'HU':
                move.show_delivery_date = True

    # # HU+
    @api.depends('partner_id')
    def _compute_l10n_hu_cash_accounting(self):
        for record in self:
            if record.is_invoice(True) and record.state == 'draft':
                if record.move_type in ['in_invoice', 'in_refund'] and record.partner_id:
                    cash_accounting = record.partner_id.l10n_hu_cash_accounting
                elif record.move_type in ['out_invoice', 'out_refund']:
                    cash_accounting = record.company_id.partner_id.l10n_hu_cash_accounting
                else:
                    cash_accounting = False
            else:
                cash_accounting = record.l10n_hu_cash_accounting
            record.l10n_hu_cash_accounting = cash_accounting

    @api.depends('l10n_hu_original_invoice_number')
    def _compute_l10n_hu_original_account_move(self):
        for record in self:
            original_invoice = None
            if record.is_invoice(True) and record.l10n_hu_original_invoice_number:
                if record.move_type in ['in_invoice', 'in_refund']:
                    original_invoice = self.env['account_move'].search([
                        ('company_id', '=', record.company_id.id),
                        ('move_type', 'in', ['in_invoice', 'in_refund']),
                        ('ref', 'ilike', record.l10n_hu_original_invoice_number)
                    ], limit=1)
                elif record.move_type in ['out_invoice', 'out_refund']:
                    original_invoice = self.env['account_move'].search([
                        ('company_id', '=', record.company_id.id),
                        ('move_type', 'in', ['out_invoice', 'out_refund']),
                        ('name', 'ilike', record.l10n_hu_original_invoice_number)
                    ], limit=1)
                else:
                    pass
            else:
                pass
            if original_invoice:
                original_account_move_id = original_invoice.id
            else:
                original_account_move_id = None
            record.l10n_hu_original_account_move = original_account_move_id

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
                record.l10n_hu_document_rate = 1.0

    def _compute_l10n_hu_delivery_period_text(self):
        for record in self:
            period_legal = ""
            period_summary = ""
            if record.move_type in ['out_invoice', 'out_refund'] \
                    and record.l10n_hu_delivery_period_start \
                    and record.l10n_hu_delivery_period_end:
                # Get period info
                delivery_period_result = record.l10n_hu_get_delivery_period({})
                if delivery_period_result.get('period_legal'):
                    period_legal = delivery_period_result['period_legal']
                if delivery_period_result.get('period_summary'):
                    period_summary = delivery_period_result['period_summary']
            record.l10n_hu_delivery_period_legal = period_legal
            record.l10n_hu_delivery_period_summary = period_summary

    def _compute_l10n_hu_rate_difference(self):
        for record in self:
            difference = record.l10n_hu_currency_rate - record.l10n_hu_document_rate
            record.l10n_hu_rate_difference = difference

    # Constraints and onchanges
    @api.onchange('l10n_hu_delivery_period_end', 'l10n_hu_delivery_period_start')
    def onchange_l10n_hu_delivery_period(self):
        if self.l10n_hu_delivery_period_end and self.l10n_hu_delivery_period_start:
            if self.l10n_hu_delivery_period_end < self.l10n_hu_delivery_period_start:
                raise exceptions.UserError(_("Period end date must be after period start date!"))
            elif self.l10n_hu_delivery_period_start > self.l10n_hu_delivery_period_end:
                raise exceptions.UserError(_("Period start date must be before period end date!"))
            else:
                pass
        else:
            pass

    # CRUD methods (and display_name, name_search, ...) overrides

    # Action methods
    def action_l10n_hu_refresh_delivery_period(self):
        """ Used by "Refresh" button in HU+ tab Period section """
        # Ensure one record in self
        self.ensure_one()

        # Initialize variables
        write_values = {}

        # Get summary
        if self.l10n_hu_delivery_period_start and self.l10n_hu_delivery_period_end:
            delivery_period_result = self.l10n_hu_get_delivery_period({})

            if delivery_period_result.get('delivery_date'):
                write_values.update({
                    'delivery_date': delivery_period_result['delivery_date'],
                })

        # Write
        if len(write_values) > 0:
            self.write(write_values)

        # Return
        return

    def action_l10n_hu_view_original_invoice(self):
        """ View original invoice """
        # Make sure there is one record in self
        self.ensure_one()

        # Initialize variables
        original_invoice = None

        # Search
        if self.l10n_hu_original_account_move:
            original_invoice = self.l10n_hu_original_account_move
        elif self.l10n_hu_original_invoice_number and not self.l10n_hu_original_account_move:
            if self.move_type in ['in_invoice', 'in_refund']:
                original_invoice = self.env['account_move'].search([
                    ('company_id', '=', self.company_id.id),
                    ('move_type', 'in', ['in_invoice', 'in_refund']),
                    ('ref', 'ilike', self.l10n_hu_original_invoice_number)
                ], limit=1)
            elif self.move_type in ['out_invoice', 'out_refund']:
                original_invoice = self.env['account_move'].search([
                    ('company_id', '=', self.company_id.id),
                    ('move_type', 'in', ['out_invoice', 'out_refund']),
                    ('name', 'ilike', self.l10n_hu_original_invoice_number)
                ], limit=1)
            else:
                pass

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

    def action_l10n_hu_wizard_currency_exchange(self):
        """ Open the L10n HU wizard to calculate the document rate """
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
    # # SUPER
    def _l10n_hu_edi_get_invoice_values(self):
        """ Super for original method in l10n_hu_edi app

        NOTE:
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

        # Return result
        return result

    # # HU+
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
    def l10n_hu_get_delivery_period(self, values):
        """ Get delivery period data

        NOTE:
        - This method takes care of special hungarian rules
        - Specification: 2007. CXXVII. 58.§ (1)
        - NJT: https://njt.hu/jogszabaly/2007-127-00-00

        :param values: dictionary

        :return: dictionary
        """
        # raise exceptions.UserError("l10n_hu_get_delivery_period BEGIN" + str(values))

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
            # NOTE: using a payment term needs a recompute, see _compute_invoice_date_due()
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
        return result
