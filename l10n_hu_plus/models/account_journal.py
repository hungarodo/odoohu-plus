# -*- coding: utf-8 -*-
# 1 : imports of python lib
import datetime

# 2 :  imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 :  imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuPlusAccountJournal(models.Model):
    # Private attributes
    _inherit = 'account.journal'

    # Default methods
    @api.model
    def _get_default_l10n_hu_proforma_mail_template_domain(self):
        return [('model_id', '=', self.env.ref('account.model_account_move').id)]

    @api.model
    def _get_selection_l10n_hu_nav_payment_method(self):
        return self.env['account.payment.term'].l10n_hu_get_nav_method_selection()

    # Field declarations
    l10n_hu_banner_enabled = fields.Boolean(
        copy=False,
        default=True,
        help="Display banner on the invoice form",
        index=True,
        string="HU Banner Enabled",
    )
    l10n_hu_cron_batch = fields.Integer(
        copy=False,
        default=36,
        help="Number of items managed by scheduled action",
        string="HU Cron Batch",
    )
    l10n_hu_delivery_date_default = fields.Selection(
        copy=False,
        default='none',
        help="Used as default value (when necessary)",
        selection=[
            ('none', "None"),
            ('today', "Today"),
        ],
        string="HU Delivery Date Default",
    )
    l10n_hu_edi_sending = fields.Selection(
        copy=False,
        default='disabled',
        help="EDI (NAV Online Invoice) and email sending",
        selection=[
            ('disabled', "Disabled"),
            ('manual', "Manual"),
            ('auto_edi', "Automated EDI (no email)"),
            ('auto_edi_email', "Automated EDI & Email"),
        ],
        string="HU EDI Sending",
        tracking=True,
    )
    l10n_hu_nav_payment_method = fields.Selection(
        copy=False,
        help="Used as default value (when necessary)",
        selection=_get_selection_l10n_hu_nav_payment_method,
        string="HU NAV Payment Method",
    )
    l10n_hu_plus_enabled = fields.Boolean(
        copy=False,
        default=False,
        help="Allow HU+ features for this journal",
        index=True,
        string="HU+ Enabled",
    )
    l10n_hu_priority = fields.Integer(
        copy=False,
        default=10,
        help="Lower number means higher priority",
        index=True,
        string="HU Priority",
    )
    l10n_hu_proforma_mail_template = fields.Many2one(
        comodel_name='mail.template',
        copy=False,
        domain=_get_default_l10n_hu_proforma_mail_template_domain,
        help="Default template for proforma emails",
        index=True,
        string="HU Proforma Mail Template",
    )
    l10n_hu_proforma_sequence = fields.Many2one(
        comodel_name='ir.sequence',
        copy=False,
        domain=[('code', 'like', 'proforma')],
        help="Proforma document naming sequence",
        index=True,
        string="HU Proforma Sequence",
    )
    l10n_hu_proforma_sequence_available = fields.Boolean(
        compute='_compute_l10n_hu_proforma_sequence_available',
        string="HU Proforma Sequence Available",
    )

    # Compute and search fields, in the same order of field declarations
    def _compute_l10n_hu_proforma_sequence_available(self):
        for record in self:
            existing_sequence = self.env['ir.sequence'].search([
                ('code', 'ilike', 'proforma'),
                ('company_id', '=', record.company_id.id),
            ])
            if existing_sequence:
                record.l10n_hu_proforma_sequence_available = True
            else:
                record.l10n_hu_proforma_sequence_available = False

    # Constraints and onchanges

    # CRUD methods (and display_name, name_search, ...) overrides

    # Action methods
    def action_l10n_hu_plus_view_documentation(self):
        """ View HU+ documentation """
        # Make sure there is one record in self
        self.ensure_one()

        # Return
        return self.company_id.action_l10n_hu_plus_view_documentation()

    def action_l10n_hu_set_proforma_sequence(self):
        """ Set a proforma sequence"""
        # Ensure one record in self
        self.ensure_one()

        # Existing sequence
        existing_sequence = self.env['ir.sequence'].search([
            ('code', 'ilike', 'proforma'),
            ('company_id', '=', self.company_id.id),
        ])
        if self.l10n_hu_proforma_sequence:
            return
        elif existing_sequence:
            self.l10n_hu_proforma_sequence = existing_sequence
            return
        else:
            # Proforma default
            sequence = self.env.ref('l10n_hu_plus.proforma_sequence')
            new_sequence = self.env['ir.sequence'].create({
                'code': sequence.code,
                'company_id': self.company_id.id,
                'name': sequence.name,
                'padding': sequence.padding,
                'prefix': sequence.prefix,
            })
            self.l10n_hu_proforma_sequence = new_sequence
            return

    # Business methods
    @api.model
    def l10n_hu_get_default_document_type(self):
        return self.env['l10n.hu.plus.tag'].search([
            ('company', '=', self.company_id.id),
            ('tag_type', '=', 'document_type'),
        ], limit=1, order='priority asc, id desc')

    @api.model
    def l10n_hu_get_default_delivery_date(self):
        # date_today = fields.Date.today()
        date_today = datetime.date.today()
        if self.l10n_hu_delivery_date_default == 'none':
            return None
        elif self.l10n_hu_delivery_date_default == 'today':
            return  fields.Date.today()
        elif self.l10n_hu_delivery_date_default == 'first_day_of_this_month':
            # Replace day to first day of this month
            return date_today.replace(day=1)
        elif self.l10n_hu_delivery_date_default == 'last_day_of_this_month':
            # Get close to the end of this month and add 4 days to 'roll it over'
            next_month = date_today.replace(day=28) + datetime.timedelta(days=4)
            # Set the day to 1 gives us the start of next month
            first_day_of_next_month = next_month.replace(day=1)
            # Remove one day to get last day of this month
            return first_day_of_next_month - datetime.timedelta(days=1)
        elif self.l10n_hu_delivery_date_default == 'last_day_of_last_month':
            # Replace day to first day of this month
            first_day_of_this_month = date_today.replace(day=1)
            # Remove one day to get last day of last month
            return first_day_of_this_month - datetime.timedelta(days=1)
        elif self.l10n_hu_delivery_date_default == 'first_day_of_next_month':
            # Get close to the end of this month and add 4 days to 'roll it over'
            next_month = date_today.replace(day=28) + datetime.timedelta(days=4)
            # Set the day to 1 gives us the first day of next month
            return next_month.replace(day=1)
        else:
            return None
