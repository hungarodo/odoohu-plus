# -*- coding: utf-8 -*-
# 1 : imports of python lib

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 : imports from odoo modules
from odoo.addons import decimal_precision as dp

# 4 : variable declarations


# Class
class L10nHuNavReportRule(models.Model):
    # Private attributes
    _name = 'l10n.hu.nav.report.rule'
    _description = "HU NAV Report Rule"
    _inherit = ['mail.activity.mixin', 'mail.thread']
    _order = 'id desc'

    # Default methods

    # Field declarations
    # # COMMON
    active = fields.Boolean(
        default=True,
        string="Active",
    )
    api_enabled = fields.Boolean(
        default=False,
        string="API Enabled",
    )
    company = fields.Many2one(
        comodel_name='res.company',
        default=lambda self: self.env.user.company_id.id,
        index=True,
        string="Company",
    )
    description = fields.Text(
        copy=False,
        string="Description",
        translate=True,
    )
    element_input_count = fields.Integer(
        compute='_compute_element_input_count',
        string="Element Input Count",
    )
    element_output_count = fields.Integer(
        compute='_compute_element_output_count',
        string="Element Output Count",
    )
    name = fields.Char(
        copy=False,
        required=True,
        string="Name",
        translate=True,
    )
    rule_type = fields.Selection(
        required=True,
        selection=[
            ('report_input', "Report Input"),
            ('report_output', "Report Output"),
        ],
        string="Rule Type",
    )
    sequence = fields.Integer(
        string="Sequence",
    )
    technical_data = fields.Text(
        copy=False,
        readonly=True,
        string="Technical Data",
    )
    technical_name = fields.Char(
        copy=False,
        index=True,
        string="Technical Name",
    )
    technical_status = fields.Char(
        copy=False,
        readonly=True,
        string="Technical Status",
    )
    technical_timestamp = fields.Datetime(
        copy=False,
        readonly=True,
        string="Technical Timestamp",
    )
    technical_type = fields.Char(
        copy=False,
        string="Technical Type",
    )
    # # CODE
    code_method = fields.Char(
        copy=False,
        string="Code Method",
    )
    code_parameters = fields.Text(
        copy=False,
        string="Code Parameters",
    )
    code_result = fields.Text(
        copy=False,
        string="Code Result",
    )
    # # DOMAIN & SEARCH
    account_move_domain = fields.Text(
        string="Account Move Domain",
    )
    account_move_line_domain = fields.Text(
        string="Account Move Line Domain",
    )
    custom_domain = fields.Text(
        string="Custom Domain",
    )
    partner_domain = fields.Text(
        string="Partner Domain",
    )
    product_domain = fields.Text(
        string="Product Domain",
    )
    search_limit = fields.Integer(
        default=0,
        string="Search Limit",
    )
    search_order = fields.Char(
        copy=False,
        string="Search Order",
    )
    # # MODEL & FIELD
    ir_model = fields.Many2one(
        comodel_name='ir.model',
        copy=True,
        index=True,
        ondelete='cascade',
        string="Model",
    )
    ir_model_field = fields.Many2one(
        comodel_name='ir.model.fields',
        copy=True,
        index=True,
        ondelete='cascade',
        string="Model Field",
    )
    ir_model_field_name = fields.Char(
        index=True,
        related='ir_model_field.name',
        store=True,
        string="Model Field Technical Name",
    )
    ir_model_name = fields.Char(
        index=True,
        related='ir_model.model',
        store=True,
        string="Model Technical Name",
    )
    # # REPORT
    report_template = fields.Many2many(
        column1='rule',
        column2='template',
        comodel_name='l10n.hu.nav.report.template',
        relation='l10n_hu_nav_report_rule_report_template',
        string="NAV Report Template",
    )
    report_data_category = fields.Many2one(
        comodel_name='l10n.hu.tag',
        domain=[('tag_type', '=', 'nav_report_data_category')],
        index=True,
        string="Report Data Category",
    )
    report_data_category_technical_name = fields.Char(
        related='report_data_category.technical_name',
        string="Report Data Category Technical Name",
    )
    report_data_locked = fields.Boolean(
        default=False,
        string="Report Data Locked",
    )
    report_data_tag = fields.Many2many(
        comodel_name='l10n.hu.tag',
        column1='object',
        column2='tag',
        domain=[('tag_type', 'in', ['general', 'nav_report_data_tag'])],
        index=True,
        relation='l10n_hu_nav_report_rule_report_data_tag_rel',
        string="Report Data Tag",
    )
    # # VALUE SETTING
    numeric_decimal = fields.Integer(
        string="Numeric Decimal",
    )
    numeric_processing = fields.Selection(
        selection=[
            ('total', "Total"),
        ],
        string="Numeric Processing",
    )
    numeric_rounding = fields.Float(
        string="Numeric Rounding",
    )
    numeric_signing = fields.Selection(
        selection=[
            ('final_abs', "Final Absolute"),
            ('item_abs', "Item Absolute"),
        ],
        string="Numeric Signing",
    )
    value_method = fields.Selection(
        default='field',
        required=True,
        selection=[
            ('code', "Code"),
            ('field', "Field"),
            ('filter', "Filter"),
            ('fixed', "Fixed"),
        ],
        string="Value Method",
    )
    value_translatable = fields.Boolean(
        default=False,
        string="Translatable Value",
    )
    value_type = fields.Selection(
        selection=[
            ('boolean', "Boolean"),
            ('char', "Single Line Text"),
            ('date', "Date"),
            ('datetime', "Date and Time"),
            ('float', "Decimal Number"),
            ('html', "HTML"),
            ('integer', "Whole Number"),
            ('text', "Multi Line Text"),
        ],
        string="Value Type",
    )
    # # VALUE STORAGE
    value_boolean = fields.Boolean(
        default=False,
        string="Boolean Value",
    )
    value_char = fields.Char(
        string="Single Line Text Value",
    )
    value_char_translatable = fields.Char(
        string="Translatable Single Line Text",
    )
    value_date = fields.Date(
        string="Date Value",
    )
    value_datetime = fields.Datetime(
        string="Datetime Value",
    )
    value_float = fields.Float(
        string="Decimal Number Value",
    )
    value_html = fields.Html(
        string="HTML",
    )
    value_html_translatable = fields.Html(
        string="Translatable HTML",
        translate=True,
    )
    value_integer = fields.Integer(
        string="Whole Number Value",
    )
    value_text = fields.Text(
        string="Multi Line Text",
    )
    value_text_translatable = fields.Text(
        string="Translatable Multi Line Text",
        translate=True,
    )

    # Compute and search fields, in the same order of field declarations
    def _compute_element_input_count(self):
        for record in self:
            record.element_input_count = self.env['l10n.hu.nav.report.element'].search_count([
                ('input_rule', '=', record.id),
            ])

    def _compute_element_output_count(self):
        for record in self:
            record.element_output_count = self.env['l10n.hu.nav.report.element'].search_count([
                ('output_rule', '=', record.id),
            ])

    # Constraints and onchanges

    # CRUD methods (and name_get, name_search, ...) overrides
    def name_get(self):
        # Initialize result
        result = []

        # Iterate through self
        for record in self:
            # Set name
            if record.name:
                name = record.name
            else:
                name = str(record.id)

            # Append to list
            result.append((record.id, name))

        # Return
        return result

    # Action methods
    def action_list_input_rule_elements(self):
        """ List related elements """
        # Ensure one
        self.ensure_one()

        # Assemble result
        result = {
            'name': _("NAV Report Element"),
            'domain': [('input_rule', '=', self.id)],
            'res_model': 'l10n.hu.nav.report.element',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
        }

        # Return result
        return result

    def action_list_output_rule_elements(self):
        """ List related elements """
        # Ensure one
        self.ensure_one()

        # Assemble result
        result = {
            'name': _("NAV Report Element"),
            'domain': [('output_rule', '=', self.id)],
            'res_model': 'l10n.hu.nav.report.element',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
        }

        # Return result
        return result

    # Business methods
