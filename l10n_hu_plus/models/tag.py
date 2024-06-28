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
    _order = 'name asc, id desc'

    # Default methods
    @api.model
    def _get_default_color(self):
        return randint(1, 11)

    # Field declarations
    active = fields.Boolean(
        default=True,
        string="Active",
    )
    code = fields.Char(
        index=True,
        string="Code",
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
    name = fields.Char(
        index=True,
        required=True,
        string="Name",
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
            ('object_category', "Object Category"),
            ('object_collection', "Object Collection"),
            ('object_type', "Object Type"),
            ('technical', "Technical"),
        ],
        string="Tag Type",
    )
    technical_name = fields.Char(
        index=True,
        string="Technical Name",
    )
    
    # Compute and search fields, in the same order of field declarations
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
            'view_mode': 'tree,form',
        }

        # Return result
        return result

    # Business methods
