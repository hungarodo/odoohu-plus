# -*- coding: utf-8 -*-
# 1 : imports of python lib

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models  # alphabetically ordered

# 3 : imports from odoo modules

# 4 : variable declarations


# Class
class L10nHuNavReportProduct(models.Model):
    # Private attributes
    _inherit = 'product.product'

    # Default methods

    # Field declarations

    # Compute and search fields, in the same order of field declarations

    # Constraints and onchanges

    # CRUD methods (and name_get, name_search, ...) overrides

    # Action methods

    # Business methods
    @api.model
    def l10n_hu_get_nav_report_product_scope(self):
        """ Helper method to determine the product scope for nav report """
        if self.detailed_type in ['consu', 'product']:
            return 'product'
        elif self.detailed_type == 'service':
            return 'service'
        else:
            return False
