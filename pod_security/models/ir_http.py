from odoo import models

class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'
    
    @classmethod
    def _get_default_csp(cls):
        csp = super()._get_default_csp() if hasattr(super(), '_get_default_csp') else {}
        csp.update({
            'default-src': ["'self'"],
            'script-src': ["'self'", "'unsafe-inline'", "'unsafe-eval'"],
            'style-src': ["'self'", "'unsafe-inline'"],
            'font-src': ["'self'", "data:"],
            'img-src': ["'self'", "data:"],
            'connect-src': ["'self'"],
            'form-action': ["'self'"],
            'frame-ancestors': ["'self'"],
            'object-src': ["'none'"],
            'base-uri': ["'self'"],
            'frame-src': ["'self'"],
            'worker-src': ["'self'"],
            'manifest-src': ["'self'"],
            'media-src': ["'self'"]
        })
        return csp
    
    @classmethod
    def _get_csp_policy(cls):
        # Dapatkan kebijakan CSP default dari Odoo 17
        csp_policy = super()._get_csp_policy()
        
        # Tambahkan atau modifikasi direktif yang diperlukan
        csp_policy.update({
            'form-action': "'self'",
            'frame-ancestors': "'self'",
            'object-src': "'none'",
            'base-uri': "'self'",
            'script-src': csp_policy.get('script-src', ["'self'"]) + ["'unsafe-inline'", "'unsafe-eval'"],
            'style-src': csp_policy.get('style-src', ["'self'"]) + ["'unsafe-inline'"],
        })
        
        return csp_policy
    
    @classmethod
    def _post_dispatch(cls, response):
        response = super()._post_dispatch(response)
        if response is None:
            return
        
        # Tambahkan header CSP
        csp = cls._get_default_csp()
        if csp:
            header_value = '; '.join(
                '%s %s' % (directive, ' '.join(values))
                for directive, values in csp.items()
            )
            response.headers['Content-Security-Policy'] = header_value
            
            # Tambahkan header keamanan lainnya
            response.headers['X-Content-Type-Options'] = 'nosniff'
            response.headers['X-Frame-Options'] = 'SAMEORIGIN'
            response.headers['X-XSS-Protection'] = '1; mode=block'
            
        return response