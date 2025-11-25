from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    bai_validate_api_url = fields.Char(string="BAI Validar Comprovativo URL", config_parameter="bai_payment_proof_validation.bai_validate_api_url")
