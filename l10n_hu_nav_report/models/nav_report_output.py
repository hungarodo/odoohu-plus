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
    line_section_table_heading = fields.Boolean(
        default=True,
        string="Section Table Heading",
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
    output_type = fields.Selection(
        default='char',
        required=True,
        selection=[
            ('html', "HTML"),
            ('char', "Single Line Text"),
            ('date', "Date"),
            ('datetime', "Date and Time"),
            ('float', "Decimal Number"),
            ('integer', "Whole Number"),
            ('text', "Multi Line Text"),
        ],
        string="Output Type",
    )
    page_break = fields.Boolean(
        default=False,
        string="Page Break"
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
    value_boolean = fields.Boolean(
        default=False,
        string="Boolean Value",
    )
    value_char = fields.Char(
        string="Single Line Text Value",
    )
    value_date = fields.Date(
        string="Date Value",
    )
    value_datetime = fields.Datetime(
        string="Datetime Value",
    )
    value_display = fields.Char(
        compute='_compute_value_display',
        store=True,
        string="Display Value",
    )
    value_float = fields.Float(
        string="Decimal Number Value",
    )
    value_html = fields.Html(
        string="HTML",
        translate=True,
    )
    value_integer = fields.Integer(
        string="Whole Number Value",
    )
    value_rule = fields.Many2one(
        comodel_name='l10n.hu.nav.report.rule',
        copy=True,
        index=True,
        string="Value Rule",
    )
    value_text = fields.Text(
        string="Multi Line Text Value",
        translate=True,
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

    # Compute and search fields, in the same order of field declarations
    @api.depends(
        'value_boolean',
        'value_char',
        'value_date',
        'value_datetime',
        'value_float',
        'value_html',
        'value_integer',
        'value_text',
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
            'output_type': nav_report_output.output_type,
            'sequence': nav_report_output.sequence,
            'technical_name': nav_report_output.technical_name,
        }

        # Process value_type
        if len(error_list) == 0:
            if self.value_type == 'char':
                output_data.update({
                    'value':  self.value_char,
                    'value_formatted':  self.value_char,
                })
            elif self.value_type == 'float':
                output_data.update({
                    'value':  self.value_float,
                    'value_formatted':  self.value_float,
                })
            elif self.value_type == 'html':
                output_data.update({
                    'value': self.render_value_html(values),
                    'value_formatted': self.value_html,
                })
            elif self.value_type == 'integer':
                output_data.update({
                    'value': self.value_integer,
                    'value_formatted': self.value_integer,
                })
            elif self.value_type == 'text':
                output_data.update({
                    'value': self.value_text,
                    'value_formatted': self.value_text,
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
        elif self.value_type == 'date':
            result = str(self.value_date)
        elif self.value_type == 'datetime':
            result = str(self.value_datetime)
        elif self.value_type == 'float':
            result = str(self.value_float)
        elif self.value_type == 'html' and self.value_html:
            result = str(self.value_html[:64])
        elif self.value_type == 'integer':
            result = str(self.value_integer)
        elif self.value_type == 'text' and self.value_text:
            result = str(self.value_text[:64])
        else:
            result = _("Value display error!")

        # Return result
        return result
