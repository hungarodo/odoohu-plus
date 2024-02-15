# -*- coding: utf-8 -*-
# 1 : imports of python lib

# 2 : imports of odoo
from odoo import _, exceptions, api, fields, models  # alphabetically ordered

# 3 : imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuInvoiceLink(models.Model):
    # Private attributes
    _name = 'l10n.hu.invoice.link'
    _description = "HU Invoice Link"

    # Default methods

    # Field declarations
    active = fields.Boolean(
        default=True,
        index=True,
        string="Active",
    )
    company = fields.Many2one(
        comodel_name='res.company',
        default=lambda self: self.env.company.id,
        index=True,
        readonly=True,
        string="Company",
    )
    link_type = fields.Selection(
        selection=[
            ('advance', "Advance"),
            ('cancellation', "Cancellation"),
            ('copy', "Copy"),
            ('generic', "Generic"),
            ('modification', "Modification"),
            ('proforma', "Proforma"),
        ],
        index=True,
        string="Link Type",
    )
    priority = fields.Integer(
        string="Priority"
    )
    link_from_invoice = fields.Many2one(
        comodel_name='account.move',
        index=True,
        ondelete='cascade',
        required=True,
        string="Link From",
    )
    link_from_name = fields.Char(
        compute='_compute_name',
        string="Link From Name",
    )
    link_to_invoice = fields.Many2one(
        comodel_name='account.move',
        index=True,
        ondelete='cascade',
        required=True,
        string="Link To Invoice",
    )
    link_to_name = fields.Char(
        compute='_compute_name',
        string="Link To Name",
    )

    # Compute and search fields, in the same order of field declarations
    def _compute_name(self):
        for record in self:
            # Get link_type_dict
            link_type_dict = record.get_link_type_dict()

            # Set
            if record.link_type\
                    and record.link_type == 'advance'\
                    and link_type_dict.get('advance') \
                    and link_type_dict['advance'].get('link_from_advance') \
                    and link_type_dict['advance'].get('link_to_advance'):
                record.link_from_name = link_type_dict['advance']['link_from_advance']
                record.link_to_name = link_type_dict['advance']['link_to_advance']
            elif record.link_type \
                    and record.link_type == 'cancellation' \
                    and link_type_dict.get('cancellation') \
                    and link_type_dict['cancellation'].get('link_from_cancellation') \
                    and link_type_dict['cancellation'].get('link_to_cancellation'):
                record.link_from_name = link_type_dict['cancellation']['link_from_cancellation']
                record.link_to_name = link_type_dict['cancellation']['link_to_cancellation']
            elif record.link_type \
                    and record.link_type == 'copy' \
                    and link_type_dict.get('copy') \
                    and link_type_dict['copy'].get('link_from_copy') \
                    and link_type_dict['copy'].get('link_to_copy'):
                record.link_from_name = link_type_dict['copy']['link_from_copy']
                record.link_to_name = link_type_dict['copy']['link_to_copy']
            elif record.link_type\
                    and record.link_type == 'modification'\
                    and link_type_dict.get('modification') \
                    and link_type_dict['modification'].get('link_from_modification') \
                    and link_type_dict['modification'].get('link_to_modification'):
                record.link_from_name = link_type_dict['modification']['link_from_modification']
                record.link_to_name = link_type_dict['modification']['link_to_modification']
            elif record.link_type\
                    and record.link_type == 'generic'\
                    and link_type_dict.get('generic') \
                    and link_type_dict['generic'].get('link_from_generic') \
                    and link_type_dict['generic'].get('link_to_generic'):
                record.link_from_name = link_type_dict['generic']['link_from_generic']
                record.link_to_name = link_type_dict['generic']['link_to_generic']
            elif record.link_type\
                    and record.link_type == 'proforma'\
                    and link_type_dict.get('proforma') \
                    and link_type_dict['proforma'].get('link_from_proforma') \
                    and link_type_dict['proforma'].get('link_to_proforma'):
                record.link_from_name = link_type_dict['proforma']['link_from_proforma']
                record.link_to_name = link_type_dict['proforma']['link_to_proforma']
            else:
                record.link_from_name = _("No link!")
                record.link_to_name = _("No link!")

    # Constraints and onchanges

    # CRUD methods (and name_get, name_search, ...) overrides
    def name_get(self):
        # Initialize result
        result = []

        # Iterate through self
        for record in self:
            # Set name
            if record.link_type and record.link_from_invoice and record.link_to_invoice:
                name = "[" + str(record.link_type) + "] "
                name += record.link_from_invoice.display_name + "[ID:" + str(record.link_from_invoice.id) + "]"
                name += " - "
                name += record.link_to_invoice.display_name + "[ID:" + str(record.link_to_invoice.id) + "]"
            else:
                name = record.name

            # Append to list
            result.append((record.id, name))

        # Return
        return result

    # Action methods
    def action_view_link_from_invoice(self):
        """ Open the link from invoice """
        # Ensure one
        self.ensure_one()

        # View
        return {
            'name': _("Invoice"),
            'res_id': self.link_from_invoice.id,
            'res_model': 'account.move',
            'target': 'current',
            'type': 'ir.actions.act_window',
            'view_mode': 'form,tree',
        }

    def action_view_link_to_invoice(self):
        """ Open the link to invoice """
        # Ensure one
        self.ensure_one()

        # View
        return {
            'name': _("Invoice"),
            'res_id': self.link_to_invoice.id,
            'res_model': 'account.move',
            'target': 'current',
            'type': 'ir.actions.act_window',
            'view_mode': 'form,tree',
        }

    # Business methods
    @api.model
    def get_link_type_selection(self):
        """ Selection list of available links

        :return list
        """
        # Get dict
        link_type_dict = self.get_link_type_dict()

        # Initialize variables
        result = []

        # Iterate
        for key, value in link_type_dict.items():
            for selection_key, selection_value in value.items():
                result.append((selection_key, selection_value))

        # Return
        return result

    @api.model
    def get_link_type_dict(self):
        """ Dictionary of available link types

        Override with super when needed

        :return: dictionary
        """
        # Initialize variables
        result = {
            'advance': {
                'link_from_advance': _("Advance Invoice"),
                'link_to_advance': _("Delivery Invoice"),
            },
            'cancellation': {
                'link_from_cancellation': _("Cancelled Invoice"),
                'link_to_cancellation': _("Cancellation Invoice"),
            },
            'copy': {
                'link_from_copy': _("Copied From Invoice"),
                'link_to_copy': _("Copied To Invoice"),
            },
            'generic': {
                'link_from_generic': _("Related Invoice"),
                'link_to_generic': _("Related Invoice"),
            },
            'modification': {
                'link_from_modification': _("Modified Invoice"),
                'link_to_modification': _("Modification Invoice"),
            },
            'proforma': {
                'link_from_proforma': _("Proforma"),
                'link_to_proforma': _("Advance Invoice"),
            },
        }

        # Return
        return result

    @api.model
    def get_link_type_from_selection_key(self, selection_key):
        """ Get link type from a selection key

        :param selection_key: string

        :return list
        """
        # Get dict
        link_type_dict = self.get_link_type_dict()

        # Initialize variables
        result = []

        # Iterate
        for link_type_key, link_type_value in link_type_dict.items():
            for value_key, value_value in link_type_value.items():
                if value_key == selection_key:
                    result = link_type_key
                    break

        # Return
        return result
