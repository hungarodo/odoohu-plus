# -*- coding: utf-8 -*-
# 1 : imports of python lib

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 : imports from odoo modules
from odoo.tools.safe_eval import safe_eval

# 4 : variable declarations


# Class
class L10nHuNavReportElement(models.Model):
    # Private attributes
    _name = 'l10n.hu.nav.report.element'
    _description = "HU NAV Report Element"
    _order = 'id desc'

    # Default methods

    # Field declarations
    active = fields.Boolean(
        default=True,
        string="Active",
    )
    code = fields.Char(
        copy=False,
        string="Code",
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
    element_type = fields.Selection(
        default='data',
        required=True,
        selection=[
            ('data', "Data"),
            ('section', "Section"),
        ],
        string="Element Type",
    )
    line_section_table_heading = fields.Boolean(
        default=True,
        string="Section Table Heading",
    )
    name = fields.Char(
        string="Name",
        translate=True,
    )
    nav_code = fields.Char(
        string="NAV Code",
    )
    nav_column = fields.Integer(
        string="NAV Column",
    )
    nav_data_type = fields.Char(
        string="NAV Data Type",
    )
    nav_dynamic = fields.Boolean(
        default=False,
        string="NAV Dynamic",
    )
    nav_eazon = fields.Char(
        string="NAV EAzon",
    )
    nav_editable = fields.Boolean(
        default=False,
        string="NAV Editable",
    )
    nav_max_length = fields.Integer(
        string="NAV Max Length",
    )
    nav_name = fields.Char(
        string="NAV Name",
    )
    nav_page = fields.Char(
        string="NAV Page",
    )
    nav_form = fields.Char(
        string="NAV Form",
    )
    nav_row = fields.Integer(
        string="NAV Row",
    )
    notes = fields.Text(
        help="Internal notes",
        string="Notes",
    )
    page_break = fields.Boolean(
        default=False,
        help="Make a page break after this element",
        string="Page Break"
    )
    reference = fields.Char(
        string="Reference",
    )
    section_object = fields.Many2one(
        comodel_name='l10n.hu.object',
        domain=[('object_type_technical_name', '=', 'nav_2365_a')],
        index=True,
        string="Section Object",
    )
    sequence = fields.Integer(
        string="Sequence",
    )
    table_heading = fields.Boolean(
        default=False,
        string="Table Heading"
    )
    technical_data = fields.Text(
        copy=False,
        readonly=True,
        string="Technical Data",
    )
    technical_name = fields.Char(
        copy=False,
        index=True,
        readonly=True,
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
        readonly=True,
        string="Technical Type",
    )
    template = fields.Many2one(
        comodel_name='l10n.hu.nav.report.template',
        index=True,
        ondelete='cascade',
        string="Template",
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
    value_method = fields.Selection(
        default='fixed',
        required=True,
        selection=[
            ('rule', "Rule"),
            ('manual', "Manual"),
            ('fixed', "Fixed"),
        ],
        string="Value Method",
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

    # Constraints and onchanges

    # CRUD methods (and name_get, name_search, ...) overrides
    def name_get(self):
        # Initialize result
        result = []

        # Iterate through self
        for record in self:
            # Set name
            if record.code and record.name:
                name = "[" + record.code + "] " + record.name
            elif record.name:
                name = record.name
            else:
                name = str(record.id)

            # Append to list
            result.append((record.id, name))

        # Return
        return result

    # Action methods
    def action_report_wizard(self):
        """ Start report wizard """
        # Ensure one record in self
        self.ensure_one()

        # Assemble context
        context = {
            'default_action_type_editable': True,
            'default_action_type_visible': True,
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
