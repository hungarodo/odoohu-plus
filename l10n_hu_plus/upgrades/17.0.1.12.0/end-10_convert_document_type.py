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
    # Initialize variables
    env = api.Environment(cr, SUPERUSER_ID, {})
    error_list = []

    # Search document_type_tags
    tags = env['l10n.hu.plus.tag'].search([('tag_type', '=', 'technical')])
    _logger.info("END Tag count: %s", len(tags))

    # Iterate tags
    for tag in tags:
        try:
            technical_data = tag.technical_data
            if technical_data.get('object_type') == 'document_type':
                tag.write({'tag_type': 'document_type'})
                if technical_data.get('account_move_ids'):
                    account_moves = env['account.move'].search([('id', 'in', technical_data['account_move_ids'])])
                    for account_move in account_moves:
                        account_move.write({'l10n_hu_plus_tag': tag.id})
        except Exception as e:
            error_list.append("END tag exception: " + str(tag.id) + " - " + str(e))

    # Log errors
    _logger.info("END Error count: %s", len(error_list))
    _logger.info("END Error list: %s", error_list)

    # Drop temp column
    cr.execute("ALTER TABLE account_move DROP COLUMN l10n_hu_document_type_temp")
    _logger.info("account_move l10n_hu_document_type_temp column dropped")
