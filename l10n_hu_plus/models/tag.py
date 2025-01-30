# -*- coding: utf-8 -*-
# 1 : imports of python lib
import datetime
import json
from random import randint

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models, tools  # alphabetically ordered

# 3 : imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuPlusTag(models.Model):
    # Private attributes
    _name = 'l10n.hu.plus.tag'
    _description = "HU+ Tag"
    _inherit = ['image.mixin', 'mail.activity.mixin', 'mail.thread']
    _order = 'priority asc, name asc, id desc'

    # Default methods
    @api.model
    def _get_default_color(self):
        return randint(1, 11)

    # Field declarations
    account_move_count = fields.Integer(
        compute='_compute_account_move_count',
        string="Account Move Count",
    )
    active = fields.Boolean(
        default=True,
        string="Active",
        tracking=True,
    )
    code = fields.Char(
        index=True,
        string="Code",
        tracking=True,
    )
    color = fields.Integer(
        default=_get_default_color,
        string="Color",
    )
    company = fields.Many2one(
        comodel_name='res.company',
        default=lambda self: self.env.company.id,
        index=True,
        readonly=True,
        required=True,
        string="Company",
    )
    description = fields.Text(
        string="Description",
    )
    locked = fields.Boolean(
        copy=False,
        default=False,
        string="Locked",
        tracking=True,
    )
    name = fields.Char(
        index=True,
        required=True,
        string="Name",
        translate=True,
    )
    object_count = fields.Integer(
        compute='_compute_object_count',
        string="Object Count",
    )
    priority = fields.Integer(
        copy=False,
        index=True,
        string="Priority",
    )
    tag_type = fields.Selection(
        copy=False,
        default='general',
        required=True,
        selection=[
            ('general', "General"),
            ('account_move', "Account Move"),
            ('document_type', "Document Type"),
            ('object_category', "Object Category"),
            ('object_collection', "Object Collection"),
            ('object_type', "Object Type"),
            ('technical', "Technical"),
        ],
        string="Tag Type",
        tracking=True,
    )
    ## KEY
    key_enabled = fields.Boolean(
        copy=False,
        default=False,
        string="Key Enabled",
    )
    key_method = fields.Selection(
        copy=False,
        selection=[
            ('uuid4', "UUID4"),
        ],
        string="Key Method",
    )
    ## TECHNICAL
    technical_data = fields.Json(
        copy=False,
        readonly=True,
        string="Technical Data",
    )
    technical_name = fields.Char(
        copy=False,
        index=True,
        string="Technical Name",
        tracking=True,
    )
    technical_timestamp = fields.Datetime(
        copy=False,
        default=fields.Datetime.now(),
        index=True,
        readonly=True,
        string="Technical Timestamp",
    )
    
    # Compute and search fields, in the same order of field declarations
    def _compute_account_move_count(self):
        for record in self:
            record.account_move_count = self.env['account.move'].search_count([
                '|',
                ('l10n_hu_document_type', '=', record.id),
                ('l10n_hu_plus_tag', '=', record.id),
            ])

    def _compute_object_count(self):
        for record in self:
            record.object_count = self.env['l10n.hu.plus.object'].search_count([
                '|', '|', '|', '|',
                ('category_tag', '=', record.id),
                ('collection_tag', '=', record.id),
                ('status_tag', '=', record.id),
                ('tag', '=', record.id),
                ('type_tag', '=', record.id),
            ])

    # Constraints and onchanges

    # CRUD methods (and display_name, name_search, ...) overrides

    # Action methods
    def action_list_account_moves(self):
        """ List related account moves """
        # Make sure only there is one record in self
        self.ensure_one()

        # Domain
        domain = ['|', ('l10n_hu_document_type', '=', self.id), ('l10n_hu_plus_tag', '=', self.id)]

        # Assemble result
        result = {
            'name': _("Account Moves"),
            'domain': domain,
            'res_model': 'account.move',
            'target': 'current',
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
        }

        # Return result
        return result

    def action_list_objects(self):
        """ List related objects """
        # Make sure only there is one record in self
        self.ensure_one()

        # Domain
        domain = [
            '|', '|', '|', '|',
            ('category_tag', '=', self.id),
            ('collection_tag', '=', self.id),
            ('status_tag', '=', self.id),
            ('tag', '=', self.id),
            ('type_tag', '=', self.id),
        ]

        # Assemble result
        result = {
            'name': _("HU+ Objects"),
            'domain': domain,
            'res_model': 'l10n.hu.plus.object',
            'target': 'current',
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
        }

        # Return result
        return result

    def action_view_technical_data(self):
        # Ensure one
        self.ensure_one()

        # data_display
        if self.technical_data:
            data_display = json.dumps(self.technical_data, default=str, indent=4)
            context = {
                'default_action_type': 'technical',
                'default_action_execute_visible': False,
                'default_technical_action': 'view_data',
                'default_technical_data_display': data_display,
            }
            result = {
                'name': _("HU+ Wizard"),
                'context': context,
                'res_model': 'l10n.hu.plus.wizard',
                'target': 'new',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
            }
            return result
        else:
            raise exceptions.UserError(_("Technical data is empty!"))

    # Business methods
