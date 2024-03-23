# -*- coding: utf-8 -*-
{
    'name': "HU+ Invoicing",  # Name first, others listed in alphabetical order
    'application': False,
    'author': "Online ERP Kft., Oregional Kft.",
    'auto_install': False,
    'category': "Accounting",  # Odoo Marketplace category
    'currency': "EUR",
    'data': [  # Files are processed in the order of listing
        'data/ir_module_category_data.xml',
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'report/report_invoice_document.xml',
        'report/report_invoice_document_template.xml',
        'views/account_journal_views.xml',
        'views/account_move_views.xml',
        'views/invoice_views.xml',
        'views/invoice_actions.xml',
        'views/invoice_line_views.xml',
        'views/invoice_line_actions.xml',
        'views/invoice_link_views.xml',
        'views/invoice_link_actions.xml',
        'views/invoice_log_views.xml',
        'views/invoice_log_actions.xml',
        'views/invoice_product_fee_views.xml',
        'views/invoice_product_fee_actions.xml',
        'views/invoice_summary_views.xml',
        'views/invoice_summary_actions.xml',
        'views/invoice_xml_export_views.xml',
        'views/invoice_xml_export_actions.xml',
        'data/ir_ui_menu_data.xml',
    ],
    'demo': [],
    'depends': [  # Include only direct dependencies
        'l10n_hu_account',
    ],
    'description': "Hungarian invoicing improvements",
    'external_dependencies': {
        'bin': [],
        'python': [],
    },
    'images': [  # Odoo Marketplace banner
        'static/description/l10n_hu_invoice_banner.png',
    ],
    'installable': True,
    'license': "OPL-1",
    'price': 0,
    'qweb': [],
    'summary': "Hungarian invoicing improvements",
    'test': [],
    'version': "1.0.13",
    'website': "https://www.hungarodo.hu/odoohu",
}
