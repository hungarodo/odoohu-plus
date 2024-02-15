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
    @api.model
    def get_element_print_data(self, values):
        """ Get print data

         :param values: dictionary

         :return: dictionary
         """
        # raise exceptions.UserError("get_element_print_data BEGIN values" + str(values))

        # Initialize variables
        debug_list = []
        error_list = []
        info_list = []
        result = {}
        warning_list = []

        # Pricelist
        if values.get('pricelist'):
            pricelist = values['pricelist']
            debug_list.append("Using pricelist: " + str(pricelist.id))
        else:
            pricelist = False
            error_list.append("Could not set pricelist!")

        # Template
        if values.get('template'):
            template = values['template']
            debug_list.append("Using template: " + str(template.id))
        elif self.template:
            template = self.template
            debug_list.append("Using template: " + str(template.id))
        else:
            template = False
            error_list.append("Could not set template!")

        # Compatibility
        if pricelist and pricelist._name == 'product.pricelist' and template and template.template_type == 'sale':
            pass
        else:
            error_list.append("pricelist is not compatible with the template")

        # Common
        element_data = {
            'id': self.id,
            'description': self.description,
            'element_type': self.element_type,
            'page_break': self.page_break,
            'reference': self.reference,
            'sequence': self.sequence,
            'table_heading': self.table_heading,
            'technical_name': self.technical_name,
        }

        # Process element types
        if len(error_list) == 0:
            if self.element_type == 'pricelist_item':
                pricelist_item_result = self.get_element_print_data_pricelist_item(values)
                element_data.update({
                    'value': pricelist_item_result.get('element_data_value'),
                })
            elif self.element_type == 'product':
                product_result = self.get_element_print_data_product(values)
                element_data.update({
                    'value': product_result['element_data_value'],
                })
            elif self.element_type == 'char':
                element_data.update({
                    'value':  self.value_char,
                })
            elif self.element_type == 'html':
                element_data.update({
                    'value': self.render_value_html(values),
                })
            elif self.element_type == 'text':
                element_data.update({
                    'value': self.value_text,
                })
            else:
                element_data.update({
                    'value': False,
                })
                error_list.append("Invalid element type")

        # Update result
        result.update({
            'debug_list': debug_list,
            'error_list': error_list,
            'info_list': info_list,
            'element_data': element_data,
            'warning_list': warning_list,
        })

        # Return result
        # raise exceptions.UserError("get_element_print_data END result" + str(result))
        return result

    @api.model
    def render_value_html(self, values):
        """ Render a html field """
        if self.element_type == 'html' and self.template and values.get('print'):
            # we simulate a mail template
            result_dict = self.env['mail.template'].sudo()._render_template(
                self.value_html,
                'oregional.pricelist.print',
                [values['print'].id],
                True
            )

            # raise exceptions.UserError(str(result_dict[self.sale_order.id]))
            return result_dict[values['print'].id]
        else:
            return
