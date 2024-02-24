# -*- coding: utf-8 -*-
# 1 : imports of python lib
import base64  # base64 encoding
import datetime
import hashlib  # passwords
import hmac
import json
import logging
import lxml  # xml processing
import requests  # http requests

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 : imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuBaseLog(models.Model):
    # Private attributes
    _name = 'l10n.hu.log'
    _description = "HU Log"
    _order = 'timestamp desc, id desc'

    # Default methods

    # Field declarations
    active = fields.Boolean(
        default=True,
        string="Active",
    )
    app = fields.Many2one(
        comodel_name='ir.module.module',
        index=True,
        readonly=True,
        string="App",
    )
    company = fields.Many2one(
        comodel_name='res.company',
        default=lambda self: self.env.company.id,
        readonly=True,
        required=True,
        string="Company",
    )
    description = fields.Text(
        help="Additional information",
        readonly=True,
        string="Description",
    )
    direction = fields.Selection(
        copy=False,
        selection=[
            ('incoming', "Incoming"),
            ('internal', "Internal"),
            ('outgoing', "Outgoing"),
        ],
        string="Direction",
    )
    level = fields.Selection(
        selection=[
            ('info', "INFO"),
            ('warning', "WARNING"),
            ('error', "ERROR"),
            ('debug', "DEBUG"),
        ],
        string="Level",
    )
    l10n_hu_object = fields.Many2many(
        comodel_name='l10n.hu.object',
        column1='log',
        column2='object',
        copy=False,
        readonly=True,
        relation='l10n_hu_log_object_rel',
        string="Object",
    )
    l10n_hu_object_count = fields.Integer(
        compute='_compute_l10n_hu_object_count',
        string="Object Count",
    )
    log_type = fields.Char(
        readonly=True,
        string="Log Type",
    )
    model = fields.Many2one(
        comodel_name='ir.model',
        index=True,
        readonly=True,
        string="Model",
    )
    name = fields.Char(
        readonly=True,
        string="Name",
    )
    source_model_name = fields.Char(
        copy=False,
        index=True,
        string="Source Model Name",
    )
    source_record_id = fields.Integer(
        copy=False,
        index=True,
        string="Source Record ID",
    )
    source_record_display_name = fields.Char(
        compute='_compute_source_record_info',
        string="Source Record Display Name",
    )
    status = fields.Selection(
        copy=False,
        default='new',
        readonly=True,
        selection=[
            ('new', "New"),
            ('processing', "Processing"),
            ('error', "Error"),
            ('done', "Done"),
        ],
        string="Status",
    )
    technical_data = fields.Text(
        copy=False,
        string="Technical Data",
    )
    technical_name = fields.Char(
        copy=False,
        index=True,
        string="Technical Name",
    )
    timestamp = fields.Datetime(
        copy=False,
        string="Processing Timestamp",
    )
    user_id = fields.Integer(
        readonly=True,
        string="User ID",
    )

    # Compute and search fields, in the same order of field declarations
    def _compute_l10n_hu_object_count(self):
        for record in self:
            record.l10n_hu_object_count = len(record.l10n_hu_object)

    @api.depends('source_model_name', 'source_record_id')
    def _compute_source_record_info(self):
        for record in self:
            # Initialize variables
            display_name = False

            # Get values
            if record.source_model_name and record.source_record_id:
                try:
                    source_record = self.env[record.source_model_name].sudo().search([
                        ('id', '=', record.source_record_id)
                    ])
                    if source_record:
                        display_name = source_record.display_name
                except:
                    pass

            # Set field
            record.source_record_display_name = display_name

    # Constraints and onchanges

    # CRUD methods (and name_get, name_search, ...) overrides
    def name_get(self):
        # Initialize variables
        result = []

        # Iterate through self
        for record in self:
            # Set name
            name = "HU-LOG-" + str(record.id)

            # Append to list
            result.append((record.id, name))

        # Return result
        return result

    # Action methods
    def action_delete(self):
        # Ensure one
        self.ensure_one()

        # Delete
        self.unlink()

        # Assemble result
        result = {
            'name': _("HU Logs"),
            'res_model': 'l10n.hu.log',
            'target': 'main',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
        }

        # Return result
        return result

    def action_list_objects(self):
        # Ensure one
        self.ensure_one()

        # Set l10n_hu_object_ids
        l10n_hu_object_ids = []
        for l10n_hu_object in self.l10n_hu_object:
            l10n_hu_object_ids.append(l10n_hu_object.id)

        # Assemble result
        result = {
            'name': _("HU Objects"),
            'domain': [('id', 'in', l10n_hu_object_ids)],
            'res_model': 'l10n.hu.object',
            'target': 'current',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
        }

        # Return result
        return result

    def action_view_source_record(self):
        # Ensure one
        self.ensure_one()

        if self.source_model_name and self.source_record_id:
            # Assemble result
            result = {
                'res_id': self.source_record_id,
                'res_model': self.source_model_name,
                'target': 'current',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
            }

            # Return result
            return result
        else:
            raise exceptions.UserError(_("Source record model name or source record id is empty!"))

    # Business methods
