# -*- coding: utf-8 -*-
# 1 : imports of python lib

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 : imports from odoo modules
from odoo.tools.safe_eval import safe_eval

# 4 : variable declarations


# Class
class L10nHuNavReportOutput(models.Model):
    # Private attributes
    _name = 'l10n.hu.nav.report.output'
    _description = "HU NAV Report Output"
    _inherit = ['mail.activity.mixin', 'mail.thread']
    _order = 'id desc'

    # Default methods

    # Field declarations
    active = fields.Boolean(
        related='report.active',
        store=True,
        string="Active",
    )
    code = fields.Char(
        string="Code",
    )
    company = fields.Many2one(
        index=True,
        related='report.company',
        store=True,
        string="Company",
    )
    description = fields.Text(
        copy=False,
        string="Description",
        translate=True,
    )
    element = fields.Many2one(
        comodel_name='l10n.hu.nav.report.element',
        index=True,
        ondelete='cascade',
        string="Element",
    )
    locked = fields.Boolean(
        default=False,
        string="Locked",
    )
    name = fields.Char(
        string="Name",
    )
    notes = fields.Text(
        help="Internal notes",
        string="Notes",
    )
    reference = fields.Char(
        string="Reference",
    )
    report = fields.Many2one(
        comodel_name='l10n.hu.nav.report',
        index=True,
        ondelete='cascade',
        string="Report",
    )
    sequence = fields.Integer(
        string="Sequence",
    )
    template = fields.Many2one(
        comodel_name='l10n.hu.nav.report.template',
        index=True,
        ondelete='cascade',
        string="Template",
    )
    technical_name = fields.Char(
        string="Technical Name",
    )
    # # PRINT
    line_section_table_heading = fields.Boolean(
        default=True,
        string="Section Table Heading",
    )
    page_break = fields.Boolean(
        default=False,
        string="Page Break"
    )
    # # VALUE
    value_display = fields.Char(
        compute='_compute_value_display',
        store=True,
        string="Display Value",
    )
    value_rule = fields.Many2one(
        comodel_name='l10n.hu.nav.report.rule',
        copy=True,
        index=True,
        string="Value Rule",
    )
    value_type = fields.Selection(
        default='char',
        required=True,
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
    # # VALUE - STORAGE
    value_boolean = fields.Boolean(
        default=False,
        string="Boolean Value",
    )
    value_char = fields.Char(
        string="Single Line Text Value",
    )
    value_char_translatable = fields.Char(
        string="Translatable Single Line Text Value",
        translate=True,
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
        string="Multi Line Text Value",
    )
    value_text_translatable = fields.Text(
        string="Translatable Multi Line Text Value",
        translate=True,
    )

    # Compute and search fields, in the same order of field declarations
    @api.depends(
        'value_boolean',
        'value_char',
        'value_char_translatable',
        'value_date',
        'value_datetime',
        'value_float',
        'value_html',
        'value_html_translatable',
        'value_integer',
        'value_text',
        'value_text_translatable',
        'value_type',
    )
    def _compute_value_display(self):
        for record in self:
            # Compute
            value_display = record.get_value_display()

            # Set
            record.value_display = value_display

    # Constraints and onchanges

    # CRUD methods (and name_get, name_search, ...) overrides
    def name_get(self):
        # Initialize result
        result = []

        # Iterate through self
        for record in self:
            # Set name
            name = record.get_value_display()

            # Append to list
            result.append((record.id, name))

        # Return
        return result

    # Action methods

    # Business methods
    @api.model
    def get_nav_report_output_value(self, values):
        """ Get output value for a report

         :param values: dictionary

         :return: dictionary
         """
        # raise exceptions.UserError("get_nav_report_output_value BEGIN" + str(values))

        # Initialize variables
        debug_list = []
        error_list = []
        info_list = []
        result = {}
        warning_list = []

        # Set nav_report_output
        if values.get('nav_report_output'):
            nav_report_output = values['nav_report_output']
            debug_list.append("Using nav_report_output from values: " + str(nav_report_output.id))
        elif len(self) == 1 and self.id:
            nav_report_output = self
            debug_list.append("Using nav_report_output from self: " + str(nav_report_output.id))
        else:
            nav_report_output = False
            error_list.append("Could not set nav_report_output!")

        # Common
        output_data = {
            'code': nav_report_output.code,
            'sequence': nav_report_output.sequence,
            'technical_name': nav_report_output.technical_name,
            'value_type': nav_report_output.value_type,
        }

        # Process value_type
        if len(error_list) == 0:
            if nav_report_output.value_type == 'char':
                output_data.update({
                    'value':  nav_report_output.value_char,
                    'value_formatted':  nav_report_output.value_char,
                })
            elif nav_report_output.value_type == 'float':
                output_data.update({
                    'value':  nav_report_output.value_float,
                    'value_formatted':  nav_report_output.value_float,
                })
            elif nav_report_output.value_type == 'html':
                output_data.update({
                    'value': nav_report_output.render_value_html(values),
                    'value_formatted': nav_report_output.value_html,
                })
            elif nav_report_output.value_type == 'integer':
                output_data.update({
                    'value': nav_report_output.value_integer,
                    'value_formatted': nav_report_output.value_integer,
                })
            elif nav_report_output.value_type == 'text':
                output_data.update({
                    'value': nav_report_output.value_text,
                    'value_formatted': nav_report_output.value_text,
                })
            else:
                output_data.update({
                    'value': False,
                })
                error_list.append("Invalid value_type")

        # Update result
        result.update(output_data)
        result.update({
            'debug_list': debug_list,
            'error_list': error_list,
            'info_list': info_list,
            'warning_list': warning_list,
        })

        # Return result
        # raise exceptions.UserError("get_nav_report_output_value END" + str(result))
        return result

    @api.model
    def get_value_display(self):
        if self.value_type == 'boolean':
            result = str(self.value_boolean)
        elif self.value_type == 'char':
            result = self.value_char
        elif self.value_type == 'char_translatable':
            result = self.value_char_translatable
        elif self.value_type == 'date':
            result = str(self.value_date)
        elif self.value_type == 'datetime':
            result = str(self.value_datetime)
        elif self.value_type == 'float':
            result = str(self.value_float)
        elif self.value_type == 'html' and self.value_html:
            result = str(self.value_html[:64])
        elif self.value_type == 'html_translatable' and self.value_html_translatable:
            result = str(self.value_html_translatable[:64])
        elif self.value_type == 'integer':
            result = str(self.value_integer)
        elif self.value_type == 'text_translatable' and self.value_text_translatable:
            result = str(self.value_text_translatable[:64])
        else:
            result = _("Value display error!")

        # Return result
        return result
