# -*- coding: utf-8 -*-
# 1 : imports of python lib
import datetime
import json
import random
import string
import uuid

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models, tools  # alphabetically ordered

# 3 : imports from odoo modules
from odoo.tools.translate import html_translate

# 4 : variable declarations


# Class
class L10nHuBaseObject(models.Model):
    # Private attributes
    _name = 'l10n.hu.object'
    _description = "Hungary Object"
    _inherit = ['image.mixin', 'mail.activity.mixin', 'mail.thread']
    _order = 'name asc, id desc'

    # Default methods

    # Field declarations
    active = fields.Boolean(
        default=True,
        string="Active",
    )
    category_tag = fields.Many2one(
        comodel_name='l10n.hu.tag',
        domain=[('tag_type', '=', 'object_category')],
        index=True,
        string="Category",
    )
    category_technical_name = fields.Char(
        related='category_tag.technical_name',
        string="Category Technical Name",
    )
    code = fields.Char(
        copy=False,
        string="Code",
    )
    collection_tag = fields.Many2one(
        comodel_name='l10n.hu.tag',
        domain=[('tag_type', '=', 'object_collection')],
        index=True,
        store=True,
        string="Collection",
    )
    collection_technical_name = fields.Char(
        related='collection_tag.technical_name',
        string="Collection Technical Name",
    )
    color = fields.Integer(
        string="Color",
    )
    company = fields.Many2one(
        comodel_name='res.company',
        default=lambda self: self.env.company.id,
        index=True,
        readonly=True,
        string="Company",
    )
    description = fields.Text(
        copy=False,
        string="Description",
    )
    external_id = fields.Char(
        copy=False,
        string="External ID",
    )
    html_content = fields.Html(
        copy=False,
        index=True,
        sanitize_attributes=False,
        sanitize_form=False,
        string="HTML Content",
        translate=html_translate,
    )
    key = fields.Char(
        copy=False,
        index=True,
        string="Key",
    )
    name = fields.Char(
        copy=False,
        index=True,
        string="Name",
    )
    priority = fields.Integer(
        copy=False,
        index=True,
        string="Priority",
    )
    reference = fields.Char(
        copy=False,
        readonly=True,
        index=True,
        string="Reference",
    )
    status_tag = fields.Many2one(
        comodel_name='l10n.hu.tag',
        domain=[('tag_type', '=', 'object_status')],
        index=True,
        string="Object Status",
    )
    status_technical_name = fields.Char(
        related='status_tag.technical_name',
        string="Status Technical Name",
    )
    tag = fields.Many2many(
        comodel_name='l10n.hu.tag',
        column1='object',
        column2='tag',
        domain=[('tag_type', 'in', ['general', 'object'])],
        index=True,
        relation='l10n_hu_object_tag_rel',
        string="Tag",
    )
    technical_data = fields.Text(
        copy=False,
        string="Technical Data",
    )
    technical_data_type = fields.Char(
        copy=False,
        string="Technical Data Type",
    )
    technical_name = fields.Char(
        copy=False,
        index=True,
        string="Technical Name",
    )
    type_tag = fields.Many2one(
        comodel_name='l10n.hu.tag',
        domain=[('tag_type', '=', 'object_type')],
        index=True,
        string="Object Type",
    )
    type_technical_name = fields.Char(
        related='type_tag.technical_name',
        index=True,
        store=True,
        string="Type Technical Name",
    )
    url = fields.Char(
        copy=False,
        index=True,
        size=1024,
        string="Url",
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
            if record.name:
                name = record.name
            else:
                name = record.id

            # Append to list
            result.append((record.id, name))

        # Return
        return result

    # Action methods
    def action_generate_key(self):
        # Ensure one record in self
        self.ensure_one()

        # Get
        if self.object_type \
                and self.object_type.key_regeneration \
                and self.object_type.key_automation == 'uuid4':
            self.key = self.get_uuid4()
        else:
            return

    # Business methods
    @api.model
    def generate_random_string(self, values=None):
        """ Generate a random string

        :param values: optional dictionary of parameters, including:
            - length: integer
            - letters: lowercase | uppercase | both | none
            - numbers: boolean
            - prefix: string
            - start_with_letter: boolean
            - suffix: string

        :return string
        """
        # Initialize variables
        result = ""

        # Set letters
        if values and values.get('letters'):
            letters = values['letters']
        elif self.object_type and self.object_type.random_name_letters:
            letters = self.object_type.random_name_letters
        else:
            letters = "both"

        # Set numbers
        if values and values.get('numbers') is not None and values.get('numbers'):
            numbers = True
        elif values and values.get('numbers') is not None and not values.get('numbers'):
            numbers = False
        elif self.object_type and self.object_type.random_name_numbers:
            numbers = True
        elif self.object_type and not self.object_type.random_name_numbers:
            numbers = False
        else:
            numbers = True

        # Set prefix
        if values and values.get('prefix'):
            result += values['prefix']
        elif self.object_type and self.object_type.random_name_prefix:
            result += self.object_type.random_name_prefix
        else:
            pass

        # Set length
        if values and values.get('length'):
            length = values['length']
        elif self.object_type and self.object_type.random_name_length:
            length = self.object_type.random_name_length
        else:
            length = 8

        # Start with letter
        if values and values.get('start_with_letter'):
            if letters == 'both' and numbers:
                result += random.choice(string.ascii_uppercase + string.ascii_lowercase)
            elif letters == 'lowercase' and numbers:
                result += random.choice(string.ascii_lowercase)
            elif letters == 'uppercase' and numbers:
                result += random.choice(string.ascii_uppercase)
            else:
                result += random.choice(string.ascii_uppercase + string.ascii_lowercase)
            length = length - 1
        elif self.object_type and self.object_type.random_name_start_with_letter:
            if letters == 'both' and numbers:
                result += random.choice(string.ascii_uppercase + string.ascii_lowercase)
            elif letters == 'lowercase' and numbers:
                result += random.choice(string.ascii_lowercase)
            elif letters == 'uppercase' and numbers:
                result += random.choice(string.ascii_uppercase)
            else:
                result += random.choice(string.ascii_uppercase + string.ascii_lowercase)
            length = length - 1
        else:
            pass

        # Iterate for random characters
        for i in range(length):
            if letters == 'both' and numbers:
                result += random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase)
            elif letters == 'lowercase' and numbers:
                result += random.choice(string.digits + string.ascii_lowercase)
            elif letters == 'uppercase' and numbers:
                result += random.choice(string.digits + string.ascii_lowercase)
            elif letters == 'none' and numbers:
                result += random.choice(string.digits + string.ascii_lowercase)
            else:
                result += random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase)

        # Set suffix
        if values and values.get('suffix'):
            result += values['suffix']
        elif self.object_type and self.object_type.random_name_suffix:
            result += self.object_type.random_name_suffix
        else:
            pass

        # Return
        return result

    @api.model
    def get_uuid4(self):
        """ Get uuid4

        :return string
        """
        # Generate uuid4
        result = uuid.uuid4()

        # Return
        return result
