# -*- coding: utf-8 -*-
{
    'name': "HU+ Base",  # Name first, others listed in alphabetical order
    'author': "Online ERP Kft, Oregional Kft.",
    'auto_install': False,
    'category': "Localization",
    'currency': "EUR",
    'data': [  # Files are processed in the order of listing
        'data/ir_actions_act_url_data.xml',
        'data/ir_cron_data.xml',
        'data/ir_module_category_data.xml',
        'security/res_groups.xml',
        'security/ir_rule.xml',
        'security/ir.model.access.csv',
        'views/document_type_views.xml',
        'views/document_type_actions.xml',
        'views/ir_config_parameter_actions.xml',
        'views/ir_cron_actions.xml',
        'views/ir_module_module_actions.xml',
        'views/log_views.xml',
        'views/log_actions.xml',
        'views/object_views.xml',
        'views/object_actions.xml',
        'views/product_product_actions.xml',
        'views/res_company_views.xml',
        'views/res_partner_views.xml',
        'views/res_partner_actions.xml',
        'views/tag_views.xml',
        'views/tag_actions.xml',
        'wizard/wizard_views.xml',
        'wizard/wizard_actions.xml',
        'wizard/wizard_line_views.xml',
        'data/ir_ui_menu_data.xml',
    ],
    'demo': [],
    'depends': [  # Include only direct dependencies
        'l10n_hu',
    ],
    'description': "Hungarian localization base improvements",
    'images': [  # Odoo Marketplace banner
        'static/description/l10n_hu_base_banner.png',
    ],
    'installable': True,
    'license': "OPL-1",
    'price': 0,
    'summary': "Hungarian localization",
    'test': [],
    'version': "1.0.18",
    'website': "https://wwww.hungarodo.hu/odoohu",
}
