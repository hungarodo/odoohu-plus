# -*- coding: utf-8 -*-
# 1 : imports of python lib

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 : imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuNavReportTemplate(models.Model):
    # Private attributes
    _name = 'l10n.hu.nav.report.template'
    _description = "HU NAV Report Template"
    _inherit = ['mail.activity.mixin', 'mail.thread']
    _order = 'id desc'

    # Default methods
    @api.model
    def _get_mail_template_domain(self):
        model = self.env['ir.model'].sudo().search([
            ('model', '=', 'l10n.hu.nav.report')
        ])

        return [('model_id', '=', model.id)]

    # Field declarations
    active = fields.Boolean(
        default=True,
        string="Active",
    )
    background_image = fields.Binary(
        copy=True,
        string="Background Image",
    )
    category = fields.Many2one(
        comodel_name='l10n.hu.tag',
        domain=[('technical_name', 'ilike', 'nav_report')],
        index=True,
        string="Category",
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
    cover_image = fields.Binary(
        copy=True,
        string="Quotation Cover Image",
    )
    description = fields.Text(
        copy=False,
        string="Description",
        translate=True,
    )
    element = fields.One2many(
        comodel_name='l10n.hu.nav.report.element',
        copy=True,
        inverse_name='template',
        string="Element",
    )
    element_count = fields.Integer(
        compute='_compute_element_count',
        string="Element Count",
    )
    name = fields.Char(
        copy=False,
        required=True,
        string="Name",
        translate=True,
    )
    mail_template = fields.Many2one(
        comodel_name='mail.template',
        domain=_get_mail_template_domain,
        index=True,
        string="Mail Template",
    )
    subtitle = fields.Char(
        copy=True,
        string="Subtitle",
        translate=True,
    )
    subtitle_html = fields.Html(
        copy=True,
        string="Subtitle HTML",
        translate=True,
    )
    subtitle_use_html = fields.Boolean(
        copy=True,
        default=False,
        string="Subtitle Use HTML",
    )
    tag = fields.Many2many(
        column1='template',
        column2='tag',
        comodel_name='l10n.hu.tag',
        domain=[('tag_type', 'in', ['general', 'nav_report'])],
        index=True,
        relation='l10n_hu_nav_report_template_tag_rel',
        string="Tag",
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
    template_type = fields.Selection(
        default='sale',
        selection=[
            ('sale', "Sale")
        ],
        string="Template Type",
    )
    title = fields.Char(
        copy=True,
        string="Title",
        translate=True,
    )
    title_html = fields.Html(
        copy=True,
        string="Title HTML",
        translate=True,
    )
    title_image = fields.Binary(
        copy=True,
        string="Title Image",
    )
    title_use_html = fields.Boolean(
        copy=True,
        default=False,
        string="Title Use HTML",
    )
    version = fields.Char(
        copy=False,
        string="Version",
    )
    use_cover = fields.Boolean(
        default=False,
        string="Use Cover",
    )

    # Compute and search fields, in the same order of field declarations
    def _compute_element_count(self):
        for record in self:
            record.element_count = self.env['l10n.hu.nav.report.element'].search_count([
                ('template', '=', record.id),
            ])

    # Constraints and onchanges

    # Compute and search fields, in the same order of field declarations

    # CRUD methods (and name_get, name_search, ...) overrides

    # Action methods
    def action_list_elements(self):
        """ List related elements """
        # Ensure one
        self.ensure_one()

        # Set views
        form_view = self.env.ref('l10n_hu_nav_report.nav_report_element_view_form')
        list_view = self.env.ref('l10n_hu_nav_report.nav_report_element_view_list_template')

        # Assemble result
        result = {
            'name': _("Elements"),
            'domain': [('template', '=', self.id)],
            'res_model': 'l10n.hu.nav.report.element',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'views': [(list_view.id, 'tree'), (form_view.id, 'form')],
        }

        # Return result
        return result

    # Business methods
    @api.model
    def create_nav_report_from_template(self, values):
        """ Create report based on a template

         :param values: dictionary

         :return: dictionary
         """
        # raise exceptions.UserError("create_nav_report_from_template BEGIN" + str(values))

        # Initialize variables
        create_values = {}
        debug_list = []
        error_list = []
        info_list = []
        nav_report = False
        result = {}
        warning_list = []

        # Set nav_report_template
        if values.get('nav_report_template'):
            nav_report_template = values['nav_report_template']
            debug_list.append("nav_report_template set from values: " + str(nav_report_template.id))
        elif len(self) == 1 and self.id:
            nav_report_template = self
            debug_list.append("nav_report_template set from self: " + str(nav_report_template.id))
        else:
            nav_report_template = False
            error_list.append("nav_report_template not set")

        if len(error_list) == 0:
            create_values.update({
                'company': nav_report_template.company.id,
                'template': nav_report_template.id,
            })

        if len(error_list) == 0:
            nav_report = self.env['l10n.hu.nav.report'].create(create_values)

        # Update result
        result.update({
            'create_values': create_values,
            'debug_list': debug_list,
            'error_list': error_list,
            'info_list': info_list,
            'nav_report': nav_report,
            'nav_report_template': nav_report_template,
            'warning_list': warning_list,
        })

        # Return result
        # raise exceptions.UserError("create_nav_report_from_template END" + str(result))
        return result
