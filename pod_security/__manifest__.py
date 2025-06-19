{
    'name': 'POD Security',
    'version': '1.0',
    'summary': 'Modul keamanan untuk POD',
    'description': 'Menambahkan fitur keamanan seperti CSP dan pengelolaan CSRF token yang aman',
    'category': 'Custom',
    'author': 'awartono.01@erajaya.com',
    'website': 'https://www.erajaya.com',
    'depends': ['base', 'web', 'pod_base'],
    'data': [
        'views/assets.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'pod_security/static/src/js/csrf_token_manager.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': True,
    'license': 'LGPL-3',
}