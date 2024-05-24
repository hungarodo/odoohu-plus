# -*- coding: utf-8 -*-
# 1 : imports of python lib

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 : imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuNavReportInput(models.Model):
    # Private attributes
    _name = 'l10n.hu.nav.report.input'
    _description = "HU NAV Report Input"
    _inherit = ['mail.activity.mixin', 'mail.thread']
    _order = 'report desc, id desc'

    # Default methods
    @api.model
    def _get_selection_payment_method(self):
        return self.env['account.payment.term'].l10n_hu_get_nav_method_selection()

    @api.model
    def _get_selection_product_uom_type(self):
        return self.env['uom.uom'].l10n_hu_get_type_selection()

    # Field declarations
    # # COMMON
    active = fields.Boolean(
        related='report.active',
        store=True,
        string="Active",
    )
    code = fields.Char(
        string="Code",
    )
    category = fields.Many2one(
        comodel_name='l10n.hu.tag',
        domain=[('tag_type', '=', 'nav_report_data_category')],
        index=True,
        string="Category",
    )
    category_technical_name = fields.Char(
        related='category.technical_name',
        string="Category Technical Name",
    )
    company = fields.Many2one(
        comodel_name='res.company',
        index=True,
        related='report.company',
        store=True,
        string="Company",
    )
    company_currency = fields.Many2one(
        comodel_name='res.currency',
        related='company.currency_id',
        readonly=True,
        string="Company Currency",
    )
    description = fields.Text(
        string="Description",
    )
    locked = fields.Boolean(
        default=False,
        string="Locked",
    )
    name = fields.Char(
        string="Name",
    )
    report = fields.Many2one(
        comodel_name='l10n.hu.nav.report',
        index=True,
        ondelete='cascade',
        required=True,
        string="Report",
    )
    rule = fields.Many2one(
        comodel_name='l10n.hu.nav.report.rule',
        index=True,
        string="Rule",
    )
    rule_technical_name = fields.Char(
        related='rule.technical_name',
        index=True,
        store=True,
        string="Rule Technical Name",
    )
    rule_value_type = fields.Selection(
        related='rule.value_type',
        index=True,
        store=True,
        string="Rule Value Type",
    )
    status = fields.Selection(
        related='report.status',
        store=True,
        string="Status",
    )
    tag = fields.Many2many(
        comodel_name='l10n.hu.tag',
        column1='object',
        column2='tag',
        domain=[('tag_type', 'in', ['general', 'nav_report_data_tag'])],
        index=True,
        relation='l10n_hu_nav_report_input_tag_rel',
        string="Tag",
    )
    # # ACCOUNT
    account_account = fields.Many2one(
        comodel_name='account.account',
        copy=False,
        readonly=True,
        string="Account",
    )
    account_fiscal_position = fields.Many2one(
        comodel_name='account.fiscal.position',
        copy=False,
        readonly=True,
        string="Account Fiscal Position",
    )
    account_move = fields.Many2one(
        comodel_name='account.move',
        copy=False,
        readonly=True,
        string="Account Move",
    )
    account_move_line = fields.Many2one(
        comodel_name='account.move.line',
        copy=False,
        readonly=True,
        string="Account Move Line",
    )
    account_payment_term = fields.Many2one(
        comodel_name='account.payment.term',
        copy=False,
        readonly=True,
        string="Payment Term",
    )
    account_tag = fields.Many2many(
        column1='input',
        column2='tag',
        comodel_name='account.account.tag',
        copy=False,
        readonly=True,
        relation='l10n_hu_nav_report_input_account_tag_rel',
        string="Account Tags",
    )
    account_tag_invert = fields.Boolean(
        copy=False,
        default=False,
        readonly=True,
        string="Account Tag Invert",
    )
    account_tax = fields.Many2many(
        column1='input',
        column2='tax',
        comodel_name='account.tax',
        copy=False,
        readonly=True,
        relation='l10n_hu_nav_report_input_account_tax_rel',
        string="Taxes",
    )
    account_tax_line = fields.Many2one(
        comodel_name='account.tax',
        copy=False,
        readonly=True,
        string="Originator Tax",
    )
    account_tax_repartition_line = fields.Many2one(
        comodel_name='account.tax.repartition.line',
        copy=False,
        readonly=True,
        string="Tax Repartition Line",
    )
    account_tax_scope = fields.Selection(
        copy=False,
        readonly=True,
        selection=[
            ('product', "Product"),
            ('service', "Service"),
        ],
        string="Tax Scope",
    )
    amount_balance = fields.Float(
        copy=False,
        readonly=True,
        string="Balance Amount",
    )
    amount_credit = fields.Float(
        copy=False,
        readonly=True,
        string="Credit Amount",
    )
    amount_currency = fields.Float(
        copy=False,
        readonly=True,
        string="Currency Amount",
    )
    amount_debit = fields.Float(
        copy=False,
        readonly=True,
        string="Debit Amount",
    )
    amount_net = fields.Float(
        copy=False,
        readonly=True,
        string="Net Amount",
    )
    amount_tax = fields.Float(
        copy=False,
        readonly=True,
        string="Tax Amount",
    )
    amount_total = fields.Float(
        copy=False,
        readonly=True,
        string="Total Amount",
    )
    delivery_date = fields.Date(
        copy=False,
        readonly=True,
        string="Delivery Date",
    )
    downpayment = fields.Boolean(
        copy=False,
        default=False,
        readonly=True,
        string="Downpayment",
    )
    fiscal_position_match = fields.Boolean(
        copy=False,
        default=False,
        readonly=True,
        string="Fiscal Position Match",
    )
    payment_date = fields.Date(
        copy=False,
        readonly=True,
        string="Payment Date",
    )
    payment_method = fields.Selection(
        copy=False,
        readonly=True,
        selection=_get_selection_payment_method,
        string="Payment Method",
    )
    tax_base_distributed = fields.Float(
        copy=False,
        readonly=True,
        string="Tax Base Distributed",
    )
    tax_base_factor = fields.Float(
        copy=False,
        readonly=True,
        string="Tax Base Factor",
    )
    tax_base_original = fields.Float(
        copy=False,
        readonly=True,
        string="Tax Base Original",
    )
    tax_base_percent = fields.Float(
        copy=False,
        readonly=True,
        string="Tax Base Percent",
    )
    # # CURRENCY
    currency = fields.Many2one(
        comodel_name='res.currency',
        copy=False,
        readonly=True,
        string="Currency",
    )
    currency_code = fields.Char(
        copy=False,
        readonly=True,
        string="Currency Code",
    )
    currency_rate = fields.Float(
        copy=False,
        readonly=True,
        string="Currency Rate",
    )
    # # PARTNER
    partner = fields.Many2one(
        comodel_name='res.partner',
        copy=False,
        readonly=True,
        string="Partner",
    )
    partner_country = fields.Many2one(
        comodel_name='res.country',
        copy=False,
        readonly=True,
        string="Partner Country",
    )
    partner_country_code = fields.Char(
        copy=False,
        readonly=True,
        string="Partner Country Code",
    )
    partner_fiscal_position = fields.Many2one(
        comodel_name='account.fiscal.position',
        copy=False,
        readonly=True,
        string="Partner Fiscal Position",
    )
    partner_name = fields.Char(
        copy=False,
        readonly=True,
        string="Partner Name",
    )
    partner_tax_number = fields.Char(
        copy=False,
        readonly=True,
        string="Partner Tax Number",
    )
    partner_tax_unit = fields.Many2one(
        comodel_name='res.partner',
        copy=False,
        readonly=True,
        string="Partner Tax Unit",
    )
    partner_trade_position = fields.Char(
        copy=False,
        readonly=True,
        string="Partner Trade Position",
    )
    tax_number = fields.Char(
        copy=False,
        readonly=True,
        string="Tax Number",
    )
    # # PRODUCT
    product = fields.Many2one(
        comodel_name='product.product',
        copy=False,
        readonly=True,
        string="Product",
    )
    product_code = fields.Char(
        copy=False,
        readonly=True,
        string="Product Code",
    )
    product_name = fields.Char(
        copy=False,
        readonly=True,
        string="Product Name",
    )
    product_scope = fields.Char(
        copy=False,
        readonly=True,
        string="Product Scope",
    )
    product_type = fields.Char(
        copy=False,
        readonly=True,
        string="Product Type",
    )
    product_uom = fields.Many2one(
        comodel_name='uom.uom',
        copy=False,
        readonly=True,
        string="Product UoM",
    )
    product_uom_category = fields.Many2one(
        comodel_name='uom.category',
        copy=False,
        readonly=True,
        string="Product UoM Category",
    )
    product_uom_category_name = fields.Char(
        copy=False,
        readonly=True,
        string="Product UoM Name",
    )
    product_uom_name = fields.Char(
        copy=False,
        readonly=True,
        string="Product UoM Name",
    )
    product_uom_type = fields.Selection(
        copy=False,
        readonly=True,
        selection=_get_selection_product_uom_type,
        string="Product Uom Type",
    )
    # # VALUE
    value_char = fields.Char(
        copy=False,
        string="Value Char",
    )
    value_date = fields.Date(
        copy=False,
        string="Value Date",
    )
    value_display = fields.Char(
        compute='_compute_value_display',
        string="Value Display"
    )
    value_float = fields.Float(
        copy=False,
        string="Value Float",
    )
    value_integer = fields.Integer(
        copy=False,
        string="Value Integer",
    )

    # Compute and search fields, in the same order of field declarations
    def _compute_value_display(self):
        for record in self:
            # Compute
            value_display = record.get_value_display()

            # Set
            record.value_display = value_display

    # Constraints and onchanges

    # CRUD methods (and name_get, name_search, ...) overrides
    def name_get(self):
        # Initialize variables
        result = []

        # Iterate through self
        for record in self:
            # Set name
            name = ""
            if record.name:
                name += record.name

            if record.value_display:
                name += record.value_display

            # Append to list
            result.append((record.id, name))

        # Return result
        return result

    # Action methods

    # Business methods
    @api.model
    def get_value_display(self):
        if self.rule and self.rule_value_type == 'boolean':
            result = str(self.value_boolean)
        elif self.rule and self.rule_value_type == 'char':
            result = self.value_char
        elif self.rule and self.rule_value_type == 'date':
            result = str(self.value_date)
        elif self.rule and self.rule_value_type == 'datetime':
            result = str(self.value_datetime)
        elif self.rule and self.rule_value_type == 'float':
            result = str(self.value_float)
        elif self.rule and self.rule_value_type == 'integer':
            result = str(self.value_integer)
        else:
            result = False

        # Return result
        return result
