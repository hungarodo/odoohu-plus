# -*- coding: utf-8 -*-
# 1 : imports of python lib
import re

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 : imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuInvoiceSummary(models.Model):
    # Private attributes
    _name = 'l10n.hu.invoice.summary'
    _description = "HU Invoice Summary"
    _order = 'write_date desc, id desc'

    # Default methods

    # Field declarations
    account_move = fields.Many2one(
        related='account_move_line.move_id',
        store=True,
        string="Account Move",
    )
    account_move_line = fields.Many2one(
        comodel_name='account.move.line',
        copy=False,
        readonly=True,
        string="Account Move Line",
    )
    account_tax = fields.Many2one(
        comodel_name='account.tax',
        copy=False,
        readonly=True,
        string="Account Tax",
    )
    account_tax_amount = fields.Float(
        copy=False,
        readonly=True,
        string="Account Tax Amount",
    )
    account_tax_amount_type = fields.Char(
        copy=False,
        readonly=True,
        string="Account Tax Amount Type",
    )
    account_tax_group = fields.Many2one(
        comodel_name='account.tax.group',
        copy=False,
        readonly=True,
        string="Account Tax Group",
    )
    account_tax_name = fields.Char(
        copy=False,
        readonly=True,
        string="Account Tax Name",
    )
    account_tax_price_include = fields.Boolean(
        copy=False,
        readonly=True,
        string="Account Tax Price Include",
    )
    company = fields.Many2one(
        related='invoice.company',
        store=True,
        string="Company",
    )
    company_currency = fields.Many2one(
        comodel_name='res.currency',
        copy=False,
        readonly=True,
        string="Company Currency",
    )
    currency = fields.Many2one(
        comodel_name='res.currency',
        copy=False,
        readonly=True,
        string="Currency",
    )
    currency_huf = fields.Many2one(
        comodel_name='res.currency',
        copy=False,
        readonly=True,
        string="Currency HUF",
    )
    eu_oss_eligible = fields.Boolean(
        related='invoice.eu_oss_eligible',
        store=True,
        string="Invoice EU OSS Eligible",
    )
    eu_oss_enabled = fields.Boolean(
        related='invoice.eu_oss_enabled',
        store=True,
        string="Invoice EU OSS Enabled",
    )
    invoice = fields.Many2one(
        comodel_name='l10n.hu.invoice',
        copy=False,
        ondelete='cascade',
        readonly=True,
        string="Invoice",
    )
    invoice_category = fields.Selection(
        copy=False,
        readonly=True,
        selection=[
            ('normal', "Normal"),
            ('simplified', "Simplified"),
            ('aggregate', "Aggregate"),
        ],
        string="Invoice Category",
    )
    name = fields.Char(
        copy=False,
        readonly=True,
        string="Invoice Line",
    )
    vat_amount_mismatch_case = fields.Selection(
        help="VAT amount mismatch case according to NAV (Hungarian Tax Authority) regulations",
        selection=[
            ('refundable_vat', "REFUNDABLE - VAT must be refunded by the recipient of the invoice"),
            ('nonrefundable_vat', "NONREFUNDABLE - VAT does not need to be refunded by the recipient of the invoice"),
            ('unknown', "UNKNOWN - Pre-3.0 invoice"),
        ],
        string="VAT Amount Mismatch Case",
    )
    vat_exemption_case = fields.Selection(
        copy=False,
        help="VAT exemption case according to NAV (Hungarian Tax Authority) regulations",
        readonly=True,
        selection=[
            ('aam', "AAM - Personal tax exemption"),
            ('tam', "TAM - Tax-exempt activity"),
            ('kbaet', "KBAET - Intra-Community"),
            ('kbauk', "KBAUK - Intra-Community New Transport"),
            ('eam', "EAM - Extra-Community"),
            ('nam', "NAM - Other International"),
            ('unknown', "UNKNOWN - Pre-3.0 invoice"),
        ],
        string="VAT Exemption Case",
    )
    vat_out_of_scope_case = fields.Selection(
        copy=False,
        help="VAT out-of-scope case according to NAV (Hungarian Tax Authority) regulations",
        readonly=True,
        selection=[
            ('atk', "ATK - Outside the scope of VAT"),
            ('eufad37', "EUFAD37 - VAT§37 Intra-Community Reverse Charge"),
            ('eufade', "EUFADE - Non-VAT§37 Intra-Community Reverse Charge"),
            ('eue', "EUE - Intra-Community non-reverse charge"),
            ('ho', "HO - Transaction in a third country"),
            ('unknown', "UNKNOWN - Pre-3.0 invoice"),
        ],
        string="VAT Out of Scope Case",
    )
    vat_percentage = fields.Float(
        copy=False,
        digits=(5, 4),
        readonly=True,
        string="VAT Percentage",
    )
    vat_rate_gross_amount = fields.Monetary(
        currency_field='currency',
        string="Vat Rate Gross Amount",
    )
    vat_rate_gross_amount_huf = fields.Monetary(
        currency_field='currency_huf',
        string="Vat Rate Gross Amount HUF",
    )
    vat_rate_net_amount = fields.Monetary(
        currency_field='currency',
        string="Vat Rate Net Amount",
    )
    vat_rate_net_amount_huf = fields.Monetary(
        currency_field='currency_huf',
        string="Vat Rate Net Amount HUF",
    )
    vat_rate_vat_amount = fields.Monetary(
        currency_field='currency',
        string="VAT Rate VAT Amount",
    )
    vat_rate_vat_amount_huf = fields.Monetary(
        currency_field='currency_huf',
        string="VAT Rate VAT Amount HUF",
    )
    vat_reason = fields.Char(
        copy=False,
        readonly=True,
        size=200,
        string="VAT Reason",
    )
    vat_type = fields.Selection(
        copy=False,
        readonly=True,
        selection=[
            ('percentage', "Percentage"),
            ('exemption', "Exemption"),
            ('out_of_scope', "Out Of Scope"),
            ('domestic_reverse_charge', "Domestic Reverse Charge"),
            ('margin_scheme_vat', "Margin Scheme VAT"),
            ('margin_scheme_no_vat', "Margin Scheme No VAT"),
        ],
        string="VAT Type",
    )
    
    # Compute and search fields, in the same order of field declarations

    # Constraints and onchanges

    # CRUD methods (and name_get, name_search, ...) overrides

    # Action methods

    # Business methods
    @api.model
    def get_values_from_account_move_line(self, values):
        """ Get tax summary values from an account move line

        We decide if an account.move.line is a tax for nav:
            - tax_group_id (m2o to account tax group) is not empty
            - tax_line_id (m2o to account tax) is not empty and l10n_hu_vat_enabled is True on the linked record

        Computation:
            - credit, debit, balance, tax_base_amount fields use accounting date, not invoice delivery date,
             we do NOT use them, use the amount_currency field and make our own conversion for foreign currencies
            - we need to consider scenarios for invoice, company and HUF currencies

        About rounding:
            We could do reverse calculation if price_include is True for the VAT rate BUT we do not
            Reverse calculation has potential errors, for example:
                - original: 79 HUF x 5% VAT = 4 HUF
                - reverse calculation: 4 HUF / 5% VAT = 80 HUF
            To avoid round issues we use Odoo's built-in tax_base_amount field
            BUT tax_base_amount uses company currency
            SO we need to reverse it to invoice currency to be sure:
                1) accounting_currency_rate = credit or debit / abs(amount_currency)
                2) tax_base_amount_invoice_currency = tax_base_amount / accounting_currency_rate
            BUT to tax base amount avoid rounding issues we skip reversing computation if the invoice CCY is HUF
                example rounding issue:
                    - company is EUR, invoice HUF, invoice net 1.000 HUF, 27% tax
                    - computation will yield different vat_rate_net_amount_base, eg: 997 HUF
                    (the computation amount result varies due to exchange rate changes)

        :param values: dictionary, including:
            account_move_line: an account.move.line record
            invoice: l10n.hu.invoice record, can be empty
            non_zero_rate: boolean showing if the tax is 0% or not (we manage them differently), defaults to True

        :return dictionary
        """
        # raise exceptions.UserError("get_values_from_account_move_line BEGIN " + str(values))

        # Initialize variables
        crud_values = {}
        debug_list = []
        error_list = []
        info_list = []
        result = {}
        warning_list = []

        # account_move_line
        if values.get('account_move_line'):
            account_move_line = values['account_move_line']
            crud_values.update({
                'account_move_line': account_move_line.id,
            })
            debug_list.append('account_move_line found in values with id: ' + str(account_move_line.id))
        else:
            account_move_line = False
            error_list.append('account_move_line not found in values')

        # invoice
        if values.get('invoice'):
            invoice = values['invoice']
            debug_list.append('invoice found in values with id: ' + str(invoice.id))
        elif self.invoice:
            invoice = self.invoice
            debug_list.append('invoice set using self: ' + str(invoice.id))
        else:
            invoice = False
            error_list.append('invoice not found in values')

        # non_zero_rate
        if values.get('non_zero_rate') is not None:
            non_zero_rate = values['non_zero_rate']
            debug_list.append('non_zero_rate found in values: ' + str(non_zero_rate))
        else:
            non_zero_rate = False
            debug_list.append('non_zero_rate not found in values, using default False')

        # Check
        if account_move_line and non_zero_rate and account_move_line.tax_line_id:
            if not account_move_line.tax_line_id.l10nhu_is_nav_vat:
                error_list.append('account_move_line tax_line_id is not HU VAT: ' + str(account_move_line.tax_line_id))
        elif account_move_line and non_zero_rate and account_move_line.tax_ids:
            for tax in account_move_line.tax_ids:
                if not tax.l10nhu_is_nav_vat:
                    error_list.append('account_move_line non_zero_rate tax_ids tax is not HU VAT: ' + str(tax.id))
        elif account_move_line and not non_zero_rate and account_move_line.tax_ids:
            for tax in account_move_line.tax_ids:
                if not tax.l10nhu_is_nav_vat:
                    error_list.append('account_move_line NOT non_zero_rate tax_ids tax is not HU VAT: ' + str(tax.id))
        else:
            error_list.append('invalid tax scenario')

        # account_tax
        if non_zero_rate:
            # normal case: we have accounting entry
            if account_move_line.tax_line_id:
                account_tax = account_move_line.tax_line_id
            # special case: Odoo does not prepare accounting if the total of taxes is 0 (eg: delivery with down payment)
            else:
                account_tax = False
                for tax in account_move_line.tax_ids:
                    if tax.l10nhu_is_nav_vat and tax.l10nhu_nav_vat_percentage != 0.0:
                        account_tax = tax
                        break
                    else:
                        pass
        else:
            account_tax = False
            for tax in account_move_line.tax_ids:
                if tax.l10n_hu_vat_enabled and tax.l10n_hu_vat_percentage == 0.0:
                    account_tax = tax
                    break
                else:
                    pass

        if account_tax:
            debug_list.append('account_tax set: ' + str(account_tax.id))
        else:
            debug_list.append('account_tax NOT set')

        # Tax group, vat_rate, price_include (if True, than unit price is a gross price)
        if account_tax:
            price_include = account_tax.price_include
            vat_percentage = account_tax.l10n_hu_vat_percentage
        else:
            price_include = False
            vat_percentage = False

        # Currencies
        company_currency = invoice.company.currency_id
        invoice_currency = invoice.currency
        huf_currency = self.env['res.currency'].search([
            ('active', 'in', [True, False]),
            ('name', '=', 'HUF'),
        ])
        if huf_currency:
            huf_currency_id = huf_currency.id
            debug_list.append('huf_currency_id set: ' + str(huf_currency_id))
        else:
            huf_currency_id = False
            error_list.append('could not set huf_currency_id')

        # Amount sign
        if invoice.invoice_operation == 'modify' \
                and invoice.account_move \
                and invoice.account_move.move_type in ['out_invoice', 'out_receipt']:
            amount_sign = 1
        elif invoice.invoice_operation == 'modify' \
                and invoice.account_move \
                and invoice.account_move.move_type in ['out_refund']:
            amount_sign = -1
        elif invoice.invoice_operation == 'storno':
            amount_sign = -1
        elif invoice.account_move.move_type == 'out_refund':
            amount_sign = -1
        else:
            amount_sign = 1

        # Respect the original intention of the line (eg: minus on an invoice/refund)
        if account_move_line.price_subtotal < 0:
            amount_sign = amount_sign * -1
            debug_list.append('amount_sign finalized with * -1: ' + str(amount_sign))
        else:
            debug_list.append('amount_sign finalized: ' + str(amount_sign))

        # vat_rate_net_amount
        # NOTE: credit/debit and tax_base_amount have Company CCY, amount_currency has Invoice CCY
        # 1) accounting_currency_rate = credit or debit / abs(amount_currency)
        if account_move_line.credit > 0 and account_move_line.amount_currency != 0:
            accounting_currency_rate = account_move_line.credit / abs(account_move_line.amount_currency)
        elif account_move_line.debit > 0 and account_move_line.amount_currency != 0:
            accounting_currency_rate = account_move_line.debit / abs(account_move_line.amount_currency)
        else:
            accounting_currency_rate = 1.0
        # 2) tax_base_amount_invoice_currency = tax_base_amount / accounting_currency_rate
        # NOTE: we may have a rounding problem if company CCY is not HUF
        # example: company CCY EUR, invoice CCY HUF, invoice net amount is 1.000 HUF, nav vat 27%
        # the vat amount is correctly 270 HUF, but calculating back the base amount yield eg: 997 HUF
        # this is because of the exchange rate decimals
        # current solution: if company ccy is not HUF and invoice ccy is HUF...
        # ...than compute base amount from VAT amount, eg: base amount = vat amount / 0,2700
        # ALSO: need to use abs() for amount_currency as it might be negative depending on accounting situation
        if company_currency.name != 'HUF' \
                and invoice_currency.name == 'HUF'\
                and vat_percentage \
                and vat_percentage != 0.0:
            # raise exceptions.UserError("vat_rate_net_amount_base CASE 1")
            vat_rate_net_amount_base = abs(account_move_line.amount_currency) / vat_percentage
        elif company_currency.name != 'HUF' \
                and invoice_currency.name == 'HUF'\
                and (not vat_percentage or vat_percentage == 0.0):
            # raise exceptions.UserError("vat_rate_net_amount_base CASE 2")
            vat_rate_net_amount_base = abs(account_move_line.amount_currency)
        else:
            # raise exceptions.UserError("vat_rate_net_amount_base CASE 3")
            # raise exceptions.UserError(str(account_move_line.tax_base_amount) + "/" + str(accounting_currency_rate))
            vat_rate_net_amount_base = account_move_line.tax_base_amount / accounting_currency_rate
            # raise exceptions.UserError(str(account_move_line.amount_currency) + "/" + str(accounting_currency_rate))
            # vat_rate_net_amount_base = account_move_line.amount_currency / accounting_currency_rate

        # v14: We rely on price_subtotal field, it stores tax amount in the currency of the invoice
        # v15: We rely on price_subtotal field, it stores tax amount in the currency of the invoice
        # v16: We rely on amount_currency field, it stores tax amount in the currency of the invoice
        # v16: We use abs() to ignore Odoo's accounting logic, we just need the amount and then use our own amount_sign
        # For price included/excluded rates use Odoo's built-in tax_base_amount field
        if price_include and vat_percentage and vat_percentage != 0.0:
            # raise exceptions.UserError("vat_rate_vat_amount CASE 1")
            vat_rate_vat_amount = abs(account_move_line.amount_currency) * amount_sign
            vat_rate_net_amount = vat_rate_net_amount_base * amount_sign
        elif not price_include and vat_percentage and vat_percentage != 0.0:
            # raise exceptions.UserError("vat_rate_vat_amount CASE 2")
            vat_rate_vat_amount = abs(account_move_line.amount_currency) * amount_sign
            vat_rate_net_amount = vat_rate_net_amount_base * amount_sign
        # For zero rates vat is 0, so we process things differently
        # The amount is aggregated later in the caller get_account_move_values_invoice_summary method
        else:
            # raise exceptions.UserError("vat_rate_vat_amount CASE 3")
            vat_rate_vat_amount = 0.0
            vat_rate_net_amount = abs(account_move_line.amount_currency) * amount_sign

        # Amount computations in invoice currency
        vat_rate_gross_amount = vat_rate_net_amount + vat_rate_vat_amount

        # Company HUF, invoice HUF
        if huf_currency \
                and company_currency == huf_currency \
                and invoice_currency == huf_currency:
            exchange_rate = 1.0
        # Company HUF, invoice NOT HUF
        elif huf_currency \
                and company_currency == huf_currency \
                and invoice_currency != huf_currency:
            exchange_rate = account_move_line.move_id.l10nhu_currency_rate_amount
        # Company NOT HUF, invoice HUF (nothing to exchange, already HUF)
        elif huf_currency \
                and company_currency != huf_currency \
                and invoice_currency == huf_currency:
            exchange_rate = 1.0
        # Company NOT HUF, invoice NOT company currency, we have a currency rate too
        elif huf_currency \
                and company_currency != huf_currency \
                and invoice_currency != company_currency \
                and invoice.currency_rate:
            exchange_rate = invoice.currency_rate.rate
        # Everything else
        else:
            exchange_rate = 1.0

        # Set HUF amounts
        vat_rate_net_amount_huf = vat_rate_net_amount * exchange_rate
        vat_rate_vat_amount_huf = vat_rate_vat_amount * exchange_rate
        vat_rate_gross_amount_huf = vat_rate_gross_amount * exchange_rate

        # Set invoice_category
        invoice_category = invoice.invoice_category

        # Set vat_exemption
        if account_tax and account_tax.l10n_hu_vat_type == 'exemption':
            vat_exemption_case = account_tax.l10n_hu_vat_exemption_case
            nav_vat_out_of_scope_case = ""
            vat_reason = account_tax.l10n_hu_vat_reason
        elif account_tax and account_tax.l10n_hu_vat_type == 'out_of_scope':
            vat_exemption_case = ""
            vat_out_of_scope_case = account_tax.l10n_hu_vat_out_of_scope_case
            vat_reason = account_tax.l10n_hu_vat_reason
        else:
            vat_exemption_case = ""
            vat_out_of_scope_case = ""
            vat_reason = ""

        # Account tax details
        if account_tax:
            account_tax_id = account_tax.id
            account_tax_amount = account_tax.amount
            account_tax_amount_type = account_tax.amount_type
            if account_tax.tax_group_id:
                account_tax_group_id = account_tax.tax_group_id.id
                account_tax_name = account_tax.tax_group_id.name
            else:
                account_tax_group_id = False
                account_tax_name = False
            account_tax_price_include = account_tax.price_include
            account_tax_vat_type = account_tax.l10n_hu_vat_type
        else:
            account_tax_id = False
            account_tax_amount = False
            account_tax_amount_type = False
            account_tax_group_id = False
            account_tax_name = False
            account_tax_price_include = False
            account_tax_vat_type = False

        # Update crud
        crud_values.update({
            'account_tax': account_tax_id,
            'account_tax_amount': account_tax_amount,
            'account_tax_amount_type': account_tax_amount_type,
            'account_tax_group': account_tax_group_id,
            'account_tax_name': account_tax_name,
            'account_tax_price_include': account_tax_price_include,
            'company': account_move_line.move_id.company_id.id,
            'company_currency': company_currency.id,
            'currency': invoice_currency.id,
            'currency_huf': huf_currency_id,
            'invoice': invoice.id,
            'invoice_category': invoice_category,
            'vat_exemption_case': vat_exemption_case,
            'vat_out_of_scope_case': vat_out_of_scope_case,
            'vat_percentage': vat_percentage,
            'vat_reason': vat_reason,
            'vat_rate_gross_amount': vat_rate_gross_amount,
            'vat_rate_gross_amount_huf': vat_rate_gross_amount_huf,
            'vat_rate_net_amount': vat_rate_net_amount,
            'vat_rate_net_amount_huf': vat_rate_net_amount_huf,
            'vat_rate_vat_amount': vat_rate_vat_amount,
            'vat_rate_vat_amount_huf': vat_rate_vat_amount_huf,
            'vat_type': account_tax_vat_type,
        })

        # Update result
        result.update({
            'account_move_line': account_move_line,
            'account_tax': account_tax,
            'amount_sign': amount_sign,
            'crud_values': crud_values,
            'debug_list': debug_list,
            'error_list': error_list,
            'info_list': info_list,
            'invoice': invoice,
            'non_zero_rate': non_zero_rate,
            'warning_list': warning_list,
        })

        # Return
        # raise exceptions.UserError("get_values_from_account_move_line END" + str(result))
        return result
