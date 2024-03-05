# -*- coding: utf-8 -*-
{
    'name': "HU+ Accounting",  # Name first, others listed in alphabetical order
    'application': False,
    'author': "Online ERP Kft., Oregional Kft.",
    'auto_install': False,
    'category': "Accounting",  # Odoo Marketplace category
    'currency': "EUR",
    'data': [  # Files are processed in the order of listing
        'views/account_fiscal_position_views.xml',
        'views/account_journal_views.xml',
        'views/account_journal_actions.xml',
        'views/account_move_views.xml',
        'views/account_move_actions.xml',
        'views/account_move_line_views.xml',
        'views/account_move_line_actions.xml',
        'views/account_payment_method_views.xml',
        'views/account_payment_method_actions.xml',
        'views/account_payment_term_views.xml',
        'views/account_payment_term_actions.xml',
        'views/account_tag_views.xml',
        'views/account_tag_actions.xml',
        'views/account_tax_views.xml',
        'views/account_tax_actions.xml',
        'views/account_tax_group_actions.xml',
        'views/res_company_views.xml',
        'views/res_partner_views.xml',
        'views/uom_uom_views.xml',
        'data/ir_ui_menu_data.xml',
    ],
    'demo': [],
    'depends': [  # Include only direct dependencies
        'l10n_hu_base',
    ],
    'description': "Hungarian accounting improvements",
    'external_dependencies': {
        'bin': [],
        'python': [],
    },
    'images': [  # Odoo Marketplace banner
        'static/description/l10n_hu_account_invoice_banner.png',
    ],
    'installable': True,
    'license': "OPL-1",
    'price': 0,
    'qweb': [],
    'summary': "Hungarian accounting improvements",
    'test': [],
    'version': "1.0.20",
    'website': "https://wwww.hungarodo.hu/odoohu"
}
