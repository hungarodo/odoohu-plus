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
    tags = []

    # Search document_types
    document_types = env['l10n.hu.plus.object'].search([('type_technical_name', '=', 'document_type')])
    _logger.info("POST Document type count: %s", len(document_types))

    # Convert document type objects to tags
    for document_type in document_types:
        _logger.info("POST Converting document_type object: %s", document_type.display_name)
        try:
            # account_moves_ids
            cr.execute("SELECT id FROM account_move WHERE l10n_hu_document_type_temp=%s", [document_type.id])
            account_moves_ids = list(cr.fetchall())
            _logger.info("POST fetch account_moves_ids count: %s", len(account_moves_ids))

            # read_result
            read_result = document_type.read([])

            # technical_data
            technical_data = {
                'account_move_ids': account_moves_ids,
                'object_id': read_result[0]['id'],
                'object_read_result': json.loads(json.dumps(read_result, default=str)),
                'object_type': 'document_type',
            }

            # tag_values
            tag_values = {
                'code': document_type.code,
                'company': document_type.company.id,
                'description': document_type.description,
                'name': document_type.name,
                'tag_type': 'technical',
                'technical_data': technical_data,
                'technical_name': document_type.technical_name,
            }
            # Create tag
            tag = env['l10n.hu.plus.tag'].create(tag_values)
            tags.append(tag)
        except Exception as e:
            error_list.append("POST document_type exception: " + str(document_type.id) + " - " + str(e))

    # Log tag count
    _logger.info("POST Tag count: %s", len(tags))

    # Log errors
    _logger.info("POST Error count: %s", len(error_list))
    _logger.info("POST Error list: %s", error_list)
