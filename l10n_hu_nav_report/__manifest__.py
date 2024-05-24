# -*- coding: utf-8 -*-
{
    'name': "HU+ NAV Reporting",  # Name first, others listed in alphabetical order
    'application': False,
    'author': "Oregional Kft.",
    'auto_install': False,
    'category': "Extra Tools",  # Odoo Marketplace category
    'currency': "EUR",
    'data': [  # Files are processed in the order of listing
        'data/ir_module_category_data.xml',
        'security/res_groups.xml',
        'security/ir_rule.xml',
        'security/ir.model.access.csv',
        'views/nav_report_views.xml',
        'views/nav_report_actions.xml',
        'views/nav_report_element_views.xml',
        'views/nav_report_element_actions.xml',
        'views/nav_report_input_views.xml',
        'views/nav_report_input_actions.xml',
        'views/nav_report_output_views.xml',
        'views/nav_report_output_actions.xml',
        'views/nav_report_rule_views.xml',
        'views/nav_report_rule_actions.xml',
        'views/nav_report_template_views.xml',
        'views/nav_report_template_actions.xml',
        'wizard/wizard_views.xml',
        'wizard/wizard_actions.xml',
        'data/ir_ui_menu_data.xml',
    ],
    'demo': [],
    'depends': [  # Include only direct dependencies
        'l10n_hu_invoice',
    ],
    'description': "NAV (Hungarian Tax Authority) reporting",
    'installable': True,
    'images': [  # Odoo Marketplace banner
        'static/description/l10n_hu_nav_report_banner.png',
    ],
    'license': "OPL-1",
    'price': 0,
    'qweb': [],
    'summary': "Hungary NAV reporting",
    'version': "1.0.13",
    'website': "https://hungarodo.hu/odoohu",
}
