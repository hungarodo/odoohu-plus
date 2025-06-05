# -*- coding: utf-8 -*-
# 1 : imports of python lib
import json
import logging

# 2 : imports of odoo
from odoo import _, api, exceptions, fields, models, SUPERUSER_ID  # alphabetically ordered

# 3 : imports from odoo modules

# 4 : variable declarations
_logger = logging.getLogger(__name__)


# UPGRADE
def migrate(cr, version):
    # Change status to new value
    cr.execute("""UPDATE account_move SET l10n_hu_plus_status='other' WHERE l10n_hu_plus_status ='information'""")
    _logger.info("account_move l10n_hu_plus_status information updated to other")
