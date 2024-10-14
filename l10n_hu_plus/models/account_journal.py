# -*- coding: utf-8 -*-
# 1 : imports of python lib

# 2 :  imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 :  imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuPlusAccountJournal(models.Model):
    # Private attributes
    _inherit = 'account.journal'

    # Default methods
    def _get_default_l10n_hu_proforma_mail_template_domain(self):
        return [('model_id', '=', self.env.ref('account.model_account_move').id)]

    # Field declarations
    l10n_hu_banner_enabled = fields.Boolean(
        copy=False,
        default=True,
        index=True,
        string="HU Banner Enabled",
    )
    l10n_hu_delivery_date_default = fields.Selection(
        copy=False,
        default='none',
        selection=[
            ('none', "None"),
            ('today', "Today"),
        ],
        string="HU Delivery Date Default",
    )
    l10n_hu_document_type = fields.Many2many(
        column1='journal',
        column2='document_type',
        comodel_name='l10n.hu.plus.object',
        domain=[('type_technical_name', '=', 'document_type')],
        index=True,
        relation='l10n_hu_journal_document_type_rel',
        string="HU Document Type",
    )
    l10n_hu_plus_enabled = fields.Boolean(
        copy=False,
        default=True,
        index=True,
        string="HU+ Enabled",
    )
    l10n_hu_priority = fields.Integer(
        copy=False,
        default=10,
        index=True,
        string="HU Priority",
    )
    l10n_hu_proforma_mail_template = fields.Many2one(
        comodel_name='mail.template',
        copy=False,
        domain=_get_default_l10n_hu_proforma_mail_template_domain,
        index=True,
        string="HU Proforma Mail Template",
    )
    l10n_hu_proforma_sequence = fields.Many2one(
        comodel_name='ir.sequence',
        copy=False,
        domain=[('code', 'like', 'proforma')],
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
    def action_l10n_hu_plus_documentation(self):
        """ HU+ documentation """
        # Make sure there is one record in self
        self.ensure_one()

        # Return
        return {
            'target': 'new',
            'type': 'ir.actions.act_url',
            'url': 'https://hungarodo.atlassian.net/wiki/spaces/ODOOHU',
        }

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
