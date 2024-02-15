# -*- coding: utf-8 -*-
# 1 : imports of python lib

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 : imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuInvoiceInvoiceLine(models.Model):
    # Private attributes
    _name = 'l10n.hu.invoice.line'
    _description = "HU Invoice Line"
    _order = 'account_move_line desc, id desc'

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
        comodel_name='res.company',
        copy=False,
        readonly=True,
        string="Company",
    )
    company_currency = fields.Many2one(
        comodel_name='res.currency',
        copy=False,
        readonly=True,
        string="Company Currency",
    )
    currency = fields.Many2one(
        related='invoice.currency',
        store=True,
        string="Currency",
    )
    currency_huf = fields.Many2one(
        related='invoice.currency_huf',
        store=True,
        string="Currency HUF",
    )
    customer = fields.Many2one(
        related='invoice.customer',
        string="Customer",
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
        related='invoice.invoice_category',
        store=True,
        string="Invoice Category",
    )
    invoice_number = fields.Char(
        related='invoice.invoice_number',
        store=True,
        string="Invoice Number",
    )
    invoice_operation = fields.Char(
        related='invoice.invoice_operation',
        store=True,
        string="Invoice Operation",
    )    
    is_price_refund = fields.Boolean(
        default=False,
        string="Price Refund",
    )
    name = fields.Char(
        copy=False,
        readonly=True,
        string="Invoice Line",
    )
    original_invoice = fields.Many2one(
        related='original_line.invoice',
        index=True,
        store=True,
        string="Original Invoice",
    )
    original_line = fields.Many2one(
        comodel_name='l10n.hu.invoice.line',
        copy=False,
        index=True,
        readonly=True,
        string="Original Line",
    )
    price_unit = fields.Float(
        string="Price Unit",
    )
    product = fields.Many2one(
        comodel_name='product.product',
        copy=False,
        readonly=True,
        string="Product",
    )
    sequence = fields.Integer(
        string="Sequence",
    )
    supplier = fields.Many2one(
        related='invoice.supplier',
        string="Supplier",
    )
    uom = fields.Many2one(
        comodel_name='uom.uom',
        copy=False,
        readonly=True,
        string="Unit of Measure",
    )
    uom_name = fields.Char(
        copy=False,
        readonly=True,
        string="UoM Name",
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
    # # NAV fields
    additional_line_data = fields.Text(
        string="Additional Line Data",
    )
    advance_account_move = fields.Many2one(
        related='advance_invoice.account_move',
        string="Advance Account Move",
    )
    advance_exchange_rate = fields.Float(
        copy=False,
        default=1.0,
        readonly=True,
        string="Advance Exchange Rate",
    )
    advance_indicator = fields.Boolean(
        string="Advance Indicator",
    )
    advance_invoice = fields.Many2one(
        comodel_name='l10n.hu.invoice',
        copy=False,
        string="Advance Invoice",
    )
    advance_payment_date = fields.Date(
        copy=False,
        readonly=True,
        string="Advance Payment Date",
    )
    advance_original_invoice = fields.Char(
        copy=False,
        readonly=True,
        size=50,
        string="Advance Original Invoice",
    )
    aggregate_invoice_line_data = fields.Char(
        string="Aggregate Invoice Line Data",
    )
    deposit_indicator = fields.Boolean(
        string="Deposit Indicator",
    )
    diesel_oil_purchase = fields.Char(
        string="Diesel Oil Purchase",
    )
    discount_description = fields.Char(
        string="Discount Description",
    )
    discount_rate = fields.Float(
        string="Discount Rate",
    )
    # Unit price is NOT monetary so that we can display digits
    discount_unit_price_net = fields.Float(
        string="Discount Unit Price Net",
    )
    discount_unit_price_gross = fields.Float(
        string="Discount Unit Price Gross",
    )
    discount_value = fields.Monetary(
        currency_field='currency',
        string="Discount Value",
    )
    ekaer_ids = fields.Char(
        string="EKAER IDs",
    )
    gpc_excise = fields.Float(
        string="GPC Excise",
    )
    intermediated_service = fields.Boolean(
        string="Intermediated Service",
    )
    line_description = fields.Char(
        size=512,
        string="Line Description",
    )
    line_expression_indicator = fields.Boolean(
        string="Line Expression Indicator",
    )
    line_gross_amount = fields.Monetary(
        currency_field='currency',
        string="Line Gross Amount",
    )
    line_gross_amount_huf = fields.Monetary(
        currency_field='currency_huf',
        string="Line Gross Amount HUF",
    )
    line_nature_indicator = fields.Char(
        string="Line Nature",
    )
    line_net_amount = fields.Monetary(
        currency_field='currency',
        string="Line Net Amount",
    )
    line_net_amount_huf = fields.Monetary(
        currency_field='currency_huf',
        string="Line Net Amount HUF",
    )
    line_number = fields.Integer(
        string="Line Number",
    )
    line_number_reference = fields.Integer(
        string="Line Number Reference",
    )
    line_operation = fields.Char(
        string="Line Operation",
    )
    line_vat_amount = fields.Monetary(
        currency_field='currency',
        string="Line VAT Amount",
    )
    line_vat_amount_huf = fields.Monetary(
        currency_field='currency_huf',
        string="Line VAT Amount HUF",
    )
    margin_scheme_indicator = fields.Boolean(
        string="Margin Scheme Indicator",
    )
    neta_declaration = fields.Boolean(
        string="NETA Declaration",
    )
    new_transport_mean = fields.Text(
        string="New Transport Mean",
    )
    obligated_for_product_fee = fields.Boolean(
        string="Obligated For Product Fee",
    )
    product_codes = fields.Char(
        string="Product Codes",
    )
    product_fee_content = fields.One2many(
        comodel_name='l10n.hu.invoice.product.fee',
        domain=[('scope', '=', 'line')],
        inverse_name='invoice_line',
        string="Product Fee Content",
    )
    product_stream = fields.Char(
        string="Product Stream",
    )
    product_weight = fields.Float(
        string="Product Weight",
    )
    quantity = fields.Float(
        string="Quantity",
    )
    references_to_other_lines = fields.Char(
        string="References To Other Lines",
    )
    takeover_amount = fields.Float(
        string="Takeover Amount",
    )
    takeover_reason = fields.Char(
        string="Takeover Reason",
    )
    unit_of_measure = fields.Char(
        string="Unit of Measure Name",
    )
    unit_of_measure_own = fields.Char(
        string="Unit of Measure Own",
    )
    # Unit price fields are NOT monetary so that we display more digits than the currency's setting
    unit_price = fields.Float(
        string="Unit Price",
    )
    unit_price_huf = fields.Float(
        string="Unit Price HUF",
    )
    unit_price_gross = fields.Float(
        string="Gross Unit Price",
    )
    unit_price_gross_huf = fields.Float(
        string="Gross Unit Price HUF",
    )
    unit_price_net = fields.Float(
        string="Net Unit Price",
    )
    unit_price_net_huf = fields.Float(
        string="Net Unit Price HUF",
    )

    # Compute and search fields, in the same order of field declarations

    # Constraints and onchanges
    @api.onchange('advance_invoice')
    def onchange_advance_invoice(self):
        if self.advance_invoice:
            self.advance_exchange_rate = self.advance_invoice.exchange_rate
            self.advance_original_invoice = self.advance_invoice.invoice_number
            self.advance_payment_date = self.advance_invoice.payment_date
        else:
            self.advance_exchange_rate = False
            self.advance_original_invoice = False
            self.advance_payment_date = False

    # CRUD methods (and name_get, name_search, ...) overrides
    @api.depends('account_move_line')
    def name_get(self):
        result = []
        for record in self:
            if record.account_move_line:
                name = record.account_move_line.display_name or ""
            elif record.id:
                name = record.id
            else:
                name = ""
            result.append((record.id, name))

        # return
        return result

    # Action methods

    # Business methods
    @api.model
    def line_tax_data(self, line, line_tax):
        """ Prepare line tax data

        :return: dictionary
        """
        # Assemble result
        result = {
            'company': line.company_id.id,
            'invoice_line': line.id,
            'amount': line_tax.amount,
            'currency': self.currency_id.id,
            'currency_name': self.currency_id.name,
            'currency_symbol': self.currency_id.symbol,
            'description': line_tax.description,
            'name': line_tax.name,
            'tax': line_tax.id,
        }

        # Return result
        return result

    @api.model
    def get_account_move_line_values(self, values):
        """ Get values from an account move line

        Note: unit price is problematic, because we do not know if it is meant to be gross or net
              we only know if it is net or gross by examining the settings of the applied tax,
              so we have to think backwards from tax settings

        :param values: dictionary

        :return: dictionary
        """
        # raise exceptions.UserError("get_account_move_line_values BEGIN" + str(values))

        # Unpack values
        account_move_line = values.get('account_move_line')
        invoice = values.get('invoice')
        invoice_operation = values.get('invoice_operation')
        line_number = values.get('line_number')
        line_number_reference = values.get('line_number_reference')
        original_account_move_line = values.get('original_account_move_line')
        original_invoice = values.get('original_invoice')

        # Check
        if not account_move_line or account_move_line.display_type in ['line_note', 'line_section']:
            return {}

        # is_processable_line
        is_processable_line = account_move_line.l10nhu_is_processable_invoice_line()
        if not is_processable_line:
            return {}

        # Initialize variables
        result = {
            'account_move_line': account_move_line.id,
        }

        # invoice
        if invoice:
            pass
        elif not invoice and self.invoice:
            invoice = self.invoice
        else:
            return {}

        # Account move
        account_move = account_move_line.move_id

        # Currencies
        company_currency = invoice.company.currency_id
        invoice_currency = invoice.currency
        currency_huf = invoice.currency_huf

        # original line (for modification/cancellation invoices)
        # always set it on creation, for partial refunds lines might be added/removed before confirming
        if invoice_operation in ['modify', 'storno'] \
                and original_invoice \
                and original_account_move_line:
            # raise exceptions.UserError("original invoice: modification/cancellation invoice")
            original_invoice_line = self.env['l10n.hu.invoice.line'].sudo().search([
                ('account_move_line', '=', original_account_move_line.id),
                ('id', '!=', self.id),
                ('invoice', '=', original_invoice.id),
            ])
            # raise exceptions.UserError(str(original_invoice_line))

            if original_invoice_line and len(original_invoice_line) == 1:
                result.update({
                    'line_number': line_number,
                    'line_number_reference': line_number_reference,
                    'line_operation': 'create',
                    'original_line': original_invoice_line.id
                })
            else:
                result.update({
                    'line_number': line_number,
                    'line_number_reference': line_number_reference,
                    'line_operation': 'create',
                })
        else:
            # raise exceptions.UserError("no original invoice")
            original_invoice_line = False
            result.update({
                'line_number': line_number,
                'line_number_reference': line_number_reference,
                'line_operation': 'create',
            })

        # Initialize amount sign for modify and storno
        # NOTE: amount_sign might be overridden/ignored later for specific operations (eg: price refund)
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

        # Total amounts
        line_net_amount = account_move_line.price_subtotal * amount_sign
        line_gross_amount = account_move_line.price_total * amount_sign
        line_vat_amount = line_gross_amount - line_net_amount

        # Set is_price_refund
        is_price_refund = False
        if invoice_operation == 'modify' or invoice.account_move.move_type == 'out_refund':
            is_refund_scope = True
        else:
            is_refund_scope = False
        refund_price_plan = account_move_line.move_id.journal_id.l10n_hu_invoice_refund_price_analytic_plan
        if is_refund_scope and refund_price_plan and account_move_line.analytic_distribution:
            """ TODO: rewrite 
            for tag in account_move_line.analytic_tag_ids:
                if tag == refund_price_tag:
                    is_price_refund = True
                    break
            """
            pass

        # Unit price
        # NOTE: we set unit_price_net from unit_price and override it later in case unit_price includes tax!
        unit_price = account_move_line.price_unit
        if is_refund_scope and is_price_refund:
            unit_price = unit_price * amount_sign
        elif is_refund_scope and not is_price_refund:
            unit_price = abs(unit_price)
        else:
            pass
        unit_price_net = unit_price

        # Initialize NAV VAT tax
        account_tax_l10n_hu_vat = False

        # We only consider one NAV VAT
        # TODO: maybe handle also on UI, that you can add only one NAV vat (tax) on a line
        for tax in account_move_line.tax_ids:
            if tax.l10n_hu_vat_enabled:
                account_tax_l10n_hu_vat = tax
                if tax.price_include and tax.l10n_hu_vat_percentage:
                    unit_price_net_raw = unit_price / (1 + tax.l10n_hu_vat_percentage)
                    unit_price_net = round(unit_price_net_raw, 2)
                else:
                    pass
                break
            else:
                pass

        # Company HUF, invoice HUF
        if currency_huf \
                and company_currency == currency_huf \
                and invoice_currency == currency_huf:
            exchange_rate = 1.0
        # Company HUF, invoice NOT HUF
        elif currency_huf \
                and company_currency == currency_huf \
                and invoice_currency != currency_huf:
            currency_rate_huf_amount = account_move.l10n_hu_currency_rate_amount
            exchange_rate = currency_rate_huf_amount
        # Company NOT HUF, invoice HUF (nothing to exchange, already HUF)
        elif currency_huf \
                and company_currency != currency_huf \
                and invoice_currency == currency_huf:
            exchange_rate = 1.0
        # Company NOT HUF, invoice NOT company currency, we have a currency rate too
        elif currency_huf \
                and company_currency != currency_huf \
                and invoice_currency != company_currency \
                and invoice.currency_rate:
            exchange_rate = invoice.currency_rate.rate
        # Other cases
        else:
            exchange_rate = 1.0

        # Set HUF amounts
        line_net_amount_huf = line_net_amount * exchange_rate
        line_vat_amount_huf = line_vat_amount * exchange_rate
        line_gross_amount_huf = line_gross_amount * exchange_rate
        unit_price_huf = round(unit_price * exchange_rate, 2)
        unit_price_net_huf = round(unit_price_net * exchange_rate, 2)

        # Set account tax and VAT
        if account_tax_l10n_hu_vat:
            account_tax_id = account_tax_l10n_hu_vat.id
            account_tax_amount = account_tax_l10n_hu_vat.amount
            account_tax_amount_type = account_tax_l10n_hu_vat.amount_type
            account_tax_price_include = account_tax_l10n_hu_vat.price_include
            vat_amount_mismatch_case = account_tax_l10n_hu_vat.l10n_hu_vat_amount_mismatch_case
            vat_exemption_case = account_tax_l10n_hu_vat.l10n_hu_vat_exemption_case
            vat_out_of_scope_case = account_tax_l10n_hu_vat.l10n_hu_vat_out_of_scope_case
            vat_percentage = account_tax_l10n_hu_vat.l10n_hu_vat_percentage
            vat_reason = account_tax_l10n_hu_vat.l10n_hu_vat_reason
            vat_type = account_tax_l10n_hu_vat.l10n_hu_vat_type

            # Tax group
            if account_tax_l10n_hu_vat.tax_group_id:
                account_tax_group_id = account_tax_l10n_hu_vat.tax_group_id.id
            else:
                account_tax_group_id = False

            # Override exemption text from the move line
            if account_move_line.l10n_hu_vat_reason:
                vat_reason = account_move_line.l10n_hu_vat_reason
        else:
            account_tax_id = False
            account_tax_amount = False
            account_tax_amount_type = False
            account_tax_group_id = False
            account_tax_price_include = False
            vat_amount_mismatch_case = False
            vat_exemption_case = False
            vat_out_of_scope_case = False
            vat_percentage = False
            vat_reason = False
            vat_type = False

        # NOW we set unit price gross and HUF
        unit_price_gross = unit_price_net * (1 + vat_percentage)
        unit_price_gross_huf = unit_price_gross * exchange_rate

        # unit_of_measure_own
        if account_move_line.product_uom_id.l10n_hu_type == 'own':
            result.update({
                'unit_of_measure_own': account_move_line.product_uom_id.name,
            })

        # line_description (match NAV: lineDescription SimpleText512NotBlankType .*[^\s].*)
        if account_move_line.name:
            account_move_line_name = account_move_line.name
            account_move_line_name_no_whitespace = ''.join(account_move_line_name.split())
            line_description = account_move_line_name_no_whitespace[:512]
        else:
            line_description = ""

        # quantity
        if is_refund_scope and is_price_refund:
            quantity = abs(account_move_line.quantity)
        else:
            quantity = account_move_line.quantity * amount_sign

        # advance_indicator
        # NOTE:
        # Odoo prepares a product for advance payment (Down payment) from code
        # The default deposit product is store on SYSTEM level here: sale.default_deposit_product_id
        # https://www.odoo.com/documentation/14.0/applications/sales/sales/invoicing/down_payment.html
        # First: We check if the product on the line matches this product
        # Second: We check line's analytic tags, if any of them match the advance tag defined on journal
        advance_indicator = False
        advance_product_id = self.env['ir.config_parameter'].sudo().get_param('sale.default_deposit_product_id')
        advance_product = self.env['product.product'].browse(int(advance_product_id))
        # advance_analytic_tag = account_move_line.move_id.journal_id.l10nhu_invoice_advance_tag
        if account_move_line.product_id == advance_product:
            advance_indicator = True
        """ TODO: rewrite
        elif account_move_line.analytic_tag_ids and advance_analytic_tag:
            for tag in account_move_line.analytic_tag_ids:
                if tag == advance_analytic_tag:
                    advance_indicator = True
                    break
        else:
            pass
        """

        # discount
        # NOTE:
        # lineDiscountData element contains the amount of the discount as a positive number.
        # must be true: quantity * unit_price - discount_value = line_net_amount
        # discount_rate: The item discount rate in percentage points, unless included in the unit price
        # discount_value: Total discount applied to the item, in the currency of the
        #                 invoice, unless included in the unit price
        if account_move_line.discount and account_move_line.discount > 0.0:
            discount_description = str(account_move_line.discount) + "% " + _("discount")
            discount_rate = account_move_line.discount
            discount_unit_price_gross = unit_price_gross * (100 - discount_rate) / 100
            discount_unit_price_net = unit_price_net * (100 - discount_rate) / 100
            discount_value = (quantity * unit_price) - line_net_amount
        else:
            discount_description = False
            discount_rate = 0.0
            discount_unit_price_gross = unit_price_gross
            discount_unit_price_net = unit_price_net
            discount_value = 0.0

        # Update result
        result.update({
            'account_tax': account_tax_id,
            'account_tax_amount': account_tax_amount,
            'account_tax_amount_type': account_tax_amount_type,
            'account_tax_group': account_tax_group_id,
            'account_tax_price_include': account_tax_price_include,
            'advance_indicator': advance_indicator,
            'company': account_move_line.move_id.company_id.id,
            'company_currency': company_currency.id,
            'discount_description': discount_description,
            'discount_rate': discount_rate,
            'discount_unit_price_gross': discount_unit_price_gross,
            'discount_unit_price_net': discount_unit_price_net,
            'discount_value': discount_value,
            'invoice': invoice.id,
            'invoice_category': invoice.invoice_category,
            'is_price_refund': is_price_refund,
            'line_description': line_description,
            'line_gross_amount': line_gross_amount,
            'line_gross_amount_huf': line_gross_amount_huf,
            'line_net_amount': line_net_amount,
            'line_net_amount_huf': line_net_amount_huf,
            'line_vat_amount': line_vat_amount,
            'line_vat_amount_huf': line_vat_amount_huf,
            'product': account_move_line.product_id.id,
            'quantity': quantity,
            'sequence': account_move_line.sequence,
            'unit_of_measure': account_move_line.product_uom_id.l10n_hu_type,
            'unit_price': unit_price,
            'unit_price_huf': unit_price_huf,
            'unit_price_gross': unit_price_gross,
            'unit_price_gross_huf': unit_price_gross_huf,
            'unit_price_net': unit_price_net,
            'unit_price_net_huf': unit_price_net_huf,
            'uom': account_move_line.product_uom_id.id,
            'uom_name': account_move_line.product_uom_id.name,
            'vat_amount_mismatch_case': vat_amount_mismatch_case,
            'vat_exemption_case': vat_exemption_case,
            'vat_out_of_scope_case': vat_out_of_scope_case,
            'vat_percentage': vat_percentage,
            'vat_reason': vat_reason,
            'vat_type': vat_type,
        })

        # Return result
        # raise exceptions.UserError("get_account_move_line_values END" + str(result))
        return result
