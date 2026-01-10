{
    'name': 'BAI Payment Validation',
    'version': '1.0',
    'summary': 'Summary Bai payment validation',
    'description': """ """,
    'author': 'Jardel Elias Bernardo',
    'website': 'https://github.com/JardelLion',
    'depends': ['purchase', 'sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'views/bai_receipt_views.xml'
    ],

   # "images": "static/description/icon.svg",
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
