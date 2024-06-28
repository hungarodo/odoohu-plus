# -*- coding: utf-8 -*-
# 1 : imports of python lib

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 : imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuPlusUomUom(models.Model):
    # Private attributes
    _inherit = 'uom.uom'

    # Default methods
    @api.model
    def _get_selection_l10n_hu_type(self):
        return self.l10n_hu_get_type_selection()

    # Field declarations
    l10n_hu_type = fields.Selection(
        selection=_get_selection_l10n_hu_type,
        string="HU Type",
    )

    # Compute and search fields, in the same order of field declarations

    # Constraints and onchanges

    # CRUD methods (and name_get, name_search, ...) overrides

    # Action methods

    # Business methods
    @api.model
    def l10n_hu_get_type_selection(self):
        """ Get a selection field compatible list of HU types

        :return: list
        """
        # Assemble result
        result = [
            ('piece', "Piece"),
            ('kilogram', "Kilogram"),
            ('ton', "Ton"),
            ('kwh', "Kilowatt Hour"),
            ('day', "Day"),
            ('hour', "Hour"),
            ('minute', "Minute"),
            ('month', "Month"),
            ('liter', "Liter"),
            ('kilometer', "Kilometer"),
            ('cubic_meter', "Cubic Meter"),
            ('meter', "Meter"),
            ('linear_meter', "Linear Meter"),
            ('carton', "Carton"),
            ('pack', "Pack"),
            ('own', "Own"),
        ]

        # Return result
        return result

    @api.model
    def l10n_hu_get_types(self):
        """ Get list of HU types

        NOTE:
        - we call type selection and assemble list

        :return: list
        """
        # Initialize variables
        result = []

        # Get selection
        selection_list = self.l10n_hu_get_type_selection()

        # Assemble result
        for selection in selection_list:
            result.append(selection[0])

        # Return result
        return result
